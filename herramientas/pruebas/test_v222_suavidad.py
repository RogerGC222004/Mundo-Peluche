# v222: menos tirones. El medidor enseña el peor cuadro; las olas ya no se rehacen cada segundo; los coches, aviones y
# bichitos no se juntan con lo de alrededor (al moverse deshacían grupos enteros); lo que se mueve se recorre con su
# posición entre medidas; los grupos vacíos se revisan en una lista simple; los árboles se acomodan de a poco al caminar;
# Math.hypot rápido. Todo debe seguir funcionando igual.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
ROGER={"quality":"min","qDef":1,"ultra":True,"shadows":False,"weather":False,"fpsCap":"30","autoRes":False,"draw":30,"hints":False,"fps":True}
NORMAL={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateSky(.05); } };
  window.__W=(k)=>new Promise(async res=>{ for(let i=0;i<k;i++){ __S(6); renderer.render(scene,camera); await new Promise(r=>setTimeout(r,300)); } res(1); }); 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    async def open_page(opts):
      ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True, device_scale_factor=2); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
      await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(opts))
      async def route(r):
        if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
        elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
        else: await r.abort()
      await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
      ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300); await ev(STEP)
      return ctx, pg, errs, ev
    ctx,pg,errs,ev=await open_page(ROGER)
    # 1. Math.hypot rápido da lo mismo
    r=await ev("[Math.hypot(3,4), Math.hypot(1,2,2), Math.hypot(-5), Math.hypot(), Math.hypot(1,1,1,1), Number.isNaN(Math.hypot(3,undefined))]")
    ok(r==[5,3,5,0,2,True], 'Math.hypot da lo mismo que antes %s'%r)
    # 2. el medidor enseña el peor cuadro
    r=await ev("(async()=>{ startGame(); { const x=PG.x+6, z=PG.z+10; player.pos.set(x,groundAt(x,z,99)+.05,z); } for(let i=0;i<40;i++){ frame(); await new Promise(r=>setTimeout(r,25)); } return ui('fps').textContent; })()")
    ok('peor' in r and ' ms' in r, 'el medidor enseña el peor cuadro: «%s»'%r)
    # 3. las olas ya no se rehacen cada segundo
    r=await ev("""(async()=>{ let mk=0; const om=swMake; swMake=function(c,n){ mk++; return om(c,n); }; for(let i=0;i<30;i++){ swellTick(); await new Promise(r=>setTimeout(r,30)); } const a=mk;
      for(let i=0;i<120;i++){ swellTick(); await new Promise(r=>setTimeout(r,25)); } swMake=om; return [a, mk-a, SWELL.all.length, SWELL.map.size]; })()""")
    ok(r[1]<=150 and r[2]>50, 'olas: en ~3 s solo se hacen las nuevas (%s; antes ~90 por segundo); hay %s en el mar'%(r[1],r[2]))
    # 4. coches, aviones y bichitos no se juntan con lo de alrededor
    r=await ev("""(()=>{ const D=acDynRoots(); let inW=0, n=0; for(const b of BATCH.batches){ if(b.local) continue; for(const o of b.src||[]){ let q=o; while(q && q.parent!==scene) q=q.parent; if(q && D.has(q)) inW++; } }
      for(const c of cars){ c.root.traverse(o=>{ if(o.isMesh && BATCH.recs.get(o)) n++; }); } return [inW, n, BATCH.batches.size]; })()""")
    ok(r[0]==0 and r[1]>0 and r[2]>80, 'ningún coche/avión/bichito quedó junto con lo de su alrededor (%s piezas de coches vigiladas, %s grupos)'%(r[1],r[2]))
    # 5. lo que se mueve: la zona apagada sigue al coche con su posición
    r=await ev("""(()=>{ const c=cars[0].root, it=AREA.list.find(q=>q[0]===c); if(!it) return null; c.userData._areaDyn=true; areaCullBegin(); areaCullEnd(); const c0=it[1].center.clone(), p0=c.position.clone();
      c.position.x+=7; areaCullBegin(); areaCullEnd(); const d=+(it[1].center.x-c0.x).toFixed(2); c.position.copy(p0); areaCullBegin(); areaCullEnd(); return [d, !!it[2]]; })()""")
    ok(r and abs(r[0]-7)<.01, 'un coche que se mueve: su zona lo sigue con su posición %s'%r)
    # 6. grupos vacíos: lista simple, se apagan y se prenden
    r=await ev("""(async()=>{ const m=IZERO.L.find(o=>o.parent && o.count===0); if(!m) return null; for(let i=0;i<8;i++) izeroTick(); const off=!(m.layers.mask&1); m.count=1; for(let i=0;i<4;i++) izeroTick(); const on=!!(m.layers.mask&1); m.count=0; for(let i=0;i<4;i++) izeroTick(); return [IZERO.L.length, off, on, !(m.layers.mask&1), new Set(IZERO.L).size===IZERO.L.length]; })()""")
    ok(r and r[1] and r[2] and r[3] and r[4], 'grupos vacíos: %s en la lista (sin repetidos); uno vacío no se dibuja y al tener copias vuelve en 4 cuadros %s'%(r and r[0], r))
    # 7. al caminar los árboles se acomodan de a poco, pero todos
    r=await ev("""(async()=>{ const T=MAP.trees[40]; { const x=T[0]+5, z=T[1]+5; player.pos.set(x,groundAt(x,z,99)+.05,z); } let n=0, part=0; for(let i=0;i<80 && (n<12 || ICULL.q<ICULL.L.length);i++){ __S(1); n++; if(ICULL.q<ICULL.L.length) part++; }
      let hit=false; for(const R of ICULL.L){ const m=R.m; if(m.material!==trunkMat) continue; for(let k=0;k<m.count;k++){ const a=m.instanceMatrix.array; if(Math.abs(a[k*16+12]-T[0])<.01 && Math.abs(a[k*16+14]-T[1])<.01) hit=true; } } return [n, ICULL.q===ICULL.L.length, hit, part]; })()""")
    ok(r[1] and r[2], 'al llegar caminando, todos los grupos quedan acomodados (%s cuadros a medias de %s) y el árbol de junto se dibuja %s'%(r[3],r[0],r))
    # 8. la lista de piezas lejanas se arma de a poco
    r=await ev("(async()=>{ LEJOS.ts=-1e9; let k=0; for(;k<40;k++){ renderer.render(scene,camera); if(!LEJOS.scanning && k>0) break; } return [k, LEJOS.L.length]; })()")
    ok(r[0]>=2 and r[1]>200, 'la lista de piezas lejanas se arma en %s cuadros (%s piezas)'%(r[0],r[1]))
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close()
    ctx,pg,errs,ev=await open_page(NORMAL)
    r=await ev("(async()=>{ startGame(); player.pos.set(START.x,START.top+.05,START.z); await __W(5); return [BATCH.batches.size, ICULL.q===ICULL.L.length, LEJOS.L.length>100]; })()")
    ok(r[0]>50 and r[1] and r[2], 'calidad Baja: todo trabaja igual %s'%r)
    ok(not errs,'sin errores (calidad Baja) %s'%errs[:3]); await ctx.close()
    await b.close()
asyncio.run(m())
