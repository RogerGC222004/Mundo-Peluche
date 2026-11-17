# v210: editor de mapas desde arriba (como el de las casitas): panel de piezas, tocar el piso 2 veces para poner, apilar, altura,
# quitar, mover, deshacer, buscar, favoritas, Probar/Editar y Listo.
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
    await ev("""window.__run=(sec)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); update(.05,t); } };
      window.__scr=(x,y,z)=>{ __run(.6); camera.updateMatrixWorld(); const v=new THREE.Vector3(x,y,z).project(camera), r=canvas.getBoundingClientRect(); return [r.left+(v.x+1)/2*r.width, r.top+(1-v.y)/2*r.height]; };
      window.__tap=(x,y,z,n=2)=>{ const [cx,cy]=__scr(x,y,z); for(let i=0;i<n;i++) medTap(cx,cy,true); }; 1""")
    await ev("menuModes(true); ui('mapBtn').click(); ui('mapName').value='Editor'; ui('mapNew').click(); 1"); await pg.wait_for_timeout(1500); await ev("(window.requestAnimationFrame=()=>0, __run(1), 1)")
    r=await ev("[MED.on, !MED.ui.inv.hidden, !MED.ui.bar.hidden, document.body.classList.contains('in-med'), getComputedStyle(ui('hud')).display, [...MED.ui.inv.querySelectorAll('.hed-tabs button')].length, MED.ui.inv.querySelectorAll('.hed-card').length]")
    ok(r[0] and r[1] and r[2] and r[3] and r[4]=='none' and r[5]==5 and r[6]==7, 'al crear un mapa entras al editor desde arriba: panel de piezas (★ + 4 pestañas (v217: + 🎡 Parque), 7 piezas de juego) y se esconden los botones del juego %s'%r)
    await pg.screenshot(path='/tmp/v210_editor.png')
    # poner con dos toques; el primero solo muestra el fantasma
    r=await ev("""(()=>{ medSelect({k:'b',a:0,b:3}); const X=FREE.X+2.5, Z=FREE.Z+.5; const n0=FREE.objs.length; __tap(X,FREE.Y,Z,1); const a=[FREE.objs.length===n0, !!MED.hov, MED.ghost&&MED.ghost.visible];
      __tap(X,FREE.Y,Z,1); const o=FREE.objs[FREE.objs.length-1]; return [...a, FREE.objs.length===n0+1, +(o.x-FREE.X).toFixed(2), +(o.z-FREE.Z).toFixed(2), +(o.box.min.y-FREE.Y).toFixed(2)]; })()""")
    ok(r[0] and r[1] and r[2] and r[3] and r[4]==2.5 and r[5]==.5 and r[6]==0, 'tocar el piso: 1er toque muestra el fantasma verde, 2º lo pone (en su cuadrito) %s'%r)
    r=await ev("""(()=>{ const o=FREE.objs[FREE.objs.length-1]; __tap(o.x, o.box.max.y, o.z, 2); const t=FREE.objs[FREE.objs.length-1]; return [t!==o, +(t.box.min.y-o.box.max.y).toFixed(2)]; })()""")
    ok(r==[True,0], 'tocar arriba de un bloque pone otro encima %s'%r)
    r=await ev("""(()=>{ medHeight(1); medHeight(1); medSelect({k:'g',a:'mover',b:0}); medRotate(); __tap(FREE.X-4.5,FREE.Y+2,FREE.Z+.5,2); const o=FREE.objs[FREE.objs.length-1]; medHeight(-5); return [o.game, o.r, +(o.y-FREE.Y).toFixed(2), MED.h]; })()""")
    ok(r==['mover',1,2,0], 'Más alto: pones una plataforma flotando a 2 m, girada %s'%r)
    # quitar, deshacer, mover
    r=await ev("""(()=>{ const n=FREE.objs.length, o=FREE.objs.find(q=>q.game==='mover'); medTool('del'); const [cx,cy]=__scr((o.box.min.x+o.box.max.x)/2,o.box.max.y,(o.box.min.z+o.box.max.z)/2); medTap(cx,cy,true); const a=MED.mark===o; medTap(cx,cy,true);
      const b=FREE.objs.length===n-1 && !FREE.objs.includes(o); medUndo(); const c=FREE.objs.length===n && FREE.objs.some(q=>q.game==='mover'); return [a,b,c]; })()""")
    ok(r==[True,True,True], 'Quitar: el 1er toque la marca en rojo, el 2º la quita; ↶ Deshacer la regresa %s'%r)
    r=await ev("""(()=>{ medTool('move'); const o=FREE.objs.find(q=>q.game==='meta'); const [cx,cy]=__scr(o.x,o.box.max.y,o.z); medTap(cx,cy,true); medTap(cx,cy,true); const held=!!MED.moving && MED.sel.a==='meta';
      __tap(FREE.X+6.5,FREE.Y,FREE.Z-3.5,2); const m=FREE.objs.find(q=>q.game==='meta'); return [held, +(m.x-FREE.X).toFixed(2), +(m.z-FREE.Z).toFixed(2), FREE.objs.filter(q=>q.game==='meta').length, !MED.moving]; })()""")
    ok(r==[True,6.5,-3.5,1,True], 'Mover: agarras la Meta y la pones en otro lugar %s'%r)
    r=await ev("""(()=>{ medUndo(); const m=FREE.objs.find(q=>q.game==='meta'); return [+(m.z-FREE.Z).toFixed(2), FREE.objs.filter(q=>q.game==='meta').length]; })()"""); ok(r==[-12,1], 'Deshacer el movimiento la regresa a donde estaba %s'%r)
    # buscar y favoritas
    r=await ev("""(()=>{ MED.tab='bloques'; medRender(); const inp=MED.ui.inv.querySelector('.hed-srch input'); inp.value='lava'; inp.oninput(); const a=[...MED.ui.inv.querySelectorAll('.hed-card span')].map(s=>s.textContent);
      inp.value=''; inp.oninput(); MED.ui.inv.querySelector('.hed-card i.fv').click(); MED.tab='fav'; medRender(); const b=MED.ui.inv.querySelectorAll('.hed-card').length; return [a.join(','), b]; })()""")
    ok(r==['Lava',1], 'el buscador encuentra «Lava» y la ☆ guarda favoritas %s'%r)
    # probar y editar
    r=await ev("""(()=>{ medPlay(); const a=[MED.on, FREE.play, document.body.classList.contains('in-med'), !ui('freeEdit').hidden]; ui('freeEdit').click(); return [...a, MED.on, FREE.play]; })()""")
    ok(r==[False,True,False,True,True,False], '▶ Probar baja a tu peluche y juegas; ✏️ Editar regresa a la vista de arriba %s'%r)
    r=await ev("""(()=>{ const n=FREE.objs.length; medDone(); const M=mapsLoad().find(m=>m.n==='Editor'); return [MED.on, FREE.on, state, !ui('mapList').hidden, M && M.s.length===n]; })()""")
    ok(r==[False,False,'menu',True,True], '✓ Listo guarda y regresa a «Mis mapas» %s'%r)
    r=await ev("(()=>{ freeEnter(); const a=[MED.on, FREE.ctx]; ui('toMenuBtn').click(); return a; })()"); ok(r==[False,'libre'], 'el Modo libre sigue con la forma fácil (sin vista de arriba) %s'%r)
    ok(not errs,'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
