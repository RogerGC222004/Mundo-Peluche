# v277: arreglos de lo que encontró Roger: agua del lago del castillo, estanque de la montaña redondo, caminos sin pasto encima, piernas tras el camello, camello se queda donde te bajas, sin tirón al mojarte, Cubito con arco, ojitos en la curva de la cabeza, idioma
import asyncio, sys, os
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open(os.environ.get('JUEGO','/home/claude/mundo-peluche.html')).read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":780,"height":360}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false}));")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(800)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t)
    await ev("window.__run=(sec)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); update(.05,t); } }; startGame(); 1"); await pg.wait_for_timeout(1200); await ev("__run(1); 1")
    # 8. ojitos: cada ojo queda pegado a la curva de su cabeza y mirando hacia afuera de ella; la pata ya tiene dos ojos
    r=await ev("""(()=>{ const res={}, chk=(lab,root)=>{ root.updateMatrixWorld(true); const E=GOOGLY.list.filter(e=>{ let q=e.g; while(q){ if(q===root) return true; q=q.parent; } return false; }); let worst=0, wd=1;
        for(const e of E){ const F=gFit(root,e.g.parent,...e.g.position.toArray(),e.r,new THREE.Vector3(0,0,1).applyQuaternion(e.g.quaternion),null); if(!F) continue;
          const lp=e.g.position, dd=lp.distanceTo(F.p)/e.r, dot=F.d.dot(new THREE.Vector3(0,0,1).applyQuaternion(e.g.quaternion)); worst=Math.max(worst,dd); wd=Math.min(wd,dot); }
        res[lab]=[E.length, +worst.toFixed(2), +wd.toFixed(2)]; };
      for(const k of Object.keys(DESA_EYE)){ const A=desAnimalSpawn(k,0,0); A.g.position.set(-2600,160,-2600); chk('d_'+k,A.g); }
      for(const k of Object.keys(FORA_EYE)){ const A=forAnimalSpawn(k,0,0,0); A.g.position.set(-2600,160,-2600); chk('b_'+k,A.g); }
      for(const sp of PETS.slice(0,6)){ const P=buildPet(sp); chk('m_'+sp.id,P.root); }
      if(!GRN.built) grnBuild(); const pata=GRN.ducks.map(D=>{ const E=GOOGLY.list.filter(e=>e.g.parent===D.o); return E.length===2?+E[0].g.position.distanceTo(E[1].g.position).toFixed(3):0; });
      return JSON.stringify({res, pata, cache:GFIT.size}); })()""")
    import json as _j; d=_j.loads(r); R=d['res']
    ok(all(v[0]>=2 for v in R.values()), 'todos los animalitos revisados tienen sus dos ojitos (%d tipos)'%len(R))
    ok(all(v[1]<.25 and v[2]>.97 for v in R.values()), 'cada ojito está sobre la curva de su cabeza y mirando hacia afuera de ella %s'%{k:v for k,v in R.items() if not(v[1]<.25 and v[2]>.97)})
    ok(len(d['pata'])==6 and all(x>.08 for x in d['pata']), 'la pata y sus patitos ya tienen dos ojos separados (antes uno encima del otro) %s'%d['pata'][:6])
    # 9. idioma: al pasar a inglés y regresar a español, todos los botones regresan a español
    r=await ev("""(async()=>{ const T=()=>new Promise(r=>setTimeout(r,150)); const snap=()=>[...document.querySelectorAll('button')].map(b=>b.textContent.trim()).filter(t=>t);
      const es0=snap(); I18N.set('en'); await T(); const en=snap(); I18N.set('es'); await T(); const es1=snap(); const bad=[]; es1.forEach((t,i)=>{ if(t!==es0[i]) bad.push([es0[i],t]); });
      const chg=en.filter((t,i)=>t!==es0[i]).length; return JSON.stringify([es0.length, chg, bad.slice(0,8)]); })()""")
    d=_j.loads(r)
    ok(d[1]>20 and len(d[2])==0, 'al cambiar de idioma y regresar, ningún botón se queda en inglés (%d botones, %d cambian) %s'%(d[0],d[1],d[2]))
    # 1. el lago del castillo tiene agua que se ve: la profundidad está bien orientada (antes x y z se cruzaban y salía casi todo «seco»)
    r=await ev("""(()=>{ const N=64, d=depthTexture(N,LAKE.x,LAKE.z,LAKE.R,WATER_Y,false), a=d.tex.image.data; let bad=0, deep=0; const st=2*LAKE.R/N;
      for(let j=0;j<N;j+=4) for(let i=0;i<N;i+=4){ const x=LAKE.x-LAKE.R+st*(i+.5), z=LAKE.z-LAKE.R+st*(j+.5), wet=terrainH(x,z)<WATER_Y-.4, v=a[j*N+i]; if(wet && v>0) deep++; if(wet && v===0) bad++; }
      return [deep,bad]; })()""")
    ok(r[0]>20 and r[1]<=r[0]*.05, 'el lago del castillo marca agua donde de verdad hay agua %s'%r)
    # 2. el estanque de la montaña es redondo y completo (antes medio estanque quedaba a ras del pasto)
    r=await ev("""(()=>{ const P=RL_POND, out=[]; for(let k=0;k<16;k++){ const a=k/16*6.283, x=P.x+Math.cos(a)*P.R*.6, z=P.z+Math.sin(a)*P.R*.6; out.push(+(P.lvl-terrainH(x,z)).toFixed(2)); } return [!!RLP_CARVE, out]; })()""")
    ok(r[0] and min(r[1])>.3, 'el estanque de la montaña tiene agua en toda la vuelta %s'%r[1])
    # 3. caminos: el pasto ya no se asoma por encima del camino (se mide en el centro y en las orillas de cada tramo)
    r=await ev("""(()=>{ let worst=9, n=0; for(const o of scene.children){ if(!o.isMesh || !o.material || !o.material.polygonOffset || o.material.polygonOffsetFactor!==-2 || o.material.polygonOffsetUnits!==-4 || !o.geometry.index) continue;
        const p=o.geometry.attributes.position, ix=o.geometry.index; for(let t=0;t<ix.count;t+=3){ const a=ix.getX(t), b=ix.getX(t+1), c=ix.getX(t+2);
          for(const [wa,wb,wc] of [[1/3,1/3,1/3],[.5,.5,0],[0,.5,.5],[.5,0,.5]]){ const x=p.getX(a)*wa+p.getX(b)*wb+p.getX(c)*wc, y=p.getY(a)*wa+p.getY(b)*wb+p.getY(c)*wc, z=p.getZ(a)*wa+p.getZ(b)*wb+p.getZ(c)*wc; worst=Math.min(worst,y-terrainH(x,z)); n++; } } }
      return [n,+worst.toFixed(3)]; })()""")
    ok(r[0]>1000 and r[1]>-.02, 'el camino queda encima del pasto en todos lados (%s puntos, lo más bajo %s m)'%(r[0],r[1]))
    # 4 y 5. camello: al bajarte las piernas regresan a su lugar; el camello se queda donde te bajaste; si te alejas mucho vuelve a su casa
    r=await ev("""(()=>{ const K=DES.camel, h0=[K.x,K.z]; arWarp(K.x+1.5,groundAt(K.x+1.5,K.z,999)+.1,K.z,0); __run(.5); desCamelStart(); __run(1); keys['KeyW']=true; __run(3); keys['KeyW']=false; __run(.2);
      const S=player.pg.cm, at=[S.x,S.z]; stopPlay(); __run(1.2); const legs=plush.userData.legs.map(l=>Math.abs(l.rotation.z)).reduce((a,b)=>Math.max(a,b),0);
      const moved=Math.hypot(K.x-h0[0],K.z-h0[1]), stay=Math.hypot(K.x-at[0],K.z-at[1]), obOk=Math.hypot(K.ob.x-K.x,K.ob.z-K.z)<.01;
      arWarp(K.home.x+200,groundAt(K.home.x+200,K.home.z,999)+.1,K.home.z,0); __run(.5); const back=Math.hypot(K.x-K.home.x,K.z-K.home.z);
      return [+legs.toFixed(3), +moved.toFixed(1), +stay.toFixed(2), obOk, +back.toFixed(2)]; })()""")
    ok(r[0]<.01, 'al bajarte del camello las piernas se cierran (%s)'%r[0])
    ok(r[1]>3 and r[2]<.5 and r[3], 'el camello se queda donde te bajaste (se movió %s m, quedó a %s m de ti)'%(r[1],r[2]))
    ok(r[4]<.01, 'si te vas lejos, el camello regresa a su lugar (%s m)'%r[4])
    # 6. mojarte por primera vez no hace un tirón (no compila un dibujo nuevo)
    r=await ev("""(()=>{ const info=renderer.info; stClear(myStn); for(let i=0;i<10;i++){ update(.05,clock.elapsedTime+=.05); renderer.render(scene,camera); } const L=LAKE, sx=L.x, sz=L.z+L.R+6; arWarp(sx,groundAt(sx,sz,999)+.1,sz,0); for(let i=0;i<20;i++){ update(.05,clock.elapsedTime+=.05); renderer.render(scene,camera); }
      const p0=info.programs.length; yaw=0; player.facing=Math.PI; keys['KeyW']=true; let on=false; for(let i=0;i<70;i++){ update(.05,clock.elapsedTime+=.05); renderer.render(scene,camera); if(myStn.on) on=true; } keys['KeyW']=false; return [on, info.programs.length-p0]; })()""")
    ok(r[0] and r[1]==0, 'al meterte al agua te mojas sin compilar nada nuevo (sin tirón) %s'%r)
    # 7. Cubito con arco: el brazo estirado al frente a la altura del hombro con el arco en la mano (antes el arco quedaba abajo, a la cintura, y el brazo doblado)
    r=await ev("""(()=>{ wardrobe.eq.body='av_cubo'; applyOutfit(plush,{...wardrobe.eq}); arWarp(0,groundAt(0,40,999)+.1,40,0); if(!bowHeld()) useSlot(1); hook.mode=0; yaw=Math.PI; pitch=0; __run(.6); plush.updateMatrixWorld(true);
      const arm=plush.userData.arms.find(a=>a.userData.side===BOW_SIDE), j=arm.userData.joint, rg=plush.userData.bowRig, W=o=>o.getWorldPosition(new THREE.Vector3()), L=v=>plush.worldToLocal(v.clone());
      const grip=rg.bow.localToWorld(new THREE.Vector3(0,0,.42)), sh=W(arm), el=W(j), out=[+(L(grip).z).toFixed(2), +grip.distanceTo(sh).toFixed(2), +(L(el).z-L(sh).z).toFixed(2)];
      hook.mode=0; bowShoot(); const st=hook.pos.distanceTo(grip); out.push(+st.toFixed(2)); bowRelease(true); delete wardrobe.eq.body; applyOutfit(plush,{...wardrobe.eq}); __run(.3); return out; })()""")
    ok(r[0]>.6 and r[1]>.7 and r[2]>0 and r[3]<.6, 'Cubito con arco: brazo estirado al frente a la altura del hombro, codo hacia adelante y la flecha sale del arco %s'%r)
    print('errores', len(errs)); [print('  E:',e[:300]) for e in dict.fromkeys(errs)]
    await b.close()
asyncio.run(m())
