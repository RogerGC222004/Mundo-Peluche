# v275: Bosque Frondoso (partes 1 y 2): árboles gigantes, casa del árbol (espiral, plataforma con barandal, casita, puentes colgantes), arroyo con piedras y cascadita, estanque, fogata y luciérnagas
import asyncio, sys, os
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open(os.environ.get('JUEGO','/home/claude/mundo-peluche.html')).read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":780,"height":360}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false}));")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(800)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t)
    await ev("window.__run=(sec)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); update(.05,t); } }; startGame(); 1"); await pg.wait_for_timeout(1200); await ev("__run(1); 1")
    W="const F=FOR, T=F.th, S=F.stream, face=(x,z)=>{ yaw=Math.atan2(-(x-player.pos.x),-(z-player.pos.z)); };"
    # 1. el bosque existe
    r=await ev("""(()=>{ %s let mono=true; for(let i=1;i<S.L.length;i++) if(S.L[i]>S.L[i-1]+.001) mono=false; return [F.giants.length, zoneName(F.fire.x,F.fire.z), TELEPORTS.some(t=>t.id==='bosque'), mono, +(S.L[S.ci-3]-S.L[S.ci]).toFixed(2), terrainH(F.pond.x,F.pond.z)<SEA_Y, F.nCover]; })()"""%W)
    ok(r[0]>=60, 'árboles gigantes: %s'%r[0]); ok(r[1]=='Bosque Frondoso' and r[2], 'se llama Bosque Frondoso y se puede ir desde el mapa')
    ok(r[3] and r[4]>=1.2, 'el arroyo siempre va de bajada y tiene una cascadita de %s m'%r[4]); ok(r[5], 'el estanque tiene agua'); ok(r[6]>3000, 'piso frondoso: %s helechos, arbustos y matitas'%r[6])
    # 2. la espiral sube hasta la casa del árbol
    r=await ev("""(()=>{ %s const H=F.slabs.find(s=>s.t==='hx'), rm=(H.r0+H.r1)/2; let a=H.a0-.35; arWarp(H.x+Math.cos(a)*(H.r1+2.5),groundAt(H.x+Math.cos(a)*(H.r1+2.5),H.z+Math.sin(a)*(H.r1+2.5),999)+.1,H.z+Math.sin(a)*(H.r1+2.5),0); __run(.4); keys['KeyW']=true;
      for(let i=0;i<300;i++){ const pa=Math.atan2(player.pos.z-H.z,player.pos.x-H.x); a=pa+.45; face(H.x+Math.cos(a)*rm,H.z+Math.sin(a)*rm); __run(.12); if(player.pos.y>T.y-.3) break; }
      for(let i=0;i<8;i++){ const pa=Math.atan2(player.pos.z-H.z,player.pos.x-H.x); face(H.x+Math.cos(pa+.3)*7,H.z+Math.sin(pa+.3)*7); __run(.15); } keys['KeyW']=false; __run(.5); return [+(player.pos.y-T.y).toFixed(2), +Math.hypot(player.pos.x-T.x,player.pos.z-T.z).toFixed(1)]; })()"""%W)
    ok(abs(r[0])<.6, 'por la espiral alrededor del tronco llegas a la plataforma de la casa del árbol %s'%r)
    # 3. el barandal no te deja caer y la casita tiene paredes (y se entra por la puerta)
    r=await ev("""(()=>{ %s const aIn=Math.atan2(-T.z,-T.x), side=aIn+1.3; arWarp(T.x+Math.cos(side)*6.5,T.y+.1,T.z+Math.sin(side)*6.5,0); __run(.4); keys['KeyW']=true; for(let i=0;i<20;i++){ face(T.x+Math.cos(side)*30,T.z+Math.sin(side)*30); __run(.15); } keys['KeyW']=false; __run(.3);
      const rail=[+(player.pos.y-T.y).toFixed(2), +Math.hypot(player.pos.x-T.x,player.pos.z-T.z).toFixed(1)];
      const ac=aIn+Math.PI, r0=F.giants[0].r+.15; arWarp(T.x+Math.cos(ac)*(r0+.9),T.y+.1,T.z+Math.sin(ac)*(r0+.9),0); __run(.3); keys['KeyW']=true; for(let i=0;i<25;i++){ face(T.x+Math.cos(ac)*30,T.z+Math.sin(ac)*30); __run(.15); } keys['KeyW']=false; __run(.3);
      return [rail, +Math.hypot(player.pos.x-T.x,player.pos.z-T.z).toFixed(1), +(player.pos.y-T.y).toFixed(2)]; })()"""%W)
    ok(abs(r[0][0])<.5 and r[0][1]<8.6, 'el barandal de la plataforma no te deja caer %s'%r[0])
    ok(r[1]>5 and r[1]<7.9 and abs(r[2])<.5, 'entras a la casita por la puerta y la pared del fondo te detiene (a %s m del tronco)'%r[1])
    # 4. los puentes colgantes llevan a los árboles vecinos (y no te caes por los lados)
    r=await ev("""(()=>{ %s const out=[]; for(const g of F.giants.filter(g=>g.plat!==undefined)){ const a=Math.atan2(g.z-T.z,g.x-T.x); arWarp(T.x+Math.cos(a)*7,T.y+.1,T.z+Math.sin(a)*7,0); __run(.3); keys['KeyW']=true; let wob=0;
        for(let i=0;i<60;i++){ face(g.x,g.z); if(i%%6===3){ keys['KeyA']=true; } else keys['KeyA']=false; __run(.15); if(Math.hypot(player.pos.x-g.x,player.pos.z-g.z)<g.r+2.6) break; } keys['KeyW']=false; keys['KeyA']=false; __run(.3);
        out.push([+(player.pos.y-(g.y+g.plat)).toFixed(2), +(Math.hypot(player.pos.x-g.x,player.pos.z-g.z)).toFixed(1)]); } return out; })()"""%W)
    ok(len(r)==3 and all(abs(a)<.6 and d<6 for a,d in r), 'por los 3 puentes colgantes llegas a los árboles vecinos %s'%r)
    # 5. las piedras del arroyo: se cruza brincando sin mojarse
    r=await ev("""(()=>{ %s const st=F.stones[2]; arWarp(st.x,st.top+.2,st.z,0); __run(.5); return [+(player.pos.y-st.top).toFixed(2), !player.swim]; })()"""%W)
    ok(abs(r[0])<.1 and r[1], 'puedes pararte en las piedras del arroyo %s'%r)
    # 6. la fogata: troncos para sentarse y el fuego no se atraviesa
    r=await ev("""(()=>{ %s const C=F.fire, nb=BENCHES.filter(b=>Math.hypot(b.x-C.x,b.z-C.z)<6).length; arWarp(C.x+6,C.y+.1,C.z,0); __run(.3); keys['KeyW']=true; for(let i=0;i<20;i++){ face(C.x,C.z); __run(.15); } keys['KeyW']=false; return [nb, +Math.hypot(player.pos.x-C.x,player.pos.z-C.z).toFixed(2), FOR_FX.flames.length]; })()"""%W)
    ok(r[0]==4 and r[1]>1.5 and r[2]==3, 'fogata con fuego y 4 troncos para sentarse; no te metes al fuego %s'%r)
    # 7. de noche: luciérnagas y la fogata alumbra
    r=await ev("""(()=>{ %s const C=F.fire; arWarp(C.x+10,C.y+.1,C.z,0); const d0=sky.dayK; sky.dayK=0; forUpdate(.016); forUpdate(.016); const ff=!!FOR_FX.ff && FOR_FX.ff.visible, gl=FOR_FX.glow.material.opacity; sky.dayK=d0; return [ff, +gl.toFixed(2)]; })()"""%W)
    ok(r[0] and r[1]>.5, 'de noche hay luciérnagas y la fogata alumbra %s'%r)
    # 8. el muelle del estanque: se pesca y salen peces de agua dulce
    r=await ev("""(()=>{ const rods=PIER.rods.filter(r=>r.pond), r=rods[0]; arWarp(r.stand[0],r.Y+.1,r.stand[1],0); __run(.5); const onDock=Math.abs(player.pos.y-r.Y)<.1; const a=pondActions(); const L=a&&a[0]?a[0].label:''; const got=[];
      for(let k=0;k<6;k++){ const b=pondActions(); if(b&&b[0]) b[0].run(); __run(.2); const F=player.fish; if(!F) break; F.T=.3; __run(1); for(let i=0;i<F.N;i++) reelFish(); const sp=F.sp; __run(1.5); got.push(sp); }
      return [rods.length, onDock, L, got.every(id=>FISH[id]&&FISH[id].fresh), got.length, FISH.filter(f=>f.fresh).length, !!FISH.find(f=>f.n==='Koi dorada' && f.r===3)]; })()""")
    ok(r[0]==4 and r[1] and r[2].startswith('Pescar'), 'muelle en el estanque con 4 cañas %s'%r[:3])
    ok(r[3] and r[4]>=5, 'en el estanque salen peces de agua dulce (%s pescados)'%r[4])
    ok(r[5]==12 and r[6], '12 peces nuevos de agua dulce, con la koi dorada legendaria')
    # 9. animalitos del bosque
    r=await ev("""(()=>{ const a=3.6, m=coastMidR(a), n=coastRN(a), x=Math.cos(a)*(m+(n-m)*.5), z=Math.sin(a)*(m+(n-m)*.5); arWarp(x,terrainH(x,z)+.1,z,0); for(let i=0;i<15;i++) __run(1); const k={}; FORA.list.forEach(A=>k[A.kind]=(k[A.kind]||0)+1); return [FORA.list.length, JSON.stringify(k)]; })()""")
    ok(r[0]>=5, 'aparecen animalitos del bosque: %s'%r[1])
    r=await ev("""(()=>{ const p=player.pos; const o=obstacles.filter(o=>!o.walk && o.top>p.y+20 && o.r<1.2 && Math.hypot(o.x-p.x,o.z-p.z)<120).sort((a,b)=>Math.hypot(a.x-p.x,a.z-p.z)-Math.hypot(b.x-p.x,b.z-p.z))[0]; if(!o) return [false,0];
      arWarp(o.x+12,terrainH(o.x+12,o.z)+.1,o.z,0); __run(.3); const A=forAnimalSpawn('ardilla',o.x+4,o.z); player.pos.set(A.x+9,terrainH(A.x+9,A.z),A.z); player.vel.set(0,0,0); let mx=0; keys['KeyW']=true; keys['ShiftLeft']=true; for(let i=0;i<40;i++){ if(i<14) yaw=Math.atan2(-(A.x-player.pos.x),-(A.z-player.pos.z)); if(i===14){ keys['KeyW']=false; keys['ShiftLeft']=false; } __run(.1); mx=Math.max(mx,A.y-terrainH(A.x,A.z)); } keys['KeyW']=false; keys['ShiftLeft']=false; return [!!A.tree, +mx.toFixed(2)]; })()""")
    ok(r[1]>1, 'la ardilla se trepa al árbol si llegas corriendo %s'%r)   # (v276: caminando ya no se asusta)
    r=await ev("""(()=>{ const g=FOR.giants[8]; arWarp(g.x+20,terrainH(g.x+20,g.z)+.1,g.z,0); for(let i=0;i<4;i++) __run(1); const ow=FORA.list.find(A=>A.kind==='buho'); if(!ow) return ['sin búho']; const d0=sky.dayK; sky.dayK=1; forUpdate(.016); const day=ow.ey.visible; sky.dayK=0; player.pos.set(ow.x+8,terrainH(ow.x+8,ow.z),ow.z); camera.position.set(ow.x+8,ow.y,ow.z); forUpdate(.016); const nightEyes=ow.ey.visible; sky.dayK=d0; return [day, nightEyes, +(ow.y-terrainH(ow.x,ow.z)).toFixed(1)]; })()""")
    ok(r[0] is False and r[1] is True and r[2]>5, 'el búho duerme de día en su rama y de noche abre los ojitos %s'%r)
    print('errores', errs[:3]); ok(not errs, 'sin errores')
    await b.close()
asyncio.run(m())
