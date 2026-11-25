# v266: el mar: conchas en la arena (12, 4 rarezas; más después de una tormenta), botellas con mensaje y mapa del tesoro,
# el cofre del barco hundido, ballenas junto al muelle de Tortu y motos acuáticas (solo su dueño la maneja).
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



    await ev("startGame()"); await pg.wait_for_timeout(1500)
    await ev("""(()=>{ window.requestAnimationFrame=()=>0; window.__run=(sec,fn)=>{ let t=clock.elapsedTime; for(let i=0;i<Math.round(sec/.05);i++){ clock.elapsedTime=(t+=.05); if(fn && fn(i)===true) return true; update(.05,t); } }; __run(1); weatherOfSlot=()=>'clear'; return 1; })()""")
    await ev("(()=>{ for(let i=0;i<200 && !SHL.cand;i++) __run(.05); return 1; })()")

    # 1. conchas en la playa
    r=await ev("""(()=>{ const cur=Math.floor(Date.now()/1000/SHL.SLOT); SHL.lists.clear(); const L=shlList(cur); const onSand=L.filter(e=>{ const t=terrainH(e.x,e.z); return onSandAt(e.x,e.z,t) || coastC(e.x,e.z)>.85; }).length;
      const w0=weatherOfSlot; weatherOfSlot=()=>'storm'; SHL.lists.clear(); const S=shlList(cur+5); weatherOfSlot=w0; SHL.lists.clear(); const R=a=>a.reduce((s,e)=>s+SHL_BY[e.id].r,0)/a.length;
      return [SHL.cand.length/2, L.length, onSand, S.length, +R(L).toFixed(2), +R(S).toFixed(2), SHL_T.length, [0,1,2,3].map(r=>SHL_T.filter(a=>a[2]===r).length).join(',')]; })()""")
    ok(r[0]>800 and r[1]==14 and r[2]>=12 and r[3]>r[1] and r[6]==12 and r[7]=='3,3,3,3', '1 salen 14 conchas en la arena cada 20 min (12 distintas, 3 de cada rareza); después de una tormenta salen %d %s'%(r[3],r))
    r=await ev("""(()=>{ const cur=Math.floor(Date.now()/1000/SHL.SLOT), e=shlList(cur)[0]; player.pos.set(e.x+3,terrainH(e.x,e.z)+.05,e.z); __run(.8); const vis=SHL.vis.has(e.key);
      const n0=invCount('cc:'+e.id); player.pos.set(e.x+.4,terrainH(e.x,e.z)+.05,e.z); __run(.6); return [vis, invCount('cc:'+e.id)-n0, SHL.got.has(e.key), SHL.vis.has(e.key), SHL.seen[e.id]>0, itStack('cc:'+e.id), !!ITEMS['cc:'+e.id].icon]; })()""")
    ok(r==[True,1,True,False,True,True,True], '1b al pasar encima la recoges: va a tu inventario (se juntan en montones) y a tu colección %s'%r)

    # 2. Tortu: vender conchas y motos
    r=await ev("""(()=>{ invAdd('cc:nautilo',1); invAdd('cc:almeja',2); coins=0; addCoins(1000); const c0=coins; openFishOv('shop'); fishTab='conchas'; renderFishOv(); const rows=ui('fishBody').querySelectorAll('.fish-row').length, cells=ui('fishBody').querySelectorAll('.shl-cell').length;
      ui('fishBody').querySelector('.fish-all').click(); const got=coins-c0; return [rows>=2, cells, got>=156, invHasAny(k=>k.startsWith('cc:'))]; })()""")
    ok(r==[True,12,True,False], '2 Tortu compra las conchas (las raras valen más) y enseña tu colección de 12 %s'%r)
    r=await ev("""(()=>{ fishTab='motos'; renderFishOv(); const rows=[...ui('fishBody').querySelectorAll('.fish-row')]; const c0=coins; rows[0].querySelector('.sbtn').click(); closeFishOv(); return [rows.length, c0-coins, [...JSK.own].join(','), JSK.eq, JSK.st]; })()""")
    ok(r==[4,350,'0',0,0], '2b Tortu vende 4 motos acuáticas: la compras una vez y queda lista %s'%r)

    # 3. la moto: junto a la tienda, del lado contrario al barco; solo su dueño la maneja
    r=await ev("""(()=>{ const s=jskSlot(myUid), [lx,lz]=pL(s.x,s.z); const [x,z]=pW(-7.3,lz); player.pos.set(x,groundAt(x,z,PIER.Y+2),z); player.vel.set(0,0,0); __run(.8);
      const a=(jskActions()||[])[0]; return [+lx.toFixed(1), SHIP_DOCK[0]>0, lz>PIER.PZ0 && lz<PIER.PZ1, tblWaterAt(s.x,s.z)!==null, a&&a.label, !!JSK.mesh && JSK.mesh.visible]; })()""")
    ok(r[0]<-8 and r[1] and r[2] and r[3] and r[4]=='🚤 Subirse a mi moto' and r[5], '3 tu moto flota junto a la plataforma de Tortu, del lado contrario al barco, y te subes desde la orilla %s'%r)
    r=await ev("""(()=>{ (jskActions()||[])[0].run(); const k=player.pg&&player.pg.k, R=JSK.ride; let mx=0; __run(3,()=>{ keys.KeyW=true; keys.ShiftLeft=true; mx=Math.max(mx,R.v); }); keys.KeyW=false; keys.ShiftLeft=false;
      const pr=seaPresence().js, lab=(jskActions()||[])[0].label; return [k, +mx.toFixed(1), JSON.stringify(pr), lab, JSK.mesh.position.distanceTo(new THREE.Vector3(R.x,JSK.mesh.position.y,R.z))<.01, player.pos.y>R.y+.5]; })()""")
    ok(r[0]=='jet' and r[1]>12 and r[2]=='[0,1]' and r[3]=='Bajarse' and r[4] and r[5], '3b manejas la moto por el mar (hasta %s m/s) sentado arriba; los demás te ven en ella %s'%(r[1],r))
    r=await ev("""(()=>{ const R=JSK.ride; let t=0; R.h=Math.atan2(-R.x,-R.z); __run(40,()=>{ keys.KeyW=true; t++; }); keys.KeyW=false; const wat=terrainH(R.x,R.z)<SEA_Y+.2; jskGetOff(); __run(.5); return [wat, JSK.st, player.pg, JSON.stringify(seaPresence().js).slice(0,5)]; })()""")
    ok(r[0] and r[1]==2 and r[2] is None and r[3]=='[0,2,', '3c la moto no se sube a la arena; si te bajas lejos del muelle, se queda flotando donde la dejaste %s'%r)
    r=await ev("""(()=>{ JSK.st=0; const fake={uid:'ana0001', name:'Ana', pos:new THREE.Vector3(), target:new THREE.Vector3(), obj:new THREE.Object3D(), facing:0}; mp.remotes.set('~ana',fake);
      seaParse(fake,{js:[2,0]}); __run(.5); const S=JSK.rem.get(fake), s=jskSlot('ana0001'), [lx,lz]=pL(s.x,s.z); const [x,z]=pW(-7.3,lz); player.pos.set(x,groundAt(x,z,PIER.Y+2),z); const myS=jskSlot(myUid);
      const near=Math.hypot(myS.x-player.pos.x,myS.z-player.pos.z)<3.6; __run(.3); const a=(jskActions()||[])[0]; return [!!(S&&S.m&&S.m.visible), S&&S.id, near || (a&&a.label.startsWith('🔒')), a&&a.label, a&&!!a.disabled]; })()""")
    ok(r[0] and r[1]==2 and r[2], '3d la moto de otro jugador también se ve junto a la tienda, pero no la puedes manejar %s'%r)
    await ev("(()=>{ mp.remotes.delete('~ana'); __run(.6); return 1; })()")

    # 4. la botella y el mapa del tesoro
    r=await ev("""(()=>{ const e=shlList(Math.floor(Date.now()/1000/SHL.SLOT))[2]; player.pos.set(e.x,terrainH(e.x,e.z)+.05,e.z); __run(.3); BOT.b=null; BOT.nextT=0; __run(.4); const b=BOT.b; if(!b) return ['sin botella'];
      const d=Math.hypot(b.x-player.pos.x,b.z-player.pos.z), t=terrainH(b.x,b.z); player.pos.set(b.x+1,Math.max(waterSurfaceY(b.x,b.z),groundAt(b.x,b.z,SEA_Y+3)),b.z); __run(.3); const a=(seaActions()||[])[0];
      const c0=coins, R0=Math.random; Math.random=()=>.9; botOpen(); Math.random=R0; return [d>25 && d<200, t<SEA_Y+.6, a&&a.label, coins-c0>=8, BOT.b, BOT.nextT>Date.now()+5*60000]; })()""")
    ok(r[0] and r[1] and r[2]=='🍾 Abrir la botella' and r[3] and r[4] is None and r[5], '4 cada rato llega una botella a la orilla (cerca de ti); al abrirla trae monedas, un regalito o un mapa %s'%r)
    r=await ev("""(()=>{ const P=player.pos; BOT.b={x:P.x+.5, z:P.z, exp:Date.now()+60000}; const R0=Math.random; let k=0; Math.random=()=>(k++===0?.1:R0()); botOpen(); Math.random=R0; __run(.6);
      const m=TQ.m, t=m&&terrainH(m.x,m.z), d=m&&Math.hypot(m.x-P.x,m.z-P.z); return [!!m, invCount('tmapa'), t<SEA_Y-5 && t>SEA_Y-20, d<900, JSON.stringify(seaPresence().tq||0).length>10]; })()""")
    ok(r==[True,1,True,True,True], '4b el mapa del tesoro: aparece un cofre en lo hondo del mar, de tu lado de la isla %s'%r)
    r=await ev("""(()=>{ const i=INV.findIndex(S=>S&&S.k==='tmapa'); const canDrop=(()=>{ const n=invCount('tmapa'); invDrop(i,1); return invCount('tmapa')<n; })(); if(i>=INV_BAR) invToHand(i); else { selectedSlot=i; holding=true; applyHeld(); }
      __run(.4); const h=document.getElementById('tqHud'); const before=mapLast; drawMap(true); return [canDrop, heldItem(), !!h && !h.hidden, h&&h.textContent.includes(' m')]; })()""")
    ok(r==[False,'tmapa',True,True], '4c el mapa no se puede tirar; en la mano te dice hacia dónde y a cuántos metros está el tesoro %s'%r)
    r=await ev("""(()=>{ const m=TQ.m, y=terrainH(m.x,m.z); player.pos.set(m.x+1.4,y+.4,m.z); player.swim=true; __run(.4); const a=(seaActions()||[])[0]; const vis=TQ.g.size; const c0=coins; a.run(); __run(.6);
      return [a.label, vis, coins-c0>=60, TQ.m, invCount('tmapa'), TQ.g.size, document.getElementById('tqHud').hidden]; })()""")
    ok(r[0]=='🏴‍☠️ Abrir el cofre del tesoro' and r[1]==1 and r[2] and r[3] is None and r[4]==0 and r[5]==0 and r[6], '4d buceas hasta el cofre y te llevas el tesoro; el mapa y el cofre se acaban %s'%r)
    # el cofre de otro: lo ves, lo abres primero y te lo da su dueño
    r=await ev("""(()=>{ const fake={uid:'beto0001', name:'Beto', pos:new THREE.Vector3(), target:new THREE.Vector3(), obj:new THREE.Object3D(), facing:0}; mp.remotes.set('~beto',fake);
      const P=player.pos, x=P.x+1, z=P.z; seaParse(fake,{tq:['cofreB',x,z]}); __run(.3); const e=tqNear(); const lab=(seaActions()||[])[0]; lab.run(); const cl=JSON.stringify(seaPresence().tqc);
      seaParse(fake,{tq:null, tqg:[['cofreB',myUid]]}); const c0=coins; __run(.8); mp.remotes.delete('~beto'); return [!!e && !e.own, lab.label.includes('Beto'), cl===JSON.stringify(['beto0001','cofreB']), coins-c0>=60, TQ.claim]; })()""")
    ok(r==[True,True,True,True,None], '4e el cofre de otro jugador también se ve: si lo encuentras y lo abres primero, te llevas su tesoro %s'%r)
    r=await ev("""(()=>{ TQ.m={id:'miCofre', x:player.pos.x+50, z:player.pos.z}; invAdd('tmapa',1); const fake={uid:'cata0001', name:'Cata', pos:new THREE.Vector3(), target:new THREE.Vector3(), obj:new THREE.Object3D(), facing:0}; mp.remotes.set('~cata',fake);
      const room=mp.room; mp.room=mp.room||{fake:1}; seaParse(fake,{tqc:[myUid,'miCofre']}); TQ.chkT=0; __run(.3); const g=JSON.stringify(seaPresence().tqg); mp.room=room; mp.remotes.delete('~cata');
      return [TQ.m, invCount('tmapa'), g.includes('cata0001')]; })()""")
    ok(r==[None,0,True], '4f si otro abre tu cofre primero, se lo lleva él (y tu mapa se acaba) %s'%r)

    # 5. el cofre del barco hundido
    r=await ev("""(()=>{ localStorage.removeItem('mundoPelucheCofreBarco'); WRK.chk=0; __run(.1); const p=wrkPos(); player.pos.set(p.x+1.2,p.y,p.z); player.swim=true; player.vel.set(0,0,0); const full0=WRECK.coins.every(c=>c.visible); const a=wrkActions()[0]; const c0=coins; a.run(); WRK.chk=0; __run(.1);
      const b=wrkActions(); return [a.label, coins-c0>=12, full0, WRECK.coins.some(c=>c.visible), b&&b[0].label.startsWith('Cofre vacío'), b&&b[0].disabled]; })()""")
    ok(r==['Abrir el cofre del barco',True,True,False,True,True], '5 el cofre del barco hundido ya se abre: premio chico, y se vuelve a llenar en 30 min (sin monedas mientras) %s'%r)

    # 6. las ballenas
    r=await ev("""(()=>{ const s=jskSlot(myUid); player.pos.set(s.x,PIER.Y+.1,s.z); __run(.3); const T0=Date.now(); let sp=0, top=-99; const L=[]; for(let k=0;k<70;k++){ const t=T0+k*500; Date.now=()=>t; __run(.1); sp=Math.max(sp,WHL.sp.filter(q=>q.visible).length); for(const W of WHL.L){ top=Math.max(top,W.o.position.y+.36*W.s); } }
      const W=WHL.L[0], [lx,lz]=pL(W.o.position.x,W.o.position.z); let dry=0; for(const W2 of WHL.L){ const p=W2.o.position; if(terrainH(p.x,p.z)>p.y-.36*W2.s) dry++; }
      return [WHL.L.length, WHL.L.every(W=>W.o.visible), +lx.toFixed(0), lz>PIER.PZ1, sp>8, +(top-SEA_Y).toFixed(2), dry]; })()""")
    ok(r[0]==2 and r[1] and r[2]<-20 and r[3] and r[4] and 0<r[5]<1.5 and r[6]==0, '6 una mamá ballena y su bebé nadan del lado derecho de la tienda de Tortu, salen a respirar y echan agua %s'%r)

    # 7. adornos de conchas para la casita
    r=await ev("""(()=>{ const D=DECO.filter(d=>d.shell); const K=HK_BY['d'+DECO.indexOf(D[0])]; invAdd('cc:perla',1); const n0=invCount('cc:perla'); const i=INV.findIndex(S=>S&&S.k==='cc:perla'); shlToHouse(i); const id=DECO.findIndex(d=>d.shell==='perla');
      return [D.length, D.every(d=>!d.price), edList(true).some(K=>K.shell), H_SMALL.has('Concha con perla'), n0-invCount('cc:perla'), HS.inv['d'+id+':0']]; })()""")
    ok(r==[12,True,False,True,1,1], '7 las conchas se vuelven adornos de tu casita (no se compran: salen de tu inventario) %s'%r)

    ok(not errs and not cerr, 'sin errores %s %s'%(errs[:3],cerr[:3]))
    await b.close()
asyncio.run(m())
