# v223: el medidor guarda el peor cuadro de los últimos 30 s (y hace cuánto fue); los coches de lejos se dibujan con una copia
# de una sola pieza por color (la pista: ~205 → ~85 dibujos) y sus luces apagadas no se dibujan; menos basura al caminar
# (pista, olas, juntar piezas, materiales, choques, zonas). Todo debe seguir funcionando igual.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
ROGER={"quality":"min","qDef":1,"ultra":True,"shadows":False,"weather":False,"fpsCap":"30","autoRes":False,"draw":30,"hints":False,"fps":True}
NORMAL={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateSky(.05); } };
  window.__D=()=>{ renderer.info.reset(); renderer.render(scene,camera); return renderer.info.render.calls; };
  window.__W=(k)=>new Promise(async res=>{ for(let i=0;i<k;i++){ __S(6); renderer.render(scene,camera); await new Promise(r=>setTimeout(r,300)); } res(1); }); 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    async def open_page(opts):
      ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True, device_scale_factor=2); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
      await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(opts))
      async def route(r):
        if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
        elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
        else: await r.abort()
      await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
      ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300); await ev(STEP)
      return ctx, pg, errs, ev
    ctx,pg,errs,ev=await open_page(ROGER)
    # 1. medidor: el peor de los últimos 30 s, con «hace X s»; se olvida a los 30 s y al viajar
    r=await ev("""(async()=>{ startGame(); { const x=PG.x+6, z=PG.z+10; player.pos.set(x,groundAt(x,z,99)+.05,z); } const W=ms=>new Promise(r=>setTimeout(r,ms)); const fl=()=>{ capLast=-1e9; fpsTime=.6; frame(); return ui('fps').textContent; };
      for(let i=0;i<5;i++) fl(); frame.wst=95; frame.wsl='lógica'; const a=fl(); for(const e of frame.wb) e[2]-=1300; frame.wst=0; const b=fl();
      for(const e of frame.wb) e[2]-=31000; frame.wst=0; const c=fl();
      frame.wst=88; frame.wsl='dibujo'; fl(); player.pos.x+=100; frame.wst=0; const d=fl(); player.pos.x-=100; fl();
      const box=ui('fps').getBoundingClientRect(), coin=ui('coinChip').getBoundingClientRect(); frame.wst=1234; frame.wsl='dibujo'; fl(); for(const e of frame.wb) e[2]-=12300; frame.wst=0; const e=fl(); const box2=ui('fps').getBoundingClientRect(), coin2=ui('coinChip').getBoundingClientRect(); let maxR=0; for(const el of ui('hud').querySelectorAll('.chip,.hint')){ const q=el.getBoundingClientRect(); if(q.width && q.top<80) maxR=Math.max(maxR,q.right); }
      return [a,b,c,d,e, Math.round(box2.right), Math.round(coin2.left), Math.round(box2.height), Math.round(maxR), innerWidth]; })()""")
    ok('peor 95 ms (lógica)' in r[0] and 'peor 95 ms (lógica) hace 1 s' in r[1] and 'peor 95' not in r[2] and 'peor 88' not in r[3], 'medidor: guarda el peor de 30 s y dice hace cuánto; a los 30 s y al viajar se olvida %s'%r[:4])
    ok(r[5]<=r[6] and r[7]<48 and r[8]<=r[9] and 'hace 12 s' in r[4], 'medidor: el texto largo («%s») cabe en dos renglones sin encimarse (termina en %s, monedas en %s, alto %s; la fila de arriba llega a %s de %s)'%(r[4].replace(chr(10),' / '),r[5],r[6],r[7],r[8],r[9]))
    # 2. coches: copia de lejos, detallado de cerca o con puertas abiertas, se ve igual
    r=await ev("""(async()=>{ const out=[]; for(const c of cars){ const P=c.L.far; let nd=0; c.root.traverse(o=>{ if(o.isMesh && !o.material.visible===false) nd++; }); out.push([!!P, P?P.children.length:0]); }
      const c=cars[0], cp=camera.position, far=()=>{ c.L.farOn=c.L.far.visible; carFarTick(c); return [c.L.far.visible, c.root.children.filter(o=>o!==c.L.far && o.isMesh && o.visible && o.material!==c.L.beam).length]; };
      const p0=c.root.position.clone(); c.root.position.set(cp.x+40,cp.y,cp.z); const A=far(); c.root.position.set(cp.x+5,cp.y,cp.z); const B=far(); c.root.position.set(cp.x+40,cp.y,cp.z); c.doorMask=1; const C=far(); c.doorMask=0; c.root.position.copy(p0); c.L.farOn=c.L.far.visible; carFarTick(c);
      return [out, A, B, C]; })()""")
    ok(all(x[0] and 3<=x[1]<=12 for x in r[0]) and r[1][0] and r[1][1]==0 and not r[2][0] and r[2][1]>0 and not r[3][0], 'coches: cada uno tiene su copia de lejos (%s piezas); lejos se usa, cerca o con la puerta abierta el detallado %s'%([x[1] for x in r[0]], r[1:]))
    r=await ev("""(async()=>{ const c=cars[0]; const x=c.x+Math.sin(c.h+1.2)*14, z=c.z+Math.cos(c.h+1.2)*14; player.pos.set(x,groundAt(x,z,99)+.05,z); __S(10);
      camera.position.set(c.x+Math.sin(c.h+1.2)*13, c.y+3, c.z+Math.cos(c.h+1.2)*13); camera.lookAt(c.x,c.y+1,c.z); camera.updateMatrixWorld();
      const px=async()=>{ renderer.render(scene,camera); const im=new Image(); im.src=renderer.domElement.toDataURL('image/png'); await im.decode(); const cv=document.createElement('canvas'); cv.width=im.width; cv.height=im.height; const g=cv.getContext('2d'); g.drawImage(im,0,0); return g.getImageData(0,0,cv.width,cv.height).data; };
      const P=c.L.far, set=f=>{ P.visible=f; for(const o of c.root.children){ if(o===P||o.isSprite||(o.isMesh&&o.material===c.L.beam)) continue; o.visible=!f; } };
      set(true); const A=await px(); set(false); const B=await px(); c.L.farOn=false; carFarTick(c); let diff=0, car=0; for(let i=0;i<A.length;i+=4){ if(Math.abs(A[i]-B[i])+Math.abs(A[i+1]-B[i+1])+Math.abs(A[i+2]-B[i+2])>40) diff++; } return [diff, A.length/4]; })()""")
    ok(r[0]<r[1]*.002, 'coches: la copia de lejos se ve igual que el detallado (%s de %s puntos distintos)'%tuple(r))
    r=await ev("""(()=>{ const c=cars[1]; c.lights=false; c.L.state=''; updateCarLights(c); const off=c.L.sprites.every(s=>!s.visible); c.lights=true; c.L.state=''; updateCarLights(c); const head=c.L.sprites.filter(s=>s.visible).length; c.lights=false; c.L.state=''; updateCarLights(c); return [off, head, c.L.sprites.length]; })()""")
    ok(r[0] and r[1]>0, 'coches: las luces apagadas no se dibujan; al prenderlas sí (%s de %s) %s'%(r[1],r[2],r))
    r=await ev("(async()=>{ const T=TELEPORTS.find(q=>q.id==='pista'); player.pos.set(T.x,groundAt(T.x,T.z,60)+.05,T.z); yaw=0; player.facing=Math.PI; await __W(8); return __D(); })()")
    ok(r<140, 'en la pista (la foto de Roger con el coche): %s dibujos (antes ~205 en mi compu, 196 en su Huawei)'%r)
    # 3. pista: la respuesta rápida coincide con revisar toda la pista
    r=await ev("""(()=>{ const P=TRACK.pts, n=P.length; const ref=(x,z)=>{ let b=-1,bd=1e18; for(let i=0;i<n;i++){ const d=(x-P[i][0])**2+(z-P[i][1])**2; if(d<bd){ bd=d; b=i; } } return Math.sqrt(bd); };
      let bad=0, near=0, k=0; for(let i=0;i<3000;i++){ const q=P[i%n], x=q[0]+(Math.sin(i*12.9898)*.5)*(i%3?80:400), z=q[1]+(Math.cos(i*78.233)*.5)*(i%3?80:400); const a=ref(x,z), t=trackNearest(x,z), b=t.d;
        for(const th of [TRACK_W/2+1.3, TRACK_W/2+9, TRACK_W*1.5]) if((a<th)!==(b<th)) bad++; if(a<24){ near++; if(Math.abs(a-b)>.01) bad++; } k++; } return [k, near, bad]; })()""")
    ok(r[2]==0 and r[1]>200, 'pista: de %s puntos (%s cerca), en todos da lo mismo que revisar toda la pista %s'%(r[0],r[1],r))
    # 4. materiales: la revisión rápida da lo mismo que la completa, y nota cuando uno cambia
    r=await ev("""(()=>{ BMAT.tick++; const L=[...BMAT.info.keys()]; let same=0, diff=0; const quick=L.map(m=>matInfo(m).chk); BMAT.tick++;
      for(let i=0;i<L.length;i++){ const m=L[i], I=BMAT.info.get(m); BMAT.info.delete(m); const f=matInfo(m).chk; BMAT.info.set(m,I); if(f===quick[i]) same++; else diff++; }
      const m=L.find(x=>x && x.color && BMAT.info.get(x) && (BMAT.info.get(x).key||'')[0]==='C'); if(!m) return [L.length, same, diff, 'sin material C', [...new Set(L.map(x=>(BMAT.info.get(x).key||'?')[0]))]]; BMAT.tick++; const k0=matInfo(m).chk; const c0=m.color.getHex(); m.color.setHex(c0^0x010203); BMAT.tick++; const k1=matInfo(m).chk, vol=matInfo(m).vol; m.color.setHex(c0);
      return [L.length, same, diff, k0!==k1, vol]; })()""")
    ok(r[2]==0 and r[3] and r[4], 'materiales: %s revisados, %s iguales a la revisión completa, %s distintos; un cambio de color se nota %s'%(r[0],r[1],r[2],r))
    # 5. olas: la lista que se arregla en su lugar es igual a hacerla de nuevo
    r=await ev("""(async()=>{ for(let i=0;i<80;i++){ swellTick(); await new Promise(r=>setTimeout(r,15)); } const S=SWELL, T=Date.now()/1000; const F=[]; S.map.forEach(L=>{ for(const w of L) if(T-w.t0<w.life) F.push(w); }); F.sort((a,b)=>a.t0-b.t0||a.id-b.id);
      const A=S.all.filter(w=>T-w.t0<w.life); const same=A.length===F.length && A.every((w,i)=>w===F[i]); const dup=new Set(S.all).size!==S.all.length;
      const G=S.near.slice().sort((a,b)=>a.dc-b.dc).slice(0,SWN); const g=G.length===S.gpu.length && G.every((w,i)=>w===S.gpu[i] || w.dc===S.gpu[i].dc);
      return [F.length, same, dup, g, S.gpu.length]; })()""")
    ok(r[0]>50 and r[1] and not r[2] and r[3], 'olas: %s en el mar, la lista es la misma que hacerla de nuevo, sin repetidas, y las %s más cercanas van a la tarjeta de video %s'%(r[0],r[4],r))
    # 6. juntar piezas: las listas de cada vuelta se reusan y el resultado es el de siempre
    r=await ev("""(async()=>{ const a=BATCH.buf; for(let i=0;i<60 && !(BATCH.buf && BATCH.buf===a && !BATCH.col && !BATCH.cyc);i++){ __S(2); await new Promise(r=>setTimeout(r,60)); }
      const L=BATCH.buf.L; let nulls=true; for(let i=0;i<L.length;i++){ if(L[i]===null) break; } let n=0; scene.traverse(o=>{ if(o.isMesh) n++; }); return [!!BATCH.buf, BATCH.buf===a || a===undefined, BATCH.batches.size, BATCH.recs.size, n]; })()""")
    ok(r[0] and r[1] and r[2]>80 and r[3]>1000, 'juntar piezas: las listas se reusan; %s grupos, %s piezas vigiladas %s'%(r[2],r[3],r))
    # 7. caminar: no hay errores y todo sigue
    r=await ev("(async()=>{ for(let i=0;i<120;i++){ keys.KeyW=true; if(i%40===0) keys.KeyA=!keys.KeyA; frame(); await new Promise(r=>setTimeout(r,10)); } keys.KeyW=false; keys.KeyA=false; return [AREA.list.length, LEJOS.L.length, obstacles.length]; })()")
    ok(r[0]>50 and r[1]>100 and r[2]>500, 'caminando un rato: zonas %s, piezas lejanas %s, choques %s'%tuple(r))
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close()
    ctx,pg,errs,ev=await open_page(NORMAL)
    r=await ev("(async()=>{ startGame(); const T=TELEPORTS.find(q=>q.id==='pista'); player.pos.set(T.x,groundAt(T.x,T.z,60)+.05,T.z); await __W(6); return [__D(), cars.filter(c=>c.L.farOn).length, BATCH.batches.size]; })()")
    ok(r[0]<300 and r[1]>0 and r[2]>50, 'calidad Baja: en la pista %s dibujos (antes ~410, con sombras), %s coches con su copia de lejos %s'%(r[0],r[1],r))
    ok(not errs,'sin errores (calidad Baja) %s'%errs[:3]); await ctx.close()
    await b.close()
asyncio.run(m())
