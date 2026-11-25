# v262: inventario de verdad — 25 espacios (5 de la barra + 20 adentro) con montones de hasta 99; lo que había antes
# (minerales, semillas, cosecha, frutas, dulces, el pez de la mano) pasa solito al inventario y lo que no cabe va a un cofre
# grande de regalo; lo que no cabe cae al piso 15 min; recoger; vender desde el inventario (Topo, Fresita, Tortu, puestos);
# gema y cristal como cosas; peces al inventario, en la mano y a Cuco; cofres en la casita (solo el dueño); colección de dulces.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
SEED="""if(!sessionStorage.getItem('t262')){ sessionStorage.setItem('t262','1'); localStorage.clear();
  localStorage.setItem('mundoPelucheMina', JSON.stringify({pick:1, ores:{oro:12, carbon:150, diamante:3}, open:[true,true,false,false,false]}));
  localStorage.setItem('mundoPelucheHuerto', JSON.stringify({plots:[], seeds:{rabano:5, maiz:2}, crop:{tomate:4}}));
  localStorage.setItem('mundoPelucheIslas', JSON.stringify({fruta:{coco:6,mango:0,platano:9}, dulcesV:{paleta:3,chicle:0,algodon:0}, escondidos:[1,4,7]}));
  localStorage.setItem('mundoPelucheBaldes', JSON.stringify({b:[[3,3,5]], h:7}));
  localStorage.setItem('mundoPelucheMonedas','5000'); }
localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false, autoRes:false}));"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    pg=await (await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, locale='es-MX')).new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
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
    # 1. lo de antes pasó al inventario (el carbón en dos montones: 99 + 51) y las herramientas a la barra
    r=await ev("""(()=>{ hLoad(); const S=INV.map(S=>S?S.k+'*'+S.n:'-'); return [S.slice(0,5), invCount('mi:carbon'), invCount('mi:oro'), invCount('se:rabano'), invCount('co:tomate'), invCount('fr:platano'), invCount('du:paleta'), invCount('pz:7'),
      Object.keys(mine.ores).length, Object.keys(farm.seeds).length, JI2.fruit.platano, DI2.cv.paleta, player.hand, INV.filter(S=>S && S.k==='mi:carbon').map(S=>S.n), CF.L.length]; })()""")
    ok(r[0]==['map*1','bow*1','flag*1','book*1','lamp*1'] and r[1]==150 and r[2]==12 and r[3]==5 and r[4]==4 and r[5]==9 and r[6]==3 and r[7]==1 and r[8]==0 and r[9]==0 and r[10]==0 and r[11]==0 and r[12]==-1 and r[13]==[99,51] and r[14]==0,
       '1 lo que tenías (minerales, semillas, cosecha, frutas, dulces y el pez de la mano) ya está en tu inventario; el carbón en 99+51; las herramientas en la barra %s'%r)
    await ev("startGame()"); await pg.wait_for_timeout(1500)
    await ev("""window.requestAnimationFrame=()=>0; window.__run=(sec,fn)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); if(fn) fn(i); update(.05,t); } }; 1""")
    # 2. la pantalla del inventario: 20 espacios, la colección de dulces arriba, mover, juntar y cambiar de lugar
    r=await ev("""(()=>{ openInv(); const g=ui('invGrid'); const out=[g.children.length, ui('invCol').textContent.trim()];
      const iOro=INV.findIndex(S=>S && S.k==='mi:oro'); invTap(iOro); out.push(ui('invSide').textContent.includes('Oro'), ui('invSide').textContent.includes('Topo'));
      invTap(2); out.push(INV[2] && INV[2].k, INV[iOro] && INV[iOro].k, hotbar[2]);   // el oro a la barra (la bandera se va adentro)
      const c=INV.findIndex(S=>S && S.k==='mi:carbon' && S.n===51); invTap(c); const c2=INV.findIndex((S,i)=>S && S.k==='mi:carbon' && i!==c); invTap(c2); out.push(INV.filter(S=>S && S.k==='mi:carbon').map(S=>S.n).sort((a,b)=>a-b));   // juntar: 51 → 99 (completa) y sobran 51
      renderHotbar(); out.push(ui('hotbar').querySelector('[data-slot="2"]').textContent.includes('12')); closeInv(false); return out; })()""")
    ok(r[0]==20 and r[1]=='3/10' and r[2] and r[3] and r[4]=='mi:oro' and r[5]=='flag' and r[6]=='mi:oro' and r[7]==[51,99] and r[8], '2 inventario con 20 espacios, «3/10» dulces escondidos arriba, mover a la barra (cambia de lugar), juntar montones; la barra dice cuántos %s'%r)
    # 3. lo que no cabe cae al piso (a tus pies); no lo recoges hasta que te alejas y regresas; o con «Recoger»
    r=await ev("""(()=>{ player.pos.set(START.x+6,START.top+.05,START.z+6); player.vel.set(0,0,0); __run(.3);
      const free=INV.filter(S=>!S).length; const left=invAdd('mi:plata',free*99+30); const d=DR.mine.find(d=>d.k==='mi:plata'); __run(.5);
      const vis=DR.vis.has('me|'+d.id); const a=drActions(); const lab=a&&a[0].label;
      return [left, !!d, d&&d.n, vis, lab, invRoom('mi:plata')]; })()""")
    ok(r[0]==30 and r[1] and r[2]==30 and r[3] and r[4]=='Recoger Plata ×30' and r[5]==0, '3 con el inventario lleno, lo que sobra (30 de plata) cae al piso y se ve; botón «Recoger Plata ×30» %s'%r)
    r=await ev("""(()=>{ const n0=invCount('mi:plata'); invTake('mi:carbon',99); __run(.3); const n1=invCount('mi:plata');   // sin alejarte no se recoge solo
      const P=player.pos.clone(); player.pos.x+=4; __run(.2); player.pos.copy(P); __run(.3); return [n0, n1, invCount('mi:plata'), DR.mine.filter(d=>d.k==='mi:plata').length]; })()""")
    ok(r[1]==r[0] and r[2]==r[0]+30 and r[3]==0, '3b no se recoge solo si no te has alejado; al alejarte y regresar, sí (cabía de nuevo) %s'%r)
    # 4. tirar algo desde el inventario; vence a los 15 min; el mapa no se tira
    r=await ev("""(()=>{ const i=INV.findIndex(S=>S && S.k==='fr:platano'); invDrop(i,4); const d=DR.mine.find(d=>d.k==='fr:platano'); const n=invCount('fr:platano');
      const im=INV.findIndex(S=>S && S.k==='map'); invDrop(im,1); const mapOk=INV.some(S=>S && S.k==='map') && !DR.mine.some(d=>d.k==='map');
      d.exp=Date.now()-1; __run(.6); return [n, !!d, d&&d.n, mapOk, DR.mine.some(x=>x.k==='fr:platano'), JSON.parse(localStorage.getItem('mundoPelucheSuelo')).L.some(x=>x.k==='fr:platano')]; })()""")
    ok(r[0]==5 and r[1] and r[2]==4 and r[3] and not r[4] and not r[5], '4 «Tirar» deja 4 plátanos en el piso; el mapa no se tira; a los 15 min desaparece %s'%r)
    # 5. vender: el Topo compra minerales, la gema y el cristal desde el inventario
    r=await ev("""(()=>{ invTake('mi:plata',invCount('mi:plata')); jiGem(); wiCrystal(); const g=[invCount('gema'), invCount('cristal')]; const c0=coins; fishMode='mine'; mineTab='sell'; openFishOv('mine');
      const txt=ui('fishBody').textContent; const all=[...ui('fishBody').querySelectorAll('button')].find(b=>b.textContent.startsWith('Vender todo')); all.click();
      const out=[g, txt.includes('Gema de la cueva'), txt.includes('Cristal mágico'), coins-c0, invCount('mi:oro'), invCount('gema')]; closeFishOv(false); return out; })()""")
    ok(r[0]==[1,1] and r[1] and r[2] and r[3]>=12*8+40+50 and r[4]==0 and r[5]==0, '5 la gema y el cristal ahora son cosas; el Topo compra minerales, gema y cristal del inventario %s'%r)
    # 6. Fresita: comprar semillas (al inventario), plantar, cosechar al inventario y vender
    r=await ev("""(()=>{ const c=CROP_BY.rabano; farmBuy(c,5); const s1=invCount('se:rabano'); farmPlant(0,'rabano'); const s2=invCount('se:rabano'); farm.plots[0].g=1; farmHarvest(0);
      const h=invCount('co:rabano'); const c0=coins; fishMode='farm'; farmTab='sell'; openFishOv('farm'); [...ui('fishBody').querySelectorAll('button')].find(b=>b.textContent.startsWith('Vender todo')).click(); closeFishOv(false);
      return [s1, s2, h, coins-c0, invCount('co:rabano'), invCount('co:tomate')]; })()""")
    ok(r[0]==10 and r[1]==9 and r[2]==1 and r[3]==5+4*18 and r[4]==0 and r[5]==0, '6 semillas compradas al inventario, se plantan desde ahí, la cosecha llega al inventario y Fresita la compra %s'%r)
    # 7. frutas y dulces: se juntan al inventario y se venden en su puesto
    r=await ev("""(()=>{ const F=JI_FRUITS.find(f=>f.k==='mango'); F.until=0; jiPick(F); const T=DI_CTREES.find(t=>t.k==='chicle'); T.until=0; diPick(T); const a=[invCount('fr:mango'), invCount('du:chicle')];
      const c0=coins; jiSell(); diSell(); return [...a, coins-c0, invCount('fr:coco'), invCount('du:paleta')]; })()""")
    ok(r[0]==5 and r[1]==6 and r[2]==6*5+5*4+5*3+3*4+6*3 and r[3]==0 and r[4]==0, '7 frutas y dulces al inventario; los puestos compran lo del inventario %s'%r)
    # 8. peces: pescar → inventario; en la mano (barra) es «el pez de la mano»; Cuco se come uno; carnada del inventario; Tortu compra del inventario
    r=await ev("""(()=>{ fishCaught({sp:3, b:-1, mesh:new THREE.Object3D()}); fishCaught({sp:3, b:-1, mesh:new THREE.Object3D()}); const n=invCount('pz:3');
      const i=INV.findIndex(S=>S && S.k==='pz:3'); invMove(i,3); selectedSlot=3; holding=true; applyHeld(); const h=player.hand;
      player.feed={t:1.2, id:3, done:false}; updateFeed(.01); const n2=invCount('pz:3'), h2=player.hand; player.feed=null; player.busy=false;
      const bs=baitsFor(null); fishBait=1; const okb=takeBait(null,0); const n3=invCount('pz:3')+invCount('pz:7');
      return [n, h, n2, h2, bs, okb, n3]; })()""")
    ok(r[0]==2 and r[1]==3 and r[2]==1 and r[3]==3 and 1 in r[4] and r[5], '8 lo que pescas va al inventario; en la mano es el pez (player.hand); Cuco se come uno; la carnada sale del inventario %s'%r)
    r=await ev("""(()=>{ invAdd('pz:12',3); const c0=coins; fishTab='sell'; openFishOv('shop'); const t=ui('fishBody').textContent; [...ui('fishBody').querySelectorAll('button')].find(b=>b.textContent.startsWith('Vender todo')).click(); closeFishOv(false);
      return [t.includes(FISH[12].n), coins-c0>=FISH[12].p*3, INV.some(S=>S && S.k.startsWith('pz:')), holding]; })()""")
    ok(r[0] and r[1] and not r[2], '8b Tortu compra los peces del inventario %s'%r)
    # 9. en la mano: un mineral se ve en la mano del peluche; botones «Tirar uno» y «Guardar»
    r=await ev("""(()=>{ invAdd('mi:rubi',3); const i=INV.findIndex(S=>S && S.k==='mi:rubi'); invMove(i,4); useSlot(4); __run(.2); const H=plush.userData.itH; const a=itActions();
      const out=[heldItem(), !!H && H.holder.visible, H && H.model && H.model.children.length>0, a && a[0].label, a && a[1].label]; itStow(); __run(.1); out.push(plush.userData.itH.holder.visible); return out; })()""")
    ok(r[0]=='mi:rubi' and r[1] and r[2] and r[3]=='Tirar uno' and r[4]=='Guardar' and not r[5], '9 el rubí en la mano se ve; «Tirar uno» y «Guardar» %s'%r)
    # 10. cofres: el mueble está en la tienda de la casita; puesto en tu casita, «Abrir el cofre»; pasar cosas, mantener presionado, guardar/sacar todo
    r=await ev("""(()=>{ const ids=['Cofre chico','Cofre mediano','Cofre grande'].map(n=>DECO.findIndex(D=>D.n===n)); const K=ids.map(id=>HK_BY['d'+id]);
      return [ids.every(i=>i>=0), K.map(k=>k&&k.sub), K.map(k=>k&&HPRICE[k.id]), K.map(k=>k&&k.mats.length), DECO[ids[2]].chest]; })()""")
    ok(r[0] and r[1]==['muebles']*3 and r[2]==[30,60,100] and r[3]==[10,10,10] and r[4]=='g', '10 tres cofres en la tienda (Casa → Muebles), 30/60/100 monedas, 10 colores %s'%r)
    r=await ev("""(()=>{ hLoad(); const L=LOTS[0]; HS.mine=L.id; const id=DECO.findIndex(D=>D.n==='Cofre mediano'); const P=[{t:HT.PISO,i:5,j:5,lv:0,r:0,m:0,k:0},{t:hDecoT(id),k:id&7,i:6,j:6,lv:0,r:0,m:3}];
      HS.str=hpEnc(P); HS.hash=hpHash(HS.str); HS.tick=0; houseUpdate(1); const b=HS.shown.get(L.id); const it=(b&&b.ia||[]).find(q=>q.k==='chest');
      player.pos.set(it.x+.6, it.y+.05, it.z); player.vel.set(0,0,0); const a=houseActions(); return [!!it, it&&it.sz, a&&a[0].label, a&&a[0].disabled]; })()""")
    ok(r[0] and r[1]=='m' and r[2]=='Abrir el cofre' and not r[3], '10b el cofre mediano puesto en tu casita: botón «Abrir el cofre» %s'%r)
    await ev("""(()=>{ const a=houseActions(); a[0].run(); return 1; })()"""); await pg.wait_for_timeout(300)
    await pg.screenshot(path='/home/claude/trabajo/v262/cofre.png')
    r=await ev("""(()=>{ const out=[!ui('cofreOv').hidden, ui('cfGrid').children.length, ui('cfInv').children.length, ui('cfBar').children.length, ui('cfTitle').textContent];
      const i=INV.findIndex(S=>S && S.k==='se:rabano'); cfPut(i); out.push(CF.open.s.filter(Boolean).map(S=>S.k+'*'+S.n), invCount('se:rabano'));
      const im=INV.findIndex(S=>S && S.k==='map'); cfPut(im); out.push(INV.some(S=>S && S.k==='map'));
      cfAllIn(); const inside=CF.open.s.filter(Boolean).length; out.push(inside>=2, INV.slice(5).some(S=>S && itStack(S.k)));
      cfTake(0); out.push(invCount('se:rabano')); cfAllOut(); out.push(CF.open.s.filter(Boolean).length); return out; })()""")
    ok(r[0] and r[1]==20 and r[2]==20 and r[3]==5 and r[4]=='Cofre mediano' and r[5]==['se:rabano*9'] and r[6]==0 and r[7] and r[8] and not r[9] and r[10]==9 and r[11]==0,
       '10c el cofre (20 lugares) y tu inventario (20 + barra); guardar uno, el mapa no se guarda, «Guardar todo», sacar uno y «Sacar todo» %s'%r)
    r=await ev("""(()=>{ invAdd('du:algodon',30); const i=INV.findIndex(S=>S && S.k==='du:algodon'); cfPutAll('du:algodon'); const inC=CF.open.s.filter(S=>S && S.k==='du:algodon').reduce((n,S)=>n+S.n,0);
      cfClose(false); cfLoad(); const C=CF.L.find(c=>c.sz==='m'); return [inC, invCount('du:algodon'), C && C.s.filter(S=>S && S.k==='du:algodon').reduce((n,S)=>n+S.n,0), C && C.pos]; })()""")
    ok(r[0]==30 and r[1]==0 and r[2]==30 and r[3]=='m|6,6,0', '10d mantener presionado pasa todos los algodones; lo del cofre se guarda %s'%r)
    # 11. el cofre de otra persona no se abre
    r=await ev("""(()=>{ const b=HS.shown.get(HS.mine); const was=b.owner; b.owner='otro123'; const a=houseActions(); b.owner=was; return [a&&a[0].label, a&&a[0].disabled]; })()""")
    ok(r[0]=='Cofre: solo el dueño lo abre 🔒' and r[1], '11 el cofre de otro: «solo el dueño lo abre» %s'%r)
    # 12. tus objetos: tirar uno y volver a guardarlo en el editor lo regresa; borrar el diseño lo quita del inventario
    r=await ev("""(()=>{ const L=obLoad(); L.push({id:'otest1', n:'Varita', ...obClean({pieza:'estrella'})}); obStore(L); obSyncInv(); invAdd('o:otest1',1); const had=INV.some(S=>S && S.k==='o:otest1');
      const i=INV.findIndex(S=>S && S.k==='o:otest1'); invDrop(i,1); const d=DR.mine.find(d=>d.k==='o:otest1'); const gone=!INV.some(S=>S && S.k==='o:otest1');
      obOpen('otest1'); obSave(); crEl.hidden=true; CR.open=false; menuEl.hidden=true; const back=INV.some(S=>S && S.k==='o:otest1');
      obStore(obLoad().filter(o=>o.id!=='otest1')); obSyncInv(); return [had, !!d && Array.isArray(d.d), gone, back, INV.some(S=>S && S.k==='o:otest1')]; })()""")
    ok(r==[True,True,True,True,False], '12 tirar tu objeto lo deja en el piso (con su diseño); guardarlo otra vez lo regresa; borrarlo lo quita %s'%r)
    # 13. se guarda y se carga igual (y lo de antes no se vuelve a pasar)
    r=await ev("""(()=>{ const a=JSON.stringify(INV); INV.fill(null); invLoad(); return [JSON.stringify(INV)===a, Object.keys(mine.ores).length, SAVE_KEYS.includes('Inv'), SAVE_KEYS.includes('Cofres')]; })()""")
    ok(r==[True,0,True,True], '13 el inventario se guarda y se carga igual; Mi progreso incluye inventario y cofres %s'%r)
    # 14. inglés
    await ev("I18N.set('en'); openInv(); 1"); await pg.wait_for_timeout(300); t1=await ev("ui('inv').textContent")
    await ev("invAdd('mi:carbon',3); invTap(INV.findIndex((S,i)=>i>=5 && S && S.k==='mi:carbon')); 1"); await pg.wait_for_timeout(300); t2=await ev("ui('inv').textContent")
    await ev("closeInv(false); I18N.set('es'); 1"); r=[('Inventory' in t1) and ('Tap something' in t1), ('Coal' in t2) and ('Drop' in t2) and ('Sell it to Mole' in t2), t2[-160:]]
    ok(r[0] and r[1], '14 en inglés %s'%r)
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
