# v233 en una sala de «Construir con amigos»: las capas (miel sobre lodo, espuma sobre agua) y las mezclas (agua de color, pintura
# mezclada) se ven igual para los dos; lo que el invitado mezcla le llega al dueño; la bola grande del invitado cae con su volumen.
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
    VOL="(()=>{ suRecount(); const o={}; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i] && C.h[i]>0) o[C.t[i]]=(o[C.t[i]]||0)+C.h[i]*.04; for(const k in o) o[k]=+o[k].toFixed(3); return o; })()"
    CEL="(x,z)=>{ const q=suCell(FREE.X+x,FREE.Z+z,false); if(!q) return null; const [C,i]=q; return [C.t[i],C.t2[i],(C.c[i]&0xffffff).toString(16),(C.c2[i]&0xffffff).toString(16)]; }"
    await ev(A,"fnCreate(false); 1"); await A.wait_for_timeout(1500)
    await ev(A,"""(()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); suClear(); const X=FREE.X, Z=FREE.Z;
      suPour(X-6,Z+4,3,0,.3,1.2); suPour(X,Z+4,1,0,.25,.6); suPour(X+6,Z+4,5,2,.04,.3); suPour(X+6.2,Z+4,5,6,.04,.3); __S(20); suPour(X-6,Z+4,4,0,.02,.3); suPour(X,Z+4,5,0,.004,.3); suPour(X,Z+5,6,0,.05,.3); __S(20); player.pos.set(X,FREE.Y+.05,Z+14); return 1; })()""")
    await sync(4)
    code=await ev(A,"FNET.code"); await ev(B,"(async()=>{ ui('freeBtn').click(); await new Promise(r=>setTimeout(r,600)); return 1; })()")
    await ev(B,"fnJoin(%s); 1"%json.dumps(code)); await B.wait_for_timeout(1500); await ev(B,"player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+14); 1")
    for i in range(40):
      await sync(1)
      if await ev(B,"fnSynced() && SU.list.filter(C=>C.n).length>=2"): break
    LS="JSON.stringify(Object.fromEntries(SU.list.filter(C=>C.n).map(C=>[C.ci+'.'+C.cj,C.n])))"
    for i in range(60):
      await sync(1)
      la=json.loads(await ev(A,LS)); lb=json.loads(await ev(B,LS))
      if all(k in lb and abs(lb[k]-v)<=max(3,v*.1) for k,v in la.items()): break
    await sync(14)
    pts=[(-6,4),(0,4),(6.1,4),(0,5)]
    ca=await ev(A,"(()=>{ const f=%s; return %s.map(([x,z])=>f(x,z)); })()"%(CEL,json.dumps(pts))); cb=await ev(B,"(()=>{ const f=%s; return %s.map(([x,z])=>f(x,z)); })()"%(CEL,json.dumps(pts)))
    LY="(()=>{ let n=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===3 && C.t2[i]===4 && C.h2[i]>0) n++; return n; })()"
    na_=await ev(A,LY); nb_=await ev(B,LY)
    ok(na_>3 and abs(nb_-na_)<=max(2,na_*.3), 'Beto ve la miel encima del lodo de Ana, en capas (%s y %s cuadritos)'%(na_,nb_))
    ok(ca[1][0]==1 and cb[1][0]==1 and cb[1][2]!='0' and ca[3][1]==6 and cb[3][1]==6, 'Beto ve el agua de color y la espuma flotando %s %s'%([ca[1],ca[3]],[cb[1],cb[3]]))
    g=lambda h:[int(h.zfill(6)[i:i+2],16) for i in (0,2,4)]
    ok(cb[2][0]==5 and abs(g(cb[2][2])[1]-g(ca[2][2])[1])<24, 'y la pintura mezclada del mismo color (%s / %s)'%(ca[2][2],cb[2][2]))
    # Beto mezcla: slime + pintura morada (lo echa él; le llega a Ana)
    await ev(B,"(()=>{ suNetPour(FREE.X+10,FREE.Z-4,2,0,.1,.4); suNetPour(FREE.X+10,FREE.Z-4,5,suCol(7),.03,.3); return 1; })()"); await sync(14)
    sa=await ev(A,"(()=>{ const q=suCell(FREE.X+10,FREE.Z-4,false); return q?[q[0].t[q[1]],q[0].s[q[1]],(q[0].c[q[1]]&0xffffff).toString(16)]:null; })()")
    ok(sa and sa[0]==2 and sa[1]>0, 'Beto echa slime y pintura: a Ana le queda slime de color %s'%sa)
    # la bola grande de Beto cae con su volumen
    v0=await ev(A,"(suRecount(), SU.vol)")
    await ev(B,"(()=>{ camMode='first'; player.pos.set(FREE.X-10,FREE.Y+.05,FREE.Z-9); player.facing=0; camera.position.set(FREE.X-10,FREE.Y+1.6,FREE.Z-9); camera.lookAt(FREE.X-10,FREE.Y,FREE.Z-7); camera.updateMatrixWorld(); suLaunch(3,0,.4); camMode='third'; return 1; })()")
    for i in range(30): await sync(1)
    v1=await ev(A,"(suRecount(), SU.vol)")
    ok(abs((v1-v0)-4.18879*.4**3)<.03, 'la bola de lodo de Beto le cae a Ana con su volumen (%.3f m³; la bola: %.3f)'%(v1-v0,4.18879*.4**3))
    pb_=await ev(A,"__PB"); ok(pb_<=3700, 'lo más que mandó Ana pesa %s bytes'%pb_)
    ok(not ea and not eb,'sin errores %s %s'%(ea[:3],eb[:3])); await b.close()
asyncio.run(m())
