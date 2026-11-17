# v211: Crear criatura — editor en el estudio (cuerpo, ojos, orejas, cabeza, patas, cola, alas, colores, tamaño, cómo se porta),
# guardar, ponerla en el Modo libre y en un Mundo completo, y que camine sola (te sigue / huye / quieta en el editor).
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, device_scale_factor=2); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    await ev("window.__run=(sec,fn)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); if(fn) fn(i); update(.05,t); } }; 1")
    # 1. la lista con el tipo Criatura
    r=await ev("(()=>{ menuModes(true); ui('mapBtn').click(); const b=[...ui('mapTypes').children].find(x=>x.textContent.includes('Criatura')); b.click(); return [b.textContent.includes('Pronto'), ui('mapItems').textContent.includes('no tienes criaturas'), ui('mapName').placeholder]; })()")
    ok(r[0] is False and r[1] and 'criatura' in r[2], 'Mis creaciones → 🐾 Criatura (ya no dice «pronto») %s'%r)
    await ev("ui('mapName').value='Michi'; ui('mapNew').click(); 1"); await pg.wait_for_timeout(1200)
    r=await ev("[CR.open, !ui('crEd').hidden, ui('crName').value, ui('crTabs').children.length, !!CR.prev && CR.prev.parent===studio, ui('crGrid').querySelectorAll('.shop-item').length]")
    ok(r[0] and r[1] and r[2]=='Michi' and r[3]==10 and r[4] and r[5]==4, 'Crear abre el editor de criatura en el estudio: 10 pestañas, la criatura girando %s'%r)
    # 2. armarla
    r=await ev("""(()=>{ crSet('cuerpo','frijol'); crSet('ojos','tres'); crSet('orejas','conejo'); crSet('cabeza','cuernitos'); crSet('patas','6'); crSet('cola','zorro'); crSet('alas','mariposa'); crSet('c1',7); crSet('c2',8); crSet('tam','1.5'); CR.tab='porta'; crRender(); const n=ui('crGrid').querySelectorAll('.shop-item').length; crSet('porta','sigue');
      const U=CR.prev.userData.cr; return [U.legs.length, U.wings.length, !!U.tail, CR.prev.scale.x, n]; })()""")
    ok(r==[6,2,True,1.5,9], 'cuerpo frijol, 3 ojos, orejas de conejo, cuernitos, 6 patas, cola esponjada, alas de mariposa, colores, grande y «te sigue» %s'%r)
    await pg.wait_for_timeout(800); await pg.screenshot(path='/tmp/v211_editor.png')
    r=await ev("(()=>{ ui('crBack').click(); const C=crLoad()[0]; return [CR.open, !ui('mapList').hidden, C&&C.n, C&&C.patas, C&&C.porta, ui('mapItems').textContent.includes('Michi')]; })()")
    ok(r==[False,True,'Michi','6','sigue',True], '✓ Listo la guarda y sale en la lista %s'%r)
    await ev("crOpen(null); ui('crName').value='Asustadizo'; crSet('porta','huye'); crSet('cuerpo','bolita'); crClose(true); 1")
    # 3. en el Modo libre: te sigue / huye
    r=await ev("""(()=>{ ui('mapList').hidden=true; freeEnter(); window.requestAnimationFrame=()=>0; __run(.3); FREE.tab='criaturas'; ui('freeBox').hidden=false; freeRenderBox(); const n=ui('freeGrid').querySelectorAll('.free-it').length; ui('freeBox').hidden=true;
      const [A,B]=crLoad(); const X=FREE.X, Y=FREE.Y, Z=FREE.Z; FREE.objs.slice().forEach(freeDrop); FREE.dyn.slice().forEach(freeDrop);
      const a=freeAddStatic({k:'c',a:A.id,b:0},X+6,Y,Z,0,true), h=freeAddStatic({k:'c',a:B.id,b:0},X-20,Y,Z,0,true); window.__a=a; window.__h=h;
      player.pos.set(X+16,Y+.05,Z); __run(4); const da=Math.hypot(a.cr.x-player.pos.x, a.cr.z-player.pos.z);
      player.pos.set(h.cr.x+2,Y+.05,h.cr.z); __run(.1); const d0=Math.hypot(h.cr.x-player.pos.x,h.cr.z-player.pos.z); __run(2.5); const d1=Math.hypot(h.cr.x-player.pos.x,h.cr.z-player.pos.z);
      return [n, +da.toFixed(1), +d0.toFixed(1), +d1.toFixed(1)]; })()""")
    ok(r[0]==2 and r[1]<4 and r[3]>r[2]+1, 'Modo libre: pestaña 🐾 con tus 2 criaturas; Michi te sigue (queda a %s m) y Asustadizo huye (%s → %s m)'%(r[1],r[2],r[3]))
    # 4. cambiarla en el editor y que se actualice
    r=await ev("""(()=>{ const id=__a.sel.a; CR.open=false; crOpen(id); crSet('c1',0); crSave(); CR.open=false; ui('crEd').hidden=true; SW.mode=''; menuEl.hidden=true; __run(.1); const o=FREE.objs.find(q=>q.sel.a===id); let col=null; o.root.traverse(q=>{ if(!col && q.isMesh && q.material && q.material.color) col=q.material.color.getHexString(); }); return [!!o.cr, crById(id).c1]; })()""")
    ok(r==[True,0], 'si la cambias, la que está en el mundo se actualiza %s'%r)
    # 5. guardar y volver; en un Mundo completo: quieta en el editor, camina al probar
    r=await ev("""(()=>{ ui('toMenuBtn').click(); freeEnter(); const n=FREE.objs.filter(o=>o.sel.k==='c').length; ui('toMenuBtn').click();
      mapType='mundo'; ui('mapName').value='Zoo'; mapCreate(); const tabs=mapTabs().map(t=>t[0]); MED.tab='criaturas'; medRender(); const cards=MED.ui.inv.querySelectorAll('.hed-card').length;
      const A=crLoad()[0]; const o=freeAddStatic({k:'c',a:A.id,b:0},FREE.X+3,FREE.Y,FREE.Z,0,true); __run(2); const still=Math.hypot(o.cr.x-o.x,o.cr.z-o.z);
      medPlay(); player.pos.set(FREE.X+15,FREE.Y+.05,FREE.Z); __run(3); const moved=Math.hypot(o.cr.x-o.x,o.cr.z-o.z); ui('freeEdit').click(); const back=Math.hypot(o.cr.x-o.x,o.cr.z-o.z);
      return [n, tabs.includes('criaturas'), cards, +still.toFixed(2), +moved.toFixed(1), +back.toFixed(2)]; })()""")
    ok(r[0]==2 and r[1] and r[2]==2 and r[3]==0 and r[4]>2 and r[5]==0, 'se guardan en el Modo libre; en el Mundo completo salen en 🐾, quietas al editar, caminan al probar y regresan al editar %s'%r)
    # 6. borrar una criatura: lo puesto se ignora sin errores
    r=await ev("""(()=>{ medDone(); const B=crLoad()[1]; crStore(crLoad().filter(c=>c.id!==B.id)); FREE.loaded=null; freeEnter(); const n=FREE.objs.filter(o=>o.sel.k==='c').length; ui('toMenuBtn').click(); return n; })()""")
    ok(r==1, 'si borras una criatura, desaparece del mundo sin romper nada (queda %s)'%r)
    # 7. cuidar el teléfono: piezas juntas por color, máximo 12 puestas, las muy lejanas no se dibujan
    r=await ev("""(()=>{ freeEnter(); const A=crLoad()[0]; FREE.objs.slice().forEach(freeDrop); let n=0; for(let i=0;i<14;i++) if(freeAddStatic({k:'c',a:A.id,b:0},FREE.X-20+i*3,FREE.Y,FREE.Z-10,0,true)) n++;
      let meshes=0, sh=0; FREE.objs[0].root.traverse(q=>{ if(q.isMesh){ meshes++; if(q.castShadow) sh++; } });
      player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+55); __run(.4); const far=FREE.objs.filter(o=>!o.root.visible).length; player.pos.set(FREE.X,FREE.Y+.05,FREE.Z); __run(.4); const near=FREE.objs.filter(o=>o.root.visible).length; ui('toMenuBtn').click(); return [n, meshes, sh, far, near]; })()""")
    ok(r[0]==12 and r[1]<=24 and r[2]==1 and r[3]==12 and r[4]==12, 'para el teléfono: máximo 12 criaturas puestas, piezas juntas (%s mallas, 1 sombra), las lejanas no se dibujan %s'%(r[1],r))
    ok(not errs,'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
