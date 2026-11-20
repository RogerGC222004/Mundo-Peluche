# v248: «Enviar comentarios» (Opciones → Para papás) y «¿Qué hay de nuevo?».
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

    # A) primera vez
    pg,errs,ctx=await abrir(b,"")
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await pg.wait_for_timeout(3500)
    n=await ev(NEWS); k=await ev("localStorage.getItem('mundoPelucheNovedades')")
    ok(not n and k==VER, '🆕 la primera vez no sale «¿Qué hay de nuevo?» y se guarda la versión (%s)'%k)

    # C) Enviar comentarios (web)
    r=await ev(r"""(async()=>{ const T=()=>new Promise(r=>setTimeout(r,80)); const OV=()=>document.getElementById('onlineOv'); const o={};
      ui('options').hidden=false; await T(); const b=ui('optFeedback'); o.vis=b.getClientRects().length>0 && /Para papás/.test(b.closest('.opt-group').textContent);
      b.click(); await T(); let c=OV(); o.adult=!c.hidden && /Solo para adultos/.test(c.textContent) && /correo/.test(c.textContent);
      const res=()=>{ const t=c.querySelector('.online-op').textContent; const m=/^([\d ]+) ([+−×÷]) ([\d ]+) =$/.exec(t); const a=+m[1].replace(/ /g,''), z=+m[3].replace(/ /g,'');
        return m[2]==='+'?a+z: m[2]==='−'?a-z: m[2]==='×'?a*z: a/z; };
      c.querySelector('.online-in').value=String(res()+1); c.querySelector('.online-ok').click(); await T(); c=OV();
      o.malo=!c.hidden && !!c.querySelector('.online-op') && !/Enviar comentarios/.test(c.querySelector('h2').textContent);
      c.querySelector('.online-in').value=String(res()); c.querySelector('.online-ok').click(); await T(); c=OV();
      o.card=!c.hidden && /Enviar comentarios/.test(c.textContent) && /MundoPelucheTJ@gmail\.com/.test(c.textContent);
      c.querySelector('.fb-go').click(); await T(); o.url=window.__fbLast||''; o.cerro=OV().hidden; ui('options').hidden=true; return o; })()""")
    ok(r['vis'], '📨 «Enviar comentarios» está en Opciones → Para papás')
    ok(r['adult'] and r['malo'], '🔒 primero pide la operación de adulto, y con la respuesta mala no deja pasar')
    ok(r['card'], '✉️ con la respuesta buena explica qué pasa y muestra el correo MundoPelucheTJ@gmail.com')
    u=r['url']; from urllib.parse import unquote
    ok(u.startswith('mailto:MundoPelucheTJ@gmail.com?') and ('v'+VER) in unquote(u) and '(web)' in unquote(u) and r['cerro'],
       '📧 «Abrir correo» arma el correo con asunto y versión %s (web) y se cierra la ventanita'%VER)
    ok(len(unquote(u))<300 and 'apodo' not in unquote(u).lower(), '🙈 el correo no lleva datos del jugador (%d letras)'%len(unquote(u)))
    ok(not errs, '🚫 sin errores (%s)'%errs[:3]); await ctx.close()

    # B) venías de otra versión
    pg,errs,ctx=await abrir(b,"localStorage.setItem('mundoPelucheNovedades','100');")
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await pg.wait_for_timeout(3500)
    n=await ev(NEWS)
    ok(bool(n) and 'Versión '+VER in n and 'Para papás' in n, '✨ si tenías otra versión sale «¿Qué hay de nuevo?» con las novedades')
    r=await ev("(()=>{ document.querySelector('#onlineOv .news-ok').click(); return [document.getElementById('onlineOv').hidden, localStorage.getItem('mundoPelucheNovedades'), state]; })()")
    ok(r[0] and r[1]==VER and r[2]=='menu', '👍 «¡Genial!» la cierra y queda guardada la versión')
    ok(not errs, '🚫 sin errores (%s)'%errs[:3]); await ctx.close()
    pg,errs,ctx=await abrir(b,"localStorage.setItem('mundoPelucheNovedades','%s');"%VER)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await pg.wait_for_timeout(3500)
    ok(not await ev(NEWS), '🔁 al volver a abrir la misma versión ya no sale')
    await ctx.close()

    # C2) en la app dice (app)
    pg,errs,ctx=await abrir(b,"window.__MP_APP={premio:'x', pruebas:true};")
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await pg.wait_for_timeout(1500)
    u=await ev("feedbackUrl()")
    ok('(app)' in unquote(u), '📱 en la app el correo dice «app»')
    await ctx.close(); await b.close()

  # D) horizontal
  pa=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','app','preparar-android.js'),encoding='utf-8').read()
  ok('android.hardware.screen.landscape' in pa and 'android:required="false"' in pa, '↔️ la app declara la pantalla horizontal como «no obligatoria» (aviso de Play)')
asyncio.run(m())
