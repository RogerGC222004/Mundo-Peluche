import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read()
html=html.replace("function frame(){","{ const _b=Date.now(), _dn=Date.now; Date.now=()=>window.__tt?_b+(window.__tt-100)*1000:_dn(); } window.__R={RC, rcW, rcL, P:()=>player, cam:camera, show, raceMove, step:(n)=>{ for(let i=0;i<n;i++){ window.__tt=(window.__tt||100)+.033; update(.033,window.__tt); } }}; function frame(){",1)
SL="(()=>{ const P=__R.P(); const [s,w]=__R.rcL(P.pos.x,P.pos.z); return JSON.stringify([+s.toFixed(2),+w.toFixed(2),+(P.pos.y-__R.RC.Y).toFixed(2), P.swim]); })()"
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":720,"height":400}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__R", timeout=120000); await pg.wait_for_timeout(2000)
    await pg.evaluate("document.getElementById('playBtn').click()"); await pg.wait_for_timeout(1500)
    put="(s,w,dy)=>{ const R=__R, P=R.P(), q=R.rcW(s,w,R.RC.Y+(dy||0)); P.pos.copy(q); P.vel.set(0,0,0); P.vy=0; P.grounded=true; P.swim=false; }"
    await pg.evaluate(f"window.__put={put}")
    await pg.evaluate("__put(5,0); __R.step(10)"); print('salida', await pg.evaluate(SL))
    # tronco giratorio en el puente C: pararse en el camino del brazo
    await pg.evaluate("__put(73.5,.5); __R.step(90)"); print('tronco (sin brincar)', await pg.evaluate(SL))
    # pistón en E
    await pg.evaluate("__put(136,0); __R.step(130)"); print('pistón', await pg.evaluate(SL))
    # plataforma móvil D: pararse encima y ver si te lleva
    r=await pg.evaluate("(()=>{ const m=__R.RC.M[0]; __R.raceMove(Date.now()/1000); __put(m.cs,m.cw); __R.step(3); const a=JSON.parse((%s)); __R.step(25); const b=JSON.parse((%s)); return JSON.stringify([a,b,[+m.cs.toFixed(2),+m.cw.toFixed(2)]]); })()"%(SL,SL))
    print('plataforma móvil', r)
    # cojín que rebota
    await pg.evaluate("__put(190.5,-1.2,3); __R.P().grounded=false; __R.P().vy=-2;")
    ys=[]
    for i in range(8):
      await pg.evaluate("__R.step(5)"); ys.append(json.loads(await pg.evaluate(SL))[2])
    print('rebote', ys)
    # caer al agua
    await pg.evaluate("__put(50,6,0); __R.P().grounded=false; __R.step(60)"); print('agua', await pg.evaluate(SL))
    # vistas
    await pg.evaluate("__R.show('pause'); document.getElementById('pause').hidden=true;")
    for name,(cs,cw,cy),(ls,lw,ly) in [('race_start.png',(-8,-14,9),(30,0,0)),('race_mid.png',(150,-22,12),(180,0,0)),('race_far.png',(-30,-60,70),(150,0,0)),('race_end.png',(320,-18,10),(350,0,0))]:
      await pg.evaluate(f"(()=>{{ const R=__R, c=R.cam, a=R.rcW({cs},{cw},R.RC.Y+{cy}), b=R.rcW({ls},{lw},R.RC.Y+{ly}); c.position.copy(a); c.lookAt(b); }})()")
      await pg.wait_for_timeout(1500); await pg.screenshot(timeout=150000,path=name)
    print('errores', errs[:4]); await b.close()
asyncio.run(m())
