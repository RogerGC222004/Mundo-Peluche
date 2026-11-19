# v239 (Modo libre): olas que viajan y rebotan en las paredes (rápidas en el agua, lentas y chiquitas en la miel), que se apagan solas;
# corrientes que arrastran lo que flota, a quien nada y la espuma (también el viento); los chorros que caen hacen olas y empujan el agua.
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



    # 1. una ola viaja desde donde cae algo, rebota en la pared y se apaga sola
    r=await ev("""(()=>{ __PL(1,.7); const X=FREE.X, Z=FREE.Z; wvImp(X,Z,.09,.5); const at=[], ser=[]; for(let k=0;k<120;k++){ __S(1); const a=[1.2,2.4,3.6].map(d=>Math.abs(wvH(X+d,Z))); at.push(a); ser.push(a[2]); }
        const first=d=>{ for(let k=0;k<at.length;k++) if(at[k][d]>.002) return k; return -1; }; const mxr=(a,b)=>Math.max(...at.slice(a,b).map(v=>v[0])); const ep=[+mxr(3,20).toFixed(4), +mxr(35,60).toFixed(4), +mxr(70,120).toFixed(4)];
        renderer.render(scene,camera); const prog=renderer.info.programs.filter(p=>p.diagnostics).length; let t=0; while(WV.act && t<3000){ __S(30); t+=30; } return [[first(0),first(1),first(2)], ep, prog, +(t*.033).toFixed(1), WV.act]; })()""")
    f=r[0]
    ok(0<=f[0]<f[1]<f[2], '🌊 una ola sale de donde cae algo y viaja (llega a 1.2 m, 2.4 m y 3.6 m en los cuadros %s)'%f)
    ok(r[1][2]>r[1][1]*1.3 and r[1][2]>.001, '↩️ rebota en la pared y regresa: a 1.2 m pasa de ida (%s m), se calma (%s m) y vuelve de regreso (%s m)'%tuple(r[1]))
    ok(r[2]==0, '🧩 las olas se dibujan sin errores')
    ok(not r[4] and r[3]<60, '😴 y se calma sola: a los %s s ya no se calcula nada'%r[3])

    # 2. la miel: olas lentas y chiquitas; la arena: sin olas
    r=await ev("""(()=>{ const sp=p=>{ __PL(p,.7); const X=FREE.X, Z=FREE.Z; wvImp(X,Z,.09,.5); let t=-1, mx=0; for(let k=0;k<45;k++){ __S(1); const h=Math.abs(wvH(X+1.8,Z)); if(h>mx) mx=h; if(t<0 && h>.003) t=k; } return [t, +mx.toFixed(4)]; }; const w=sp(1), m=sp(4); __PL(7,.5); wvImp(FREE.X,FREE.Z,.09,.5); __S(2); return [w,m,WV.act]; })()""")
    ok(r[0][0]>=0 and (r[1][0]<0 or r[1][0]>r[0][0]*1.5) and r[1][1]<r[0][1], '🍯 en la miel la ola va mucho más lento y más chiquita que en el agua (agua: llega en %s cuadros, %s m; miel: %s, %s m)'%(r[0][0],r[0][1],r[1][0],r[1][1]))
    ok(not r[2], '🏖️ en la arena no hay olas')

    # 3. lo que flota sube y baja con las olas
    r=await ev("""(()=>{ __PL(1,.7); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; const b=freeAddDyn('playa',X+1.5,Y+1,Z,true); __S(150); const y0=b.root.position.y; let mn=9, mx=-9; wvImp(X,Z,.12,.5); for(let k=0;k<60;k++){ __S(1); const y=b.root.position.y; if(y<mn) mn=y; if(y>mx) mx=y; } return [+(mx-mn).toFixed(3), !!b.sleep]; })()""")
    ok(r[0]>.005, '🏐 la pelota que flota sube y baja cuando pasa la ola (%s m)'%r[0])

    # 4. la corriente: un chorro empuja el agua y se lleva lo que flota; no atraviesa la pared
    r=await ev("""(()=>{ __PL(1,.6); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; const b=freeAddDyn('playa',X-1,Y+1,Z,true), c=freeAddDyn('caja',X-1,Y+1,Z+1.4,true); __S(150); const a0=[b.root.position.x,c.root.position.x], sl=[!!b.sleep,!!c.sleep];
        for(let k=0;k<450;k++){ wvPush(X-4.2,Z+.5,1.6,0,.6,.5); __S(1); } const u=wvU(X+1,Z+.5), a1=[b.root.position.x,c.root.position.x]; for(let k=0;k<450;k++){ wvPush(X-4.2,Z+.5,1.6,0,.6,.5); __S(1); }
        const [ix,iz]=wvCell(X+4.4,Z); return [+(a1[0]-a0[0]).toFixed(2), +(a1[1]-a0[1]).toFixed(2), +u[0].toFixed(3), +(b.root.position.x-X).toFixed(2), +WV.ux[iz*WV_N+ix].toFixed(3), sl]; })()""")
    ok(r[0]>.4 and r[1]>.2 and r[2]>.03, '🌀 un chorro hace corriente (%s m/s a 5 m) y en 15 s se lleva la pelota (%s m) y la caja que flotan (%s m), aunque estuvieran dormidas %s'%(r[2],r[0],r[1],r[5]))
    ok(r[3]<4.5 and r[4]<=0.001, '🧱 la corriente no atraviesa la pared: la pelota se queda en la alberca (a %s m del centro; corriente contra la pared %s)'%(r[3],r[4]))

    # 5. un chorro que cae (máquina, cascada, manguera) hace olas y empuja hacia donde va
    r=await ev("""(()=>{ __PL(1,.6); const X=FREE.X, Z=FREE.Z; for(let k=0;k<120;k++){ for(let j=0;j<3;j++) fuLanded({r:.05,vx:2.5,vy:-3,vz:0,v:0,p:1,y:FREE.Y+.6},X-3+Math.random()*.2,Z+(Math.random()-.5)*.3); __S(1); } const u=wvU(X-2,Z); return [WV.act, +u[0].toFixed(3), +Math.abs(wvH(X-3,Z)).toFixed(4)]; })()""")
    ok(r[0] and r[1]>.05, '⛲ el agua que cae de un chorro hace olas y empuja el agua hacia donde va (%s m/s)'%r[1])

    # 6. tú: al caer al agua salpica una ola; si nadas en la corriente te lleva
    r=await ev("""(()=>{ __PL(1,1.4); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; player.pos.set(X,Y+3.2,Z); player.vel.set(0,0,0); player.vy=0; let mx=0, act=false; for(let k=0;k<50;k++){ __S(1); if(WV.act) act=true; mx=Math.max(mx,Math.abs(wvH(X+1,Z))); } const sw=player.swim;
        for(let k=0;k<30;k++){ wvPush(X,Z,1.2,0,1.6,.5); __S(1); } const x0=player.pos.x; for(let k=0;k<60;k++){ wvPush(X,Z,1.2,0,1.6,.5); stick.x=0; stick.y=0; __S(1); } return [act, +mx.toFixed(3), sw, +(player.pos.x-x0).toFixed(2)]; })()""")
    ok(r[0] and r[1]>.005, '🤽 al caer al agua tu peluche hace una ola (%s m)'%r[1])
    ok(r[2] and r[3]>.3, '🏊 y si nadas en una corriente, te lleva (%s m en 2 s)'%r[3])

    # 7. la espuma se va con el viento
    r=await ev("""(()=>{ __PL(1,.5); const X=FREE.X, Z=FREE.Z; for(let x=-1;x<=1;x+=.4) suPour(X+x,Z,6,0,.02,.2); __S(5); const fx=()=>{ let sx=0,sv=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t2[i]===6 && C.h2[i]>0){ const [x]=suXZ(C,i); sx+=x*C.h2[i]; sv+=C.h2[i]; } return sv?sx/sv-X:null; };
        const f0=fx(); weatherNow.wind=1.3; for(let k=0;k<120;k++) __S(1); const f1=fx(); weatherNow.wind=.1; __S(2); return [f0&&+f0.toFixed(2), f1&&+f1.toFixed(2)]; })()""")
    ok(r[0] is not None and r[1] is not None and r[1]>r[0]+.15, '🌬️ con viento, la espuma se va para el mismo lado (%s → %s m)'%(r[0],r[1]))

    # 8. calmado no cuesta nada; con olas y corriente, poquito
    r=await ev("""(()=>{ __PL(1,.7); const X=FREE.X, Z=FREE.Z; __S(30); const off=!WV.act; WV.ms=0; for(let k=0;k<60;k++){ if(k%10===0) wvImp(X+(k%3-1)*2,Z,.08,.5); wvPush(X-4,Z,1.5,0,.5,.4); __S(1); } return [off, +WV.ms.toFixed(3), WV.x1-WV.x0+1, WV.z1-WV.z0+1]; })()""")
    ok(r[0], '😴 con el agua quieta no se calcula nada')
    ok(r[1]<1.5, '⚡ con olas y corriente en toda la alberca (%s×%s cuadritos) cuesta %s ms por cuadro'%(r[2],r[3],r[1]))
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
