# v230 (Modo libre): el letrero de arriba se va solo si no haces nada; al construir siempre «Poner · Girar · Listo»; los bloques
# se pegan a los lados (y abajo) de uno que está en el aire; el resorte se estira, rebota y se bambolea (y ya no queda «aplastado»);
# y el papalote vuela enfrente de hacia donde miras: si corres sube, si te paras baja, y «Jalar el hilo» lo sube de golpe.
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
    # 1. el letrero se va solo
    r=await ev("""(()=>{ __CLR(); __AT(-8,-8); const el=ui('freeTxt'); freeSelect({k:'b',a:1,b:0}); __S(3); const a=[el.textContent, el.classList.contains('fade')]; __S(120); const b=el.classList.contains('fade');
      FREE.legacyAim=true; freePlace(); FREE.legacyAim=false; __S(2); const c=el.classList.contains('fade'); __S(120); const dd=el.classList.contains('fade'); freeSelect(null);
      const g=freeAddDyn('balon',FREE.X-8,FREE.Y,FREE.Z-7.2); __S(2); freeGrab(g); __S(3); const e=[el.textContent, el.classList.contains('fade')]; __S(120); const f=el.classList.contains('fade'); freeRelease(0); __S(2); return [a,b,c,dd,e,f,el.textContent, el.classList.contains('fade'), getComputedStyle(el).opacity]; })()""")
    ok(r[0][1]==False and r[1] and r[2]==False and r[3] and 'Cargas' in r[4][0] and r[4][1]==False and r[5] and 'Cargas' not in r[6] and r[7]==False, 'el letrero sale cuando escoges, pones o cargas algo y a los 4 segundos sin hacer nada se desvanece; al soltar ya no dice «Cargas…» %s'%r)
    # 2. al construir: Poner · Girar · Listo (con cualquier cosa)
    r=await ev("""(()=>{ __CLR(); __AT(-8,-8); const out=[]; for(const s of [{k:'b',a:0,b:0},{k:'p',a:'balon',b:0},{k:'p',a:'trompo',b:0},{k:'p',a:'filaD',b:0},{k:'p',a:'porteria',b:0}]){ freeSelect(s); out.push(freeActions().map(a=>a&&a.label).join('·')); }
      const A=freeActions(); setActions(A[0],A[1],A[2]); const vis=[!ui('act1').hidden,!ui('act2').hidden,!ui('act3').hidden, ui('act3').textContent]; FREE.rot=0; A[1].run(); const rot=FREE.rot; A[2].run(); const after=FREE.sel; const B=freeActions(); setActions(B&&B[0],B&&B[1],B&&B[2]);
      return [out, vis, rot, after, ui('act3').hidden]; })()""")
    ok(all(x=='Poner·Girar·Listo' for x in r[0]) and r[1][:3]==[True,True,True] and 'Listo' in r[1][3] and r[2]==1 and r[3] is None and r[4], 'al construir siempre salen «Poner», «Girar» y «Listo» (con bloques, pelotas, juguetes, la fila y la portería); «Listo» deja de poner %s'%r)
    r=await ev("""(()=>{ __CLR(); __AT(-8,-8); freeSelect({k:'p',a:'carrito',b:0}); FREE.rot=1; FREE.legacyAim=true; freePlace(); FREE.legacyAim=false; freeSelect(null); const d=FREE.dyn.find(q=>q.id==='carrito'); return d? +new THREE.Euler().setFromQuaternion(d.root.quaternion,'YXZ').y.toFixed(2):null; })()""")
    ok(r is not None and abs(r-1.57)<.02, 'los juguetes también se giran antes de ponerlos (el carrito queda viendo de lado: %s)'%r)
    # 3. bloques en el aire: junto a uno suspendido se quedan a su altura
    r=await ev("""(()=>{ __CLR(); __AT(-8.5,-8); const X=FREE.X-8.5, Y=FREE.Y, Z=FREE.Z-4.5; freeAddStatic({k:'b',a:0,b:0},X,Y+3,Z,0); freeAddStatic({k:'b',a:0,b:1},X+3,Y,Z,0); freeSelect({k:'b',a:0,b:2}); __S(2);
      const T=(cx,cy,cz,x,y,z)=>{ camMode='first'; camera.position.set(cx,cy,cz); camera.lookAt(x,y,z); camera.updateMatrixWorld(); const a=freeAim(); return [+(a.x-FREE.X).toFixed(2), +(a.y-FREE.Y).toFixed(2), +(a.z-FREE.Z).toFixed(2), a.ok]; };
      const out=[T(X,Y+3.5,Z-4, X,Y+3.5,Z-.5), T(X-4,Y+3.4,Z, X-.5,Y+3.4,Z), T(X,Y+7,Z-2, X,Y+4,Z), T(X+3,Y+.5,Z-4, X+3,Y+.5,Z-.5), T(X,Y+1.2,Z-1.2, X,Y+3,Z)];
      T(X,Y+3.5,Z-4, X,Y+3.5,Z-.5); freePlace(); const n=FREE.objs.filter(q=>q.box && Math.abs(q.box.min.y-(Y+3))<.05).length;
      freeSelect({k:'b',a:1,b:0}); __S(2); out.push(T(X,Y+1.2,Z-1.2, X,Y+3,Z)); camMode='third'; freeSelect(null); return [out, n]; })()""")
    o=r[0]
    ok(o[0][1]==3 and o[0][3] and abs(o[0][2]-(-5.5))<.01, 'apuntas al lado de un bloque en el aire (a 3 m): el nuevo se pega a ese lado, a 3 m %s'%o[0])
    ok(o[1][1]==3 and abs(o[1][0]-(-9.5))<.01, 'también por los otros lados %s'%o[1])
    ok(o[2][1]==4, 'arriba de él se pone encima (a 4 m) %s'%o[2])
    ok(o[3][1]==0, 'junto a un bloque en el piso sigue yendo al piso %s'%o[3])
    ok(r[1]>=2, 'y sí se queda ahí al ponerlo (%s bloques a 3 m)'%r[1])
    ok(o[4][1]==2 and o[4][3] and o[5][1]==2.5, 'apuntando abajo de él se cuelga debajo: un cubo a 2 m y un medio bloque a 2.5 m %s %s'%(o[4],o[5]))
    # 4. el resorte
    r=await ev("""(()=>{ __CLR(); __AT(-8,-8); freeAddStatic({k:'b',a:0,b:2},FREE.X-7.5,FREE.Y,FREE.Z-6.5,0); const d=freeAddDyn('slinky',FREE.X-7.5,FREE.Y+1,FREE.Z-6.5); __S(10); player.pos.set(FREE.X-7.5,FREE.Y+1.05,FREE.Z-7.2); player.facing=0; toyActions()[0].run(); __S(150);
      const I=d.root.userData.rings, flat=[...Array(12).keys()].map(k=>Math.abs(__UPQ(I,k)[0])); const rest=__UPQ(I,11)[1]-__UPQ(I,0)[1];
      __AT(-6,-4); const e=freeAddDyn('slinky',FREE.X-6,FREE.Y,FREE.Z-3); __S(20); freeGrab(e); let mx=0, side=0; for(let i=0;i<40;i++){ __S(1); mx=Math.max(mx,__UPQ(e.root.userData.rings,11)[1]-__UPQ(e.root.userData.rings,0)[1]); }
      for(let i=0;i<10;i++){ player.pos.x+=.15; __S(1); } for(let i=0;i<10;i++){ __S(1); side=Math.max(side,Math.abs(e.sk.sx)+Math.abs(e.sk.sz)); }
      freeRelease(0); e.root.position.y=FREE.Y+2.2; e.v.set(0,0,0); let mn=9, any=false; for(let i=0;i<60;i++){ __S(1); if(e.sk){ mn=Math.min(mn,e.sk.st); } } const end=e.sk?+e.sk.st.toFixed(3):null; const fl2=Math.abs(__UPQ(e.root.userData.rings,5)[0]);
      return [+(d.root.position.y-FREE.Y).toFixed(2), +Math.min(...flat).toFixed(2), +rest.toFixed(3), +mx.toFixed(2), +side.toFixed(3), +mn.toFixed(2), end, +fl2.toFixed(2)]; })()""")
    ok(r[0]<.3 and r[1]>.95 and .25<r[2]<.32, 'resorte: baja del bloque y queda parado con sus aros acostados (ya no «aplastado») %s'%r[:3])
    ok(r[3]>.55, 'cargado cuelga de tu mano y se estira (%s m de largo; quieto mide .29)'%r[3])
    ok(r[4]>.02, 'si caminas con él se bambolea (%s)'%r[4])
    ok(r[5]<-.15 and r[6] is not None and abs(r[6])<.05 and r[7]>.95, 'si lo sueltas desde arriba se aplasta al caer (%s), rebota y vuelve a quedar derechito (%s)'%(r[5],r[6]))
    # 5. el papalote
    r=await ev("""(()=>{ __CLR(); __AT(-6,-8); camMode='third'; const d=freeAddDyn('papalote',FREE.X-6,FREE.Y,FREE.Z-7.2); __S(3); freeGrab(d); __S(30);
      const vis=()=>{ __S(1); const v=d.root.position.clone().project(camera); const dir=new THREE.Vector3(); camera.getWorldDirection(dir); const to=d.root.position.clone().sub(camera.position); return [Math.abs(v.x)<1 && Math.abs(v.y)<1 && to.dot(dir)>0, +(d.root.position.y-player.pos.y).toFixed(2)]; };
      const a=vis(); for(let i=0;i<120;i++){ player.pos.z+=.17; __S(1); } const b=vis(); for(let i=0;i<240;i++) __S(1); const c=vis(); for(let i=0;i<90;i++){ player.pos.z+=.17; player.facing=Math.PI/2; yaw=Math.PI*1.5; __S(1); } const e=vis();
      const h0=d.root.position.y; const A=freeActions(); const lab=A[1]&&A[1].label; A[1].run(); let hm=0; for(let i=0;i<45;i++){ __S(1); hm=Math.max(hm,d.root.position.y-h0); } const str=!!(d.str&&d.str.visible); return [a,b,c,e,lab,+hm.toFixed(2),str]; })()""")
    ok(all(x[0] for x in r[:4]), 'el papalote se ve en la pantalla (enfrente de hacia donde miras), aunque camines o gires %s'%[x[0] for x in r[:4]])
    ok(r[1][1]>r[0][1]+1.5 and r[2][1]<r[1][1]-1.2 and r[2][1]>3, 'si corres sube (%s m) y si te paras baja despacito (%s m) sin caerse'%(r[1][1],r[2][1]))
    ok(r[4]=='🪁 Jalar el hilo' and r[5]>1.2 and r[6], '«Jalar el hilo» lo sube de golpe (%s m) %s'%(r[5],r[4]))
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close(); await b.close()
asyncio.run(m())
