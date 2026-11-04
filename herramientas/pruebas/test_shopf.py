import asyncio, sys
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":int(sys.argv[1]),"height":int(sys.argv[2])}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheRopa', JSON.stringify({own:['go_roja','hn_rana_verde'],eq:{hat:'go_roja'}}))")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=120000); await pg.wait_for_timeout(1500)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    await ev("coins=60; openShop(); shopCat='gorras'; renderShop(); 1"); await pg.wait_for_timeout(500)
    st=lambda: pg.evaluate("[document.getElementById('shopCount').textContent, [...document.querySelectorAll('#shopGrid .shop-item .nm')].slice(0,6).map(e=>e.textContent), document.querySelectorAll('#shopGrid .nw').length, [...document.querySelectorAll('.shop-tab .tnw')].length]")
    print('inicio', await st())
    await pg.fill('#shopSearch','rojo'); await pg.wait_for_timeout(300); print('rojo', await st())
    await pg.fill('#shopSearch','sombrero vaquero'); await pg.wait_for_timeout(300); print('vaquero', await st())
    await pg.fill('#shopSearch',''); await pg.click('[data-f=new]'); await pg.wait_for_timeout(300); print('nuevo', await st())
    await pg.click('[data-f=new]'); await pg.click('[data-f=mine]'); await pg.wait_for_timeout(300); print('mio', await st())
    await pg.click('[data-f=afford]'); await pg.wait_for_timeout(300); print('alcanza', await st())
    await ev("shopCat='mascotas'; renderShop(); 1"); print('mascotas alcanza', await st())
    await pg.click('[data-f=afford]'); await pg.fill('#shopSearch','zzz'); await pg.wait_for_timeout(300); print('nada', await st(), await pg.evaluate("document.querySelector('.shop-empty')&&document.querySelector('.shop-empty').textContent"))
    await pg.fill('#shopSearch',''); await ev("shopCat='gorras'; renderShop(); 1"); await pg.wait_for_timeout(500)
    await pg.screenshot(path='shopf_%s.png'%sys.argv[1])
    print('errores', errs[:3]); await b.close()
asyncio.run(m())
