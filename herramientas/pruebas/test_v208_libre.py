# v208: Modo libre — planicie, poner/girar/quitar piezas enfrente, física (pelotas, cajas, barriles, resorte), guardar y salir.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; FREE.legacyAim=true; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, device_scale_factor=2); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheEnLinea','{\"on\":true,\"tip\":true}'); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    await ev("window.__run=(sec,fn)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); if(fn) fn(i); update(.05,t); } }; 1")
    # 1. entrar
    await ev("menuModes(true); ui('freeBtn').click(); 1"); await pg.wait_for_timeout(300)
    r=await ev("[!ui('freeStart').hidden, ui('freePub').textContent.includes('Crear sala'), !!ui('freeCode')]"); ok(r==[True,True,True], 'Modo libre muestra Empezar solo y Construir con amigos (crear sala, código) %s'%r)
    await ev("ui('freeSolo').click(); 1"); await pg.wait_for_timeout(1500); await ev("(window.requestAnimationFrame=()=>0, __run(1), 1)")
    r=await ev("[FREE.on, state, +player.pos.y.toFixed(2), Math.round(player.pos.x), !ui('freeHud').hidden, player.swim]"); ok(r[0] and r[1]=='play' and abs(r[2]-.6)<.1 and r[3]==9000 and r[4] and not r[5], 'entras a la planicie parado en el pasto %s'%r)
    # 2. el menú de objetos
    r=await ev("(()=>{ ui('freeObj').click(); const a=ui('freeGrid').children.length; FREE.tab='jardin'; FREE.sub='plantas'; freeRenderBox(); const b=ui('freeGrid').children.length; FREE.tab='fisica'; freeRenderBox(); const c=ui('freeGrid').children.length; const n=HK.length; return [a,b,c,n]; })()")
    ok(r[0]==15 and r[1]>=10 and r[2]==42 and r[3]>150, 'Objetos: 15 bloques (v254: 9 nuevos), plantas del Taller (%d), 42 de física (v229: dominó, fila, bolo, bolos y torre); en total %d piezas del Taller'%(r[1],r[3]))
    await pg.screenshot(path='/tmp/v208_menu.png')
    # 3. poner un cubo enfrente, girar, otro encima
    r=await ev("""(()=>{ ui('freeBox').hidden=true; freeSelect({k:'b',a:0,b:3}); __run(.2); const a=freeAim(); freePlace(); const o=FREE.objs[0]; freePlace(); const o2=FREE.objs[1];
      return [FREE.objs.length, +a.x.toFixed(2), +o.box.max.y.toFixed(2), o2?+o2.box.min.y.toFixed(2):null, scanActions.length>=0 && actA && actA.label]; })()""")
    ok(r[0]==2 and abs(r[2]-1.6)<.05 and r[3] and abs(r[3]-1.6)<.05, 'un cubo enfrente y otro encima (se apilan) %s'%r)
    # 4. chocas con el cubo y te puedes subir
    r=await ev("""(()=>{ const o=FREE.objs[0]; player.pos.set(o.x, FREE.Y+.05, o.z+2); player.facing=Math.PI; let minD=9; __run(1.5,()=>{ keys['KeyW']=true; }); keys['KeyW']=false; const d=Math.abs(player.pos.z-o.z);
      player.pos.set(o.x, 3.5, o.z); player.vy=0; __run(1); return [+d.toFixed(2), +player.pos.y.toFixed(2)]; })()""")
    ok(r[0]>=.85 and abs(r[1]-2.6)<.1, 'el cubo no se atraviesa (%s m) y te puedes parar encima (y=%s)'%(r[0],r[1]))
    # 5. una pieza del Taller (árbol) y un mueble
    r=await ev("""(()=>{ player.pos.set(FREE.X+5,FREE.Y+.05,FREE.Z+5); player.facing=0; const K=HK.find(K=>K.cat==='jardin' && K.sub==='plantas'); freeSelect({k:'h',a:K.id,b:K.mats[0]}); __run(.1); freeRotate(); freePlace();
      const K2=HK.find(K=>K.cat==='casa' && K.sub==='muebles'); player.pos.x+=4; freeSelect({k:'h',a:K2.id,b:K2.mats[0]}); __run(.1); freePlace(); const o=FREE.objs[FREE.objs.length-2]; return [FREE.objs.length, K.n, K2.n, o.r, +(o.box.max.y-o.box.min.y).toFixed(2)]; })()""")
    ok(r[0]==4 and r[3]==1 and r[4]>.3, 'piezas del Taller: %s (girada) y %s %s'%(r[1],r[2],r))
    # 6. física: pelota que pateas, caja, barril, resorte
    r=await ev("""(()=>{ player.pos.set(FREE.X-10,FREE.Y+.05,FREE.Z); player.facing=0; freeSelect({k:'p',a:'playa',b:0}); __run(.1); freePlace(); const B=FREE.dyn[0]; __run(1.5); const y0=+B.root.position.y.toFixed(2), z0=B.root.position.z;
      __run(.6,()=>{ player.pos.z+=.12; player.vel.set(0,0,2.4); }); player.vel.set(0,0,0); __run(1); const moved=+(B.root.position.z-z0).toFixed(2);
      return [FREE.dyn.length, y0, moved]; })()""")
    ok(r[0]==1 and abs(r[1]-(.6+.45))<.05 and r[2]>1, 'pelota de playa: cae al pasto y al caminarle encima sale rodando %s m'%r[2])
    r=await ev("""(()=>{ player.pos.set(FREE.X-10,FREE.Y+.05,FREE.Z-15); player.facing=0; for(const id of ['goma','tela','boliche','caja','barril']){ freeSelect({k:'p',a:id,b:0}); __run(.05); freePlace(); player.pos.x+=1.5; }
      const goma=FREE.dyn[1]; goma.root.position.y+=4; let top=0; __run(14,()=>{ top=Math.max(top, goma.root.position.y); }); const rest=FREE.dyn.every(d=>d.root.position.y<FREE.Y+d.r+.2);
      return [FREE.dyn.length, rest, FREE.dyn.map(d=>d.id+':'+(d.root.position.y-FREE.Y-d.r).toFixed(2)+':'+d.v.y.toFixed(2)).join(' ')]; })()""")
    ok(r[:2]==[6,True], 'goma, tela, boliche, caja y barril: todos caen y se quedan en el piso %s'%r)
    r=await ev("""(()=>{ player.pos.set(FREE.X+20,FREE.Y+.05,FREE.Z+20); player.facing=0; freeSelect({k:'p',a:'resorte',b:0}); __run(.05); freePlace(); const o=FREE.objs[FREE.objs.length-1];
      player.pos.set(o.x,FREE.Y+1,o.z); player.vy=0; let top=0; __run(2,()=>{ top=Math.max(top,player.pos.y); }); return [o.pad, +top.toFixed(1)]; })()""")
    ok(r[0] and r[1]>4, 'el resorte te avienta para arriba (hasta %s m)'%r[1])
    # 7. quitar
    r=await ev("""(()=>{ const n=FREE.objs.length; const o=FREE.objs[0]; player.pos.set(o.x,FREE.Y+.05,o.z+2.2); player.facing=Math.PI; freeSetDel(true); __run(.1); const t=FREE.tgt, tot=n+FREE.dyn.length; freeRemove(); return [!!t, FREE.objs.length+FREE.dyn.length===tot-1, !!t && FREE.og.children.includes(t.root)]; })()""")
    ok(r==[True,True,False], 'Quitar: marca lo que tienes enfrente y lo borra %s'%r)
    await ev("freeSetDel(false); freeSelect({k:'b',a:3,b:0}); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+6); player.facing=Math.PI; __run(.2); 1")
    try: await pg.screenshot(path='/tmp/v208_libre.png', timeout=90000)
    except Exception as e: print('(sin foto)')
    # 8. guardar, salir y volver
    r=await ev("""(()=>{ const n=FREE.objs.length, d=FREE.dyn.length; ui('toMenuBtn').click(); const out=[FREE.on, FREE.g.visible, state, Math.round(player.pos.x)];
      FREE.loaded=null; freeEnter(); return [...out, FREE.objs.length===n, FREE.dyn.length===d, n, d]; })()""")
    ok(r[0] is False and r[1] is False and r[2]=='menu' and r[3]==0 and r[4] and r[5], 'al salir regresas a la isla; al volver está todo lo que pusiste (%s cosas y %s con física) %s'%(r[6],r[7],r[:4]))
    r=await ev("(()=>{ const g=groundAt(0,0,5); return +g.toFixed(2); })()"); 
    ok(not errs,'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
