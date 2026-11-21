# v255: idiomas (español / inglés)
#  A) teléfono en inglés sin idioma guardado → el juego arranca en inglés: título Plush'N'Play, menú, opciones, carga
#  B) botones de acción, avisos y textos con partes que cambian (nombres, números, emojis) también salen en inglés
#  C) en Opciones → 🌐 se cambia a español al momento, se guarda y al volver a abrir se queda en español
#  D) teléfono en español → arranca en español y no se traduce nada (sin trabajo extra)
#  E) lista de textos que siguen en español en las pantallas principales (para revisar a mano)
import asyncio, json, re
from playwright.async_api import async_playwright
JUEGO='/home/claude/mundo-peluche.html'
REAL=open('threerepo/build/three.min.js').read()
SRC=open(JUEGO, encoding='utf-8').read(); VER=re.search(r"const GAME_VERSION='(\d+)'",SRC).group(1)
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+SRC.replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
async def abrir(b, locale, limpiar=True, ctx=None):
  if ctx is None: ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True, locale=locale)
  pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
  if limpiar: await pg.add_init_script("if(!sessionStorage.getItem('t255')){ sessionStorage.setItem('t255','1'); localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheNovedades','%s'); }"%(json.dumps(OPTS),VER))
  async def route(r):
    u=r.request.url
    if u.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
    elif "three" in u: await r.fulfill(body=REAL, content_type="application/javascript")
    else: await r.abort()
  await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
  await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
  return pg, errs, ctx
