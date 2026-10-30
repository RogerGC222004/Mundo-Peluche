import asyncio, json, sys
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read()
html=html.replace("const iRideCuco=","window.__CU=CU; window.__P=()=>player; window.__acts=()=>[actA&&actA.label, actB&&actB.label]; window.__keys=keys; window.__step=n=>{ for(let i=0;i<n;i++){ cucoUpdate(.05,i*.05); } return [CU.x,CU.y,CU.z,CU.v,CU.wet,CU.h,terrainH(CU.x,CU.z)].map(v=>typeof v==='number'?+v.toFixed(2):v); }; window.__cam=camera; window.__show=show; const iRideCuco=",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":720,"height":400}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__CU", timeout=120000); await pg.wait_for_timeout(3000)
    await pg.evaluate("document.getElementById('playBtn').click()"); await pg.wait_for_timeout(1500)
    await pg.evaluate("(()=>{ const C=__CU, P=__P(); P.pos.set(C.x+Math.cos(C.h)*7.5, 0.2, C.z-Math.sin(C.h)*7.5); })()"); await pg.wait_for_timeout(800)
    await pg.keyboard.press('KeyE'); await pg.wait_for_timeout(2500)
    print('montado', await pg.evaluate("JSON.stringify(__P().pg)"))
    # dar la vuelta (hacia el mar) y avanzar
    print('gira', await pg.evaluate("__keys.KeyA=true; const r=__step(80); __keys.KeyA=false; JSON.stringify(r)"))
    print('avanza', await pg.evaluate("__keys.KeyW=true; JSON.stringify(__step(200))"))
    print('avanza', await pg.evaluate("JSON.stringify(__step(300))"))
    print('avanza', await pg.evaluate("__keys.KeyW=false; JSON.stringify(__step(60))"))
    await pg.wait_for_timeout(2500); await pg.screenshot(timeout=150000, path='cuco_sea.png')
    print('jinete', await pg.evaluate("JSON.stringify(__P().pos.toArray().map(v=>+v.toFixed(1)))"))
    await pg.keyboard.press('KeyE'); await pg.wait_for_timeout(1500)
    print('bajado', await pg.evaluate("JSON.stringify([__P().pg, __P().swim, __P().pos.toArray().map(v=>+v.toFixed(1)), __acts()])"))
    await pg.wait_for_timeout(1500); await pg.screenshot(timeout=150000, path='cuco_swim.png')
    # vuelta a subir nadando
    await pg.keyboard.press('KeyE'); await pg.wait_for_timeout(2500)
    print('resubido', await pg.evaluate("JSON.stringify([__P().pg, __P().swim])"))
    print('a tierra', await pg.evaluate("__keys.KeyS=true; const a=__step(10); __keys.KeyS=false; __keys.KeyD=true; __step(80); __keys.KeyD=false; __keys.KeyW=true; const r=__step(600); __keys.KeyW=false; JSON.stringify(r)"))
    await pg.wait_for_timeout(2500); await pg.screenshot(timeout=150000, path='cuco_land.png')
    await pg.keyboard.press('KeyM'); await pg.wait_for_timeout(2500); await pg.screenshot(timeout=150000, path='cuco_map.png')
    print('errores', errs[:5]); await b.close()
asyncio.run(m())
