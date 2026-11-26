# v270: brincar mientras avanzas con la palanca (corres desde la mitad, el aire no te frena, más margen al brincar en la orilla)
# y en cada minijuego solo los botones que sirven, con su nombre (Turbo, Embestida, Brinco alto…); instrucciones al día.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
SEED="""localStorage.clear(); localStorage.setItem('mundoPelucheEcon124','1');
localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false, autoRes:false}));"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    pg=await (await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, locale='es-MX')).new_page(); errs=[]; cerr=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console",lambda msg: cerr.append(msg.text[:200]) if msg.type=='error' and ('Shader' in msg.text or 'WebGL' in msg.text or 'GL_' in msg.text) else None)
    await pg.add_init_script(SEED)
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=180000)
    await ev("""(()=>{ startGame(); window.requestAnimationFrame=()=>0; window.__run=(sec,fn)=>{ let t=clock.elapsedTime; for(let i=0;i<Math.round(sec/.05);i++){ clock.elapsedTime=(t+=.05); if(fn && fn(i)===true) return true; update(.05,t); updateRemotes(.05,t); updateSky(.05); scene.updateMatrixWorld(); } }; __run(1); return 1; })()""")
    # 1. carrera: de cojín en cojín empujando la palanca a 2/3 (antes caminabas y no alcanzabas)
    r=await ev("""(()=>{ mgqLocal(3,0,1); __run(25,()=>AR.G[3].ph===3); const out=[]; settings.alwaysRun=false; const P=RC.P.filter(p=>p.t==='p' && p.s<60);
      for(const mag of [.65,1]){ let okN=0; for(let k=0;k<4;k++){ const a=P[k], b=P[k+1], wa=rcW(a.s,a.w,a.y+.1), wb=rcW(b.s,b.w,b.y); player.pos.copy(wa); player.vy=0; player.vel.set(0,0,0); AR.me.st=2; __run(.4);
        yaw=Math.atan2(wb.x-wa.x,wb.z-wa.z)+Math.PI; let jumped=false, t=clock.elapsedTime, land=false; stick.x=0; stick.y=-mag;
        for(let i=0;i<120;i++){ if(!jumped && Math.hypot(player.pos.x-wa.x,player.pos.z-wa.z)>=1.0){ jump(); jumped=true; } clock.elapsedTime=(t+=1/30); update(1/30,t); if(player.pos.y<SEA_Y) break; if(jumped && player.grounded && player.pos.y>RC.Y-.2){ land=Math.hypot(player.pos.x-wb.x,player.pos.z-wb.z)<b.r+.2; break; } }
        stick.y=0; if(land) okN++; } out.push(okN); }
      arLeave(); __run(1); return out; })()""")
    ok(r==[4,4], '1 carrera de obstáculos: brincas de cojín en cojín aunque no empujes la palanca hasta el fondo %s'%r)
    # 2. saltar justo después de salirte de la orilla (un cuarto de segundo de margen)
    r=await ev("""(()=>{ player.pos.set(START.x+2,START.top+.05,START.z); __run(.5); player.grounded=false; player.vy=0; player.lastGroundT=performance.now()/1000-.2; jump(); const a=player.vy; player.vy=0; player.grounded=false; player.lastGroundT=performance.now()/1000-.35; jump(); return [a, player.vy]; })()""")
    ok(r[0]>6 and r[1]<1, '2 si te acabas de salir de la orilla (0.2 s) todavía brincas; mucho después ya no %s'%r)
    # 3. los botones de cada minijuego
    r=await ev("""(()=>{ const vis=id=>ui(id).style.visibility!=='hidden', lab=id=>ui(id).textContent.trim(), out={};
      for(const [a,n] of [[5,1],[2,1],[3,0],[NUMI,0],[POGI,0],[COLI,0]]){ mgqLocal(a,n,1); if(a===POGI) POG.ask=3; __run(25,()=>AR.G[a].ph>=1); __run(.2); out[AR_SPOTS[a].id]=[vis('tJump')?lab('tJump'):'-', vis('tDive'), vis('tGest'), vis('tWave')]; arLeave(); __run(1); }
      out.fuera=[vis('tJump')?lab('tJump'):'-', vis('tDive'), vis('tGest'), vis('tWave')]; return out; })()""")
    ok(r['carritos'][0]=='Turbo' and r['bola'][0]=='Embestida' and r['carrera'][0]=='Saltar' and r['numero'][0]=='-' and r['pogo'][0]=='Brinco alto' and r['colores'][0]=='-' and not any(r[k][1] or r[k][2] or r[k][3] for k in ['carritos','bola','carrera','numero','pogo','colores']) and r['fuera']==['Saltar',True,True,True], '3 en cada minijuego solo los botones que sirven, con su nombre; al salir regresan todos %s'%r)
    # 4. las instrucciones ya hablan del botón con su nombre
    r=await ev("(()=>{ const t=JSON.stringify(HOWTO.G); return [t.includes('Saltar = '), t.includes('«Turbo»'), t.includes('«Embestida»'), t.includes('«Brinco alto»'), t.includes('hasta el fondo'), t.includes('al fondo)')]; })()")
    ok(r==[False,True,True,True,False,False], '4 las instrucciones de los minijuegos usan el nombre de cada botón (ya no «Saltar = turbo») %s'%r)
    ok(not errs and not cerr, 'sin errores %s %s'%(errs[:3],cerr[:3]))
    await b.close()
asyncio.run(m())
