# v234 en una sala de «Construir con amigos»: la 🚰 máquina de sustancias se ve y se configura igual para todos; el invitado
# puede agarrar la manguera (la sustancia sale por donde apunta), soltarla prendida (sigue echando ahí) y recogerla; la máquina de
# burbujas se puede volver a configurar desde un invitado; la cubeta del invitado le sigue llegando al dueño.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
BUS=open('/home/claude/mundo-peluche/herramientas/pruebas/test_v215_amigos.py').read().split('BUS = """',1)[1].split('"""',1)[0]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); ctx=await b.new_context(viewport={"width":560,"height":320})
    await ctx.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'min', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await ctx.route("https://**/*", route)
    async def open_game(name):
      pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); await pg.add_init_script(BUS)
      await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
      await pg.evaluate("""n=>__T.ev(`profile.name=${JSON.stringify(n)}; window.requestAnimationFrame=()=>0; window.__PB=0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateRemotes(.05,t); } scene.updateMatrixWorld(); FNET.bT=0; sendPresence(true); __PB=Math.max(__PB,mp.presBytes||0); };
        window.__UP=d=>new THREE.Vector3(0,1,0).applyQuaternion(d.root.quaternion).y; window.__AIM=()=>{ camera.position.set(player.pos.x,player.pos.y+1.6,player.pos.z-2); camera.lookAt(player.pos.x,player.pos.y+1.7,player.pos.z+5); camera.updateMatrixWorld(); }; 1`)""", name)
      return pg, errs
    A,ea=await open_game('Ana'); B,eb=await open_game('Beto')
    await B.evaluate("__T.ev('MY_PID=`beto0001`; 1')")
    ev=lambda P,s: asyncio.wait_for(P.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    async def sync(n=10):
      for i in range(n):
        await ev(A,"__S(2); 1"); await A.wait_for_timeout(40); await ev(B,"__S(2); 1"); await B.wait_for_timeout(40)
    await ev(A,"fnCreate(false); 1"); await A.wait_for_timeout(1500)
    await ev(A,"""(()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); suClear(); const X=FREE.X, Z=FREE.Z;
      const o=freeAddStatic({k:'p',a:'fuentes',b:FU_DEF},X-8,FREE.Y,Z+6,0,true); fnLocalAdd(o); fuSet(o,[{on:0,p:3,q:1,x:0,col:0},{on:0,p:1,q:1,x:1,col:0},{on:0,p:5,q:1,x:1,col:7},{on:0,p:4,q:2,x:1,col:5}]);
      const m=freeAddStatic({k:'p',a:'burbujas',b:0},X+8,FREE.Y,Z+6,0,true); fnLocalAdd(m); player.pos.set(X,FREE.Y+.05,Z-6); return 1; })()""")
    await sync(4)
    code=await ev(A,"FNET.code"); await ev(B,"(async()=>{ ui('freeBtn').click(); await new Promise(r=>setTimeout(r,600)); return 1; })()")
    await ev(B,"fnJoin(%s); 1"%json.dumps(code)); await B.wait_for_timeout(1500); await ev(B,"player.pos.set(FREE.X,FREE.Y+.05,FREE.Z-4); 1")
    for i in range(40):
      await sync(1)
      if await ev(B,"fnSynced() && FREE.objs.some(o=>o.gad==='fuentes')"): break
    M="FREE.objs.find(o=>o.gad==='fuentes')"
    ba=await ev(A,M+".sel.b"); bb=await ev(B,"(()=>{ const o=%s; return o?o.sel.b:null; })()"%M)
    ok(ba==bb and ba>2**32, 'Beto ve la máquina de sustancias de Ana con la misma configuración (%s / %s)'%(ba,bb))
    # Beto la configura: el goteo con pintura roja, la fuente con slime
    await ev(B,"(()=>{ const o=%s; const C=fuCfg(o); C[0]={on:1,p:4,q:2,x:0,col:0}; C[1]={on:1,p:2,q:2,x:1,col:0}; fuSet(o,C); return 1; })()"%M)
    await sync(12)
    ca=await ev(A,"JSON.stringify(fuCfg(%s))"%M); cb=await ev(B,"JSON.stringify(fuCfg(%s))"%M)
    ok(ca==cb and json.loads(ca)[0]['on']==1 and json.loads(ca)[1]['p']==2, 'Beto la configura y a Ana le cambia igual')
    await sync(10)
    KS="[...new Set(SU.list.flatMap(C=>[...C.t,...C.t2].filter(Boolean)))].sort()"; ka=await ev(A,KS); kb=await ev(B,KS)
    ok(2 in ka and 4 in ka and 2 in kb and 4 in kb, 'la máquina echa lo que escogió Beto y los dos lo ven %s %s'%(ka,kb))
    pa=await ev(B,"FU.pts.length"); ok(pa>0, 'Beto también ve las gotitas que salen (%s)'%pa)
    # Beto agarra la manguera y se la lleva
    await ev(A,"(()=>{ const o=%s; const C=fuCfg(o); C[0].on=0; C[1].on=0; fuSet(o,C); suClear(); FU.pts.length=0; return 1; })()"%M); await sync(8)
    await ev(B,"(()=>{ const o=%s; player.pos.set(o.x+2,FREE.Y+.05,o.z); __S(1); fuGrab(o); const C=fuCfg(o); C[3].on=1; fuSet(o,C); return 1; })()"%M)
    for i in range(16):
      await ev(B,"(()=>{ player.pos.x+=.6; player.facing=Math.PI/2; return 1; })()"); await sync(1)
    await sync(6)
    r=await ev(A,"""(()=>{ const o=%s; const S=fuSrc(o,3,fuCfg(o)[3]); let rb=null; for(const r of mp.remotes.values()) if(r.fg) rb=r; return [o.hose&&o.hose.held, !!rb, rb?+Math.hypot(S.x-rb.pos.x,S.z-rb.pos.z).toFixed(2):null, !!(o.fuR && o.fuR.mesh.parent)]; })()"""%M)
    ok(r[0]=='beto0001' and r[1] and r[2] is not None and r[2]<1.2 and r[3], 'Ana ve que Beto trae la manguera (la cuerda llega hasta su mano) %s'%r)
    xb=await ev(B,"[player.pos.x-FREE.X, player.pos.z-FREE.Z]")
    await sync(10)
    r=await ev(A,"""(()=>{ const o=%s; suRecount(); let n=0, near=0; for(const C of SU.list) for(let i=0;i<256;i++) if(C.t[i]===4){ n++; const gx=(C.ci*16+(i&15)+.5)*SU.cs, gz=(C.cj*16+(i>>4)+.5)*SU.cs; if(Math.hypot(gx-%f,gz-%f)<9) near++; } return [n, near]; })()"""%(M,xb[0],xb[1]))
    ok(r[0]>5 and r[1]>=r[0]*.8, 'y la miel sale por donde Beto apunta (%s de %s cuadritos cerca de Beto)'%(r[1],r[0]))
    # Beto la suelta prendida lejos: sigue echando ahí
    await ev(B,"fuDrop(); 1"); await sync(6)
    await ev(A,"suClear(); 1"); await sync(16)
    r=await ev(A,"(()=>{ const o=%s; return o.hose?[+(o.hose.x-FREE.X).toFixed(1),+(o.hose.z-FREE.Z).toFixed(1),o.hose.held]:null; })()"%M)
    ok(r and abs(r[0]-xb[0])<2 and r[2] is None, 'Beto la suelta y a Ana le queda tirada ahí %s'%r)
    v=await ev(A,"(suRecount(), SU.vol)"); vb=await ev(B,"(suRecount(), SU.vol)")
    ok(v>.2 and vb>.1, 'y sigue echando miel donde quedó (Ana %.2f m³, Beto %.2f m³)'%(v,vb))
    # Beto la recoge
    await ev(B,"(()=>{ const o=%s; fuRoll(o); return 1; })()"%M); await sync(8)
    r=await ev(A,"(()=>{ const o=%s; return [o.hose, !!o.fuR]; })()"%M); rb_=await ev(B,"(()=>{ const o=%s; return [o.hose, !!o.fuR]; })()"%M)
    ok(r==[None,False] and rb_==[None,False], 'Beto la recoge y se enrolla para los dos')
    # la máquina de burbujas de Ana se puede configurar desde Beto otra vez (eso se había descompuesto en la v232)
    await ev(B,"(()=>{ const o=FREE.objs.find(q=>q.gad==='burbujas'); freeBubOpen(o); const ov=ui('freeBubOv'); [...ov.querySelectorAll('.bub-row')][0].querySelectorAll('button')[2].click(); ov.hidden=true; return o.sel.b; })()")
    await sync(10)
    bb=await ev(A,"FREE.objs.find(q=>q.gad==='burbujas').sel.b")
    ok((bb&3)==2, 'Beto cambia el tamaño de las burbujas de la máquina de Ana y sí le cambia (%s)'%bb)
    # y la cubeta de Beto le sigue llegando a Ana
    await ev(A,"(()=>{ const o=%s; const C=fuCfg(o); C[3].on=0; fuSet(o,C); suClear(); FU.pts.length=0; return 1; })()"%M); await sync(6); await ev(A,"suClear(); FU.pts.length=0; 1"); await sync(4)
    await ev(B,"(()=>{ suNetPour(FREE.X+4,FREE.Z+10,1,0,.2,.5); return 1; })()"); await sync(10)
    v=await ev(A,"(suRecount(), SU.vol)"); ok(abs(v-.2)<.03, 'lo que Beto echa con la cubeta le llega a Ana (%.3f m³)'%v)
    pb_=await ev(A,"__PB"); pbb=await ev(B,"__PB"); ok(pb_<=3700 and pbb<=3700, 'lo más que mandó cada uno pesa %s y %s bytes'%(pb_,pbb))
    ok(not ea and not eb,'sin errores %s %s'%(ea[:3],eb[:3])); await b.close()
asyncio.run(m())
