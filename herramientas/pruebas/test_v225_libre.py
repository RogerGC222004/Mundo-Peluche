# v225 (Modo libre): la barra solo con íconos propios (sin emojis) y el texto de ayuda en su renglón; «Borrar todo» con
# confirmación (solo: todo; en una sala: solo lo tuyo); balón, imán, cañones, tubo, hielo y dulces rehechos; el dado rueda dando
# tumbos y cae en una cara; la gelatina tiembla al tocarla y se aplasta si estás encima.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); } };
  window.__CLR=()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); FREE.hold=null; freeSelect(null); };
  window.__AT=(x,z)=>{ player.pos.set(FREE.X+x,FREE.Y+.05,FREE.Z+z); player.vel.set(0,0,0); player.vy=0; player.facing=0; yaw=Math.PI; __S(3); }; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    for W,H,tag in [(780,360,'Huawei'),(876,393,'Doogee')]:
      ctx=await b.new_context(viewport={"width":W,"height":H}, has_touch=True, device_scale_factor=2); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
      await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
      async def route(r):
        if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
        elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
        else: await r.abort()
      await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
      ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300); await ev(STEP)
      # 1. la barra: solo íconos, el texto completo en su renglón y nada se encima
      r=await ev("""(async()=>{ freeEnter(); __CLR(); __AT(0,0); await new Promise(r=>setTimeout(r,500)); const ids=['freeObj','freeDel','freePaintB','freeEnvB','freeClear'];
        const txt=ids.map(id=>ui(id).textContent.trim()).join(''), svg=ids.every(id=>ui(id).querySelector('svg') && ui(id).title), emo=/\\p{Extended_Pictographic}/u.test(ui('freeHud').textContent);
        const T=ui('freeTxt'), tip=[T.textContent, getComputedStyle(T).display!=='none', T.scrollWidth<=T.clientWidth+1];
        const rect=id=>ui(id).getBoundingClientRect(), H=rect('freeHud'), C=rect('camChip'), K=rect('coinChip'); const legend=!ui('freeLegend').hidden && ui('freeLegend').children.length===5;
        freeSelect({k:'b',a:0,b:0}); freeRenderHud(); const t2=[T.textContent, T.scrollWidth<=T.clientWidth+1]; freeSelect(null);
        return [txt, svg, emo, tip, H.right<=C.left && H.left>=K.right && H.right<=innerWidth, legend, t2, Math.round(H.left), Math.round(H.right), Math.round(C.left)]; })()""")
      ok(r[0]=='' and r[1] and not r[2], '%s: la barra del Modo libre son puros íconos dibujados (sin texto ni emojis), cada uno con su nombre'%tag)
      ok(r[3][1] and r[3][2] and 'cajita' in r[3][0] and r[6][1] and r[4] and r[5], '%s: el texto de ayuda se lee completo abajo de la barra («%s» / «%s»), la barra no se encima (%s–%s, cámara en %s) y la primera vez sale qué es cada ícono'%(tag,r[3][0],r[6][0],r[7],r[8],r[9]))
      if tag=='Huawei':
        # 2. borrar todo
        r=await ev("""(()=>{ __CLR(); freeAddStatic({k:'b',a:0,b:1},FREE.X+2,FREE.Y,FREE.Z+2,0); freeAddStatic({k:'p',a:'canon',b:0},FREE.X-2,FREE.Y,FREE.Z+2,0); freeAddDyn('balon',FREE.X,FREE.Y,FREE.Z+4); __S(2);
          ui('freeClear').click(); const open=!ui('freeClearOv').hidden, msg=ui('freeClearP').textContent; ui('freeClearNo').click(); const kept=FREE.objs.length+FREE.dyn.length;
          ui('freeClear').click(); ui('freeClearYes').click(); return [open, msg, kept, FREE.objs.length+FREE.dyn.length, ui('freeClearOv').hidden]; })()""")
        ok(r[0] and '3 cosas' in r[1] and r[2]==3 and r[3]==0 and r[4], 'Borrar todo: pregunta antes («%s»); con «Cancelar» no pasa nada y con «Sí, borrar» queda vacío'%r[1])
        r=await ev("""(()=>{ __CLR(); const a=freeAddStatic({k:'b',a:0,b:1},FREE.X+2,FREE.Y,FREE.Z+2,0), c=freeAddStatic({k:'b',a:0,b:2},FREE.X+4,FREE.Y,FREE.Z+2,0), d=freeAddDyn('playa',FREE.X,FREE.Y,FREE.Z+4); a.au=MY_PID; c.au='otro1234'; d.au='otro1234';
          const was=[FNET.on,FNET.host,FNET.dirty]; FNET.on=true; FNET.host=true; FNET.dirty=FNET.dirty||new Set(); freeClearAsk(); const msg=ui('freeClearP').textContent; freeWipeMine(); const left=[FREE.objs.includes(a), FREE.objs.includes(c), FREE.dyn.includes(d)];
          FNET.on=was[0]; FNET.host=was[1]; FNET.dirty=was[2]; __CLR(); return [msg, left]; })()""")
        ok('1 cosa' in r[0] and 'amigos' in r[0] and r[1]==[False,True,True], 'Borrar todo en una sala: solo quita lo tuyo («%s») %s'%(r[0],r[1]))
        # 3. el dado rueda dando tumbos y cae en una cara; el balón tiene sus 12 pentágonos
        r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const d=freeAddDyn('dado',FREE.X,FREE.Y,FREE.Z); __S(10); const q0=d.spin.quaternion.clone(); d.v.set(0,0,6); __S(12); const turned=+(q0.angleTo(d.spin.quaternion)).toFixed(2); __S(110);
          const e=new THREE.Matrix4().makeRotationFromQuaternion(d.spin.quaternion).elements, al=[0,4,8].every(c=>Math.max(Math.abs(e[c]),Math.abs(e[c+1]),Math.abs(e[c+2]))>.999);
          const B=freeAddDyn('balon',FREE.X+3,FREE.Y,FREE.Z); let n=0; B.root.traverse(o=>{ if(o.isMesh) n++; }); return [turned, d.sleep, al, n]; })()""")
        ok(r[0]>1 and r[1] and r[2] and r[3]<=3, 'el dado gira al empujarlo (%s rad) y al pararse queda con una cara para arriba %s; el balón son %s piezas (12 pentágonos juntos)'%(r[0],r[1:3],r[3]))
        # 4. la gelatina tiembla al tocarla y se aplasta si estás encima
        r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const g=freeAddStatic({k:'p',a:'gelatina',b:0},FREE.X+.5,FREE.Y,FREE.Z+.5,0); __S(4); const idle=+g.root.userData.wob.scale.y.toFixed(3);
          player.pos.set(FREE.X+.5,FREE.Y+.05,FREE.Z+.5-.92); __S(1); const wob=g.wob>0; __S(20);
          player.pos.set(FREE.X+.5,FREE.Y+1.02,FREE.Z+.5); player.vy=0; player.grounded=true; FREE.pvy=0; for(let i=0;i<10;i++){ player.pos.y=FREE.Y+1; player.grounded=true; player.vy=0; FREE.pvy=0; __S(1); } const sq=+g.root.userData.wob.scale.y.toFixed(2);
          return [idle, wob, sq]; })()""")
        ok(r[1] and r[2]<.95, 'gelatina: al chocarla tiembla %s y si estás encima se aplasta (alto %s)'%(r[1],r[2]))
        # 5. el tubo suelta la pelota por su boquita de abajo
        r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const t=freeAddStatic({k:'p',a:'tubo',b:0},FREE.X,FREE.Y,FREE.Z,0); freeTube(t); const d=t.shots[0], p=d.root.position.clone(); __S(10); return [+(p.y-FREE.Y).toFixed(2), +(p.z-FREE.Z).toFixed(2), +(d.root.position.z-FREE.Z).toFixed(1)]; })()""")
        ok(r[0]<1 and r[1]>.8 and r[2]>r[1], 'tubo: la pelota sale por la boquita de abajo, enfrente, y rueda hacia adelante %s'%r)
      ok(not errs,'%s: sin errores %s'%(tag,errs[:3])); await ctx.close()
    await b.close()
asyncio.run(m())
