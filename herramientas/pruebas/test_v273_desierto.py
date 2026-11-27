# v273: Desierto Canela (parte 1): dunas, arena (huellas, hundirse), cactus con carita, oasis, pirámide (escalones, túnel, cuarto y cofre)
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
    # 1. el desierto existe: dunas de 1 a 10 m, cactus, oasis con agua, nombre
    r=await ev("""(()=>{ let mn=1e9, mx=-1e9; const a=.4, m=coastMidR(a), n=coastRN(a); for(let f=.2;f<=.7;f+=.004){ const r=m+(n-m)*f, x=Math.cos(a)*r, z=Math.sin(a)*r; const h=terrainH(x,z); mn=Math.min(mn,h); mx=Math.max(mx,h); }
      const O=DES.oasis; return [+(mx-mn).toFixed(1), DES.cactiN, terrainH(O.x,O.z)<SEA_Y, zoneName(Math.cos(a)*(m+(n-m)*.4),Math.sin(a)*(m+(n-m)*.4)), TELEPORTS.some(t=>t.id==='desierto')]; })()""")
    ok(r[0]>4 and r[0]<40, 'hay dunas (subidas y bajadas de %s m en una línea)'%r[0])
    ok(r[1]>300, 'cactus de peluche: %s'%r[1]); ok(r[2], 'el oasis tiene agua'); ok(r[3]=='Desierto Canela' and r[4], 'se llama Desierto Canela y se puede ir desde el mapa %s'%r[3:])
    # 2. arena: huellas y hundirse un poquito
    r=await ev("""(()=>{ const a=.4, m=coastMidR(a), n=coastRN(a); let x=0,z=0; for(let f=.3;f<.7;f+=.01){ const r=m+(n-m)*f; x=Math.cos(a)*r; z=Math.sin(a)*r; if(desSandAt(x,z) && !obsNear(x,z).some(o=>Math.hypot(o.x-x,o.z-z)<o.r+3)) break; }
      arWarp(x,groundAt(x,z,999)+.1,z,0); __run(1.5); const s0=decals?1:0; keys['KeyW']=true; __run(2.5); keys['KeyW']=false; __run(.6);
      return [desSandAt(player.pos.x,player.pos.z), +(player.sinkK||0).toFixed(3), onSandAt(player.pos.x,player.pos.z,player.pos.y)]; })()""")
    ok(r[0] and r[2], 'caminando en la arena del desierto (cuenta como arena: deja huellas y polvito)')
    ok(r[1]>.05, 'te hundes un poquito en la arena (%s m)'%r[1])
    # 3. la pirámide: subir caminando por los escalones hasta arriba
    r=await ev("""(()=>{ const P=DES.pyr; arWarp(P.x+1.9,P.H+.1,P.z+P.B+4,0); __run(1); yaw=0; keys['KeyW']=true; let top=0; for(let i=0;i<120;i++){ yaw=0; __run(.25); top=Math.max(top,player.pos.y-P.H); } keys['KeyW']=false; __run(.5);
      return [+top.toFixed(2), +(P.L*P.SH).toFixed(2)]; })()""")
    ok(r[0]>r[1]-.5, 'se sube caminando hasta arriba de la pirámide (%s de %s m)'%(r[0],r[1]))
    # 4. el túnel y el cuarto: entrar caminando, llegar al cofre y abrirlo
    r=await ev("""(()=>{ const P=DES.pyr; arWarp(P.x-P.B-4,P.H+.1,P.z,0); __run(1); yaw=-Math.PI/2; keys['KeyW']=true; let minx=1e9; for(let i=0;i<80;i++){ yaw=-Math.PI/2; __run(.2); minx=Math.min(minx,Math.abs(player.pos.x-(P.x+.6))); if(Math.hypot(player.pos.x-DES.chest.x,player.pos.z-DES.chest.z)<1.9) break; } keys['KeyW']=false; __run(.4);
      const inside=Math.abs(player.pos.x-P.x)<4 && Math.abs(player.pos.z-P.z)<4 && player.pos.y<P.H+1; const a=desActions(); const lab=a&&a[0]?a[0].label:''; if(a&&a[0]&&!a[0].disabled){ const c0=coins; a[0].run(); __run(.6); return [inside,lab,coins-c0,desDone()]; } return [inside,lab,0,desDone()]; })()""")
    ok(r[0], 'se entra caminando por el túnel hasta el cuarto de adentro')
    ok(r[1]=='Abrir el cofre de la pirámide' and r[2]==100 and r[3], 'el cofre da 100 monedas y se vacía hasta mañana %s'%r)
    # 5. paredes: desde adentro del túnel no se atraviesa hacia los lados
    r=await ev("""(()=>{ const P=DES.pyr; arWarp(P.x-P.B+4,P.H+.1,P.z,0); __run(.5); yaw=Math.PI; keys['KeyW']=true; for(let i=0;i<12;i++){ yaw=Math.PI; __run(.25); } keys['KeyW']=false; return [+(player.pos.z-P.z).toFixed(2), +(player.pos.y-P.H).toFixed(2)]; })()""")
    ok(abs(r[0])<1.3 and r[1]<.3, 'las paredes del túnel no se atraviesan %s'%r)
    # --- parte 2 ---
    # 6. tabla de arena: en una duna, deslizarse, brincar y bajarse solito al pararse
    r=await ev("""(()=>{ const a=.4, m=coastMidR(a), n=coastRN(a); let best=null; for(let f=.25;f<.7;f+=.004){ const r=m+(n-m)*f, x=Math.cos(a)*r, z=Math.sin(a)*r, e=2, g=Math.hypot(terrainH(x+e,z)-terrainH(x-e,z),terrainH(x,z+e)-terrainH(x,z-e))/(2*e); if(desSandAt(x,z) && (!best||g>best[2]) && !obsNear(x,z).some(o=>Math.hypot(o.x-x,o.z-z)<o.r+6)) best=[x,z,g]; }
      const [x,z]=best; arWarp(x,groundAt(x,z,999)+.1,z,0); __run(.6); const lab=(desActions()||[])[0]; const L=lab?lab.label:''; if(lab) lab.run(); __run(.1); const on=player.pg && player.pg.k==='sandb';
      let mx=0, air=false; for(let i=0;i<20;i++){ __run(.2); if(player.pg && player.pg.sb){ mx=Math.max(mx,Math.hypot(player.pg.sb.vx,player.pg.sb.vz)); if(i===5){ jump(); } if(player.pg.sb.air) air=true; } }
      __run(10); return [L,on,+mx.toFixed(1),air,0,+best[2].toFixed(2)]; })()""")
    await asyncio.sleep(.3)
    r[4]=await ev("(()=>{ __run(.2); const S=player.pg&&player.pg.sb; return S?[S.slow,Math.hypot(S.vx,S.vz),S.air,S.crash,player.pg.k]:true; })()")
    ok(r[0]=='Tabla de arena' and r[1], 'en la arena aparece «Tabla de arena» y te subes %s'%r[:2])
    ok(r[2]>2.5 and r[3], 'la tabla se desliza por la duna (hasta %s m/s) y brinca'%r[2])
    ok(r[4] is True, 'al pararse te bajas solito')
    # 7. camello: subirse, caminar y bajarse
    r=await ev("""(()=>{ const K=DES.camel; arWarp(K.x+1.5,groundAt(K.x+1.5,K.z,999)+.1,K.z,0); __run(.6); const a=desActions(); const L=a&&a[0]?a[0].label:''; if(a&&a[0]) a[0].run(); __run(.2); const on=player.pg && player.pg.k==='camel', x0=player.pg&&player.pg.cm?player.pg.cm.x:0, z0=player.pg&&player.pg.cm?player.pg.cm.z:0;
      keys['KeyW']=true; __run(4); keys['KeyW']=false; __run(1); const cm=player.pg&&player.pg.cm, d=cm?Math.hypot(cm.x-x0,cm.z-z0):0, high=cm?player.pos.y-terrainH(cm.x,cm.z):0; stopPlay(); __run(.5);
      return [L,on,+d.toFixed(1),+high.toFixed(2),!player.pg,K.idle.visible,!(K.ride&&K.ride.visible)]; })()""")
    ok(r[0]=='Montar el camello' and r[1], 'junto al oasis te subes al camello %s'%r[:2])
    ok(r[2]>8 and r[3]>1.8, 'el camello camina (%s m en 4 s) y vas sentado arriba (%s m)'%(r[2],r[3]))
    ok(r[4] and r[5] and r[6], 'te bajas y el camello vuelve a su lugar')
    # 8. remolino: te levanta girando y «Tirarse» te saca
    r=await ev("""(()=>{ let W=desWhirlPos(0,Date.now()/1000), tries=0; while(W.k<.8 && tries<20){ tries++; __run(1); W=desWhirlPos(0,Date.now()/1000); } if(W.k<.8) return ['sin remolino']; arWarp(W.x+.5,groundAt(W.x+.5,W.z,999)+.1,W.z,0); for(let i=0;i<10 && !player.whirl;i++){ W=desWhirlPos(0,Date.now()/1000); player.pos.set(W.x+.5,terrainH(W.x,W.z),W.z); __run(.1); }
      const got=!!player.whirl; __run(1.5); const up=player.pos.y-terrainH(player.pos.x,player.pos.z); startDive(); __run(.2); return [got,+up.toFixed(1),!player.whirl]; })()""")
    ok(r[0] and r[1]>2.5 and r[2], 'un remolino te levanta (%s m) y con «Tirarse» sales %s'%(r[1] if len(r)>1 else '',r))
    # 9. animalitos
    r=await ev("""(()=>{ const a=.4, m=coastMidR(a), n=coastRN(a), rr=m+(n-m)*.45, x=Math.cos(a)*rr, z=Math.sin(a)*rr; arWarp(x,groundAt(x,z,999)+.1,z,0); __run(14); return [DESA.list.length, [...new Set(DESA.list.map(A=>A.kind))].join(',')]; })()""")
    ok(r[0]>=4, 'aparecen animalitos cerca: %s (%s)'%(r[0],r[1]))
    print('errores', errs[:3]); ok(not errs,'sin errores')
    await b.close()
asyncio.run(m())
