# v221: lo que todavía frenaba al Huawei de Roger era el procesador, no los dibujos. Ahora:
# (1) las piezas sueltas que quedan más allá de la niebla no se revisan al dibujar (LEJOS) y las zonas apagadas que no se
#     mueven tampoco recalculan sus piezas; (2) en ultra ligero los choques automáticos solo se arman cerca (200 m);
# (3) al cargar se juntan de una vez las piezas quietas (antes, en un teléfono lento, tardaba minutos y la feria
#     mandaba más de 300 dibujos); (4) el laberinto ya no recibe choques automáticos de más (error de la v220).
# Lo que se ve tiene que quedar igual.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
ROGER={"quality":"min","qDef":1,"ultra":True,"shadows":False,"weather":False,"fpsCap":"30","autoRes":False,"draw":30,"hints":False}
NORMAL={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateSky(.05); } };
  window.__D=()=>{ renderer.info.reset(); renderer.render(scene,camera); return [renderer.info.render.calls, renderer.info.render.triangles]; };
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
    # 1. al cargar ya está todo junto: la feria recién llegando no manda cientos de dibujos
    r=await ev("[BATCH.batches.size, window.__ldBatchMs, BATCH.warm]")
    ok(r[0]>80 and r[2] is True, 'al cargar se juntan las piezas quietas: %s grupos en %s ms (en mi compu)'%(r[0],r[1]))
    r=await ev("(()=>{ startGame(); { const x=FAIR.x+8, z=FAIR.z-FAIR.R-6; player.pos.set(x,groundAt(x,z,99)+.05,z); } player.facing=0; yaw=Math.PI; __S(8); return __D(); })()")
    ok(r[0]<160, 'en la feria, recién llegando: %s dibujos (antes de juntar al cargar, unos 250 en mi compu y más de 300 en el Huawei)'%r[0])
    # 2. lo que se ve queda igual con y sin esconder las piezas lejanas
    PLACES=[('castillo',"player.pos.set(START.x,START.top+.05,START.z); player.facing=Math.PI; yaw=0;"),
            ('feria',"{ const x=FAIR.x+8, z=FAIR.z-FAIR.R-6; player.pos.set(x,groundAt(x,z,99)+.05,z); } player.facing=0; yaw=Math.PI;"),
            ('playa',"{ const a=2.2, r=coastAtA(a)-6, x=Math.cos(a)*r, z=Math.sin(a)*r; player.pos.set(x,groundAt(x,z,99)+.05,z); player.facing=Math.atan2(-x,-z); yaw=player.facing+Math.PI; }")]
    for name,js in PLACES:
      await ev("(async()=>{ %s await __W(6); return 1; })()"%js)
      r=await ev("""(()=>{ const seen=()=>{ const S=new Set(), o=renderer.renderBufferDirect; renderer.renderBufferDirect=function(c,s,g,m,ob){ S.add(ob); return o.apply(this,arguments); }; renderer.render(scene,camera); renderer.renderBufferDirect=o; return S; };
        const vis0=new Map(scene.children.map(c=>[c,c.visible])); const a=seen(), hid=LEJOS.hid.length; const changed=scene.children.filter(c=>vis0.get(c)!==c.visible).length; const L=LEJOS.L; LEJOS.L=[]; LEJOS.tp=-1e9; const b=seen(); LEJOS.L=L; LEJOS.tp=-1e9; seen();
        const lost=[...b].filter(o=>!a.has(o)).map(o=>{ const g=o.geometry; if(!g.boundingSphere) g.computeBoundingSphere(); return +(g.boundingSphere.center.clone().applyMatrix4(o.matrixWorld).distanceTo(camera.position)-g.boundingSphere.radius*o.matrixWorld.getMaxScaleOnAxis()).toFixed(0); });
        const leak=scene.children.filter(c=>c._lj && !c.visible && !LEJOS.L.includes(c) ).length;
        return [hid, a.size, b.size, lost, LEJOS.offN, changed===0]; })()""")
      ok(r[0]>300 and all(d>40 for d in r[3]) and r[4]==0 and r[5], '%s: %s piezas lejanas no se revisan; se dibuja lo mismo (%s/%s; las que faltan estaban a %s m, detrás de la niebla) y después del dibujo vuelven a estar como estaban %s'%(name,r[0],r[1],r[2],r[3],r[4:]))
    # 3. una pieza lejana que se mueve cerca de ti se ve en el siguiente dibujo
    r=await ev("""(()=>{ const c=LEJOS.hid.find(o=>o.isMesh && (o.layers.mask&1) && !o.material.transparent && o.geometry && o.geometry.boundingSphere && o.geometry.boundingSphere.radius<3 && Math.abs(o.quaternion.w)>.999); if(!c) return null;
      const p0=c.position.clone(), cp=camera.position, fw=new THREE.Vector3(); camera.getWorldDirection(fw); const bc=c.geometry.boundingSphere.center;
      c.position.set(cp.x+fw.x*6-bc.x*c.scale.x, cp.y+fw.y*6-bc.y*c.scale.y, cp.z+fw.z*6-bc.z*c.scale.z);
      let drawn=false; const o=renderer.renderBufferDirect; renderer.renderBufferDirect=function(cc,s,g,m,ob){ if(ob===c) drawn=true; return o.apply(this,arguments); }; renderer.render(scene,camera); renderer.renderBufferDirect=o;
      const mw=c.matrixWorld.elements.slice(12,15).map(v=>+v.toFixed(1)), want=[c.position.x,c.position.y,c.position.z].map(v=>+v.toFixed(1)); c.position.copy(p0); renderer.render(scene,camera); return [drawn, JSON.stringify(mw)===JSON.stringify(want), c._lj.mv]; })()""")
    ok(r and r[0] and r[1] and r[2]>=1, 'una pieza lejana que se mueve frente a ti se dibuja al instante y ya no se esconde %s'%r)
    # 4. una zona apagada y quieta no recalcula sus piezas; si se mueve, sí
    r=await ev("""(()=>{ const z=AREA.list.map(it=>it[0]).find(c=>c.children.length>3 && !c.userData._areaDyn && c.parent===scene && c.position.distanceTo(camera.position)>200); if(!z) return null;
      renderer.render(scene,camera); renderer.render(scene,camera); const q1=z._acQuiet===undefined?null:true;
      areaCullBegin(); const off=AREA.off.includes(z), quiet=!!z._acQuiet; areaCullEnd();
      const p0=z.position.clone(); z.position.x+=1; renderer.render(scene,camera); const kid=z.children.find(k=>k.isMesh||k.children.length)||z.children[0]; const e=z.matrixWorld.elements[12]; z.position.copy(p0); renderer.render(scene,camera); renderer.render(scene,camera);
      return [off, quiet, +(e-p0.x).toFixed(2)]; })()""")
    ok(r and r[0] and r[1] and r[2]==1, 'una zona lejos y quieta se salta sus piezas; si se mueve, su posición se recalcula en ese mismo dibujo %s'%r)
    # 5. choques: el laberinto ya no recibe choques automáticos; en ultra ligero solo se arman cerca
    r=await ev("""(()=>{ const s=AC.seen.get(MZ.mesh), t=AC.seen.get(MZ.tops); return [MZ.mesh.userData.noCol===true, MZ.tops.userData.noCol===true, !s || !s.ok, !t || !t.ok, obstacles.filter(o=>!valleIn(o.x,o.z) && Math.hypot(o.x,o.z)<=coastMidR(Math.atan2(o.z,o.x))*1.02).length]; })()""")   # (v274: solo la isla de antes: sin la tierra nueva ni el valle)   # (v271: sin contar los árboles y rocas de la tierra nueva; v272: ni las cercas y cosas del valle, que se ponen a mano)
    ok(r[0] and r[1] and r[2] and r[3] and r[4]<7000, 'el laberinto ya no recibe choques automáticos (en la v220 eran 4 mil de más); choques en total: %s'%r[4])
    r=await ev("""(async()=>{ AC.t=-1e9; AC.list=null; AC.col=null; for(let i=0;i<400 && !AC.list;i++) acTick(); const L=AC.list||[], px=player.pos.x, pz=player.pos.z; const far=L.filter(o=>!o.isInstancedMesh && Math.hypot(o.matrixWorld.elements[12]-px,o.matrixWorld.elements[14]-pz)>205).length; return [L.length, far]; })()""")
    ok(r[0]>0 and r[1]==0, 'en ultra ligero los choques automáticos revisan solo lo de cerca (%s piezas, ninguna a más de 200 m)'%r[0])
    # 6. Modo libre: casi nada de la isla se revisa al dibujar
    r=await ev("(async()=>{ ui('toMenuBtn').click(); freeEnter(); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z); await __W(5); let n=0; areaCullBegin(); lejosBegin(); scene.traverseVisible(()=>n++); areaCullEnd(); return [n, ...__D()]; })()")
    ok(r[0]<1200 and r[2]<20000, 'Modo libre: al dibujar se recorren %s piezas (antes ~1800); %s dibujos, %s triángulos'%(r[0],r[1],r[2]))
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close()
    # 7. calidad Baja (sin ultra): también junta al cargar y esconde lo lejano; los choques revisan cerca y lejos como antes
    ctx,pg,errs,ev=await open_page(NORMAL)
    r=await ev("(async()=>{ startGame(); player.pos.set(START.x,START.top+.05,START.z); await __W(5); return [BATCH.warm, BATCH.batches.size>50, LEJOS.hid.length>200, ...__D()]; })()")
    ok(r[0] and r[1] and r[2], 'calidad Baja: se junta al cargar y lo lejano tampoco se revisa %s'%r)
    ok(not errs,'sin errores (calidad Baja) %s'%errs[:3]); await ctx.close()
    await b.close()
asyncio.run(m())
