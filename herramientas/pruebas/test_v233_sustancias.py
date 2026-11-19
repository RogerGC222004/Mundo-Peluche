# v233 (Modo libre): 🪣 Sustancias, segunda ronda. Las espesas salen mucho más de la cubeta; un cuarto de bloques se llena como
# recipiente (y se derrama por arriba o por un hueco); una sustancia encima de otra queda en capas (la espuma flota) y algunas se
# mezclan (agua + pintura, pintura + pintura, agua + lodo, slime + pintura); la bola lleva justo su volumen y cae de su tamaño;
# ondas solo en el agua (y la pintura), el slime tiembla, el lodo salpica gotas de verdad, la espuma tiene burbujas que revientan;
# la superficie se dibuja lisita y no se mete en los bloques.
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
    pg.on("console", lambda m: errs.append(m.text) if m.type=='warning' and ('juguetes' in m.text or 'gadgets' in m.text) else None)
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev("(()=>{ freeEnter(); return 1; })()"); await ev(STEP)
    H="""window.__LOOKAT=(x,z)=>{ camMode='first'; camera.position.set(player.pos.x,player.pos.y+1.6,player.pos.z); camera.lookAt(x,FREE.Y,z); camera.updateMatrixWorld(); };
      window.__AREA=(p)=>{ let n=0, mx=0, v=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===p && C.h[i]>.0015){ n++; mx=Math.max(mx,C.h[i]); v+=C.h[i]*.04; } return [n,+mx.toFixed(3),+v.toFixed(4)]; };
      window.__H=(x,z)=>{ const q=suAt(x,z); return q?+q[1].toFixed(3):0; }; 1"""
    await ev(H)
    # 1. cuánto sale en 1 s con el chorro grande
    r=await ev("""(()=>{ const out={}; for(const p of [1,2,3,4,6]){ __CLR(); suClear(); __AT(-20,-20); freeSelect({k:'s',a:p,b:0}); SU.mode=2; __S(1); SU.holdEnd=0; __LOOKAT(FREE.X-20,FREE.Z-16); suHoldStart(); for(let i=0;i<30;i++){ __LOOKAT(FREE.X-20,FREE.Z-16); suTick(1/30); } suHoldEnd(); suRecount(); out[SU_T[p].id]=+SU.vol.toFixed(3); freeSelect(null); } return out; })()""")
    ok(r['agua']<.2 and r['slime']>r['agua']*3 and r['miel']>r['agua']*3 and r['lodo']>r['agua']*3.5 and r['espuma']>r['agua']*5, 'las espesas salen mucho más que el agua en 1 s con el chorro grande %s'%r)
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); suPour(FREE.X-20,FREE.Z-16,3,0,.6,.8); __S(60); return __AREA(3); })()""")
    ok(r[1]>.18, 'el lodo se queda amontonado, con volumen (lo más alto: %s m)'%r[1])
    # 2. un cuarto de bloques se llena como recipiente
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); const X=Math.floor(FREE.X-12), Z=Math.floor(FREE.Z-12), B=[]; for(let n=0;n<5;n++) for(let m=0;m<5;m++){ if(n%4 && m%4) continue; B.push(freeAddStatic({k:'b',a:0,b:0},X+n+.5,FREE.Y,Z+m+.5,0)); }
        for(let k=0;k<10;k++){ suPour(X+2.5,Z+2.5,1,0,.3,1); __S(8); } __S(120); let inn=[], out=0; for(const C of SU.list) for(let i=0;i<256;i++){ if(C.h[i]<=0) continue; const [x,z]=suXZ(C,i); if(x>X+1 && x<X+4 && z>Z+1 && z<Z+4) inn.push(suB(C,i)+C.h[i]); else out++; }
        const lv=[Math.min(...inn),Math.max(...inn)], n0=inn.length; const W=B.find(o=>Math.abs(o.x-(X+4.5))<.1 && Math.abs(o.z-(Z+2.5))<.1); freeDrop(W); __S(150); let out2=0; for(const C of SU.list) for(let i=0;i<256;i++){ if(C.h[i]<=0) continue; const [x,z]=suXZ(C,i); if(!(x>X+1 && x<X+4 && z>Z+1 && z<Z+4)) out2++; }
        return [n0, out, +(lv[0]-FREE.Y).toFixed(3), +(lv[1]-lv[0]).toFixed(3), out2]; })()""")
    ok(r[0]==225 and r[1]==0 and .25<r[2]<.4 and r[3]<.02, 'el cuarto se llena parejito (nivel %s m, diferencia %s m) y no se sale nada %s'%(r[2],r[3],r[:2]))
    ok(r[4]>10, 'si quitas un bloque de la pared, sale por el hueco (%s cuadritos afuera)'%r[4])
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); const X=Math.floor(FREE.X-12), Z=Math.floor(FREE.Z-12); for(let n=0;n<3;n++) for(let m=0;m<3;m++){ if(n===1 && m===1) continue; freeAddStatic({k:'b',a:0,b:0},X+n+.5,FREE.Y,Z+m+.5,0); }
        for(let k=0;k<14;k++){ suPour(X+1.5,Z+1.5,1,0,.12,.3); __S(4); } __S(150); let inn=0, out=0, top=0; for(const C of SU.list) for(let i=0;i<256;i++){ if(C.h[i]<=0) continue; const [x,z]=suXZ(C,i); if(x>X+1 && x<X+2 && z>Z+1 && z<Z+2){ inn++; top=Math.max(top,suB(C,i)+C.h[i]-FREE.Y); } else out++; } return [inn,out,+top.toFixed(2)]; })()""")
    ok(r[1]>0 and r[2]>.95, 'si lo llenas hasta arriba, se derrama por la orilla %s'%r)
    # 3. el dibujo no se mete en los bloques (arriba de un bloque, ni junto a la pared)
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); const X=Math.floor(FREE.X-12), Z=Math.floor(FREE.Z-12); const o=freeAddStatic({k:'b',a:0,b:0},X+.5,FREE.Y,Z+.5,0); for(let n=0;n<4;n++) freeAddStatic({k:'b',a:0,b:0},X+3+n+.5,FREE.Y,Z+.5,0);
        suPour(X+.5,Z+.5,2,0,.06,.3); suPour(X+5,Z+1.6,1,0,.2,.6); suPour(X+5,Z+1.6,3,0,.05,.3); __S(60); for(const C of SU.list) suBuild(C);
        const boxes=FREE.objs.map(q=>q.box); let bad=0, onTop=0, n=0; for(const C of SU.list) for(const M of C.ms){ if(!M || !M.visible) continue; const P=M.geometry.attributes.position.array, N=M.geometry.drawRange.count/6*4;
          for(let v=0;v<N;v++){ const x=P[v*3], y=P[v*3+1], z=P[v*3+2]; n++; for(const b of boxes){ if(x>b.min.x+.012 && x<b.max.x-.012 && z>b.min.z+.012 && z<b.max.z-.012 && y<b.max.y-.006){ bad++; } if(x>b.min.x && x<b.max.x && z>b.min.z && z<b.max.z && y>=b.max.y-.006) onTop++; } } }
        return [n, bad, onTop]; })()""")
    ok(r[0]>100 and r[1]==0 and r[2]>0, 'lo de arriba de un bloque y lo que toca una pared no se mete en los bloques %s'%r)
    # 4. capas
    r=await ev("""(()=>{ const out={}; __CLR(); suClear(); __AT(-20,-20); const X=FREE.X-14, Z=FREE.Z-14; const cel=(x,z)=>{ const q=suCell(x,z,false); return q?[q[0].t[q[1]], q[0].t2[q[1]], +q[0].h[q[1]].toFixed(3), +q[0].h2[q[1]].toFixed(3)]:null; };
        suPour(X,Z,3,0,.35,1.3); __S(30); suPour(X,Z,4,0,.02,.3); __S(10); out.mielSobreLodo=cel(X,Z);
        suPour(X+5,Z,6,0,.08,.4); __S(5); suPour(X+5,Z,1,0,.04,.3); __S(20); out.aguaBajoEspuma=cel(X+5,Z);
        suPour(X+10,Z,1,0,.12,.6); __S(30); suPour(X+10,Z,6,0,.05,.3); __S(10); out.espumaSobreAgua=cel(X+10,Z); return out; })()""")
    ok(r['mielSobreLodo'][0]==3 and r['mielSobreLodo'][1]==4, 'la miel encima del lodo queda en capas, como pastel %s'%r['mielSobreLodo'])
    ok(r['aguaBajoEspuma'][0]==1 and r['aguaBajoEspuma'][1]==6 and r['espumaSobreAgua'][0]==1 and r['espumaSobreAgua'][1]==6, 'la espuma siempre flota (aunque eches el agua después) %s'%r)
    # 5. mezclas
    r=await ev("""(()=>{ const out={}; __CLR(); suClear(); __AT(-20,-20); const X=FREE.X-14, Z=FREE.Z-14, hx=c=>(c&0xffffff).toString(16).padStart(6,'0'); const cel=(x,z)=>{ const q=suCell(x,z,false); return [q[0].t[q[1]], hx(q[0].c[q[1]]), q[0].s[q[1]]]; };
        suPour(X,Z,1,0,.3,.5); __S(20); suPour(X,Z,5,0,.004,.3); __S(40); out.aguaRoja=cel(X,Z);
        suPour(X+5,Z,5,2,.03,.3); suPour(X+5.2,Z,5,6,.03,.3); __S(40); out.amarilloAzul=cel(X+5.1,Z);
        suPour(X+10,Z,2,0,.1,.4); __S(10); suPour(X+10,Z,5,7,.03,.3); __S(20); out.slimeMorado=cel(X+10,Z);
        suPour(X,Z+6,3,0,.15,.4); suPour(X,Z+6,1,0,.12,.4); suPour(X+6,Z+6,3,0,.15,.4); __S(150); out.lodoAguado=cel(X,Z+6); let a=0, b=0; for(const C of SU.list) for(let i=0;i<256;i++){ if(C.t[i]!==3 && C.t[i]!==1) continue; const [x,z]=suXZ(C,i); if(Math.hypot(x-X,z-Z-6)<3) a++; if(Math.hypot(x-X-6,z-Z-6)<3) b++; } out.area=[a,b]; return out; })()""")
    g=lambda h:[int(h[i:i+2],16) for i in (0,2,4)]
    ok(r['aguaRoja'][0]==1 and 0<r['aguaRoja'][2]<128 and g(r['aguaRoja'][1])[0]>150, 'agua + un poco de pintura = agua de color %s'%r['aguaRoja'])
    c=g(r['amarilloAzul'][1]); ok(r['amarilloAzul'][0]==5 and c[1]>c[0] and c[1]>c[2], 'pintura amarilla + azul = verde (%s)'%r['amarilloAzul'][1])
    ok(r['slimeMorado'][0]==2 and r['slimeMorado'][2]>0 and r['slimeMorado'][1]!='000000', 'slime + pintura = slime de color %s'%r['slimeMorado'])
    ok(r['lodoAguado'][0]==3 and r['lodoAguado'][2]>0 and r['area'][0]>r['area'][1], 'agua + lodo = lodo aguado, que corre más (%s contra %s cuadritos)'%tuple(r['area']))
    # 6. la bola lleva su volumen y cae de su tamaño
    r=await ev("""(()=>{ const out={}; for(const p of [3,1]){ __CLR(); suClear(); __AT(-20,-20); const X=FREE.X-14, Z=FREE.Z-14, R=.4; suLaunch(p,0,R,[X,FREE.Y+2,Z,0,-3,0]); const v=SU.balls[0].v; let n=0, k=0; for(;k<40 && SU.balls.length;k++) __S(1); __S(1);
        for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===p && C.h[i]>0){ const [x,z]=suXZ(C,i); if(Math.hypot(x-X,z-Z)<1.2) n++; } const r0=Math.sqrt(n*.04/Math.PI); __S(90); suRecount(); out[SU_T[p].id]=[+v.toFixed(3), +SU.vol.toFixed(3), +r0.toFixed(2)]; } return out; })()""")
    ok(abs(r['lodo'][1]-r['lodo'][0])<r['lodo'][0]*.05 and abs(r['agua'][1]-r['agua'][0])<r['agua'][0]*.06, 'lo que cae es justo lo que llevaba la bola %s'%r)
    ok(.25<r['lodo'][2]<.7, 'la bola de lodo (radio .4) deja una plasta de su tamaño (radio %s m)'%r['lodo'][2])
    # 7. cada una a su manera: ondas solo en el agua; el slime tiembla, la miel no; el lodo salpica gotas de lodo; la espuma revienta
    r=await ev("""(()=>{ const out={}; for(const p of [1,2,3,4,6]){ __CLR(); suClear(); __AT(-20,-20); const X=FREE.X-14, Z=FREE.Z-14; suPour(X,Z,p,0,p===6?.3:.15,.7); __S(30); SU.rip.length=0; SU.U.uRipN.value=0; SU.pops.length=0; let drops=0, wb=0, pops=0; const v0=(suRecount(),SU.vol);
        player.pos.set(X-1.4,FREE.Y+.05,Z); for(let i=0;i<40;i++){ player.pos.x+=.07; player.vel.set(2.1,0,0); __S(1); drops=Math.max(drops,SU.drops.filter(d=>d.p===3).length); pops=Math.max(pops,SU.pops.length); for(const C of SU.list) for(let k=0;k<256;k++) wb=Math.max(wb,C.wb[k]); }
        suRecount(); out[SU_T[p].id]=[SU.rip.length, +wb.toFixed(2), drops, pops, +(SU.vol/v0).toFixed(2)]; } return out; })()""")
    ok(r['agua'][0]>0 and r['lodo'][0]==0 and r['slime'][0]==0 and r['miel'][0]==0, 'las ondas solo salen en el agua %s'%{k:v[0] for k,v in r.items()})
    ok(r['slime'][1]>0 and r['miel'][1]==0, 'el slime tiembla al pisarlo; la miel no %s'%{k:v[1] for k,v in r.items()})
    ok(r['lodo'][2]>0, 'al correr por el lodo salpican gotitas de lodo de verdad (%s)'%r['lodo'][2])
    ok(r['espuma'][3]>0 and r['espuma'][4]<.85, 'al pasar por la espuma sus burbujas revientan (chispitas %s; queda %s)'%(r['espuma'][3],r['espuma'][4]))
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); const X=FREE.X-14, Z=FREE.Z-14; suPour(X,Z,6,0,.3,.6); __S(5); camMode='first'; camera.position.set(X,FREE.Y+2,Z-3); camera.lookAt(X,FREE.Y,Z); camera.updateMatrixWorld(); suFoamDraw(); return SU.bub?SU.bub.count:0; })()""")
    ok(r>40, 'la espuma tiene burbujitas de verdad encima (%s)'%r)
    # 8. lisita: donde se juntan dos cuadritos, la luz es la misma (sin escalones)
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); const X=FREE.X-14, Z=FREE.Z-14; suPour(X,Z,3,0,.5,.6); suPour(X+3,Z,4,0,.3,.6); __S(60); for(const C of SU.list) suBuild(C); let mx=0, n=0; const mp=new Map();
        for(const C of SU.list) for(const M of C.ms){ if(!M || !M.visible) continue; const P=M.geometry.attributes.position.array, Nn=M.geometry.attributes.normal.array, N=M.geometry.drawRange.count/6*4;
          for(let v=0;v<N;v++){ const k=M.id+':'+Math.round(P[v*3]*500)+','+Math.round(P[v*3+2]*500), e=mp.get(k); if(e){ n++; mx=Math.max(mx,Math.abs(e[0]-Nn[v*3])+Math.abs(e[1]-Nn[v*3+1])+Math.abs(e[2]-Nn[v*3+2]),Math.abs(e[3]-P[v*3+1])); } else mp.set(k,[Nn[v*3],Nn[v*3+1],Nn[v*3+2],P[v*3+1]]); } }
        return [n, +mx.toFixed(4)]; })()""")
    ok(r[0]>200 and r[1]<.002, 'la superficie es lisita: las esquinas compartidas tienen la misma altura y la misma luz %s'%r)
    # 9. guardar con capas y colores (y los guardados de antes)
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); const X=FREE.X-14, Z=FREE.Z-14; suPour(X,Z,3,0,.35,1.3); __S(20); suPour(X,Z,4,0,.02,.3); suPour(X+5,Z,5,2,.03,.3); suPour(X+5.2,Z,5,6,.03,.3); __S(30); suRecount(); const v0=SU.vol;
        const pk=JSON.parse(JSON.stringify(suPack())); suUnpack(pk); suRecount(); const q=suCell(X,Z,false), q2=suCell(X+5.1,Z,false); const a=[q[0].t[q[1]],q[0].t2[q[1]]], c=(q2[0].c[q2[1]]&0xffffff).toString(16), v1=SU.vol;
        suClear(); const C=suChunk(0,0,true); suDec(C,'0,10;5,6,3,1e1e1e;0,243'); return [+v0.toFixed(3), +v1.toFixed(3), a, c, C.t[10], (C.c[10]&0xffffff).toString(16), C.s[10], +C.h[11].toFixed(3)]; })()""")
    ok(abs(r[1]-r[0])<r[0]*.03 and r[2]==[3,4], 'se guardan las capas y los colores (%s → %s m³, capas %s, color %s)'%(r[0],r[1],r[2],r[3]))
    ok(r[4]==5 and r[5]=='3f6fc6' and r[6]==255 and abs(r[7]-.15)<.01, 'los mundos guardados antes (v232) se siguen abriendo bien %s'%r[4:])
    # 10. lo que tarda
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); [1,2,3,4,5,6].forEach((p,k)=>suPour(FREE.X-30+k*6,FREE.Z+10,p,3,.15*SU_T[p].vm,.4)); suPour(FREE.X-30,FREE.Z+10,5,0,.02,.3); suPour(FREE.X-18,FREE.Z+10,4,0,.05,.3); const t0=performance.now(); for(let i=0;i<60;i++) suTick(1/30); const ms=(performance.now()-t0)/60;
        const C=SU.list.reduce((a,c)=>c.n>a.n?c:a); const t1=performance.now(); for(let i=0;i<20;i++){ C.dirty=true; suBuild(C); } const mb=(performance.now()-t1)/20; return [+ms.toFixed(2), +mb.toFixed(2), C.n]; })()""")
    ok(r[0]<8 and r[1]<4, 'con 6 sustancias (y capas) moviéndose tarda %s ms por cuadro; dibujar un trozo lleno %s ms (aquí, sin tarjeta de video)'%(r[0],r[1]))
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close(); await b.close()
asyncio.run(m())
