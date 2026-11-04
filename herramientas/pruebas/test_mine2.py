import asyncio, sys, base64, io
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw
REAL=open('threerepo/build/three.min.js').read()
pre='<script>window.__off=0; const _dn=Date.now.bind(Date); Date.now=()=>_dn()+window.__off; const _raf=window.requestAnimationFrame.bind(window); window.requestAnimationFrame=f=>window.__stop?0:_raf(f);</script>'
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+pre+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":480,"height":300}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'high', qDef:1, hints:false, weather:false, shadows:true})); localStorage.setItem('mundoPelucheMina', JSON.stringify({pick:4, open:[true,true,true,true,true], ores:{}, veins:{}}))")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=120000); await pg.wait_for_timeout(2000)
    await pg.evaluate("document.getElementById('playBtn').click()"); await pg.wait_for_timeout(1500)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    await ev("(()=>{ const n=Date.now(); const cur=((n/1000)%DAY_LEN)/DAY_LEN; window.__off+=(("+sys.argv[1]+"-cur)*DAY_LEN*1000); window.__stop=true; return 1; })()"); await pg.wait_for_timeout(300)
    shots=[]
    async def run(sec):
      for i in range(int(sec/.05)): await ev("update(.05,performance.now()/1000)")
    async def shot(lab):
      d=await ev("(()=>{ updateSky(.05); updateRemotes(.016,performance.now()/1000); caveUpdate(.016,performance.now()/1000); renderer.render(scene,camera); return canvas.toDataURL('image/png'); })()")
      im=Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB'); ImageDraw.Draw(im).text((4,4),lab,fill=(255,255,0)); shots.append(im)
    for js,lab in eval(sys.argv[2]):
      await ev(js); await run(.8); await shot(lab)
    print('draw calls', await ev("(()=>{ renderer.info.reset(); renderer.render(scene,camera); return [renderer.info.render.calls, renderer.info.render.triangles]; })()"))
    print('errores', errs[:5])
    w,h=shots[0].size; cols=3; rows=(len(shots)+cols-1)//cols; c=Image.new('RGB',(w*cols,h*rows))
    for i,im in enumerate(shots): c.paste(im,((i%cols)*w,(i//cols)*h))
    c.save(sys.argv[3]); await b.close()
asyncio.run(m())
