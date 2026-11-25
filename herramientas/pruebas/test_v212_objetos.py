# v212: Crear objeto para el inventario — editor (pieza, mango, adorno, colores, tamaño, qué hace), inventario y barra (se guarda),
# en la mano en la isla y en el Modo libre, lanzar (rebota y regresa), empujar (pelotas, cajas, criaturas, amigos), luz, y lo que ven los demás.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, device_scale_factor=1); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("if(!sessionStorage.getItem('t212')){ sessionStorage.setItem('t212','1'); localStorage.clear(); } localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route)
    async def load():
      await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    await load()
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    RUN="window.__run=(sec,fn)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); if(fn) fn(i); update(.05,t); } }; 1"
    await ev(RUN)
    # 1. Mis creaciones → 🎒 Objeto
    r=await ev("(()=>{ menuModes(true); ui('mapBtn').click(); const b=[...ui('mapTypes').children].find(x=>x.textContent.includes('Objeto')); b.click(); return [b.textContent.includes('Pronto'), ui('mapItems').textContent.includes('no tienes objetos'), ui('mapName').placeholder]; })()")
    ok(r[0] is False and r[1] and 'objeto' in r[2], 'Mis creaciones → 🎒 Objeto (ya no dice «pronto») %s'%r)
    await ev("ui('mapName').value='Bumerán'; ui('mapNew').click(); 1"); await pg.wait_for_timeout(800)
    r=await ev("[CR.open, CR.kind, ui('crName').value, [...ui('crTabs').children].map(b=>b.textContent).join(','), ui('crGrid').querySelectorAll('.shop-item').length, !!CR.prev && CR.prev.parent===studio, ui('crName').placeholder]")
    ok(r[0] and r[1]=='o' and r[2]=='Bumerán' and r[3]=='Pieza,Mango,Adorno,Colores,Tamaño,Qué hace' and r[4]==10 and r[5], 'Crear abre el editor de objeto en el estudio: 6 pestañas y 10 piezas %s'%r)
    # 2. armarlo: todas las combinaciones se arman sin errores
    r=await ev("""(()=>{ let n=0; for(const P of OB_OPTS.pieza) for(const M of OB_OPTS.mango) for(const A of OB_OPTS.adorno){ const g=obBuild({pieza:P[0],mango:M[0],adorno:A[0],c1:3,c2:6,tam:'1',hace:n%4?'cargar':'luz'}); let k=0; g.traverse(q=>{ if(q.isMesh) k++; }); if(k>0 && k<=6) n++; }
      crSet('pieza','luna'); crSet('mango','no'); crSet('adorno','picos'); crSet('c1',5); crSet('c2',9); crSet('tam','1.4'); CR.tab='hace'; crRender(); const txt=ui('crGrid').textContent; crSet('hace','lanzar');
      return [n, OB_OPTS.pieza.length*OB_OPTS.mango.length*OB_OPTS.adorno.length, txt.includes('Lanzar'), ui('crGrid').textContent.includes('regresa a tu mano')]; })()""")
    ok(r[0]==r[1] and r[2] and r[3], 'las %s combinaciones de pieza, mango y adorno se arman (máx. 6 dibujos cada una); «Qué hace» explica cada cosa %s'%(r[1],r))
    r=await ev("(()=>{ ui('crBack').click(); const O=obLoad()[0]; return [CR.open, !ui('mapList').hidden, O&&O.n, O&&O.pieza, O&&O.hace, ui('mapItems').textContent.includes('Bumerán'), inventory.includes('o:'+O.id), !!ITEMS['o:'+O.id] && ITEMS['o:'+O.id].icon.includes('<img')]; })()")
    ok(r==[False,True,'Bumerán','luna','lanzar',True,True,True], '✓ Listo lo guarda: sale en la lista y en tu inventario con su fotito %s'%r)
    await ev("""(()=>{ const mk=(n,d)=>{ obOpen(null); ui('crName').value=n; for(const k in d) crSet(k,d[k]); crClose(true); };
      mk('Martillo',{pieza:'cubo',mango:'largo',adorno:'ojitos',c1:0,c2:10,hace:'empujar'}); mk('Linterna',{pieza:'dona',mango:'asa',adorno:'cascabel',c1:8,c2:6,hace:'luz'}); mk('Corona',{pieza:'gema',mango:'no',hace:'cargar'}); return 1; })()""")
    # 3. a la barra desde el inventario, y se guarda
    r=await ev("""(()=>{ ui('toMenuBtn').click(); ui('mapList').hidden=true; menuEl.hidden=false; ui('soloBtn').click(); return 1; })()""")
    await pg.wait_for_timeout(2500); await ev("window.requestAnimationFrame=()=>0; __run(.5); 1")
    r=await ev("""(()=>{ const L=obLoad(); openInv(); const put=(k,j)=>{ const i=INV.findIndex(S=>S && S.k===k); ui('invGrid').children[i-INV_BAR].click(); useSlot(j); }; put('o:'+L[0].id,2); put('o:'+L[1].id,3); put('o:'+L[2].id,4); closeInv();   // (v262: tocas el objeto y luego el espacio de la barra)
      const saved=JSON.parse(localStorage.getItem('mundoPelucheInv')); return [state, inventory.length, hotbar[2]==='o:'+L[0].id, hotbar[3]==='o:'+L[1].id, hotbar[4]==='o:'+L[2].id, saved.s[2][0]===hotbar[2], ui('hotbar').querySelectorAll('.ob-ic').length]; })()""")
    ok(r==['play',9,True,True,True,True,3], 'en el inventario (5 + 4 objetos); se ponen en la barra y la barra se guarda %s'%r)
    # 4. en la mano en la isla: lanzar → vuela, rebota y regresa
    r=await ev("""(()=>{ useSlot(2); __run(.2); const H=plush.userData.obH; const lab=(ui('actA')||{}).textContent||document.querySelector('.act')?.textContent||'';
      const a=obActions(); obDo('tira'); __run(.35); const fly=OBH.fly.length, sent=OBH.oa&&OBH.oa[1], hidden=!H.holder.visible; const p0=OBH.fly[0]?OBH.fly[0].p.clone():null;
      let far=0; __run(3.5,()=>{ if(OBH.fly[0]) far=Math.max(far, OBH.fly[0].p.distanceTo(player.pos)); });
      return [heldItem()==='o:'+obLoad()[0].id, !!H && H.model!=null, a[0].label, fly, sent, hidden, +far.toFixed(1), OBH.fly.length, H.holder.visible]; })()""")
    ok(r[0] and r[1] and r[2].startswith('Lanzar') and r[3]==1 and r[4]==1 and r[5] and r[6]>4 and r[7]==0 and r[8], 'en la isla: lo traes en la mano; «Lanzar» lo avienta (llegó a %s m), y regresa a tu mano %s'%(r[6],r))
    # 5. luz de noche y en la cueva
    r=await ev("""(()=>{ useSlot(4); __run(.1); const k=Math.floor(Date.now()/1000/DAY_LEN)*DAY_LEN; const old=Date.now; Date.now=()=>(k+.75*DAY_LEN)*1000; __run(1,()=>updateSky(.05)); const H=plush.userData.obH, U=H.model.userData.ob;
      const night=1-(sky.dayK??1), on=U.glow.visible, at=!!OBH.lightAt, lab=obActions()[0].label; obActions()[0].run(); __run(.1); const off=U.glow.visible, em=U.mat.emissiveIntensity; obActions()[0].run(); __run(.1); Date.now=old; __run(.5);
      return [+night.toFixed(2), on, at, lab, off, em]; })()""")
    ok(r[0]>.2 and r[1] and r[2] and r[3]=='Apagar luz' and r[4] is False and r[5]==0, 'la Linterna da luz de noche (y en la cueva); «Apagar luz» la apaga %s'%r)
    # 6. en el Modo libre: lanzar le pega a una pelota; empujar mueve la caja y la criatura
    r=await ev("""(()=>{ crOpen(null); ui('crName').value='Michi'; crClose(true); ui('mapList').hidden=true; ui('toMenuBtn').click(); freeEnter(); window.requestAnimationFrame=()=>0; __run(.3); FREE.objs.slice().forEach(freeDrop); FREE.dyn.slice().forEach(freeDrop);
      const X=FREE.X, Y=FREE.Y, Z=FREE.Z; player.pos.set(X,Y+.05,Z); player.vel.set(0,0,0); player.facing=0; yaw=Math.PI; __run(.3);
      const ball=freeAddDyn('playa',X,Y+.05,Z+6,true); __run(1); const b0=ball.root.position.clone();
      useSlot(2); __run(.2); camera.position.set(X,Y+1.6,Z-3); camera.lookAt(X,Y+.4,Z+6); camera.updateMatrixWorld(); const cg=camera.getWorldDirection; camera.getWorldDirection=v=>v.set(0,-.2,1).normalize(); obDo('tira'); __run(.3); camera.getWorldDirection=cg; __run(2.5);
      const moved=ball.root.position.distanceTo(b0);
      FREE.dyn.slice().forEach(freeDrop); player.pos.set(X,Y+.05,Z); player.facing=0; const box=freeAddDyn('caja',X,Y+.05,Z+1.6,true); const C=crLoad()[0]; const cr=freeAddStatic({k:'c',a:C.id,b:0},X+.5,Y,Z+1.4,0,true); __run(.6);
      const k0=box.root.position.clone(), c0=[cr.cr.x,cr.cr.z]; useSlot(3); __run(.2); const lab=obActions()[0].label; obDo('empuja'); __run(1.2);
      const bm=box.root.position.distanceTo(k0), cm=Math.hypot(cr.cr.x-c0[0], cr.cr.z-c0[1]); ui('toMenuBtn').click(); return [+moved.toFixed(1), lab, +bm.toFixed(1), +cm.toFixed(1), OBH.oa[1]]; })()""")
    ok(r[0]>.5 and r[1]=='Empujar' and r[2]>.8 and r[3]>.8 and r[4]==2, 'Modo libre: lo lanzado le pega a la pelota (%s m); «Empujar» mueve la caja (%s m) y a la criatura (%s m) %s'%(r[0],r[2],r[3],r))
    # 7. los demás: lo ven en tu mano, ven cuando lo lanzas, y si te empujan sales volando
    r=await ev("""(()=>{ ui('soloBtn').click(); return 1; })()"""); await pg.wait_for_timeout(1500)
    r=await ev("""(()=>{ window.requestAnimationFrame=()=>0; const __run=(sec,fn)=>window.__run(sec,i=>{ if(fn) fn(i); updateRemotes(.05,clock.elapsedTime); }); __run(.3); if(heldItem()!==hotbar[3]) useSlot(3); __run(.1); const pres=obPresence(), d=obUnpack(pres.ob), same=JSON.stringify(obPack(d))===JSON.stringify(pres.ob);
      const P=player.pos, base={n:'Ana', c:2, id:'ana12345', p:[P.x+1.2,P.y,P.z], f:0, h:'o:xyz', ob:obPack({pieza:'corazon',mango:'corto',adorno:'mono',c1:0,c2:8,tam:'1',hace:'lanzar'})};
      const peer=(pr)=>onPeers({peers:[{peer:'ana', presence:{...base,...pr}}]});
      peer({}); __run(.3); const R=mp.remotes.get('ana'); const H=R && R.obj.userData.obH; const vis=!!H && H.holder.visible;
      peer({oa:[100,3]}); __run(.1); peer({oa:[101,1,P.x+1.2,P.y+1.4,P.z,0,3,12]}); __run(.25); const rfly=OBH.fly.filter(f=>!f.own).length; __run(3.5); const back=OBH.fly.length;
      player.vel.set(0,0,0); player.vy=0; const y0=P.y; peer({oa:[102,2,myUid,1,0]}); let up=0; __run(.6,()=>{ up=Math.max(up,P.y-y0); });
      return [same, vis, rfly, back, +up.toFixed(2), R.held]; })()""")
    ok(r[0] and r[1] and r[2]==1 and r[3]==0 and r[4]>.3 and r[5]=='o', 'multijugador: tu objeto va en tu presencia (7 números); ves el de Ana en su mano, cuando lo lanza, y si te empuja sales volando %s'%r)
    # 8. al volver a abrir el juego sigue todo; borrar un objeto lo quita de la barra
    await load(); await ev(RUN)
    r=await ev("""(()=>{ const L=obLoad(); return [L.length, hotbar[2]==='o:'+L[0].id, hotbar[3]==='o:'+L[1].id, inventory.filter(k=>k.startsWith('o:')).length]; })()""")
    ok(r==[4,True,True,4], 'al volver a abrir el juego: tus 4 objetos y la barra como la dejaste %s'%r)
    r=await ev("""(()=>{ const id=obLoad()[0].id; menuModes(true); ui('mapBtn').click(); [...ui('mapTypes').children].find(x=>x.textContent.includes('Objeto')).click(); const del=ui('mapItems').querySelector('.chip.del'); del.click(); del.click();
      return [obLoad().length, inventory.includes('o:'+id), hotbar.includes('o:'+id), !ITEMS['o:'+id], JSON.parse(localStorage.getItem('mundoPelucheInv')).s.some(e=>e && e[0]==='o:'+id)]; })()""")
    ok(r==[3,False,False,True,False], 'borrar un objeto lo quita del inventario y de la barra %s'%r)
    ok(not errs,'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
