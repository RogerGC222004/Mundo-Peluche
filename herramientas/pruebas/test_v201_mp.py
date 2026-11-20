# v201: dos jugadores de verdad en una sala: gestos, lengua (con giro de cabeza), globos de pintura y boca 3D del Chibi se ven en el otro.
import asyncio, re, sys, json, os
os.chdir('/tmp/claude-0/-home-claude/71ba1456-fe89-5ecb-af02-76c832933a55/scratchpad')
exec(open('test_book_mp.py').read().split('async def m():')[0])
page_html=page_html.replace("function wiMapDraw(g){","window.__G=s=>eval(s); function wiMapDraw(g){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); ctx=await b.new_context(viewport={"width":500,"height":300}); await ctx.add_init_script("window.__NOR=true; localStorage.setItem('mundoPelucheEnLinea','{\"on\":true,\"tip\":true}'); ")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=page_html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await ctx.route("https://**/*", route)
    A,ea=await open_game(ctx,'Ana'); await A.evaluate("document.getElementById('mpCreate').click()"); await A.wait_for_timeout(500)
    code=re.search(r'Código (\w{6})', await A.text_content('#roomDiag')).group(1)
    B,eb=await open_game(ctx,'Beto'); await B.wait_for_selector('#mpCode',state='visible',timeout=120000); await B.fill('#mpCode',code,timeout=120000); await B.evaluate("document.getElementById('mpJoin').click()"); await B.wait_for_timeout(2500)
    G=lambda P,s: P.evaluate("s=>{ try{ const v=__G(s); return JSON.stringify(v===undefined?null:v); }catch(e){ return 'ERR '+e; } }", s)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t)
    R="(()=>{ for(let i=0;i<8;i++) updateRemotes(.05,performance.now()/1000+i*.05); return [...mp.remotes.values()][0]; })()"
    U="for(let i=0;i<6;i++) update(.05,performance.now()/1000+i*.05);"
    # 1) bailecito
    print('A baila', await G(A,U+"wardrobe.own.push('ge_baile'); playGesture('baile'); sendPresence(true); [!!plush.userData.gs, mp.presBytes]"))
    await B.wait_for_timeout(1500); r=json.loads(await G(B,"(()=>{ const r="+R+"; const gs=r.obj.userData.gs; return [gs&&gs.id, r.geKey]; })()")); ok(r[0]=='baile','B ve el bailecito de A %s'%r)
    # 2) lengua con la cámara fija y la cabeza girada
    print('A lengua', await G(A,U+"plush.userData.gs&&gEnd(plush); wardrobe.own.push('ge_lengua'); playGesture('lengua'); "+U+U+"TGCAM.on=true; look(-150,0,.005); "+U+"sendPresence(true); [!!plush.userData.tg, JSON.stringify(tgHeadPresence())]"))
    await B.wait_for_timeout(1500); r=json.loads(await G(B,"(()=>{ const r="+R+"; for(let i=0;i<40;i++) tongueTick(r.obj,.05,false); const tg=r.obj.userData.tg; return [!!tg, tg&&tg.e, tg&&+tg.hy.toFixed(2)]; })()")); ok(r[0] and r[1]==1 and r[2]>.5,'B ve la lengua de A y su cabeza girada %s'%r)
    print('A guarda la lengua', await G(A,"playGesture('lengua'); TGCAM.on=false; sendPresence(true); plush.userData.tg.want"))
    await B.wait_for_timeout(1500); r=json.loads(await G(B,"(()=>{ const r="+R+"; for(let i=0;i<40;i++) if(r.obj.userData.tg) tongueTick(r.obj,.05,false); return !r.obj.userData.tg; })()")); ok(r,'B ve que A la guardó %s'%r)
    # 3) globo de pintura
    print('A lanza', await G(A,U+U+U+U+"PBALL.last=0; throwPaint('estrella'); [PBALL.fly.length, JSON.stringify(paintPresence())]"))
    await B.wait_for_timeout(1500); r=json.loads(await G(B,"(()=>{ const r="+R+"; const a=PBALL.fly.length; for(let i=0;i<60;i++) paintTick(.05); return [a, PBALL.splats.length]; })()")); ok(r==[1,1],'B ve el globo de A volar y la mancha %s'%r)
    # 4) Chibi con boca 3D
    print('A chibi', await G(A,"shopPick(SHOP_BY.av_chibi); wardrobe.own.push('bo_risa'); shopPick(SHOP_BY.bo_risa); shopFlush(); closeShop&&0; sendPresence(true); [plush.userData.av, plush.userData.ch.m3Kind, mp.presBytes]"))
    await B.wait_for_timeout(1500); r=json.loads(await G(B,"(()=>{ const r="+R+"; const C=r.obj.userData.ch; return [r.obj.userData.av, C&&C.m3Kind, C&&C.hairStyle!==undefined]; })()")); ok(r[0]=='c' and r[1]=='risa','B ve al Chibi de A con su boca abierta 3D %s'%r)
    r=json.loads(await G(A,"(()=>{ playGesture('aplaudir'); return JSON.stringify({ge:gestPresence(), hd:tgHeadPresence(), pb:paintPresence()}).length; })()")); ok(r<200,'lo nuevo en la presencia es poquito: %s bytes'%r)
    print('errores', ea[:3], eb[:3]); await b.close()
asyncio.run(m())
