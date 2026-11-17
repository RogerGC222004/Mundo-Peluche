# v205: Jugar abre los modos de juego; Un jugador empieza; Multijugador abre las salas; los demás dicen «pronto»; Volver regresa
import asyncio
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, device_scale_factor=2); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    vis=lambda i: pg.evaluate("i=>{ const e=document.getElementById(i); return !!e && !!(e.offsetWidth||e.offsetHeight); }", i)
    async def tap(i):
      r=await pg.evaluate("i=>{ const b=document.getElementById(i).getBoundingClientRect(); return [b.left+b.width/2,b.top+b.height/2]; }", i); await pg.touchscreen.tap(r[0],r[1]); await pg.wait_for_timeout(500)
    ok(await vis('playBtn') and not await vis('mpBtn'), 'menú principal: Jugar sí, Multijugador ya no')
    await tap('playBtn'); r=[await vis(i) for i in ['soloBtn','mpBtn','mgBtn','freeBtn','mapBtn','modesBack','shopBtn']]
    ok(r==[True]*6+[False], 'al tocar Jugar salen los 5 modos y Volver %s'%r)
    await pg.screenshot(path='/tmp/v205_modos.png')
    r=await pg.evaluate("(()=>{ const b=[...document.querySelectorAll('#menuModes .btn')].map(e=>e.getBoundingClientRect()); return Math.max(...b.map(x=>x.bottom))<=innerHeight && Math.max(...b.map(x=>x.right))<=innerWidth; })()")
    ok(r, 'los botones caben en la pantalla del teléfono acostado')
    await tap('mapBtn'); ok(await vis('mapItems'), 'Crear mapa abre «Mis mapas» (v209)'); await tap('mapBack')
    await tap('mgBtn'); await pg.wait_for_timeout(800); ok(await vis('mgqBack'), 'Minijuegos abre la lista (v206)'); await pg.screenshot(path='/tmp/v206_lista.png'); await tap('mgqBack')
    await tap('modesBack'); ok(await vis('playBtn') and await vis('shopBtn') and not await vis('soloBtn'), 'Volver regresa al menú principal')
    await tap('playBtn'); await tap('mpBtn'); ok(await pg.evaluate("s=>__T.ev(s)","(()=>{ const o=document.getElementById('mp'); return !!o && !o.hidden; })()"), 'Multijugador abre las salas')
    await pg.evaluate("s=>__T.ev(s)","(ui('mpBack').click(), menuModes(true), 1)"); await tap('soloBtn'); await pg.wait_for_timeout(800)
    ok(await pg.evaluate("s=>__T.ev(s)","state==='play' && document.getElementById('menuModes').hidden"), 'Un jugador empieza el juego (y el menú queda listo en el principal)')
    ok(not errs,'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
