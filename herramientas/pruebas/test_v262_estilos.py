# v262: estilos visuales (Opciones → «Estilo visual»): Peluche, Pixel art (con tamaño de cuadritos y 6 filtros), Caricatura y Neón.
# Revisa: las opciones (y que el tamaño y el filtro solo salen con pixel art), que se guarden, que cada estilo dibuje sin errores
# y se vea distinto (pixel = cuadritos, neón = oscuro), que los letreros queden marcados para dibujarse aparte (se puedan leer),
# que el neón vuelva a dejar el agua como estaba, y que al regresar a Peluche todo quede como antes.
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

    # 1. las opciones: 4 estilos; el tamaño y el filtro solo con pixel art; se guardan
    r=await ev("""(()=>{ openOptions(); const B=[...ui('optVStyle').querySelectorAll('button')], out=[B.map(b=>b.dataset.v), settings.vstyle, ui('optPxRow1').hidden, ui('optPxRow2').hidden];
      B[1].click(); out.push(settings.vstyle, ui('optPxRow1').hidden, ui('optPxRow2').hidden, settings.pxSize, settings.pxFilter);
      ui('optPxSize').querySelector('[data-v="0"]').click(); ui('optPxFilter').querySelector('[data-v="3"]').click();
      const sv=JSON.parse(localStorage.getItem('mundoPelucheOpciones')||'{}'); out.push(sv.vstyle, sv.pxSize, sv.pxFilter, ui('optPxFilter').querySelectorAll('button').length);
      B[3].click(); out.push(settings.vstyle, ui('optPxRow1').hidden, B[3].getAttribute('aria-pressed'));
      ui('resetOptions').click(); out.push(settings.vstyle); return out; })()""")
    ok(r[0]==['peluche','pixel','cari','neon'] and r[1]=='peluche' and r[2] and r[3], '1a «Estilo visual» tiene Peluche, Pixel art, Caricatura y Neón; empieza en Peluche y sin las opciones de pixel %s'%r[:4])
    ok(r[4]=='pixel' and not r[5] and not r[6] and r[7]=='2' and r[8]=='0', '1b al escoger Pixel art salen «Tamaño de los cuadritos» (Grandes) y «Filtro del pixel art» (Natural) %s'%r[4:9])
    ok(r[9]=='pixel' and r[10]=='0' and r[11]=='3' and r[12]==6, '1c se guarda el estilo, el tamaño (Chicos) y el filtro (Retro); hay 6 filtros %s'%r[9:13])
    ok(r[13]=='neon' and r[14] and r[15]=='true' and r[16]=='peluche', '1d con Neón se esconden las de pixel; «Restablecer» regresa a Peluche %s'%r[13:])
    r=await ev("""(async()=>{ I18N.set('en'); openOptions(); await new Promise(f=>setTimeout(f,400)); const t=[...ui('optVStyle').querySelectorAll('button')].map(b=>b.textContent.trim()); const f=[...ui('optPxFilter').querySelectorAll('button')].map(b=>b.textContent.trim()); I18N.set('es'); optionsEl.hidden=true; return [t,f]; })()""")
    ok(r[0]==['Plush','Pixel art','Cartoon','Neon'] and 'Pastel sunset' in r[1] and 'Blue night' in r[1], '1e en inglés: %s / %s'%(r[0],r[1]))

    await ev("startGame()"); await pg.wait_for_timeout(1500)
    await ev("""window.requestAnimationFrame=()=>0; window.__run=(sec)=>{ let t=clock.elapsedTime; for(let i=0;i<Math.round(sec/.05);i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateSky(.05); } };
      window.__tp=(id)=>{ const T=TELEPORTS.find(t=>t.id===id); player.pos.set(T.x,terrainH(T.x,T.z)+.1,T.z); player.vel.set(0,0,0); __run(1.2); return 1; };
      // dibuja un cuadro como el juego y lee una cuadrícula de puntitos (y una fila seguida para ver los cuadritos)
      window.__shot=(st,sz,fl)=>{ settings.vstyle=st; settings.pxSize=sz||'2'; settings.pxFilter=fl||'0'; const gl=renderer.getContext();
        for(let k=0;k<2;k++){ const S=SP.on&&state!=='menu'?spaceScene:scene; if(vsOn()) vsRender(S,camera); else renderer.render(S,camera); }
        const W=gl.drawingBufferWidth, H=gl.drawingBufferHeight, px=new Uint8Array(4), pts=[]; let lum=0, n=0;
        for(let j=1;j<10;j++) for(let i=1;i<16;i++){ gl.readPixels(Math.floor(W*i/16),Math.floor(H*j/10),1,1,gl.RGBA,gl.UNSIGNED_BYTE,px); const l=(px[0]*.2126+px[1]*.7152+px[2]*.0722)/255; pts.push(l); lum+=l; n++; }
        const row=new Uint8Array(4*240); gl.readPixels(Math.floor(W*.3),Math.floor(H*.45),240,1,gl.RGBA,gl.UNSIGNED_BYTE,row); let same=0; for(let i=1;i<240;i++){ const a=4*i, b=a-4; if(row[a]===row[b]&&row[a+1]===row[b+1]&&row[a+2]===row[b+2]) same++; }
        const mean=lum/n, vr=pts.reduce((s,v)=>s+(v-mean)**2,0)/n; return {err:gl.getError(), mean:+mean.toFixed(3), sd:+Math.sqrt(vr).toFixed(3), same:+(same/239).toFixed(2)}; }; 1""")

    # 2. cada estilo dibuja sin errores y se ve como debe
    await ev("__tp('ar_plat'); 1")
    R=json.loads(await ev("JSON.stringify({pel:__shot('peluche'), px:__shot('pixel','2','0'), cari:__shot('cari'), neon:__shot('neon')})"))
    print('   ', R)
    ok(all(v['err']==0 and v['sd']>0.03 for v in R.values()), '2a los 4 estilos dibujan sin errores y no salen en blanco (hay de todo en la pantalla)')
    ok(R['px']['same']>=max(0.5,R['pel']['same']+0.2), '2b pixel art se ve en cuadritos (puntos iguales seguidos: %s contra %s en peluche)'%(R['px']['same'],R['pel']['same']))
    ok(R['neon']['mean']<R['pel']['mean']*0.6, '2c neón es oscuro (%s contra %s)'%(R['neon']['mean'],R['pel']['mean']))
    ok(abs(R['cari']['mean']-R['pel']['mean'])<0.25, '2d caricatura conserva la luz del día (%s contra %s)'%(R['cari']['mean'],R['pel']['mean']))
    r=json.loads(await ev("JSON.stringify((()=>{ const o=[]; for(const sz of ['0','1','2']) for(const fl of ['0','1','2','3','4','5']){ const s=__shot('pixel',sz,fl); o.push([sz+fl,s.err,s.sd]); } return o; })())"))
    bad=[x for x in r if x[1]!=0 or x[2]<0.02]
    ok(not bad and not cerr, '2e los 3 tamaños × 6 filtros del pixel art dibujan bien (18 combinaciones) %s %s'%(bad,cerr[:2]))

    # 3. letreros: lo que tiene letras queda marcado (también si se copia a otro dibujo) y entra en la pasada de letras
    r=await ev("""(()=>{ const a=document.createElement('canvas'), q=a.getContext('2d'); window.__vsTxtNew=0; q.fillRect(0,0,4,4); const o=[!!a.__txt, window.__vsTxtNew];
      q.fillText('Hola',1,10); o.push(a.__txt, window.__vsTxtNew); const b=document.createElement('canvas'); b.getContext('2d').drawImage(a,0,0); o.push(b.__txt);
      const c=document.createElement('canvas'); c.getContext('2d').strokeText('x',1,1); o.push(c.__txt);
      VSX.scanT=-1e9; settings.vstyle='pixel'; vsScan(scene); const near=VSX.txt.filter(m=>m.getWorldPosition(new THREE.Vector3()).distanceTo(player.pos)<40);
      o.push(VSX.txt.length, near.length, near.every(m=>m.layers.test(new THREE.Layers().set(2)) || (m.layers.mask&4)), vsTxtNear(camera)); return o; })()""")
    ok(r[0]==False and r[1]==0 and r[2]==1 and r[3]==1 and r[4]==1 and r[5]==1, '3a un dibujo con letras queda marcado (y avisa para buscarlo pronto); copiarlo a otro también lo marca; sin letras no %s'%r[:6])
    ok(r[6]>20 and r[7]>=2 and r[8] and r[9], '3b los letreros del minijuego entran en la pasada de letras (se ven nítidos) %s'%r[6:])
    # los carteles de instrucciones se pintan al acercarte: el siguiente vistazo (al segundo) ya los encuentra
    r=await ev("""(()=>{ const tex=[]; scene.traverse(o=>{ const m=o.material; if(o.isMesh && m && !Array.isArray(m) && m.map && m.map.__paint && !m.map.__done) tex.push(o); }); if(!tex.length) return ['ninguno'];
      const o=tex[0], before=VSX.txt.includes(o); o.material.map.__paint(); VSX.scanT=performance.now()-1100; vsScan(scene); return [before, !!o.material.map.image.__txt, VSX.txt.includes(o)]; })()""")
    ok(r==[False,True,True], '3c un cartel de instrucciones recién pintado entra a la pasada de letras al segundo %s'%r)

    # 4. neón: el agua cuenta como piso en su pasada y luego queda como estaba
    await ev("__tp('muelle'); 1")
    r=await ev("""(()=>{ const before=waterMats.map(m=>m.depthWrite); const s=__shot('neon'); const after=waterMats.map(m=>m.depthWrite); return [s.err, JSON.stringify(before)===JSON.stringify(after), waterMats.some(m=>m.__vsDw), before.filter(x=>!x).length]; })()""")
    ok(r[0]==0 and r[1] and not r[2] and r[3]>=1, '4 neón dibuja el agua (con su cuadrícula) y la deja como estaba %s'%r)

    # 5. de regreso a Peluche: nada se queda prendido (cámara, brillitos del agua, puntitos de sombra)
    r=await ev("""(()=>{ const p0=camera.position.clone(); __shot('pixel','2','1'); const o=[camera.position.distanceTo(p0)<1e-6, !camera.view || !camera.view.enabled, waterMats.every(m=>!m.uniforms.uPxSpark || m.uniforms.uPxSpark.value===0), !PX.probe || PX.probe.sh.coefficients[8].x===0];
      const s=__shot('peluche'); o.push(vsOn(), s.err, renderer.getRenderTarget()===null); return o; })()""")
    ok(r==[True,True,True,True,False,0,True], '5 al volver a Peluche la cámara, el agua y las sombras quedan como siempre %s'%r)

    # 6. en el espacio y en el menú también funciona
    r=await ev("""(()=>{ enterSpace('walk',{P:MOON, d:new THREE.Vector3(0,1,0)}); __run(2); const a=__shot('neon'), b=__shot('pixel','1','2'), c=__shot('cari'); exitSpace(true); __run(1); return [SP.on, a.err, b.err, c.err, a.sd>0.02, b.sd>0.02, c.sd>0.02]; })()""")
    ok(r==[False,0,0,0,True,True,True], '6 en la Luna los estilos también dibujan bien %s'%r)
    ok(not errs and not cerr, 'sin errores (%s %s)'%(errs[:3],cerr[:3]))
    await b.close()
asyncio.run(m())
