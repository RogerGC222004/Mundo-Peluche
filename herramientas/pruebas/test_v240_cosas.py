# v240 (Modo libre): las cosas con física se manchan justo donde tocaron y con la forma del contacto (cuadrícula 3D pegada a la cosa: gira con ella); el agua las
# lava; la miel y el slime las hacen pegajosas (casi no ruedan); embarradas o pintadas dejan rastro; si las agarras o te pegan, te manchan.
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
  window.__PL=(p,dep)=>{ __CLR(); suClear(); FU.pts.length=0; SU.drops.length=0; const X=FREE.X, Y=FREE.Y, Z=FREE.Z; for(let a=-5;a<=5;a++) for(let c=-5;c<=5;c++) if(Math.abs(a)===5||Math.abs(c)===5) for(let y=0;y<2;y++) freeAddStatic({k:'b',a:0,b:6},X+a,Y+y,Z+c,0,true); __S(1); const m=SU.cs; for(let x=-4.4;x<=4.41;x+=m) for(let z=-4.4;z<=4.41;z+=m) suPour(X+x,Z+z,p,0,dep*m*m,.1); player.pos.set(X+6.5,Y+.05,Z+6.5); player.vel.set(0,0,0); __S(40); wvOff(); __S(1); };
  window.__AT=(x,z)=>{ player.pos.set(FREE.X+x,FREE.Y+.05,FREE.Z+z); player.vel.set(0,0,0); player.vy=0; player.facing=0; yaw=Math.PI; FREE.ppPrev=null; __S(2); };
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




    window_js="""window.__VXW=(d)=>{ const V=d.root.userData.stn.vx; d.root.updateMatrixWorld(true); const e=V.bone.matrixWorld.elements, P=V.P, out=[]; for(let i=0;i<VX_N3;i++){ const x=P[i*3], y=P[i*3+1], z=P[i*3+2]; out.push([e[0]*x+e[4]*y+e[8]*z+e[12], e[1]*x+e[5]*y+e[9]*z+e[13], e[2]*x+e[6]*y+e[10]*z+e[14], V.t[i], V.a[i]]); } return out; }; 1"""
    await ev(window_js)
    # 1. una caja que se mete en el lodo: se mancha exactamente lo que quedó debajo de la superficie (raya recta)
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,-12); const X=FREE.X, Y=FREE.Y, Z=FREE.Z, m=SU.cs; for(let x=-1;x<=1.01;x+=m) for(let z=-1;z<=1.01;z+=m) suPour(X+x,Z+z,3,0,.25*m*m,.1); __S(20);
        const c=freeAddDyn('caja',X,Y+.8,Z,true); __S(60); const top=suAt(c.root.position.x,c.root.position.z)[2]; const W=__VXW(c); let up=0, dn=0, dnM=0, mx=-9; for(const w of W){ if(w[3]===3 && w[4]>0){ mx=Math.max(mx,w[1]); } if(w[1]<top-.03){ dn++; if(w[3]===3 && w[4]>0) dnM++; } else if(w[1]>top+.03){ up++; } }
        camera.position.set(X+1.5,Y+1.5,Z+2); camera.lookAt(X,Y+.3,Z); renderer.render(scene,camera); let wr=0; c.root.traverse(q=>{ if(q.isMesh && q.material && q.material.userData && q.material.userData.stOrig) wr++; });
        return [+(mx-top).toFixed(3), dn, dnM, wr, renderer.info.programs.filter(p=>p.diagnostics).length]; })()""")
    ok(r[1]>0 and r[2]>=r[1]*.95 and r[0]<.03 and r[3]>0, '📦 la caja que se mete al lodo se embarra exactamente hasta donde llegó el lodo: todo lo de abajo (%s de %s cuadritos) y nada arriba de la raya (%s cm)'%(r[2],r[1],round(r[0]*100,1)))
    ok(r[4]==0, '🧩 las cosas manchadas se dibujan sin errores')

    # 2. una bola de pintura le pega a la pelota: un círculo justo donde pegó, que gira con la pelota
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,-12); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; const g=freeAddDyn('goma',X,Y+.3,Z,true); __S(30); const p=g.root.position, r=.13, mm=new THREE.Mesh(_suSph,suBallMat(5,suCol(4),255)); FREE.g.add(mm);
        SU.balls.push({x:p.x-1.2,y:p.y,z:p.z,vx:7,vy:.6,vz:0,r,p:5,c:suCol(4),s:255,v:suVolOf(r),t:.5,m:mm}); for(let i=0;i<14 && SU.balls.length;i++) __S(1); g.v.set(0,0,0); const cen=()=>{ const W=__VXW(g); let sx=0,sy=0,sz=0,n=0; for(const w of W) if(w[3]===5 && w[4]>0){ sx+=w[0]; sy+=w[1]; sz+=w[2]; n++; } return n?[sx/n-g.root.position.x,sy/n-g.root.position.y,sz/n-g.root.position.z,n]:null; };
        const a=cen(); g.spin.rotateZ(1.2); const b2=cen(); return [a&&a.map(v=>+v.toFixed(2)), b2&&b2.map(v=>+v.toFixed(2))]; })()""")
    ok(r[0] is not None and r[0][0]<-.1 and abs(r[0][2])<.1, '🎯 una bola de pintura le pega a la pelota y la mancha justo de ese lado (centro de la mancha %s)'%r[0])
    ok(r[1] is not None and abs(r[1][1]-r[0][1])+abs(r[1][0]-r[0][0])>.05, '🔄 y la mancha gira con la pelota (%s → %s)'%(r[0],r[1]))

    # 2b. rueda sobre una capita de pintura: se pinta una franja (lo que tocó el piso al girar), no toda
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,-12); const X=FREE.X, Y=FREE.Y, Z=FREE.Z, m=SU.cs; for(let x=-.8;x<=.81;x+=m) for(let z=-.8;z<=.81;z+=m) suPour(X+x,Z+z,5,SU_F|0x2a6bff,.02*m*m,.1); __S(20); const g=freeAddDyn('goma',X-1.4,Y+.3,Z,true); __S(10); g.v.set(2.5,0,0); freeWake(g); __S(45);
        const V=g.root.userData.stn.vx, P=V.P; let n=0, tot=0, far=0; let r=0; for(let i=0;i<VX_N3;i++) r=Math.max(r,Math.abs(P[i*3])); for(let i=0;i<VX_N3;i++){ const x=P[i*3], y=P[i*3+1], z=P[i*3+2], d=Math.hypot(x,y,z); if(d>r*1.05 || d<r*.75) continue; tot++; if(V.t[i]===5 && V.a[i]>0){ n++; if(Math.abs(z)>r*.6) far++; } } return [n, tot, far]; })()""")
    ok(r[0]>0 and r[0]<r[1]*.6 and r[2]<=r[0]*.25, '🛞 al rodar sobre la pintura se pinta la franja que tocó el piso (%s de %s cuadritos de la orilla; de lado casi nada: %s)'%(r[0],r[1],r[2]))

    # 3. la miel la hace pegajosa: casi no rueda
    r=await ev("""(()=>{ const roll=honey=>{ __CLR(); suClear(); __AT(0,-12); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; const g=freeAddDyn('goma',X,Y+.3,Z,true); __S(30); if(honey){ stObjHit(g,4,g.root.position.x,g.root.position.y-.2,g.root.position.z,.4,1,0); } const x0=g.root.position.x; g.v.set(3,0,0); freeWake(g); __S(60); return +(g.root.position.x-x0).toFixed(2); };
        return [roll(false), roll(true)]; })()""")
    ok(r[1]<r[0]*.6, '🍯 con miel la pelota casi no rueda (limpia: %s m; con miel: %s m)'%(r[0],r[1]))

    # 4. rueda por la pintura y deja rastro en lo seco (y se le va quitando)
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,-12); const X=FREE.X, Y=FREE.Y, Z=FREE.Z, m=SU.cs; for(let x=-.6;x<=.61;x+=m) for(let z=-.6;z<=.61;z+=m) suPour(X+x,Z+z,5,SU_F|0x2a6bff,.03*m*m,.1); __S(20); let far0=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===5 && C.h[i]>0 && suXZ(C,i)[0]-X>1.4) far0++;
        const g=freeAddDyn('goma',X-1.5,Y+.4,Z,true); __S(20); g.v.set(4,0,0); freeWake(g); const tot5=()=>{ const S=g.root.userData.stn; if(!S||!S.vx) return 0; let t=0; for(let i=0;i<VX_N3;i++) if(S.vx.t[i]===5) t+=S.vx.a[i]; return t; }; let mx=0; for(let k=0;k<90;k++){ __S(1); mx=Math.max(mx,tot5()); } let far=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===5 && C.h[i]>0 && suXZ(C,i)[0]-X>1.4) far++;
        return [+mx.toFixed(1), far0, far, +(g.root.position.x-X).toFixed(2), +tot5().toFixed(1)]; })()""")
    ok(r[0]>5, '🎨 la pelota que pasa por la pintura sale pintada (%s)'%r[0])
    ok(r[2]>r[1]+2 and r[4]<r[0], '🛞 y al rodar por lo seco deja un rastro de pintura (%s cuadritos) y se le va quitando (%s → %s)'%(r[2]-r[1],r[0],r[4]))

    # 5. en el agua se lava
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,-12); const X=FREE.X, Y=FREE.Y, Z=FREE.Z, m=SU.cs; const g=freeAddDyn('goma',X,Y+.3,Z,true); __S(30); stObjHit(g,3,g.root.position.x,g.root.position.y-.25,g.root.position.z,.16,1,0); const a0=stCoat(g.root.userData.stn,3);
        for(let x=-1;x<=1.01;x+=m) for(let z=-1;z<=1.01;z+=m) suPour(X+x,Z+z,1,0,.6*m*m,.1); for(let k=0;k<150;k++) __S(1); return [+a0.toFixed(2), +stCoat(g.root.userData.stn,3).toFixed(2)]; })()""")
    ok(r[1]<r[0]*.3, '🚿 en el agua se le quita el lodo (%s → %s)'%(r[0],r[1]))

    # 6. agarras algo embarrado: tus manos; te pega algo con miel: te mancha
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,-12); stClear(myStn); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; const d=freeAddDyn('caja',X,Y+.3,Z,true); __S(30); stObjHit(d,3,X,Y+.6,Z,.4,1,0); __S(1); player.pos.set(X-1,Y+.05,Z); __S(2); stClear(myStn); freeGrab(d);
        const B=stBones(plush), J=plush.userData.arms.map(a=>B.indexOf(a.userData.joint)); const h=myStn.sp.filter(s=>J.includes(s.bi) && s.p===3).length; try{ freeRelease(0); }catch(e){} __S(20); stClear(myStn);
        const b=freeAddDyn('goma',X+3,Y+1.2,Z,true); __S(2); stObjHit(b,4,b.root.position.x,b.root.position.y,b.root.position.z,.4,1,0); player.pos.set(X+3.7,Y+.05,Z); b.v.set(4,0,0); freeWake(b); for(let k=0;k<20;k++) __S(1); return [h, myStn.sp.filter(s=>s.p===4).length]; })()""")
    ok(r[0]==2, '🤲 si agarras la caja embarrada, se te embarran las manos (%s)'%r[0])
    ok(r[1]>=1, '🍯 si te pega una pelota con miel, te deja miel (%s manchones)'%r[1])

    # 7. el tope: hasta 20 cosas manchadas (las más viejas se limpian solas)
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,-12); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; const L=[]; for(let k=0;k<26;k++){ const d=freeAddDyn('dado',X+(k%6)*1.2-3,Y+.3,Z+Math.floor(k/6)*1.2-3,true); if(d){ L.push(d); stObjHit(d,5,d.root.position.x,d.root.position.y+.3,d.root.position.z,.3,1,0xff3344); __S(1); } } __S(5); return [L.length, ST_OBJ.size]; })()""")
    ok(r[1]<=20, '📏 nunca hay más de 20 cosas manchadas a la vez (%s cosas, %s manchadas)'%(r[0],r[1]))

    # 8. rendimiento: 10 cosas manchadas
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,-12); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; camera.position.set(X,Y+3,Z+6); camera.lookAt(X,Y,Z); const L=[]; for(let k=0;k<10;k++) L.push(freeAddDyn(k%2?'caja':'goma',X+(k%5)*1.1-2.2,Y+.3,Z+Math.floor(k/5)*1.2-.6,true)); __S(40);
        const T=()=>{ for(let i=0;i<3;i++) renderer.render(scene,camera); const t0=performance.now(); for(let i=0;i<10;i++){ __S(1); renderer.render(scene,camera); } return (performance.now()-t0)/10; }; const a=T(); for(const d of L) stObjHit(d,[3,4,5][Math.floor(Math.random()*3)],d.root.position.x,d.root.position.y+.2,d.root.position.z,.35,1,0x33aaff); __S(3); const b2=T(); return [+a.toFixed(1), +b2.toFixed(1)]; })()""")
    ok(r[1]<r[0]*1.6+3, '⚡ con 10 cosas manchadas el cuadro tarda %s ms contra %s ms (aquí, sin tarjeta de video)'%(r[1],r[0]))
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
