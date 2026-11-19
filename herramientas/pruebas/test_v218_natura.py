# v218: 🌳 Naturaleza (alberca para nadar, charco, tobogán de agua, árboles/flores con viento), 🛹 vehículos (carrito y
# patineta: se manejan, suben rampas, brincan, tumban juguetes y se quedan donde los dejas) y rampas de verdad.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("if(!sessionStorage.getItem('t218')){ sessionStorage.setItem('t218','1'); localStorage.clear(); } localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    await ev("""window.__run=(sec,fn)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); if(fn) fn(i); update(.05,t); updateSky(.05); scene.updateMatrixWorld(); } };
      window.__act=()=>{ const a=freeActions(); return a?a.map(x=>x&&x.label):null; }; window.__do=(lab)=>{ const a=freeActions()||[]; const x=a.find(q=>q&&q.label===lab); if(x) x.run(); return !!x; };
      window.__walk=(sec,dx,dz)=>{ __run(sec,()=>{ const L=Math.hypot(dx,dz); yaw=Math.atan2(-dx,-dz); stick.x=0; stick.y=-.8; }); stick.x=0; stick.y=0; }; 1""")
    # 1. el menú
    r=await ev("""(async()=>{ freeEnter(); window.requestAnimationFrame=()=>0; FREE.objs.slice().forEach(freeDrop); FREE.dyn.slice().forEach(freeDrop); freeOpenBox();
      [...ui('freeTabs').children].find(b=>b.textContent.includes('Naturaleza')).click(); const subs=[...ui('freeSubs').children].map(b=>b.textContent).join('|'); const agua=[...ui('freeGrid').children].map(b=>b.textContent).join(',');
      [...ui('freeSubs').children][1].click(); const plantas=[...ui('freeGrid').children].map(b=>b.textContent).join(',');
      [...ui('freeTabs').children].find(b=>b.textContent.includes('Parque')).click(); [...ui('freeSubs').children].find(b=>b.textContent.includes('Vehículos')).click(); const veh=[...ui('freeGrid').children].map(b=>b.textContent).join(',');
      for(let i=0;i<60;i++) freeThumbPump(); const bad=Object.keys(FTH.c).filter(k=>/^[nv]:/.test(k) && FTH.c[k]==='x'); ui('freeBox').hidden=true; return [subs, agua, plantas, veh, bad.length]; })()""")
    ok(r[1]=='Alberca,Charco,Tobogán de agua' and r[2]=='Árbol,Árbol de flores,Palmera,Arbusto,Flores,Pasto alto' and r[3]=='Carrito,Patineta' and r[4]==0, 'Objetos → 🌳 Naturaleza (💧 Agua y 🌸 Plantas) y 🎡 Parque → 🛹 Vehículos, con fotito %s'%r)
    # 2. plantas con viento y árboles que sí estorban
    r=await ev("""(()=>{ const X=FREE.X,Y=FREE.Y,Z=FREE.Z, t=freeAddStatic({k:'n',a:'arbol',b:0},X-30,Y,Z-30,0,true), f=freeAddStatic({k:'n',a:'flores',b:0},X-26,Y,Z-30,0,true); let wm=null; t.root.traverse(q=>{ if(q.isMesh && q.material===pqWindMat()) wm=q; });
      const P=new THREE.Vector3(X-30-.5,Y,Z-30); freeCollide(P); const blocked=Math.hypot(P.x-(X-30),P.z-(Z-30))>.6; const P2=new THREE.Vector3(X-26.2,Y,Z-30); freeCollide(P2);
      return [!!wm, !!(wm&&wm.geometry.attributes.sw), pqWindMat().customProgramCacheKey(), blocked, Math.abs(P2.x-(X-26.2))<1e-6, f.solid]; })()""")
    ok(r==[True,True,'pqWind',True,True,False], 'plantas: se mecen con el viento de la isla; el tronco del árbol estorba y las flores no %s'%r)
    # 3. rampas de verdad: subes caminando; por atrás es pared
    r=await ev("""(()=>{ const X=FREE.X+20,Y=FREE.Y,Z=FREE.Z+20; const rp=freeAddStatic({k:'b',a:3,b:2},X+.5,Y,Z+.5,0,true); player.pos.set(X+.5,Y+.05,Z-1.5); player.vel.set(0,0,0); __run(.2); let top=0; __run(1.2,()=>{ yaw=Math.PI; stick.y=-.8; top=Math.max(top,player.pos.y-Y); }); stick.y=0;
      const g1=+(freeGround(X+.5,Z+.5,Y+3)-Y).toFixed(2), g2=+(freeGround(X+.5,Z+.9,Y+3)-Y).toFixed(2); player.pos.set(X+.5,Y+.05,Z+2.5); __run(.2); __walk(1,0,-1); const back=player.pos.z-Z; return [+top.toFixed(2), g1, g2, +back.toFixed(2)]; })()""")
    ok(r[0]>.8 and abs(r[1]-.5)<.05 and abs(r[2]-.9)<.05 and r[3]>1.3, 'rampa: caminando subes hasta arriba (%s m); a la mitad mide %s m; por atrás es pared %s'%(r[0],r[1],r))
    # 4. alberca: subes la escalerita, te echas, nadas, las pelotas flotan y sales nadando hacia la orilla
    r=await ev("""(()=>{ const X=FREE.X,Y=FREE.Y,Z=FREE.Z-20, o=freeAddStatic({k:'n',a:'alberca',b:0},X,Y,Z,0,true); const bp=freeAddDyn('playa',X-1,Y+3,Z-1,true), bb=freeAddDyn('boliche',X+1,Y+3,Z-1,true);
      player.pos.set(X,Y+.05,Z+5.5); player.vel.set(0,0,0); __run(.2); let rim=0, inn=false; __run(3,()=>{ if(player.swim) inn=true; if(inn){ stick.y=0; return; } yaw=0; stick.y=-.8; rim=Math.max(rim,player.pos.y-Y); }); stick.y=0; rim=+rim.toFixed(2); __run(1.5); const swim=player.swim, fy=+(player.pos.y-Y).toFixed(2);
      __run(2); const balls=[+(bp.root.position.y-Y).toFixed(2), +(bb.root.position.y-Y).toFixed(2)]; let out=null; __run(3,()=>{ if(out) { stick.y=0; return; } yaw=-Math.PI/2; stick.y=-.8; if(!player.swim) out=[player.swim, +(player.pos.y-Y).toFixed(2), +(player.pos.x-X).toFixed(1)]; }); stick.y=0; out=out||[player.swim,0,0];
      return [rim, swim, fy, balls, out, swimLevel(X,Z)-Y]; })()""")
    ok(r[0]>1.4 and r[1] and .1<r[2]<.6 and r[3][0]>1.1 and r[3][1]<.5 and r[4][0]==False and r[4][1]>1.4 and abs(r[5]-1.35)<.06, 'alberca: subes la escalera (%s m), te echas y nadas; la pelota de playa flota y la de boliche se hunde; nadando a la orilla te sales %s'%(r[0],r))
    # 5. charco: chapoteas y vas más despacio
    r=await ev("""(()=>{ const X=FREE.X+10,Y=FREE.Y,Z=FREE.Z-20, o=freeAddStatic({k:'n',a:'charco',b:0},X,Y,Z,0,true); player.pos.set(X,Y+.05,Z); player.vel.set(0,0,0); __run(.2); const x0=player.pos.x; SU.rip.length=0; __walk(.5,1,0); const wet=SU.rip.length>0, sp=(player.pos.x-x0)/.5;   /* (v237: el charco es agua de verdad: al caminar haces ondas y salpicas) */
      player.pos.set(X+6,Y+.05,Z); __run(.2); const x1=player.pos.x; __walk(.5,1,0); const sp2=(player.pos.x-x1)/.5; return [wet, +sp.toFixed(1), +sp2.toFixed(1)]; })()""")
    ok(r[0] and r[1]<r[2]*.8, 'charco: chapoteas y caminas más despacio (%s m/s en el agua, %s afuera) %s'%(r[1],r[2],r))
    # 6. tobogán de agua
    r=await ev("""(()=>{ const X=FREE.X-20,Y=FREE.Y,Z=FREE.Z+10, o=freeAddStatic({k:'v',a:'tobogan',b:5},X,Y,Z,0,true); player.pos.set(X,Y+.05,Z-4.6); player.vel.set(0,0,0); __run(.2); const acts=__act(); __do('Subir al tobogán');
      let top=0, ys=[]; __run(3.8,i=>{ if(player.pg) top=Math.max(top,player.pos.y-Y); }); return [acts&&acts[0], +top.toFixed(2), player.pg, +(player.pos.z-Z).toFixed(1), player.inWater, Math.abs(player.pos.x-X)<.3]; })()""")
    ok(r[0]=='Subir al tobogán' and r[1]>2.5 and r[2] is None and 4<r[3]<5.5 and r[4] and r[5], 'tobogán de agua: subes la escalera (%s m), te resbalas y caes con ¡splash! en su alberquita %s'%(r[1],r))
    # 7. carrito: manejas, subes la rampa y brincas, tumbas un dominó y se queda donde lo dejas
    r=await ev("""(()=>{ const X=FREE.X+25,Y=FREE.Y,Z=FREE.Z-35, o=freeAddStatic({k:'v',a:'carrito',b:0},X+.5,Y,Z+.5,0,true); freeAddStatic({k:'b',a:3,b:2},X+.5,Y,Z+12.5,0,true); const dm=freeAddStatic({k:'t',a:'domino',b:11},X+.5,Y,Z+22.5,0,true);
      player.pos.set(X+.5,Y+.05,Z-.6); player.vel.set(0,0,0); __run(.2); const acts=__act(); __do('Manejar el carrito'); const z0=o.root.position.z; let air=false, top=0;
      __run(3.2,()=>{ yaw=Math.PI; stick.y=-1; if(player.pg&&player.pg.drive){ if(player.pg.drive.air) air=true; top=Math.max(top,player.pg.drive.y-Y); } }); stick.y=0; __run(1.5);
      const moved=o.root.position.z-z0, knocked=dm.toy.st>0; const acts2=__act(); __do('Bajarse'); __run(1); return [acts&&acts[0], +moved.toFixed(1), air, +top.toFixed(2), knocked, acts2&&acts2[0], player.pg, +(o.z-(Z+.5)).toFixed(1), +o.root.position.distanceTo(new THREE.Vector3(o.x,o.y,o.z)).toFixed(2)]; })()""")
    ok(r[0]=='Manejar el carrito' and r[1]>15 and r[2] and r[3]>1.2 and r[4] and r[5]=='Bajarse' and r[6] is None and r[7]>15 and r[8]<.05, 'carrito: manejas (%s m), subes la rampa y ¡brincas! (%s m), tumbas el dominó y al bajarte se queda ahí %s'%(r[1],r[3],r))
    # 8. patineta (parado) y con una pared enfrente te detienes
    r=await ev("""(()=>{ const X=FREE.X-25,Y=FREE.Y,Z=FREE.Z-35, o=freeAddStatic({k:'v',a:'patineta',b:7},X+.5,Y,Z+.5,0,true); for(let i=-2;i<=2;i++) freeAddStatic({k:'b',a:0,b:0},X+.5+i,Y,Z+8.5,0,true);
      player.pos.set(X+.5,Y+.05,Z-.4); __run(.2); __do('Subirse a la patineta'); const pose=player.pg && pqVehPose(o,0); __run(3,()=>{ yaw=Math.PI; stick.y=-1; }); stick.y=0; const z=o.root.position.z-Z; __do('Bajarse'); __run(.5);
      return [pose && pose.sit===0, +z.toFixed(2), player.pg]; })()""")
    ok(r[0] and 5<r[1]<8.1 and r[2] is None, 'patineta: vas parado y la pared te detiene (llegaste a %s m, la pared está a 8) %s'%(r[1],r))
    # 9. se guarda (con el carrito donde lo dejaste)
    r=await ev("""(()=>{ freeSave(); const o=JSON.parse(localStorage.getItem('mundoPelucheLibre')); const car=o.s.find(e=>e[0]==='v'&&e[1]==='carrito'); car[5]+=35-.5; ui('toMenuBtn').click(); __run(.2); FREE.loaded=null; freeEnter(); __run(.3);
      const c2=FREE.pqv.find(q=>q.pq==='carrito'); suRecount(); return [o.s.filter(e=>e[0]==='n').length, car[5]>15, (FREE.nat||[]).length, (FREE.wat||[]).length, c2 && +(c2.z-FREE.Z+35-.5).toFixed(1), +SU.vol.toFixed(1)]; })()""")
    ok(r[0]==4 and r[1] and r[2]==4 and r[3]==1 and r[4]>15 and r[5]>15, 'se guarda: las plantas y el agua vuelven, y el carrito está donde lo dejaste %s'%r)
    # 10. editor de mapas: pestaña Naturaleza
    r=await ev("""(()=>{ ui('toMenuBtn').click(); menuModes(true); ui('mapBtn').click(); mapType='juego'; ui('mapName').value='Agua'; mapCreate(); const tabs=mapTabs().map(t=>t[0]).join(','); MED.tab='natura'; MED.sub='agua'; medRender();
      const cards=[...document.querySelectorAll('#medGrid .hed-card')].map(c=>c.textContent).join('|'); medDone(); return [tabs, cards.includes('Alberca') && cards.includes('Tobogán')]; })()""")
    ok(r[0]=='juego,bloques,fisica,parque,natura' and r[1], 'editor de mapas: Minijuego trae 🌳 Naturaleza (alberca, charco y tobogán) %s'%r)
    # 11. rendimiento: 60 árboles, 60 flores, 30 pastos, 4 albercas y 6 carritos
    r=await ev("""(async()=>{ const W=ms=>new Promise(r=>setTimeout(r,ms)); ui('toMenuBtn').click(); __run(.2); localStorage.removeItem('mundoPelucheLibre'); FREE.loaded=null; freeEnter(); FREE.objs.slice().forEach(freeDrop); FREE.dyn.slice().forEach(freeDrop); const X=FREE.X,Y=FREE.Y,Z=FREE.Z;
      player.pos.set(X,Y+.05,Z+50); for(let i=0;i<6;i++){ __run(.5); renderer.render(scene,camera); await W(600); } renderer.info.reset(); renderer.render(scene,camera); const base=renderer.info.render.calls;
      const T=['arbol','arbolflor','palmera'], F=['flores','pasto','arbusto']; for(let i=0;i<60;i++) freeAddStatic({k:'n',a:T[i%3],b:0},X-50+(i%12)*8+.5,Y,Z-50+Math.floor(i/12)*6+.5,0,true);
      for(let i=0;i<90;i++) freeAddStatic({k:'n',a:F[i%3],b:0},X-50+(i%15)*6+3.5,Y,Z-20+Math.floor(i/15)*4+.5,0,true); for(let i=0;i<4;i++) freeAddStatic({k:'n',a:'alberca',b:0},X+30,Y,Z-40+i*8,0,true); for(let i=0;i<6;i++) freeAddStatic({k:'v',a:'carrito',b:i},X+40,Y,Z-40+i*4,0,true);
      for(let i=0;i<10;i++){ __run(.5); renderer.render(scene,camera); await W(700); } renderer.info.reset(); renderer.render(scene,camera); const calls=renderer.info.render.calls-base;
      let t=clock.elapsedTime; const t0=performance.now(); for(let i=0;i<60;i++){ clock.elapsedTime=(t+=.05); update(.05,t); } return [freeOwn(), calls, +((performance.now()-t0)/60).toFixed(2)]; })()""")
    ok(r[0]==160 and r[1]<300 and r[2]<4, 'con 150 plantas, 4 albercas y 6 carritos: cada cuadro tarda %s ms y se dibujan %s cosas más %s'%(r[2],r[1],r))
    ok(not errs,'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
