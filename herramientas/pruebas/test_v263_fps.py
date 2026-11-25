# v263: Límite de FPS según la pantalla: el juego mide cuántos Hz tiene y solo ofrece los límites que van parejos (toda, la mitad y
# lo más cercano a 30), más «Automático» (de fábrica) y «Libre». Automático baja si muchos cuadros llegan tarde y prueba subir después.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
SEED="""localStorage.clear(); localStorage.setItem('mundoPelucheEcon124','1');
localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false, autoRes:false}));"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    pg=await (await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, locale='es-MX')).new_page(); errs=[]; cerr=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console",lambda msg: cerr.append(msg.text[:200]) if msg.type=='error' and ('Shader' in msg.text or 'WebGL' in msg.text or 'GL_' in msg.text) else None)
    await pg.add_init_script(SEED)
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=180000)

    # 1. de fábrica: Automático; los límites que van parejos con cada pantalla
    r=await ev("(()=>{ const o=[settings.fpsCap]; for(const hz of [60,90,120,144]){ SCRHZ.v=hz; o.push(capList()); } return o; })()")
    ok(r[0]=='auto', '1a de fábrica el límite es «Automático» (%s)'%r[0])
    ok(r[1:]==[[60,30],[90,45,30],[120,60,30],[144,72,36]], '1b los límites parejos: 60 Hz %s · 90 Hz %s · 120 Hz %s · 144 Hz %s'%tuple(r[1:]))
    # 2. la fila en Opciones (con una pantalla de 120 Hz) y en inglés
    r=await ev("""(async()=>{ SCRHZ.v=120; openOptions(); const B=()=>[...ui('optFpsCap').querySelectorAll('button')].map(b=>b.dataset.v), o=[B(), ui('optHz').textContent, ui('optFpsCap').querySelector('[data-v="auto"]').getAttribute('aria-pressed')];
      ui('optFpsCap').querySelector('[data-v="60"]').click(); o.push(settings.fpsCap, JSON.parse(localStorage.getItem('mundoPelucheOpciones')||'{}').fpsCap);
      SCRHZ.v=60; syncOptionsUI(); o.push(B()); I18N.set('en'); await new Promise(f=>setTimeout(f,400)); o.push(ui('optHz').textContent, ui('optFpsCap').querySelector('[data-v="auto"]').textContent.trim()); I18N.set('es'); optionsEl.hidden=true; return o; })()""")
    ok(r[0]==['auto','120','60','30','free'] and r[1]=='Tu pantalla: 120 Hz' and r[2]=='true', '2a con pantalla de 120 Hz salen Automático, 120, 60, 30 y Libre; dice «%s»'%r[1])
    ok(r[3]=='60' and r[4]=='60' and r[5]==['auto','60','30','free'] and r[6]=='Your screen: 60 Hz' and r[7]=='Auto', '2b se guarda lo que escoges; con 60 Hz solo Automático, 60, 30 y Libre; en inglés «%s» / «%s»'%(r[6],r[7]))
    # 3. si tenías un límite que no va parejo con tu pantalla, pasa a Automático (Libre y los parejos se quedan)
    r=await ev("(()=>{ const o=[]; SCRHZ.v=120; for(const v of ['90','60','free','45']){ settings.fpsCap=v; hzChanged(); o.push(settings.fpsCap); } return o; })()")
    ok(r==['auto','60','free','auto'], '3 un límite que no va parejo (90 o 45 en 120 Hz) pasa a Automático; 60 y Libre se quedan %s'%r)
    # 4. Automático: con muchos cuadros tarde baja; si le sobra, prueba subir; si no pudo, espera más para volver a probar
    await ev("startGame()"); await pg.wait_for_timeout(1500)
    r=await ev("""(()=>{ settings.fpsCap='auto'; SCRHZ.v=120; FPA.lvl=0; FPA.n=FPA.late=FPA.prev=0; FPA.upAt=0; FPA.wait=20000; let t=1e6; const o=[fpsCapNow()];
      const run=(ms,n)=>{ for(let i=0;i<n;i++){ t+=ms; fpsAuto(t); } };
      run(16.7,400); o.push(fpsCapNow());          // el teléfono solo llega a 60: baja a 60
      run(16.7,180); o.push(fpsCapNow());          // a 60 va parejo pero aún no toca probar
      t+=20000; run(16.7,181); o.push(fpsCapNow()); // ya pasaron 20 s parejo: prueba 120 otra vez
      run(16.7,400); o.push(fpsCapNow(), FPA.wait); // no pudo: regresa a 60 y espera más (40 s) para volver a probar
      run(33.4,300); o.push(fpsCapNow());          // si ni a 60 llega: 30
      settings.fpsCap='free'; o.push(fpsCapNow()); settings.fpsCap='30'; o.push(fpsCapNow()); settings.fpsCap='auto'; FPA.lvl=0; return o; })()""")
    ok(r==[0,60,60,0,60,80000,30,0,30], '4 Automático: a 120 Hz sin límite; si llega tarde baja a 60; parejo 20 s → prueba 120; no pudo → 60 y espera más; si tampoco → 30 %s'%r)
    ok(not errs, 'sin errores (%s)'%errs[:3])
    await b.close()
asyncio.run(m())
