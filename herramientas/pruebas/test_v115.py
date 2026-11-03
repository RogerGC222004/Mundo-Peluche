import asyncio, json, sys
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
SRC=sys.argv[1] if len(sys.argv)>1 else '/home/claude/mundo-peluche.html'
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open(SRC).read()
html=html.replace("function frame(){","window.__T={ev(s){ return eval(s); }}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":320,"height":200}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false, shadows:false}))")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=120000); await pg.wait_for_timeout(2000)
    await pg.evaluate("document.getElementById('playBtn').click()"); await pg.wait_for_timeout(1000)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    async def run(sec):
      n=int(sec/.05)
      for i in range(n):
        await ev("update(.05,performance.now()/1000)"); await pg.wait_for_timeout(50)
    print('versión', await ev("GAME_VERSION"), 'tone', await ev("renderer.toneMapping"))
    # ---------- avión: caminar por el pasillo y sentarse en cada fila ----------
    await ev("player.ac={i:0,mode:'inside',t0:performance.now()/1000,l:[0,PL.F,5.2],f:0,seat:-1}; 1")
    res=[]
    for k in range(10):
      z=3.6-k*1.2
      lab=await ev(f"(()=>{{ player.ac.l=[0.1,PL.F,{z}+.3]; const r=airActions(); const a=r.find(x=>x&&/Sentarse|Pilotar/.test(x.label)); return a?a.label:null; }})()")
      res.append(lab)
    print('acciones por fila:', res)
    await ev("(()=>{ player.ac.l=[0.1,PL.F,-1.2+.3]; const r=airActions(); r.find(x=>x&&/Sentarse/.test(x.label)).run(); })()")
    await run(.8)
    print('sentado:', await ev("[player.ac.mode, player.ac.seat, player.ac.l.map(v=>+v.toFixed(2)), PLANE_SEATS[player.ac.seat]]"))
    await ev("standAir()"); await run(.2)
    print('de pie:', await ev("[player.ac.mode, player.ac.l.map(v=>+v.toFixed(2))]"))
    # caminar hacia atrás hasta el fondo: no se sale del pasillo
    await ev("player.ac.l=[0,PL.F,-12]; clampInside(aircraft[0],player.ac.l); 1"); print('fondo del pasillo:', await ev("player.ac.l.map(v=>+v.toFixed(2))"))
    await ev("player.ac=null; forceFirst(false); 1")
    # ---------- helicóptero: subir, sentarse atrás, bajar ----------
    await ev("(()=>{ const a=aircraft[2], c=Math.cos(a.h), s=Math.sin(a.h), lx=2.7, lz=0; player.pos.set(a.x+lx*c+lz*s, a.y, a.z-lx*s+lz*c); player.vel.set(0,0,0); })()")
    await run(.3)
    lab=await ev("(()=>{ const r=airActions(); return r.map(x=>x&&x.label); })()"); print('junto al helicóptero:', lab)
    await ev("airActions()[0].run()"); await run(1.8)
    print('adentro:', await ev("player.ac && [player.ac.mode, player.ac.l.map(v=>+v.toFixed(2))]"))
    await ev("player.ac.l=[.3,HE.F,-.45]; 1")
    print('atrás:', await ev("airActions().map(x=>x&&x.label)"))
    await ev("airActions().find(x=>x&&/Sentarse/.test(x.label)).run()"); await run(.8)
    print('sentado heli:', await ev("[player.ac.mode, player.ac.seat, player.ac.l.map(v=>+v.toFixed(2))]"))
    # ¿la cabeza queda dentro del casco? punto más alto del peluche vs casco en esa posición
    print('margen cabeza (casco - cabeza, >0 = cabe):', await ev("(()=>{ const [x,y,z]=player.ac.l; const top=y+BODY_Y+1.68; const k=1-(x/HE.SX)**2-(z/HE.SZ)**2; return +(HE.CY+HE.SY*Math.sqrt(Math.max(0,k-0)) - top).toFixed(2); })()"))
    await ev("standAir()"); await run(.2); await ev("player.ac.l[0]=0.9; 1")
    print('en la abertura:', await ev("airActions().map(x=>x&&x.label)"))
    await ev("airActions()[0].run()"); await run(1.4)
    print('abajo:', await ev("[player.ac, +(player.pos.y-aircraft[2].y).toFixed(2)]"))
    # ---------- rueda de la fortuna ----------
    await ev("(()=>{ const d=MINIS.find(m=>m.id==='rueda'); const p=bW(d.e,0,0,-3); player.pos.set(p.x,FY,p.z); startMini(d); })()"); await run(.5)
    print('rueda: altura del peluche sobre el andén', await ev("+(player.pos.y-FY).toFixed(2)"), 'mini', await ev("player.mg&&player.mg.g.id"))
    await ev("endMini(player.mg,null)"); await run(.3); await ev("player.mg=null; document.body.classList.remove('in-mg'); 1")
    # ---------- carrusel ----------
    await ev("(()=>{ const d=MINIS.find(m=>m.id==='carrusel'); const p=bW(d.e,0,0,-5.5); player.pos.set(p.x,FY,p.z); startMini(d); })()"); await run(.5)
    print('mini:', await ev("player.mg&&player.mg.g.id")); a=await ev("[player.pos.x,player.pos.y,player.pos.z,player.facing]"); await run(.5); b2=await ev("[player.pos.x,player.pos.y,player.pos.z,player.facing]")
    import math
    mv=math.atan2(b2[0]-a[0], b2[2]-a[2]); print('carrusel: dirección de avance vs hacia dónde mira (debe ser ~0):', round(((mv-b2[3]+math.pi)%(2*math.pi))-math.pi,2))
    for i in range(4):
      print('  muestra', await ev("(()=>{ const d=MINIS.find(m=>m.id==='carrusel'); return [player.pos.x.toFixed(2), player.pos.z.toFixed(2), player.facing.toFixed(2), d.e.yaw.toFixed(2), player.mg&&player.mg.g.id, player.mg&&player.mg.over, player.mg&&+player.mg.t.toFixed(1), state, (Date.now()/1000%24).toFixed(2)]; })()")); await run(.3)
    print('errores:', errs[:4] or 'ninguno'); await b.close()
asyncio.run(m())
