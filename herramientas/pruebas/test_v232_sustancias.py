# v232 (Modo libre): 🪣 Sustancias: agua, slime, lodo, miel, pintura y espuma. Se echan con la cubeta (Echar · Chorro · Listo),
# se extienden por el piso según qué tan espesas son, los bloques las detienen, lo que pisa deja huella (el agua se rellena, el
# lodo no), el lodo y la miel te frenan, la pintura mancha los bloques y deja huellitas, la espuma se deshace sola, y con
# «Chorro: 🔮 bola» se carga una bola que sale volando y revienta al chocar (más o menos según qué tan espesa es).
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.033); update(.033,t); } };
  window.__CLR=()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); FREE.hold=null; freeSelect(null); };
  window.__AT=(x,z)=>{ player.pos.set(FREE.X+x,FREE.Y+.05,FREE.Z+z); player.vel.set(0,0,0); player.vy=0; player.facing=0; yaw=Math.PI; FREE.ppPrev=null; __S(2); };
  window.__LOOK=(x,y,z)=>{ camMode='first'; camera.position.set(player.pos.x,player.pos.y+1.6,player.pos.z); camera.lookAt(x,y,z); camera.updateMatrixWorld(); };
  window.__UPQ=(I,k)=>{ const m=new THREE.Matrix4(), q=new THREE.Quaternion(), p=new THREE.Vector3(), s=new THREE.Vector3(); I.getMatrixAt(k,m); m.decompose(p,q,s); return [new THREE.Vector3(0,0,1).applyQuaternion(q).y, p.y]; }; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type=='warning' and ('juguetes' in m.text or 'gadgets' in m.text) else None)
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev("(()=>{ freeEnter(); return 1; })()"); await ev(STEP)
    H="""window.__LOOKAT=(x,z)=>{ camMode='first'; camera.position.set(player.pos.x,player.pos.y+1.6,player.pos.z); camera.lookAt(x,FREE.Y,z); camera.updateMatrixWorld(); };
      window.__AREA=(p)=>{ let n=0, mx=0, v=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===p && C.h[i]>.0015){ n++; mx=Math.max(mx,C.h[i]); v+=C.h[i]*.04; } return [n,+mx.toFixed(3),+v.toFixed(4)]; };
      window.__H=(x,z)=>{ const q=suAt(x,z); return q?+q[1].toFixed(3):0; }; 1"""
    await ev(H)
    # 1. el menú y los botones
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); FREE.tab='sustancias'; try{ freeRenderBox(); }catch(e){} const cards=[...document.querySelectorAll('#freeGrid .free-item, #freeBox .free-item')].map(c=>c.textContent.trim()).filter(Boolean);
      freeSelect({k:'s',a:1,b:0}); __S(2); const L=[]; for(let i=0;i<5;i++){ const A=freeActions(); L.push(A.map(a=>a&&a.label).join(' · ')); A[1].run(); } const A=freeActions(); A[2].run(); return [cards, L, FREE.sel, SU_T.filter(Boolean).map(T=>T.n)]; })()""")
    ok(r[3]==['Agua','Slime','Lodo','Miel','Pintura','Espuma'], 'hay 6 sustancias: %s'%r[3])
    ok(r[1][0]=='🪣 Echar · Chorro: chico · Listo' and r[1][1].endswith('mediano · Listo') and r[1][2].endswith('grande · Listo') and r[1][3]=='🔮 Cargar bola · Chorro: 🔮 bola · Listo' and r[1][4]==r[1][0] and r[2] is None, 'con la cubeta: «Echar · Chorro · Listo»; Chorro cambia chico → mediano → grande → 🔮 bola; «Listo» la guarda %s'%r[1])
    # 2. echar: un toque echa un chorrito; mantenerlo echa más
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); freeSelect({k:'s',a:1,b:0}); SU.mode=0; __S(2); __LOOKAT(FREE.X-20,FREE.Z-17); suHoldStart(); suHoldEnd(); const a=SU.vol; SU.holdEnd=0;
      __LOOKAT(FREE.X-20,FREE.Z-17); suHoldStart(); SU.hold.t-=0; for(let i=0;i<60;i++){ __LOOKAT(FREE.X-20,FREE.Z-17); suTick(1/30); } suHoldEnd(); const b=SU.vol; SU.holdEnd=0; SU.mode=2; __LOOKAT(FREE.X-23,FREE.Z-17); suHoldStart(); for(let i=0;i<30;i++){ __LOOKAT(FREE.X-23,FREE.Z-17); suTick(1/30); } suHoldEnd(); const c=SU.vol-b;
      freeSelect(null); camMode='third'; return [+a.toFixed(4), +(b-a).toFixed(4), +c.toFixed(4), __H(FREE.X-20,FREE.Z-17)>0]; })()""")
    ok(r[0]>=.004 and abs(r[1]-.05)<.01 and abs(r[2]-.16)<.03 and r[3], 'un toque echa un chorrito (%s m³); 2 s con el chorro chico echan %s m³ y 1 s con el grande %s m³'%(r[0],r[1],r[2]))
    # 3. cómo se extiende cada una
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); [1,2,3,4,5,6].forEach((p,k)=>suPour(FREE.X-30+k*6,FREE.Z+10,p,3,.05,.3)); const A=[]; __S(30); A.push([1,2,3,4,5,6].map(__AREA)); __S(90); A.push([1,2,3,4,5,6].map(__AREA)); return A; })()""")
    a1,a2=r; area=lambda i:a2[i][0]; alto=lambda i:a2[i][1]
    ok(area(0)>area(1)>area(2) and area(0)>area(3) and alto(2)>alto(1)>alto(0), 'el agua se extiende más y queda delgadita; el slime menos y el lodo casi nada (amontonado) %s'%[x[:2] for x in a2])
    ok(a2[3][0]>a1[3][0] and a1[3][0]<a1[0][0], 'la miel se va extendiendo despacito (%s → %s cuadritos)'%(a1[3][0],a2[3][0]))
    ok(alto(5)>alto(1) and a2[5][2]<a1[5][2], 'la espuma queda alta y esponjosa, y se va deshaciendo sola (%s → %s m³)'%(a1[5][2],a2[5][2]))
    # 4. los bloques la detienen; desde arriba de un bloque escurre al piso
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); const X=FREE.X-10.5, Z=FREE.Z-10.5; freeAddStatic({k:'b',a:0,b:0},X+1,FREE.Y,Z,0); suPour(X,Z,1,0,.03,.3); __S(60); const dentro=__H(X+1,Z), antes=__H(X-.6,Z);
      freeAddStatic({k:'b',a:0,b:1},X+6,FREE.Y,Z,0); suPour(X+6,Z,2,0,.06,.25); __S(150); const top=__H(X+6,Z), piso=Math.max(__H(X+6.65,Z),__H(X+5.35,Z),__H(X+6,Z+.65),__H(X+6,Z-.65)); return [dentro, antes>0, top, piso]; })()""")
    ok(r[0]==0 and r[1], 'un bloque es pared: el agua no se mete en él %s'%r)
    ok(r[3]>0, 'el slime que echas arriba de un bloque escurre por las orillas hasta el piso %s'%r)
    # 5. huellas: en el lodo se quedan, en el agua se rellenan
    r=await ev("""(()=>{ const out={}; for(const [p,v] of [[3,.16],[1,.05],[2,.1]]){ __CLR(); suClear(); __AT(-20,-20); const X=FREE.X-10, Z=FREE.Z+20; suPour(X,Z,p,0,v,.7); __S(p===1?60:20); const h0=__H(X,Z);
        player.pos.set(X-1.4,FREE.Y+.05,Z); for(let i=0;i<40;i++){ player.pos.x+=.07; player.vel.set(2.1,0,0); __S(1); } const h1=__H(X,Z); player.pos.set(X+5,FREE.Y+.05,Z+5); __S(60); const off=[[.4,.7],[-.4,.7],[.4,-.7],[-.4,-.7]].map(([a,b])=>__H(X+a,Z+b)); out[SU_T[p].id]=[+h0.toFixed(3),+h1.toFixed(3),+__H(X,Z).toFixed(3),+(off.reduce((s,v)=>s+v,0)/4).toFixed(3)]; } return out; })()""")
    L,A,S=r['lodo'],r['agua'],r['slime']
    ok(L[1]<L[0]*.4 and L[2]<L[0]*.5, 'al caminar por el lodo queda tu huella y se queda marcada %s'%L)
    ok(A[2]>A[3]*.75 and A[2]>0, 'en el agua también la abres, pero se vuelve a llenar: queda igual que a los lados %s'%A)
    ok(S[1]<S[0]*.5 and S[2]>S[1], 'en el slime se va cerrando poco a poco %s'%S)
    # 6. te frenan
    r=await ev("""(()=>{ const out={}; for(const p of [1,3,4]){ __CLR(); suClear(); __AT(-20,-20); const X=FREE.X-10, Z=FREE.Z-10; suPour(X,Z,p,0,.25,1.2); __S(5); player.pos.set(X,FREE.Y+.05,Z); player.vel.set(0,0,0); __S(12); out[SU_T[p].id]=[+SU.slow.toFixed(2), SU.slip]; } return out; })()""")
    ok(r['agua'][0]>.85 and r['agua'][1] and r['lodo'][0]<.7 and r['miel'][0]<.5, 'el agua casi no te frena (y resbalas un poco), el lodo te frena y la miel más %s'%r)
    # 7. la pintura mancha bloques y deja huellitas
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); const X=FREE.X-10.5, Z=FREE.Z-10.5; const o=freeAddStatic({k:'b',a:0,b:9},X+1,FREE.Y,Z,0); suPour(X,Z,5,6,.04,.35); __S(40); const col=FREE.objs.find(q=>q.box.min.x<X+1&&q.box.max.x>X+1).sel.b;
      player.pos.set(X-.3,FREE.Y+.05,Z-.8); player.vel.set(0,0,0); __S(2); for(let i=0;i<60;i++){ player.pos.z-=.06; player.vel.set(0,0,-1.8); player.facing=Math.PI; __S(1); } let n=0; for(const C of SU.list) for(let k=0;k<256;k++){ if(C.t[k]===5 && C.h[k]>0 && C.h[k]<.006){ const [x,z]=suXZ(C,k); if(z<Z-1.2) n++; } }
      for(let i=0;i<20;i++) __S(30); let m=0; for(const C of SU.list) for(let k=0;k<256;k++){ if(C.t[k]===5 && C.h[k]>0 && C.h[k]<.006){ const [x,z]=suXZ(C,k); if(z<Z-1.2) m++; } } return [col, n, m]; })()""")
    ok(r[0]==6, 'la pintura que toca un bloque lo pinta de su color (%s)'%r[0])
    ok(r[1]>=3 and r[2]<r[1], 'al salir de la pintura dejas huellitas de color (%s) que se van borrando (%s después de 20 s)'%(r[1],r[2]))
    # 8. la bola
    r=await ev("""(()=>{ const out={}; for(const p of [1,3,4,5]){ __CLR(); suClear(); __AT(-20,-20); const X=FREE.X-20, Z=FREE.Z-14; const o=freeAddStatic({k:'b',a:0,b:9},X,FREE.Y,Z,0); freeAddStatic({k:'b',a:0,b:9},X,FREE.Y+1,Z,0);
        player.pos.set(X,FREE.Y+.05,Z-4); player.facing=0; yaw=Math.PI; freeSelect({k:'s',a:p,b:2}); SU.mode=3; __S(2); camMode='first'; camera.position.set(X,FREE.Y+1.5,Z-4); camera.lookAt(X,FREE.Y+1.2,Z); camera.updateMatrixWorld();
        SU.holdEnd=0; suHoldStart(); SU.hold.t-=1800; const r0=+suBallR(1.8).toFixed(2); suHoldEnd(); const nb=SU.balls.length; let hitT=0; for(let i=0;i<90;i++){ __S(1); if(!hitT && !SU.balls.length) hitT=i; }
        let far=0, n=0; for(const C of SU.list) for(let k=0;k<256;k++) if(C.t[k]===p && C.h[k]>.0015){ const [x,z]=suXZ(C,k); far=Math.max(far,Math.hypot(x-X,z-(Z-.5))); n++; } out[SU_T[p].id]=[r0,nb,hitT,+far.toFixed(2),n,+SU.vol.toFixed(3), FREE.objs.some(q=>q.sel.k==='b' && q.sel.b===2)?2:FREE.objs.map(q=>q.sel.b).join('')]; freeSelect(null); camMode='third'; } return out; })()""")
    ok(all(v[1]==1 and 0<v[2]<60 and v[4]>0 for v in r.values()), 'la bola se carga, sale volando y revienta al chocar con el bloque %s'%{k:v[:3] for k,v in r.items()})
    ok(r['agua'][3]>1.6 and r['lodo'][3]<r['agua'][3]*.75, 'el agua revienta en gotitas que caen lejos (hasta %s m); el lodo cae casi junto, como plasta (%s m)'%(r['agua'][3],r['lodo'][3]))
    ok(r['pintura'][6]==2, 'la bola de pintura pinta el bloque donde pega (%s)'%r['pintura'][6])
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); const X=FREE.X-20, Z=FREE.Z-14; freeAddStatic({k:'b',a:0,b:9},X,FREE.Y,Z,0); suLaunch(4,0,.3,[X,FREE.Y+.6,Z-1.5,0,0,8]); __S(10); const v1=SU.vol, e=SU.emit.length; __S(60); return [+v1.toFixed(3), e, +SU.vol.toFixed(3)]; })()""")
    ok(r[1]==1 and r[2]>r[0], 'la bola de miel no revienta: escurre despacito al pie del bloque (%s → %s m³)'%(r[0],r[2]))
    # 9. quitar con el bote de basura y con la escoba; guardar
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); suPour(FREE.X-20,FREE.Z-16,2,0,.04,.3); suPour(FREE.X-16,FREE.Z-16,1,0,.03,.3); __S(10); const v0=+SU.vol.toFixed(3); freeSetDel(true); __S(1); __LOOKAT(FREE.X-20,FREE.Z-16); FREE.tgt=null; freeRemove(); const v1=+SU.vol.toFixed(3); freeSetDel(false);
      suPour(FREE.X-20,FREE.Z-16,6,0,.05,.3); suPour(FREE.X-10,FREE.Z-10,5,4,.05,.3); __S(5); suRecount(); const v2=SU.vol; FREE.ctx='libre'; freeSave(); FREE.loaded=null; freeLoad(); suRecount(); const v3=SU.vol, ty=new Set(); for(const C of SU.list) for(let k=0;k<256;k++) if(C.t[k]) ty.add(C.t[k]);
      freeWipeMine(); camMode='third'; return [v0, v1, +v2.toFixed(3), +v3.toFixed(3), [...ty].sort().join(''), SU.list.length, SU.vol]; })()""")
    ok(r[1]<r[0] and r[1]>0, 'con el bote de basura quitas el charco al que apuntas (el otro se queda) %s'%r[:2])
    ok(abs(r[3]-r[2])<r[2]*.08 and r[4]=='156', 'se guardan: al volver al modo libre siguen ahí (%s → %s m³)'%(r[2],r[3]))
    ok(r[5]==0 and r[6]==0, 'la escoba las limpia todas %s'%r[5:])
    # 10. las pelotas y lo que tarda
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); const X=FREE.X-10, Z=FREE.Z-10; const a=freeAddDyn('balon',X-3,FREE.Y,Z+3); a.v.set(6,0,0); __S(60); const libre=a.root.position.x-(X-3);
      suPour(X,Z,4,0,.5,1.2); __S(5); const b=freeAddDyn('balon',X-1.5,FREE.Y,Z); b.v.set(6,0,0); __S(60); const miel=b.root.position.x-(X-1.5);
      suClear(); [1,2,3,4,5,6].forEach((p,k)=>suPour(FREE.X-30+k*6,FREE.Z+10,p,3,.06,.3)); const t0=performance.now(); for(let i=0;i<60;i++) suTick(1/30); const ms=(performance.now()-t0)/60; __S(400); const t1=performance.now(); for(let i=0;i<60;i++) suTick(1/30); const ms2=(performance.now()-t1)/60;
      return [+libre.toFixed(2), +miel.toFixed(2), +ms.toFixed(2), +ms2.toFixed(3), SU.list.filter(C=>C.aw>0).length]; })()""")
    ok(r[1]<r[0]*.6, 'una pelota que rueda entra a la miel y se frena (%s m contra %s m sin miel)'%(r[1],r[0]))
    ok(r[2]<6 and r[3]<r[2], 'con 6 charcos moviéndose tarda %s ms por cuadro, y ya quietos %s ms (aquí, sin tarjeta de video)'%(r[2],r[3]))
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close(); await b.close()
asyncio.run(m())
