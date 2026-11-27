# v276: sugerencias de los testers: «Califica Mundo Peluche» (Para papás, sin premio) y «¿Quieres salir del juego?» al apretar atrás en el menú de la app.
#  A) primera vez que se abre el juego: no sale ninguna ventanita, solo se guarda la versión
#  B) si antes tenías otra versión: sale «¿Qué hay de nuevo?» una vez; «¡Genial!» la cierra; al volver a abrir ya no sale
#  C) Enviar comentarios: pide la operación de adulto; con la respuesta mala no pasa; con la buena muestra el correo
#     y «Abrir correo» arma mailto: con asunto y versión (web/app), sin datos del jugador
#  D) el arreglo de horizontal está en el script que prepara la app de Android
import asyncio, json, os, re
from playwright.async_api import async_playwright
JUEGO='/home/claude/mundo-peluche.html'
REAL=open('threerepo/build/three.min.js').read()
SRC=open(JUEGO, encoding='utf-8').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+SRC.replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
VER=re.search(r"const GAME_VERSION='(\d+)'",SRC).group(1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
async def abrir(b, pre):
  ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True, user_agent="Mozilla/5.0 (Linux; Android 10) Chrome/120 Mobile")
  pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
  await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1'); window.__fbNoNav=true;\n%s"%(json.dumps(OPTS),pre))
  async def route(r):
    u=r.request.url
    if u.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
    elif "three" in u: await r.fulfill(body=REAL, content_type="application/javascript")
    else: await r.abort()
  await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
  await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
  return pg, errs, ctx
NEWS="(()=>{ const o=document.getElementById('onlineOv'); return !!o && !o.hidden && /hay de nuevo/.test(o.textContent) ? o.textContent : ''; })()"
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    RES=r"""const res=c=>{ const t=c.querySelector('.online-op').textContent; const m=/^([\d ]+) ([+−×÷]) ([\d ]+) =$/.exec(t); const a=+m[1].replace(/ /g,''), z=+m[3].replace(/ /g,'');
        return m[2]==='+'?a+z: m[2]==='−'?a-z: m[2]==='×'?a*z: a/z; };"""
    # web
    pg,errs,ctx=await abrir(b,"localStorage.setItem('mundoPelucheNovedades','%s');"%VER)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await pg.wait_for_timeout(2500)
    r=await ev(r"""(async()=>{ const T=()=>new Promise(r=>setTimeout(r,80)); const OV=()=>document.getElementById('onlineOv'); const o={}; %s
      ui('options').hidden=false; await T(); const b=ui('optRate'); o.vis=b.getClientRects().length>0 && /Para papás/.test(b.closest('.opt-group').textContent);
      b.click(); await T(); let c=OV(); o.adult=!c.hidden && /Solo para adultos/.test(c.textContent) && /calificar/.test(c.textContent);
      o.atras=window.mundoAtras() && OV().hidden && !ui('options').hidden;
      b.click(); await T(); c=OV(); c.querySelector('.online-in').value=String(res(c)+1); c.querySelector('.online-ok').click(); await T(); c=OV();
      o.malo=!c.hidden && !!c.querySelector('.online-op');
      c.querySelector('.online-in').value=String(res(c)); c.querySelector('.online-ok').click(); await T(); c=OV();
      o.card=!c.hidden && /Califica Mundo Peluche/.test(c.textContent) && !/premio|regalo|monedas/i.test(c.textContent);
      c.querySelector('.rt-go').click(); await T(); o.url=window.__rtLast||''; o.cerro=OV().hidden; ui('options').hidden=true; await T();
      o.menuWeb=[state, window.mundoAtras(), OV().hidden]; return o; })()"""%RES)
    ok(r['vis'], '⭐ «Califica Mundo Peluche» está en Opciones → Para papás')
    ok(r['adult'] and r['malo'] and r['atras'], '🔒 primero pide la operación de adulto (con la mala no pasa; «atrás» la cierra)')
    ok(r['card'] and r['url']=='https://play.google.com/store/apps/details?id=com.rogergc.mundopeluche' and r['cerro'], '⭐ con la buena abre la página del juego en Play Store, sin ofrecer premio %s'%r['url'])
    ok(r['menuWeb']==['menu',False,True], '🌐 en la web «atrás» en el menú no pregunta nada %s'%r['menuWeb'])
    ok(not errs, '🚫 sin errores (%s)'%errs[:3]); await ctx.close()
    # app
    pg,errs,ctx=await abrir(b,"window.__MP_APP={premio:'x', pruebas:true}; localStorage.setItem('mundoPelucheNovedades','%s');"%VER)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await pg.wait_for_timeout(2500)
    r=await ev(r"""(async()=>{ const T=()=>new Promise(r=>setTimeout(r,80)); const OV=()=>document.getElementById('onlineOv'); const o={};
      o.st=state; o.h=window.mundoAtras(); await T(); let c=OV(); o.pide=!c.hidden && /¿Quieres salir del juego\?/.test(c.textContent);
      o.atras2=window.mundoAtras() && OV().hidden && state==='menu';
      window.mundoAtras(); await T(); OV().querySelector('.ex-no').click(); await T(); o.no=OV().hidden && state==='menu' && !window.__exitLast;
      window.mundoAtras(); await T(); OV().querySelector('.ex-go').click(); await T(); o.si=OV().hidden && window.__exitLast===1;
      ui('options').hidden=false; await T(); o.opt=window.mundoAtras() && ui('options').hidden && OV().hidden; return o; })()""")
    ok(r['st']=='menu' and r['h'] and r['pide'], '📱 en la app, «atrás» en el menú principal pregunta «¿Quieres salir del juego?»')
    ok(r['atras2'] and r['no'], '↩️ «No, seguir jugando» (o «atrás» otra vez) cierra el aviso y te quedas en el menú')
    ok(r['si'], '👋 «Sí, salir» cierra el juego')
    ok(r['opt'], '⚙️ si hay algo abierto (Opciones), «atrás» primero lo cierra sin preguntar')
    ok(not errs, '🚫 sin errores (%s)'%errs[:3]); await ctx.close()
    await b.close()
asyncio.run(m())
