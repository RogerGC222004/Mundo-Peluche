# v269: arreglos de la revisión: no te saca de un minijuego nuevo, Rebote sin quedarte en el agua, avisos de isla sin encimarse,
# textos en inglés que faltaban y «Tú solo» sin «Esperando a otro jugador…».
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
    await ev("""(()=>{ startGame(); window.requestAnimationFrame=()=>0; window.__run=(sec,fn)=>{ let t=clock.elapsedTime; for(let i=0;i<Math.round(sec/.05);i++){ clock.elapsedTime=(t+=.05); if(fn && fn(i)===true) return true; update(.05,t); updateSky(.05); scene.updateMatrixWorld(); } }; __run(1); return 1; })()""")
    # 1. terminas un minijuego desde el menú y en seguida empiezas otro: ya no te saca a la lista
    await ev("(()=>{ mgqLocal(7,0,1); __run(30,()=>AR.G[7].ph===3); __run(2); AR.G[7].ms=0; __run(3); ui('arRes').click(); ui('toMenuBtn').click(); __run(.3); mgqLocal(9,0,1); __run(2); return 1; })()")
    await pg.wait_for_timeout(7000)
    r=await ev("(()=>{ __run(.5); return [AR.me.a, state]; })()")
    ok(r==[9,'play'], '1 si empiezas otro minijuego justo al terminar uno, ya no te regresa al menú %s'%r)
    await ev("(()=>{ arLeave(); __run(1); mgqLocal(7,0,1); __run(30,()=>AR.G[7].ph===3); __run(2); AR.G[7].ms=0; __run(3); return 1; })()")
    await pg.wait_for_timeout(7000)
    r=await ev("[state, ui('mgq').hidden]")
    ok(r==['menu',False], '1b y si no haces nada, sí regresas a la lista de minijuegos como antes %s'%r)
    await ev("(()=>{ closeMgq(); menuModes(false); startGame(); __run(1); return 1; })()")
    # 2. Rebote sobre pelotas: el último en caer (se acaba al momento) va a la orilla
    r=await ev("""(()=>{ mgqLocal(2,1,1); __run(30,()=>AR.G[2].ph===3); __run(30,()=>AR.me.a<0); __run(2); const A=AR_SPOTS[2]; return [!!player.swim, +Math.hypot(player.pos.x-A.watch[0],player.pos.z-A.watch[1]).toFixed(1)]; })()""")
    ok(r[0]==False and r[1]<4, '2 Rebote sobre pelotas: si te caes al final, ya no te quedas en el agua debajo de la pista %s'%r)
    # 3. Tú solo: arriba dice «¡Prepárate!», no «Esperando a otro jugador…»
    r=await ev("(()=>{ mgqLocal(POGI,0,1); POG.ask=3; __run(.3); renderArHud(); const t=ui('arTxt').textContent; arLeave(); __run(1); return t; })()")
    ok(r.startswith('¡Prepárate!'), '3 en «Tú solo» arriba dice «%s»'%r)
    # 4. al llegar a una isla: el aviso del mapa sale después del letrero grande
    r=await ev("(()=>{ const src=[...document.scripts].map(s=>s.text).join(''); return [(src.match(/setTimeout\\(\\(\\)=>flashNote\\('Ya puedes volver aquí desde el mapa'\\),2900\\)/g)||[]).length, (src.match(/[^>(]flashNote\\('Ya puedes volver aquí desde el mapa'\\)/g)||[]).length]; })()")
    ok(r==[3,0], '4 al llegar a las 3 islas, «Ya puedes volver aquí desde el mapa» sale después de «¡Llegaste a la isla!» %s'%r)
    # 5. en inglés: los textos que faltaban
    await ev("(()=>{ I18N.set('en'); openMgq(); return 1; })()"); await pg.wait_for_timeout(500)
    r=await ev("(()=>{ const t=ui('mgqMsg').textContent, solo=[...ui('mgqList').querySelectorAll('.mgq-b.solo')].map(b=>b.textContent)[0]; closeMgq(); mapType='juego'; return [t.slice(0,20), solo]; })()")
    r2=await ev("I18N.t('Todavía no tienes minijuegos. Ponle nombre a uno y tócale «Crear».')")
    ok(r[0].startswith('Play solo') and 'Solo' in r[1] and 'Tú' not in r[1] and r2.startswith("You don't have any minigames"), '5 en inglés: el texto de Minijuegos, «Tú solo» y «Todavía no tienes minijuegos…» ya salen traducidos %s %s'%(r,r2))
    await ev("(()=>{ I18N.set('es'); return 1; })()")
    ok(not errs and not cerr, 'sin errores %s %s'%(errs[:3],cerr[:3]))
    await b.close()
asyncio.run(m())
