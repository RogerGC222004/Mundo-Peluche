# v240 en una sala: la pelota que Ana mete al lodo, Beto también la ve embarrada; y el rastro de pintura que deja, también.
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



    # 1. Ana hace un charco de lodo y uno de pintura y pone una pelota; Beto llega
    await ev(A,"""(()=>{ const X=FREE.X, Y=FREE.Y, Z=FREE.Z+10, m=SU.cs; for(let x=-1;x<=1.01;x+=m) for(let z=-1;z<=1.01;z+=m) suPour(X+x,Z+z,3,0,.3*m*m,.1); __S(10); player.pos.set(X+4,Y+.05,Z+3); window.__BL=freeAddDyn('goma',X-2.5,Y+.4,Z,true); fnLocalAdd(__BL); __S(2); return 1; })()""")
    await ev(B,"player.pos.set(FREE.X-4,FREE.Y+.05,FREE.Z+13); __S(2); 1")
    await sync(20)
    # 2. la pelota rueda al lodo (la mueve Ana)
    await ev(A,"(()=>{ __BL.v.set(3,0,0); freeWake(__BL); return 1; })()")
    seen=None
    for i in range(30):
      await ev(A,"__S(2); 1"); await A.wait_for_timeout(30); await ev(B,"__S(2); 1"); await B.wait_for_timeout(30)
      seen=await ev(B,"(()=>{ for(const d of FREE.dyn){ if(d.P.id!=='goma') continue; const S=d.root.userData.stn; if(S && stCoat(S,3)>0){ let w=0; d.root.traverse(q=>{ if(q.isMesh && q.material && q.material.userData && q.material.userData.stOrig) w++; }); return [S.vx.n, +stCoat(S,3).toFixed(2), w]; } } return null; })()")
      if seen and seen[2]>0: break
    sa=await ev(A,"(()=>{ const S=__BL.root.userData.stn; return S?+stCoat(S,3).toFixed(2):0; })()")
    ok(seen is not None and seen[1]>.2 and sa>.2, '🟤 la pelota que Ana mete al lodo, Beto también la ve embarrada (Ana %s, Beto %s)'%(sa, seen))
    # 3. rastro: la pelota pintada rueda por lo seco (lo hace Ana) y Beto ve el rastro
    await ev(A,"""(()=>{ const X=FREE.X, Y=FREE.Y, Z=FREE.Z+10; __BL.root.position.set(X+3,Y+.4,Z+3); __BL.v.set(0,0,0); __S(2); stObjHit(__BL,5,__BL.root.position.x,__BL.root.position.y-.2,__BL.root.position.z,.4,1,0xff3399); __BL.v.set(0,0,-4); freeWake(__BL); for(let k=0;k<40;k++) __S(1); return 1; })()""")
    await sync(20)
    tr=await ev(B,"(()=>{ let n=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===5 && C.h[i]>0) n++; return n; })()")
    ta=await ev(A,"(()=>{ let n=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===5 && C.h[i]>0) n++; return n; })()")
    ok(ta>2 and tr>2, '🛞 la pelota pintada deja rastro de pintura y Beto también lo ve (Ana %s cuadritos, Beto %s)'%(ta,tr))
    pb_=await ev(A,"__PB"); ok(pb_<=3700, 'lo más que mandó Ana pesa %s bytes'%pb_)
    ok(not ea and not eb,'sin errores %s %s'%(ea[:3],eb[:3])); await b.close()
asyncio.run(m())
