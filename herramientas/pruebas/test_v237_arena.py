# v237 (Modo libre): la arena. No corre como líquido: se amontona con su pendiente de verdad (~33°) y solo se desliza si está más
# empinada; mojada aguanta paredes (castillos) y con mucha agua se vuelve lodo; se seca solita. Te paras encima, dejas huellas y saltan
# granitos; las pelotas, las cajas y el carrito se paran encima y dejan su marca; lo que cae de una orilla o sale de la máquina se ve
# como granitos cayendo. Se guarda con el mundo.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.033); update(.033,t); } };
  window.__CLR=()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); FREE.hold=null; freeSelect(null); };
  window.__AT=(x,z)=>{ player.pos.set(FREE.X+x,FREE.Y+.05,FREE.Z+z); player.vel.set(0,0,0); player.vy=0; player.facing=0; yaw=Math.PI; FREE.ppPrev=null; __S(2); };
  window.__PILE=(x,z,n,s)=>{ for(let i=0;i<n;i++){ suPour(FREE.X+x,FREE.Z+z,7,0,.02,.3,s||0); __S(1); } __S(90); };
  window.__SLOPE=(x,z)=>{ const X=FREE.X+x, Z=FREE.Z+z, t0=suSandTop(X,Z); let r=0; for(let d=.2;d<4;d+=.1){ if(suSandTop(X+d,Z)<=-1e8 && suSandTop(X-d,Z)<=-1e8){ r=d; break; } } return [t0-FREE.Y, r]; }; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type=='error' and ('shader' in m.text or 'WebGL' in m.text) else None)
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev("(()=>{ freeEnter(); return 1; })()"); await ev(STEP)

    # 0. la arena está en el menú de sustancias y en la máquina
    r=await ev("(()=>{ const T=SU_BY.arena; const f=freeAddStatic({k:'p',a:'fuentes',b:0},FREE.X+30,FREE.Y,FREE.Z,0,true); fuSet(f,[0,1,2,3].map(i=>({on:0,p:7,q:1,x:1,col:0}))); const c=fuCfg(f); freeDrop(f); return [!!T, T&&T.i, c[0].p]; })()")
    ok(r[0] and r[1]==7 and r[2]==7, '🏖️ la arena está entre las sustancias (cubeta y máquina) %s'%r)

    # 1. el montón: pendiente de arena de verdad, y se queda quieto
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-10); __PILE(0,0,120); const [h,rad]=__SLOPE(0,0); suRecount(); const v0=SU.vol; __S(240); const [h2]=__SLOPE(0,0); suRecount();
        return [+h.toFixed(2), +rad.toFixed(2), +(h/rad).toFixed(2), +(h2-h).toFixed(3), SU.list.filter(C=>C.aw>0 && C.n).length, +(SU.vol-v0).toFixed(4)]; })()""")
    ok(r[2]>.5 and r[2]<.85, '⛰️ la arena hace un montón con su pendiente de verdad (%s m de alto, %s m de radio: %.0f°)'%(r[0],r[1],__import__('math').degrees(__import__('math').atan(r[2]))))
    ok(abs(r[3])<.03 and r[4]==0, 'y se queda quieto: no se escurre como líquido (cambió %s m; trocitos despiertos %s)'%(r[3],r[4]))
    ok(abs(r[5])<.001, 'sin perder ni inventar arena (%s m³)'%r[5])

    # 2. mojada aguanta paredes (más empinada), y se ve más oscura
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-10); __PILE(0,0,120,200); const [h,rad]=__SLOPE(0,0); return [+h.toFixed(2), +rad.toFixed(2), +(h/rad).toFixed(2), suSandWet(FREE.X,FREE.Z), suHex(7,0,200)!==suHex(7,0,0)]; })()""")
    ok(r[2]>1.0, '🏰 la arena mojada aguanta formas paradas, como para castillos (%s de pendiente; la seca ~0.65)'%r[2])
    ok(r[3]>150 and r[4], 'y se ve más oscurita (qué tan mojada: %s de 255)'%r[3])

    # 3. el agua encima la moja; mucha agua la vuelve lodo; se seca solita
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-10); const X=FREE.X, Z=FREE.Z; for(let x=-1;x<=1.01;x+=.2) for(let z=-1;z<=1.01;z+=.2) suPour(X+x,Z+z,7,0,.15*.04,.1); __S(10);
        for(let i=0;i<20;i++){ suPour(X,Z,1,0,.004,.4); __S(1); } __S(60); const w1=suSandWet(X,Z); __S(300); const w2=suSandWet(X,Z);
        for(let i=0;i<150;i++){ suPour(X+.4,Z,1,0,.02,.3); __S(1); } __S(300); let mud=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===3) mud++;
        suClear(); __PILE(4,0,40,200); const d1=suSandWet(X+4,Z); __S(300); const d2=suSandWet(X+4,Z); return [w1, d2, mud, d1]; })()""")
    ok(r[0]>40, '💧 el agua que le cae encima la moja (se la chupa): %s de 255'%r[0])
    ok(r[1]<r[3]-5, '☀️ y la arena mojada se va secando solita (%s → %s en 10 s)'%(r[3],r[1]))
    ok(r[2]>3, '🟤 con mucha agua se vuelve lodo (%s cuadritos de lodo)'%r[2])

    # 4. caminar encima: te paras arriba, vas más despacio, quedan huellas y saltan granitos
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; GR.n=0; const X=FREE.X, Y=FREE.Y, Z=FREE.Z; for(let x=-2;x<=2.01;x+=.2) for(let z=-1;z<=1.01;z+=.2) suPour(X+x,Z+z,7,0,.25*.04,.1); __S(20);
        player.pos.set(X-1.8,Y+.4,Z); player.facing=Math.PI/2; __S(4); let gap=0, gmax=0; const top0=suSandTop(X,Z); yaw=-Math.PI/2; for(let i=0;i<30;i++){ stick.x=0; stick.y=-1; yaw=-Math.PI/2; __S(1); const t=suSandTop(player.pos.x,player.pos.z); if(t>-1e8) gap=Math.max(gap,t-player.pos.y); gmax=Math.max(gmax,GR.n); }
        const sand=(player.pos.x-(X-1.8))/(30*.033); stick.y=0; __AT(0,-12); const g0=player.pos.x; for(let i=0;i<30;i++){ stick.x=0; stick.y=-1; yaw=-Math.PI/2; __S(1); } stick.y=0; const grass=(player.pos.x-g0)/(30*.033);
        const fp=suSandTop(X,Z); return [+gap.toFixed(3), +sand.toFixed(2), +grass.toFixed(2), +(top0-fp).toFixed(3), gmax, player.swim]; })()""")
    ok(r[0]<.1, '🚶 en la arena te paras encima: solo se te hunden los pies un poquito (%s m), no te hundes como en el agua'%r[0])
    ok(r[1]<r[2]*.95, 'y caminas un poco más despacio (%s m/s contra %s en el pasto)'%(r[1],r[2]))
    ok(r[3]>.015, '👣 quedan tus huellas (%s m de hondo)'%r[3])
    ok(r[4]>5, '✨ y saltan granitos al caminar (%s a la vez)'%r[4])

    # 5. en un montón muy hondo no se nada
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; const X=FREE.X, Y=FREE.Y, Z=FREE.Z; for(let x=-1.4;x<=1.41;x+=.2) for(let z=-1.4;z<=1.41;z+=.2) suPour(X+x,Z+z,7,0,1.3*.04,.1,220); __S(20); player.pos.set(X,Y+1.4,Z); __S(30); return [player.swim, +(player.pos.y-Y).toFixed(2), +(suSandTop(X,Z)-Y).toFixed(2)]; })()""")
    ok(not r[0] and r[1]>r[2]-.15, '🏊 en la arena no se nada: te quedas parado encima (a %s m; la arena llega a %s m)'%(r[1],r[2]))

    # 6. las pelotas y las cajas se paran encima; al moverse dejan su marca; la arena las frena
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-10); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; for(let x=-2.4;x<=2.41;x+=.2) for(let z=-1.2;z<=1.21;z+=.2) suPour(X+x,Z+z,7,0,.3*.04,.1); __S(20);
        const b=freeAddDyn('goma',X-2,Y+.8,Z,true); __S(30); const yb=b.root.position.y-Y; b.v.set(5,0,0); const x0=b.root.position.x; __S(45); const dS=b.root.position.x-x0, groove=.3-(suSandTop(X-1.2,Z)-Y);
        const c=freeAddDyn('goma',X-2,Y+.4,Z-8,true); __S(20); c.v.set(5,0,0); const x1=c.root.position.x; __S(45); const dG=c.root.position.x-x1;
        const L=bxPlaceMulti('torre',X+1,Y+.35,Z,0,true); L.forEach(d=>bxWake(d)); __S(150); const by=Math.min(...L.map(d=>d.bx.x.y-Y));
        return [+yb.toFixed(2), +dS.toFixed(2), +dG.toFixed(2), +groove.toFixed(3), +by.toFixed(2)]; })()""")
    ok(r[0]>.45 and r[0]<.6, '⚽ la pelota se para encima de la arena (a %s m; la arena llega a 0.3 y la pelota mide 0.25 de radio)'%r[0])
    ok(r[1]<r[2]*.8, 'la arena la frena más que el pasto (rodó %s m contra %s m)'%(r[1],r[2]))
    ok(r[3]>.008, 'y deja su surquito (%s m)'%r[3])
    ok(r[4]>.3, '🧱 los bloques se quedan encima de la arena, no se meten (el más bajito a %s m)'%r[4])

    # 7. el carrito: deja marcas de llantas y la arena lo frena un poco
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; const X=FREE.X, Y=FREE.Y, Z=FREE.Z; for(let x=-1.2;x<=1.21;x+=.2) for(let z=-3;z<=3.01;z+=.2) suPour(X+x,Z+z,7,0,.15*.04,.1); __S(20);
        const o=freeAddStatic({k:'v',a:'carrito',b:0},X,Y,Z-9,0,true); __S(2); player.pos.set(X,Y+.05,Z-9.6); __S(1); pqRide(o,0); yaw=Math.PI; stick.y=-1; __S(1); const D=player.pg && player.pg.drive; if(!D) return null;
        const t0=suSandTop(X+.28,Z), t1=suSandTop(X,Z); let out=0, inn=9; for(let i=0;i<120;i++){ stick.y=-1; stick.x=0; __S(1); if(D.z<Z-4) out=Math.max(out,D.v); if(Math.abs(D.z-Z)<1.5) inn=Math.min(inn,D.v); } stick.y=0; stopPlay(); __S(2);
        return [+out.toFixed(1), +inn.toFixed(1), +(t0-suSandTop(X+.28,Z)).toFixed(3), +(t1-suSandTop(X,Z)).toFixed(3)]; })()""")
    ok(r is not None and r[1]<r[0]*.97, '🚗 la arena frena un poco al carrito (afuera %s m/s, en la arena %s m/s)'%((r[0],r[1]) if r else (None,None)))
    ok(r is not None and r[2]>.01, '🛞 y quedan las marcas de las llantas (%s m de hondo)'%(r[2] if r else None))

    # 8. lo que cae de una orilla se ve como granitos cayendo; al pie se hace el montón
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; GR.n=0; __AT(-8,-8); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; for(let a=0;a<2;a++) for(let c=0;c<2;c++) for(let y=0;y<2;y++) freeAddStatic({k:'b',a:0,b:6},X+a,Y+y,Z+c,0,true); __S(1);
        let fu=0, pts=0; for(let i=0;i<70;i++){ suPour(X+.5,Z+.5,7,0,.03,.5,0,Y+3); __S(1); fu=Math.max(fu,FU.pts.filter(P=>P.p===7).length); pts=Math.max(pts,GR.M?GR.M.geometry.drawRange.count:0); } __S(150);
        let foot=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===7 && C.h[i]>.02){ const [x,z]=suXZ(C,i); if(suB(C,i)<Y+.1 && Math.max(Math.abs(x-X-.5),Math.abs(z-Z-.5))>1.05) foot++; } return [fu, pts, foot]; })()""")
    ok(r[0]>5 and r[1]>40, '⏳ la arena que cae de una orilla baja en granitos (%s chorritos, %s granitos a la vez)'%(r[0],r[1]))
    ok(r[2]>10, 'y abajo se hace su montón (%s cuadritos con arena al pie)'%r[2])

    # 9. la máquina echa arena
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-10); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; const f=freeAddStatic({k:'p',a:'fuentes',b:0},X-4,Y,Z,0,true); fuSet(f,[0,1,2,3].map(i=>({on:i===3?1:0,p:7,q:2,x:1,col:0}))); f.hose={x:X-1.2,z:Z,a:Math.PI/2,held:null};
        __S(150); let n=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===7 && C.h[i]>0) n++; fuSet(f,[0,1,2,3].map(i=>({on:0,p:7,q:2,x:1,col:0}))); return [n]; })()""")
    ok(r[0]>10, '🚿 la máquina con arena hace su montón (%s cuadritos)'%r[0])

    # 10. se guarda con el mundo (y lo mojada)
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-10); __PILE(0,0,60,160); suRecount(); const v0=SU.vol, w0=suSandWet(FREE.X,FREE.Z); const P=suPack(); suClear(); suUnpack(P); __S(2); suRecount(); return [+v0.toFixed(3), +SU.vol.toFixed(3), w0, suSandWet(FREE.X,FREE.Z), SU.hasSand]; })()""")
    ok(abs(r[0]-r[1])<.01 and abs(r[2]-r[3])<20 and r[4], '💾 la arena se guarda con el mundo, y lo mojada también (%s → %s m³; %s → %s)'%tuple(r[:4]))

    # 11. rendimiento
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-6); __PILE(0,0,150); __PILE(3,1,80,200); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; player.pos.set(X-2.5,Y+.05,Z); __S(2);
        let t0=performance.now(); for(let i=0;i<60;i++){ player.vel.set(2.5,0,.3); suPour(X+.3,Z-.3,7,0,.01,.3,0,Y+2); __S(1); } const a=(performance.now()-t0)/60; __AT(0,-6); __S(200); t0=performance.now(); __S(60); const b2=(performance.now()-t0)/60; return [+a.toFixed(2), +b2.toFixed(2), GR.max]; })()""")
    ok(r[0]<8, '⚡ caminando en la arena mientras cae más: cada cuadro tarda %s ms (aquí, sin tarjeta de video)'%r[0])
    ok(r[1]<r[0], 'y quieta, menos: %s ms (granitos a la vez como máximo: %s)'%(r[1],r[2]))
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
