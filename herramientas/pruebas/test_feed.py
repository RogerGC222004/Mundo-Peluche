import asyncio, json, sys
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read()
html=html.replace("function pierFallback(){","window.__PI={PIER, CU, cucoMouth, P:()=>player, cam:camera, show, acts:()=>{ actKey=''; scanActions(); return [actA&&actA.label, actB&&actB.label]; }, run:k=>{ const a=k?actB:actA; if(a&&!a.disabled) a.run(); return a&&a.label; }, step:(n)=>{ for(let i=0;i<n;i++){ updateFeed(.05); cucoFeedAnim(.05,i*.05); } }}; function pierFallback(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":720,"height":400}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__PI", timeout=120000); await pg.wait_for_timeout(2500)
    await pg.evaluate("document.getElementById('playBtn').click()"); await pg.wait_for_timeout(1500)
    await pg.evaluate("(()=>{ const C=__PI.CU, P=__PI.P(); P.hand=2; const d=C.B+5.2; P.pos.set(C.x+Math.sin(C.h)*d+Math.cos(C.h)*1.5, 0, C.z+Math.cos(C.h)*d-Math.sin(C.h)*1.5); P.facing=C.h+Math.PI; })()")
    await pg.wait_for_timeout(2500); print('acts', await pg.evaluate("JSON.stringify(__PI.acts())"))
    await pg.evaluate("__PI.run(0)")
    await pg.evaluate("__PI.step(19)")
    await pg.evaluate("__PI.show('pause'); document.getElementById('pause').hidden=true;")
    await pg.evaluate("(()=>{ const C=__PI.CU, cam=__PI.cam, P=__PI.P(); const m=__PI.cucoMouth(); cam.position.set(P.pos.x+Math.cos(C.h)*7, 3.5, P.pos.z-Math.sin(C.h)*7); cam.lookAt((m.x+P.pos.x)/2, 2.2, (m.z+P.pos.z)/2); })()")
    await pg.wait_for_timeout(1500); await pg.screenshot(timeout=120000,path='feed1.png')
    await pg.evaluate("__PI.show('play')"); await pg.evaluate("__PI.step(6)"); await pg.evaluate("__PI.show('pause'); document.getElementById('pause').hidden=true;")
    await pg.evaluate("(()=>{ const C=__PI.CU, cam=__PI.cam, P=__PI.P(); const m=__PI.cucoMouth(); cam.position.set(P.pos.x+Math.cos(C.h)*7, 3.5, P.pos.z-Math.sin(C.h)*7); cam.lookAt((m.x+P.pos.x)/2, 2.2, (m.z+P.pos.z)/2); })()")
    await pg.wait_for_timeout(1500); await pg.screenshot(timeout=120000,path='feed2.png')
    await pg.evaluate("__PI.show('play')"); await pg.evaluate("__PI.step(30)")
    print('después', await pg.evaluate("JSON.stringify([__PI.P().hand, !!__PI.P().feed, __PI.P().busy, document.getElementById('toast').textContent])"))
    print('errores', errs[:5]); await b.close()
asyncio.run(m())
