# v216: Modo libre más grande y a tu gusto — 1000 piezas y 100 con física (sala: 500/50), rejilla de choques, pelotas que
# se duermen, 🎨 pintar, 🌤️ piso/hora/clima (se guardan; también en los mapas).
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("if(!sessionStorage.getItem('t216')){ sessionStorage.setItem('t216','1'); localStorage.clear(); } localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:true})); localStorage.setItem('mundoPelucheEcon124','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route)
    async def load():
      await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
      await ev("window.__run=(sec,fn)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); if(fn) fn(i); update(.05,t); updateSky(.05); } }; 1")
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    await load()
    # 1. límites nuevos
    r=await ev("""(()=>{ freeEnter(); window.requestAnimationFrame=()=>0; FREE.objs.slice().forEach(freeDrop); FREE.dyn.slice().forEach(freeDrop); const X=FREE.X,Y=FREE.Y,Z=FREE.Z;
      let n=0; for(let i=0;i<1005;i++){ if(freeAddStatic({k:'b',a:i%3,b:i%12},X-60+(i%40)*3+.5,Y,Z-60+Math.floor(i/40)*3+.5,0,true)) n++; }
      let nd=0; for(let i=0;i<105;i++){ if(freeAddDyn(['playa','goma','caja','barril'][i%4],X-50+(i%20)*5+1.7,Y+2,Z-50+Math.floor(i/20)*5+1.7,true)) nd++; }
      freeLimits(true); const net=[FREE_MAX,FREE_DYN]; freeLimits(false); return [n, nd, net.join('/'), FREE_MAX, FREE_DYN]; })()""")
    ok(r==[1000,100,'500/50',1000,100], 'límites: 1000 piezas y 100 con física (en sala con amigos 500 y 50) %s'%r)
    # 2. rejilla: el suelo y los choques ven solo lo de cerca, y se actualiza al quitar
    r=await ev("""(()=>{ const X=FREE.X,Y=FREE.Y,Z=FREE.Z, o=FREE.objs.find(q=>Math.abs(q.x-(X-60+.5))<.01 && Math.abs(q.z-(Z-60+.5))<.01); const g1=freeGround(o.x,o.z,Y+5), q=fgQuery(o.x,o.z,o.x,o.z).length;
      freeDrop(o); const g2=freeGround(o.x,o.z,Y+5); const p=new THREE.Vector3(X-60+3.5-.6,Y,Z-60+.5); freeCollide(p); return [+(g1-Y).toFixed(2), q, +(g2-Y).toFixed(2), +(p.x-(X-60+3.5)).toFixed(2)]; })()""")
    ok(r[0]>0 and r[1]<=4 and r[2]==0 and r[3]<=-.9, 'la rejilla: el suelo arriba de un bloque (%s m), revisa solo %s cosas, al quitarlo vuelve al piso, y los bloques te detienen %s'%(r[0],r[1],r))
    # 3. pelotas que se duermen (y despiertan)
    r=await ev("""(()=>{ __run(9); const dorm=FREE.dyn.filter(d=>d.sleep).length; const d=FREE.dyn[0], p0=d.root.position.clone(); player.pos.set(p0.x-1.2,FREE.Y+.05,p0.z); player.vel.set(4,0,0); __run(.4,()=>player.vel.set(4,0,0)); const moved=d.root.position.distanceTo(p0);
      const e=FREE.dyn[50]; e.v.set(5,2,0); __run(.1); const woke=!e.sleep; return [dorm, moved>.2, woke]; })()""")
    ok(r==[100,True,True], 'las 100 pelotas se quedan quietas y se duermen; al empujarlas despiertan y se mueven %s'%r)
    r=await ev("""(()=>{ let t=clock.elapsedTime; for(let i=0;i<60;i++){ clock.elapsedTime=(t+=.05); update(.05,t); } FREE.dyn.forEach(d=>{ d.sleep=true; d.v.set(0,0,0); }); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+66);
      const t0=performance.now(); for(let i=0;i<60;i++){ clock.elapsedTime=(t+=.05); update(.05,t); } return +((performance.now()-t0)/60).toFixed(2); })()""")
    ok(r<4, 'con 1000 piezas y 100 pelotas dormidas cada cuadro tarda %s ms (antes con lo mismo: ~5.9 ms)'%r)
    # 4. 🎨 pintar
    r=await ev("""(()=>{ FREE.objs.slice().forEach(freeDrop); FREE.dyn.slice().forEach(freeDrop); const X=FREE.X,Y=FREE.Y,Z=FREE.Z; player.pos.set(X,Y+.05,Z); player.facing=0;
      const blk=freeAddStatic({k:'b',a:0,b:0},X+.5,Y,Z+1.5,0,true); const K=HK.find(k=>(k.mats||[]).length>2), hp=freeAddStatic({k:'h',a:K.id,b:K.mats[0]},X+4.5,Y,Z+8,0,true); const C=crOpen(null); ui('crName').value='Pato'; crClose(true); ui('mapList').hidden=true; menuEl.hidden=true;
      const cr=freeAddStatic({k:'c',a:crLoad()[0].id,b:0},X-4.5,Y,Z+8,0,true);
      ui('freePaintB').click(); const bar=!document.getElementById('freePaint').hidden, acts=freeActions().map(a=>a&&a.label).join(','); FREE.pcol=5; freePaintBar(); FREE.tgt=blk; freePaintDo(); const c1=blk.sel.b;
      FREE.tgt=hp; freePaintDo(); const m1=hp.sel.b; FREE.tgt=cr; freePaintDo(); const msg=ui('toast').textContent; freeSave(); const saved=JSON.parse(localStorage.getItem('mundoPelucheLibre')).s.find(e=>e[0]==='b')[2];
      freePaintSet(false); return [bar, acts, c1, m1===K.mats[1], msg, saved, document.getElementById('freePaint').hidden]; })()""")
    ok(r[0] and r[1]=='Pintar,Listo' and r[2]==5 and r[3] and 'no se puede pintar' in r[4] and r[5]==5 and r[6], '🎨 Pintar: barra de colores, el bloque cambia a azul, la pieza del Taller a su siguiente tela, la criatura no; se guarda %s'%r)
    # 5. 🌤️ piso, hora y clima
    r=await ev("""(()=>{ ui('freeEnvB').click(); const el=document.getElementById('freeEnv'), rows=el.querySelectorAll('.env-row'); const n=[...rows].map(d=>d.children.length).join(',');
      [...rows[0].children].find(b=>b.textContent.includes('Arena')).click(); [...rows[1].children].find(b=>b.textContent.includes('Noche')).click(); [...rows[2].children].find(b=>b.textContent.includes('Lluvia')).click();
      __run(.5); const floor=FREE.floor.material[2].map===FREE_FLOOR.arena, night=sky.dayK<.2, rain=weatherNow.id==='rain';
      [...rows[0].children].find(b=>b.textContent.includes('Espacio')).click(); __run(.5); const sp=[weatherNow.id, sky.dayK<.2, !!el.querySelector('.env-row:nth-of-type(2) button[disabled]') || [...el.querySelectorAll('.env-row')][1].children[0].disabled];
      el.querySelector('#freeEnvOk').click(); freeSave(); const env=JSON.parse(localStorage.getItem('mundoPelucheLibre')).env; return [n, floor, night, rain, sp.join(','), JSON.stringify(env), el.hidden]; })()""")
    ok(r[0]=='5,4,7' and r[1] and r[2] and r[3] and r[4]=='clear,true,true' and '"piso":"espacio"' in r[5] and r[6], '🌤️ Lugar: piso arena, de noche y con lluvia; en el espacio siempre es de noche y despejado; se guarda %s'%r)
    r=await ev("""(()=>{ ui('toMenuBtn').click(); __run(.3); const fuera=freeEnvSky()===null; freeEnter(); __run(.3); return [fuera, FREE.env.piso, FREE.floor.material[2].map===FREE_FLOOR.espacio]; })()""")
    ok(r==[True,'espacio',True], 'al salir el cielo vuelve al de la isla; al volver tu planicie sigue en el espacio %s'%r)
    # 6. también en los mapas (desde el editor 🧰 → Lugar)
    r=await ev("""(()=>{ ui('toMenuBtn').click(); menuModes(true); ui('mapBtn').click(); mapType='mundo'; ui('mapName').value='Isla dulce'; mapCreate(); const t=[...MED.ui.tools.querySelectorAll('button')].find(b=>b.textContent.includes('Lugar')); t.click();
      const rows=document.querySelectorAll('#freeEnv .env-row'); [...rows[0].children].find(b=>b.textContent.includes('Dulce')).click(); document.querySelector('#freeEnvOk').click(); const id=FREE.ctx; medDone(); return [!!t, (mapById(id).env||{}).piso]; })()""")
    ok(r==[True,'dulce'], 'en el editor de mapas también: 🧰 → 🌤️ Lugar, y se guarda con el mapa %s'%r)
    ok(not errs,'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
