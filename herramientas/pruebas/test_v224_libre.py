# v224 (Modo libre): el fantasmita va donde apunta el puntero; 17 cosas nuevas de física (balón, canica, rueda, dado, espuma,
# hielo, globo, cojín, tabla, gelatina, cañones, ventilador, imán, botón, tubo y piñata); agarrar y lanzar las cosas con física.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); } };
  window.__CLR=()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); FREE.hold=null; FREE.chg=null; freeSelect(null); };
  window.__AT=(x,z,f)=>{ player.pos.set(FREE.X+x,FREE.Y+.05,FREE.Z+z); player.vel.set(0,0,0); player.vy=0; player.facing=f||0; yaw=player.facing+Math.PI; __S(3); }; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True, device_scale_factor=2); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300); await ev(STEP)
    await ev("(()=>{ freeEnter(); __CLR(); __AT(0,0,0); return 1; })()")
    # 1. el fantasmita sigue al puntero
    r=await ev("""(()=>{ freeSelect({k:'b',a:0,b:2}); __S(4); const cross=!ui('cross').hidden && ui('cross').classList.contains('aim-hi'); const out=[];
      for(const pt of [-.55,-.25]){ pitch=pt; __S(4); const a=freeAim(); out.push(+Math.hypot(a.x-player.pos.x,a.z-player.pos.z).toFixed(1)); }
      yaw=player.facing+Math.PI+.9; __S(4); const a=freeAim(), ang=Math.atan2(a.x-player.pos.x,a.z-player.pos.z); yaw=player.facing+Math.PI; pitch=-.3; __S(4);
      return [cross, out, +ang.toFixed(2)]; })()""")
    ok(r[0] and r[1][1]>r[1][0]+.9 and abs(r[2])>.3, 'puntero: se ve en el Modo libre; mirando más abajo la pieza va más cerca (%s m) y al girar la cámara se va de lado (ángulo %s)'%(r[1],r[2]))
    r=await ev("""(()=>{ __S(2); const a=freeAim(); freePlace(); const o=FREE.objs[FREE.objs.length-1]; if(!o) return null;
      const h=freeRay(false); freePlace(); const o2=FREE.objs[FREE.objs.length-1], side=[+(o2.y-FREE.Y).toFixed(2), Math.abs(o2.x-o.x)+Math.abs(o2.z-o.z)];
      let h2=null; for(let pt=-1.3;pt<0;pt+=.05){ pitch=pt; __S(1); const q=freeRay(false); if(q && q.o && q.ny===1){ h2=q; break; } } __S(2); h2=freeRay(false); freePlace(); const o3=FREE.objs[FREE.objs.length-1]; pitch=-.3; __S(4);
      return [FREE.objs.length, +(o.y-FREE.Y).toFixed(2), h && h.o===o && h.ny<.5, side, h2 && h2.ny, +(o3.y-FREE.Y).toFixed(2), h2 && h2.o && o3.x===h2.o.x && o3.z===h2.o.z]; })()""")
    ok(r and r[0]==3 and r[1]==0 and r[2] and r[3]==[0,1] and r[4]==1 and r[5]==1 and r[6], 'puntero: un bloque en el piso donde apuntas; apuntando a su lado el siguiente va junto, y apuntando arriba va encima %s'%r)
    r=await ev("""(()=>{ pitch=.6; __S(4); const a=freeAim(); const n=FREE.objs.length; freePlace(); pitch=-.3; __S(4); return [a.ok, a.why, FREE.objs.length===n, FREE.gBad]; })()""")
    ok(not r[0] and r[1]=='lejos' and r[2], 'puntero: apuntando al cielo la pieza queda en rojo y no se pone %s'%r)
    # 2. las 17 cosas nuevas se arman (con su fotito) y se pueden poner
    r=await ev("""(async()=>{ __CLR(); __AT(0,0,0); const ids=['balon','canica','rueda','dado','espuma','hielo','globo','cojin','tabla','gelatina','canon','canonA','ventilador','iman','boton','tubo','pinata']; const bad=[];
      for(const id of ids){ const m=freeMake({k:'p',a:id,b:0}); if(!m || !m.children.length) bad.push(id); } const tab=[]; FREE.tab='fisica'; try{ freeRenderBox&&freeRenderBox(); }catch(e){}
      const th=ids.map(id=>freeThumbRender('p:'+id+':0')).filter(u=>!u || u==='x').length;
      const vis=FREE_PHYS.filter(P=>!P.hid && !P.toy).length; return [bad, th, vis]; })()""")
    ok(not r[0] and r[1]==0 and r[2]==42, 'las 17 cosas nuevas se arman y tienen su fotito; en «Física» hay %s cosas %s'%(r[2],r))
    # 3. agarrar y lanzar
    r=await ev("""(()=>{ __CLR(); __AT(0,0,0); const d=freeAddDyn('balon',FREE.X,FREE.Y,FREE.Z+1.4); __S(10); const A=freeActions(); const lab=A&&A[0]&&A[0].label; A[0].run(); __S(3);
      const p=d.root.position, up=+(p.y-player.pos.y).toFixed(2), B=freeActions(); const p0=p.clone();
      freeThrowStart(); FREE.chg.t-=1200; freeThrowEnd(); __S(30); const far=+Math.hypot(p.x-p0.x,p.z-p0.z).toFixed(1);
      return [lab, up, B&&B.map(x=>x&&x.label), far, FREE.hold===null, d.held]; })()""")
    ok(r[0].startswith('✋ Agarrar') and r[1]>2 and r[2][0].startswith('🎯 Lanzar') and r[2][1]=='Soltar' and r[3]>6 and r[4] and r[5] is None, 'agarrar: «%s», lo cargas arriba de la cabeza (%s m) y lanzándolo con fuerza llega a %s m'%(r[0],r[1],r[3]))
    r=await ev("""(()=>{ const res={}; for(const [id,pw] of [['balon',.15],['boliche',1],['balon',1]]){ __CLR(); __AT(0,0,0); const d=freeAddDyn(id,FREE.X,FREE.Y,FREE.Z+1.3); __S(6); freeGrab(d); __S(2); const p0=d.root.position.clone(); freeRelease(pw); __S(40); res[id+pw]=+Math.hypot(d.root.position.x-p0.x,d.root.position.z-p0.z).toFixed(1); }
      __CLR(); __AT(0,0,0); const d=freeAddDyn('caja',FREE.X,FREE.Y,FREE.Z+1.3); __S(6); freeGrab(d); __S(2); const y0=d.root.position.y; freeRelease(0); __S(30); res.soltar=+Math.hypot(d.root.position.x-player.pos.x,d.root.position.z-player.pos.z).toFixed(1); res.cae=+(y0-d.root.position.y).toFixed(1); return res; })()""")
    ok(r['balon1']>r['balon0.15']+3 and r['boliche1']<r['balon1']*.75 and r['soltar']<2.5 and r['cae']>1.5, 'lanzar: más fuerte llega más lejos (%s vs %s m), la bola de boliche más corto (%s m) y «Soltar» lo deja enfrente (%s m) %s'%(r['balon1'],r['balon0.15'],r['boliche1'],r['soltar'],r))
    # 4. cañones, botón y tubo
    r=await ev("""(()=>{ __CLR(); __AT(0,0,0); const c=freeAddStatic({k:'p',a:'canon',b:0},FREE.X,FREE.Y,FREE.Z+1.5,0); __S(4); const A=freeActions(); const lab=A&&A[0]&&A[0].label;
      for(let i=0;i<7;i++){ freeFire(c,true); __S(2); } const shots=FREE.dyn.filter(d=>d.tmp).length; __S(20); const far=Math.max(...FREE.dyn.map(d=>d.root.position.z-FREE.Z));
      const a=freeAddStatic({k:'p',a:'canonA',b:0},FREE.X+6,FREE.Y,FREE.Z,1); const n0=FREE.dyn.length; __S(80); const auto=FREE.dyn.filter(d=>d.src===undefined && d.tmp).length;
      return [lab, shots, +far.toFixed(1), (a.shots||[]).length]; })()""")
    ok(r[0]=='💥 Disparar' and r[1]==6 and r[2]>5 and r[3]>=1, 'cañón: «Disparar» de cerca; cada uno tiene máximo 6 pelotas (%s), llegan a %s m; el automático dispara solo (%s en 4 s)'%(r[1],r[2],r[3]))
    r=await ev("""(()=>{ __CLR(); __AT(0,-6,0); const bt=freeAddStatic({k:'p',a:'boton',b:0},FREE.X,FREE.Y,FREE.Z,0), tb=freeAddStatic({k:'p',a:'tubo',b:0},FREE.X+3,FREE.Y,FREE.Z,0), cn=freeAddStatic({k:'p',a:'canon',b:0},FREE.X-3,FREE.Y,FREE.Z,2), lejos=freeAddStatic({k:'p',a:'tubo',b:0},FREE.X+14,FREE.Y,FREE.Z,0);
      __S(4); const n0=FREE.dyn.length; __AT(0,0,0); __S(4); const a=[(tb.shots||[]).length,(cn.shots||[]).length,(lejos.shots||[]).length]; __S(4); const again=(tb.shots||[]).length;
      __AT(0,-6,0); __S(4); const box=freeAddDyn('caja',FREE.X,FREE.Y+1.5,FREE.Z); __S(30); return [a, again, (tb.shots||[]).length, bt.on]; })()""")
    ok(r[0]==[1,1,0] and r[1]==1 and r[2]==2 and r[3], 'botón: al pisarlo el tubo suelta una pelota y el cañón cercano dispara (el de 14 m no); quedarse parado no repite; una caja encima también lo activa %s'%r)
    # 5. ventilador, imán, hielo, globo
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10,0); const f=freeAddStatic({k:'p',a:'ventilador',b:0},FREE.X,FREE.Y,FREE.Z,0), d=freeAddDyn('playa',FREE.X,FREE.Y,FREE.Z+2); __S(30); const fan=+(d.root.position.z-FREE.Z-2).toFixed(1);
      __CLR(); const im=freeAddStatic({k:'p',a:'iman',b:0},FREE.X,FREE.Y,FREE.Z,0), e=freeAddDyn('canica',FREE.X+4,FREE.Y,FREE.Z); __S(40); const iman=+(4-Math.hypot(e.root.position.x-FREE.X,e.root.position.z-FREE.Z)).toFixed(1);
      __CLR(); const h=freeAddDyn('hielo',FREE.X,FREE.Y,FREE.Z), c=freeAddDyn('caja',FREE.X+3,FREE.Y,FREE.Z); __S(10); h.v.set(0,0,5); c.v.set(0,0,5); __S(40); const sl=[+(h.root.position.z-FREE.Z).toFixed(1), +(c.root.position.z-FREE.Z).toFixed(1)];
      __CLR(); const g=freeAddDyn('globo',FREE.X,FREE.Y,FREE.Z); __S(80); const gy=+(g.root.position.y-FREE.Y).toFixed(1);
      return [fan, iman, sl, gy]; })()""")
    ok(r[0]>1.5 and r[1]>1.5 and r[2][0]>r[2][1]*1.8 and 2.6<r[3]<4.2, 'ventilador empuja (%s m), imán jala (%s m), el hielo resbala más que la caja %s y el globo flota a %s m'%(r[0],r[1],r[2],r[3]))
    # 6. gelatina y piñata
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10,0); const g=freeAddStatic({k:'p',a:'gelatina',b:0},FREE.X+.5,FREE.Y,FREE.Z+.5,0); player.pos.set(FREE.X+.5,FREE.Y+5,FREE.Z+.5); player.vy=0; player.grounded=false; let best=-99, up=0;
      for(let i=0;i<40;i++){ __S(1); if(player.vy>best) best=player.vy; } return [+best.toFixed(1), g.solid, +(g.box.max.y-FREE.Y).toFixed(2)]; })()""")
    ok(r[0]>6 and r[1], 'gelatina: es sólida y al caerle encima rebotas (subes a %s)'%r[0])
    r=await ev("""(()=>{ __CLR(); FREE.sticks=[]; FREE.myStick=null; __AT(-10,-10,0); const o=freeAddStatic({k:'p',a:'pinata',b:0},FREE.X,FREE.Y,FREE.Z,0); const [bx,bz]=freeStickBox(o); __AT(bx-FREE.X,bz-FREE.Z-1,0); __S(2);
      const A=freeActions(), lab=A&&A[0]&&A[0].label; A[0].run(); __S(2); const inHand=!!FREE.myStick && FREE.myStick.g.parent!==FREE.og, B=freeActions().map(x=>x&&x.label);
      const [cx,,cz]=freePinataC(o); __AT(cx-FREE.X,cz-FREE.Z-1.3,0); for(let i=0;i<3;i++){ freeSwing(); __S(12); } const candies=FREE.dyn.filter(d=>d.P.id==='dulce'); const hidden=!o.root.userData.pinB.visible;
      __S(30); const c=candies[0], cp=c.root.position; freeStickDrop(); c.v.set(0,0,0); c.sleep=true; cp.y=FREE.Y+c.r; __AT(cp.x-FREE.X,cp.z-FREE.Z-.8,0); c.v.set(0,0,0); c.sleep=true; __S(1); const E=freeActions(), el=E&&E[0]&&E[0].label; E[0].run(); __S(25);
      const left=FREE.dyn.filter(d=>d.P.id==='dulce').length;
      for(let i=0;i<11;i++){ freeStickTake(); freeStickDrop(); } const nS=FREE.sticks.length, inWorld=FREE.sticks.filter(q=>q.g.parent).length;
      return [lab, inHand, B, candies.length, hidden, el, left, FREE.eat, nS, inWorld]; })()""")
    ok(r[0]=='🪅 Tomar un palo' and r[1] and r[2]==['💥 Golpear','Dejar el palo'] and r[3]==6 and r[4], 'piñata: en su cajita tomas un palo, con 3 golpes suelta 6 dulces y se esconde un rato %s'%r[:5])
    ok(r[5]=='🍬 Comer dulce' and r[6]==5 and r[7] is None, 'dulces: «%s» y tu peluche se lo come (quedan %s)'%(r[5],r[6]))
    ok(r[8]==10 and r[9]==10, 'palos: máximo 10 en el mundo; al tomar el 11º desaparece el primero (%s, %s a la vista)'%(r[8],r[9]))
    # 7. guardar: lo que disparan los cañones no se guarda
    r=await ev("""(()=>{ __CLR(); __AT(0,0,0); const c=freeAddStatic({k:'p',a:'canon',b:0},FREE.X,FREE.Y,FREE.Z+1.5,0); freeAddDyn('balon',FREE.X+3,FREE.Y,FREE.Z); freeFire(c,true); freeFire(c,true); __S(4); freeSave();
      const k=Object.keys(localStorage).find(k=>/libre|free/i.test(k) && localStorage.getItem(k).includes('canon')); const J=k?JSON.parse(localStorage.getItem(k)):null; return [!!J, J?(J.d||[]).length:-1, J?(J.s||[]).filter(e=>e[1]==='canon').length:-1]; })()""")
    ok(r[0] and r[1]==1 and r[2]==1, 'guardar: se guarda el cañón y el balón, no las pelotas disparadas %s'%r)
    # 8. en una sala: otro jugador lo carga (el anfitrión lo pone arriba de su cabeza) y lo lanza
    r=await ev("""(()=>{ __CLR(); __AT(0,0,0); const d=freeAddDyn('balon',FREE.X+4,FREE.Y,FREE.Z); fnLocalAdd(d); __S(4); const fake={fpid:'P2', pos:new THREE.Vector3(FREE.X+4,FREE.Y,FREE.Z+.5), facing:0}; mp.remotes.set('zz',fake);
      fnApplyOp('P2',[1,'g',d.nid,1]); __S(3); const up=+(d.root.position.y-fake.pos.y).toFixed(1); const mine=freeGrabTarget()===d;
      fnApplyOp('P2',[2,'g',d.nid,0]); fnApplyOp('P2',[3,'k',d.nid,0,4,8]); __S(10); const moved=+(d.root.position.z-FREE.Z).toFixed(1); mp.remotes.delete('zz'); return [up, mine, moved, d.held]; })()""")
    ok(r[0]>2 and not r[1] and r[2]>2 and r[3] is None, 'sala: el anfitrión pone el balón arriba de la cabeza de quien lo carga (%s m), nadie más lo puede agarrar, y al lanzarlo sale volando (%s m)'%(r[0],r[2]))
    # 9. el arco: la flecha se clava en una cosa con física, la empuja un poco (lo ligero más) y luego la puedes jalar
    r=await ev("""(()=>{ __CLR(); __AT(0,0,0); const i=hotbar.indexOf('bow'); if(i<0) return null; selectedSlot=i; holding=true; applyHeld(); const res={};
      for(const id of ['playa','boliche']){ __CLR(); const d=freeAddDyn(id,FREE.X,FREE.Y,FREE.Z+8); __S(6); const c=d.root.position.clone(); const hit=freeArrowHit(c.clone().add(new THREE.Vector3(0,0,-d.r)));
        hook.mode=1; hook.vel.set(0,0,30); hook.pos.set(c.x,c.y,c.z-d.r-.05); stickTo(hit,hook.pos.clone()); const push=+Math.hypot(d.v.x,d.v.z).toFixed(1); __S(20);
        const z1=d.root.position.z; bowPull(); let n=0; for(;n<120 && hook.mode;n++){ updateMyBow(.05); __S(1); } res[id]=[hit&&hit.kind, push, +(z1-FREE.Z).toFixed(1), +(d.root.position.z-FREE.Z).toFixed(1), n]; }
      holding=false; applyHeld(); return res; })()""")
    ok(r and r['playa'][0]=='fdyn' and r['playa'][1]>r['boliche'][1]*2 and r['playa'][3]<2.2 and r['boliche'][3]<2.2 and r['boliche'][4]>r['playa'][4], 'arco: la flecha se clava, el golpe empuja más a la pelota de playa (%s) que a la bola de boliche (%s), y al jalar las dos llegan a ti (la de boliche más despacio: %s vs %s cuadros) %s'%(r and r['playa'][1], r and r['boliche'][1], r and r['boliche'][4], r and r['playa'][4], r))
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close(); await b.close()
asyncio.run(m())
