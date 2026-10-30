import asyncio, re, sys, json
exec(open('test_fair.py').read().split('which=sys.argv')[0])
page_html=page_html.replace('  renderer.render(scene,camera);\n  fpsFrames++','  if(!window.__NOR) renderer.render(scene,camera);\n  fpsFrames++').replace('if(shopOpen()) renderStudio(dt); else renderer.render(scene,camera);','if(window.__NOR){} else if(shopOpen()) renderStudio(dt); else renderer.render(scene,camera);')
REAL=open('threerepo/build/three.min.js').read()
page_html=page_html.replace('// presencia: en qué minijuego estoy (y datos del hockey)','window.__S={SP, MOON, enterSpace, exitSpace, get remotes(){return mp.remotes}, spaceBite:()=>spaceBite(), spaceScene, plantFlag, bookPlanets, get flags(){return flags}, MOONf:()=>MOON.flagMeshes&&MOON.flagMeshes.length, speciesOf, markSeen, coins:()=>coins};\n// presencia: en qué minijuego estoy (y datos del hockey)',1)
page_html=page_html.replace('var arenaReady=true;','var arenaReady=true; window.__AR={AR, AR_SPOTS, PLAT, BOLA, PAPA, join:a=>arJoin(a), get remotes(){return mp.remotes}, myUid, terrainH};')
A_IDX=int(sys.argv[1]) if len(sys.argv)>1 else 0
STATE="""(()=>{ const R=window.__AR, me=R.AR.me, G=R.AR.G[%d]; const P=__P(); return JSON.stringify({me:[me.a,me.st], ph:G.ph, ms:Math.round(G.ms), pl:G.pl.length, el:G.el.length, h:G.h===R.myUid?'YO':(G.h?'otro':null), lead:R.AR.lead[%d], pos:[+P.pos.x.toFixed(1),+P.pos.y.toFixed(1),+P.pos.z.toFixed(1)], hud:document.getElementById('arTxt').textContent, res:document.getElementById('arRes').hidden?'':document.getElementById('arResTitle').textContent+' '+document.getElementById('arResCoins').textContent, removed:R.PLAT.removed.reduce((a,b)=>a+b,0)}); })()"""%(A_IDX,A_IDX)
async def open_game(ctx,name):
  pg=await ctx.new_page(); errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
  await pg.add_init_script(BUS)
  await pg.goto("https://test.local/", timeout=120000); await pg.wait_for_function("typeof window.__S==='object'", timeout=120000); await pg.wait_for_timeout(500)
  for k in range(20):
    await pg.evaluate("document.getElementById('mpBtn').click()"); await pg.wait_for_timeout(700)
    if await pg.is_visible('#mpName'): break
  print(name,'errs',errs[:2]); await pg.wait_for_timeout(800); await pg.evaluate("n=>{ const e=document.getElementById('mpName'); e.value=n; e.dispatchEvent(new Event('input')); }", name)
  return pg, errs
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); ctx=await b.new_context(viewport={"width":500,"height":300}); await ctx.add_init_script("window.__NOR=true;")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=page_html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await ctx.route("https://**/*", route)
    A,ea=await open_game(ctx,'Ana'); await A.evaluate("document.getElementById('mpCreate').click()"); await A.wait_for_timeout(500)
    code=re.search(r'Código (\w{6})', await A.text_content('#roomDiag')).group(1)
    pages=[A]; errs=[ea]
    for n in ['Beto']:
      X,ex=await open_game(ctx,n); await X.wait_for_selector('#mpCode',state='visible',timeout=120000); await X.fill('#mpCode',code,timeout=120000); await X.evaluate("document.getElementById('mpJoin').click()"); await X.wait_for_timeout(1200); pages.append(X); errs.append(ex)
    A,B=pages[0],pages[1]
    for X in (A,B): await X.evaluate("(()=>{ const S=__S; S.enterSpace('walk',{P:S.MOON, d:new THREE.Vector3(0,1,0)}); return 1; })()")
    await A.wait_for_timeout(2500)
    await A.evaluate("(()=>{ __S.SP.face.set(1,0,0); __S.spaceBite(); return 1; })()"); await A.wait_for_timeout(2500)
    print('mordidas A,B:', await A.evaluate("__S.MOON.bites.length"), await B.evaluate("__S.MOON.bites.length"))
    print('B ve a A en el espacio:', await B.evaluate("JSON.stringify([...__S.remotes.values()].map(r=>[r.name, !!r.sp, r.obj.parent===__S.spaceScene, r.obj.visible, r.obj.position.toArray().map(v=>Math.round(v))]))"))
    await A.evaluate("(()=>{ const P=__S.MOON; __S.speciesOf(P).slice(0,2).forEach(q=>__S.markSeen(P,q)); })()")
    await A.evaluate("__S.plantFlag()"); await A.wait_for_timeout(2500)
    print('libro de B:', await B.evaluate("JSON.stringify(__S.bookPlanets().map(e=>[e.P.name,e.who,e.disc,[...e.prog]]))"), 'banderas en la luna (B):', await B.evaluate("__S.MOONf()"))
    print('monedas A:', await A.evaluate("__S.coins()"))
    print('pos A:', await A.evaluate("__S.SP.pos.toArray().map(v=>Math.round(v))"))
    await A.evaluate("__S.exitSpace(true)"); await A.wait_for_timeout(2000)
    print('A volvió; B lo ve:', await B.evaluate("JSON.stringify([...__S.remotes.values()].map(r=>[r.name, !!r.sp, r.obj.parent===__S.spaceScene, r.obj.visible]))"), 'mordidas B', await B.evaluate("__S.MOON.bites.length"))
    print('errores:', [e[:3] for e in errs]); await b.close()
asyncio.run(m())
