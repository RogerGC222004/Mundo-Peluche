# v209: Crear mapa — lista de mapas, editor con piezas de juego, Probar (lava, estrellas, bandera, plataforma, bloque que se cae, meta, récord)
import asyncio, json
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
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    await ev("window.__run=(sec,fn)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); if(fn) fn(i); update(.05,t); } }; 1")
    # 1. lista y mapa nuevo
    await ev("menuModes(true); ui('mapBtn').click(); 1"); await pg.wait_for_timeout(300)
    r=await ev("[!ui('mapList').hidden, ui('mapItems').textContent.includes('Todavía no tienes mapas')]"); ok(r==[True,True], 'Crear mapa abre «Mis mapas» (vacía) %s'%r)
    await ev("ui('mapName').value='Obby de Roger'; ui('mapNew').click(); 1"); await pg.wait_for_timeout(1500); await ev("(window.requestAnimationFrame=()=>0, __run(.5), 1)")
    r=await ev("[FREE.on, FREE.ctx!=='libre', FREE.play, FREE.objs.map(o=>o.game).join(','), Math.round(player.pos.z-FREE.Z), !ui('freePlay').hidden]")
    ok(r[0] and r[1] and r[2] is False and r[3]=='inicio,meta' and r[4]==8 and r[5], 'mapa nuevo: ya trae Inicio y Meta, apareces en el Inicio y está «▶ Probar» %s'%r)
    r=await ev("(()=>{ ui('freeObj').click(); for(let i=0;i<30;i++) freeThumbPump(); const n=ui('freeGrid').querySelectorAll('.free-it').length, tabs=[...ui('freeTabs').children].map(b=>b.textContent); ui('freeBox').hidden=true; return [n, tabs[0], tabs.length]; })()")
    ok(r==[7,'🎮 Juego',3], 'Minijuego: en Objetos solo salen Juego (7 piezas), Bloques y Física %s'%r)
    await pg.screenshot(path='/tmp/v209_juego.png')
    # 2. armar el mapa: lava, estrella, bandera, plataforma que se mueve, bloque que se cae
    await ev("""(()=>{ const X=FREE.X, Y=FREE.Y, Z=FREE.Z, A=(id,x,z,r=0)=>freeAddStatic({k:'g',a:id,b:0},X+x,Y,Z+z,r,true);
      window.__lava=A('lava',0,4); window.__star=A('estrella',4,4); window.__flag=A('bandera',0,0); window.__mov=A('mover',8,0); window.__cae=A('cae',-8,0); A('estrella',-4,-4); freeSave(); return 1; })()""")
    # 3. probar
    r=await ev("(()=>{ freePlayStart(); const a=[FREE.play, FREE.run.stars, Math.round(player.pos.z-FREE.Z), ui('freeObj').hidden, !ui('freeEdit').hidden]; __run(1); return [...a, ui('freeTxt').textContent]; })()")
    ok(r[0] and r[1]==2 and r[2]==8 and r[3] and r[4] and '⏱' in r[5] and '0/2' in r[5], 'Probar: empiezas en el Inicio, sale el tiempo y ⭐ 0/2 %s'%r)
    r=await ev("(()=>{ const L=__lava; player.pos.set(L.x,L.box.max.y+.02,L.z); __run(.2); return Math.round(player.pos.z-FREE.Z); })()"); ok(r==8, 'pisar lava te regresa al Inicio (z=%s)'%r)
    r=await ev("(()=>{ const S=__star; player.pos.set(S.x,FREE.Y+.05,S.z); __run(.2); return [FREE.run.got.size, S.root.visible]; })()"); ok(r==[1,False], 'tocar una estrella la junta %s'%r)
    r=await ev("(()=>{ const F=__flag; player.pos.set(F.x,FREE.Y+.05,F.z); __run(.2); const cp=FREE.run.cp===F; const L=__lava; player.pos.set(L.x,L.box.max.y+.02,L.z); __run(.2); return [cp, +(player.pos.x-F.x).toFixed(1), +(player.pos.z-F.z).toFixed(1)]; })()")
    ok(r==[True,0,0], 'la bandera guarda tu lugar: la lava ya te regresa a la bandera %s'%r)
    r=await ev("(()=>{ const M=__mov; player.pos.set(M.root.position.x, M.box.max.y+.02, M.root.position.z); __run(.1); const x0=player.pos.x, m0=M.root.position.x; __run(1); return [+(M.root.position.x-m0).toFixed(2), +(player.pos.x-x0).toFixed(2), +(player.pos.y-M.box.max.y).toFixed(2)]; })()")
    ok(abs(r[0])>.5 and abs(r[0]-r[1])<.15 and abs(r[2])<.1, 'la plataforma se mueve y te lleva encima %s'%r)
    r=await ev("(()=>{ const C=__cae; player.pos.set(C.x, C.box.max.y+.02, C.z); __run(.3); const a=C.solid; __run(.6); const b=[C.solid, C.root.visible, +(player.pos.y-FREE.Y).toFixed(2)]; __run(3); return [a,...b, C.solid]; })()")
    ok(r[0] is True and r[1] is False and r[2] is False and r[3]<.1 and r[4] is True, 'el bloque que se cae: tiembla, desaparece (caes) y luego regresa %s'%r)
    r=await ev("(()=>{ const G=FREE.objs.find(o=>o.game==='meta'); player.pos.set(G.x,FREE.Y+.05,G.z); __run(.2); const a=FREE.run.done; const S2=FREE.objs.filter(o=>o.game==='estrella')[1]; player.pos.set(S2.x,FREE.Y+.05,S2.z); __run(.2); player.pos.set(G.x,FREE.Y+.05,G.z); __run(.2); const M=mapById(FREE.ctx); return [a, FREE.run.done, FREE.run.got.size, !!M.best, ui('freeTxt').textContent]; })()")
    ok(r[0] is False and r[1] and r[2]==2 and r[3] and 'Terminado' in r[4], 'la meta sin todas las estrellas no cuenta; con las 2, ¡llegaste! y se guarda el récord %s'%r)
    try: await ev("renderer.render(scene,camera), 1"); await pg.screenshot(path='/tmp/v209_jugando.png', timeout=90000)
    except Exception as e: print('(sin foto)')
    # 4. editar regresa todo; salir y la lista muestra el récord
    r=await ev("(()=>{ ui('freeEdit').click(); return [FREE.play, __cae.root.visible, __star.root.visible, Math.abs(__mov.root.position.x-__mov.x)<1e-6, !ui('freeObj').hidden]; })()"); ok(r==[False,True,True,True,True], 'Editar: todo regresa a su lugar y vuelven los botones %s'%r)
    r=await ev("(()=>{ ui('toMenuBtn').click(); menuModes(true); ui('mapBtn').click(); return [FREE.on, ui('mapItems').textContent]; })()"); ok(r[0] is False and 'Obby de Roger' in r[1] and 'récord' in r[1] and '8 piezas' in r[1], 'al salir el mapa queda guardado con su récord: %s'%r[1])
    # 5. jugar desde la lista y el modo libre sigue aparte
    r=await ev("(()=>{ ui('mapItems').querySelector('.chip.play').click(); const a=[FREE.play, FREE.objs.length]; ui('toMenuBtn').click(); freeEnter(); const b=[FREE.ctx, FREE.objs.some(o=>o.game)]; ui('toMenuBtn').click(); return [...a,...b]; })()")
    ok(r==[True,8,'libre',False], '«▶ Jugar» entra directo a jugar; el modo libre sigue con sus propias cosas %s'%r)
    r=await ev("(()=>{ menuModes(true); ui('mapBtn').click(); const t=[...ui('mapTypes').children].map(b=>b.textContent); [...ui('mapTypes').children][1].click(); ui('mapName').value='Mi isla'; ui('mapNew').click(); const tabs=mapTabs().map(x=>x[1]); ui('toMenuBtn').click(); menuModes(true); ui('mapBtn').click(); return [t.length, t[2].includes('Pronto'), tabs.length, ui('mapItems').textContent.includes('🏝️ Mundo')]; })()")
    ok(r==[4,True,6,True], 'qué vas a hacer: Minijuego / Mundo completo (todas las pestañas) / Criatura y Objeto «pronto» %s'%r)
    r=await ev("(()=>{ mapsStore(mapsLoad().filter(m=>m.t!=='mundo')); renderMaps(); return 1; })()")
    r=await ev("(()=>{ menuModes(true); ui('mapBtn').click(); const del=ui('mapItems').querySelector('.chip.del'); del.click(); del.click(); return mapsLoad().length; })()"); ok(r==0, 'borrar un mapa pide tocar dos veces y lo borra')
    ok(not errs,'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
