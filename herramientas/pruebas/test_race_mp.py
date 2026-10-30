import asyncio, re, sys, json
exec(open('test_fair.py').read().split('which=sys.argv')[0])
page_html=page_html.replace('  renderer.render(scene,camera);\n  fpsFrames++','  if(!window.__NOR) renderer.render(scene,camera);\n  fpsFrames++').replace('if(shopOpen()) renderStudio(dt); else renderer.render(scene,camera);','if(window.__NOR){} else if(shopOpen()) renderStudio(dt); else renderer.render(scene,camera);')
page_html=page_html.replace("  if(shopOpen()) renderStudio(dt); else renderer.render(SP.on","  if(window.__NOR){} else if(shopOpen()) renderStudio(dt); else renderer.render(SP.on")
REAL=open('threerepo/build/three.min.js').read()
page_html=page_html.replace('var arenaReady=true;','var arenaReady=true; window.__AR={RC, rcW, AR, AR_SPOTS, PLAT, BOLA, PAPA, join:a=>arJoin(a), get remotes(){return mp.remotes}, myUid, terrainH};')
A_IDX=3
STATE="""(()=>{ const R=window.__AR, me=R.AR.me, G=R.AR.G[%d]; const P=__P(); return JSON.stringify({me:[me.a,me.st], ph:G.ph, ms:Math.round(G.ms), pl:G.pl.length, el:G.el.length, h:G.h===R.myUid?'YO':(G.h?'otro':null), lead:R.AR.lead[%d], pos:[+P.pos.x.toFixed(1),+P.pos.y.toFixed(1),+P.pos.z.toFixed(1)], hud:document.getElementById('arTxt').textContent, res:document.getElementById('arRes').hidden?'':document.getElementById('arResTitle').textContent+' '+document.getElementById('arResCoins').textContent, removed:R.PLAT.removed.reduce((a,b)=>a+b,0)}); })()"""%(A_IDX,A_IDX)
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
    for n in ['Beto','Caro']:
      X,ex=await open_game(ctx,n); await X.fill('#mpCode',code); await X.evaluate("document.getElementById('mpJoin').click()"); await X.wait_for_timeout(1200); pages.append(X); errs.append(ex)
    # todos a la placa y unirse con el botón
    for X in pages:
      await X.evaluate(f"(()=>{{ const R=window.__AR, A=R.AR_SPOTS[{A_IDX}], [x,z]=A.plate; __P().pos.set(x,R.terrainH(x,z)+.05,z); return 1; }})()")
    await A.wait_for_timeout(600)
    print('botón:', await A.evaluate("document.getElementById('act1').textContent"))
    for X in pages: await X.evaluate("document.getElementById('act1').click()")
    fin_done=set()
    for step in range(80):
      await A.wait_for_timeout(1000)
      ss=[json.loads(await X.evaluate(STATE)) for X in pages]
      if step%3==0 or ss[0]['ph']==4: print(step, ' | '.join(f"{s['me']} ph{s['ph']} {s['ms']} pl{s['pl']} el{s['el']} h{s['h']} L{int(s['lead'])} y{s['pos'][1]} rm{s['removed']} '{s['hud']}' {s['res']}" for s in ss))
      if A_IDX==1 and ss[0]["ph"]==3 and step<26:
        # el que tiene la papa persigue a otro
        for i,X in enumerate(pages):
          if ss[i]['h']=='YO':
            j=(i+1)%3; await X.evaluate(f"(()=>{{ const R=window.__AR; const o=[...R.remotes.values()].find(r=>r.az&&r.az[1]===2); if(o){{ __P().pos.x=o.pos.x+.5; __P().pos.z=o.pos.z; }} return 1; }})()")
            break
      if ss[0]['ph']==3 and 'a' not in fin_done:
        fin_done.add('a'); await pages[0].evaluate("(()=>{ const R=window.__AR, q=R.rcW(390,0,R.RC.Y+.1); __P().pos.copy(q); return 1; })()")
      elif ss[0]['ph']==3 and 'b' not in fin_done:
        fin_done.add('b'); await pages[1].evaluate("(()=>{ const R=window.__AR, q=R.rcW(100,8,R.RC.Y); __P().pos.copy(q); return 1; })()")
      elif ss[0]['ph']==3 and 'c' not in fin_done and step>25:
        fin_done.add('c'); await pages[2].evaluate("(()=>{ const R=window.__AR, q=R.rcW(392,1,R.RC.Y+.1); __P().pos.copy(q); return 1; })()")
      if A_IDX==2 and ss[0]['ph']==3 and step%2==0:
        await pages[1].evaluate("(()=>{ window.__AR.BOLA.v.set(6,0); return 1; })()")
      if any(s['res'] for s in ss) and step>5: 
        await A.wait_for_timeout(1500); ss=[json.loads(await X.evaluate(STATE)) for X in pages]; print('FIN', [s['res'] for s in ss], [s['me'] for s in ss]); break
    await A.wait_for_timeout(8000)
    ss=[json.loads(await X.evaluate(STATE)) for X in pages]; print('después', [(s['me'],s['ph'],s['pos']) for s in ss])
    print('errores:', [e[:3] for e in errs]); await b.close()
asyncio.run(m())
