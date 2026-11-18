# v228: la zona de inicio limpia (las plataformas y pistones de la carrera ya nacen en su lugar, no amontonados donde apareces)
# y menos tirón al llegar y al teletransportarte: los talleres de vehículos y el papel de los carteles de los minijuegos se
# preparan en la pantalla de carga, los carteles se pintan copiando el papel, y una vuelta de cámara sube las imágenes del inicio.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    # 1. nada de la carrera en la zona de inicio; cada plataforma y pistón ya está en la pista
    r=await ev("""(()=>{ let near=0, far=0; const v=new THREE.Vector3(); for(const m of RC.M){ m.o.getWorldPosition(v); if(Math.hypot(v.x-START.x,v.z-START.z)<20) near++; else far++; }
      for(const q of RC.R){ q.o.getWorldPosition(v); if(Math.hypot(v.x-START.x,v.z-START.z)<20) near++; else far++; }
      const A=rcA(), on=RC.M.every(m=>{ m.o.getWorldPosition(v); return Math.hypot(v.x-A.center[0],v.z-A.center[1])<RC.L; });
      const rc=new THREE.Raycaster(); rc.camera=camera; let hits=0; scene.updateMatrixWorld(true); for(let x=-2.4;x<=2.4;x+=.6) for(let z=-2.4;z<=2.4;z+=.6){ rc.set(new THREE.Vector3(START.x+x,5,START.z+z),new THREE.Vector3(0,-1,0)); const h=rc.intersectObjects(scene.children,true).find(h=>{ for(let q=h.object;q;q=q.parent){ if(q===plush || !q.visible) return false; } return (h.object.layers.mask&1) && !h.object.isPoints && !h.object.isSprite; }); if(h && h.point.y>START.top+.4) hits++; }
      return [near, far, on, hits]; })()""")
    ok(r[0]==0 and r[2] and r[3]==0, 'inicio: ninguna plataforma ni pistón de la carrera queda donde apareces (%s en el inicio, %s en la pista) y encima del botón no hay nada %s'%(r[0],r[1],r))
    # 2. lo pesado ya se hizo en la pantalla de carga
    r=await ev("""(()=>{ const papers=['¿Cómo se juega?','Instrucciones'].length; const t=HOWTO.get('canasta')[0]; const a=performance.now(); t.__paint(); const ms=performance.now()-a; const t2=HOWTO.get('papa')[1]; const a2=performance.now(); t2.__paint(); const ms2=performance.now()-a2;
      return [VE.built, VE.TS.length, +ms.toFixed(1), +ms2.toFixed(1), state]; })()""")
    ok(r[0] and r[1]>=2 and r[4]=='menu', 'los talleres de vehículos ya están armados antes de entrar a jugar (%s talleres)'%r[1])
    ok(r[2]<12 and r[3]<12, 'los carteles de los minijuegos se pintan rapidito (%s ms y %s ms; antes 20–60 ms cada uno)'%(r[2],r[3]))
    # 3. al entrar a jugar casi no hay imágenes nuevas que subir (ya se subieron en la carga)
    r=await ev("""(async()=>{ window.requestAnimationFrame=()=>0; const R=renderer, t0=R.info.memory.textures; startGame(); let mx=0; for(let i=0;i<12;i++){ capLast=-1e9; const a=performance.now(); frame(); mx=Math.max(mx,performance.now()-a); await new Promise(r=>setTimeout(r,16)); }
      return [R.info.memory.textures-t0, Math.round(mx), VE.TS.length]; })()""")
    ok(r[0]<=4, 'al aparecer casi no hay imágenes nuevas que subir (%s; antes 38)'%r[0])
    # 4. la carrera sigue funcionando: al acercarte, las plataformas se mueven
    r=await ev("""(()=>{ const A=rcA(); player.pos.set(A.center[0],groundAt(A.center[0],A.center[1],99)+.05,A.center[1]); let t=clock.elapsedTime; const m=RC.M[0], p0=m.o.position.clone(); for(let i=0;i<30;i++){ clock.elapsedTime=(t+=.05); update(.05,t); } return [RC.near, +m.o.position.distanceTo(p0).toFixed(2)]; })()""")
    ok(r[0] and r[1]>.05, 'carrera: al acercarte las plataformas se siguen moviendo %s'%r)
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close(); await b.close()
asyncio.run(m())
