# v201 parte 5: sacar la lengua (solo frijolito): abre poco a poco, física, no atraviesa el cuerpo, cámara fija gira la cabeza, se ve en los demás.
import asyncio, sys
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":844,"height":390}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("""if(!sessionStorage.getItem('ya')){ sessionStorage.setItem('ya','1'); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');
      localStorage.setItem('mundoPelucheRopa', JSON.stringify({own:['ge_lengua'],eq:{},gest:['saludar','lengua'],pint:['estrella']})); }""")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(800)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t)
    run="(sec,fn)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); if(fn) fn(i); update(.05,t); } }"
    await ev("window.__run="+run+"; startGame(); 1"); await pg.wait_for_timeout(1200); await ev("__run(1); 1")
    r=await ev("(()=>{ playGesture('lengua'); __run(.2); const tg=plush.userData.tg; return [!!tg, +tg.o.toFixed(2), +tg.e.toFixed(2), plush.userData.body.geometry===FJ_GEO.open]; })()")
    ok(r[0] and 0<r[1]<1 and r[2]==0 and r[3],'la boca se abre poco a poco y la lengua todavía no sale %s'%r)
    r=await ev("(()=>{ __run(1.2); const tg=plush.userData.tg; return [tg.o, tg.e, tg.mesh.visible, gestPresence().startsWith('2.'), ui('camFixChip').hidden]; })()")
    ok(r==[1,1,True,True,True],'luego sale toda; va en la presencia; ya no sale «Fijar cámara» (v203) %s'%r)
    try: await pg.screenshot(path=OUT+'/lengua_juego.png', timeout=90000)
    except Exception as e: print('(sin foto)', str(e)[:60])
    # caminar y saltar con la lengua afuera: se queda, se mueve y no atraviesa el cuerpo
    ins="(()=>{ const o=plush, tg=o.userData.tg, b=o.userData.body, p=tg.mesh.geometry.attributes.position, v=new THREE.Vector3(), M=FJ_MOUTH_OPEN; let bad=0; for(let i=0;i<p.count;i++){ v.fromBufferAttribute(p,i); o.localToWorld(v); b.worldToLocal(v); if(v.y<.02||v.y>1.66) continue; const R=fjR(v.y); if(mouthSD(M,Math.atan2(v.x,v.z)*R,v.y-M.Y)<.012) continue; if(Math.hypot(v.x,v.z)-R< -0.003) bad++; } return bad; })()"
    r=await ev("(()=>{ const tip0=plush.userData.tg.pts[11].clone(); let worst=0, moved=0; keys.KeyW=true; try{ __run(1.5,()=>{ worst=Math.max(worst,"+ins+"); }); }finally{ keys.KeyW=false; } keys.Space=true; __run(.1); keys.Space=false; __run(1.2,()=>{ worst=Math.max(worst,"+ins+"); }); return [!!plush.userData.tg && plush.userData.tg.want===1, worst]; })()")
    ok(r==[True,0],'caminando y saltando la lengua sigue afuera y no atraviesa el cuerpo %s'%r)
    # v203: sin cámara fija: mover la cámara mueve la cámara (como siempre)
    r=await ev("(()=>{ const y0=yaw; look(-100,0,.005); __run(.3); return [TGCAM.on, yaw!==y0, ui('camFixChip').hidden]; })()"); ok(r==[False,True,True],'con la lengua afuera la cámara se mueve normal %s'%r)
    r=await ev("(()=>{ playGesture('lengua'); __run(.3); const a=plush.userData.tg && plush.userData.tg.e<1; __run(1.5); return [a, !plush.userData.tg, plush.userData.body.geometry===fjBodyGeo(), plush.userData.body.material.userData.plush===true, plush.userData.crease.visible, ui('camFixChip').hidden, gestPresence()===undefined]; })()")
    ok(r==[True,True,True,True,True,True,True],'al guardarla entra poco a poco y todo vuelve a como estaba %s'%r)
    # nadar la guarda; otro gesto la guarda
    r=await ev("(()=>{ playGesture('lengua'); __run(1.5); player.busy=true; __run(1.5); const a=!plush.userData.tg; player.busy=false; __run(.3); playGesture('lengua'); __run(1.5); playGesture('saludar'); __run(1.2); return [a, !plush.userData.tg || plush.userData.tg.want===0]; })()")
    ok(r==[True,True],'si no puedes (ocupado, nadando, vehículo…) o haces otro gesto, la lengua se guarda %s'%r)
    # cambiar de color de peluche con la lengua afuera: sigue el hueco
    r=await ev("(()=>{ __run(1.5); playGesture('lengua'); __run(1.5); recolor(plush,3); __run(.2); const tg=plush.userData.tg; return [tg.base===plushMatFor(3), plush.userData.body.material===tg.mat]; })()")
    ok(r==[True,True],'si cambias de color con la lengua afuera, la boca sigue abierta %s'%r)
    # otro jugador
    r=await ev("(()=>{ const rr=makeRemote(1,'Ana'); scene.add(rr.obj); gestParse(rr,{ge:'2.123',hd:[50,-10]}); for(let i=0;i<40;i++) tongueTick(rr.obj,.05,false); const tg=rr.obj.userData.tg; const a=[!!tg, tg.e, +tg.hy.toFixed(2)]; gestParse(rr,{}); for(let i=0;i<40;i++) tongueTick(rr.obj,.05,false); return [a, !rr.obj.userData.tg]; })()")
    ok(r[0][0] and r[0][1]==1 and abs(r[0][2]-.5)<.02 and r[1],'otro jugador: le sale la lengua, gira la cabeza como él y la guarda %s'%r)
    r=await ev("(()=>{ wardrobe.eq.body='av_chibi'; applyOutfit(plush,wardrobe.eq); __run(.1); const gone=!plush.userData.tg; playGesture('lengua'); return [gone && !plush.userData.tg, gwItems('gest').map(i=>i.gest).includes('lengua')]; })()")
    ok(r==[True,False],'el Chibi no saca la lengua (ni sale en su ruedita) %s'%r)
    print('errores', errs[:3]); await b.close()
asyncio.run(m())
