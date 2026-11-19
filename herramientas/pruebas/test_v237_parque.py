# v237 (Modo libre): el parque con física de verdad. El columpio es un péndulo (lo empujas o te subes y te impulsas), el molino
# lo mueven el viento, los empujones y los chorros, la piñata cuelga de su cuerda y se mece hacia donde le pegas, la alberca y el
# charco tienen agua de verdad (se derrama, nadas, las cosas flotan) y donde pega la cortina de agua queda espuma blanca.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.033); update(.033,t); } };
  window.__CLR=()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); FREE.hold=null; freeSelect(null); };
  window.__AT=(x,z)=>{ player.pos.set(FREE.X+x,FREE.Y+.05,FREE.Z+z); player.vel.set(0,0,0); player.vy=0; player.facing=0; yaw=Math.PI; FREE.ppPrev=null; __S(2); };
  window.__WAT=(cx,cz,R)=>{ let v=0, out=0; for(const C of SU.list) for(let i=0;i<256;i++){ if(!(C.h[i]>0) || C.t[i]!==1) continue; const [x,z]=suXZ(C,i); if(R(x-cx,z-cz)) v+=C.h[i]*SU.cs*SU.cs; else out++; } return [v,out]; }; 1"""
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

    # 1. el columpio: lo empujas y se mece solito (de un lado a otro) hasta que se detiene
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,-6); const sw=freeAddStatic({k:'v',a:'columpio',b:5},FREE.X,FREE.Y,FREE.Z,0,true); __S(2); window.__SW=sw;
        player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+.9); __S(1); const near=!!pqSwNear(), acts=(pqActions()||[]).filter(a=>a).map(a=>a.label);
        pqSwPush(sw); let mx=0, zc=0, last=0; for(let i=0;i<150;i++){ __S(1); const th=sw.ride.th; mx=Math.max(mx,Math.abs(th)); if(last && th && Math.sign(th)!==Math.sign(last)) zc++; if(th) last=th; }
        const U=sw.root.userData.pq, vis=U && U.mov ? +U.mov.rotation.x.toFixed(3) : null; const same=vis===null?false:Math.abs(vis-sw.ride.th)<1e-3;
        __S(700); return [near, acts, +mx.toFixed(2), zc, same, +Math.abs(sw.ride.th).toFixed(3), +Math.abs(sw.ride.w).toFixed(3)]; })()""")
    ok(r[0] and '🫸 Empujar el columpio' in r[1], '🫸 junto al columpio sale «Empujar el columpio» %s'%r[1])
    ok(r[2]>.3 and r[3]>=3, '💨 al empujarlo se mece de verdad (hasta %s rad, cruza %s veces por en medio)'%(r[2],r[3]))
    ok(r[4], 'y lo que ves es justo ese vaivén (el asiento se mueve igual que la física)')
    ok(r[5]<.02 and r[6]<.02, 'el aire lo va frenando hasta que se queda quieto (%s rad, %s rad/s)'%(r[5],r[6]))

    # 2. subirse e impulsarse con las piernas: cada vez más alto, pero no da la vuelta
    r=await ev("""(()=>{ const sw=__SW; player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+.6); __S(1); pqRide(sw,0); const acts=(pqActions()||[]).filter(a=>a).map(a=>a.label); let a1=0, a2=0, top=0;
        for(let i=0;i<360;i++){ if(i%8===0) pqSwPump(sw); __S(1); if(i>40 && i<100) a1=Math.max(a1,Math.abs(sw.ride.th)); if(i>260) a2=Math.max(a2,Math.abs(sw.ride.th)); top=Math.max(top,Math.abs(sw.ride.th)); }
        const seat=pqSwSeat(sw), py=player.pos.y; stopPlay(); __S(2); return [acts, +a1.toFixed(2), +a2.toFixed(2), +top.toFixed(2), +Math.abs(py-seat[1]).toFixed(2), !player.pg]; })()""")
    ok('🦵 Impulsarse' in r[0] and 'Bajarse' in r[0], '🦵 arriba del columpio salen «Impulsarse» y «Bajarse» %s'%r[0])
    ok(r[2]>r[1]+.15 and r[2]>.6, 'impulsándote vas cada vez más alto (%s → %s rad)'%(r[1],r[2]))
    ok(r[3]<1.3, 'pero entre más alto, menos sirve: no da la vuelta (máximo %s rad)'%r[3])
    ok(r[4]<.9 and r[5], 'vas sentado en el asiento (a %s m) y te bajas bien'%r[4])

    # 3. el columpio no atraviesa a quien está parado enfrente: rebota y lo empuja
    r=await ev("""(()=>{ const sw=__SW; sw.ride.th=.9; sw.ride.w=0; player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+.05); player.vel.set(0,0,0); __S(1); let hit=0, mv=0; const z0=player.pos.z;
        for(let i=0;i<40;i++){ const w0=sw.ride.w; __S(1); if(Math.abs(sw.ride.w)<Math.abs(w0)*.5 && Math.abs(w0)>.5) hit++; } mv=Math.abs(player.pos.z-z0); return [hit, +mv.toFixed(2)]; })()""")
    ok(r[0]>=1 and r[1]>.05, '🧍 si te paras enfrente, el asiento te pega, rebota y te empuja (%s golpes, te movió %s m)'%(r[0],r[1]))

    # 4. el molino: lo empujas caminando contra un aspa, lo mueve el viento y se frena solito
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,-6); const mo=freeAddStatic({k:'p',a:'molino',b:0},FREE.X+10,FREE.Y,FREE.Z,0,true); __S(2); const M=mo.mv; M.w=0; M.a=0; window.__MO=mo;
        player.pos.set(FREE.X+10+1.5*Math.sin(.15),FREE.Y+.05,FREE.Z+1.5*Math.cos(.15)); let w1=0, through=0; for(let i=0;i<20;i++){ player.vel.set(-Math.cos(.15)*3,0,Math.sin(.15)*3); __S(1); w1=Math.min(w1,M.w); }
        const rot=mo.root.userData.rot, vis=!!rot && Math.abs(rot.rotation.y-M.a)<1e-3; __AT(0,-6); __S(260); const st=M.w;
        weatherNow.wind=.8; M.w=0; __S(150); const wd=M.w; weatherNow.wind=0; __S(400); return [+w1.toFixed(2), +st.toFixed(3), +wd.toFixed(2), +M.w.toFixed(3), vis]; })()""")
    ok(r[0]<-.25 and r[4], '🌀 al recargarte en un aspa y caminar, el molino gira (%s rad/s) y se ve girar'%r[0])
    ok(abs(r[1])<.03, 'y se va frenando solito hasta pararse (%s)'%r[1])
    ok(abs(r[2])>.5, '🌬️ con viento fuerte gira solo (%s rad/s)'%r[2])
    ok(abs(r[3])<.03, 'y cuando se calma el viento se para (%s)'%r[3])

    # 5. un chorro de la máquina que le pega a un aspa también lo mueve
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-12); const X=FREE.X+6, Z=FREE.Z-6; const o=freeAddStatic({k:"p",a:"molino",b:0},X,FREE.Y,Z,0,true); __S(1); o.mv.w=0; o.mv.a=0;   /* (un aspa atravesada en el camino del chorro) */
        const f=freeAddStatic({k:'p',a:'fuentes',b:0},X-5,FREE.Y,Z,0,true); fuSet(f,[0,1,2,3].map(i=>({on:i===3?1:0,p:1,q:3,x:1,col:0}))); f.hose={x:X-2.6,z:Z+1.6,a:Math.PI/2,held:null};
        let mx=0, np=0; for(let i=0;i<150;i++){ __S(1); mx=Math.max(mx,Math.abs(o.mv.w)); np=Math.max(np,FU.pts.length); } fuSet(f,[0,1,2,3].map(i=>({on:0,p:1,q:3,x:1,col:0}))); return [+mx.toFixed(2), np]; })()""")
    ok(r[0]>.15 and r[1]>10, '🚿 el chorro de la máquina que le pega a un aspa lo hace girar (%s rad/s)'%r[0])

    # 6. la piñata: cuelga de su cuerda y se mece hacia donde le pegas; luego se queda quieta
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-6); const pi=freeAddStatic({k:'p',a:'pinata',b:0},FREE.X-10,FREE.Y,FREE.Z,0,true); __S(2); const c0=freePinataC(pi);
        freePinataHit(pi,true,2.2,0); let mx=0, dx=0; for(let i=0;i<14;i++){ __S(1); const c=freePinataC(pi); dx=Math.max(dx,c[0]-c0[0]); } for(let i=0;i<60;i++){ __S(1); mx=Math.max(mx,Math.abs(pi.pn.az)+Math.abs(pi.pn.ax)); }
        const pin=pi.root.userData.pin; const vis=pin && Math.abs(pin.rotation.z-pi.pn.az)<1e-3 && Math.abs(pin.rotation.x-pi.pn.ax)<1e-3 && Math.abs(pi.pn.az)>.01;
        freePinataHit(pi,true,0,2.2); let dz=0; const c1=freePinataC(pi); for(let i=0;i<14;i++){ __S(1); dz=Math.max(dz,freePinataC(pi)[2]-c1[2]); }
        __S(500); return [+mx.toFixed(2), +dx.toFixed(2), +dz.toFixed(2), vis, +(Math.abs(pi.pn.ax)+Math.abs(pi.pn.az)).toFixed(3)]; })()""")
    ok(r[0]>.3, '🪅 al pegarle a la piñata se mece en su cuerda (hasta %s rad)'%r[0])
    ok(r[1]>.15 and r[2]>.15, 'hacia donde le pegaste: de lado %s m, de frente %s m'%(r[1],r[2]))
    ok(r[3], 'y lo que ves se mece igualito a la física de la cuerda')
    ok(r[4]<.03, 'luego se va calmando hasta quedarse colgada quieta (%s)'%r[4])

    # 7. la alberca: se llena de agua de verdad, no se sale, nadas y la pelota flota; si le echas más, se derrama
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-8); const al=freeAddStatic({k:'n',a:'alberca',b:0},FREE.X,FREE.Y,FREE.Z,0,true); __S(3); suRecount(); const v=SU.vol;
        const lev=[]; for(const [x,z] of [[0,0],[1.5,1.5],[-1.6,.4]]){ const q=suCell(FREE.X+x,FREE.Z+z,false); lev.push(q?+(suB(q[0],q[1])+q[0].h[q[1]]-FREE.Y).toFixed(2):null); }
        __S(60); suRecount(); const v2=SU.vol; const out=__WAT(FREE.X,FREE.Z,(x,z)=>Math.max(Math.abs(x),Math.abs(z))<2.3)[1];
        player.pos.set(FREE.X,FREE.Y+1.2,FREE.Z); player.vel.set(0,0,0); player.vy=0; let sw=0; for(let i=0;i<30;i++){ __S(1); if(player.swim) sw++; } const py=player.pos.y-FREE.Y;
        const b=freeAddDyn('playa',FREE.X+.6,FREE.Y+.5,FREE.Z+.6); __S(100); const by=b.root.position.y-FREE.Y;
        player.pos.set(FREE.X+4,FREE.Y+.05,FREE.Z); __S(2); for(let i=0;i<30;i++){ suPour(FREE.X,FREE.Z,1,0,.3,.8); __S(2); } __S(60); const spill=__WAT(FREE.X,FREE.Z,(x,z)=>Math.max(Math.abs(x),Math.abs(z))<2.6)[1];
        return [+v.toFixed(1), lev, +(v2-v).toFixed(2), out, sw, +py.toFixed(2), +by.toFixed(2), spill]; })()""")
    ok(r[0]>17 and r[0]<26 and all(l is not None and abs(l-1.35)<.06 for l in r[1]), '🏊 la alberca se llena con agua de verdad (%s m³, nivel %s m)'%(r[0],r[1]))
    ok(abs(r[2])<.05 and r[3]==0, 'y se queda adentro: no se sale ni se pierde (%s m³, %s cuadritos fuera)'%(r[2],r[3]))
    ok(r[4]>=20 and r[5]>-.1 and r[5]<1.2, 'al meterte nadas (%s de 30 cuadros nadando, a %s m)'%(r[4],r[5]))
    ok(r[6]>1.0 and r[6]<1.6, '🏐 la pelota de playa flota en el agua (a %s m; el agua llega a 1.35)'%r[6])
    ok(r[7]>20, '💦 si le echas más agua, se derrama por la orilla (%s cuadritos mojados afuera)'%r[7])

    # 8. guardar y volver a cargar: no se le echa otra vez el agua (ya la tiene)
    r=await ev("""(()=>{ freeSave(); suRecount(); const v0=SU.vol; FREE.loaded=null; freeLoad(); __S(5); suRecount(); return [+v0.toFixed(2), +SU.vol.toFixed(2)]; })()""")
    ok(abs(r[0]-r[1])<.3, '💾 al guardar y cargar el mundo la alberca no se vuelve a llenar (%s → %s m³)'%(r[0],r[1]))

    # 9. el charco: su agua se queda en lo mojado (en forma de charco, no un círculo que se escurre)
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-8); const ch=freeAddStatic({k:'n',a:'charco',b:0},FREE.X+10,FREE.Y,FREE.Z,0,true); __S(3); const a=__WAT(FREE.X+10,FREE.Z,(x,z)=>(x/1.85)**2+(z/1.4)**2<1);
        __S(200); const b=__WAT(FREE.X+10,FREE.Z,(x,z)=>(x/1.85)**2+(z/1.4)**2<1); let wide=0, tall=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.h[i]>0 && C.t[i]===1){ const [x,z]=suXZ(C,i); wide=Math.max(wide,Math.abs(x-FREE.X-10)); tall=Math.max(tall,Math.abs(z-FREE.Z)); }
        return [+a[0].toFixed(3), a[1], +b[0].toFixed(3), b[1], +wide.toFixed(2), +tall.toFixed(2)]; })()""")
    ok(r[0]>.06 and r[0]<.12, '🟦 el charco trae agua de verdad (%s m³)'%r[0])
    ok(r[3]<=2 and abs(r[2]-r[0])<.01, 'y se queda dentro de lo mojado, aunque pase el rato (%s m³, %s cuadritos fuera)'%(r[2],r[3]))
    ok(r[4]>r[5]+.15, 'con su forma alargada de charco (%s m de largo × %s m de ancho, desde el centro)'%(r[4],r[5]))

    # 10. la cortina de agua: deja espuma blanca donde pega; cuando deja de caer se deshace; no se inventa ni se pierde agua
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); const X=FREE.X, Z=FREE.Z; for(let a=0;a<3;a++) for(let c=0;c<3;c++) for(let y=0;y<2;y++) freeAddStatic({k:'b',a:0,b:6},X+a-1,FREE.Y+y,Z+c-1,0,true);
        const VOL=()=>{ suRecount(); return SU.vol+FU.pts.reduce((a,P)=>a+(P.v||0),0)+[...SU.falls.values()].reduce((a,F)=>a+F.acc+(F.q||[]).filter((_,i)=>i%2).reduce((x,y)=>x+y,0),0)+wlVol(); };
        const v0=VOL(); let poured=0, fo=0, near=0; for(let i=0;i<110;i++){ poured+=suPour(X,Z,1,0,.03,.5)||0; __S(1); fo=Math.max(fo,SU.U.uFoN.value); }
        for(const e of SU.fo){ const m=Math.max(Math.abs(e.x-X),Math.abs(e.z-Z)); if(m>1.5 && m<2.3) near++; } const st=SU.U.uFoS.value[0].x;
        let foamCells=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===6 || C.t2[i]===6) foamCells++;
        __S(400); const left=SU.U.uFoN.value, vd=VOL()-v0-poured; return [fo, near, +st.toFixed(2), left, foamCells, +vd.toFixed(4)]; })()""")
    ok(r[0]>=4 and r[1]>=4 and r[2]>.5, '🫧 donde pega la cortina de agua queda espuma blanca (%s tiras, %s junto a la pared, fuerza %s)'%(r[0],r[1],r[2]))
    ok(r[3]==0, 'y cuando deja de caer agua, la espuma se deshace (%s tiras)'%r[3])
    ok(r[4]==0 and abs(r[5])<.01, 'la espuma no gasta ni inventa agua (%s cuadritos de espuma de jabón; diferencia %s m³)'%(r[4],r[5]))

    # 11. rendimiento: columpio, molino y piñata moviéndose a la vez
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(0,-12); const L=[]; for(let k=0;k<4;k++){ L.push(freeAddStatic({k:'v',a:'columpio',b:5},FREE.X-6+k*4,FREE.Y,FREE.Z,0,true)); L.push(freeAddStatic({k:'p',a:'molino',b:0},FREE.X-6+k*4,FREE.Y,FREE.Z+6,0,true)); L.push(freeAddStatic({k:'p',a:'pinata',b:0},FREE.X-6+k*4,FREE.Y,FREE.Z+12,0,true)); }
        __S(3); for(const o of L){ if(o.pq==='columpio') pqSwImp(o,1); else if(o.gad==='molino') o.mv.w=2; else freePinataPush(o,2,0); }
        let t0=performance.now(); for(let i=0;i<60;i++) pqTick(.033); const a=(performance.now()-t0)/60; t0=performance.now(); __S(60); const all=(performance.now()-t0)/60; return [+a.toFixed(3), +all.toFixed(1)]; })()""")
    ok(r[0]<.5, '⚡ 4 columpios meciéndose cuestan %s ms por cuadro (aquí, sin tarjeta de video)'%r[0])
    print('     (todo el juego con 4 columpios, 4 molinos y 4 piñatas moviéndose: %s ms por cuadro aquí)'%r[1])
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
