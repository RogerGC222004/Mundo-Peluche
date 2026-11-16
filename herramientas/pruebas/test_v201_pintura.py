# v201 parte 6: globos de pintura: vuelan en arco, revientan en suelo/pared dejando su dibujo, en el agua no, máximo 16 manchas, y se ven en los demás.
import asyncio, sys
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":844,"height":390}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false}));")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(800)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t)
    await ev("window.__run=(sec)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); update(.05,t); } }; startGame(); 1"); await pg.wait_for_timeout(1200); await ev("__run(1); 1")
    r=await ev("(()=>{ throwPaint('estrella'); const a=PBALL.fly.length, pr=paintPresence(); __run(.1); const y1=PBALL.fly[0]&&PBALL.fly[0].p.y; __run(2.5); return [a, Array.isArray(pr)&&pr.length===8, PBALL.fly.length, PBALL.splats.length, plush.userData.gs?plush.userData.gs.id:'' ]; })()")
    ok(r[0]==1 and r[1] and r[2]==0 and r[3]==1,'lanzar: sale el globo, va en la presencia, cae y deja su mancha %s'%r)
    r=await ev("(()=>{ paintLaunch('estrella', player.pos.clone().add(new THREE.Vector3(0,1.4,0)), new THREE.Vector3(.3,-1,.2), true); __run(1); const s=PBALL.splats[PBALL.splats.length-1]; const n=new THREE.Vector3(0,0,1).applyQuaternion(s.m.quaternion); return [+n.y.toFixed(2), +(s.m.position.y-groundAt(s.m.position.x,s.m.position.z,s.m.position.y+.5)).toFixed(3), s.m.material===PBALL.mat.estrella]; })()")
    ok(r[0]>.8 and 0<r[1]<.06 and r[2],'en el suelo queda acostada y pegadita %s'%r)
    # contra una pared: un obstáculo justo enfrente
    r=await ev("(()=>{ const o={x:player.pos.x, z:player.pos.z+3, r:1, top:player.pos.y+5}; obstacles.push(o); paintLaunch('flor', player.pos.clone().add(new THREE.Vector3(0,1.4,.5)), new THREE.Vector3(0,1,9), true); __run(1); const s=PBALL.splats[PBALL.splats.length-1]; const n=new THREE.Vector3(0,0,1).applyQuaternion(s.m.quaternion); obstacles.splice(obstacles.indexOf(o),1); return [s.m.material===PBALL.mat.flor, +n.z.toFixed(2), +Math.abs(n.y).toFixed(2), +(s.m.position.z-(o.z-o.r)).toFixed(2)]; })()")
    ok(r[0] and r[1]<-.9 and r[2]<.1 and abs(r[3])<.1,'contra una pared queda parada en la pared %s'%r)
    r=await ev("(()=>{ const n0=PBALL.splats.length; paintLaunch('luna', new THREE.Vector3(1200,4,1200), new THREE.Vector3(0,0,1), true); __run(1.5); return [PBALL.splats.length-n0, PBALL.fly.length]; })()")
    ok(r==[0,0],'en el mar no deja mancha %s'%r)
    r=await ev("(()=>{ for(let i=0;i<20;i++){ paintLaunch('rayo', player.pos.clone().add(new THREE.Vector3(i*.3-3,1.5,0)), new THREE.Vector3(0,2,2), true); } __run(1.5); return PBALL.splats.length; })()")
    ok(r==16,'máximo 16 manchas a la vez: %s'%r)
    # otro jugador lanza
    r=await ev("(()=>{ const rr=makeRemote(1,'Ana'); rr.pos.copy(player.pos); paintParse(rr,{}); const n0=PBALL.fly.length; paintParse(rr,{pb:[4,777,Math.round(player.pos.x*100),Math.round((player.pos.y+1.5)*100),Math.round(player.pos.z*100),0,150,900]}); const a=PBALL.fly.length-n0; paintParse(rr,{pb:[4,777,0,0,0,0,0,0]}); const b=PBALL.fly.length-n0; paintParse(rr,{pb:[4,778,999900,0,0,0,0,0]}); const c=PBALL.fly.length-n0; return [a,b,c, PBALL.fly[PBALL.fly.length-1].id]; })()")
    ok(r==[1,1,1,'corazon'],'se ve el globo de otro jugador (una vez; si viene de lejos no) %s'%r)
    r=await ev("(()=>{ player.swim=true; const n0=PBALL.fly.length; PBALL.last=0; throwPaint('flor'); const a=PBALL.fly.length-n0; player.swim=false; return a; })()"); ok(r==0,'nadando no se lanza')
    try: await ev("(()=>{ yaw=player.facing+Math.PI; pitch=-.35; __run(.2); return 1; })()"); await pg.screenshot(path=OUT+'/pintura_juego.png', timeout=90000)
    except Exception as e: print('(sin foto)', str(e)[:60])
    print('errores', errs[:3]); await b.close()
asyncio.run(m())
