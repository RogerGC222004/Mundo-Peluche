# v237 (Modo libre): las cosas con física dentro de las sustancias. Flotan o se hunden según lo que pesan, la sustancia las frena suave
# (la miel y el lodo mucho, el agua poquito), lo que apartan se va como una olita y nunca se hacen torres ni picos. Nadar también abre
# una estela que se cierra sola, el carrito se frena y la va abriendo, y lo de lejos se dibuja aunque cerca no pare de moverse.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.033); update(.033,t); } };
  window.__CLR=()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); FREE.hold=null; freeSelect(null); };
  window.__AT=(x,z)=>{ player.pos.set(FREE.X+x,FREE.Y+.05,FREE.Z+z); player.vel.set(0,0,0); player.vy=0; player.facing=0; yaw=Math.PI; FREE.ppPrev=null; __S(2); };
  window.__POOL=(p,dep,walls)=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-12); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; if(walls!==false) for(let a=-3;a<=3;a++) for(let c=-3;c<=3;c++) if(Math.abs(a)===3||Math.abs(c)===3) for(let y=0;y<2;y++) freeAddStatic({k:'b',a:0,b:6},X+a,Y+y,Z+c,0,true);
    __S(1); const m=SU.cs; for(let x=-2.4;x<=2.41;x+=m) for(let z=-2.4;z<=2.41;z+=m) suPour(X+x,Z+z,p,0,dep*m*m,.1); __S(40); };
  window.__MX=()=>{ let mx=0; for(const C of SU.list) for(let i=0;i<256;i++){ const h=C.h[i]+C.h2[i]; if(h>mx) mx=h; } return mx; };
  window.__VOL=()=>{ suRecount(); return SU.vol+FU.pts.reduce((a,P)=>a+(P.v||0),0)+wlVol(); }; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev("(()=>{ freeEnter(); return 1; })()"); await ev(STEP)

    # 1. la torrecita de bloques en la miel (lo que vio Roger): los bloques que se mueven ya no hacen paredes ni picos
    r=await ev("""(()=>{ __POOL(4,.8); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; const h0=__MX(), v0=__VOL(); const L=bxPlaceMulti('torre',X,Y+.8,Z,0,true); let mx=0;
        for(let i=0;i<240;i++){ if(i%30===0) for(const d of L){ bxWake(d); d.v.x+=(Math.random()-.5)*3; d.v.z+=(Math.random()-.5)*3; } __S(1); mx=Math.max(mx,__MX()); }
        const ys=L.map(d=>d.bx.x.y-Y), avg=ys.reduce((a,b)=>a+b,0)/ys.length; __S(200); return [+h0.toFixed(2), +mx.toFixed(2), +(__VOL()-v0).toFixed(4), +avg.toFixed(2), L.filter(d=>d.sleep).length, L.length]; })()""")
    ok(r[1]<r[0]+.35, '🧱🍯 los bloques moviéndose en la miel ya no hacen paredes ni picos (lo más alto: %s m; antes de meterlos %s m)'%(r[1],r[0]))
    ok(abs(r[2])<.01, 'y no se inventa ni se pierde miel al apartarla (%s m³)'%r[2])
    ok(r[3]>.45, '🪵 los bloques son de madera: flotan en la miel (en promedio a %s m; la miel llega a 0.8)'%r[3])
    ok(r[4]>=r[5]-2, 'y cuando se calman se quedan quietos flotando (se duermen %s de %s)'%(r[4],r[5]))

    # 2. echarle miel encima a la torrecita: no se hacen torres de miel más altas que sin la torrecita
    r=await ev("""(()=>{ const out=[]; for(const tw of [true,false]){ __CLR(); suClear(); FU.pts.length=0; __AT(0,-9); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; const L=tw?bxPlaceMulti('torre',X,Y,Z,0,true):[];
        for(let i=0;i<300;i++){ suPour(X+(Math.random()-.5)*.6,Z+(Math.random()-.5)*.6,4,0,.05,.4,0,Y+3); __S(1); } out.push(+__MX().toFixed(2)); } return out; })()""")
    ok(r[0]<=r[1]+.3, '🍯 al echarle miel encima a la torrecita no se hacen torres de miel (con torrecita %s m, sin ella %s m)'%(r[0],r[1]))
    ok(r[1]<2.8, 'y la miel se escurre: un montón no sube como pico (%s m de alto con 15 m³)'%r[1])

    # 3. qué flota y qué se hunde (según lo que pesa cada cosa)
    r=await ev("""(()=>{ const R={}; for(const [p,dep] of [[1,1],[4,1],[3,1]]){ __POOL(p,dep); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; const ids=['playa','goma','caja','dado','boliche','canica'], ds={};
        ids.forEach((id,k)=>{ ds[id]=freeAddDyn(id,X+(k%3-1)*1.3,Y+1.8,Z+(Math.floor(k/3)-.5)*1.4,true); }); __S(240); R[SU_T[p].id]=Object.fromEntries(ids.map(id=>[id,+(ds[id].root.position.y-Y).toFixed(2)])); } return R; })()""")
    for sus in ['agua','miel','lodo']:
      q=r[sus]; fl=all(q[k]>.75 for k in ['playa','goma','caja','dado']); hu=all(q[k]<.5 for k in ['boliche','canica'])
      ok(fl and hu, '🛟 en %s: la pelota de playa, la de goma, la caja y el dado flotan; el boliche y la canica se hunden %s'%(sus,q))

    # 4. una pelota rodando por la miel se va frenando suave (no de golpe), y en el agua casi nada
    r=await ev("""(()=>{ const R=[]; for(const p of [4,1]){ __POOL(p,.35); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; const h0=__MX(); const b=freeAddDyn('goma',X-2.2,Y+.4,Z,true); b.v.set(7,0,0); const sp=[]; let mx=0;
        for(let i=0;i<30;i++){ __S(1); sp.push(Math.hypot(b.v.x,b.v.z)); mx=Math.max(mx,__MX()); } R.push([+sp[4].toFixed(1), +sp[14].toFixed(1), +sp[29].toFixed(1), +(mx-h0).toFixed(2)]); } return R; })()""")
    ok(r[0][0]>2.5 and r[0][1]<r[0][0] and r[0][2]<1.2, '⚽🍯 la pelota que rueda en la miel se va frenando poco a poco (%s → %s → %s m/s)'%tuple(r[0][:3]))
    ok(r[1][1]>r[0][1]+1, '💧 en el agua se frena mucho menos (%s m/s contra %s en la miel)'%(r[1][1],r[0][1]))
    ok(r[0][3]<.3 and r[1][3]<.3, 'y lo que va apartando es una olita, no un pico (miel +%s m, agua +%s m)'%(r[0][3],r[1][3]))

    # 5. nadar también abre la sustancia: una estela que se cierra sola (rápido en el agua, despacito en la miel)
    r=await ev("""(()=>{ const R={}; for(const p of [1,4]){ __POOL(p,1.1); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; player.pos.set(X-2.2,Y+.6,Z); __S(6); const t0=suAt(X,Z)[2]; let mn=9, sw=0;
        for(let i=0;i<40;i++){ player.vel.set(2.4,0,0); __S(1); if(player.swim) sw++; const q=suAt(X-.6,Z); if(q) mn=Math.min(mn,q[2]); } __S(30); const q1=suAt(X-.6,Z); R[SU_T[p].id]=[sw, +(t0-mn).toFixed(2), +(t0-q1[2]).toFixed(2)]; } return R; })()""")
    ok(r['agua'][0]>30 and r['miel'][0]>30, '🏊 se puede nadar en el agua y en la miel')
    ok(r['miel'][1]>.1 and r['agua'][1]>.06, 'nadando vas abriendo la sustancia (miel %s m, agua %s m de hondo)'%(r['miel'][1],r['agua'][1]))
    ok(r['agua'][2]<.03 and r['miel'][2]>r['agua'][2], 'y se cierra sola: en el agua enseguida (%s m), en la miel despacito (%s m al segundo)'%(r['agua'][2],r['miel'][2]))

    # 6. el carrito: la miel lo frena y lo va abriendo
    r=await ev("""(()=>{ __POOL(4,.3,false); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; const o=freeAddStatic({k:'v',a:'carrito',b:0},X,Y,Z-9,0,true); __S(2); player.pos.set(X,Y+.05,Z-9.6); __S(1); pqRide(o,0); yaw=Math.PI; stick.y=-1; __S(1); const D=player.pg && player.pg.drive;
        if(!D) return null; let out=0, inn=9, dug=0; const v0=__VOL(); for(let i=0;i<150;i++){ stick.y=-1; stick.x=0; __S(1); const st=suAt(D.x,D.z); if(D.z<Z-4) out=Math.max(out,D.v); if(st && Math.abs(D.z-Z)<1) inn=Math.min(inn,D.v); }
        stick.y=0; const q=suAt(X,Z); stopPlay(); __S(2); return [+out.toFixed(1), +inn.toFixed(1), +(__VOL()-v0).toFixed(4)]; })()""")
    ok(r is not None and r[1]<r[0]*.8, '🚗🍯 la miel frena al carrito (afuera %s m/s, adentro %s m/s)'%(r[0],r[1]) if r else 'el carrito no arrancó')
    ok(r is not None and abs(r[2])<.01, 'y al irla abriendo no se inventa ni se pierde miel (%s m³)'%(r[2] if r else None))

    # 7. si le llega sustancia a una caja dormida en el piso, despierta y flota
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-10); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; const d=freeAddDyn('caja',X,Y+.5,Z,true); __S(80); const s0=d.sleep, y0=d.root.position.y-Y;
        for(let a=-3;a<=3;a++) for(let c=-3;c<=3;c++) if(Math.abs(a)===3||Math.abs(c)===3) freeAddStatic({k:'b',a:0,b:6},X+a,Y,Z+c,0,true); __S(1); const m=SU.cs; for(let x=-2.4;x<=2.41;x+=m) for(let z=-2.4;z<=2.41;z+=m) suPour(X+x,Z+z,1,0,.9*m*m,.1); __S(150); return [s0, +y0.toFixed(2), +(d.root.position.y-Y).toFixed(2)]; })()""")
    ok(r[0] and r[2]>r[1]+.3, '📦 la caja dormida en el piso, al llegarle el agua, sube a flotar (%s → %s m)'%(r[1],r[2]))

    # 8. lo de lejos se dibuja aunque cerca de ti la sustancia no pare de moverse
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-4); const X=FREE.X, Z=FREE.Z; const near=()=>{ for(let k=0;k<6;k++) suPour(X+(k%3-1)*3.2,Z+(Math.floor(k/3))*3.2,4,0,.05,1.5); };
        for(let i=0;i<120;i++){ near(); __S(1); } for(let i=0;i<200;i++){ near(); if(i===10) for(let k=0;k<5;k++) suPour(X-14+k*3.2,Z+16,4,0,.3,1.2); __S(1); }
        let far=0, drawn=0; for(const C of SU.list){ if(!C.n) continue; const fz=FREE.Z+(C.cj+.5)*3.2; if(fz-Z>12){ far++; if(C.ms.some(M=>M && M.userData.on)) drawn++; } } return [far, drawn]; })()""")
    ok(r[0]>0 and r[1]==r[0], '🔭 la miel de lejos sí se ve aunque cerca no pare de moverse (%s de %s pedacitos dibujados)'%(r[1],r[0]))

    # 9. rendimiento: la torrecita, 6 pelotas y tú nadando en la miel
    r=await ev("""(()=>{ __POOL(4,.9); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; bxPlaceMulti('torre',X+1,Y+.9,Z,0,true).forEach(d=>bxWake(d)); for(let k=0;k<6;k++){ const b=freeAddDyn(['playa','goma','caja','dado','balon','barril'][k],X-1.5+k*.5,Y+1.5,Z-1,true); b.v.set(Math.random()*3,0,Math.random()*3); }
        player.pos.set(X-2,Y+.6,Z+1.5); __S(10); let t0=performance.now(); for(let i=0;i<60;i++){ player.vel.set(1.5,0,0); __S(1); } const a=(performance.now()-t0)/60; __S(300); t0=performance.now(); __S(60); const b2=(performance.now()-t0)/60; return [+a.toFixed(2), +b2.toFixed(2)]; })()""")
    ok(r[0]<12, '⚡ con la torrecita, 6 cosas flotando y tú nadando en la miel cada cuadro tarda %s ms (aquí, sin tarjeta de video)'%r[0])
    ok(r[1]<r[0], 'y cuando todo se calma, menos: %s ms'%r[1])
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
