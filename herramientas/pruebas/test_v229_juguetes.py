# v229 (Modo libre): dominó, bolos y torre de bloques con físicas de cajas de verdad (en «Física»); portería y canasta con
# choques (postes, red, tablero, poste y aro); y 10 juguetes nuevos en Parque → Juguetes: trompo, pelota saltarina, resorte que
# baja escalones, carrito de cuerda, avioncito de papel, papalote, bumerán, globo con helio, cohete de agua y lanzadora de discos.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.033); update(.033,t); } };
  window.__CLR=()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); FREE.hold=null; freeSelect(null); freeBubClear(); };
  window.__AT=(x,z)=>{ player.pos.set(FREE.X+x,FREE.Y+.05,FREE.Z+z); player.vel.set(0,0,0); player.vy=0; player.facing=0; yaw=Math.PI; FREE.ppPrev=null; __S(2); };
  window.__UP=d=>new THREE.Vector3(0,1,0).applyQuaternion(d.root.quaternion).y;
  window.__AIM=()=>{ camera.position.set(player.pos.x,player.pos.y+1.6,player.pos.z-2); camera.lookAt(player.pos.x,player.pos.y+1.7,player.pos.z+5); camera.updateMatrixWorld(); }; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type=='warning' and ('cajas' in m.text or 'juguetes' in m.text) else None)
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev("(()=>{ freeEnter(); return 1; })()"); await ev(STEP)
    # 1. dónde están en el menú
    r=await ev("""(()=>{ const fis=FREE_PHYS.filter(P=>!P.hid && !P.toy).map(P=>P.n), jug=FREE_PHYS.filter(P=>P.toy && !P.hid).map(P=>P.n); FREE.tab='parque'; FREE.sub='juguetes'; let menu=''; try{ freeInvOpen && freeInvOpen(); }catch(e){}
      const bad=FREE_PHYS.filter(P=>P.toy||P.box||P.multi).filter(P=>{ const m=freeMake({k:'p',a:P.id,b:0}); return !m || !m.children.length; }).map(P=>P.id);
      return [fis.includes('Dominó') && fis.includes('Fila de 8 dominós') && fis.includes('Bolos (10)') && fis.includes('Torre de bloques'), jug, bad]; })()""")
    ok(r[0] and len(r[1])==10 and not r[2], 'menú: dominó, fila, bolos y torre están en «Física»; en Parque → Juguetes hay 10 juguetes %s'%r[1])
    # 2. la fila de dominós cae en cadena
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const L=bxPlaceMulti('fila',FREE.X,FREE.Y+.01,FREE.Z,0); __S(20); const up0=L.every(d=>__UP(d)>.99); const d0=L[0]; bxWake(d0); d0.bx.w.set(3,0,0); const C=[]; for(let k=0;k<6;k++){ __S(15); C.push(L.filter(d=>__UP(d)<.6).length); } return [up0, C, L.map(d=>+__UP(d).toFixed(2))]; })()""")
    ok(r[0] and r[1][-1]==8 and r[1][2]<8, 'la fila de dominós se para derechita y al empujar el primero se caen los 8 en cadena %s'%r[1])
    # 3. bolos y bola de boliche
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const L=bxPlaceMulti('bolos',FREE.X,FREE.Y+.01,FREE.Z,0); __S(20); const b=freeAddDyn('boliche',FREE.X,FREE.Y,FREE.Z-6); b.v.set(0,0,12); __S(120); return [L.length, L.filter(d=>__UP(d)<.6).length]; })()""")
    ok(r[0]==10 and r[1]>=5, 'bolos: la bola de boliche tumba %s de %s bolos'%(r[1],r[0]))
    # 4. la torre se queda parada y se derrumba con un golpe
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const L=bxPlaceMulti('torre',FREE.X,FREE.Y+.01,FREE.Z,0); const y0=L.map(d=>d.root.position.y); L.forEach(bxWake); __S(90); const drift=Math.max(...L.map((d,i)=>Math.abs(d.root.position.y-y0[i])));
      const ball=freeAddDyn('boliche',FREE.X-4,FREE.Y,FREE.Z); ball.v.set(14,0,0); __S(90); return [L.length, +drift.toFixed(3), L.filter(d=>d.root.position.y<FREE.Y+1.2).length]; })()""")
    ok(r[0]==12 and r[1]<.05 and r[2]>=8, 'torre de 12 bloques: se queda parada (se mueve %s m) y con la bola se derrumba (%s abajo)'%(r[1],r[2]))
    # 5. empujarlas con tu peluche, agarrarlas y aventarlas
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const d=freeAddDyn('bloque2',FREE.X,FREE.Y,FREE.Z+1); d.sleep=true; const z0=d.root.position.z; player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-.2); FREE.ppPrev=player.pos.clone(); for(let i=0;i<60;i++){ player.pos.z+=.06; __S(1); } const moved=d.root.position.z-z0;
      const e=freeAddDyn('domino',FREE.X+3,FREE.Y,FREE.Z); e.sleep=true; player.pos.set(FREE.X+3,FREE.Y+.05,FREE.Z-1); FREE.ppPrev=player.pos.clone(); for(let i=0;i<20;i++){ player.pos.z+=.06; __S(1); } __S(40); const tip=__UP(e);
      __AT(-6,0); const f=freeAddDyn('domino',FREE.X-6,FREE.Y,FREE.Z+1); __S(3); freeGrab(f); __S(3); const held=f.root.position.y>player.pos.y+PLAYER_H; __AIM(); freeRelease(.6); __S(60); return [+moved.toFixed(2), +tip.toFixed(2), held, +(f.root.position.z-FREE.Z).toFixed(1), +(f.root.position.y-FREE.Y).toFixed(2)]; })()""")
    ok(r[0]>1.5 and r[1]<.6 and r[2] and r[3]>2 and r[4]<.6, 'tu peluche empuja un bloque por el mapa (%s m), tumba un dominó al chocarlo y lo puede cargar y aventar %s'%(r[0],r[1:]))
    # 6. se guarda cómo quedaron (y los juguetes viejos del parque se vuelven piezas con física)
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const d=freeAddDyn('domino',FREE.X,FREE.Y,FREE.Z+2); bxWake(d); d.bx.w.set(3,0,0); __S(60); const up=__UP(d); freeSave(); FREE.loaded=null; freeLoad(); const e=FREE.dyn.find(q=>q.id==='domino');
      const k='mundoPelucheLibre'; localStorage.setItem(k,JSON.stringify({v:1, s:[['t','domino',11,0,0,3,1],['t','torre',0,4,0,4,0],['t','bolo',0,-3,0,3,0]], d:[]})); FREE.loaded=null; freeLoad();
      const kinds={}; FREE.dyn.forEach(q=>kinds[q.id.replace(/\\d$/,'')]=(kinds[q.id.replace(/\\d$/,'')]||0)+1); return [+up.toFixed(2), e?+__UP(e).toFixed(2):null, FREE.objs.filter(o=>o.sel.k==='t').length, kinds]; })()""")
    ok(r[0]<.5 and r[1] is not None and r[1]<.5 and r[2]==0 and r[3].get('domino')==1 and r[3].get('bloque')==12 and r[3].get('bolo')==1, 'al guardar, el dominó caído sigue caído; los dominós, bolos y torres de antes se vuelven piezas con física %s'%r)
    # 7. portería
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const g=freeAddStatic({k:'p',a:'porteria',b:0},FREE.X,FREE.Y,FREE.Z,0); const [px,pz]=freeW(g,1.5,0); const a=freeAddDyn('balon',px,FREE.Y,pz+4); a.root.position.y=FREE.Y+.8; a.v.set(0,0,-10); __S(40); const reb=a.v.z>0 && a.root.position.z>pz+.5;
      const c=freeAddDyn('balon',FREE.X,FREE.Y,FREE.Z+4); c.root.position.y=FREE.Y+.7; c.v.set(0,2,-16); __S(60); const inside=c.root.position.z<FREE.Z && c.root.position.z>FREE.Z-1.15, gol=(g.gT||0)>0;
      const [qx,qz]=freeW(g,-1.5,0); player.pos.set(qx,FREE.Y+.05,qz+1); for(let i=0;i<30;i++){ player.pos.z-=.08; freeCollide(player.pos); } const blocked=player.pos.z>qz+.3;
      player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-2.2); for(let i=0;i<30;i++){ player.pos.z+=.08; freeCollide(player.pos); } const net=player.pos.z<FREE.Z-1.4; return [reb,inside,gol,blocked,net]; })()""")
    ok(all(r), 'portería: el balón rebota en el poste; el que entra se queda en la red y es gol; tu peluche no atraviesa el poste ni la red %s'%r)
    # 8. canasta
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const c=freeAddStatic({k:'p',a:'canasta',b:0},FREE.X,FREE.Y,FREE.Z,0); const [hx,hz]=freeW(c,0,.36); const a=freeAddDyn('basket',hx,FREE.Y,hz); a.root.position.set(hx+.03,FREE.Y+4.2,hz); a.v.set(0,0,0); __S(40); const can=(c.cT||0)>0;
      const [ax,az]=freeW(c,.38,.36); const b=freeAddDyn('basket',ax,FREE.Y,az); b.root.position.set(ax,FREE.Y+4,az); b.v.set(0,0,0); __S(12); const rim=b.root.position.x-ax>.05 || b.root.position.x-ax<-.05;
      const t=freeAddDyn('basket',FREE.X,FREE.Y,FREE.Z+3); t.root.position.set(FREE.X,FREE.Y+3.35,FREE.Z+3); t.v.set(0,0,-10); __S(12); const board=t.v.z>0;
      player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+1); for(let i=0;i<30;i++){ player.pos.z-=.08; freeCollide(player.pos); } const pole=player.pos.z>FREE.Z-.1; return [can,rim,board,pole]; })()""")
    ok(all(r), 'canasta: el balón cabe por el aro y es canasta; el aro lo rebota si pega en la orilla; rebota en el tablero; tu peluche no atraviesa el poste %s'%r)
    # 9. juguetes (1)
    r=await ev("""(()=>{ const out=[]; __CLR(); __AT(-10,-10); let d=freeAddDyn('trompo',FREE.X,FREE.Y,FREE.Z); __S(5); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-1); player.facing=0; const A=toyActions(); A[0].run(); __S(30); const s1=d.ts; __S(350); out.push([A[0].label, s1, d.ts, +d.spin.rotation.x.toFixed(2)]);
      __CLR(); __AT(-10,-10); d=freeAddDyn('saltarina',FREE.X,FREE.Y,FREE.Z); d.root.position.y=FREE.Y+3; let n=0; for(let i=0;i<300;i++){ const vy=d.v.y; __S(1); if(vy<-1 && d.v.y>1) n++; } out.push(n);
      __CLR(); __AT(-10,-10); d=freeAddDyn('carrito',FREE.X+.5,FREE.Y,FREE.Z+.5); __S(5); player.pos.set(FREE.X+.5,FREE.Y+.05,FREE.Z-.5); player.facing=0; toyActions()[0].run(); freeAddStatic({k:'b',a:0,b:1},FREE.X+.5,FREE.Y,FREE.Z+4.5,0); let zm=0; for(let i=0;i<120;i++){ __S(1); zm=Math.max(zm,d.root.position.z-FREE.Z); } out.push([+zm.toFixed(1), +(d.root.position.z-FREE.Z).toFixed(1)]);
      __CLR(); __AT(-10,-10); freeAddStatic({k:'b',a:0,b:2},FREE.X+.5,FREE.Y,FREE.Z+.5,0); d=freeAddDyn('slinky',FREE.X+.5,FREE.Y+1,FREE.Z+.5); __S(10); player.pos.set(FREE.X+.5,FREE.Y+1.05,FREE.Z-.2); player.facing=0; toyActions()[0].run(); __S(150); out.push([+(d.root.position.y-FREE.Y).toFixed(2), +(d.root.position.z-FREE.Z).toFixed(1), d.ts]);
      __CLR(); __AT(-10,-10); d=freeAddDyn('avion',FREE.X,FREE.Y,FREE.Z); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-1); player.facing=0; __AIM(); freeGrab(d); __S(2); freeRelease(.8); let air=0; for(let i=0;i<200;i++){ __S(1); if(d.ts===1) air++; } out.push([+Math.hypot(d.root.position.x-player.pos.x,d.root.position.z-player.pos.z).toFixed(1), +(air*.033).toFixed(1)]);
      return out; })()""")
    ok(r[0][0]=='🌀 Hacer girar' and r[0][1]==1 and r[0][2]==2 and r[0][3]>1, 'trompo: «Hacer girar», gira y al final se cae de lado %s'%r[0])
    ok(r[1]>=6, 'pelota saltarina: rebota %s veces desde 3 m'%r[1])
    ok(3<r[2][0]<4.2 and r[2][1]<2.5, 'carrito de cuerda: avanza solo y al chocar con un bloque da la vuelta %s'%r[2])
    ok(r[3][0]<.3 and r[3][1]>1.5 and r[3][2]==0, 'resorte: baja del bloque al piso dando maromas y se para %s'%r[3])
    ok(8<r[4][0]<28 and r[4][1]>1.2, 'avioncito de papel: planea %s m (%s s en el aire)'%(r[4][0],r[4][1]))
    # 10. juguetes (2)
    r=await ev("""(()=>{ const out=[]; __CLR(); __AT(-10,-10); let d=freeAddDyn('papalote',FREE.X,FREE.Y,FREE.Z); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-1); freeGrab(d); for(let i=0;i<90;i++){ player.pos.z+=.05; __S(1); } const hy=d.root.position.y-player.pos.y, str=!!(d.str && d.str.visible); freeRelease(0); let vm=0; for(let i=0;i<60;i++){ __S(1); vm=Math.min(vm,d.v.y); } out.push([+hy.toFixed(1),str,+vm.toFixed(2)]);
      __CLR(); __AT(-10,-10); d=freeAddDyn('bumeran',FREE.X,FREE.Y,FREE.Z); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z); player.facing=0; __AIM(); freeGrab(d); __S(2); freeRelease(.7); let far=0; for(let i=0;i<110;i++){ __S(1); far=Math.max(far,Math.hypot(d.root.position.x-FREE.X,d.root.position.z-FREE.Z)); } out.push([+far.toFixed(1), FREE.hold===d]);
      __CLR(); __AT(-10,-10); d=freeAddDyn('helio',FREE.X,FREE.Y,FREE.Z); __S(200); const h1=d.root.position.y-FREE.Y; d.root.position.set(FREE.X,FREE.Y+1,FREE.Z+1); const bb=freeAddDyn('playa',FREE.X+.5,FREE.Y,FREE.Z+.5), bl=freeAddDyn('boliche',FREE.X-.6,FREE.Y,FREE.Z+.5); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z); freeGrab(d); __S(2); const H=freeActions(); const lab=H&&H[1]&&H[1].label; H[1].run(); __S(120); out.push([+h1.toFixed(1), lab, +(d.tie===bb||d.tie===bl), +(d.tie.root.position.y-FREE.Y).toFixed(1)]);
      __CLR(); __AT(-10,-10); d=freeAddDyn('cohete',FREE.X,FREE.Y,FREE.Z); __S(5); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-1); for(let i=0;i<3;i++) toyActions()[0].run(); const L=toyActions(); const labs=[L[0].label,L[1].label]; L[1].run(); let top=0, ch=false, vmn=0; for(let i=0;i<400;i++){ __S(1); top=Math.max(top,d.root.position.y-FREE.Y); if(d.ts===2){ ch=true; vmn=Math.min(vmn,d.v.y); } } out.push([labs, +top.toFixed(1), ch, +vmn.toFixed(2), d.ts]);
      __CLR(); __AT(-10,-10); const LZ=freeAddStatic({k:'p',a:'lanzadora',b:0},FREE.X,FREE.Y,FREE.Z,0); player.pos.set(FREE.X+1.4,FREE.Y+.05,FREE.Z); const lb=toyActions(); const lab2=lb&&lb[0].label; lb[0].run(); const disc=FREE.dyn.find(q=>q.P.toy==='disco'); let dist=0; for(let i=0;i<150;i++){ __S(1); dist=Math.max(dist,disc.root.position.z-FREE.Z); }
      __CLR(); __AT(-10,-10); const L3=freeAddStatic({k:'p',a:'lanzadora',b:0},FREE.X,FREE.Y,FREE.Z,0); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+4); toyDisc(L3); let caught=false; for(let i=0;i<60;i++){ __S(1); if(FREE.hold && FREE.hold.P.toy==='disco'){ caught=true; break; } } out.push([lab2, +dist.toFixed(1), caught]);
      return out; })()""")
    ok(r[0][0]>4 and r[0][1] and -1.5<r[0][2]<0, 'papalote: vuela %s m arriba de ti con su hilo y al soltarlo baja despacito (%s m/s)'%(r[0][0],r[0][2]))
    ok(r[1][0]>5 and r[1][1], 'bumerán: llega a %s m y regresa a tus manos'%r[1][0])
    ok(r[2][0]>5 and 'Amarrar' in (r[2][1] or '') and r[2][2]==1, 'globo con helio: sube (%s m); con «%s» se amarra y lo ligero flota (%s m)'%(r[2][0],r[2][1],r[2][3]))
    ok(r[3][0]==['💦 Bombear (3/3)','🚀 ¡Lanzar!'] and r[3][1]>6 and r[3][2] and -1.4<r[3][3]<-.8 and r[3][4]==0, 'cohete de agua: se bombea 3 veces, sube %s m, abre su paracaídas y baja despacito %s'%(r[3][1],r[3][2:]))
    ok(r[4][0]=='🥏 Lanzar disco' and 10<r[4][1]<40 and r[4][2], 'lanzadora: avienta un disco que planea %s m y si te llega lo atrapas'%r[4][1])
    # 11. girar antes de poner y cuánto tarda la física con muchas piezas
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); freeSelect({k:'p',a:'filaD',b:0}); const lab=freeActions()[1].label; FREE.rot=1; FREE.legacyAim=true; freePlace(); FREE.legacyAim=false; const L=FREE.dyn.filter(q=>q.id==='domino'); const xs=L.map(q=>+(q.root.position.x-FREE.X).toFixed(2)), yaw=L.length && Math.abs(Math.abs(new THREE.Euler().setFromQuaternion(L[0].root.quaternion,'YXZ').y)-Math.PI/2)<.01; freeSelect(null); FREE.rot=0;
      __CLR(); for(let k=0;k<4;k++) bxPlaceMulti('fila',FREE.X-6+k*3,FREE.Y+.01,FREE.Z,0); bxPlaceMulti('torre',FREE.X+7,FREE.Y+.01,FREE.Z,0); FREE.dyn.forEach(d=>{ if(d.bx){ bxWake(d); } }); FREE.dyn.filter(d=>d.id==='domino').forEach((d,i)=>{ if(i%8===0) d.bx.w.set(3,0,0); });
      const t0=performance.now(); for(let i=0;i<30;i++) bxPhys(.033,FREE.dyn); const ms=(performance.now()-t0)/30; return [lab, L.length, yaw, Math.max(...xs)-Math.min(...xs), +ms.toFixed(2), FREE.dyn.length]; })()""")
    ok(r[0]=='Girar' and r[1]==8 and r[2] and r[3]>3.5, 'la fila de dominós se puede girar antes de ponerla %s'%r[:4])
    ok(r[4]<25, 'con %s piezas cayendo, la física tarda %s ms por cuadro (aquí, sin tarjeta de video)'%(r[5],r[4]))
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close(); await b.close()
asyncio.run(m())
