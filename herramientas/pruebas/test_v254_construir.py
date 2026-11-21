# v254 (Modo libre, ronda A): 9 bloques nuevos, 5 materiales, luces que alumbran y botones/palancas/placas/temporizadores con canales
#  A) los 15 bloques se arman con los 6 materiales (sin errores) y tienen su fotito; lo de antes (fieltro) se arma igual que antes
#  B) por dentro: escalón, esquina, techo y cúpula se pisan a su altura; el cilindro es redondo; el cuarto de bloque se acomoda cada 50 cm
#  C) pintar deja el material; lo guardado se vuelve a cargar igualito (forma, color, material, canal)
#  D) las luces: farol, foco, tira y bloque que brilla alumbran de verdad de noche (entran a las 8 luces); «Apagar» las apaga
#  E) canales: botón → puerta; palanca → elevador; temporizador → luz; placa → cañón (dispara al pisarla); sin canal todo sigue como antes
#  F) en una sala: cualquiera prende la luz o mueve la palanca; el canal solo lo cambia quien la puso
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
SRC=open('/home/claude/mundo-peluche.html',encoding='utf-8').read()
pre='<script>window.__off=0; const _dn=Date.now.bind(Date); Date.now=()=>_dn()+window.__off;</script>'
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+pre+SRC.replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateSky(.05); try{ wlUpdate(); }catch(e){} } };
  window.__CLR=()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); FREE.hold=null; FREE.chg=null; freeSelect(null); };
  window.__AT=(x,z,f)=>{ player.pos.set(FREE.X+x,FREE.Y+.05,FREE.Z+z); player.vel.set(0,0,0); player.vy=0; player.facing=f||0; yaw=player.facing+Math.PI; __S(3); };
  window.__ADD=(k,a,b,x,y,z,r)=>freeAddStatic({k,a,b},FREE.X+x,FREE.Y+(y||0),FREE.Z+z,r||0,true); 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1'); localStorage.setItem('mundoPelucheNovedades','999');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300); await ev(STEP)
    await ev("(()=>{ freeEnter(); __CLR(); __AT(0,0,0); return 1; })()")
    # A) todos los bloques con todos los materiales
    r=await ev("""(()=>{ let n=0, bad=[]; for(let a=0;a<FREE_SHAPES.length;a++) for(let mt=0;mt<6;mt++){ const o=freeMake({k:'b',a,b:freeBPick(a,3,mt)}); if(!o || !o.children.length) bad.push(a+':'+mt); else n++; }
      const old=freeMake({k:'b',a:0,b:3}), m=old.children[0]; return {n,bad,shapes:FREE_SHAPES.length,oldGeo:m.geometry===_freeBox && m.material===FM(FREE_COLS[3]) && m.position.y===.5, mats:FREE_MATS.length}; })()""")
    ok(r['shapes']==15 and r['mats']==6 and r['n']==90 and not r['bad'], '🧱 los %d bloques se arman con los %d materiales (%d piezas)'%(r['shapes'],r['mats'],r['n']))
    ok(r['oldGeo'], '🧸 el cubo de fieltro de siempre se arma igualito que antes')
    r=await ev("""(()=>{ const out=[]; for(const [a,mt] of [[6,1],[7,2],[8,3],[9,4],[10,5],[11,0],[12,1],[13,0],[14,0],[0,3]]){ const u=freeThumbRender('b:'+a+':'+freeBPick(a,5,mt)); out.push(u && u!=='x' && u.length>500); } return out; })()""")
    ok(all(r), '🖼️ las fotitos de los bloques nuevos y con material salen (%d de %d)'%(sum(r),len(r)))
    r=await ev("""(()=>{ FREE.tab='bloques'; ui('freeBox').hidden=false; freeRenderBox(); const g=ui('freeGrid').querySelectorAll('.free-it').length, mats=[...ui('freeSubs2').querySelectorAll('.fchip')].map(b=>b.textContent);
      FREE.tab='mecan'; freeRenderBox(); const mec=[...ui('freeGrid').querySelectorAll('.free-it span')].map(s=>s.textContent); const tabs=[...ui('freeTabs').querySelectorAll('.fchip')].map(b=>b.textContent);
      FREE.tab='fisica'; freeRenderBox(); const fis=ui('freeGrid').querySelectorAll('.free-it').length; ui('freeBox').hidden=true; return {g,mats,mec,tabs,fis}; })()""")
    ok(r['g']==15 and r['mats']==['Fieltro','Madera','Piedra','Ladrillo','Galleta','Dulce'], '🎨 en «Bloques» hay 15 formas y los materiales %s'%r['mats'])
    ok(any('Luces y botones' in t for t in r['tabs']) and r['mec']==['Farol','Foco de color','Tira de luces','Botón','Palanca','Placa para pisar','Temporizador'] and r['fis']==42, '💡 pestaña «Luces y botones» con %s; «Física» sigue con %d'%(r['mec'],r['fis']))
    # B) por dentro
    r=await ev("""(()=>{ __CLR(); const S=id=>FREE_SHAPES.findIndex(s=>s.id===id); const H=(o,dx,dz)=>+(freeGround(o.x+dx,o.z+dz,FREE.Y+5)-FREE.Y).toFixed(2);
      const es=__ADD('b',S('escalon'),0,2.5,0,2.5), eq=__ADD('b',S('esquina'),0,4.5,0,2.5), te=__ADD('b',S('techo'),0,6.5,0,2.5), cu=__ADD('b',S('cupula'),0,8.5,0,2.5), ci=__ADD('b',S('cilindro'),0,10.5,0,2.5);
      return {es:[H(es,0,-.25),H(es,0,.25)], eq:[H(eq,-.4,-.4),H(eq,.4,.4),H(eq,.4,-.4)], te:[H(te,0,0),H(te,.4,0)], cu:[H(cu,0,0),H(cu,.45,.1)], ci:[H(ci,0,0),H(ci,.47,.47)]}; })()""")
    ok(r['es']==[.5,1.0], '🪜 el escalón se pisa a 50 cm y a 1 m %s'%r['es'])
    ok(r['eq'][0]<.15 and r['eq'][1]>.85 and r['eq'][2]<.15, '📐 la esquina de rampa sube hacia su esquina %s'%r['eq'])
    ok(abs(r['te'][0]-.5)<.02 and r['te'][1]<.15, '🏠 el techo tiene su punta en medio %s'%r['te'])
    ok(abs(r['cu'][0]-.5)<.02 and r['cu'][1]<.25, '⛺ la cúpula es redondita %s'%r['cu'])
    ok(abs(r['ci'][0]-1)<.02 and r['ci'][1]==0, '🛢️ el cilindro es redondo (en su esquina no hay piso) %s'%r['ci'])
    r=await ev("""(()=>{ __CLR(); __AT(0,0,0); const S=FREE_SHAPES.findIndex(s=>s.id==='cuarto'); freeSelect({k:'b',a:S,b:0}); const xs=new Set(); for(let pt=-.9;pt<-.3;pt+=.07){ pitch=pt; __S(1); const a=freeAim(); xs.add(+(((a.z-FREE.Z)%1+1)%1).toFixed(2)); } pitch=-.3; freeSelect(null); return [...xs].sort(); })()""")
    ok(len(r)>=2 and all(v in (.25,.75) for v in r), '🟫 el cuarto de bloque se acomoda cada 50 cm %s'%r)
    # C) pintar y guardar
    r=await ev("""(()=>{ __CLR(); const S=FREE_SHAPES.findIndex(s=>s.id==='pared'); const o=__ADD('b',S,freeBPick(S,2,3),1,0,3); fnLocalAdd(o); FREE.pcol=6; FREE.tgt=o; freePaintDo(); const b1=o.sel.b;
      const l=__ADD('p','foco',4,-2,0,3); l.sel.b=4|(3<<8); freeSave(); FREE.loaded=null; freeLoad(); const o2=FREE.objs.find(q=>q.sel.k==='b'), l2=FREE.objs.find(q=>q.sel.a==='foco');
      return [freeBMat(b1), freeBCol(b1), o2 && o2.sel.a===S && o2.sel.b===b1, l2 && chOf(l2.sel)]; })()""")
    ok(r[0]==3 and r[1]==6, '🖌️ pintar cambia el color y deja el material (ladrillo azul)')
    ok(r[2] and r[3]==3, '💾 al guardar y volver a abrir queda igual: forma, color, material y canal')
    # D) luces
    await ev("(()=>{ const n=Date.now(); const cur=((n/1000)%DAY_LEN)/DAY_LEN; window.__off+=((.75-cur)*DAY_LEN*1000); return 1; })()")
    r=await ev("""(()=>{ __CLR(); __AT(0,0,0); const S=FREE_SHAPES.findIndex(s=>s.id==='brilla'); const L=[__ADD('p','farol',0,-3,0,4), __ADD('p','foco',5,0,0,4), __ADD('p','tira',0,3,0,4), __ADD('b',S,2,5,0,4)]; __S(4);
      camera.updateMatrixWorld(); let near=0; for(const o of L){ const u=o.root.userData.lit, P=new THREE.Vector3(o.x,o.y+u.y,o.z); for(const v of WL.V){ if(v.w<=0) continue; const q=new THREE.Vector3(v.x,v.y,v.z).applyMatrix4(camera.matrixWorld); if(q.distanceTo(P)<.05){ near++; break; } } }
      const on=L.map(o=>o.root.userData.lit.st); const f=L[1]; const A=mecActions; __AT(0,2.6,0); __S(2); const a=freeActions(); return {near, on, lab:a&&a[0]&&a[0].label, lab2:a&&a[1]&&a[1].label}; })()""")
    ok(r['near']==4 and all(r['on']), '🏮 de noche el farol, el foco, la tira y el bloque que brilla alumbran de verdad (%d de 4)'%r['near'])
    ok(r['lab']=='💡 Apagar' and r['lab2']=='⚪ Sin canal', '👉 enfrente de una luz: «%s» y «%s»'%(r['lab'],r['lab2']))
    r=await ev("""(()=>{ const a=freeActions(); a[0].run(); __S(2); const o=FREE.objs.find(q=>q.sel.a==='foco'); const st=o.root.userData.lit.st; const b=freeActions()[0].label; freeActions()[0].run(); __S(2); return [st, b, o.root.userData.lit.st]; })()""")
    ok(r[0] is False and r[1]=='💡 Prender' and r[2] is True, '💡 «Apagar» la apaga y «Prender» la vuelve a prender')
    # E) canales
    r=await ev("""(()=>{ __CLR(); __AT(0,-6,0); const bt=__ADD('p','boton',1<<8,0,0,0), pu=__ADD('v','puerta',6|(1<<8),4,0,0), pv=__ADD('v','puerta',6,8,0,0); __S(10);
      const d0=pu.ride.door, s0=pu.solid; __AT(0,0,0); __S(12); const d1=pu.ride.door, far=pv.ride.door; __AT(0,-6,0); __S(16); return [d0,s0,d1,far,pu.solid]; })()""")
    ok(r[0]<.05 and r[1] and r[2]>.9 and r[4], '🚪 botón rojo → puerta roja: cerrada aunque estés cerca; se abre al pisar el botón y se cierra al bajarte')
    r=await ev("""(()=>{ __CLR(); __AT(0,-6,0); const pa=__ADD('p','palanca',2<<8,0,0,0), el=__ADD('v','elevador',7|(2<<8),5,0,0); __S(20); const y0=el.box.max.y;
      __AT(0,-1.2,0); __S(2); const a=freeActions(); a[0].run(); __S(80); const y1=el.box.max.y; freeActions()[0].run(); __S(80); return [a[0].label, +(y0-el.y).toFixed(2), +(y1-el.y).toFixed(2), +(el.box.max.y-el.y).toFixed(2)]; })()""")
    ok(r[0]=='✋ Mover palanca' and r[1]<.4 and r[2]>4 and r[3]<.4, '🎚️ palanca azul → elevador azul: sube al moverla y baja al regresarla %s'%r)
    r=await ev("""(()=>{ __CLR(); __AT(0,-6,0); const tm=__ADD('p','timer',(3<<8)|(0<<1),0,0,0), lz=__ADD('p','foco',2|(3<<8),3,0,0); const seen=new Set(); for(let i=0;i<60;i++){ __S(1); seen.add(lz.root.userData.lit.st); } return [...seen].sort(); })()""")
    ok(r==[False,True], '⏱ temporizador verde → luz verde: se prende y se apaga sola')
    r=await ev("""(()=>{ __CLR(); __AT(0,-6,0); const pl=__ADD('p','placa',4<<8,0,0,0), cn=__ADD('p','canon',4<<8,3,0,0), cs=__ADD('p','canon',0,-3,0,0); __S(10); const n0=FREE.dyn.length;
      __AT(0,0,0); __S(6); const n1=FREE.dyn.length; __S(10); const n2=FREE.dyn.length; return [n0,n1,n2, (cn.shots||[]).length, (cs.shots||[]).length]; })()""")
    ok(r[0]==0 and r[1]==1 and r[2]==1 and r[3]==1 and r[4]==0, '💥 placa amarilla → cañón amarillo: dispara una vez al pisarla (el cañón sin canal no) %s'%r)
    r=await ev("""(()=>{ __CLR(); __AT(0,-6,0); const bt=__ADD('p','boton',0,0,0,0), tb=__ADD('p','tubo',0,3,0,0); __S(6); const n0=FREE.dyn.length; __AT(0,0,0); __S(6); return [n0, FREE.dyn.length]; })()""")
    ok(r[0]==0 and r[1]>=1, '🔘 sin canal, el botón sigue activando el tubo de al lado como antes')
    r=await ev("""(()=>{ __CLR(); __AT(0,-1.2,0); const bt=__ADD('p','boton',0,0,0,0); __S(2); const a=freeActions(), l0=a&&a[0]&&a[0].label; a[0].run(); __S(2); const l1=freeActions()[0].label; const dot=bt.root.children.some(c=>c.isMesh && c.material.isMeshBasicMaterial && c.scale.x<.1); return [l0,l1,chOf(bt.sel),dot]; })()""")
    ok(r[0]=='⚪ Sin canal' and r[1]=='🔴 Canal rojo' and r[2]==1 and r[3], '🔴 tocar «Sin canal» lo pone en rojo y le sale su puntito rojo %s'%r[:3])
    # F) sala
    r=await ev("""(()=>{ __CLR(); FNET.on=true; FNET.host=true; const l=__ADD('p','foco',2,0,0,3), pa=__ADD('p','palanca',0,2,0,3); for(const o of [l,pa]){ o.nid='w'+o.id; o.au='otroaaaa'; o.bk=0; }
      const B=o=>o.sel.b|0; fnApplyOp('amigoxyz',[1,'cb',l.nid,B(l)|16]); const a=B(l); fnApplyOp('amigoxyz',[2,'cb',pa.nid,B(pa)|1]); const b2=B(pa); fnApplyOp('amigoxyz',[3,'cb',l.nid,B(l)|(2<<8)]); const c=chOf(l.sel); fnApplyOp('otroaaaa',[4,'cb',l.nid,B(l)|(2<<8)]); const d=chOf(l.sel);
      FNET.on=false; FNET.host=false; return [a&16, b2&1, c, d]; })()""")
    ok(r[0]==16 and r[1]==1, '👥 en una sala, cualquiera prende o apaga la luz y mueve la palanca')
    ok(r[2]==0 and r[3]==2, '🔒 el canal solo lo cambia quien la puso')
    ok(not errs, '🚫 sin errores (%s)'%errs[:3])
    await b.close()
asyncio.run(m())
