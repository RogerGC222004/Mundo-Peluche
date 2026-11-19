# v235 (Modo libre): 🪣 Sustancias, cuarta ronda. Cascadas: lo que se cae de un bloque baja como chorro y llega cuando de verdad
# caería; las orillas avanzan poco a poco; lo de cerca se redibuja en cada cuadro y lo lejano se dibuja junto; lo pesado se va al fondo
# (sin torres ni picos); la huella en lodo alto ya no deja picos; la máquina sale apagada, lo que echa es sustancia de verdad (cada gotita
# del tamaño de lo que lleva) y «llenar hasta» la apaga sola.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.033); update(.033,t); } };
  window.__CLR=()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); FREE.hold=null; freeSelect(null); };
  window.__AT=(x,z)=>{ player.pos.set(FREE.X+x,FREE.Y+.05,FREE.Z+z); player.vel.set(0,0,0); player.vy=0; player.facing=0; yaw=Math.PI; FREE.ppPrev=null; __S(2); };
  window.__LOOK=(x,y,z)=>{ camMode='first'; camera.position.set(player.pos.x,player.pos.y+1.6,player.pos.z); camera.lookAt(x,y,z); camera.updateMatrixWorld(); };
  window.__UPQ=(I,k)=>{ const m=new THREE.Matrix4(), q=new THREE.Quaternion(), p=new THREE.Vector3(), s=new THREE.Vector3(); I.getMatrixAt(k,m); m.decompose(p,q,s); return [new THREE.Vector3(0,0,1).applyQuaternion(q).y, p.y]; }; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type=='warning' and ('juguetes' in m.text or 'gadgets' in m.text or 'maquina' in m.text or 'sustancias' in m.text) else None)
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev("(()=>{ freeEnter(); return 1; })()"); await ev(STEP)

    await ev("""(()=>{ window.__LAKE=(p,d,a,b)=>{ for(let ci=a;ci<=b;ci++) for(let cj=a;cj<=b;cj++){ const C=suChunk(ci,cj,true); if(C) suDec(C,'F|'+p+'|'+(p===5?'f00':'0')+'|'+Math.round(d/.003).toString(36)); } suRecount(); };
      window.__WALK=(k)=>{ const x=player.pos.x, z=player.pos.z; keys.KeyW=true; __S(k); keys.KeyW=false; return Math.hypot(player.pos.x-x,player.pos.z-z); }; return 1; })()""")
    T="""const __VOL=()=>{ suRecount(); return SU.vol+FU.pts.reduce((a,P)=>a+(P.v||0),0)+[...SU.falls.values()].reduce((a,F)=>a+F.acc+(F.q||[]).filter((_,i)=>i%2).reduce((x,y)=>x+y,0),0); }; window.__VOL=__VOL;
      window.__PLAT=(x0,z0,n,h)=>{ for(let a=0;a<n;a++) for(let b=0;b<n;b++) for(let y=0;y<h;y++) freeAddStatic({k:'b',a:0,b:2},FREE.X+x0+a+.5,FREE.Y+y,FREE.Z+z0+b+.5,0,true); }; 1"""
    await ev(T)
    # 1. cascada: lo que se cae de un bloque baja como chorro (se ve) y llega abajo cuando de verdad caería
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); __PLAT(-1,-1,2,2); const v0=__VOL(); suPour(FREE.X,FREE.Z,1,0,.6,.5); let first=-1, fallsMax=0, inst=0;
        for(let i=0;i<60;i++){ __S(1); fallsMax=Math.max(fallsMax,SU.falls.size); inst=Math.max(inst,FU.pts.filter(P=>!P.o).length);   /* (v236: las cascadas ya son gotitas de verdad) */ let g=0; for(const C of SU.list) for(let k=0;k<256;k++) if(C.h[k]>0 && suB(C,k)<FREE.Y+.1) g+=C.h[k]; if(first<0 && g>.0005) first=i; }
        for(let i=0;i<150;i++) __S(1); let g=0; for(const C of SU.list) for(let k=0;k<256;k++) if(C.h[k]>0 && suB(C,k)<FREE.Y+.1) g+=C.h[k]*.04; return [fallsMax, inst, first, +g.toFixed(3), +(__VOL()-v0).toFixed(3)]; })()""")
    ok(r[0]>3 and r[1]>3, '💧 el agua que se cae de los bloques baja como chorro: %s chorros a la vez, %s gotitas cayendo'%(r[0],r[1]))
    ok(r[2]>=6, 'y llega al piso cuando de verdad caería de 2 m (al cuadro %s, no de golpe)'%r[2])
    ok(r[3]>.3 and abs(r[4]-.6)<.01, 'abajo queda lo que cayó (%s m³) y no se pierde ni se inventa nada (%s m³ de %s)'%(r[3],r[4],.6))
    # 2. la orilla avanza poco a poco (no de cuadrito en cuadrito)
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); const x=FREE.X+5, z=FREE.Z+5; const A=[];
        const area=()=>{ let a=0; for(const C of SU.list){ suBuild(C); const M=C.ms[3]; if(!M || !M.userData.on) continue; const P=M.geometry.attributes.position.array, n=M.geometry.drawRange.count/6; for(let c=0;c<n;c++){ const o=c*12; a+=Math.abs((P[o+3]-P[o])*(P[o+8]-P[o+2])); } } return a; };
        for(let i=0;i<40;i++){ suPour(x,z,3,0,.012,.3); __S(1); A.push(area()); } const Fa=A[A.length-1]; let mx=0; for(let i=10;i<A.length;i++) mx=Math.max(mx,(A[i]-A[i-1])/Fa); let n=0; for(const C of SU.list) for(let k=0;k<256;k++) if(C.h[k]>0) n++; return [+A[A.length-1].toFixed(2), +(n*.04).toFixed(2), +mx.toFixed(3)]; })()""")
    ok(r[0]<=r[1] and r[2]<.19, 'el lodo que se extiende crece poco a poco: en un cuadro crece a lo más %s%% de lo que acaba midiendo (se ve %s m² de %s m² mojados)'%(round(r[2]*100,1),r[0],r[1]))
    # 3. lo de cerca se redibuja en cada cuadro (sin saltitos) y lo lejano se junta
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-40,0); const X0=FREE.X+5, Z0=FREE.Z-30; for(let x=0;x<60;x+=3) for(let z=0;z<60;z+=3) suPour(X0+x+1,Z0+z+1,1,0,3,1);
        let late=0; for(let i=0;i<40;i++){ player.pos.set(FREE.X-40,FREE.Y+.05,FREE.Z); suPour(FREE.X-38,FREE.Z+2,1,0,.02,.3); __S(1); if(i>10) late+=SU.list.filter(C=>!C.far2 && C.dirty).length; }
        camera.position.set(FREE.X-40,FREE.Y+3,FREE.Z-4); for(let i=0;i<20;i++) suTick(.033); for(const S of [...SU.sc.values()]) if(S.dirty) suFarMerge(S); const n=SU.list.length, sep=SU.list.reduce((a,C)=>a+C.ms.filter(m=>m&&m.visible).length,0), jun=[...SU.sc.values()].reduce((a,S)=>a+S.ms.filter(G=>G&&G.visible).length,0), lagos=Object.values(SU.flatM).filter(M=>M&&M.visible).length;
        let vin=0; for(const S of SU.sc.values()) for(const G of S.ms) if(G && G.visible) vin+=G.geometry.drawRange.count/6; let vall=0; for(const C of SU.list) if(C.inF) for(const M of C.ms) if(M && M.userData.on) vall+=M.geometry.drawRange.count/6;
        return [late, n, sep+jun+lagos, jun, vin, vall]; })()""")
    ok(r[0]==0, 'lo que se mueve cerca de ti se redibuja en cada cuadro (quedaron pendientes: %s)'%r[0])
    ok(r[2]<r[1]*.6 and r[3]>0 and r[4]==r[5], 'lo lejano se dibuja junto: %s trozos con agua en %s dibujos (%s juntos), sin que falte nada (%s = %s cuadritos)'%(r[1],r[2],r[3],r[4],r[5]))
    # 4. capas: lo pesado se va al fondo, sin torres ni picos
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); const x=FREE.X+4, z=FREE.Z+4; suPour(x,z,1,0,2,1.2); __S(30); suPour(x,z,4,0,.4,.4); __S(10); let a=[0,0]; for(const C of SU.list) for(let i=0;i<256;i++){ if(C.t[i]===4 && C.t2[i]===1 && C.h2[i]>.003) a[0]++; if(C.t[i]===1 && C.t2[i]===4 && C.h2[i]>.003) a[1]++; }
        suClear(); suPour(x,z,4,0,.4,.6); __S(20); suPour(x,z,1,0,.4,.6); __S(10); let b=[0,0]; for(const C of SU.list) for(let i=0;i<256;i++){ if(C.t[i]===4 && C.t2[i]===1 && C.h2[i]>.003) b[0]++; if(C.t[i]===1 && C.t2[i]===4 && C.h2[i]>.003) b[1]++; }
        suClear(); const v0=__VOL(); for(let i=0;i<150;i++){ suPour(x,z,1,0,.03,.8); suPour(x+.5,z,4,0,.008,.3); __S(1); } let mx=0; for(const C of SU.list){ suBuild(C); C.ms.forEach(M=>{ if(!M || !M.userData.on) return; const P=M.geometry.attributes.position.array, n=M.geometry.drawRange.count/6; for(let c=0;c<n;c++){ let y0=1e9, y1=-1e9; for(let v=0;v<4;v++){ const y=P[(c*4+v)*3+1]; y0=Math.min(y0,y); y1=Math.max(y1,y); } mx=Math.max(mx,y1-y0); } }); }
        return [a, b, +mx.toFixed(3), +(__VOL()-v0).toFixed(3)]; })()""")
    ok(r[0][0]>0 and r[0][1]==0 and r[1][0]>0 and r[1][1]==0, 'la miel se va al fondo del agua (echándola encima o abajo): miel abajo/agua arriba en %s y %s cuadritos, al revés en ninguno'%(r[0][0],r[1][0]))
    ok(r[2]<.8, 'echando agua y miel juntas no salen torres ni velas: lo más empinado de un cuadrito es %s m'%r[2])
    ok(abs(r[3]-(.03+.008)*150)<.02, 'y no se pierde ni se inventa sustancia (%s m³)'%r[3])
    # 5. la huella en un montón de lodo alto ya no deja picos
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); const x=FREE.X+4, z=FREE.Z+4; for(let i=0;i<60;i++) suPour(x,z,3,0,.05,.6); __S(40);
        const spikes=()=>{ let n=0; for(const C of SU.list) for(let i=0;i<256;i++){ if(!(C.h[i]>.05)) continue; const S=suB(C,i)+C.h[i]+C.h2[i]; let s=0, k=0; for(const [dx,dz] of _suN){ const N=suNb(C,i,dx,dz,false); if(!N) continue; s+=suB(N[0],N[1])+N[0].h[N[1]]+N[0].h2[N[1]]; k++; } if(k===4) n=Math.max(n,S-s/4); } return +n.toFixed(3); };
        const s0=spikes(); player.pos.set(x-2.5,FREE.Y+.05,z+.3); yaw=-Math.PI/2; keys.KeyW=true; for(let i=0;i<70;i++) __S(1); yaw=Math.PI/2; for(let i=0;i<70;i++) __S(1); keys.KeyW=false; __S(20); return [s0, spikes()]; })()""")
    ok(r[1]<.2, 'caminar por un montón de lodo alto deja huella pero sin picos (el pico más alto: %s m → %s m)'%(r[0],r[1]))
    # 6. la máquina: apagada de inicio; lo que sale es sustancia de verdad; «llenar hasta» la apaga sola
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); const o=freeAddStatic({k:'p',a:'fuentes',b:FU_DEF},FREE.X,FREE.Y,FREE.Z,0,true); __S(20); const off=[fuCfg(o).every(c=>!c.on), FU.pts.length, +__VOL().toFixed(4)];
        const C=fuCfg(o); C[1].on=1; C[1].q=2; fuSet(o,C); const v0=__VOL(); __S(60); const fl=FU.pts.reduce((a,P)=>a+(P.v||0),0), vr=+(__VOL()-v0).toFixed(3); let big=0; for(const P of FU.pts) big=Math.max(big,P.r);
        return [off, vr, +fl.toFixed(3), +big.toFixed(3), FU.pts.every(P=>Math.abs(4.18879*P.r**3-P.v)<1e-6)]; })()""")
    ok(r[0][0] and r[0][1]==0 and r[0][2]==0, 'la máquina sale apagada: no echa nada hasta que la prendes %s'%r[0])
    ok(abs(r[1]-.4)<.02 and r[2]>.05, 'lo que sale de la fuente es sustancia de verdad: %s m³ en 2 s (de 0.4), %s m³ todavía volando'%(r[1],r[2]))
    ok(r[4], 'cada gotita se ve del tamaño de lo que lleva')
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); for(let a=-4;a<4;a++){ for(const [x,z] of [[a+.5,-3.5],[a+.5,3.5],[-3.5,a+.5],[3.5,a+.5]]) freeAddStatic({k:'b',a:0,b:4},FREE.X+x,FREE.Y,FREE.Z+z,0,true); }
        const o=freeAddStatic({k:'p',a:'fuentes',b:FU_DEF},FREE.X,FREE.Y,FREE.Z,0,true); const C=fuCfg(o); C[1].on=1; C[1].q=3; C.lim=1; fuSet(o,C); let t=-1; for(let i=0;i<500;i++){ __S(1); if(!fuCfg(o)[1].on){ t=i; break; } } __S(60);
        const q=suCell(FREE.X+2.4,FREE.Z+.1,false), d=q?q[0].h[q[1]]+q[0].h2[q[1]]:0; return [t, +d.toFixed(3), fuCfg(o).lim, FU_LIMN[fuCfg(o).lim]]; })()""")
    ok(r[0]>0 and .15<r[1]<.4 and r[2]==1, '«Llenar hasta: Tobillos»: la fuente llenó el corral y se apagó sola (al cuadro %s; quedó de %s m)'%(r[0],r[1]))
    r=await ev("""(()=>{ const o=FREE.objs.find(q=>q.gad==='fuentes'); fuOpen(o); const ov=ui('freeBubOv'); const rows=[...ov.querySelectorAll('.bub-row b')].map(b=>b.textContent); ov.hidden=true;
        freeSave(); FREE.loaded=null; freeLoad(); const o2=FREE.objs.find(q=>q.gad==='fuentes'); return [rows, o2 && fuCfg(o2).lim]; })()""")
    ok(r[0][-1].startswith('Llenar hasta') and r[1]==1, 'la ventanita tiene «Llenar hasta» y se guarda con el mundo %s'%r)
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close(); await b.close()
asyncio.run(m())
