# v238 (Modo libre): tu peluche se mancha con lo que toca. Lodo en las patas, pintura de panza, miel que te cae encima (gotea y te
# frena), slime en pegotes, arenita (más si estás mojado), espuma en la cabeza y agua (te ves mojadito; te lava lo demás). Se va solito
# con el tiempo. Funciona en el frijolito, el Chibi, el Amigurumi y tu mascota. Y el lodo del piso se seca y se agrieta.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.033); update(.033,t); petsUpdate(.033,t); } };
  window.__CLR=()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); FREE.hold=null; freeSelect(null); };
  window.__CLEAN=()=>{ stClear(myStn); __S(2); };
  window.__POOL=(p,dep,x0,z0,col,s)=>{ const m=SU.cs; for(let x=-1;x<=1.01;x+=m) for(let z=-1;z<=1.01;z+=m) suPour(FREE.X+(x0||0)+x,FREE.Z+(z0||0)+z,p,col||0,dep*m*m,.1,s); __S(15); };
  window.__WALK=(x0,z0,n)=>{ player.pos.set(FREE.X+x0,FREE.Y+.05,FREE.Z+z0); player.vel.set(0,0,0); __S(2); for(let i=0;i<n;i++){ stick.x=0; stick.y=-1; yaw=-Math.PI/2; __S(1); } stick.y=0; __S(2); };
  window.__WR=o=>{ let n=0, t=0; o.traverse(m=>{ if(m.isMesh && m.material && m.material.isMeshStandardMaterial){ t++; if(m.material.userData && m.material.userData.stOrig) n++; } }); return [n,t]; };
  window.__RES=()=>{ __CLR(); suClear(); FU.pts.length=0; SU.drops.length=0; __CLEAN(); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-12); __S(3); }; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type=='error' and ('shader' in m.text.lower() or 'webgl' in m.text.lower() or 'manchas' in m.text) else None)
    pg.on("console", lambda m: errs.append(m.text) if m.type=='warning' and 'manchas' in m.text else None)
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev("(()=>{ freeEnter(); return 1; })()"); await ev(STEP)

    # 1. caminar por el lodo: lodo en las patas hasta donde te llegó
    r=await ev("""(()=>{ __RES(); __POOL(3,.4,0,0); __WALK(-2.2,0,60); renderer.render(scene,camera); const S=myStn; return [+S.A[3].toFixed(2), +S.L[3].toFixed(2), +S.F[3].toFixed(2), +S.T[3].toFixed(2), __WR(plush), stPack(S)]; })()""")
    ok(r[0]>.8 and r[1]>.25 and r[1]<.75 and r[2]==0 and r[3]==0, '🟤 al caminar por el lodo te quedan las patas embarradas hasta donde te llegó (%s m; panza %s, cabeza %s)'%(r[1],r[2],r[3]))
    ok(r[4][0]>8, 'y se pinta en tu peluche (%s de %s piezas manchadas)'%tuple(r[4]))
    ok(isinstance(r[5],str) and r[5].startswith('3'), 'y va en tu presencia para que te vean así: «%s»'%r[5])

    # 2. tirarte de panza en la pintura: la panza del color de la pintura
    r=await ev("""(()=>{ __RES(); __POOL(5,.06,0,0,3); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z); player.vel.set(0,0,0); __S(3); startDive(); let mx=0; for(let i=0;i<45;i++){ __S(1); mx=Math.max(mx,player.diveAngle||0); } const S=myStn; return [+S.F[5].toFixed(2), +S.A[5].toFixed(2), S.col===suHex(5,suCol(3),255)]; })()""")
    ok(r[0]>.5 and r[1]>.8 and r[2], '🎨 si te tiras de panza en la pintura quedas pintado de ese color (panza %s)'%r[0])

    # 3. una bola de miel que te cae en la cabeza: miel arriba, gotea y te frena
    r=await ev("""(()=>{ __RES(); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z); __S(2); const v=suVolOf(.3); SU.balls.push({p:4,c:0,s:0,r:.3,v,x:FREE.X,y:FREE.Y+3.6,z:FREE.Z,vx:0,vy:-2,vz:0,t:.5,m:new THREE.Mesh(_suSph,suBallMat(4,0,0))}); __S(30);
        const T4=myStn.T[4]; const v0=SU.vol; let dr=0; for(let i=0;i<120;i++){ __S(1); dr=Math.max(dr,SU.drops.filter(d=>d.p===4).length); }
        return [+T4.toFixed(2), dr]; })()""")
    ok(r[0]>.5, '🍯 si te cae una bola de miel en la cabeza, te quedas con miel arriba (%s)'%r[0])
    ok(r[1]>=1, 'y vas goteando miel de verdad (%s gotitas a la vez)'%r[1])

    # 4. miel en las patas: caminas más lento
    r=await ev("""(()=>{ __RES(); __POOL(4,.08,0,0); __WALK(-2.2,0,50); const a4=myStn.A[4]; const run=(zz)=>{ player.pos.set(FREE.X+6,FREE.Y+.05,FREE.Z+zz); player.vel.set(0,0,0); __S(2); for(let i=0;i<30;i++){ stick.x=0; stick.y=-1; yaw=-Math.PI/2; __S(1); } const x0=player.pos.x; for(let i=0;i<30;i++){ stick.x=0; stick.y=-1; yaw=-Math.PI/2; __S(1); } stick.y=0; return (player.pos.x-x0)/(30*.033); };
        const conM=run(-4), sl=SU.slow; __CLEAN(); myStn.A[4]=0; __S(60); const sinM=run(6);   /* (lejos de donde goteó la miel) */ return [+a4.toFixed(2), +conM.toFixed(2), +sinM.toFixed(2), +sl.toFixed(2)]; })()""")
    ok(r[0]>.8 and r[1]<r[2]*.88, '🐝 con miel pegada en las patas caminas más lento (%s m/s contra %s limpio)'%(r[1],r[2]))

    # 5. arena: seca solo un poquito en las patas; si estás mojado se te pega más
    r=await ev("""(()=>{ __RES(); __POOL(7,.2,0,0); __WALK(-2.2,0,50); const a=[+myStn.A[7].toFixed(2), +myStn.L[7].toFixed(2)]; __CLEAN(); myStn.A[1]=1; myStn.L[1]=1; __WALK(-2.2,0,50); return a.concat([+myStn.A[7].toFixed(2), +myStn.L[7].toFixed(2)]); })()""")
    ok(r[0]>0 and r[0]<=.65 and r[1]<.5, '🏖️ en la arena seca solo te queda arenita en las patas (%s, hasta %s m)'%(r[0],r[1]))
    ok(r[2]>r[0] and r[3]>r[1], 'y si vienes mojado se te pega más y más arriba (%s, hasta %s m)'%(r[2],r[3]))

    # 6. espuma: si te metes a un montón de espuma te queda en la cabeza
    r=await ev("""(()=>{ __RES(); __POOL(6,2.2,0,0); __WALK(-2.2,0,50); return [+myStn.A[6].toFixed(2), +myStn.T[6].toFixed(2), +myStn.L[6].toFixed(2)]; })()""")
    ok(r[0]>.5 and (r[1]>.5 or r[2]>1.2), '🫧 al meterte a la espuma se te queda hasta en la cabeza (arriba %s, hasta %s m)'%(r[1],r[2]))

    # 7. el agua: te ves mojado y te lava lo demás
    r=await ev("""(()=>{ __RES(); __POOL(3,.4,-4,0); __WALK(-6.2,0,60); const m0=myStn.A[3]; __CLR(); const X=FREE.X, Z=FREE.Z; for(let a=-3;a<=3;a++) for(let c=-3;c<=3;c++) if(Math.abs(a)===3||Math.abs(c)===3) for(let y=0;y<2;y++) freeAddStatic({k:'b',a:0,b:6},X+a,FREE.Y+y,Z+c,0,true); __S(1); const m=SU.cs; for(let x=-2.4;x<=2.41;x+=m) for(let z=-2.4;z<=2.41;z+=m) suPour(X+x,Z+z,1,0,1.3*m*m,.1); __S(30);
        player.pos.set(X,FREE.Y+.8,Z); __S(100); return [+m0.toFixed(2), +myStn.A[3].toFixed(2), +myStn.A[1].toFixed(2), +myStn.L[1].toFixed(2), player.swim]; })()""")
    ok(r[4] and r[2]>.8 and r[3]>1, '💧 al nadar quedas mojadito (agua %s, hasta %s m)'%(r[2],r[3]))
    ok(r[0]>.8 and r[1]<.2, 'y el agua te lava el lodo (%s → %s)'%(r[0],r[1]))

    # 8. se va solita con el tiempo; ya limpio, el peluche vuelve a su material normal
    r=await ev("""(()=>{ __RES(); myStn.A[3]=1; myStn.L[3]=.5; myStn.A[5]=1; myStn.F[5]=1; __S(5); const w0=__WR(plush)[0]; const a=[]; for(let k=0;k<4;k++){ __S(300); a.push(+myStn.A[3].toFixed(2)); } __S(3000); __S(30); return [w0, a, +myStn.A[3].toFixed(3), +myStn.A[5].toFixed(3), myStn.on, __WR(plush)[0]]; })()""")
    ok(r[1][0]<1 and r[1][1]<r[1][0] and r[1][3]<r[1][1], '⏳ las manchas se van quitando solitas, poco a poco (lodo %s)'%r[1])
    ok(not r[4] and r[5]==0 and r[0]>0, 'y al final quedas limpio: el peluche vuelve a ser el de siempre (%s piezas con mancha)'%r[5])

    # 9. el Chibi y el Amigurumi también se manchan, y cambiarte de ropa manchado no rompe nada
    r=await ev("""(()=>{ const out=[]; for(const av of ['av_chibi','av_amigu']){ __RES(); applyOutfit(plush,Object.assign({},wardrobe.eq,{body:av})); __S(2); myStn.A[3]=1; myStn.L[3]=.6; __S(3); renderer.render(scene,camera); const w=__WR(plush);
        applyOutfit(plush,Object.assign({},wardrobe.eq,{body:av})); __S(20); renderer.render(scene,camera); const w2=__WR(plush); const tag=plush.userData.legs.map(l=>l.children.find(m=>m.isMesh && m.material===tagMat)).find(Boolean); out.push([plush.userData.av, w[0], w2[0], w2[1], tag?tag.visible:null]); }
        applyOutfit(plush,Object.assign({},wardrobe.eq,{body:''})); __S(2); __CLEAN(); __S(30); return out; })()""")
    ok(r[0][0]=='c' and r[0][1]>3 and r[0][2]>3 and r[0][4] is not True, '🧒 el Chibi se mancha (y después de cambiarle algo sigue manchado: %s piezas; la etiqueta sigue escondida)'%r[0][2])
    ok(r[1][0]=='a' and r[1][1]>3 and r[1][2]>3, '🧶 el Amigurumi también (%s piezas)'%r[1][2])

    # 10. tu mascota se mancha por donde camina
    r=await ev("""(()=>{ __RES(); const id=Object.keys(PET_BY)[0]; pets.eq=id; __POOL(3,.35,0,0); player.pos.set(FREE.X-3.5,FREE.Y+.05,FREE.Z); __S(40); for(let i=0;i<90;i++){ stick.x=0; stick.y=-1; yaw=-Math.PI/2; __S(1); } stick.y=0; __S(10); const R=myPet.inst && myPet.inst.P.root; const S=R && R.userData.stn;
        const res=[!!R, S?+S.A[3].toFixed(2):null, R?__WR(R)[0]:0]; pets.eq=null; __S(3); return res; })()""")
    ok(r[0] and r[1] is not None and r[1]>.3 and r[2]>0, '🐶 tu mascota también se embarra cuando pasa por el lodo (%s; %s piezas)'%(r[1],r[2]))

    # 11. el lodo del piso se seca: se aclara, se agrieta, ya no se escurre y te puedes parar encima; con agua se ablanda
    r=await ev("""(()=>{ __RES(); __POOL(3,.25,0,0); const q=()=>suCell(FREE.X,FREE.Z,false), c0=q()[0].c[q()[1]]; __S(2700); const c1=q()[0].c[q()[1]]; suBuild(q()[0]); const col=suHex(3,c1,0)!==suHex(3,0,0);
        const P=suPack(); suClear(); suUnpack(P); __S(2); const c2=q()[0].c[q()[1]];
        player.pos.set(FREE.X,FREE.Y+.6,FREE.Z); __S(30); const py=player.pos.y-FREE.Y, top=suSandTop(FREE.X,FREE.Z)-FREE.Y; __CLEAN(); __WALK(-2.2,0,50); const st=myStn.A[3];
        for(let i=0;i<40;i++){ suPour(FREE.X,FREE.Z,1,0,.004,.6); __S(1); } __S(60); const c3=q()[0].c[q()[1]]; return [c0, c1, col, c2, +py.toFixed(2), +top.toFixed(2), +st.toFixed(2), c3]; })()""")
    ok(r[0]<25 and r[1]>170 and r[2], '☀️ el lodo del piso se va secando solito y se aclara (%s → %s de 255)'%(r[0],r[1]))
    ok(abs(r[3]-r[1])<20, '💾 lo seco se guarda con el mundo (%s → %s)'%(r[1],r[3]))
    ok(abs(r[4]-r[5])<.08 and r[6]<.2, '🧱 ya seco es una costra: te paras encima y no te embarra (pies a %s m, costra a %s m; mancha %s)'%(r[4],r[5],r[6]))
    ok(r[7]<r[1]-60, '💧 y con agua se vuelve a ablandar (%s → %s)'%(r[1],r[7]))

    # 12. rendimiento: manchado y sin manchar
    r=await ev("""(()=>{ __RES(); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z); __S(3); camera.position.set(FREE.X,FREE.Y+1.4,FREE.Z+2.6); camera.lookAt(FREE.X,FREE.Y+.9,FREE.Z); const T=()=>{ for(let i=0;i<3;i++) renderer.render(scene,camera); const t0=performance.now(); for(let i=0;i<10;i++){ __S(1); renderer.render(scene,camera); } return (performance.now()-t0)/10; };
        const a=T(); for(const p of [1,3,4,5,6,7]){ myStn.A[p]=1; myStn.L[p]=.4; } myStn.T[4]=1; myStn.F[5]=1; __S(3); const b2=T(); __CLEAN(); return [+a.toFixed(1), +b2.toFixed(1)]; })()""")
    ok(r[1]<r[0]*1.6+3, '⚡ con 6 manchas a la vez el cuadro tarda %s ms contra %s ms limpio (aquí, sin tarjeta de video: dibujar es lentísimo)'%(r[1],r[0]))
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
