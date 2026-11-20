# v237 en una sala: el columpio, el molino y la piñata se mueven igual para todos (los mueve el dueño de la sala; los demás le
# mandan sus empujones, impulsos y golpes), y la capa de sustancia en las paredes se ve igual en todos los mundos.
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
        window.__G=(k)=>FREE.objs.find(o=>o.pq===k || o.gad===k); 1`)""", name)
      return pg, errs
    A,ea=await open_game('Ana'); B,eb=await open_game('Beto')
    await B.evaluate("__T.ev('MY_PID=`beto0001`; 1')")
    ev=lambda P,s: asyncio.wait_for(P.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    async def sync(n=10):
      for i in range(n):
        await ev(A,"__S(2); 1"); await A.wait_for_timeout(40); await ev(B,"__S(2); 1"); await B.wait_for_timeout(40)
    await ev(A,"fnCreate(false); 1"); await A.wait_for_timeout(1500)
    await ev(A,"""(()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); suClear(); FU.pts.length=0; weatherNow.wind=0;
      for(const [s,x,z] of [[{k:'v',a:'columpio',b:5},-6,4],[{k:'p',a:'molino',b:0},0,10],[{k:'p',a:'pinata',b:0},6,4]]){ const o=freeAddStatic(s,FREE.X+x,FREE.Y,FREE.Z+z,0,true); fnLocalAdd(o); }
      player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-6); return 1; })()""")
    await sync(4)
    code=await ev(A,"FNET.code"); await ev(B,"(async()=>{ ui('freeBtn').click(); await new Promise(r=>setTimeout(r,600)); return 1; })()")
    await ev(B,"fnJoin(%s); 1"%json.dumps(code)); await B.wait_for_timeout(1500); await ev(B,"weatherNow.wind=0; player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-4); 1")
    for i in range(40):
      await sync(1)
      if await ev(B,"fnSynced() && !!__G('columpio') && !!__G('molino') && !!__G('pinata')"): break
    r=await ev(B,"[!!__G('columpio'), !!__G('molino'), !!__G('pinata')]")
    ok(all(r), 'Beto ve el columpio, el molino y la piñata de Ana %s'%r)

    # 1. Ana empuja el columpio: Beto lo ve mecerse igual
    await ev(A,"(()=>{ const o=__G('columpio'); player.pos.set(o.x,FREE.Y+.05,o.z+.9); __S(1); pqSwPush(o); return 1; })()")
    th=[]
    for i in range(10):
      await sync(1); th.append(await ev(B,"[+__G('columpio').ride.th.toFixed(2), +__G('columpio').root.userData.pq.mov.rotation.x.toFixed(2)]"))
    mb=max(abs(t[0]) for t in th); vis=all(abs(t[0]-t[1])<.02 for t in th)
    ok(mb>.2 and vis, '🫸 Ana empuja el columpio y Beto lo ve mecerse (hasta %s rad)'%mb)
    ra=await ev(A,"+__G('columpio').ride.th.toFixed(2)"); rb=await ev(B,"+__G('columpio').ride.th.toFixed(2)")
    ok(abs(ra-rb)<.3, 'y van al mismo ritmo (Ana %s, Beto %s rad)'%(ra,rb))

    # 2. Beto se sube y se impulsa: a Ana le llegan sus impulsos
    await ev(A,"(()=>{ const o=__G('columpio'); o.ride.th=0; o.ride.w=0; pqDirty(o); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-6); return 1; })()"); await sync(6)
    await ev(B,"(()=>{ const o=__G('columpio'); player.pos.set(o.x,FREE.Y+.05,o.z+.6); __S(1); pqRide(o,0); return 1; })()")
    amp=0
    for i in range(30):
      await ev(B,"(()=>{ const o=__G('columpio'); o.ride.pt=0; o.ride.ot=0; pqSwPump(o); return 1; })()"); await sync(1)
      amp=max(amp, abs(await ev(A,"__G('columpio').ride.th")))
    sitting=await ev(A,"(()=>{ for(const r of mp.remotes.values()) if(r.pl && PG_KINDS[r.pl[0]]==='fmv') return true; return false; })()")
    ok(amp>.3, '🦵 Beto se sube y se impulsa: el columpio de Ana sube (hasta %.2f rad)'%amp)
    ok(sitting, 'y Ana ve a Beto sentado en el columpio')
    await ev(B,"stopPlay(); 1"); await sync(2)

    # 3. Beto le pega a la piñata: se mece para los dos, hacia donde le pegó
    await ev(B,"(()=>{ const o=__G('pinata'); window.__C0=freePinataC(o); freePinataHit(o,true,0,2.2); return 1; })()")
    da=0; db=0
    for i in range(8):
      await sync(1)
      da=max(da, await ev(A,"(()=>{ const o=__G('pinata'), c=freePinataC(o); return c[2]-o.z; })()")); db=max(db, await ev(B,"(()=>{ const o=__G('pinata'), c=freePinataC(o); return c[2]-o.z; })()"))
    ok(da>.15 and db>.15, '🪅 Beto le pega a la piñata y se mece para los dos hacia donde le pegó (Ana %.2f m, Beto %.2f m)'%(da,db))

    # 4. Beto empuja un aspa del molino caminando: a Ana le llega el empujón; luego los dos lo ven girar igual
    await ev(A,"(()=>{ const o=__G('molino'); o.mv.w=0; o.mv.a=0; pqDirty(o); return 1; })()"); await sync(4)
    await ev(B,"(()=>{ const o=__G('molino'); o.mv.a=0; o.mv.w=0; return 1; })()")
    for i in range(10):
      await ev(B,"(()=>{ const o=__G('molino'), a=o.mv.a+.15; player.pos.set(o.x+1.5*Math.sin(a),FREE.Y+.05,o.z+1.5*Math.cos(a)); player.vel.set(-Math.cos(a)*3,0,Math.sin(a)*3); __S(1); return 1; })()")
      await sync(1)
    wa=await ev(A,"+__G('molino').mv.w.toFixed(2)")
    await ev(B,"player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-4); player.vel.set(0,0,0); 1"); await sync(3)
    wa2=await ev(A,"+__G('molino').mv.w.toFixed(2)"); wb2=await ev(B,"+__G('molino').mv.w.toFixed(2)")
    ok(abs(wa)>.15, '🌀 Beto empuja un aspa del molino y en el mundo de Ana también gira (%s rad/s)'%wa)
    ok(abs(wa2-wb2)<max(.2,abs(wa2)*.4), 'y los dos lo ven girar igual (Ana %s, Beto %s rad/s)'%(wa2,wb2))

    # 5. la capa en las paredes: Ana embarra miel en una torre y Beto ve las paredes igual
    await ev(A,"""(()=>{ const L=[]; for(let a=0;a<3;a++) for(let c=0;c<3;c++) for(let y=0;y<2;y++){ const o=freeAddStatic({k:'b',a:0,b:6},FREE.X+20+a-1,FREE.Y+y,FREE.Z+c-1,0,true); fnLocalAdd(o); } return 1; })()""")
    await sync(6)
    await ev(A,"(()=>{ for(let i=0;i<80;i++){ suPour(FREE.X+20,FREE.Z,4,0,.03,.5); __S(1); } return 1; })()")
    for i in range(30):
      await sync(1)
    va=await ev(A,"[SU.wl.size, +wlVol().toFixed(3)]"); vb=await ev(B,"[SU.wl.size, +wlVol().toFixed(3)]")
    ok(va[1]>.01 and vb[0]>=max(1,va[0]-2) and abs(vb[1]-va[1])<max(.01,va[1]*.35), '🍯 la miel en las paredes se ve igual para los dos (Ana %s hojas %s m³, Beto %s hojas %s m³)'%(va[0],va[1],vb[0],vb[1]))
    # Ana limpia: a Beto también se le limpian las paredes
    await ev(A,"(()=>{ suClear(); return 1; })()")
    for i in range(30):
      await sync(1)
      if await ev(B,"SU.wl.size===0"): break
    rb=await ev(B,"SU.wl.size"); ok(rb==0, '🧹 Ana limpia y a Beto también se le limpian las paredes (%s hojas)'%rb)
    # 6. la arena: Ana hace un montón de arena y Beto lo ve igual; Beto camina encima y no se hunde
    await ev(A,"(()=>{ for(let i=0;i<80;i++){ suPour(FREE.X-12,FREE.Z+6,7,0,.02,.3); __S(1); } return 1; })()")
    for i in range(30):
      await sync(1)
      if await ev(B,"SU.hasSand && suSandTop(FREE.X-12,FREE.Z+6)>FREE.Y+.4"): break
    ta=await ev(A,"+(suSandTop(FREE.X-12,FREE.Z+6)-FREE.Y).toFixed(2)"); tb=await ev(B,"+(suSandTop(FREE.X-12,FREE.Z+6)-FREE.Y).toFixed(2)")
    ok(tb>.3 and abs(ta-tb)<.15, '🏖️ Ana hace un montón de arena y Beto lo ve igual (Ana %s m, Beto %s m)'%(ta,tb))
    r=await ev(B,"(()=>{ player.pos.set(FREE.X-12,FREE.Y+1.5,FREE.Z+6); player.vel.set(0,0,0); __S(25); return [+(player.pos.y-FREE.Y).toFixed(2), player.swim]; })()")
    ok(r[0]>tb-.12 and not r[1], 'y Beto se para encima de la arena (a %s m)'%r[0])
    pb_=await ev(A,"__PB"); ok(pb_<=3700, 'lo más que mandó Ana pesa %s bytes'%pb_)
    ok(not ea and not eb,'sin errores %s %s'%(ea[:3],eb[:3])); await b.close()
asyncio.run(m())
