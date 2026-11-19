# v234 (Modo libre): 🪣 Sustancias, tercera ronda. Se nada en las sustancias hondas (agua y pintura normal; slime y miel muy despacito;
# en el lodo te hundes hasta la cintura; en la espuma no se nada); pueden llenar toda la planicie hasta 10 m (los lagos quietos se
# dibujan de una pieza y se guardan cortito); la 🚰 máquina de sustancias (4 salidas: goteo, fuente, regadera y manguera de 20 m).
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
    pg.on("console", lambda m: errs.append(m.text) if m.type=='warning' and ('juguetes' in m.text or 'gadgets' in m.text or 'maquina' in m.text or 'sustancias' in m.text) else None)
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev("(()=>{ freeEnter(); return 1; })()"); await ev(STEP)

    await ev("""(()=>{ window.__LAKE=(p,d,a,b)=>{ for(let ci=a;ci<=b;ci++) for(let cj=a;cj<=b;cj++){ const C=suChunk(ci,cj,true); if(C) suDec(C,'F|'+p+'|'+(p===5?'f00':'0')+'|'+Math.round(d/.003).toString(36)); } suRecount(); };
      window.__WALK=(k)=>{ const x=player.pos.x, z=player.pos.z; keys.KeyW=true; __S(k); keys.KeyW=false; return Math.hypot(player.pos.x-x,player.pos.z-z); }; return 1; })()""")
    # 1. nadar en las sustancias hondas
    g=await ev("(()=>{ __CLR(); suClear(); __AT(1.6,1.6); __S(5); return __WALK(30); })()")
    R={}
    for p in [1,5,2,4,3,6]:
      R[p]=await ev("""(()=>{ __CLR(); suClear(); __LAKE(%d,1.6,-3,3); __AT(1.6,1.6); __S(25); const q=suAt(player.pos.x,player.pos.z); const S=q?q[2]:null;
        const r=[player.swim, SU.swimP, +(player.pos.y-FREE.Y).toFixed(2), S===null?null:+(S-FREE.Y).toFixed(2)]; yaw=Math.PI; r.push(+__WALK(30).toFixed(2)); return r; })()"""%p)
    print('suelo', round(g,2), R)
    ok(R[1][0] and R[1][1]==1 and R[1][4]>g*.5, 'en el agua honda se nada normal %s'%R[1])
    ok(R[5][0] and R[5][1]==5 and R[5][4]>g*.5, 'en la pintura también %s'%R[5])
    ok(R[2][0] and R[2][1]==2 and R[2][4]<R[1][4]*.55, 'en el slime se nada muy despacito %s'%R[2])
    ok(R[4][0] and R[4][1]==4 and R[4][4]<R[1][4]*.45, 'en la miel todavía más despacito %s'%R[4])
    ok(R[3][0] and R[3][1]==3 and R[3][2]>R[1][2]+.3 and R[3][4]<R[1][4]*.5, 'en el lodo te hundes hasta la cintura y vas lento %s'%R[3])
    ok(not R[6][0] and R[6][2]<.4 and R[6][4]>g*.5, 'en la espuma no se nada: te hundes hasta el piso y casi no te frena %s'%R[6])
    # 2. llenar toda la planicie (lagos) y el tope de 10 m
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); const X0=FREE.X-30, Z0=FREE.Z-30; for(let x=0;x<40;x+=2) for(let z=0;z<40;z+=2) suPour(X0+x+1,Z0+z+1,1,0,6,1); suRecount(); const v=SU.vol;
        player.pos.set(X0+20,FREE.Y+.05,Z0+20); player.vel.set(0,0,0); const T=[]; for(let i=0;i<40;i++){ const a=performance.now(); __S(1); T.push(performance.now()-a); }
        for(let i=0;i<300;i++) __S(1); const T2=[]; for(let i=0;i<30;i++){ const a=performance.now(); __S(1); T2.push(performance.now()-a); } const avg=L=>+(L.reduce((a,b)=>a+b,0)/L.length).toFixed(1);
        const lagos=SU.list.filter(C=>C.flat).length, fm=Object.keys(SU.flatM).filter(k=>SU.flatM[k]&&SU.flatM[k].visible).length, pk=JSON.stringify(suPack()||[]); suUnpack(JSON.parse(pk)); suRecount();
        return [+v.toFixed(0), avg(T), avg(T2), lagos, fm, pk.length, +SU.vol.toFixed(0), player.swim]; })()""")
    ok(r[0]>2300 and r[6]>r[0]*.97, 'se pueden echar %s m³ de agua (toda una planicie) y se guardan %s m³'%(r[0],r[6]))
    ok(r[5]<250000, 'y se guarda (%s KB)'%(r[5]//1000))
    ok(r[1]<70 and r[2]<20, 'tarda %s ms por cuadro mientras se acomoda y %s ms ya quieta (aquí, sin tarjeta de video)'%(r[1],r[2]))
    ok(r[7], 'y en medio se nada')
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-30,-30); __LAKE(1,.8,0,6); for(const C of SU.list) suBuild(C); suFlatDraw(); const a=SU.list.filter(C=>C.flat).length, M=SU.flatM[1], tri=M&&M.visible?M.geometry.index.count/3:0, ms=SU.list.reduce((n,C)=>n+C.ms.filter(Boolean).length,0), pk=JSON.stringify(suPack()).length;
        __S(20); for(const C of SU.list) if(C.dirty) suBuild(C); return [a, tri, ms, pk, SU.list.filter(C=>C.flat).length]; })()""")
    ok(r[0]==49 and r[1]==98 and r[2]==0, 'un lago quieto se dibuja de una pieza: 49 trozos en %s triangulitos, sin mallas aparte %s'%(r[1],r))
    ok(r[3]<49*30, 'y se guarda cortito (%s letras para 49 trozos)'%r[3])
    ok(r[4]>=20, 'mientras se acomoda, lo de en medio sigue siendo lago (%s trozos)'%r[4])
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); __LAKE(4,9.95,0,0); const x=FREE.X+1.6, z=FREE.Z+1.6; const got=suPour(x,z,4,0,2,.6); suRecount(); let mx=0; for(const C of SU.list) for(let i=0;i<256;i++) mx=Math.max(mx,suB(C,i)+C.h[i]+C.h2[i]-FREE.Y); return [+got.toFixed(3), +mx.toFixed(3)]; })()""")
    ok(r[0]<.2 and r[1]<=10.001, 'la sustancia no sube de 10 m (echando 2 m³ arriba de una de 9.95 m solo cupieron %s m³; lo más alto: %s m)'%(r[0],r[1]))
    # 3. la máquina de sustancias: cada salida echa en su lugar
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); const o=freeAddStatic({k:'p',a:'fuentes',b:FU_DEF},FREE.X,FREE.Y,FREE.Z,0,true); const C=fuCfg(o);
        return [!!o, o.solid, C.map(c=>c.on), C[1].p, FREE_PHYS_BY.fuentes.hid, fuNearActions()===null]; })()""")
    ok(r[0] and r[1] and r[2]==[0,0,0,0] and r[3]==1, 'se pone la máquina (choca contigo) y sale apagada (v235; la fuente trae agua) %s'%r)
    W=[]
    for k,(p,q,x) in enumerate([(3,2,0),(1,2,2),(5,2,2),(4,2,1)]):
      W.append(await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); const o=freeAddStatic({k:'p',a:'fuentes',b:0},FREE.X,FREE.Y,FREE.Z,1,true); const C=[0,1,2,3].map(i=>({on:i===%d?1:0,p:%d,q:%d,x:%d,col:6})); fuSet(o,C);
          let hi=0; for(let i=0;i<90;i++){ __S(1); for(const P of FU.pts) hi=Math.max(hi,P.y-FREE.Y); } suRecount(); const S=fuSrc(o,%d,fuCfg(o)[%d]); let v=FU.pts.reduce((a,P)=>a+(P.v||0),0)/.04, vv=v, cx=0, cz=0, rmax=0;   /* (v235: + lo que va volando) */ const quad=[0,0,0,0];
          for(const Q of SU.list) for(let i=0;i<256;i++){ const h=Q.h[i]+Q.h2[i]; if(!(h>0)) continue; const gx=(Q.ci*16+(i&15)+.5)*SU.cs+FREE.X, gz=(Q.cj*16+(i>>4)+.5)*SU.cs+FREE.Z, w=h; v+=w; cx+=gx*w; cz+=gz*w; const d=Math.hypot(gx-o.x,gz-o.z); if(d>rmax) rmax=d; if(d>1) quad[(gx>o.x?1:0)+(gz>o.z?2:0)]++; }
          cx/=(v-vv); cz/=(v-vv); const R=fuReel(o); return [+(v*.04).toFixed(3), +Math.hypot(cx-S.x,cz-S.z).toFixed(2), +Math.hypot(cx-o.x,cz-o.z).toFixed(2), +rmax.toFixed(2), quad.filter(n=>n>0).length, +hi.toFixed(2), +Math.hypot(cx-R.x,cz-R.z).toFixed(2), [...new Set(SU.list.flatMap(Q=>[...Q.t].filter(Boolean)))], FU.pts.length]; })()"""%(k,p,q,x,k,k)))
    print(W)
    ok(W[0][7]==[3] and W[0][1]<.45 and abs(W[0][0]-.18)<.04, '🫗 el goteo echa lodo justo abajo de su grifo (%s m³, a %s m del grifo)'%(W[0][0],W[0][1]))
    ok(W[1][7]==[1] and W[1][8]>0 and W[1][5]>2.5 and W[1][4]==4, '⛲ la fuente avienta su chorro hacia arriba (%s m) y cae alrededor de la máquina (por los 4 lados)'%W[1][5])
    ok(W[2][7]==[5] and W[2][3]>3.4 and W[2][4]==4, '💧 la regadera reparte la pintura en un círculo grande (hasta %s m, por los 4 lados)'%W[2][3])
    ok(W[3][7]==[4] and 2.6<W[3][6]<6.5, '🚿 la manguera enrollada echa miel por su lado, como a %s m'%W[3][6])
    ok(all(abs(w[0]-.6)<.06 for w in W[1:]), 'y cada una echa lo que dice «Mucho» %s'%[w[0] for w in W])
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); const o=freeAddStatic({k:'p',a:'fuentes',b:FU_DEF},FREE.X,FREE.Y,FREE.Z,0,true); const C=[{on:1,p:6,q:3,x:3,col:0},{on:1,p:2,q:0,x:3,col:0},{on:0,p:5,q:1,x:0,col:11},{on:1,p:5,q:2,x:3,col:9}]; fuSet(o,C);
        const D=fuCfg(o), same=JSON.stringify(D)===JSON.stringify(C); FU.pts.length=0; suRecount(); const v0=SU.vol; __S(30); suRecount(); const v=SU.vol-v0+FU.pts.reduce((a,P)=>a+(P.v||0),0);
        fuOpen(o); const ov=ui('freeBubOv'); const rows=[...ov.querySelectorAll('.bub-row b')].map(b=>b.textContent); const tabs=ov.querySelector('.bub-row').querySelectorAll('button').length;
        [...ov.querySelectorAll('.bub-row')][2].querySelectorAll('button')[0].click(); const after=fuCfg(o)[FU.tab].p; ov.hidden=true;
        freeSave(); const J=JSON.parse(localStorage.getItem('mundoPelucheLibre')), e=J.s.find(q=>q[1]==='fuentes'); FREE.loaded=null; freeLoad(); const o2=FREE.objs.find(q=>q.gad==='fuentes');
        return [same, +v.toFixed(3), rows, tabs, after, e[2]===o.sel.b, !!o2 && o2.sel.b===o.sel.b, o.sel.b>2**32]; })()""")
    ok(r[0] and abs(r[1]-(.8*.3+.012+.2)*1)<.06, 'se puede prender más de una a la vez, cada una con su sustancia y lo que sale (%s m³ en 1 s)'%r[1])
    ok(r[2][:3]==['Salida','Sustancia','Cuánto sale'] and r[3]==4 and r[4]==1, 'la ventanita de ⚙️ Configurar tiene una pestaña por salida y cambia la sustancia %s'%r[2])
    ok(r[5] and r[6] and r[7], 'toda la configuración se guarda con el mundo')
    # 4. la manguera: se estira 20 m, sigue echando donde la sueltas, se recoge
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(-20,-20); const o=freeAddStatic({k:'p',a:'fuentes',b:0},FREE.X-10,FREE.Y,FREE.Z,0,true); fuSet(o,[0,1,2,3].map(i=>({on:i===3?1:0,p:4,q:2,x:2,col:0})));
        player.pos.set(o.x+2,FREE.Y+.05,o.z); __S(2); const na=(fuNearActions()||[]).filter(Boolean).map(a=>a.label); fuGrab(o); const mano=fuHoldActions().filter(Boolean).map(a=>a.label);
        for(let i=0;i<70;i++){ player.pos.x+=.5; __S(1); } const A=fuReel(o), d=Math.hypot(player.pos.x-A.x,player.pos.z-A.z); const rope=!!(o.fuR && o.fuR.mesh.parent);
        let L=0; { const P=o.fuR.P; for(let i=0;i<40;i++) L+=Math.hypot(P[i*3+3]-P[i*3],P[i*3+4]-P[i*3+1],P[i*3+5]-P[i*3+2]); }
        player.facing=0; fuDrop(); const hx=o.hose.x, hz=o.hose.z; suClear(); FU.pts.length=0; __AT(-20,-20); __S(45); suRecount(); let n=0, far=0; for(const Q of SU.list) for(let i=0;i<256;i++) if(Q.t[i]===4){ const gx=(Q.ci*16+(i&15)+.5)*SU.cs+FREE.X, gz=(Q.cj*16+(i>>4)+.5)*SU.cs+FREE.Z; if(Math.hypot(gx-hx,gz-hz)<10) n++; else far++; }
        const tip=(()=>{ player.pos.set(hx,FREE.Y+.05,hz+.5); __S(2); return (fuNearActions()||[]).filter(Boolean).map(a=>a.label); })();
        fuGrab(o); const t2=FREE.hose===o; freeSelect({k:'b',a:0,b:1}); __S(2); const auto=!FREE.hose && !!o.hose && !o.hose.held; freeSelect(null);
        player.pos.set(o.x+2,FREE.Y+.05,o.z); __S(2); const nb=(fuNearActions()||[]).filter(Boolean).map(a=>a.label); fuRoll(o); __S(2);
        return [na, mano, +d.toFixed(2), rope, +L.toFixed(1), n, far, tip, t2, auto, nb, !o.hose && !o.fuR]; })()""")
    ok(r[0]==['⚙️ Configurar máquina','🚿 Agarrar manguera'] and r[1][:2]==['⏸️ Cerrar manguera','Soltar'], 'junto a la máquina: «Configurar» y «Agarrar manguera»; con ella en la mano: «Cerrar manguera» y «Soltar» %s'%r[:2])
    ok(19<r[2]<=19.5 and r[3] and 19<r[4]<21.5, 'la manguera se estira hasta 20 m y ya no da más (llegaste a %s m; mide %s m)'%(r[2],r[4]))
    ok(r[5]>15 and r[6]==0, 'al soltarla prendida sigue echando donde quedó (%s cuadritos de miel ahí)'%r[5])
    ok(r[7]==['🚿 Agarrar manguera'] and r[8], 'la puedes volver a agarrar de la punta')
    ok(r[9], 'si escoges otra cosa para poner, la manguera se suelta sola')
    ok(r[10]==['⚙️ Configurar máquina','🧺 Recoger manguera'] and r[11], 'y «Recoger manguera» la enrolla otra vez %s'%r[10])
    # 5. la escoba también suelta lo que traes en la mano (eso se había descompuesto)
    r=await ev("""(()=>{ __CLR(); suClear(); __AT(0,0); const d=freeAddDyn('balon',player.pos.x,FREE.Y,player.pos.z+1); __S(3); freeGrab(d); const a=FREE.hold===d; freePaintSet(true); freeWipeMine(); return [a, FREE.hold, !!FREE.paint, FREE.sel]; })()""")
    ok(r[0] and r[1] is None and not r[2] and r[3] is None, 'la escoba suelta lo que traes, deja de pintar y de escoger %s'%r)
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close(); await b.close()
asyncio.run(m())
