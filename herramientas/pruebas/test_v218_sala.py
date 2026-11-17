# v218 en una sala de «Construir con amigos»: Beto maneja el carrito de Ana (Ana lo ve) y donde se baja ahí se queda
# para los dos; Ana ve a Beto en el tobogán y nadando en la alberca.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
BUS=open('/home/claude/mundo-peluche/herramientas/pruebas/test_v215_amigos.py').read().split('BUS = """',1)[1].split('"""',1)[0]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); ctx=await b.new_context(viewport={"width":560,"height":320})
    await ctx.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'min', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await ctx.route("https://**/*", route)
    async def open_game(name):
      pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); await pg.add_init_script(BUS)
      await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
      await pg.evaluate("n=>__T.ev(`profile.name=${JSON.stringify(n)}; window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateRemotes(.05,t); } scene.updateMatrixWorld(); FNET.bT=0; sendPresence(true); }; window.__do=(lab)=>{ const a=freeActions()||[]; const x=a.find(q=>q&&q.label===lab); if(x) x.run(); return !!x; }; 1`)", name)
      return pg, errs
    A,ea=await open_game('Ana'); B,eb=await open_game('Beto')
    # (los relojes de las dos páginas no empiezan igual: Beto va 37 s adelantado)
    await B.evaluate("__T.ev('MY_PID=`beto0001`; clock.elapsedTime+=37; 1')")
    ev=lambda P,s: asyncio.wait_for(P.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    async def sync(n=10):
      for i in range(n):
        await ev(A,"__S(2); 1"); await A.wait_for_timeout(40); await ev(B,"__S(2); 1"); await B.wait_for_timeout(40)
    # 1. Ana pone agua, plantas y un carrito
    await ev(A,"fnCreate(true); 1"); await A.wait_for_timeout(1500)
    await ev(A,"""(()=>{ const X=FREE.X,Y=FREE.Y,Z=FREE.Z; const S=(sel,x,z,r)=>{ const o=freeAddStatic(sel,X+x,Y,Z+z,r||0,true); fnLocalAdd(o); return o; };
      S({k:'n',a:'alberca',b:0},-12,-12); S({k:'v',a:'tobogan',b:5},8,-14); S({k:'n',a:'arbol',b:0},-20,0); S({k:'v',a:'carrito',b:0},0.5,10.5); player.pos.set(X,Y+.05,Z+25); return 1; })()""")
    code=await ev(A,"FNET.code"); await ev(B,"(async()=>{ ui('freeBtn').click(); await new Promise(r=>setTimeout(r,600)); return 1; })()")
    await ev(B,"fnJoin(%s); 1"%json.dumps(code)); await B.wait_for_timeout(1500)
    for i in range(30):
      await sync(1)
      if await ev(B,"fnSynced() && (FREE.pqv||[]).length===2 && (FREE.nat||[]).length===2"): break
    r=await ev(B,"[(FREE.pqv||[]).length, (FREE.nat||[]).length, (FREE.wat||[]).length]")
    ok(r==[2,2,2], 'Beto entra y ve la alberca, el tobogán, el árbol y el carrito de Ana %s'%r)
    # 2. Beto maneja el carrito: Ana lo ve moverse con Beto adentro; al bajarse se queda donde lo dejó (para los dos)
    await ev(B,"(()=>{ const o=FREE.pqv.find(q=>q.pq==='carrito'); player.pos.set(o.x,FREE.Y+.05,o.z-1.1); player.vel.set(0,0,0); __S(1); return __do('Manejar el carrito'); })()")
    seen=[]
    for i in range(10):
      await ev(B,"(()=>{ yaw=Math.PI; stick.y=-1; __S(2); stick.y=0; return 1; })()"); await B.wait_for_timeout(40); await ev(A,"__S(2); 1"); await A.wait_for_timeout(40)
      seen.append(await ev(A,"(()=>{ const o=FREE.pqv.find(q=>q.pq==='carrito'), rr=[...mp.remotes.values()][0]; return [+(o.root.position.z-o.z).toFixed(1), rr? +o.root.position.distanceTo(rr.pos).toFixed(2):99]; })()"))
    ok(max(s[0] for s in seen)>3 and min(s[1] for s in seen[-4:])<1.2, 'Beto maneja el carrito y Ana lo ve avanzar con Beto adentro %s'%seen[-3:])
    await ev(B,"(()=>{ __do('Bajarse'); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+25); return 1; })()"); await sync(14)
    rA=await ev(A,"(()=>{ const o=FREE.pqv.find(q=>q.pq==='carrito'); return [+(o.z-FREE.Z).toFixed(1), +o.root.position.distanceTo(new THREE.Vector3(o.x,o.y,o.z)).toFixed(2)]; })()")
    rB=await ev(B,"(()=>{ const o=FREE.pqv.find(q=>q.pq==='carrito'); return [+(o.z-FREE.Z).toFixed(1), +o.root.position.distanceTo(new THREE.Vector3(o.x,o.y,o.z)).toFixed(2)]; })()")
    ok(rA[0]>13 and abs(rA[0]-rB[0])<.6 and rA[1]<.2 and rB[1]<.2, 'al bajarse, el carrito se queda donde lo dejó Beto, igual para los dos (Ana %s, Beto %s)'%(rA,rB))
    # 3. Beto se avienta del tobogán: Ana lo ve subir y resbalarse
    await ev(B,"(()=>{ const o=FREE.pqv.find(q=>q.pq==='tobogan'); const [x,z]=pqWorld(o,0,-4.3); player.pos.set(x,FREE.Y+.05,z); player.vel.set(0,0,0); __S(1); return __do('Subir al tobogán'); })()")
    hs=[]
    for i in range(26):
      await ev(B,"__S(3); 1"); await B.wait_for_timeout(40); await ev(A,"__S(1); 1"); await A.wait_for_timeout(40)
      hs.append(await ev(A,"(()=>{ const rr=[...mp.remotes.values()][0]; return rr? +(rr.pos.y-FREE.Y).toFixed(2) : -1; })()"))
    rb=await ev(B,"[player.pg, player.inWater]")
    ok(max(hs)>2.3 and rb[0] is None, 'Beto se resbala del tobogán y Ana lo ve allá arriba (%s m) y luego abajo %s'%(max(hs),hs))
    # 4. Beto nada en la alberca: Ana lo ve nadando
    await ev(B,"(()=>{ const o=FREE.nat.find(q=>q.pq==='alberca'); player.pos.set(o.x,o.y+1.2,o.z); player.vy=0; player.grounded=false; __S(20); return player.swim; })()"); await sync(6)
    r=await ev(A,"(()=>{ const rr=[...mp.remotes.values()][0]; return [rr.swim, +(rr.pos.y-FREE.Y).toFixed(2)]; })()")
    ok(r[0] and r[1]<1, 'Beto nada en la alberca y Ana lo ve nadando %s'%r)
    rp=await ev(A,"mp.presBytes"); ok(rp<=3500, 'lo que manda Ana pesa %s bytes'%rp)
    ok(not ea and not eb,'sin errores %s %s'%(ea[:3],eb[:3])); await b.close()
asyncio.run(m())
