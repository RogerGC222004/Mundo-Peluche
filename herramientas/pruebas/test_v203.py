# v203: el botón de atajo dice tu gesto desde que abres el juego; tocar «← Menú» cierra la tienda
import asyncio
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("""localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');
      if(!sessionStorage.getItem('x')){ sessionStorage.setItem('x',1); localStorage.setItem('mundoPelucheRopa', JSON.stringify({own:['ge_saludar','ge_lengua'],eq:{},gest:['saludar','lengua'],pint:[]})); }""")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route)
    async def load():
      await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    await load()
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    await ev("openShop(); shopCat='gestos'; renderShop(); 1"); await pg.wait_for_timeout(500)
    await pg.click('#shopAtajo [data-g=lengua]'); await pg.wait_for_timeout(300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    print('en la tienda:', await ev("[gestAtajo(), document.getElementById('tWave').textContent, document.getElementById('tWave').dataset.lbl]"))
    r=await pg.evaluate("(()=>{ const b=document.getElementById('shopBack2').getBoundingClientRect(); return [b.left+b.width/2, b.top+b.height/2]; })()"); await pg.touchscreen.tap(r[0],r[1]); await pg.wait_for_timeout(600)
    ok(await ev("document.getElementById('shop').hidden && !document.getElementById('menu').hidden"), 'tocar «← Menú» cierra la tienda y regresa al menú')
    await ev("startGame(); 1"); await pg.wait_for_timeout(1500)
    print('jugando:', await ev("[gestAtajo(), document.getElementById('tWave').textContent, getComputedStyle(document.getElementById('tWave')).display]"))
    await load(); await ev("startGame(); 1"); await pg.wait_for_timeout(1500)
    r=await ev("[gestAtajo(), document.getElementById('tWave').textContent, JSON.stringify(wardrobe.atajo)]"); ok(r[1]=='Sacar', 'al volver a abrir el juego el botón de atajo dice tu gesto %s'%r)
    ok(not errs, 'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
