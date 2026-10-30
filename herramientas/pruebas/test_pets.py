import asyncio, json, base64
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read()
html=html.replace("function frame(){","window.__P={pets, PETS, myPet, P:()=>player, cam:camera, show, step:(n,fn)=>{ for(let i=0;i<n;i++){ window.__tt=(window.__tt||100)+.033; if(fn) fn(i); update(.033,window.__tt); petsUpdate(.033,window.__tt); } }, petPresence, renderer, scene}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    pg=await b.new_page(viewport={"width":900,"height":500}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheMonedas','500'); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false}))")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__P", timeout=120000); await pg.wait_for_timeout(1500)
    print('errs carga', errs[:3])
    await pg.evaluate("document.getElementById('shopBtn').click()"); await pg.wait_for_timeout(600)
    await pg.evaluate("[...document.querySelectorAll('#shopTabs button')].find(b=>b.textContent.includes('Mascotas')).click()"); await pg.wait_for_timeout(400)
    n=await pg.evaluate("document.querySelectorAll('#shopGrid .shop-item').length"); print('mascotas en tienda', n)
    await pg.evaluate("document.querySelectorAll('#shopGrid .shop-item')[5].click()"); await pg.wait_for_timeout(1500)
    await pg.screenshot(path='pet_shop_try.png', timeout=150000)
    print('barra', await pg.evaluate("[document.getElementById('shopBuy').hidden, document.getElementById('shopBuyTxt').textContent, document.getElementById('shopBuyBtn').textContent]"))
    await pg.evaluate("document.getElementById('shopBuyBtn').click()"); await pg.wait_for_timeout(500)
    print('comprada', await pg.evaluate("[JSON.stringify(__P.pets), localStorage.getItem('mundoPelucheMonedas'), document.getElementById('shopPetName').hidden]"))
    await pg.fill('#petNameIn','Toby'); await pg.evaluate("document.getElementById('petNameBtn').click()"); await pg.wait_for_timeout(1200)
    print('nombre', await pg.evaluate("[JSON.stringify(__P.pets.names), JSON.stringify(__P.petPresence()), localStorage.getItem('mundoPelucheMascotas')]"))
    await pg.screenshot(path='pet_shop_own.png', timeout=150000)
    await pg.evaluate("document.getElementById('shopBack').click()"); await pg.wait_for_timeout(300)
    await pg.evaluate("document.getElementById('playBtn').click()"); await pg.wait_for_timeout(1500)
    # caminar: mover al jugador hacia adelante
    r=await pg.evaluate("""(()=>{ const P=__P.P(); const out=[]; const p0=P.pos.clone();
      __P.step(60,i=>{ P.pos.x+=0.12; P.facing=Math.PI/2; });
      const m=__P.myPet.inst; out.push(['tras caminar', +P.pos.x.toFixed(2), +m.x.toFixed(2), +m.z.toFixed(2), +Math.hypot(m.x-P.pos.x,m.z-P.pos.z).toFixed(2), m.P.root.visible, m.name]);
      __P.step(40); out.push(['quieto', +Math.hypot(m.x-P.pos.x,m.z-P.pos.z).toFixed(2), +m.y.toFixed(2), +P.pos.y.toFixed(2)]);
      P.pos.x+=60; __P.step(2); out.push(['teletransporte', +Math.hypot(m.x-P.pos.x,m.z-P.pos.z).toFixed(2)]);
      return out; })()""")
    for x in r: print(x)
    await pg.evaluate("""(()=>{ const P=__P.P(), m=__P.myPet.inst, c=__P.cam; __P.show('pause'); document.getElementById('pause').hidden=true; c.position.set(m.x+2.4,m.y+1.6,m.z+2.6); c.lookAt(m.x,m.y+.5,m.z); })()""")
    await pg.wait_for_timeout(1500); await pg.screenshot(path='pet_world.png', timeout=150000)
    print('errores', errs[:5]); await b.close()
asyncio.run(m())
