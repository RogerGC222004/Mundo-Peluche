# v201 (revisión final): menos detalle de lejos. Frijolito: cuerpo con boquita más ligero (72 col · 48+40 hileras) y, a más de 11 m,
# frijol liso + calcomanía sencilla; la sombrita de la boca no hace sombra. Chibi con boca 3D: cabeza 80×60 y, de lejos, la redonda normal.
# La lengua de lejos usa el frijol liso y su malla se rehace 1 de cada 3 cuadros. Regresa a lo detallado a menos de 9.5 m.
import asyncio, sys
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":844,"height":390}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("""localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');""")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(800)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    run="(sec,fn)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); if(fn) fn(i); update(.05,t); } }"
    await ev("window.__run="+run+"; startGame(); 1"); await pg.wait_for_timeout(1200); await ev("(window.requestAnimationFrame=()=>0, __run(1), 1)")
    # 1. cuántos triangulitos
    r=await ev("(()=>{ const t=g=>g.index.count/3; return [t(fjBodyGeo()), t(fjBodyGeoLo()), t(fjBodyGeoOpen()), t(fjCreaseGeo()), t(fjCreaseGeo(true)), t(chHeadGeo3('risa')), t(chGeos().head), plush.userData.crease.castShadow]; })()")
    ok(r[0]<=13000 and r[1]<=3000 and r[2]<=13000 and r[4]<=900 and r[5]<=10000 and r[7] is False, 'triangulitos: cuerpo %d (antes 24800), lejos %d, abierto %d, sombrita %d / lejos %d, cabeza Chibi boca 3D %d (antes 30800), redonda %d; la sombrita no hace sombra'%tuple(r[:7]))
    # 2. tu peluche (cerca de la cámara) se queda con lo detallado
    r=await ev("(()=>{ const u=plush.userData; return [u.lodFar, u.body.geometry===fjBodyGeo(), u.crease.geometry===fjCreaseGeo(false), +plush.getWorldPosition(new THREE.Vector3()).distanceTo(camera.position).toFixed(1)]; })()")
    ok(r[0] is False and r[1] and r[2], 'tu peluche (a %s m de la cámara) lleva todo el detalle %s'%(r[3],r[:3]))
    # 3. otro frijolito: lejos → sencillo; a 10 m sigue igual (no parpadea); a 9 m regresa lo detallado
    put="(o,d)=>{ const v=new THREE.Vector3(); camera.getWorldDirection(v); v.y=0; v.normalize(); const p=camera.position.clone().addScaledVector(v,d); p.y=camera.position.y; o.position.copy(p); o.updateMatrixWorld(true); plushLod(o); const u=o.userData; return [u.lodFar, u.body.geometry===FJ_GEO.lo, u.crease.geometry===fjCreaseGeo(true)]; }"
    r=await ev("(()=>{ window.__put="+put+"; const o=window.__o=makePlush(2); scene.add(o); return [__put(o,15), __put(o,10), __put(o,9), __put(o,10.5), __put(o,12)]; })()")
    ok(r==[[True,True,True],[True,True,True],[False,False,False],[False,False,False],[True,True,True]], 'otro frijolito: a 15 m sencillo, a 10 m sigue sencillo, a 9 m detallado, a 10.5 m sigue detallado, a 12 m sencillo %s'%r)
    # 4. Chibi con boca 3D (risa): de lejos cabeza redonda con el mismo hueco por pixel
    r=await ev("""(()=>{ const o=window.__c=makePlush(1); scene.add(o); applyOutfit(o,{body:'av_chibi',chair:'hp_largo',cmouth:'bo_risa'}); const C=o.userData.ch, h=C.skinned[1];
      const a=[__put(o,6)[0], h.geometry===chHeadGeo3('risa'), h.material.customProgramCacheKey()]; const b=[__put(o,20)[0], h.geometry===chGeos().head, h.material.customProgramCacheKey(), !!C.m3 && C.m3.visible!==false]; const c=[__put(o,7)[0], h.geometry===chHeadGeo3('risa')]; return [a,b,c]; })()""")
    ok(r==[[False,True,'chMouth3'],[True,True,'chMouth3',True],[False,True]], 'Chibi con boca 3D: cerca cabeza detallada, lejos la redonda (mismo hueco y boquita adentro), y regresa %s'%r)
    # 5. la lengua de lejos: frijol liso con hueco; la malla se rehace 1 de cada 3 cuadros; al acercarse vuelve la boca abierta detallada
    r=await ev("""(()=>{ const o=window.__o; __put(o,16); tongueSet(o,true); let n=0; const g0=o.userData.body.geometry; const pos=()=>o.userData.tg&&o.userData.tg.mesh.geometry.attributes.position.version;
      for(let i=0;i<40;i++){ plushLod(o); tongueTick(o,.05,false); } const tg=o.userData.tg, v0=pos(); for(let i=0;i<9;i++){ plushLod(o); tongueTick(o,.016,false); } const dv=pos()-v0;
      const far=[o.userData.body.geometry===FJ_GEO.lo, tg.e===1, tg.mesh.visible, dv];
      __put(o,5); for(let i=0;i<3;i++){ plushLod(o); tongueTick(o,.05,false); } const near=[o.userData.body.geometry===FJ_GEO.open, o.userData.body.material.customProgramCacheKey().startsWith('fjMouth')];
      tongueSet(o,false); for(let i=0;i<40;i++){ plushLod(o); tongueTick(o,.05,false); } const back=[!o.userData.tg, o.userData.body.geometry===fjBodyGeo(), o.userData.crease.visible];
      return [far, near, back]; })()""")
    ok(r[0][:3]==[True,True,True] and 2<=r[0][3]<=4 and r[1]==[True,True] and r[2]==[True,True,True], 'lengua de lejos: frijol liso con hueco y malla 1 de cada 3 cuadros (%d de 9); de cerca boca abierta detallada; al guardarla todo vuelve %s'%(r[0][3],r))
    # 6. un jugador de verdad (presencia) lejos usa lo sencillo
    r=await ev("""(()=>{ const me={peer:'yo', sameTab:true, presence:{}}, q=camera.position, pr={n:'Ana',c:1,p:[+(q.x+25).toFixed(2),+(groundAt(q.x+25,q.z,99)).toFixed(2),+q.z.toFixed(2)],id:'abc123',rm:''};
      onPeers({peers:[me,{peer:'p1',kind:'viewer',presence:pr}]}); for(let i=0;i<20;i++) updateRemotes(.05,clock.elapsedTime+i*.05); const r=[...mp.remotes.values()][0]; return r?[r.obj.userData.lodFar, r.obj.userData.body.geometry===FJ_GEO.lo]:['sin remoto']; })()""")
    ok(r==[True,True], 'otro jugador a 25 m: su frijolito va sencillo %s'%r)
    # 7. dibujar 6 peluches (3 frijolitos, 3 Chibis con boca 3D) cerca y lejos
    r=await ev("""(()=>{ [window.__o,window.__c].forEach(o=>scene.remove(o)); const rs=[]; for(let i=0;i<6;i++){ const o=makePlush(i); scene.add(o); if(i%2) applyOutfit(o,{body:'av_chibi',chair:'hp_largo',cmouth:'bo_risa'}); rs.push(o); }
      const v=new THREE.Vector3(); camera.getWorldDirection(v); v.y=0; v.normalize(); const sd=new THREE.Vector3(-v.z,0,v.x);
      const at=(d)=>{ rs.forEach((o,i)=>{ const p=camera.position.clone().addScaledVector(v,d).addScaledVector(sd,(i-2.5)*1.2); p.y=groundAt(p.x,p.z,99); o.position.copy(p); o.rotation.y=Math.atan2(-v.x,-v.z); o.updateMatrixWorld(true); plushLod(o); });
        renderer.info.reset(); renderer.render(scene,camera); return Math.round(renderer.info.render.triangles/1000); };
      rs.forEach(o=>o.visible=false); renderer.info.reset(); renderer.render(scene,camera); const base=Math.round(renderer.info.render.triangles/1000); rs.forEach(o=>o.visible=true);
      const c=at(7)-base, l=at(16)-base; rs.forEach(o=>scene.remove(o)); return [c,l]; })()""")
    ok(r[0]>0 and r[1]<r[0], '6 peluches: cerca +%dk triangulitos, lejos +%dk (antes de la revisión: cerca +245k)'%(r[0],r[1]))
    ok(not errs,'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
