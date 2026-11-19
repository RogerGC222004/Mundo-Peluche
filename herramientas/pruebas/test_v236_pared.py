# v236 (Modo libre): la capa en la pared. Lo espeso (miel, slime, lodo, pintura) que se sale por una orilla, que choca o que se embarra
# en el lado de un bloque se queda en la pared de verdad: baja por su peso, deja la pared embarrada, hace chorros con gota, al llegar
# abajo se va al piso (o cuelga y se cae), se guarda con el mundo y no cuesta mucho.
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
    T="""const __VOL=()=>{ suRecount(); return SU.vol+FU.pts.reduce((a,P)=>a+(P.v||0),0)+[...SU.falls.values()].reduce((a,F)=>a+F.acc+(F.q||[]).filter((_,i)=>i%2).reduce((x,y)=>x+y,0),0)+(typeof wlVol==='function'?wlVol():0); }; window.__VOL=__VOL;   // (v236: y lo que está en las paredes)
      window.__PLAT=(x0,z0,n,h)=>{ for(let a=0;a<n;a++) for(let b=0;b<n;b++) for(let y=0;y<h;y++) freeAddStatic({k:'b',a:0,b:2},FREE.X+x0+a+.5,FREE.Y+y,FREE.Z+z0+b+.5,0,true); }; 1"""
    await ev(T)
    await ev("""(()=>{ window.__TOW=(x,z,b)=>{ for(let a=0;a<3;a++) for(let c=0;c<3;c++) for(let y=0;y<2;y++) freeAddStatic({k:'b',a:0,b:b||6},FREE.X+x+a-1,FREE.Y+y,FREE.Z+z+c-1,0,true); };
      window.__WL=(p)=>{ let v=0, cells=0, sh=0; for(const W of SU.wl.values()){ let n=0; for(let i=0;i<1024;i++) if(W.h[i]>0 && (!p || W.t[i]===p)){ v+=W.h[i]*WL_A; n++; } if(n){ sh++; cells+=n; } } return [sh,cells,+v.toFixed(4)]; };
      window.__FACE=(ax,sg)=>[...SU.wl.values()].filter(W=>W.ax===ax && W.sg===sg); return 1; })()""")
    # 1. la miel que se desborda de una torre se queda en las 4 paredes: una capa que dobla la orilla y baja con chorros
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); __TOW(0,0); const v0=__VOL(); let poured=0; for(let i=0;i<120;i++){ poured+=suPour(FREE.X,FREE.Z,4,0,.03,.5)||0; __S(1); }
        const faces=[[0,1],[0,-1],[1,1],[1,-1]].map(([a,s])=>__FACE(a,s).length); let top=0, topN=0; const fr=[];
        for(const W of __FACE(1,-1)) for(let iu=0;iu<32;iu++){ const u=W.u0+(iu+.5)*WL_CS; if(Math.abs(u-FREE.X)>1.4) continue; const iy=Math.floor((FREE.Y+1.95-W.y0)/WL_CS); if(iy<0||iy>31) continue; topN++; if(W.h[iy*32+iu]>0) top++;
          let lo=null; for(let k=0;k<32;k++) if(W.h[k*32+iu]>WL_ST[4]*1.2){ lo=W.y0+k*WL_CS-FREE.Y; break; } if(lo!==null) fr.push(lo); }
        const m=fr.reduce((a,b)=>a+b,0)/Math.max(1,fr.length), sd=Math.sqrt(fr.reduce((a,b)=>a+(b-m)*(b-m),0)/Math.max(1,fr.length));
        return [faces, __WL(4), +(top/Math.max(1,topN)).toFixed(2), +sd.toFixed(2), +(__VOL()-v0-poured).toFixed(4), FU.pts.filter(P=>P.p===4).length]; })()""")
    ok(all(n>0 for n in r[0]), '🍯 la miel que se sale se queda en las 4 paredes de la torre %s (%s cuadritos, %s m³ en la pared)'%(r[0],r[1][1],r[1][2]))
    ok(r[2]>=.8, 'arriba es una capa entera que dobla la orilla (%s de la orilla mojada)'%r[2])
    ok(r[3]>.08, 'y abajo baja disparejo, en chorros (las puntas varían %s m)'%r[3])
    ok(abs(r[4])<.01, 'no se pierde ni se inventa miel (diferencia %s m³)'%r[4])
    ok(r[5]<15, 'ya no son gotitas sueltas: es capa (%s gotitas de miel)'%r[5])
    # 2. llega abajo y se va al piso; la pared queda embarrada y se duerme
    r=await ev("""(()=>{ const v0=__VOL(); __S(400); suRecount(); let foot=0; for(const C of SU.list) for(let k=0;k<256;k++){ if(!(C.h[k]>0) || C.t[k]!==4) continue; const [x,z]=suXZ(C,k); const m=Math.max(Math.abs(x-FREE.X),Math.abs(z-FREE.Z)); if(m>1.5 && m<2.5 && suB(C,k)<FREE.Y+.1) foot+=C.h[k]*.04; }
        let low=0; for(const W of SU.wl.values()) for(let i=0;i<1024;i++) if(W.h[i]>0 && W.y0+(i>>5)*WL_CS<FREE.Y+.5) low++;
        const coat=__WL(4); let t=0; for(let i=0;i<600 && [...SU.wl.values()].some(W=>W.aw>0);i++){ __S(1); t++; }
        return [+foot.toFixed(3), low, coat, t, [...SU.wl.values()].filter(W=>W.aw>0).length, +(__VOL()-v0).toFixed(4)]; })()""")
    ok(r[0]>.05 and r[1]>10, '⬇️ baja hasta el piso y se junta al pie de la pared (%s m³ al pie; %s cuadritos abajo de 50 cm)'%(r[0],r[1]))
    ok(r[2][1]>200, 'la pared se queda embarrada (%s cuadritos con miel pegada)'%r[2][1])
    ok(abs(r[5])<.01, 'todo ese rato no se pierde miel (%s m³)'%r[5])
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); for(let z=-1;z<=1;z++) for(let y=0;y<3;y++) freeAddStatic({k:'b',a:0,b:4},FREE.X+3.5,FREE.Y+y,FREE.Z+z,0,true); const o=FREE.objs.find(q=>q.sel && q.sel.k==='b' && Math.abs(q.y-FREE.Y-2)<.1); const rr=.2; suSplat(4,0,0,4.18879*rr*rr*rr,FREE.X+3-rr*.5,FREE.Y+2.4,FREE.Z,6,0,0,-1,0,0,o,rr); let t=0; for(let i=0;i<1500 && (!SU.wl.size || [...SU.wl.values()].some(W=>W.aw>0));i++){ __S(1); t++; }
        return [t, SU.wl.size, [...SU.wl.values()].filter(W=>W.aw>0).length, __WL(4)[1]]; })()""")
    ok(r[1]>0 and r[2]==0, '😴 una bola de miel en la pared escurre, se detiene y la pared se duerme: ya no cuesta nada (a los %s s; %s cuadritos embarrados)'%(round(r[0]*.033,1),r[3]))
    # 3. el chorro de miel de la máquina pega en la pared y se queda embarrado ahí, a la altura donde pegó
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); const o=freeAddStatic({k:'p',a:'fuentes',b:0},FREE.X,FREE.Y,FREE.Z,0,true); for(let z=-2;z<=2;z++) for(let y=0;y<3;y++) freeAddStatic({k:'b',a:0,b:4},FREE.X+5.5,FREE.Y+y,FREE.Z+z,0,true);
        fuSet(o,[0,1,2,3].map(i=>({on:i===3?1:0,p:4,q:2,x:2,col:0}))); const v0=__VOL(); let slide=0, through=0; for(let i=0;i<70;i++){ __S(1); for(const P of FU.pts){ if(P.st===1 && P.p===4) slide++; if(P.x>FREE.X+6.05) through++; } }
        const W=__FACE(0,-1); let hi=0, n=0; for(const w of W) for(let i=0;i<1024;i++) if(w.h[i]>0){ n++; hi=Math.max(hi,w.y0+((i>>5)+.5)*WL_CS-FREE.Y); }
        return [n, +hi.toFixed(2), slide, through, __WL(4)[2]]; })()""")
    ok(r[0]>3 and r[1]>.4, '🚿 el chorro de miel de la máquina se queda embarrado en la pared donde pega (%s cuadritos, hasta %s m de alto)'%(r[0],r[1]))
    ok(r[2]<20 and r[3]==0, 'no rebota ni la atraviesa: se queda (%s gotitas escurriendo sueltas, %s atravesaron)'%(r[2],r[3]))
    # 4. una bola de slime contra la pared: se embarra donde pegó y luego escurre
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); for(let z=-1;z<=1;z++) for(let y=0;y<3;y++) freeAddStatic({k:'b',a:0,b:4},FREE.X+3.5,FREE.Y+y,FREE.Z+z,0,true);
        const o=FREE.objs.find(q=>q.sel && q.sel.k==='b' && Math.abs(q.y-FREE.Y-2)<.1); const r=.18, v=4.18879*r*r*r; suSplat(2,0,0,v,FREE.X+3-r*.5,FREE.Y+2.3,FREE.Z,6,0,0,-1,0,0,o,r);
        const at=()=>{ let n=0, ys=0, w=0; for(const W of SU.wl.values()) for(let i=0;i<1024;i++) if(W.h[i]>0 && W.t[i]===2){ n++; ys+=(W.y0+((i>>5)+.5)*WL_CS-FREE.Y)*W.h[i]; w+=W.h[i]; } return [n,+(ys/Math.max(w,1e-9)).toFixed(2)]; };
        const a=at(); __S(90); const b=at(); return [a,b]; })()""")
    ok(r[0][0]>2 and abs(r[0][1]-2.3)<.25, '🟢 una bola de slime contra la pared se embarra donde pegó (%s cuadritos a %s m)'%(r[0][0],r[0][1]))
    ok(r[1][1]<r[0][1]-.1, 'y luego escurre hacia abajo (su centro bajó de %s a %s m)'%(r[0][1],r[1][1]))
    # 5. si abajo no hay pared (una losa en el aire), la gota cuelga, engorda y se cae
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); for(let a=-1;a<=1;a++) for(let c=-1;c<=1;c++) freeAddStatic({k:'b',a:0,b:6},FREE.X+a,FREE.Y+2.5,FREE.Z+c,0,true);
        for(let a=-1;a<=1;a++) for(let c=-1;c<=1;c++) freeAddStatic({k:'b',a:0,b:6},FREE.X+a,FREE.Y,FREE.Z+c,0,true);
        const v0=__VOL(); let poured=0; for(let i=0;i<60;i++){ poured+=suPour(FREE.X,FREE.Z,4,0,.03,.5)||0; __S(1); } let drops=0, mid=0; for(let i=0;i<300;i++){ __S(1); for(const P of FU.pts) if(!P.o && P.p===4 && P.y<FREE.Y+2.45 && P.y>FREE.Y+1.1){ mid++; } }
        suRecount(); let below=0; for(const C of SU.list) for(let k=0;k<256;k++) if(C.h[k]>0 && C.t[k]===4){ const b=suB(C,k); if(b<FREE.Y+1.1) below+=C.h[k]*.04; }
        return [mid, +below.toFixed(3), __WL(4)[0], +(__VOL()-v0-poured).toFixed(4)]; })()""")
    ok(r[0]>5 and r[1]>.005, '💧 donde la pared se acaba la gota cuelga, engorda y se cae (%s ratos cayendo; %s m³ llegaron abajo)'%(r[0],r[1]))
    ok(abs(r[3])<.01, 'sin perder miel (%s m³)'%r[3])
    # 6. si quitas el bloque, lo que estaba en su pared se cae
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); __TOW(0,0); for(let i=0;i<120;i++){ suPour(FREE.X,FREE.Z,4,0,.03,.5); __S(1); } __S(60); const v0=__VOL(), w0=__WL(4)[2];
        const o=FREE.objs.find(q=>q.sel && q.sel.k==='b' && Math.abs(q.x-FREE.X)<.1 && q.z<FREE.Z-.9 && q.y>FREE.Y+.5); freeDrop(o); __S(3); const fall=FU.pts.filter(P=>!P.o && P.p===4).length; __S(150);
        return [w0, fall, __WL(4)[2], +(__VOL()-v0).toFixed(4)]; })()""")
    ok(r[1]>0 and r[2]<r[0], '🧱 si quitas un bloque, la miel de su pared se cae (%s gotitas; en la pared había %s y quedan %s m³)'%(r[1],r[0],r[2]))
    ok(abs(r[3])<.01, 'y no se pierde (%s m³)'%r[3])
    # 7. se guarda con el mundo y se carga igual
    r=await ev("""(()=>{ const a=__WL(4); const pk=wlPack(); const s=JSON.stringify(pk||[]); suClear(); const b=__WL(4); wlUnpack(JSON.parse(s)); const c=__WL(4); return [a,b,c,s.length]; })()""")
    ok(r[1][1]==0 and abs(r[2][2]-r[0][2])<.002 and abs(r[2][1]-r[0][1])<=r[0][1]*.03, '💾 lo de las paredes se guarda con el mundo y vuelve igual (%s → %s m³; %s letras)'%(r[0][2],r[2][2],r[3]))
    # 8. el agua no se queda en la pared (cae en chorro); la pintura sí, con su color
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); __TOW(0,0); for(let i=0;i<60;i++){ suPour(FREE.X,FREE.Z,1,0,.03,.5); __S(1); } const wa=SU.wl.size;
        __CLR(); suClear(); FU.pts.length=0; __TOW(0,0); for(let i=0;i<90;i++){ suPour(FREE.X,FREE.Z,5,3,.03,.5); __S(1); } let pc=0, ok=0; for(const W of SU.wl.values()) for(let i=0;i<1024;i++) if(W.h[i]>0 && W.t[i]===5){ pc++; if((W.c[i]&0xffffff)===(suCol(3)&0xffffff)) ok++; }
        return [wa, pc, ok]; })()""")
    ok(r[0]==0, '💧 el agua no se queda pegada en la pared: cae en chorro (%s hojas)'%r[0])
    ok(r[1]>20 and r[2]==r[1], '🎨 la pintura sí escurre por la pared, con su color (%s cuadritos)'%r[1])
    # 9. rendimiento: 4 paredes con miel corriendo
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); __TOW(0,0); for(let i=0;i<120;i++){ suPour(FREE.X,FREE.Z,4,0,.03,.5); __S(1); }
        __LOOK(FREE.X,FREE.Y+1,FREE.Z); let t0=performance.now(); for(let i=0;i<40;i++) wlTick(.033); const tick=(performance.now()-t0)/40;
        for(const W of SU.wl.values()) W.dirty=true; t0=performance.now(); for(const W of SU.wl.values()) wlBuild(W); const build=(performance.now()-t0)/SU.wl.size;
        let draws=0; for(const W of SU.wl.values()) for(const M of W.ms) if(M && M.visible) draws++; return [+tick.toFixed(2), +build.toFixed(2), draws, SU.wl.size]; })()""")
    ok(r[0]<2.5, '⚡ calcular las 4 paredes con miel corriendo cuesta %s ms por cuadro (aquí, sin tarjeta de video)'%r[0])
    ok(r[2]<=r[3], 'y se dibuja con un dibujo por pared (%s dibujos, %s hojas; armar cada una %s ms)'%(r[2],r[3],r[1]))
    # 10. escoba/limpiar: se borra todo, también las paredes
    r=await ev("(()=>{ suClear(); return [SU.wl.size, FREE.g.children.filter(o=>o.isMesh && o.material && o.material===fuFlowMat(4) && o.visible).length]; })()")
    ok(r[0]==0 and r[1]==0, '🧹 al limpiar también se limpian las paredes %s'%r)
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
