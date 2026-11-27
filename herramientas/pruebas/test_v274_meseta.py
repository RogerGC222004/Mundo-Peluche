# v274: Meseta Champiñón (parte 1): la meseta, sus tres subidas (escalera, rampa en zigzag, espiral), hongos, trampolines y mirador
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
    W="const M=MES, go=(f,u,v)=>{ const [x,z]=mesAt(f,u,v); arWarp(x,groundAt(x,z,999)+.1,z,0); __run(.4); return [x,z]; }, face=(x,z)=>{ yaw=Math.atan2(-(x-player.pos.x),-(z-player.pos.z)); };"
    # 1. la meseta existe: alta, plana arriba, con nombre, mapa y hongos
    r=await ev("""(()=>{ %s const h=terrainH(M.x+10,M.z-8), f=M.acc[0]+1, [x,z]=mesAt(f,0,M.S+20); return [+(h-M.base).toFixed(1), +(terrainH(x,z)-M.base).toFixed(1), zoneName(M.x,M.z), TELEPORTS.some(t=>t.id==='meseta'), M.nSmall, M.nMid, M.bouncy.length, (M.colossal||[]).length]; })()"""%W)
    ok(r[0]>18 and abs(r[1])<1.5, 'la meseta mide %s m de alto y alrededor es llano (%s)'%(r[0],r[1]))
    ok(r[2]=='Meseta Champiñón' and r[3], 'se llama Meseta Champiñón y se puede ir desde el mapa %s'%r[2:4])
    ok(r[4]>300 and r[5]>40 and r[6]>8 and r[7]>=4, 'hongos: %s chiquitos, %s medianos, %s trampolines, %s colosales'%tuple(r[4:8]))
    # 2. la pared no se sube caminando
    r=await ev("""(()=>{ %s const f=M.acc[0]+1.1; go(f,0,M.S+6); face(M.x,M.z); keys['KeyW']=true; __run(5); keys['KeyW']=false; __run(.5); return [+(player.pos.y-M.base).toFixed(1), +(Math.hypot(player.pos.x-M.x,player.pos.z-M.z)-mesRim(f)).toFixed(1)]; })()"""%W)
    ok(r[1]>8.5 and r[0]<3, 'caminando contra la pared no se sube (altura %s m, a %s m de la orilla)'%(r[0],r[1]))
    # 3. la escalera: caminando se llega arriba
    r=await ev("""(()=>{ %s const f=M.acc[0], [x0,z0]=go(f,0,M.stair.L+3); keys['KeyW']=true; for(let i=0;i<50;i++){ const [tx,tz]=mesAt(f,0,-10); face(tx,tz); __run(.2); } keys['KeyW']=false; __run(.5); return [+(player.pos.y-M.top).toFixed(2), +(Math.hypot(player.pos.x-M.x,player.pos.z-M.z)-mesRim(f)).toFixed(1)]; })()"""%W)
    ok(abs(r[0])<1 and r[1]<0, 'por la escalera llegas arriba de la meseta %s'%r)
    # 4. bajar por la orilla: resbalas hasta el pie
    r=await ev("""(()=>{ %s const f=M.acc[0]+1.4; go(f,0,-6); const [tx,tz]=mesAt(f,0,40); keys['KeyW']=true; for(let i=0;i<20;i++){ face(tx,tz); __run(.2); } keys['KeyW']=false; __run(2); return [+(player.pos.y-terrainH(player.pos.x,player.pos.z)).toFixed(2), +(player.pos.y-M.base).toFixed(1)]; })()"""%W)
    ok(abs(r[0])<.3 and r[1]<2, 'si caminas por la orilla, bajas resbalando hasta el pie %s'%r)
    # 5. la rampa en zigzag: ida, vuelta, ida y el puente
    r=await ev("""(()=>{ %s const f=M.acc[1], hu=18, W2=3.2, v0=12; const pts=[[-hu-2,v0+1.6],[hu+1.6,v0+1.6],[hu+1.6,v0+4.8],[-hu-1.6,v0+4.8],[-hu-1.6,v0+8],[hu+1.6,v0+8],[hu+1.6,-6]]; go(f,pts[0][0],pts[0][1]); keys['KeyW']=true; let mx=0;
      for(let k=1;k<pts.length;k++){ const [tx,tz]=mesAt(f,pts[k][0],pts[k][1]); for(let i=0;i<60 && Math.hypot(player.pos.x-tx,player.pos.z-tz)>.9;i++){ face(tx,tz); __run(.15); mx=Math.max(mx,player.pos.y); } } keys['KeyW']=false; __run(.5); return [+(player.pos.y-M.top).toFixed(2), +(mx-M.top).toFixed(2), +(Math.hypot(player.pos.x-M.x,player.pos.z-M.z)-mesRim(f)).toFixed(1)]; })()"""%W)
    ok(abs(r[0])<1 and r[2]<0, 'por la rampa en zigzag y su puente llegas arriba %s'%r)
    # 6. la espiral de hongos repisa
    r=await ev("""(()=>{ %s const S=M.slabs.find(s=>s.t==='hx'); const rm=(S.r0+S.r1)/2; let a=S.a0-.35; arWarp(S.x+Math.cos(a)*(S.r1+2.5),groundAt(S.x+Math.cos(a)*(S.r1+2.5),S.z+Math.sin(a)*(S.r1+2.5),999)+.1,S.z+Math.sin(a)*(S.r1+2.5),0); __run(.4); keys['KeyW']=true;
      for(let i=0;i<260;i++){ const pa=Math.atan2(player.pos.z-S.z,player.pos.x-S.x); a=pa+.45; face(S.x+Math.cos(a)*rm,S.z+Math.sin(a)*rm); __run(.12); if(player.pos.y>M.top-.3) break; }
      const f=M.spiral.f, [tx,tz]=mesAt(f,0,-6); for(let i=0;i<40;i++){ face(tx,tz); __run(.15); } keys['KeyW']=false; __run(.5); return [+(player.pos.y-M.top).toFixed(2), +(Math.hypot(player.pos.x-M.x,player.pos.z-M.z)-mesRim(f)).toFixed(1)]; })()"""%W)
    ok(abs(r[0])<1 and r[1]<0, 'por la espiral alrededor del hongo colosal llegas arriba %s'%r)
    # 7. los trampolines de la escalera de hongos te avientan al siguiente, hasta el mirador
    r=await ev("""(()=>{ %s const B=M.bouncy.filter(b=>b.th!==undefined && Math.hypot(b.x-M.mir.x,b.z-M.mir.z)<15); const out=[]; for(const b of B){ arWarp(b.x,b.top+.05,b.z,0); player.grounded=true; player.vy=0; __run(.1); __run(3.2); out.push(+(player.pos.y-b.th).toFixed(2)); } return [B.length,out]; })()"""%W)
    ok(r[0]==3 and all(abs(v)<.8 for v in r[1]), 'los 3 trampolines te avientan al siguiente hongo y al mirador %s'%r)
    # 8. en el mirador: no te caes caminando (barandal de honguitos)
    r=await ev("""(()=>{ %s const C=M.mir; arWarp(C.x,C.top+.1,C.z,0); __run(.5); keys['KeyW']=true; for(let i=0;i<30;i++){ yaw=1.1; __run(.15); } keys['KeyW']=false; __run(.5); return [+(player.pos.y-C.top).toFixed(2), +Math.hypot(player.pos.x-C.x,player.pos.z-C.z).toFixed(1)]; })()"""%W)
    ok(abs(r[0])<.8, 'en el mirador el barandal no te deja caer %s'%r)
    # 9. de noche los hongos brillan
    r=await ev("""(()=>{ const d0=sky.dayK; sky.dayK=0; mesUpdate(.016); const g=MES_GLOW.value; sky.dayK=d0; mesUpdate(.016); return [+g.toFixed(2), +MES_GLOW.value.toFixed(2), !!MES.sp]; })()""")
    ok(r[0]>.4 and r[2], 'de noche los hongos brillan y hay esporas de luz %s'%r)
    # 10. el suelo es micelio gris en toda la zona (y no en el desierto ni el valle)
    r=await ev("""(()=>{ const a=1.43, m=coastMidR(a), n=coastRN(a); const x=Math.cos(a)*(m+(n-m)*.5), z=Math.sin(a)*(m+(n-m)*.5); return [+mycW(x,z).toFixed(2), +mycW(MES.x,MES.z).toFixed(2), mycW(DES.pyr.x,DES.pyr.z), mycW(VALLE.plaza.x,VALLE.plaza.z)]; })()""")
    ok(r[0]>.9 and r[1]>.9 and r[2]==0 and r[3]==0, 'el suelo de la zona y de la meseta es micelio gris %s'%r)
    # 11. bosque de hongos: muchos medianos y «árboles»
    r=await ev("""(()=>{ const k={}; MES.mid.forEach(q=>k[q[3]]=(k[q[3]]||0)+1); return [MES.mid.length, k.arbol||0, (MES.colossal||[]).length]; })()""")
    ok(r[0]>1500 and r[1]>150 and r[2]>=12, 'bosque de hongos: %s medianos, %s hongos árbol, %s colosales'%tuple(r))
    # 12. peluchitos hongo: aparecen, con ojitos saltones; saludan, se esconden y te siguen
    r=await ev("""(()=>{ const a=1.45, m=coastMidR(a), n=coastRN(a), x=Math.cos(a)*(m+(n-m)*.62), z=Math.sin(a)*(m+(n-m)*.62); arWarp(x,terrainH(x,z)+.1,z,0); for(let i=0;i<12;i++) __run(1); return [MF.list.length, MF.I?MF.I.ew.count:0]; })()""")
    ok(r[0]>=4 and r[1]==2*r[0], 'aparecen peluchitos hongo (%s) con sus ojitos saltones (%s)'%tuple(r))
    r=await ev("""(()=>{ const A=MF.list[0]; player.pos.set(A.x+4,terrainH(A.x+4,A.z),A.z); player.vel.set(0,0,0); A.waveCd=0; A.follow=false; __run(.5); const wave=A.waveT>0;
      player.pos.set(A.x+6,terrainH(A.x+6,A.z),A.z); for(let i=0;i<8;i++){ player.vel.set(-7,0,0); update(.05,clock.elapsedTime+=.05); } const hid=+A.hide.toFixed(2);
      player.vel.set(0,0,0); player.pos.set(A.x+3,terrainH(A.x+3,A.z),A.z); __run(3); __run(3.5); const fol=A.follow;
      keys['KeyW']=true; yaw=Math.PI/2; __run(5); keys['KeyW']=false; __run(2); const d=Math.hypot(A.x-player.pos.x,A.z-player.pos.z); return [wave, hid, fol, +d.toFixed(1)]; })()""")
    ok(r[0], 'si te acercas caminando, te saluda')
    ok(r[1]>.7, 'si llegas corriendo, se esconde bajo su sombrero (%s)'%r[1])
    ok(r[2] and r[3]<6, 'si te quedas quieto junto a él, te sigue (queda a %s m después de caminar)'%r[3])
    print('errores', errs[:3]); ok(not errs, 'sin errores')
    await b.close()
asyncio.run(m())
