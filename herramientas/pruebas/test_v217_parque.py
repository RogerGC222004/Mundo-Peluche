# v217: 🎡 Parque en el Modo libre — piezas que se mueven (columpio, sube y baja, carrusel, puerta, elevador) y
# juguetes con física (dominós en cadena y en esquina, bolos con la bola de boliche, torre que se derrumba),
# «Volver a pararlos», pintar, guardar, editor desde arriba y rendimiento.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("if(!sessionStorage.getItem('t217')){ sessionStorage.setItem('t217','1'); localStorage.clear(); } localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
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
      window.__act=()=>{ const a=freeActions(); return a?a.map(x=>x&&x.label):null; }; window.__do=(lab)=>{ const a=freeActions()||[]; const x=a.find(q=>q&&q.label===lab); if(x) x.run(); return !!x; }; 1""")
    # 1. el menú: pestaña 🎡 Parque con 5 que se mueven y 4 juguetes (con su fotito)
    r=await ev("""(async()=>{ freeEnter(); window.requestAnimationFrame=()=>0; FREE.objs.slice().forEach(freeDrop); FREE.dyn.slice().forEach(freeDrop); freeOpenBox();
      const tab=[...ui('freeTabs').children].find(b=>b.textContent.includes('Parque')); tab.click(); const subs=[...ui('freeSubs').children].map(b=>b.textContent).join('|'); const a=[...ui('freeGrid').children].map(b=>b.textContent);
      [...ui('freeSubs').children][1].click(); const t=[...ui('freeGrid').children].map(b=>b.textContent); for(let i=0;i<40;i++) freeThumbPump(); const bad=Object.keys(FTH.c).filter(k=>/^[vt]:/.test(k) && FTH.c[k]==='x');
      ui('freeBox').hidden=true; return [subs, a.join(','), t.join(','), bad.length]; })()""")
    ok('Se mueven' in r[0] and 'Juguetes' in r[0] and r[1]=='Columpio,Sube y baja,Carrusel,Puerta,Elevador' and r[2]=='Dominó,Fila de 8 dominós,Bolos (10),Torre de bloques' and r[3]==0, 'Objetos → 🎡 Parque: «Se mueven» (5) y «Juguetes» (4), todos con su fotito %s'%r)
    # 2. ponerlos caminando (la fila son 8 dominós y los bolos 10)
    r=await ev("""(()=>{ const X=FREE.X,Y=FREE.Y,Z=FREE.Z; const put=(sel,x,z,f)=>{ player.pos.set(X+x,Y+.05,Z+z); player.facing=f||0; freeSelect(sel); freePlace(); freeSelect(null); };
      put({k:'v',a:'columpio',b:5},-20,-20); put({k:'v',a:'subebaja',b:2},-12,-20); put({k:'v',a:'carrusel',b:0},-4,-20); put({k:'v',a:'puerta',b:6},4,-20); put({k:'v',a:'elevador',b:7},12,-20);
      const n0=freeOwn(); put({k:'t',a:'fila',b:11},-20,10); const n1=freeOwn(); put({k:'t',a:'bolos',b:0},-10,10); const n2=freeOwn(); put({k:'t',a:'torre',b:0},0,10);
      return [n0, n1-n0, n2-n1, freeOwn(), FREE.pqv.length, FREE.toys.length]; })()""")
    ok(r==[5,8,10,24,5,19], 'se ponen caminando: 5 que se mueven, la fila son 8 dominós, los bolos 10 y la torre 1 %s'%r)
    # 3. columpio: te subes, te columpias, te bajas
    r=await ev("""(()=>{ const o=FREE.pqv.find(q=>q.pq==='columpio'), a=o.r*Math.PI/2; player.pos.set(o.x+Math.sin(a)*.6,FREE.Y+.05,o.z+Math.cos(a)*.6); player.facing=a+Math.PI; player.vel.set(0,0,0); __run(.2);
      const acts=__act(); __do('Columpiarse'); const ys=[], zs=[]; __run(5,i=>{ if(i%5===0){ zs.push(player.pos.z-o.z); ys.push(player.pos.y); } }); const amp=o.ride.amp, k=player.pg&&player.pg.k;
      const acts2=__act(); __do('Bajarse'); __run(.3); return [acts&&acts[0], k, +amp.toFixed(2), +(Math.max(...zs)-Math.min(...zs)).toFixed(2), +(Math.max(...ys)-Math.min(...ys)).toFixed(2), acts2&&acts2[0], player.pg, +(Math.hypot(player.pos.x-o.x,player.pos.z-o.z)).toFixed(1), player.grounded]; })()""")
    ok(r[0]=='Columpiarse' and r[1]=='fmv' and r[2]>.5 and r[3]>1.2 and r[4]>.2 and r[5]=='Bajarse' and r[6] is None and r[7]>=1, 'columpio: «Columpiarse» te sienta y te columpia (ida y vuelta %s m), «Bajarse» te deja enfrente %s'%(r[3],r))
    # 4. sube y baja (dos asientos) y carrusel (te subes y das vueltas; parado también te lleva)
    r=await ev("""(()=>{ const o=FREE.pqv.find(q=>q.pq==='subebaja'), U=o.root.userData.pq; U.seats[1].getWorldPosition(_pqV); player.pos.set(_pqV.x,FREE.Y+.05,_pqV.z+.6); __run(.2); const acts=__act(); __do('Subirse al sube y baja');
      const zs=[]; __run(3,i=>zs.push(U.mov.rotation.z)); const seat=player.pg&&player.pg.i; jump(); __run(.2); return [acts&&acts[0], seat, +(Math.max(...zs)-Math.min(...zs)).toFixed(2), player.pg]; })()""")
    ok(r[0]=='Subirse al sube y baja' and r[2]>.3 and r[3] is None, 'sube y baja: te subes a un lado, sube y baja, y con Saltar te bajas %s'%r)
    r=await ev("""(()=>{ const o=FREE.pqv.find(q=>q.pq==='carrusel'), U=o.root.userData.pq; U.seats[0].getWorldPosition(_pqV); const dx=_pqV.x-o.x, dz=_pqV.z-o.z, d=Math.hypot(dx,dz); player.pos.set(o.x+dx/d*2,FREE.Y+.05,o.z+dz/d*2); __run(.1);
      const acts=__act(); __do('Subirse al carrusel'); const a0=Math.atan2(player.pos.x-o.x,player.pos.z-o.z); __run(2); const a1=Math.atan2(player.pos.x-o.x,player.pos.z-o.z); __do('Bajarse'); __run(.2); const out=Math.hypot(player.pos.x-o.x,player.pos.z-o.z);
      player.pos.set(o.x+1,o.box.max.y,o.z); player.vy=0; player.grounded=true; __run(.1); const b0=Math.atan2(player.pos.x-o.x,player.pos.z-o.z); __run(2); const b1=Math.atan2(player.pos.x-o.x,player.pos.z-o.z), on=Math.abs(player.pos.y-o.box.max.y)<.1;
      const dd=x=>Math.abs(Math.atan2(Math.sin(x),Math.cos(x))); return [acts&&acts[0], +dd(a1-a0).toFixed(2), +out.toFixed(1), +dd(b1-b0).toFixed(2), on]; })()""")
    ok(r[0]=='Subirse al carrusel' and r[1]>.8 and r[2]>2 and r[3]>.8 and r[4], 'carrusel: sentado das vueltas (%s rad en 2 s), te bajas afuera; parado encima también te lleva (%s rad) %s'%(r[1],r[3],r))
    # 5. elevador: te sube 4 m y te baja
    r=await ev("""(()=>{ const o=FREE.pqv.find(q=>q.pq==='elevador'); let t=0; while(pqElevY(o,pqClock())>.01 && t<200){ __run(.1); t++; } player.pos.set(o.x,o.box.max.y,o.z); player.vy=0; player.grounded=true; __run(.1);
      let top=0; __run(7,()=>{ top=Math.max(top,player.pos.y-FREE.Y); }); let low=99; __run(6,()=>{ low=Math.min(low,player.pos.y-FREE.Y); }); return [+top.toFixed(2), +low.toFixed(2), Math.abs(player.pos.x-o.x)<1]; })()""")
    ok(r[0]>4 and r[1]<.4 and r[2], 'elevador: parado encima te sube hasta %s m y te vuelve a bajar %s'%(r[0],r))
    # 6. puerta: cerrada no deja pasar; cuando llegas se abre sola y luego se cierra
    r=await ev("""(()=>{ const o=FREE.pqv.find(q=>q.pq==='puerta'); player.pos.set(o.x,FREE.Y+.05,o.z+8); __run(1); const closed=o.solid; const p=new THREE.Vector3(o.x,FREE.Y+.05,o.z+.3); freeCollide(p); const pushed=Math.abs(p.z-(o.z+.3))>.2;
      player.pos.set(o.x,FREE.Y+.05,o.z+2); __run(.8); const open=[+o.ride.door.toFixed(2), o.solid]; player.pos.set(o.x,FREE.Y+.05,o.z-1.5); __run(.2); player.pos.set(o.x,FREE.Y+.05,o.z-9); __run(1.5); return [closed, pushed, ...open, o.solid]; })()""")
    ok(r==[True,True,1,False,True], 'puerta: cerrada te detiene; al llegar se abre sola (pasas) y al irte se cierra %s'%r)
    # 7. dominós: empujas el primero y se caen todos (también dando vuelta a la izquierda en una esquina)
    r=await ev("""(()=>{ const X=FREE.X+25, Y=FREE.Y, Z=FREE.Z-10, D=[]; const put=(x,z,r)=>{ const o=freeAddStatic({k:'t',a:'domino',b:11},X+x,Y,Z+z,r,true); D.push(o); return o; };
      for(let i=0;i<4;i++) put(0,i,0); put(0,4,1); for(let i=1;i<=3;i++) put(-i,4,1);
      player.pos.set(X,Y+.05,Z-1.4); player.facing=0; __run(.2); const acts=__act(); __do('Empujar'); __run(5);
      return [acts&&acts.includes('Empujar'), D.filter(o=>o.toy.st===2).length, D.length, D[4].toy.s===-1 && D[4].toy.dx<-.9, D.slice(5).every(o=>o.toy.dx<-.9), +Math.max(...D.map(o=>o.toy.th)).toFixed(2)]; })()""")
    ok(r[0] and r[1]==r[2]==8 and r[3] and r[4], 'dominós: «Empujar» el primero y se caen los %s en cadena, y en la esquina dan vuelta a la izquierda %s'%(r[1],r))
    r=await ev("""(()=>{ const F=FREE.toys.filter(o=>o.pq==='domino' && Math.abs(o.x-(FREE.X-19.5))<.6 && o.z>FREE.Z+5).sort((a,b)=>a.z-b.z); const f=F[0]; player.pos.set(f.x,FREE.Y+.05,f.z-1.6); player.facing=0; player.vel.set(0,0,4); __run(.9,()=>player.vel.set(0,0,4)); player.vel.set(0,0,0); __run(4);
      return [F.length, F.filter(o=>o.toy.st===2).length, F.filter(o=>o.toy.th<1.2 && o.toy.st===2).length]; })()""")
    ok(r[0]==8 and r[1]==8 and r[2]>=5, 'la fila de 8: caminas contra el primero y se caen todos, recargados uno en otro (%s recargados) %s'%(r[2],r))
    # 8. bolos con la bola de boliche
    r=await ev("""(()=>{ const B=FREE.toys.filter(o=>o.pq==='bolo'), cx=B.reduce((s,o)=>s+o.x,0)/10, cz=B.reduce((s,o)=>s+o.z,0)/10, head=B.reduce((a,o)=>o.z<a.z?o:a,B[0]);
      const ball=freeAddDyn('boliche',head.x,FREE.Y,head.z-6,true); ball.v.set(0,0,9); player.pos.set(cx+8,FREE.Y+.05,cz); __run(5); const down=B.filter(o=>o.toy.st).length; return [down, +Math.max(...B.map(o=>Math.hypot(o.toy.ox,o.toy.oz))).toFixed(2)]; })()""")
    ok(r[0]>=6 and r[1]>.2, 'bolos: la bola de boliche tumba %s de 10 (y salen rodando hasta %s m) %s'%(r[0],r[1],r))
    # 9. torre: corres contra ella y se derrumba
    r=await ev("""(()=>{ const o=FREE.toys.find(q=>q.pq==='torre'), U=o.root.userData.pq; player.pos.set(o.x,FREE.Y+.05,o.z-2.2); player.facing=0; player.vel.set(0,0,5); __run(.6,()=>{ player.vel.set(0,0,5); }); player.vel.set(0,0,0); player.pos.set(o.x+8,FREE.Y+.05,o.z); __run(5);
      const L=U.blocks.filter(B=>B.loose); return [o.toy.st, L.length, L.filter(B=>B.sleep).length, +Math.max(...L.map(B=>B.m.position.y-FREE.Y)).toFixed(2), +Math.max(...L.map(B=>Math.hypot(B.m.position.x-o.x,B.m.position.z-o.z))).toFixed(1)]; })()""")
    ok(r[0]==2 and r[1]>=6 and r[2]==r[1] and r[3]<1.2 and r[4]>.8, 'torre: corres contra ella y se caen %s bloques, quedan acostados en el piso (el más alto a %s m) %s'%(r[1],r[3],r))
    # 10. volver a pararlos
    r=await ev("""(()=>{ const o=FREE.toys.find(q=>q.pq==='torre'); player.pos.set(o.x,FREE.Y+.05,o.z-3); __run(.1); const acts=__act(); __do('Volver a pararlos'); __run(.2); const U=o.root.userData.pq;
      const B=FREE.toys.filter(q=>q.pq==='bolo'); player.pos.set(B[0].x,FREE.Y+.05,B[0].z-3); __run(.1); __do('Volver a pararlos'); __run(.1);
      return [acts&&acts.includes('Volver a pararlos'), o.toy.st, U.blocks.every(b=>!b.loose && b.m.parent===o.root), B.filter(q=>q.toy.st).length, Math.abs(B[0].root.userData.pq.tip.position.x)<1e-6]; })()""")
    ok(r==[True,0,True,0,True], '«Volver a pararlos»: la torre se vuelve a armar y los bolos se paran %s'%r)
    # 11. pintar: el carrusel y un dominó sí; un bolo no
    r=await ev("""(()=>{ const c=FREE.pqv.find(q=>q.pq==='carrusel'), d=FREE.toys.find(q=>q.pq==='domino'), bo=FREE.toys.find(q=>q.pq==='bolo'); freePaintSet(true); FREE.pcol=3; FREE.tgt=c; freePaintDo(); FREE.pcol=8; FREE.tgt=d; freePaintDo(); FREE.tgt=bo; freePaintDo(); const msg=ui('toast').textContent; freePaintSet(false);
      return [c.sel.b, d.sel.b, msg, !!c.root.userData.pq.mov.parent, d.toy.st===2 ? Math.abs(d.root.userData.pq.tip.rotation.x)>.3 : true]; })()""")
    ok(r[0]==3 and r[1]==8 and 'no se puede pintar' in r[2] and r[3] and r[4], '🎨 se pintan el carrusel y los dominós (aunque estén caídos siguen caídos); los bolos no %s'%r)
    # 12. se guarda y vuelve
    r=await ev("""(()=>{ freeSave(); const o=JSON.parse(localStorage.getItem('mundoPelucheLibre')); const ks=o.s.map(e=>e[0]+':'+e[1]); ui('toMenuBtn').click(); __run(.2); FREE.loaded=null; freeEnter(); __run(.3);
      return [ks.filter(k=>k[0]==='v').length, ks.filter(k=>k==='t:domino').length, ks.filter(k=>k==='t:bolo').length, ks.filter(k=>k==='t:torre').length, FREE.pqv.length, FREE.toys.length, FREE.toys.every(q=>q.toy.st===0), FREE.pqv.find(q=>q.pq==='carrusel').sel.b]; })()""")
    ok(r==[5,16,10,1,5,27,True,3], 'se guarda: al volver están los 5 juegos y los 27 juguetes (parados) con sus colores %s'%r)
    # 13. editor de mapas desde arriba: pestaña Parque; la fila se pone de un toque y ↶ la quita completa
    r=await ev("""(()=>{ ui('toMenuBtn').click(); menuModes(true); ui('mapBtn').click(); mapType='mundo'; ui('mapName').value='Parque'; mapCreate(); const tabs=mapTabs().map(t=>t[0]).join(',');
      MED.tab='parque'; MED.sub='juguetes'; medRender(); const cards=[...document.querySelectorAll('#medGrid .hed-card')].map(c=>c.textContent).join('|'); medSelect({k:'t',a:'fila',b:11}); const n0=freeOwn();
      medPlace({x:FREE.X+.5,y:FREE.Y,z:FREE.Z+.5,ok:true}); const n1=freeOwn(); medUndo(); const n2=freeOwn(); medDone(); return [tabs, cards.includes('Fila de 8'), n1-n0, n2-n0]; })()""")
    ok(r[0].startswith('juego,bloques,fisica,parque') and r[1] and r[2]==8 and r[3]==0, 'editor de mapas: pestaña 🎡 Parque; la fila pone 8 dominós y ↶ Deshacer los quita todos %s'%r)
    # 14. rendimiento: 300 dominós, 20 juegos que se mueven y 10 torres
    r=await ev("""(async()=>{ const W=ms=>new Promise(r=>setTimeout(r,ms)); ui('toMenuBtn').click(); __run(.2); localStorage.removeItem('mundoPelucheLibre'); freeEnter(); FREE.objs.slice().forEach(freeDrop); FREE.dyn.slice().forEach(freeDrop); const X=FREE.X,Y=FREE.Y,Z=FREE.Z;
      player.pos.set(X,Y+.05,Z+50); for(let i=0;i<8;i++){ __run(.5); renderer.render(scene,camera); await W(700); } renderer.info.reset(); renderer.render(scene,camera); const base=renderer.info.render.calls;
      for(let i=0;i<300;i++) freeAddStatic({k:'t',a:'domino',b:i%12},X-45+(i%30)*1+.5,Y,Z-45+Math.floor(i/30)*3+.5,0,true);
      const V=['columpio','subebaja','carrusel','puerta','elevador']; for(let i=0;i<20;i++) freeAddStatic({k:'v',a:V[i%5],b:i%12},X-40+(i%5)*8,Y,Z+10+Math.floor(i/5)*8,0,true);
      for(let i=0;i<10;i++) freeAddStatic({k:'t',a:'torre',b:0},X+20+(i%5)*3,Y,Z-20+Math.floor(i/5)*3,0,true);
      player.pos.set(X,Y+.05,Z+50); for(let i=0;i<10;i++){ __run(.5); renderer.render(scene,camera); await W(700); } renderer.info.reset(); renderer.render(scene,camera); const calls=renderer.info.render.calls-base;
      let t=clock.elapsedTime; const t0=performance.now(); for(let i=0;i<60;i++){ clock.elapsedTime=(t+=.05); update(.05,t); } const ms=(performance.now()-t0)/60; return [freeOwn(), calls, +ms.toFixed(2)]; })()""")
    ok(r[0]==330 and r[2]<4 and r[1]<400, 'con 300 dominós, 20 juegos moviéndose y 10 torres: cada cuadro tarda %s ms y se dibujan %s cosas %s'%(r[2],r[1],r))
    ok(not errs,'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