# textos visibles que parecen español (para la lista de pendientes)
RESTOS=r"""(sel=>{ const ES=/[áéíóúñ¿¡]|\b(el|la|los|las|de|del|con|para|tu|tus|un|una|y|que|en|al|se|no|sí|más|ver|toca)\b/i, out=new Set();
  for(const root of document.querySelectorAll(sel)){ if(!root.getClientRects().length) continue; const w=document.createTreeWalker(root,4); let n;
    while((n=w.nextNode())){ const t=n.nodeValue.trim(); if(!t || !/\p{L}{2}/u.test(t)) continue; const p=n.parentElement; if(!p || !p.getClientRects().length || p.closest('[data-noi18n],svg')) continue; if(ES.test(t)) out.add(t.slice(0,90)); } }
  return [...out]; })"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    # ---------- A) inglés automático ----------
    pg,errs,ctx=await abrir(b,'en-US')
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    r=await ev("""({lang:I18N.lang, chosen:I18N.chosen, title:document.title, h:document.documentElement.lang, play:ui('playBtn').textContent.trim(), shop:ui('shopBtn').textContent.trim(),
      opt:ui('optionsBtn').textContent.trim(), tw:[...document.querySelectorAll('#menu .title text')].map(t=>t.textContent).join('|'), tw3:document.querySelectorAll('.tw3').length, aria:document.querySelector('#menu .title').getAttribute('aria-label'),
      full:document.querySelector('label[for=optFull]').firstChild.nodeValue, copy:document.querySelector('.copy-tag').textContent, ph:ui('mpName').placeholder, tl:ui('stIn').title})""")
    print(r)
    ok(r['lang']=='en' and not r['chosen'] and r['h']=='en', 'A1 teléfono en inglés → el juego arranca en inglés (sin escoger nada)')
    ok(r['title']=="Plush'N'Play" and r['aria']=="Plush'N'Play" and r['tw'].startswith("Plush|Plush|Plush|'N'|'N'|'N'|Play"), "A2 el título es Plush'N'Play (pestaña, logo y lector de pantalla)")
    ok(r['play']=='Play' and r['shop']=='Customize' and r['opt']=='Options', 'A3 menú principal en inglés')
    ok(r['full']=='Fullscreen' and 'All rights reserved' in r['copy'], 'A4 opciones y pie del menú en inglés')
    ok(r['ph']=='Plushie' and r['tl']=='Zoom in', 'A5 textos de ayuda (placeholder y title) en inglés')
    # ---------- B) textos que el juego escribe después ----------
    r=await ev("""(async()=>{ const T=()=>new Promise(r=>setTimeout(r,60)); const o={};
      flashNote('Sonido silenciado'); await T(); o.toast=ui('toast').textContent;
      flashNote('Ubicación copiada: X 1 · Y 2'); await T(); o.toast2=ui('toast').textContent;
      setActions({label:'Abrir puerta',run(){}},{label:'Subir con Ana',run(){}},{label:'💦 Bombear (2/3)',run(){}}); await T();
      o.a1=ui('act1').textContent; o.a2=ui('act2').textContent; o.a3=ui('act3').textContent;
      setActions({label:'¡Jalar! (1/3)',run(){}},{label:'Esperando que pique…',run(){}},{label:'Vender 4 frutas (+12 monedas)',run(){}}); await T();
      o.b1=ui('act1').textContent; o.b2=ui('act2').textContent; o.b3=ui('act3').textContent;
      setActions(null,null,null);
      const el=document.createElement('div'); el.id='t255'; el.innerHTML='<p>Salas activas</p><span title="Cerrar">Sala de Pepe · 3 jugadores</span>'; document.body.appendChild(el); await T();
      o.dyn=el.textContent; o.dynT=el.querySelector('span').title; el.remove();
      o.tip=document.getElementById('ldTip') ? 1 : 0; o.txl=txl('Consejo: Pesca en el muelle y véndele tus peces a Tortu.');
      o.news=txl(NEWS['255'][0]);
      return o; })()""")
    print(r)
    ok(r['toast']=='Sound muted' and r['toast2'].startswith('Location copied: X 1'), 'B1 avisos en inglés (también con partes que cambian)')
    ok(r['a1'].startswith('Open door') and r['a2'].startswith('Ride with Ana') and 'Pump (2/3)' in r['a3'], 'B2 botones de acción en inglés (con nombres, números y emojis)')
    ok(r['b1'].startswith('Pull! (1/3)') and r['b2'].startswith('Waiting for a bite…') and r['b3'].startswith('Sell 4 fruits (+12 coins)'), 'B3 acciones con signos y números')
    ok(r['dyn']=="Active roomsPepe's room · 3 players" and r['dynT']=='Close', 'B4 lo que se agrega a la página se traduce solo (texto y title)')
    ok(r['txl'].startswith('Tip: Fish at the pier') and r['news'].startswith('The game is now in English'), 'B5 consejos de la carga y novedades en inglés')
    # ---------- E) pendientes en pantallas principales ----------
    await ev("(()=>{ openOptions(); return 1; })()")
    rest=await ev(RESTOS+"('#options,#menu')"); print('PENDIENTES (opciones y menú):', rest)
    ok(len(rest)<=2, 'E1 opciones y menú: casi nada queda en español ('+str(len(rest))+')')
    await pg.screenshot(path='dest/v255_opciones_en.png')
    # ---------- C) cambiar a español ----------
    r=await ev("""(async()=>{ const T=()=>new Promise(r=>setTimeout(r,80)); document.querySelector('#optLang [data-v=es]').click(); await T();
      return {lang:I18N.lang, title:document.title, full:document.querySelector('label[for=optFull]').firstChild.nodeValue, play:ui('playBtn').textContent.trim(), tw:[...document.querySelectorAll('#menu .title text')].map(t=>t.textContent).join('|'),
        pressed:document.querySelector('#optLang [data-v=es]').getAttribute('aria-pressed'), stored:localStorage.getItem('mundoPelucheIdioma'), ph:ui('mpName').placeholder, langRow:document.querySelector('#optLang').closest('.opt').textContent}; })()""")
    print(r)
    ok(r['lang']=='es' and r['stored']=='es' and r['pressed']=='true', 'C1 Opciones → Español cambia el idioma y lo guarda')
    ok(r['title']=='Mundo Peluche' and r['tw']=='Mundo|Mundo|Mundo|Peluche|Peluche|Peluche' and r['play']=='Jugar' and r['full']=='Pantalla completa' and r['ph']=='Peluchito', 'C2 todo regresa a español al momento (menú, opciones, título)')
    ok('Idioma · Language' in r['langRow'] and 'English' in r['langRow'], 'C3 la fila del idioma se lee en los dos idiomas')
    r=await ev("""(async()=>{ const T=()=>new Promise(r=>setTimeout(r,80)); flashNote('Sonido silenciado'); await T(); const a=ui('toast').textContent;
      document.querySelector('#optLang [data-v=en]').click(); await T(); const b=ui('playBtn').textContent.trim(); document.querySelector('#optLang [data-v=es]').click(); await T();
      return {a, b, c:ui('playBtn').textContent.trim()}; })()""")
    ok(r['a']=='Sonido silenciado' and r['b']=='Play' and r['c']=='Jugar', 'C4 se puede ir y venir entre idiomas')
    ok(not errs, 'A-C sin errores en la página '+str(errs[:2]))
    pg2,errs2,_=await abrir(b,'en-US',limpiar=False,ctx=ctx)
    r=await pg2.evaluate("s=>__T.ev(s)","({lang:I18N.lang, play:ui('playBtn').textContent.trim()})")
    ok(r['lang']=='es' and r['play']=='Jugar', 'C5 al volver a abrir se queda en español aunque el teléfono esté en inglés')
    await ctx.close()
    # ---------- D) teléfono en español ----------
    pg,errs,ctx=await abrir(b,'es-MX')
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    r=await ev("""(async()=>{ flashNote('Sonido silenciado'); await new Promise(r=>setTimeout(r,60)); return {lang:I18N.lang, title:document.title, play:ui('playBtn').textContent.trim(), t:txl('Jugar'), toast:ui('toast').textContent, stored:localStorage.getItem('mundoPelucheIdioma')}; })()""")
    print(r)
    ok(r['lang']=='es' and r['title']=='Mundo Peluche' and r['play']=='Jugar' and r['t']=='Jugar' and r['toast']=='Sonido silenciado' and r['stored'] is None, 'D1 teléfono en español → todo en español, sin traducir nada')
    ok(not errs, 'D sin errores en la página '+str(errs[:2]))
    await ctx.close()
    # ---------- E2) jugando en inglés ----------
    pg,errs,ctx=await abrir(b,'en-GB')
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev("(()=>{ startGame(); return 1; })()"); await pg.wait_for_timeout(2500)
    rest=await ev(RESTOS+"('#hud,#touch,#hotbar,#actions')"); print('PENDIENTES (jugando):', rest)
    r=await ev("({cam:ui('camChip').textContent.trim(), pause:ui('pauseChip').textContent.trim(), jump:ui('tJump').textContent.trim()})"); print(r)
    ok(r['pause']=='Pause' and r['jump']=='Jump', 'E2 botones en pantalla en inglés al jugar')
    await pg.screenshot(path='dest/v255_jugando_en.png')
    ok(not errs, 'E sin errores en la página '+str(errs[:2]))
    await b.close()
asyncio.run(m())
