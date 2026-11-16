# v204: con la tabla de surf en la espalda (dos materiales) recolor() tronaba: el aviso «falló vestir al peluche» y antes la tienda no cerraba
import asyncio
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":844,"height":390}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    r=await pg.evaluate("s=>__T.ev(s)", """(()=>{ const id=Object.keys(TBL_BOARDS)[0]; TBL.mine=tblAttach(plush,id,0,null); let err='';
      try{ applyOutfit(plush,wardrobe.eq); recolor(plush,3); }catch(e){ err=e.message; } openShop(); let shut; try{ closeShop(); shut=document.getElementById('shop').hidden; }catch(e){ err+=' cerrar:'+e.message; }
      return [id, !!TBL.mine.parent, err, shut]; })()""")
    print(('BIEN ' if r[2]=='' and r[3] else 'MAL  ')+'con la tabla de surf en la espalda: vestir, cambiar color y salir de la tienda sin error %s'%r, errs[:2]); await b.close()
asyncio.run(m())
