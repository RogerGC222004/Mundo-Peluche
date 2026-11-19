# v238b (Modo libre): las manchas quedan en el punto exacto (una bola por la espalda, un brazo, las manos que se meten en la sustancia,
# lo que agarras metido en lodo, la bola que haces), la ropa tiene su propia mancha (la nueva sale limpia; lo de abajo queda limpio al
# quitártela) y cada tela es distinta (hule: botas de lluvia, impermeable; tejido: Amigurumi, suéteres).
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.033); update(.033,t); petsUpdate(.033,t); } };
  window.__CLR=()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); FREE.hold=null; freeSelect(null); };
  window.__CLEAN=()=>{ stClear(myStn); __S(2); };
  window.__POOL=(p,dep,x0,z0,col,s)=>{ const m=SU.cs; for(let x=-1;x<=1.01;x+=m) for(let z=-1;z<=1.01;z+=m) suPour(FREE.X+(x0||0)+x,FREE.Z+(z0||0)+z,p,col||0,dep*m*m,.1,s); __S(15); };
  window.__WALK=(x0,z0,n)=>{ player.pos.set(FREE.X+x0,FREE.Y+.05,FREE.Z+z0); player.vel.set(0,0,0); __S(2); for(let i=0;i<n;i++){ stick.x=0; stick.y=-1; yaw=-Math.PI/2; __S(1); } stick.y=0; __S(2); };
  window.__WR=o=>{ let n=0, t=0; o.traverse(m=>{ if(m.isMesh && m.material && m.material.isMeshStandardMaterial){ t++; if(m.material.userData && m.material.userData.stOrig) n++; } }); return [n,t]; };
  window.__RES=()=>{ __CLR(); suClear(); FU.pts.length=0; SU.drops.length=0; __CLEAN(); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-12); __S(3); }; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type=='error' and ('shader' in m.text.lower() or 'webgl' in m.text.lower() or 'manchas' in m.text) else None)
    pg.on("console", lambda m: errs.append(m.text) if m.type=='warning' and 'manchas' in m.text else None)
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev("(()=>{ freeEnter(); return 1; })()"); await ev(STEP)


    LL="Object.values(SHOP_BY).find(it=>it.slot==='shoes' && /lluvia/i.test(it.name)).id"
    # 1. una bola de pintura que te pega por la espalda: el manchón queda en la espalda (no en la panza)
    r=await ev("""(()=>{ __RES(); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z); __S(3); plush.updateMatrixWorld(true); const P=player.pos, fw=new THREE.Vector3(0,0,1).applyQuaternion(plush.quaternion).setY(0).normalize(); const r=.13, m=new THREE.Mesh(_suSph,suBallMat(5,suCol(3),255)); FREE.g.add(m);
        SU.balls.push({x:P.x-fw.x*1.1,y:P.y+1.0,z:P.z-fw.z*1.1,vx:fw.x*7,vy:.6,vz:fw.z*7,r,p:5,c:suCol(3),s:255,v:suVolOf(r),t:.5,m}); for(let i=0;i<12 && SU.balls.length;i++) __S(1); __S(2); renderer.render(scene,camera);
        const s=myStn.sp.find(s=>s.p===5); return [s?[s.bi,+s.x.toFixed(2),+s.y.toFixed(2),+s.z.toFixed(2),+s.r.toFixed(2)]:null, +myStn.F[5].toFixed(2), myStn.U?myStn.U.uSpN.value:0, renderer.info.programs.filter(p=>p.diagnostics).length, __WR(plush)[0]]; })()""")
    ok(r[0] is not None and r[0][0]==0 and r[0][3]<-.15 and r[1]<.05 and r[2]>=1 and r[4]>0, '🎯 una bola de pintura por la espalda deja el manchón en la espalda (a %s m del centro, hacia atrás) y no en la panza (%s)'%(r[0] and r[0][3], r))
    ok(r[3]==0, '🧩 la mancha nueva se dibuja sin errores')

    # 2. en un brazo: el manchón se pega al brazo y se mueve con él
    r=await ev("""(()=>{ __RES(); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z); __S(3); plush.updateMatrixWorld(true); const P=player.pos, a=plush.userData.arms[1], t=stTip(a,new THREE.Vector3()), mid=a.getWorldPosition(new THREE.Vector3()).lerp(t,.6), sd=mid.clone().sub(P).setY(0).normalize();
        myStn.rcT=0; stSpot(plush,myStn,3,mid.clone().addScaledVector(sd,.25),.18,1,0); const s=myStn.sp[0]; myStn.fr=-1; stFrame(plush); const p0=myStn.U.uSpP.value[0].clone(); a.rotation.z+=.9; plush.updateMatrixWorld(true); myStn.fr=-1; stFrame(plush); const p1=myStn.U.uSpP.value[0].clone(); a.rotation.z-=.9;
        return [s?s.bi:null, stBones(plush).indexOf(a), stBones(plush).indexOf(a.userData.joint), +Math.hypot(p0.x-p1.x,p0.y-p1.y,p0.z-p1.z).toFixed(2)]; })()""")
    ok(r[0] in (r[1],r[2]) and r[3]>.1, '💪 lodo en el brazo: queda pegado al brazo (hueso %s) y al moverlo se va con él (%s m)'%(r[0],r[3]))

    # 3. las manos que se meten en la sustancia (brazos abajo, en un charco hondo de pintura)
    r=await ev("""(()=>{ __RES(); __POOL(5,1.3,0,0,3); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z); player.vel.set(0,0,0); __S(1); stClear(myStn); for(const a of plush.userData.arms){ a.rotation.z=0; a.rotation.x=0; } plush.updateMatrixWorld(true); myStn.hT=0; stHands(plush,myStn,.1); const q=suCell(FREE.X,FREE.Z,false), [C0,i0]=q, top=+(suB(C0,i0)+C0.h[i0]+C0.h2[i0]-FREE.Y).toFixed(2);
        const B=stBones(plush), J=plush.userData.arms.map(a=>B.indexOf(a.userData.joint)); const h=myStn.sp.filter(s=>J.includes(s.bi)); const tip=+(stTip(plush.userData.arms[0],new THREE.Vector3()).y-FREE.Y).toFixed(2); stClear(myStn); suClear(); __S(3); return [h.length, h.map(s=>s.p), tip, top]; })()""")
    ok(r[0]==2 and all(p==5 for p in r[1]), '🖐️ si metes las manos en la pintura, se te pintan las manos (%s manchones; manos a %s m, pintura hasta %s m)'%(r[0],r[2],r[3]))

    # 4. agarras una caja metida en el lodo: lodo en las manos
    r=await ev("""(()=>{ __RES(); __POOL(3,.35,0,0); const d=freeAddDyn('caja',FREE.X,FREE.Y+.25,FREE.Z,true); __S(60); player.pos.set(FREE.X-1,FREE.Y+.05,FREE.Z+2.5); __S(2); stClear(myStn); freeGrab(d); const B=stBones(plush), J=plush.userData.arms.map(a=>B.indexOf(a.userData.joint)); const h=myStn.sp.filter(s=>J.includes(s.bi) && s.p===3); try{ freeRelease(0); }catch(e){} return [h.length, +(d.root.position.y-FREE.Y).toFixed(2)]; })()""")
    ok(r[0]==2, '📦 agarras una caja que estaba metida en el lodo y se te embarran las manos (%s)'%r)

    # 5. hacer una bola de lodo te ensucia las manos
    r=await ev("""(()=>{ __RES(); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z); __S(3); FREE.sel={k:'s',a:3}; SU.hold={p:3,mode:3,t:performance.now()-1200,col:0,done:0}; for(let i=0;i<20;i++) __S(1); SU.hold=null; FREE.sel=null; if(SU.hb) SU.hb.visible=false; __S(1); const B=stBones(plush), J=plush.userData.arms.map(a=>B.indexOf(a.userData.joint)); return myStn.sp.filter(s=>J.includes(s.bi) && s.p===3).length; })()""")
    ok(r==2, '🤲 hacer una bola de lodo te deja lodo en las manos (%s)'%r)

    # 6. la ropa: cada prenda con su mancha y su tela
    r=await ev("""(()=>{ __RES(); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-12); applyOutfit(plush,Object.assign({},wardrobe.eq,{hat:'go_roja',top:'su_verde',shoes:%s})); __S(3); stTouch(myStn,3,.6,0,0); stAdd(myStn,4,'T',1,0); __S(3); renderer.render(scene,camera);
        const K=[...myStn.clm.entries()].map(([k,c])=>[k.split('|')[0],c.cls,+c.A[3].toFixed(2),+c.L[3].toFixed(2)]); let cw=0; plush.traverse(m=>{ if(m.isMesh && m.material && m.material.userData && m.material.userData.stOrig && stGKey(plush,m)) cw++; }); return [K,cw]; })()"""%LL)
    cls={k[0]:k[1] for k in r[0]}
    ok(cls.get('shoes')=='h' and cls.get('top')=='t' and cls.get('hat')=='f', '👢 cada prenda sabe de qué tela es: botas de lluvia de hule, suéter tejido, gorra de tela (%s)'%cls)
    ok(all(k[2]>.9 for k in r[0]) and r[1]>5, '👕 y cada una se mancha (%s piezas de ropa con mancha)'%r[1])
    r=await ev("""(()=>{ for(let i=0;i<4;i++) __S(150); const g=k=>{ for(const [kk,c] of myStn.clm) if(kk.startsWith(k+'|')) return c; }; return [+g('shoes').A[3].toFixed(2), +g('top').A[3].toFixed(2), +g('hat').A[3].toFixed(2), +myStn.A[3].toFixed(2), stFeet(myStn)===g('shoes')]; })()""")
    ok(r[0]<.05 and r[0]<r[3] and r[1]>r[3], '🧽 20 s después: las botas de hule ya están limpias (%s), el suéter tejido sigue más sucio (%s) que la tela normal (%s)'%(r[0],r[1],r[3]))
    ok(r[4], '🍯 lo que pisa son las botas: la miel te frena según tus botas')

    # 7. te quitas la gorra y las botas: lo de abajo está limpio; ropa nueva sale limpia
    r=await ev("""(()=>{ __RES(); applyOutfit(plush,Object.assign({},wardrobe.eq,{hat:'go_roja',top:'su_verde',shoes:%s})); __S(3); stTouch(myStn,3,.6,0,0); stAdd(myStn,4,'T',1,0); __S(3); applyOutfit(plush,Object.assign({},wardrobe.eq,{top:'su_verde'})); __S(3); const nx=myStn.X.length, top=[...myStn.clm.values()][0];
        applyOutfit(plush,Object.assign({},wardrobe.eq,{top:'su_verde',hat:'go_roja'})); __S(3); let hat=null; for(const [k,c] of myStn.clm) if(k.startsWith('hat|')) hat=c; renderer.render(scene,camera); const U=myStn.U; return [nx, +top.A[3].toFixed(2), hat?+hat.A[4].toFixed(2):null, U.uStXn.value, myStn.X.map(x=>+x.mn.y.toFixed(2))]; })()"""%LL)
    ok(r[0]==2 and r[3]==2, '🧢 al quitarte la gorra y las botas, lo que tapaban queda limpio (%s zonas: %s)'%(r[0],r[4]))
    ok(r[1]>.5, '👕 el suéter que te dejaste puesto sigue manchado (%s)'%r[1])
    ok(r[2] is not None and r[2]<.01, '🧢✨ y si te vuelves a poner una gorra, sale limpia (%s)'%r[2])
    r=await ev("""(()=>{ __S(2); const n0=myStn.X.length; stTouch(myStn,3,.5,0,0); __S(2); const n1=myStn.X.length; stClear(myStn); __S(3); applyOutfit(plush,wardrobe.eq); __S(2); return [n0,n1]; })()""")
    ok(r[1]<r[0], '🟤 si te vuelves a meter al lodo sin botas, ahora sí se te embarran las patas (zonas limpias %s → %s)'%(r[0],r[1]))

    # 8. el hule casi no se moja; el tejido se queda mojado más tiempo
    r=await ev("""(()=>{ __RES(); applyOutfit(plush,Object.assign({},wardrobe.eq,{shoes:%s})); __S(3); stTouch(myStn,1,.4,0,0); __S(2); let bo=null; for(const [k,c] of myStn.clm) if(k.startsWith('shoes|')) bo=c; const w0=+bo.A[1].toFixed(2);
        stClear(myStn); applyOutfit(plush,Object.assign({},wardrobe.eq,{body:'av_amigu'})); __S(3); stTouch(myStn,1,.6,0,0); for(let i=0;i<3;i++) __S(150); const wa=+myStn.A[1].toFixed(2); stClear(myStn); applyOutfit(plush,wardrobe.eq); __S(3); stTouch(myStn,1,.6,0,0); for(let i=0;i<3;i++) __S(150); const wf=+myStn.A[1].toFixed(2); stClear(myStn); __S(2); return [w0,wa,wf]; })()"""%LL)
    ok(r[0]<=.31, '☔ las botas de lluvia casi no se mojan (%s)'%r[0])
    ok(r[1]>r[2]+.1, '🧶 el Amigurumi (tejido) se queda mojado más tiempo que el frijolito (%s contra %s)'%(r[1],r[2]))

    # 9. lo que se manda a los amigos: los manchones y la ropa, y se lee igual
    r=await ev("""(()=>{ __RES(); applyOutfit(plush,Object.assign({},wardrobe.eq,{shoes:%s})); __S(3); stTouch(myStn,3,.4,0,0); for(let k=0;k<6;k++){ myStn.rcT=0; stSpot(plush,myStn,k%%2?5:4,new THREE.Vector3(player.pos.x+Math.cos(k)*.8,player.pos.y+.4+k*.2,player.pos.z+Math.sin(k)*.8),.2,1,0x22cc88); } __S(1); const x=stPackX(myStn), R=stNew(); R.rem=true; stUnpackX(R,x);
        const ok=R.sp.length===myStn.sp.length && R.sp.every((s,i)=>{ const q=myStn.sp[i]; return s.p===q.p && s.bi===q.bi && Math.abs(s.x-q.x)<.01 && Math.abs(s.y-q.y)<.01 && Math.abs(s.z-q.z)<.01 && Math.abs(s.r-q.r)<.013; }); const res=[x?x.length:0, ok, R.cl1.on, +R.cl1.A[3].toFixed(1), myStn.sp.length]; stClear(myStn); applyOutfit(plush,wardrobe.eq); __S(2); return res; })()"""%LL)
    ok(r[1] and r[2] and r[4]==6, '📡 los 6 manchones y la ropa manchada viajan a tus amigos y se leen igualito (%s letras)'%r[0])
    ok(r[0]<=140, 'y caben en poquito (%s letras)'%r[0])

    # 10. el Chibi y el Amigurumi también (manchón por la espalda)
    r=await ev("""(()=>{ const out=[]; for(const av of ['av_chibi','av_amigu']){ __RES(); applyOutfit(plush,Object.assign({},wardrobe.eq,{body:av})); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z); __S(3); plush.updateMatrixWorld(true); const P=player.pos, fw=new THREE.Vector3(0,0,1).applyQuaternion(plush.quaternion).setY(0).normalize(); myStn.rcT=0;
        stSpot(plush,myStn,4,new THREE.Vector3(P.x-fw.x*.9,P.y+1.1,P.z-fw.z*.9),.25,1,0); __S(2); renderer.render(scene,camera); const s=myStn.sp[0]; out.push([av, s?+s.z.toFixed(2):null, __WR(plush)[0]]); } stClear(myStn); applyOutfit(plush,wardrobe.eq); __S(3); return out; })()""")
    ok(all(x[1] is not None and x[1]<-.1 and x[2]>0 for x in r), '🧸 el Chibi y el Amigurumi también: miel en la espalda %s'%r)

    # 11. rendimiento: con 6 manchones y ropa manchada
    r=await ev("""(()=>{ __RES(); applyOutfit(plush,Object.assign({},wardrobe.eq,{hat:'go_roja',top:'su_verde',shoes:%s})); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z); __S(3); camera.position.set(FREE.X,FREE.Y+1.4,FREE.Z+2.6); camera.lookAt(FREE.X,FREE.Y+.9,FREE.Z); const T=()=>{ for(let i=0;i<3;i++) renderer.render(scene,camera); const t0=performance.now(); for(let i=0;i<10;i++){ __S(1); renderer.render(scene,camera); } return (performance.now()-t0)/10; };
        const a=T(); for(const p of [1,3,4,5,6,7]){ myStn.A[p]; stTouch(myStn,p,.4,0,0); } stAdd(myStn,4,'T',1,0); for(let k=0;k<6;k++){ myStn.rcT=0; stSpot(plush,myStn,(k%%6)+2,new THREE.Vector3(player.pos.x+Math.cos(k)*.8,player.pos.y+.4+k*.2,player.pos.z+Math.sin(k)*.8),.2,1,0x22cc88); } __S(3); const b2=T(); stClear(myStn); applyOutfit(plush,wardrobe.eq); __S(3); return [+a.toFixed(1), +b2.toFixed(1)]; })()"""%LL)
    ok(r[1]<r[0]*1.7+3, '⚡ con ropa, 6 sustancias y 6 manchones el cuadro tarda %s ms contra %s ms limpio (aquí, sin tarjeta de video)'%(r[1],r[0]))
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
