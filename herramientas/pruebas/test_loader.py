import asyncio, time
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read()
async def run(b, vp, three_ok=True, tag=''):
  pg=await b.new_page(viewport={"width":vp[0],"height":vp[1]}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
  async def route(r):
    if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
    elif "three" in r.request.url:
      if three_ok: await asyncio.sleep(1.5); await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    elif "fonts.g" in r.request.url: await r.abort()
    else: await r.abort()
  await pg.route("https://**/*", route); t0=time.time(); await pg.goto("https://test.local/", wait_until='commit')
  await pg.wait_for_selector('#loader', timeout=60000); await pg.wait_for_timeout(700)
  await pg.screenshot(path=f'ld_{tag}_a.png', timeout=150000)
  if three_ok:
    seen=[]
    for i in range(80):
      st=await pg.evaluate("(()=>{ const s=document.getElementById('ldStep'); return s?s.textContent:'(sin cargador)'; })()")
      if not seen or seen[-1]!=st: seen.append(st)
      if st=='(sin cargador)': break
      await pg.wait_for_timeout(250)
    print(tag,'pasos',seen,'segundos',round(time.time()-t0,1), 'ms por cuadro', await pg.evaluate("window.__ldFrameMs"))
    await pg.wait_for_timeout(1500); await pg.screenshot(path=f'ld_{tag}_b.png', timeout=150000)
  else:
    await pg.wait_for_timeout(3000); await pg.screenshot(path=f'ld_{tag}_err.png', timeout=150000)
    print(tag,'error visible', await pg.evaluate("[!document.getElementById('ldErr').hidden, document.getElementById('ldErrMsg').textContent]"))
  print(tag,'errores', errs[:3]); await pg.close()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    await run(b,(740,360),True,'tel'); await run(b,(1280,720),True,'pc'); await run(b,(740,360),False,'sin3d')
    await b.close()
asyncio.run(m())
