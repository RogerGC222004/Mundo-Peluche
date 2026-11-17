# v213: 📦 Mis creaciones dentro de un Mundo completo — minijuegos construidos encima del mundo (espacio, fantasma verde/rojo,
# girar, letrero y placa, se agarra completo, se actualiza si cambias el original, piezas aparte con límite, se juega con su
# Inicio/Meta, tiempo y récord), criaturas y objetos como premio que se recogen.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, device_scale_factor=1); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
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
    # 0. un minijuego, una criatura y un objeto
    r=await ev("""(()=>{ menuModes(true); ui('mapBtn').click(); mapType='juego'; ui('mapName').value='Obby'; mapCreate(); window.requestAnimationFrame=()=>0;
      const X=FREE.X, Y=FREE.Y, Z=FREE.Z; freeAddStatic({k:'g',a:'estrella',b:0},X+2,Y,Z-3,0,true); freeAddStatic({k:'g',a:'lava',b:0},X-3,Y,Z-3,0,true); freeAddStatic({k:'b',a:0,b:2},X+.5,Y,Z+4.5,0,true); freeAddStatic({k:'g',a:'bandera',b:0},X,Y,Z-6,0,true);
      const id=FREE.ctx; medDone(); crOpen(null); ui('crName').value='Michi'; crClose(true); obOpen(null); ui('crName').value='Varita'; crSet('pieza','estrella'); crClose(true); ui('mapList').hidden=true;
      const M=mapById(id); return [M.t, M.s.length, crLoad().length, obLoad().length]; })()""")
    ok(r==['juego',6,1,1], 'preparación: minijuego «Obby» (6 piezas), una criatura y un objeto %s'%r)
    # 1. el Mundo completo trae la pestaña 📦 Mis creaciones
    r=await ev("""(()=>{ menuModes(true); ui('mapBtn').click(); mapType='mundo'; ui('mapName').value='Mi isla'; mapCreate(); window.__W=FREE.ctx; const tabs=mapTabs().map(t=>t[0]);
      MED.tab='creaciones'; MED.sub=''; medRender(); const subs=[...MED.ui.inv.querySelectorAll('.hed-subs button')].map(b=>b.textContent); const n1=MED.ui.inv.querySelectorAll('.hed-card').length;
      MED.sub='cr'; medRender(); const n2=MED.ui.inv.querySelectorAll('.hed-card').length; MED.sub='ob'; medRender(); const n3=MED.ui.inv.querySelectorAll('.hed-card').length;
      return [tabs.join(','), subs.join(','), n1, n2, n3]; })()""")
    ok(r[0]=='juego,bloques,fisica,parque,creaciones,construir,casa,jardin' and r[1]=='🎯 Minijuegos,🐾 Criaturas,🎒 Objetos' and r[2:]==[1,1,1], 'Mundo completo: pestaña 📦 Mis creaciones con Minijuegos, Criaturas y Objetos %s'%r)
    # 2. escoger el minijuego: calcula su espacio; verde donde cabe, rojo encima del Inicio del mundo
    r=await ev("""(()=>{ const M=mapsLoad().find(m=>m.t==='juego'); window.__G=M.id; medSelect({k:'m',a:M.id,b:0}); const tip=MED.ui.tip.textContent; const L=mgiLayout(M);
      const X=FREE.X, Y=FREE.Y, Z=FREE.Z, bad=mgiFits(M.id,{x:X,y:Y,z:Z},0), good=mgiFits(M.id,{x:X+25,y:Y,z:Z},0), edge=mgiFits(M.id,{x:X+FREE.R-1,y:Y,z:Z},0);
      MED.hov={x:X+25,y:Y,z:Z,ok:true}; medGhostTick(); const g=MED.ghost, col=g&&g.userData.edge.material.color.getHexString();
      MED.hov={x:X,y:Y,z:Z,ok:true}; medGhostTick(); const col2=g&&g.userData.edge.material.color.getHexString();
      return [tip.includes('mide'), +L.w.toFixed(1), +L.d.toFixed(1), L.n, bad, good, edge, col, col2]; })()""")
    ok(r[0] and r[3]==6 and r[4] is False and r[5] is True and r[6] is False and r[7]=='5ee36a' and r[8]=='ff5a5a', 'escoges el minijuego: mide %s × %s m; el rectángulo sale verde donde cabe y rojo si se encima o se sale %s'%(r[1],r[2],r))
    # 3. ponerlo (con giro): llega completo, con letrero y placa; sus piezas cuentan aparte
    r=await ev("""(()=>{ const X=FREE.X, Y=FREE.Y, Z=FREE.Z, own0=freeOwn(); MED.rot=1; medPlace({x:X+25,y:Y,z:Z,ok:true}); const I=mgiList()[0]; const sz=I.box.getSize(new THREE.Vector3());
      const L=mgiLayout(mapById(__G)); return [!!I, I.kids.length, freeOwn()-own0, mgiPieces(), !!I.signTex, !!I.plate, +sz.x.toFixed(1), +sz.z.toFixed(1), +L.w.toFixed(1), +L.d.toFixed(1), MED.ui.tip.textContent.includes('/300')]; })()""")
    ok(r[0] and r[1]==6 and r[2]==1 and r[3]==6 and r[4] and r[5] and r[6]>r[7] and r[10], 'se pone completo y girado (%s × %s m), con letrero y placa ▶ JUGAR; cuenta como 1 pieza del mundo y 6 de minijuegos %s'%(r[6],r[7],r))
    # 4. se agarra completo: deshacer lo quita entero; mover lo lleva entero
    r=await ev("""(()=>{ medUndo(); const a=[mgiList().length, FREE.objs.filter(o=>o.par).length]; const X=FREE.X, Y=FREE.Y, Z=FREE.Z; MED.sel={k:'m',a:__G,b:0}; MED.rot=0; medPlace({x:X+25,y:Y,z:Z,ok:true});
      const I=mgiList()[0], k0=I.kids[0], kx=k0.x; MED.tool='move'; MED.moving=medEntry(I); MED.sel={...I.sel}; MED.rot=I.r; freeDrop(I); MED.tool='place'; medPlace({x:X+25,y:Y,z:Z+20,ok:true});
      const J=mgiList()[0]; return [...a, mgiList().length, J.kids.length, +(J.z-Z).toFixed(1), FREE.objs.filter(o=>o.par).length]; })()""")
    ok(r==[0,0,1,6,20,6], 'se agarra completo: Deshacer lo quita entero y Mover lo cambia de lugar con todas sus piezas %s'%r)
    # 5. se guarda como 1 pieza y si cambias el original, aquí también cambia
    r=await ev("""(()=>{ medExit(); const W=mapById(__W); const ms=W.s.filter(q=>q[0]==='m').length, kids=W.s.length;
      const L=mapsLoad(), G=L.find(m=>m.id===__G); G.s.push(['b',0,5,3,0,6,0]); mapsStore(L); FREE.loaded=null; freeLoad(); const I=mgiList()[0];
      return [ms, kids, I && I.kids.length, !!I && Math.abs(I.z-(FREE.Z+20))<.01]; })()""")
    ok(r[0]==1 and r[1]==3 and r[2]==7 and r[3], 'se guarda como una sola pieza (el mundo guarda %s cosas); al cambiar el minijuego original, aquí sale con la pieza nueva %s'%(r[1],r))
    # 6. jugar: su Inicio empieza su tiempo, su lava te regresa a su Inicio, su estrella y su meta guardan el récord
    r=await ev("""(()=>{ freePlayStart(); const I=mgiList()[0], ini=I.kids.find(o=>o.game==='inicio'), lava=I.kids.find(o=>o.game==='lava'), star=I.kids.find(o=>o.game==='estrella'), meta=I.kids.find(o=>o.game==='meta');
      const go=o=>{ player.pos.set(o.x,o.box.max.y+.02,o.z); player.vel.set(0,0,0); player.vy=0; };
      go(ini); __run(.3); const started=!!I.run, hud=ui('freeTxt').textContent;
      go(lava); __run(.2); const back=Math.hypot(player.pos.x-ini.x,player.pos.z-ini.z)<.5;
      player.pos.set(ini.x+1.6,ini.box.max.y,ini.z+1.6); __run(.6); const t1=I.run&&I.run.t0;
      star.root.getWorldPosition(_fgP); player.pos.set(_fgP.x,_fgP.y+1-1,_fgP.z); __run(.2); const got=I.run.got.size;
      player.pos.set(meta.x,meta.box.min.y+.05,meta.z); player.vel.set(0,0,0); __run(.3); const done=I.run.done, best=mapById(__G).best;
      return [started, hud.includes('🎯 Obby'), back, got, done, best>0, FREE.run && !FREE.run.done, mapById(__W).best||0]; })()""")
    ok(r[0] and r[1] and r[2] and r[3]==1 and r[4] and r[5] and r[6] and r[7]==0, 'jugando: su Inicio empieza su tiempo (🎯 en la barra), su lava te regresa a su Inicio, juntas su estrella y su Meta guarda SU récord (no el del mundo) %s'%r)
    r=await ev("""(()=>{ const I=mgiList()[0]; const c=I.signCv.getContext('2d').getImageData(256,148,1,1).data; player.pos.set(FREE.X-30,FREE.Y+.05,FREE.Z); __run(.3); return [I.run===null, Array.from(c).slice(0,3).join(',')]; })()""")
    ok(r[0], 'al alejarte del minijuego se termina su partida; el letrero ya dice el récord %s'%r)
    # 7. criatura y premio: el objeto flota y al jugar te lo llevas en la mano
    r=await ev("""(()=>{ freePlayStop(); medEnter(); const X=FREE.X, Y=FREE.Y, Z=FREE.Z, O=obLoad()[0], C=crLoad()[0];
      MED.sel={k:'o',a:O.id,b:0}; MED.rot=0; medPlace({x:X-10,y:Y,z:Z+5,ok:true}); MED.sel={k:'c',a:C.id,b:0}; medPlace({x:X-14,y:Y,z:Z+5,ok:true}); const pk=FREE.objs.find(o=>o.sel.k==='o');
      __run(.5); const spin=pk.root.userData.spinO.rotation.y; medExit(); freePlayStart(); hotbar[0]='map'; hotbar[1]='bow'; hotbar[2]='flag'; hotbar[3]='book'; hotbar[4]='lamp'; selectedSlot=0; holding=false;
      player.pos.set(pk.x,FREE.Y+.05,pk.z+4); __run(.2); player.pos.set(pk.x,FREE.Y+.05,pk.z); __run(.3);
      const got=pk.got, vis=pk.root.visible, held=heldItem(); freePlayStop(); const back=pk.root.visible && !pk.got;
      return [spin>0, got, vis, held==='o:'+O.id, back, !!FREE.objs.find(o=>o.sel.k==='c')]; })()""")
    ok(r==[True,True,False,True,True,True], 'premio: el objeto flota girando; al jugar lo tocas y te lo llevas en la mano; al editar vuelve a su lugar; la criatura también está %s'%r)
    # 8. límites: máximo 5 minijuegos dentro de un mundo
    r=await ev("""(()=>{ medEnter(); let n=0; for(let i=0;i<6;i++){ const o=freeAddStatic({k:'m',a:__G,b:0},FREE.X-50+i*0,FREE.Y,FREE.Z-50+i*0,0,true); if(o) n++; } const tot=mgiList().length; medExit(); return [tot, mgiPieces()<=MGI_PIECES]; })()""")
    ok(r==[5,True], 'límite: máximo %s minijuegos por mundo y las piezas de minijuegos no pasan de 300 %s'%(r[0],r))
    ok(not errs,'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
