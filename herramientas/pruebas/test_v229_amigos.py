# v229 en una sala de «Construir con amigos»: las piezas con física (dominós, torre) y los juguetes nuevos se ven igual
# para los dos (dónde están y cómo van girados), la fila que pone el invitado queda exacta (no se mueve medio metro), los
# dominós que tumba Ana se caen también para Beto, y Beto puede usar los juguetes (trompo, cohete, bumerán, lanzadora).
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
BUS=open('/home/claude/mundo-peluche/herramientas/pruebas/test_v215_amigos.py').read().split('BUS = """',1)[1].split('"""',1)[0]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); ctx=await b.new_context(viewport={"width":560,"height":320})
    await ctx.add_init_script("localStorage.setItem('mundoPelucheEnLinea','{\"on\":true,\"tip\":true}'); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'min', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await ctx.route("https://**/*", route)
    async def open_game(name):
      pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); await pg.add_init_script(BUS)
      await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
      await pg.evaluate("""n=>__T.ev(`profile.name=${JSON.stringify(n)}; window.requestAnimationFrame=()=>0; window.__PB=0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateRemotes(.05,t); } scene.updateMatrixWorld(); FNET.bT=0; sendPresence(true); __PB=Math.max(__PB,mp.presBytes||0); };
        window.__UP=d=>new THREE.Vector3(0,1,0).applyQuaternion(d.root.quaternion).y; window.__AIM=()=>{ camera.position.set(player.pos.x,player.pos.y+1.6,player.pos.z-2); camera.lookAt(player.pos.x,player.pos.y+1.7,player.pos.z+5); camera.updateMatrixWorld(); }; 1`)""", name)
      return pg, errs
    A,ea=await open_game('Ana'); B,eb=await open_game('Beto')
    await B.evaluate("__T.ev('MY_PID=`beto0001`; 1')")
    ev=lambda P,s: asyncio.wait_for(P.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    async def sync(n=10):
      for i in range(n):
        await ev(A,"__S(2); 1"); await A.wait_for_timeout(40); await ev(B,"__S(2); 1"); await B.wait_for_timeout(40)
    # 1. Ana crea la sala y pone una fila de dominós girada, una torre y juguetes
    await ev(A,"fnCreate(false); 1"); await A.wait_for_timeout(1500)
    r=await ev(A,"""(()=>{ const X=FREE.X,Y=FREE.Y,Z=FREE.Z; for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d);
      bxPlaceMulti('fila',X-6,Y+.01,Z+4,1).forEach(fnLocalAdd); bxPlaceMulti('torre',X+5,Y+.01,Z+4,0).forEach(fnLocalAdd);
      for(const [id,x,z] of [['trompo',0,-3],['cohete',3,-3],['bumeran',-3,-3]]){ const d=freeAddDyn(id,X+x,Y,Z+z,true); fnLocalAdd(d); }
      const L=freeAddStatic({k:'p',a:'lanzadora',b:0},X+7,Y,Z-6,0,true); fnLocalAdd(L); player.pos.set(X,Y+.05,Z+14); return [FREE.dyn.length, FREE.objs.length]; })()""")
    await sync(4)
    code=await ev(A,"FNET.code"); await ev(B,"(async()=>{ ui('freeBtn').click(); await new Promise(r=>setTimeout(r,600)); return 1; })()")
    await ev(B,"fnJoin(%s); 1"%json.dumps(code)); await B.wait_for_timeout(1500); await ev(B,"player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+14); 1")   # (lejos de las piezas: si llega encima, las empuja)
    for i in range(40):
      await sync(1)
      if await ev(B,"fnSynced() && FREE.dyn.length===%d && FREE.objs.filter(o=>o.gad==='lanzadora').length===1"%r[0]): break
    await ev(B,"player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+14); 1"); await sync(4)
    POS="FREE.dyn.filter(d=>d.bx).map(d=>[d.nid, +(d.root.position.x-FREE.X).toFixed(3), +(d.root.position.y-FREE.Y).toFixed(3), +(d.root.position.z-FREE.Z).toFixed(3), d.root.quaternion.toArray().map(v=>+v.toFixed(3))])"
    pa={q[0]:q for q in await ev(A,POS)}; pb={q[0]:q for q in await ev(B,POS)}
    def worst(pa,pb):
      dp=dq=0; miss=0
      for k,q in pa.items():
        if k not in pb: miss+=1; continue
        w=pb[k]; dp=max(dp,abs(q[1]-w[1]),abs(q[2]-w[2]),abs(q[3]-w[3])); dq=max(dq,1-abs(sum(x*y for x,y in zip(q[4],w[4]))))
      return miss, round(dp,3), round(dq,4)
    mi,dp,dq=worst(pa,pb)
    ok(len(pa)==20 and mi==0 and dp<.06 and dq<.01, 'Beto entra y ve la fila girada y la torre de Ana justo donde están (%s piezas, se separan %s m) %s'%(len(pb),dp,(mi,dp,dq)))
    # 2. Beto pone su propia fila (girada al revés): Ana la ve exacta, no movida al medio metro
    rb=await ev(B,"""(()=>{ const L=bxPlaceMulti('fila',FREE.X-6,FREE.Y+.01,FREE.Z-9,2); L.forEach(fnLocalAdd); return L.map(d=>[d.nid, +(d.root.position.x-FREE.X).toFixed(3), +(d.root.position.y-FREE.Y).toFixed(3), +(d.root.position.z-FREE.Z).toFixed(3), d.root.quaternion.toArray().map(v=>+v.toFixed(3))]); })()""")
    await sync(10)
    pa={q[0]:q for q in await ev(A,POS)}; mi,dp,dq=worst({q[0]:q for q in rb},pa)
    au=await ev(A,"FREE.dyn.filter(d=>d.au==='beto0001').length")
    ok(len(rb)==8 and au==8 and mi==0 and dp<.06 and dq<.01, 'Beto pone una fila de 8 dominós y a Ana le aparece exacta (se separan %s m) %s'%(dp,(au,mi,dp,dq)))
    # 3. Ana empuja el primer dominó de su fila: se caen los 8 para los dos
    await ev(A,"""(()=>{ const L=FREE.dyn.filter(d=>d.id==='domino' && d.au===MY_PID); const w=new THREE.Vector3(3,0,0).applyQuaternion(L[0].root.quaternion); bxWake(L[0]); L[0].bx.w.copy(w); return 1; })()""")
    await sync(45)
    FALL="(()=>{ const L=FREE.dyn.filter(d=>d.id==='domino' && d.au!=='beto0001'); return [L.length, L.filter(d=>__UP(d)<.6).length]; })()"
    ra=await ev(A,FALL); rb=await ev(B,FALL)
    pa={q[0]:q for q in await ev(A,POS)}; pb={q[0]:q for q in await ev(B,POS)}; mi,dp,dq=worst(pa,pb)
    ok(ra==[8,8] and rb==[8,8] and dp<.15, 'Ana tumba su fila y Beto ve caer los 8 y quedar igual (se separan %s m) %s %s'%(dp,ra,rb))
    # 4. Beto hace girar el trompo y bombea y lanza el cohete
    r=await ev(B,"""(()=>{ const d=FREE.dyn.find(q=>q.id==='trompo'); player.pos.set(d.root.position.x,FREE.Y+.05,d.root.position.z-1); player.facing=0; player.vel.set(0,0,0); __S(1); const A=toyActions(); const lab=A&&A[0].label; A&&A[0].run(); return lab; })()""")
    await sync(6)
    ta=await ev(A,"FREE.dyn.find(q=>q.id==='trompo').ts"); tb=await ev(B,"FREE.dyn.find(q=>q.id==='trompo').ts")
    ok(r=='🌀 Hacer girar' and ta==1 and tb==1, 'Beto hace girar el trompo: gira para los dos %s'%[r,ta,tb])
    r=await ev(B,"""(()=>{ const d=FREE.dyn.find(q=>q.id==='cohete'); player.pos.set(d.root.position.x,FREE.Y+.05,d.root.position.z-1); player.facing=0; player.vel.set(0,0,0); __S(1); for(let i=0;i<3;i++){ toyActions()[0].run(); } const L=toyActions(); const labs=L.map(a=>a.label); L[1].run(); return labs; })()""")
    hA=hB=0
    for i in range(14):
      await sync(1); hA=max(hA,await ev(A,"FREE.dyn.find(q=>q.id==='cohete').root.position.y-FREE.Y")); hB=max(hB,await ev(B,"FREE.dyn.find(q=>q.id==='cohete').root.position.y-FREE.Y"))
    ok(r==['💦 Bombear (3/3)','🚀 ¡Lanzar!'] and hA>5 and hB>4, 'Beto bombea y lanza el cohete: sube %.1f m (Beto lo ve a %.1f m) %s'%(hA,hB,r))
    # 5. Beto avienta el bumerán: regresa a Beto y Beto lo tiene en las manos
    await ev(B,"""(()=>{ const d=FREE.dyn.find(q=>q.id==='bumeran'); player.pos.set(d.root.position.x,FREE.Y+.05,d.root.position.z-.9); player.facing=0; player.vel.set(0,0,0); __S(1); freeGrab(d); return 1; })()""")
    await sync(3)
    await ev(B,"(()=>{ __AIM(); freeRelease(.7); return 1; })()")
    far=0; got=False
    for i in range(45):
      await sync(1)
      far=max(far,await ev(A,"(()=>{ const d=FREE.dyn.find(q=>q.id==='bumeran'), r=[...mp.remotes.values()][0]; return Math.hypot(d.root.position.x-r.pos.x,d.root.position.z-r.pos.z); })()"))
      if await ev(B,"!!FREE.hold && FREE.hold.id==='bumeran'") and far>4: got=True; break
    await sync(2); ha=await ev(A,"FREE.dyn.find(q=>q.id==='bumeran').held")
    ok(far>4 and got and ha=='beto0001', 'Beto avienta el bumerán: se va %.1f m y regresa a sus manos (lo tiene: %s, para Ana lo carga Beto: %s)'%(far,got,ha))
    await ev(B,"(()=>{ freeRelease(0); return 1; })()"); await sync(3)
    # 6. Beto usa la lanzadora: sale un disco para los dos
    r=await ev(B,"""(()=>{ const L=FREE.objs.find(o=>o.gad==='lanzadora'); player.pos.set(L.root.position.x+1.4,FREE.Y+.05,L.root.position.z); player.facing=-Math.PI/2; player.vel.set(0,0,0); __S(1); const a=toyActions(); const lab=a&&a[0].label; a&&a[0].run(); return lab; })()""")
    nb=0
    for i in range(12):
      await sync(1); nb=await ev(B,"FREE.dyn.filter(q=>q.id==='disco').length")
      if nb: break
    na=await ev(A,"FREE.dyn.filter(q=>q.id==='disco').length")
    ok(r=='🥏 Lanzar disco' and na==1 and nb==1, 'Beto usa la lanzadora: sale un disco y los dos lo ven %s'%[r,na,nb])
    pb_=await ev(A,"__PB"); ok(pb_<=3500, 'lo más que mandó Ana pesa %s bytes (con piezas cayendo)'%pb_)
    ok(not ea and not eb,'sin errores %s %s'%(ea[:3],eb[:3])); await b.close()
asyncio.run(m())
