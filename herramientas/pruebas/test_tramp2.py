import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read()
html=html.replace("function frame(){","window.__TR={TR, trDoor, P:()=>player, keys, touchHold, PG, step:(n)=>{ let mx=-9; for(let i=0;i<n;i++){ window.__tt=(window.__tt||100)+.033; update(.033,window.__tt); mx=Math.max(mx,player.pos.y-TR.top); } return +mx.toFixed(2); }, acts:()=>{ actKey=''; scanActions(); return [actA&&actA.label, actB&&actB.label]; }, run:k=>{ const a=k?actB:actA; if(a&&!a.disabled) a.run(); return a&&a.label; }, jump}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":400,"height":250}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__TR", timeout=120000); await pg.wait_for_timeout(2000)
    await pg.evaluate("document.getElementById('playBtn').click()"); await pg.wait_for_timeout(1500)
    await pg.evaluate("(()=>{ const T=__TR.TR, o=__TR.trDoor(T.R+1.6,0); const P=__TR.P(); P.pos.set(o.x, T.base+.1, o.z); })()"); 
    await pg.evaluate("__TR.step(10)"); print('afuera', await pg.evaluate("JSON.stringify(__TR.acts())"))
    await pg.evaluate("__TR.run(0)"); await pg.evaluate("__TR.step(60)")
    print('arriba', await pg.evaluate("JSON.stringify([(__TR.P().pos.y-__TR.TR.top).toFixed(2), __TR.P().busy, Math.hypot(__TR.P().pos.x-__TR.TR.x,__TR.P().pos.z-__TR.TR.z).toFixed(2), __TR.acts()])"))
    await pg.evaluate("__TR.run(0)"); await pg.evaluate("__TR.step(50)"); print('cerrada', await pg.evaluate("JSON.stringify([__TR.TR.open, __TR.TR.k, __TR.acts()])"))
    await pg.evaluate("(()=>{ const T=__TR.TR, P=__TR.P(); P.pos.set(T.x, T.top, T.z); P.vy=0; P.grounded=true; })()"); await pg.evaluate("__TR.step(5)")
    print('salto normal', await pg.evaluate("__TR.jump(); __TR.step(40)"), 'rebote solo', await pg.evaluate("__TR.step(40)"), await pg.evaluate("__TR.step(40)"))
    print('con Saltar sostenido', await pg.evaluate("__TR.jump(); __TR.touchHold.up=true; const a=[]; for(let i=0;i<6;i++) a.push(__TR.step(45)); __TR.touchHold.up=false; JSON.stringify(a)"))
    print('soltar', await pg.evaluate("const a=[]; for(let i=0;i<6;i++) a.push(__TR.step(45)); JSON.stringify(a)"))
    r=await pg.evaluate("(()=>{ const T=__TR.TR, P=__TR.P(); P.pos.set(T.x,T.top,T.z); P.vy=0; P.grounded=true; __TR.jump(); __TR.touchHold.up=true; let mx=0; for(let i=0;i<400;i++){ __TR.step(1); const d=Math.hypot(P.pos.x-T.x,P.pos.z-T.z); if(P.pos.y-T.top>T.NH+.4) { P.pos.x+=.12; } mx=Math.max(mx,d); if(d>T.R+3) break; } __TR.touchHold.up=false; __TR.step(60); return [Math.hypot(P.pos.x-T.x,P.pos.z-T.z).toFixed(2), (P.pos.y-T.base).toFixed(2)]; })()")
    print('salirse por arriba', r)
    r=await pg.evaluate("(()=>{ const T=__TR.TR, P=__TR.P(); P.pos.set(T.x,T.top,T.z); P.vy=0; P.grounded=true; __TR.step(5); for(let i=0;i<150;i++){ P.pos.x+=.1; __TR.step(1); } return [Math.hypot(P.pos.x-T.x,P.pos.z-T.z).toFixed(2)]; })()")
    print('caminando contra la red', r)
    await pg.evaluate("(()=>{ const T=__TR.TR, P=__TR.P(), d=__TR.trDoor(T.R-1.0,T.top); P.pos.set(d.x,T.top,d.z); P.vy=0; P.grounded=true; })()"); await pg.evaluate("__TR.step(10)")
    print('en la puerta', await pg.evaluate("JSON.stringify(__TR.acts())"))
    await pg.evaluate("__TR.run(0)"); await pg.evaluate("__TR.step(50)"); print('abierta', await pg.evaluate("JSON.stringify([__TR.TR.open, __TR.acts()])"))
    await pg.evaluate("__TR.run(1)"); await pg.evaluate("__TR.step(50)")
    print('abajo', await pg.evaluate("JSON.stringify([(__TR.P().pos.y-__TR.TR.base).toFixed(2), __TR.P().busy, Math.hypot(__TR.P().pos.x-__TR.TR.x,__TR.P().pos.z-__TR.TR.z).toFixed(2)])"))
    print('errores', errs[:4]); await b.close()
asyncio.run(m())
