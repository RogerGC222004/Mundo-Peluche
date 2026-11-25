# v264: minijuegos desde el menú (Tú solo, CPU o Jugadores; al terminar regresas a la lista), modo solo con récord en 7 minijuegos,
# el Modo libre ya no empieza en el mar, y el Chibi y el Cubito parpadean y descansan (mecen los brazos y voltean).
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

    # 1. el menú de minijuegos: sin internet también; Tú solo en los que tiene sentido, CPU y Jugadores en todos
    r=await ev("""(async()=>{ ONLINE.on=false; ui('mgBtn').click(); await new Promise(f=>setTimeout(f,300)); const cards=[...ui('mgqList').querySelectorAll('.mgq-g')];
      const o=cards.map(c=>[c.querySelector('b').textContent.trim(), [...c.querySelectorAll('.mgq-b')].map(b=>b.classList.contains('solo')?'S':b.classList.contains('cpu')?'C':'J').join('')]); return [ui('mgq').hidden, o, document.getElementById('onlineOv') ? document.getElementById('onlineOv').hidden : true]; })()""")
    solos=[x[0] for x in r[1] if x[1].startswith('S')]
    ok(not r[0] and r[2] and len(r[1])==14 and all(x[1] in ('SCJ','CJ') for x in r[1]), '1a «Minijuegos» abre la lista sin pedir internet; los 14 tienen CPU y Jugadores')
    ok(len(solos)==8 and all(any(n in s for s in solos) for n in ['Plataformas','Carrera','Laberinto','Banda','Canasta','Pinta','perlas','número']), '1b «Tú solo» en 8: %s'%solos)
    r=await ev("""(async()=>{ const c=[...ui('mgqList').querySelectorAll('.mgq-g')][1]; c.querySelector('.mgq-b.jug').click(); await new Promise(f=>setTimeout(f,300)); const ov=document.getElementById('onlineOv'); const o=[!!ov && !ov.hidden && /línea/.test(ov.textContent)]; if(ov) onlineClose(); return o; })()""")
    ok(r[0], '1c «Jugadores» pide que un adulto prenda «Jugar en línea» (si está apagado)')
    # 2. CPU desde el menú: escoges cuántos y la dificultad (sin «Solo yo»), y empieza en el minijuego
    r=await ev("""(async()=>{ mgqCpu(7); const o=[!cpuOv.hidden, ui('cpuSolo').hidden, ui('mgq').hidden]; ui('cpuCancel').click(); o.push(cpuOv.hidden, !ui('mgq').hidden, state);
      mgqCpu(7); CPU.pick.n=2; CPU.pick.d=0; ui('cpuGo').click(); await new Promise(f=>setTimeout(f,300)); o.push(state, CPU.on, CPU.a, cpuBots().length, AR.me.a, MENU_MG.a); return o; })()""")
    ok(r[:6]==[True,True,True,True,True,'menu'], '2a desde el menú, «CPU» abre cuántos y dificultad (sin «Solo yo»); «Cancelar» regresa a la lista %s'%r[:6])
    ok(r[6:]==['play',True,7,2,7,7], '2b «¡A jugar!» empieza Canasta de frutas contra 2 peluches de la CPU %s'%r[6:])
    await ev("""window.requestAnimationFrame=()=>0; window.__run=(sec)=>{ let t=clock.elapsedTime; for(let i=0;i<Math.round(sec/.05);i++){ clock.elapsedTime=(t+=.05); update(.05,t); } }; 1""")
    # 3. en el mapa, el letrero de la CPU ofrece «Solo yo» en los que tienen modo solo
    r=await ev("(()=>{ ui('toMenuBtn').click(); startGame(); const o=[]; for(const a of [0,1,4,7,NUMI]){ cpuOpen(a); o.push(!ui('cpuSolo').hidden); closeCpuOv(false); } return o; })()")
    ok(r==[True,False,True,True,True], '3 en el mapa, «Solo yo» sale en Plataformas, Laberinto, Canasta y ¡Al número!, no en Papa caliente %s'%r)
    # 4. tú solo en Canasta de frutas: no se acaba de inmediato (dura su tiempo)
    r=await ev("(()=>{ ui('toMenuBtn').click(); mgqLocal(7,0,1); __run(12); const G=AR.G[7]; const a=[G.ph, G.pl.length]; __run(3); return [a, G.ph, CPU.n]; })()")
    ok(r==[[3,1],3,0], '4 tú solo en Canasta de frutas: la partida sigue aunque seas el único (dura su tiempo) %s'%r)
    # 5. tú solo en Plataformas desde el menú: al caerte termina, sale tu récord y regresas a la lista de minijuegos
    r=await ev("""(()=>{ ui('toMenuBtn').click(); localStorage.removeItem('mundoPelucheSoloRec'); mgqLocal(0,0,1); __run(12); const G=AR.G[0]; const o=[G.ph]; __run(4); arOut(0,'test'); __run(.3);
      return [o[0], G.ph, ui('arResTitle').textContent, ui('arResText').textContent, JSON.parse(localStorage.getItem('mundoPelucheSoloRec')||'{}').plat>3000]; })()""")
    ok(r[0]==3 and r[1]==4 and r[2]=='¡Récord nuevo!' and 'Aguantaste' in r[3] and 'Récord' in r[3] and r[4], '5a tú solo en Plataformas: al quedar fuera se acaba y sale «%s» · %s'%(r[2],r[3]))
    await pg.wait_for_timeout(7000)
    r=await ev("[state, !ui('mgq').hidden, MENU_MG.a, AR.me.a, CPU.on]")
    ok(r==['menu',True,-1,-1,False], '5b al terminar regresas al menú, a la lista de minijuegos %s'%r)
    r=await ev("""(()=>{ mgqLocal(0,0,1); __run(12); __run(1); arOut(0,'test'); __run(.3); const t=[ui('arResTitle').textContent, ui('arResText').textContent]; ui('toMenuBtn').click(); return t; })()""")
    ok(r[0]=='¡Bien jugado!' and 'Récord' in r[1], '5c si no superas tu récord: «%s» · %s'%(r[0],r[1]))
    # 6. el Modo libre: la planicie se ve desde el principio
    r=await ev("(()=>{ freeEnter(); __run(.5); areaCullBegin(); const v=FREE.g.visible; areaCullEnd(); const o=[v, FREE.on]; ui('toMenuBtn').click(); return o; })()")
    ok(r==[True,True], '6 al entrar al Modo libre la planicie se ve de inmediato (ya no empiezas en el mar) %s'%r)
    # 7. el Chibi y el Cubito parpadean y, quietos, mecen los brazos y voltean
    for body,lab in [("{body:'av_chibi', ceyes:'co_cafe'}",'Chibi'),("{body:'av_cubo'}",'Cubito')]:
      r=await ev("""(()=>{ startGame(); wardrobe.eq=%s; applyOutfit(plush,wardrobe.eq); const u=plush.userData, C=u.av==='c'?u.ch:u.cb; const mats=new Set(), angs=[]; let armMax=0;
        player.vel.set(0,0,0); for(let i=0;i<240;i++){ __run(.05); mats.add(C.face.material); angs.push(u.lf?u.lf.ang:0); armMax=Math.max(armMax, Math.abs(u.arms[0].rotation.x)); }
        const turned=angs.some(a=>Math.abs(a)>.1); player.vel.set(4,0,0); __run(.3); const idle=u.lf.idle; ui('toMenuBtn').click(); return [u.av, mats.size, turned, +armMax.toFixed(3), idle]; })()"""%body)
      ok(r[1]>=3 and r[3]>.01 and r[4]<1, '7 el %s parpadea (%s caras distintas), voltea la cabeza o los ojos y mece los brazos al quedarse quieto; al moverse se le quita %s'%(lab,r[1],r))
    ok(not errs, 'sin errores (%s)'%errs[:3])
    await b.close()
asyncio.run(m())
