# v235 en una sala: la máquina de sustancias sale apagada; «llenar hasta» viaja con la configuración; las gotitas que salen las ven
# todos, pero solo las del dueño de la sala son sustancia de verdad (a los demás les llega lo que cayó).
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
    await ev(A,"fnCreate(false); 1"); await A.wait_for_timeout(1500)
    await ev(A,"""(()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); suClear(); FU.pts.length=0; const o=freeAddStatic({k:'p',a:'fuentes',b:FU_DEF},FREE.X-6,FREE.Y,FREE.Z+6,0,true); fnLocalAdd(o); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-6); return 1; })()""")
    await sync(4)
    code=await ev(A,"FNET.code"); await ev(B,"(async()=>{ ui('freeBtn').click(); await new Promise(r=>setTimeout(r,600)); return 1; })()")
    await ev(B,"fnJoin(%s); 1"%json.dumps(code)); await B.wait_for_timeout(1500); await ev(B,"player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-4); 1")
    for i in range(40):
      await sync(1)
      if await ev(B,"fnSynced() && FREE.objs.some(o=>o.gad==='fuentes')"): break
    M="FREE.objs.find(o=>o.gad==='fuentes')"
    r=await ev(B,"(()=>{ const o=%s; return o?fuCfg(o).map(c=>c.on):null; })()"%M)
    ok(r==[0,0,0,0], 'Beto ve la máquina de Ana apagada (así sale ahora) %s'%r)
    # Beto la prende con «llenar hasta: rodillas»
    await ev(B,"(()=>{ const o=%s; const C=fuCfg(o); C[1].on=1; C[1].q=2; C.lim=2; fuSet(o,C); return 1; })()"%M)
    await sync(10)
    ra=await ev(A,"(()=>{ const C=fuCfg(%s); return [C[1].on, C.lim]; })()"%M); rb=await ev(B,"(()=>{ const C=fuCfg(%s); return [C[1].on, C.lim]; })()"%M)
    ok(ra==[1,2] and rb==[1,2], 'Beto la prende con «Llenar hasta: Rodillas» y a Ana le queda igual %s %s'%(ra,rb))
    await sync(16)
    pa=await ev(A,"[FU.pts.length, FU.pts.some(P=>P.v>0)]"); pb=await ev(B,"[FU.pts.length, FU.pts.every(P=>!(P.v>0))]")
    va=await ev(A,"(suRecount(), SU.vol)"); vb=await ev(B,"(suRecount(), SU.vol)")
    ok(pa[0]>0 and pa[1] and pb[0]>0 and pb[1], 'los dos ven las gotitas; las de Ana son las de verdad (las de Beto son para ver) %s %s'%(pa,pb))
    ok(va>.1 and vb>.1 and abs(va-vb)<max(.08,va*.3), 'y la sustancia que echan les llega a los dos (Ana %.2f m³, Beto %.2f m³)'%(va,vb))
    pb_=await ev(A,"__PB"); ok(pb_<=3700, 'lo más que mandó Ana pesa %s bytes'%pb_)
    ok(not ea and not eb,'sin errores %s %s'%(ea[:3],eb[:3])); await b.close()
asyncio.run(m())
