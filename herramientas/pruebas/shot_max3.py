import asyncio, json, sys, base64
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
pre='<script>window.__off=0; const _dn=Date.now.bind(Date); Date.now=()=>_dn()+window.__off; const _raf=window.requestAnimationFrame.bind(window); window.requestAnimationFrame=f=>window.__stop?0:_raf(f);</script>'
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+pre+open('/home/claude/mundo-peluche.html').read()
html=html.replace("function frame(){","""window.__M={DAY_LEN, P:()=>player, cam:camera, show, FX, sky, weatherNow, renderer, scene, PIER, updateSky, update,
 setP:(p)=>{ const n=Date.now(); const cur=((n/1000)%DAY_LEN)/DAY_LEN; window.__off+=((p-cur)*DAY_LEN*1000); },
 shot:(q,cp,lk)=>{ if(q==="max0"){ q="max"; FX.mDown.uniforms.thr.value=100; } else FX.mDown.uniforms.thr.value=1.0; settings.quality=q; applySettings(); updateSky(.016); for(let i=0;i<3;i++) update(.016, 50+i*.016); camera.position.set(...cp); camera.lookAt(...lk); camera.updateMatrixWorld(); updateSky(.016);
   renderer.info.reset(); const t0=performance.now(); if(FX.on) fxRender(scene,camera); else renderer.render(scene,camera); const gl=renderer.getContext();
   return [canvas.toDataURL('image/png'), gl.getError(), renderer.info.render.calls, performance.now()-t0]; }}; function frame(){""",1)
JOBS=json.loads(sys.argv[1])
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    pg=await b.new_page(viewport={"width":640,"height":360}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); pg.on("console",lambda m: errs.append(m.text) if m.type in('error','warning') else None)
    pg.on("crash", lambda: print("CRASH", flush=True))
    await pg.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'high', qDef:1, hints:false, weather:false}))")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__M", timeout=120000); await pg.wait_for_timeout(1500)
    await pg.evaluate("document.getElementById('playBtn').click()"); await pg.wait_for_timeout(2500)
    await pg.evaluate("window.__stop=true"); await pg.wait_for_timeout(500)
    await pg.evaluate("document.querySelectorAll('#hud,#touch,.hud,#controlsHud').forEach(e=>e.style.visibility='hidden')")
    for name,ph,cam,look,qs in JOBS:
      await pg.evaluate(f"__M.setP({ph})")
      for q in qs:
        r=await pg.evaluate(f"__M.shot('{q}',{json.dumps(cam)},{json.dumps(look)})")
        open(f'mx_{name}_{q}.png','wb').write(base64.b64decode(r[0].split(',')[1])); print(name,q,'glErr',r[1],'calls',r[2],'ms',round(r[3]), flush=True)
    print('errores', errs[:6], flush=True); await b.close()
asyncio.run(m())
