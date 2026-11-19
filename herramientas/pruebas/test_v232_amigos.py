# v232 en una sala de «Construir con amigos»: las sustancias se ven para los dos (las manda el dueño), lo que echa el invitado le
# llega al dueño, las bolas de los dos se ven, la pintura mancha para todos, el bote de basura y la escoba quitan para todos, y
# las huellas de Beto se marcan también en el lodo de Ana.
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
    VOL="(()=>{ suRecount(); const o={}; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i] && C.h[i]>0) o[C.t[i]]=(o[C.t[i]]||0)+C.h[i]*.04; for(const k in o) o[k]=+o[k].toFixed(3); return o; })()"
    await ev(A,"fnCreate(false); 1"); await A.wait_for_timeout(1500)
    await ev(A,"""(()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); suClear(); suPour(FREE.X-6,FREE.Z+4,1,0,.05,.4); suPour(FREE.X-2,FREE.Z+4,2,0,.05,.4); suPour(FREE.X+3,FREE.Z+4,3,0,.12,.6); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+14); return 1; })()""")
    await sync(4)
    code=await ev(A,"FNET.code"); await ev(B,"(async()=>{ ui('freeBtn').click(); await new Promise(r=>setTimeout(r,600)); return 1; })()")
    await ev(B,"fnJoin(%s); 1"%json.dumps(code)); await B.wait_for_timeout(1500); await ev(B,"player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+14); 1")
    for i in range(40):
      await sync(1)
      if await ev(B,"fnSynced() && SU.list.filter(C=>C.n).length>=3"): break
    await sync(10)
    va=await ev(A,VOL); vb=await ev(B,VOL)
    ok(all(k in vb and abs(vb[k]-va[k])<=va[k]*.25+.002 for k in va), 'Beto entra y ve el agua, el slime y el lodo de Ana %s %s'%(va,vb))
    # 2. Beto echa miel: a Ana le llega
    await ev(B,"(()=>{ suNetPour(FREE.X+8,FREE.Z-4,4,0,.06,.4); return 1; })()"); await sync(10)
    va=await ev(A,VOL); vb=await ev(B,VOL)
    ok(va.get('4',0)>.045 and vb.get('4',0)>.045, 'Beto echa miel y le aparece a Ana también %s'%[va.get('4'),vb.get('4')])
    # 3. bolas: la de Beto (de pintura, a un bloque) y la de Ana
    await ev(A,"(()=>{ freeAddStatic({k:'b',a:0,b:9},FREE.X+.5,FREE.Y,FREE.Z-9.5,0,true); fnLocalAdd(FREE.objs[FREE.objs.length-1]); return 1; })()"); await sync(8)
    await ev(B,"(()=>{ camMode='first'; player.pos.set(FREE.X+.5,FREE.Y+.05,FREE.Z-13); player.facing=0; camera.position.set(FREE.X+.5,FREE.Y+1.5,FREE.Z-13); camera.lookAt(FREE.X+.5,FREE.Y+1.4,FREE.Z-9.5); camera.updateMatrixWorld(); SU.balls.forEach(b=>b.m.parent&&b.m.parent.remove(b.m)); SU.balls.length=0; suLaunch(5,6,.3); return SU.balls.length; })()")
    seenA=0
    for i in range(14):
      await sync(1); seenA=max(seenA,await ev(A,"SU.balls.length"))
    colA=await ev(A,"FREE.objs.find(o=>o.sel.k==='b').sel.b"); await sync(10); colB=await ev(B,"(FREE.objs.find(o=>o.sel.k==='b')||{sel:{}}).sel.b")
    wA=await ev(A,"[...SU.wl.values()].reduce((a,W)=>a+W.t.filter((t,k)=>t===5 && W.h[k]>0).length,0)"); wB=await ev(B,"[...SU.wl.values()].reduce((a,W)=>a+W.t.filter((t,k)=>t===5 && W.h[k]>0).length,0)")
    ok(seenA>=1 and colA==9 and colB==9 and wA>0, 'Beto avienta una bola de pintura: Ana la ve volar y le queda pintada la pared donde pegó; el bloque no cambia de color para nadie (v236; lo de las paredes lo calcula cada quien) %s'%[seenA,colA,colB,wA,wB])
    await ev(A,"(()=>{ camMode='first'; player.pos.set(FREE.X-8,FREE.Y+.05,FREE.Z-8); player.facing=0; camera.position.set(FREE.X-8,FREE.Y+1.5,FREE.Z-8); camera.lookAt(FREE.X-8,FREE.Y+1,FREE.Z-2); camera.updateMatrixWorld(); suLaunch(1,0,.3); camMode='third'; return 1; })()")
    seenB=0
    for i in range(8):
      await sync(1); seenB=max(seenB,await ev(B,"SU.balls.length"))
    ok(seenB>=1, 'y Beto ve volar la bola de agua de Ana (%s)'%seenB)
    # 4. huellas de Beto en el lodo de Ana
    await sync(20)
    h0=await ev(A,"(()=>{ const q=suAt(FREE.X+3,FREE.Z+4); return q?q[1]:0; })()")
    await ev(B,"(()=>{ camMode='third'; player.pos.set(FREE.X+1.4,FREE.Y+.05,FREE.Z+4); return 1; })()")
    for i in range(20):
      await ev(B,"(()=>{ player.pos.x+=.16; player.vel.set(3,0,0); return 1; })()"); await sync(1)
    h1=await ev(A,"(()=>{ const q=suAt(FREE.X+3,FREE.Z+4); return q?q[1]:0; })()")
    ok(h0>.05 and h1<h0*.5, 'Beto camina por el lodo y Ana ve su huella (%.3f → %.3f m)'%(h0,h1))
    # 5. el bote de basura y la escoba de Beto
    await ev(B,"(()=>{ suRemoveAt(FREE.X-2,FREE.Z+4); fnOp(['qx',-2,4]); return 1; })()"); await sync(8)
    va=await ev(A,VOL)
    ok('2' not in va and va.get('1',0)>0, 'Beto quita el slime con el bote de basura y a Ana se le quita (el agua se queda) %s'%va)
    await ev(B,"(()=>{ freeWipeMine(); return 1; })()"); await sync(40)
    va=await ev(A,VOL); vb=await ev(B,VOL)
    ok(not va and not vb, 'la escoba de Beto limpia las sustancias para los dos %s %s'%(va,vb))
    pb_=await ev(A,"__PB"); ok(pb_<=3700, 'lo más que mandó Ana pesa %s bytes'%pb_)
    ok(not ea and not eb,'sin errores %s %s'%(ea[:3],eb[:3])); await b.close()
asyncio.run(m())
