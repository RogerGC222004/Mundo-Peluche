# v241 (Modo libre): la pintura se seca (mate, ya no corre ni mancha; el agua la ablanda), los colores se mezclan, salpicaduras con
# gotitas de verdad, molde de castillo de arena (se desmorona al secarse), polvito de arena seca y el chorro de miel que se enrolla.
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





    # 1. la pintura se seca, se ve mate y ya no se va
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,-12); const X=FREE.X, Y=FREE.Y, Z=FREE.Z, m=SU.cs; for(let x=-.8;x<=.81;x+=m) for(let z=-.8;z<=.81;z+=m) suPour(X+x,Z+z,5,SU_F|0x2a6bff,.03*m*m,.1); __S(20);
        const st=()=>{ let n=0, s=0, v=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===5 && C.h[i]>0){ n++; s+=C.pd[i]; v+=C.h[i]; } return [n, n?Math.round(s/n):0, +v.toFixed(3)]; }; const a=st(); __S(3000); const b2=st(); __S(900); const c=st();
        camera.position.set(X,Y+2,Z+1); camera.lookAt(X,Y,Z); renderer.render(scene,camera); let aw=0; for(const C of SU.list){ if(C.dirty) suBuild(C); C.ms.forEach((M,k)=>{ if(M && k===5) aw=Math.max(aw,M.geometry.attributes.aW.array[0]); }); } return [a,b2,c,+aw.toFixed(2),renderer.info.programs.filter(p=>p.diagnostics).length]; })()""")
    ok(r[0][1]<20 and r[1][1]>200, '🎨 la pintura recién echada está fresca (seca: %s de 255) y en ~1½ min se seca (%s)'%(r[0][1],r[1][1]))
    ok(r[2][0]==r[1][0] and abs(r[2][2]-r[1][2])<1e-4, '🧱 ya seca no corre ni se borra: se queda igual (%s → %s cuadritos)'%(r[1][0],r[2][0]))
    ok(r[3]>.8 and r[4]==0, '✨ y se dibuja mate (sin brillo, con grietitas) sin errores (%s)'%r[3])

    # 2. el agua la vuelve a ablandar; se guarda seca
    r=await ev("""(()=>{ const X=FREE.X, Z=FREE.Z; const q=suCell(X,Z,false), s0=q[0].pd[q[1]]; const enc=suQ(5,q[0].c[q[1]],q[0].s[q[1]],s0), dec=suUnQ(5,enc)[2]; suPour(X,Z,1,0,.004,.3); __S(80); const q2=suCell(X,Z,false); return [s0, dec, q2[0].pd[q2[1]], q2[0].t[q2[1]]]; })()""")
    ok(r[1]>180, '💾 la pintura seca se guarda y se comparte seca (%s → %s)'%(r[0],r[1]))
    ok(r[2]<r[0]-30, '💧 el agua encima la vuelve a ablandar (seca %s → %s)'%(r[0],r[2]))

    # 3. pisar pintura seca: no te mancha ni dejas huellas
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,-12); const X=FREE.X, Y=FREE.Y, Z=FREE.Z, m=SU.cs; for(let x=-1;x<=1.01;x+=m) for(let z=-1;z<=1.01;z+=m) suPour(X+x,Z+z,5,SU_F|0xff3d9a,.03*m*m,.1); __S(20); __S(3000); stClear(myStn); SU.feet=null;
        __WALK(-2.2,0,70); return [+myStn.A[5].toFixed(2), !!SU.feet, +(player.pos.x-X).toFixed(1)]; })()""")
    ok(r[0]<.05 and not r[1], '👣 caminar sobre pintura seca no te mancha ni deja huellas (mancha %s; pasaste hasta x=%s)'%(r[0],r[2]))

    # 4. los colores se mezclan donde se juntan
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,-12); const X=FREE.X, Z=FREE.Z, m=SU.cs; for(let x=-.6;x<=-.01;x+=m) for(let z=-.4;z<=.41;z+=m) suPour(X+x,Z+z,5,SU_F|0xff2020,.05*m*m,.1); for(let x=.1;x<=.71;x+=m) for(let z=-.4;z<=.41;z+=m) suPour(X+x,Z+z,5,SU_F|0xffee20,.05*m*m,.1); __S(90);
        let mix=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===5 && C.h[i]>0){ const c=C.c[i]&0xffffff, g=(c>>8)&255; if(g>70 && g<200) mix++; } return mix; })()""")
    ok(r>=2, '🟠 el rojo y el amarillo se mezclan donde se juntan (%s cuadritos naranjas)'%r)

    # 5. salpicaduras: al caer a la pintura salen gotitas que dejan puntitos afuera; en la miel no
    r=await ev("""(()=>{ const jump=(p,j)=>{ __CLR(); suClear(); __AT(0,-12); const X=FREE.X, Y=FREE.Y, Z=FREE.Z, m=SU.cs; for(let x=-1.2;x<=1.21;x+=m) for(let z=-1.2;z<=1.21;z+=m) suPour(X+x,Z+z,p,p===5?SU_F|0xff3d9a:0,.35*m*m,.1); __S(30);
          if(j){ player.pos.set(X,Y+3.4,Z); player.vel.set(0,0,0); player.vy=0; } let mx=0; for(let k=0;k<40;k++){ __S(1); mx=Math.max(mx,SU.drops.filter(d=>d.vy>.4 && d.t<.3).length); } __S(60); let out=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.h[i]>0 && (C.t[i]===p)){ const [x,z]=suXZ(C,i); if(Math.hypot(x-X,z-Z)>2.6) out++; } player.pos.set(X+6,Y+.05,Z); __S(3); return [mx, out]; };
        const a=jump(5,true), c=jump(5,false); return [[a[0], a[1]-c[1]], jump(4,true)]; })()""")
    ok(r[0][0]>=8 and r[0][1]>=1, '💦 al caer a la pintura salen gotitas (%s) que dejan puntitos afuera (%s)'%(r[0][0],r[0][1]))
    ok(r[1][0]==0, '🍯 en la miel no salpica (%s gotitas)'%r[1][0])

    # 6. el molde de castillo: almenas; aguanta mientras está mojado y se desmorona al secarse; también desde un invitado
    r=await ev("""(()=>{ __CLR(); suClear(); const X=FREE.X, Y=FREE.Y, Z=FREE.Z, m=SU.cs; player.pos.set(X+5,Y+.05,Z); __S(2); for(let x=-1.4;x<=1.41;x+=m) for(let z=-1.4;z<=1.41;z+=m) suPour(X+x,Z+z,7,0,.05*m*m,.1,204); __S(20);
        const ok=suMold(X+.1,Z+.1); const tp=(dx,dz)=>{ const q=suCell(X+(dx+.5)*m,Z+(dz+.5)*m,false); if(!q) return -9; const [C,i]=q; return +(suB(C,i)+C.h[i]+C.h2[i]-Y).toFixed(2); }; const a=[tp(3,3),tp(3,2),tp(0,0),tp(5,0)]; __S(600); const b2=[tp(3,3),tp(3,2),tp(0,0)]; __S(6000); const c=[tp(3,3),tp(0,0)];
        suNetOp('x',['su','qm',4,4]); __S(2); const d=[tp(23,23)]; return [ok,a,b2,c,d]; })()""")
    ok(r[0] and r[1][0]-r[1][1]>.08 and r[1][0]-r[1][3]>.3, '🏰 el molde hace una torre de arena con almenas (almena %s m, entre almenas %s m, centro %s m; afuera %s m)'%tuple(r[1]))
    ok(abs(r[2][0]-r[1][0])<.03, '💪 mojada aguanta (a los 20 s la almena sigue a %s m)'%r[2][0])
    ok(r[3][0]<r[1][0]-.08, '🌬️ y cuando se seca se va desmoronando (a los 3 min: %s m)'%r[3][0])
    ok(r[4][0]>.35, '👫 también funciona si lo pone un amigo (%s m)'%r[4][0])

    # 7. polvito al caminar en arena seca; el chorro de miel se enrolla
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,-12); const X=FREE.X, Z=FREE.Z, m=SU.cs; for(let x=-1.6;x<=1.61;x+=m) for(let z=-1;z<=1.01;z+=m) suPour(X+x,Z+z,7,0,.08*m*m,.1); __S(20); const d0=DUST.next; __WALK(-2.2,0,50); const dust=(DUST.next-d0+DUST.N)%DUST.N;
        suClear(); __S(2); player.pos.set(X,FREE.Y+.05,Z); __S(2); FREE.sel={k:'s',a:4}; SU.mode=1; SU.hold={t:performance.now(),mode:1,p:4,col:0,done:0}; let on=false; for(let k=0;k<30;k++){ __S(1); if(SU.coil && SU.coil.visible) on=true; } SU.hold=null; __S(2); const off=!(SU.coil && SU.coil.visible); FREE.sel=null; __S(1); return [dust, on, off]; })()""")
    ok(r[0]>=4, '🌫️ al caminar en arena seca sale polvito (%s puntitos)'%r[0])
    ok(r[1] and r[2], '🍯 el chorro de miel se enrolla donde cae (y se quita al dejar de echar)')
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
