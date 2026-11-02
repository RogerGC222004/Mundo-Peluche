import asyncio, base64
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
pre='<script>const _raf=window.requestAnimationFrame.bind(window); window.requestAnimationFrame=f=>window.__stop?0:_raf(f);</script>'
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+pre+open('/home/claude/mundo-peluche.html').read()
html=html.replace("function frame(){","window.__B={BL, blEnter, P:()=>player, plush, camera, scene, renderer, touchHold, stick, update, canvas}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":640,"height":360}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false}))")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__B", timeout=120000); await pg.wait_for_timeout(2500)
    await pg.evaluate("document.getElementById('playBtn').click()"); await pg.wait_for_timeout(1500); await pg.evaluate("window.__stop=true"); await pg.wait_for_timeout(300)
    for k,(up,fw,n) in enumerate([(1,0,140),(1,1,120),(0,1,80)]):
      d=await pg.evaluate(f"""(()=>{{ const B=__B, b=B.BL[3], P=B.P(); if(!P.balloon){{ P.pos.set(b.x+1.2,b.y,b.z); B.blEnter(b); }}
        B.touchHold.up={'true' if up else 'false'}; B.stick.y={-1 if fw else 0}; let t=200+{k}*10; for(let i=0;i<{n};i++){{ t+=.033; B.update(.033,t); }} B.touchHold.up=false; B.stick.y=0;
        const C=B.camera; C.position.set(b.x+7,b.y+5,b.z+9); C.lookAt(b.x,b.y+2.5,b.z); C.updateMatrixWorld(true); B.renderer.info.reset(); B.renderer.render(B.scene,C);
        return [B.canvas.toDataURL('image/png'), [b.x,b.y,b.z].map(v=>+v.toFixed(1)), b.g.position.toArray().map(v=>+v.toFixed(1)), B.plush.position.toArray().map(v=>+v.toFixed(1))]; }})()""")
      open(f'bl_vuelo{k}.png','wb').write(base64.b64decode(d[0].split(',')[1])); print('globo', d[1], 'modelo', d[2], 'peluche', d[3])
    print(errs[:3]); await b.close()
asyncio.run(m())
