# v239 en una sala: cuando Ana cae a la alberca, Beto ve las olas (y al revés); lo que se lleva la corriente se ve igual en los dos.
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
      player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-6); return 1; })()""")
    await sync(4)
    code=await ev(A,"FNET.code"); await ev(B,"(async()=>{ ui('freeBtn').click(); await new Promise(r=>setTimeout(r,600)); return 1; })()")
    await ev(B,"fnJoin(%s); 1"%json.dumps(code)); await B.wait_for_timeout(1500); await ev(B,"weatherNow.wind=0; player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-4); 1")
    for i in range(40):
      await sync(1)
      if await ev(B,"fnSynced()"): break


    # 0. Ana arma una alberca de agua (con paredes) y Beto llega
    await ev(A,"""(()=>{ const X=FREE.X, Y=FREE.Y, Z=FREE.Z+10; for(let a=-5;a<=5;a++) for(let c=-5;c<=5;c++) if(Math.abs(a)===5||Math.abs(c)===5) for(let y=0;y<2;y++) freeAddStatic({k:'b',a:0,b:6},X+a,Y+y,Z+c,0,true); __S(1); const m=SU.cs; for(let x=-4.4;x<=4.41;x+=m) for(let z=-4.4;z<=4.41;z+=m) suPour(X+x,Z+z,1,0,1.3*m*m,.1); __S(20); player.pos.set(X+6.5,Y+.05,Z); __S(2); return 1; })()""")
    await ev(B,"player.pos.set(FREE.X-6.5,FREE.Y+.05,FREE.Z+10); __S(2); 1")
    for i in range(40):
      await sync(1)
      if await ev(B,"SU.list.length>0 && (()=>{ const a=suAt(FREE.X,FREE.Z+10); return !!a && a[2]-FREE.Y>1; })()"): break
    okw=await ev(B,"(()=>{ const a=suAt(FREE.X,FREE.Z+10); return !!a && a[2]-FREE.Y>1; })()")
    ok(okw, '🏊 Beto ya ve la alberca llena que hizo Ana')

    # 1. Ana cae a la alberca: Beto ve las olas
    await ev(A,"(()=>{ wvOff(); player.pos.set(FREE.X,FREE.Y+3.4,FREE.Z+10); player.vel.set(0,0,0); player.vy=0; return 1; })()")
    await ev(B,"wvOff(); 1")
    seen=0; amax=0
    for i in range(40):
      await ev(A,"__S(1); 1"); await A.wait_for_timeout(30); await ev(B,"__S(1); 1"); await B.wait_for_timeout(30)
      w=await ev(B,"(()=>{ let mx=0; for(const d of [0,.6,1.2,1.8,2.4]) for(const s of [-1,1]) mx=Math.max(mx,Math.abs(wvH(FREE.X+d*s,FREE.Z+10))); return [WV.act, +mx.toFixed(4)]; })()")
      if w[0]: seen+=1
      amax=max(amax,w[1])
    aw=await ev(A,"[player.swim, WV.act]")
    ok(seen>0 and amax>.004, '🌊 Ana cae a la alberca y Beto ve las olas (hasta %s m; Ana nadando: %s)'%(amax,aw[0]))

    # 2. Beto (invitado) se avienta: Ana ve las olas
    await ev(B,"(()=>{ wvOff(); player.pos.set(FREE.X-2,FREE.Y+3.4,FREE.Z+12); player.vel.set(0,0,0); player.vy=0; return 1; })()")
    await ev(A,"(()=>{ wvOff(); player.pos.set(FREE.X+6.5,FREE.Y+.05,FREE.Z+10); __S(1); wvOff(); return 1; })()")
    amax=0
    for i in range(40):
      await ev(B,"__S(1); 1"); await B.wait_for_timeout(30); await ev(A,"__S(1); 1"); await A.wait_for_timeout(30)
      w=await ev(A,"(()=>{ let mx=0; for(const d of [0,.6,1.2,1.8]) for(const s of [-1,1]) mx=Math.max(mx,Math.abs(wvH(FREE.X-2+d*s,FREE.Z+12))); return +mx.toFixed(4); })()")
      amax=max(amax,w)
    ok(amax>.004, '🌊 Beto se avienta a la alberca y Ana también ve sus olas (hasta %s m)'%amax)

    # 3. la corriente se lleva una pelota (lo mueve Ana, la anfitriona) y Beto la ve llegar al mismo lugar
    await ev(B,"(()=>{ player.pos.set(FREE.X-6.5,FREE.Y+.05,FREE.Z+10); return 1; })()")
    await ev(A,"(()=>{ player.pos.set(FREE.X+6.5,FREE.Y+.05,FREE.Z+10); window.__BL=freeAddDyn('playa',FREE.X-2,FREE.Y+2,FREE.Z+10,true); fnLocalAdd(__BL); return 1; })()")
    await sync(12)
    x0=await ev(A,"+(__BL.root.position.x-FREE.X).toFixed(2)")
    for i in range(30):
      await ev(A,"(()=>{ for(let k=0;k<6;k++){ wvPush(FREE.X-4.2,FREE.Z+10,1.6,0,.7,.5); __S(1); } return 1; })()"); await A.wait_for_timeout(30); await ev(B,"__S(2); 1"); await B.wait_for_timeout(30)
    await sync(10)
    xa=await ev(A,"+(__BL.root.position.x-FREE.X).toFixed(2)")
    xb=await ev(B,"(()=>{ let best=null; for(const d of FREE.dyn){ if(d.P.id!=='playa') continue; const x=d.root.position.x-FREE.X; if(best===null || Math.abs(d.root.position.z-FREE.Z-10)<1.5) best=x; } return best===null?null:+best.toFixed(2); })()")
    ok(xa-x0>.3 and xb is not None and abs(xb-xa)<.4, '🏐 la corriente se lleva la pelota (Ana: de %s a %s m) y Beto la ve en el mismo lugar (%s m)'%(x0,xa,xb))
    pb_=await ev(A,"__PB"); ok(pb_<=3700, 'lo más que mandó Ana pesa %s bytes (las olas no se mandan: cada quien las calcula)'%pb_)
    ok(not ea and not eb,'sin errores %s %s'%(ea[:3],eb[:3])); await b.close()
asyncio.run(m())
