# v238 en una sala: si Ana se embarra, Beto la ve embarrada; si se lava en el agua, Beto la ve limpia. Y la mascota de Ana también.
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

    # 1. Ana se mete al lodo: Beto la ve embarrada
    await ev(A,"(()=>{ const m=SU.cs; for(let x=-1;x<=1.01;x+=m) for(let z=-1;z<=1.01;z+=m) suPour(FREE.X+x,FREE.Z+z,3,0,.4*m*m,.1); __S(10); player.pos.set(FREE.X-2.2,FREE.Y+.05,FREE.Z); __S(2); for(let i=0;i<60;i++){ stick.x=0; stick.y=-1; yaw=-Math.PI/2; __S(1); } stick.y=0; return [myStn.A[3], myStn.L[3]]; })()")
    seen=None
    for i in range(30):
      await sync(1)
      seen=await ev(B,"(()=>{ for(const r of mp.remotes.values()){ if(r.stn && r.stn.on && r.stn.A[3]>.5){ let w=0; r.obj.traverse(m=>{ if(m.isMesh && m.material && m.material.userData && m.material.userData.stOrig) w++; }); return [+r.stn.A[3].toFixed(2), +r.stn.L[3].toFixed(2), w]; } } return null; })()")
      if seen and seen[2]>3: break
    la=await ev(A,"+myStn.L[3].toFixed(2)")
    ok(seen is not None and seen[2]>3 and abs(seen[1]-la)<.12, '🟤 Ana se embarra las patas y Beto la ve embarrada igual (Ana hasta %s m, Beto la ve hasta %s m; %s piezas)'%(la, seen[1] if seen else None, seen[2] if seen else 0))
    sn=await ev(A,"stPresence()"); ok(isinstance(sn,str) and len(sn)<=24, 'y solo cuesta %s letras en la presencia («%s»)'%(len(sn) if sn else 0,sn))

    # 2. Ana se tira de panza en pintura azul: Beto la ve azul
    await ev(A,"(()=>{ const m=SU.cs; for(let x=-1;x<=1.01;x+=m) for(let z=-1;z<=1.01;z+=m) suPour(FREE.X+8+x,FREE.Z+z,5,4,.06*m*m,.1); __S(10); player.pos.set(FREE.X+8,FREE.Y+.05,FREE.Z); player.vel.set(0,0,0); __S(3); startDive(); __S(45); return [myStn.F[5], myStn.col]; })()")
    pa=await ev(A,"[+myStn.F[5].toFixed(2), myStn.col]")
    pb=None
    for i in range(20):
      await sync(1)
      pb=await ev(B,"(()=>{ for(const r of mp.remotes.values()) if(r.stn && r.stn.A[5]>.5) return [+r.stn.F[5].toFixed(2), r.stn.col]; return null; })()")
      if pb: break
    same=pb is not None and all(abs(((pa[1]>>s)&255)-((pb[1]>>s)&255))<20 for s in (16,8,0))
    ok(pb is not None and pb[0]>.4 and same, '🎨 Ana se tira de panza en pintura y Beto la ve pintada del mismo color (%s / %s)'%(hex(pa[1]), hex(pb[1]) if pb else None))

    # 3b. (v238b) Ana con botas de lluvia y un manchón de pintura en la espalda: Beto ve el manchón y la ropa manchada
    await ev(A,"""(()=>{ player.dive=null; player.diveAngle=0; player.pos.set(FREE.X-8,FREE.Y+.05,FREE.Z+8); __S(3); stClear(myStn); const id=Object.values(SHOP_BY).find(it=>it.slot==='shoes' && /lluvia/i.test(it.name)).id; wardrobe.eq=Object.assign({},wardrobe.eq,{shoes:id}); applyOutfit(plush,wardrobe.eq); try{ sendPresence(true); }catch(e){} __S(3);
      plush.updateMatrixWorld(true); const fw=new THREE.Vector3(0,0,1).applyQuaternion(plush.quaternion), P=player.pos; myStn.rcT=0; stSpot(plush,myStn,5,new THREE.Vector3(P.x-fw.x*.7+.05,P.y+1.0,P.z-fw.z*.7),.3,1,0x3aa0ff); stTouch(myStn,3,.35,0,0); __S(3); return [myStn.sp.length, stPresenceX()]; })()""")
    sx=await ev(A,"stPresenceX()")
    rb=None
    for i in range(30):
      await sync(1)
      rb=await ev(B,"""(()=>{ for(const r of mp.remotes.values()){ const S=r.stn; if(!S || !S.sp.length || !S.cl1 || !S.cl1.on) continue; let cw=0; r.obj.traverse(m=>{ if(m.isMesh && m.material && m.material.userData && m.material.userData.stOrig && stGKey(r.obj,m) && S.cl1.mats.get(m.material.userData.stOrig)===m.material) cw++; }); const s=S.sp[0]; return [s.p, s.bi, +s.z.toFixed(2), s.c, +S.cl1.A[3].toFixed(2), cw]; } return null; })()""")
      if rb and rb[5]>0: break
    ok(rb is not None and rb[0]==5 and rb[2]<-.1 and rb[5]>0, '🎯 Beto ve el manchón azul en la espalda de Ana y sus botas embarradas (%s; «sx» = %s letras)'%(rb, len(sx) if sx else 0))

    # 3. Ana se lava: Beto la ve limpia
    await ev(A,"(()=>{ player.dive=null; player.diveAngle=0; player.pos.set(FREE.X-8,FREE.Y+.05,FREE.Z+8); __S(3); stClear(myStn); __S(3); return 1; })()")
    cl=None
    for i in range(20):
      await sync(1)
      cl=await ev(B,"(()=>{ for(const r of mp.remotes.values()){ let w=0; r.obj.traverse(m=>{ if(m.isMesh && m.material && m.material.userData && m.material.userData.stOrig) w++; }); return [r.stn?r.stn.on:false, w]; } return null; })()")
      if cl and not cl[0] and cl[1]==0: break
    ok(cl is not None and not cl[0] and cl[1]==0, '🚿 Ana se lava y Beto la ve limpia otra vez %s'%cl)
    pb_=await ev(A,"__PB"); ok(pb_<=3700, 'lo más que mandó Ana pesa %s bytes'%pb_)
    ok(not ea and not eb,'sin errores %s %s'%(ea[:3],eb[:3])); await b.close()
asyncio.run(m())
