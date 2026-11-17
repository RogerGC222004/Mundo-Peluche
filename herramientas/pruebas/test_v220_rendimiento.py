# v220: rendimiento para teléfonos lentos (el Huawei de Roger). Con su configuración (Mínima, ultra ligero, 30 m, sin sombras
# ni clima) el juego manda a dibujar mucho menos: de cada grupo de copias (hojas, troncos, rocas, flores…) solo las de cerca,
# los bombones de los portales ya no se dibujan desde toda la isla, en el Modo libre no se pintan las montañas de la isla,
# los carteles de instrucciones son 2 dibujos (antes 8), los grupos vacíos no gastan dibujo y el mapa se redibuja menos
# cuando el juego va lento. Lo que no se ve igual se choca (las rocas) y al regresar todo vuelve a aparecer.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
ROGER={"quality":"min","qDef":1,"ultra":True,"shadows":False,"weather":False,"fpsCap":"30","autoRes":False,"draw":30,"hints":False}
NORMAL={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateSky(.05); } scene.updateMatrixWorld(); };
  window.__D=()=>{ renderer.info.reset(); renderer.render(scene,camera); return [renderer.info.render.calls, renderer.info.render.triangles]; }; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    async def open_page(opts):
      ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True, device_scale_factor=2); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
      await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(opts))
      async def route(r):
        if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
        elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
        else: await r.abort()
      await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
      ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300); await ev(STEP)
      return ctx, pg, errs, ev
    ctx,pg,errs,ev=await open_page(ROGER)
    W="(async()=>{ const W=ms=>new Promise(r=>setTimeout(r,ms)); %s for(let k=0;k<10;k++){ __S(8); renderer.render(scene,camera); await W(350); } return %s; })()"
    # 1. con la configuración de Roger se dibuja mucho menos
    r=await ev(W%("freeEnter(); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z); player.facing=Math.PI; yaw=0;","[...__D(), farRelief.visible, deepFloor.visible]"))
    ok(r[0]<=32 and r[1]<20000 and r[2] is False and r[3] is False, 'Modo libre vacío: %s dibujos y %s triángulos (antes 42 y 108 mil), sin las montañas ni el fondo del mar de la isla'%(r[0],r[1]))
    r=await ev(W%("ui('toMenuBtn').click(); startGame(); player.pos.set(START.x,START.top+.05,START.z); player.facing=Math.PI; yaw=0;","[...__D(), farRelief.visible, deepFloor.visible]"))
    ok(r[1]<200000 and r[2] is True and r[3] is True, 'en el castillo: %s dibujos y %s triángulos (antes 139 y 363 mil); al volver a la isla vuelven las montañas'%(r[0],r[1]))
    r=await ev(W%("{ const x=PG.x+6, z=PG.z+10; player.pos.set(x,groundAt(x,z,99)+.05,z); } player.facing=Math.PI; yaw=0;","__D()"))
    ok(r[1]<100000, 'en el parque: %s dibujos y %s triángulos (antes 107 y 262 mil)'%(r[0],r[1]))
    r=await ev(W%("{ const x=FAIR.x+8, z=FAIR.z-FAIR.R-6; player.pos.set(x,groundAt(x,z,99)+.05,z); } player.facing=0; yaw=Math.PI;","__D()"))
    ok(r[0]<=140 and r[1]<120000, 'en la feria: %s dibujos y %s triángulos (antes 144 y 267 mil)'%(r[0],r[1]))
    # 2. de cada grupo de copias, solo las de cerca; al regresar vuelven
    FIND="""(()=>{ const T=MAP.trees[40]; let hit=null; for(const r of ICULL.L){ const m=r.m; if(m.material!==trunkMat) continue; for(let k=0;k<m.count;k++){ const a=m.instanceMatrix.array; if(Math.abs(a[k*16+12]-T[0])<.01 && Math.abs(a[k*16+14]-T[1])<.01){ hit=[r.N,m.count]; break; } } if(hit) break; } return hit; })()"""
    r1=await ev(W%("{ const T=MAP.trees[40], x=T[0]+5, z=T[1]+5; player.pos.set(x,groundAt(x,z,99)+.05,z); }",FIND))
    r2=await ev(W%("{ const T=MAP.trees[40], a=Math.atan2(T[1],T[0])+Math.PI, x=Math.cos(a)*150, z=Math.sin(a)*150; player.pos.set(x,groundAt(x,z,99)+.05,z); }",FIND))
    r3=await ev(W%("{ const T=MAP.trees[40], x=T[0]+5, z=T[1]+5; player.pos.set(x,groundAt(x,z,99)+.05,z); }",FIND))
    ok(r1 and r1[1]<r1[0] and r2 is None and r3 and r3[0]==r1[0], 'un árbol: se dibuja de cerca (con %s de %s troncos de su grupo), lejos no, y al regresar vuelve %s %s %s'%(r1 and r1[1], r1 and r1[0], r1, r2, r3))
    # 3. lo que no se dibuja igual se choca (los choques se arman con todas las copias)
    await ev("(async()=>{ for(let k=0;k<30;k++){ __S(2); acTick(); await new Promise(r=>setTimeout(r,60)); } return 1; })()")
    r=await ev("""(()=>{ let n=0, dyn=0, mv=0, full=0, obs=0; for(const R of ICULL.L){ const rec=AC.seen.get(R.m); if(!rec) continue; n++; if(rec.dyn) dyn++; if(rec.mv) mv++; if(rec.obs && rec.obs.length){ obs++; if(rec.obs.length>R.m.count) full++; } } return [n,dyn,mv,obs,full]; })()""")
    ok(r[0]>5 and r[1]==0 and r[2]==0 and r[3]>0 and r[4]>0, 'choques: los grupos de copias no se toman como "que se mueven" y sus choques se arman con todas las copias, aunque se dibujen menos (revisados, movidos, que se mueven, con choques, con más choques que dibujadas) %s'%r)
    # 4. los bombones de los portales: solo si estás cerca del castillo
    r=await ev("""(()=>{ const B=ICULL.L.filter(R=>R.N===580/2); return B.map(R=>[R.N,R.m.count,R.bs.radius<0]); })()""")
    ok(len(r)==2 and all(e[1]==0 and e[2] for e in r), 'lejos del castillo los bombones de los portales no se dibujan %s'%r)
    # 5. los carteles de instrucciones: 2 dibujos cada uno
    r=await ev("""(()=>{ const out=[]; scene.traverse(o=>{ if(o.isMesh && o.material && o.material.map && o.material.map.__paint && o.parent && o.parent!==scene) out.push(o.parent.children.filter(c=>c.isMesh).length); }); return [out.length, [...new Set(out)]]; })()""")
    ok(r[0]>=20 and r[1]==[2], 'los %s carteles de instrucciones son de 2 dibujos (madera + dibujo) %s'%(r[0],r))
    # 6. ultra ligero: tu peluche sencillo de lejos, detallado si acercas la cámara
    r=await ev(W%("{ const x=PG.x+6, z=PG.z+10; player.pos.set(x,groundAt(x,z,99)+.05,z); } camDist=5.5;","plush.userData.body.geometry===FJ_GEO.lo"))
    r2=await ev(W%("camDist=2.4;","plush.userData.body.geometry===FJ_GEO.body"))
    ok(r and r2, 'ultra ligero: tu peluche de lejos es el sencillo y si acercas la cámara el detallado %s %s'%(r,r2))
    # 7. huellas: solo se dibujan hasta la última que sigue viva
    r=await ev("""(()=>{ const F=scene.children.find(o=>o.isInstancedMesh && o.instanceMatrix.count===280); const a=F.count; decals.foot(player.pos.x,player.pos.y+.05,player.pos.z,0,true,clock.elapsedTime); const b=F.count; decals.update(clock.elapsedTime+PRINT_TIME+1); return [a,b,F.count]; })()""")
    ok(r[1]>=1 and r[2]==0, 'huellas: se dibujan solo las que hay (%s → %s → %s)'%tuple(r))
    # 8. el mapa se redibuja menos cuando el juego va lento
    r=await ev("""(()=>{ const i=hotbar.indexOf('map'); selectedSlot=i; holding=true; applyHeld(); frame.ema=.11; drawMap(true); const a=mapLast; drawMap(false); const b=mapLast; frame.ema=.016; mapLast-=70; drawMap(false); const c=mapLast; selectedSlot=0; holding=false; applyHeld(); return [a===b, c!==b]; })()""")
    ok(r==[True,True], 'mapa: a 9 cuadros por segundo no se redibuja en cada cuadro; a 60 sí cada 66 ms %s'%r)
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close()
    # 9. en calidad normal (sin ultra) también se dibujan solo las copias de cerca, y el peluche es el de siempre
    ctx,pg,errs,ev=await open_page(NORMAL)
    r=await ev(W%("startGame(); { const x=PG.x+6, z=PG.z+10; player.pos.set(x,groundAt(x,z,99)+.05,z); } player.facing=Math.PI; yaw=0;","[ICULL.L.length, ICULL.L.filter(R=>R.m.count<R.N).length, plush.userData.body.geometry===FJ_GEO.body, capsuleGeo(ARM_R,ARM_UP).attributes.position.count]"))
    ok(r[0]>10 and r[1]>5 and r[2] and r[3]==342, 'calidad Baja: %s grupos de copias, %s con solo las de cerca; el peluche y sus brazos como siempre %s'%(r[0],r[1],r))
    ok(not errs,'sin errores (calidad Baja) %s'%errs[:3]); await ctx.close()
    await b.close()
asyncio.run(m())
