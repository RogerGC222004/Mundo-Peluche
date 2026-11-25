# v262: estilos visuales (Opciones → «Estilo visual»): Peluche, Pixel art (con tamaño de cuadritos y 6 filtros), Caricatura y Neón.
# Revisa: las opciones (y que el tamaño y el filtro solo salen con pixel art), que se guarden, que cada estilo dibuje sin errores
# y se vea distinto (pixel = cuadritos, neón = oscuro), que los letreros queden marcados para dibujarse aparte (se puedan leer),
# que el neón vuelva a dejar el agua como estaba, y que al regresar a Peluche todo quede como antes.
# Ronda 2: en teléfonos que no pueden, Caricatura y Neón salen apagados con aviso; versión ligera en Baja y Mínima;
# Caricatura de noche ya no aclara la noche; los letreros en Neón son letreros de neón (cartel oscuro, letras que brillan).
# v263: Crayones (Crayón suave, Crayón fuerte, Dibujo de niño); las hondas se leen con precisión (sin rayas en los teléfonos);
# el pixel art acomoda la vista de cuadrito en cuadrito y deja la cámara como estaba.
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
    ok(r[0]==['peluche','pixel','cari','neon','crayon'] and r[1]=='peluche' and r[2] and r[3], '1a «Estilo visual» tiene Peluche, Pixel art, Caricatura, Neón y Crayones; empieza en Peluche y sin las opciones de pixel %s'%r[:4])
    ok(r[4]=='pixel' and not r[5] and not r[6] and r[7]=='2' and r[8]=='0', '1b al escoger Pixel art salen «Tamaño de los cuadritos» (Grandes) y «Filtro del pixel art» (Natural) %s'%r[4:9])
    ok(r[9]=='pixel' and r[10]=='0' and r[11]=='3' and r[12]==6, '1c se guarda el estilo, el tamaño (Chicos) y el filtro (Retro); hay 6 filtros %s'%r[9:13])
    ok(r[13]=='neon' and r[14] and r[15]=='true' and r[16]=='peluche', '1d con Neón se esconden las de pixel; «Restablecer» regresa a Peluche %s'%r[13:])
    r=await ev("""(async()=>{ I18N.set('en'); openOptions(); await new Promise(f=>setTimeout(f,400)); const t=[...ui('optVStyle').querySelectorAll('button')].map(b=>b.textContent.trim()); const f=[...ui('optPxFilter').querySelectorAll('button')].map(b=>b.textContent.trim()); I18N.set('es'); optionsEl.hidden=true; return [t,f]; })()""")
    ok(r[0]==['Plush','Pixel art','Cartoon','Neon','Crayons'] and 'Pastel sunset' in r[1] and 'Blue night' in r[1], '1e en inglés: %s / %s'%(r[0],r[1]))

    r=await ev("""(()=>{ settings.vstyle='neon'; VSX.can=false; openOptions(); const B=k=>ui('optVStyle').querySelector('[data-v="'+k+'"]'); const o=[B('cari').classList.contains('off') && B('crayon').classList.contains('off'), B('neon').getAttribute('aria-disabled'), B('pixel').classList.contains('off'), B('peluche').getAttribute('aria-pressed'), ui('optVNote').hidden];
      settings.vstyle='peluche'; syncOptionsUI(); B('neon').click(); o.push(settings.vstyle, ui('optVNote').hidden, ui('optVNote').textContent.trim()); B('pixel').click(); o.push(settings.vstyle);
      VSX.can=null; syncOptionsUI(); o.push(B('neon').classList.contains('off')); ui('resetOptions').click(); optionsEl.hidden=true; return o; })()""")
    ok(r[0] and r[1]=='true' and not r[2] and r[3]=='true' and r[4], '1f en un teléfono que no puede, Caricatura, Neón y Crayones salen apagados (y se ve Peluche escogido) %s'%r[:5])
    ok(r[5]=='peluche' and r[6]==False and r[7]=='Tu teléfono no puede mostrar este estilo' and r[8]=='pixel' and r[9]==False, '1g al tocarlos sale el aviso «%s» y no cambia; Pixel art sí se puede; en un teléfono normal no salen apagados %s'%(r[7],r[5:]))

    r=await ev("""(async()=>{ openOptions(); const o=[ui('optCrRow').hidden, settings.crTrazo]; ui('optVStyle').querySelector('[data-v="crayon"]').click(); o.push(settings.vstyle, ui('optCrRow').hidden, ui('optPxRow1').hidden, [...ui('optCrTrazo').querySelectorAll('button')].map(b=>b.textContent.trim()));
      ui('optCrTrazo').querySelector('[data-v="2"]').click(); const sv=JSON.parse(localStorage.getItem('mundoPelucheOpciones')||'{}'); o.push(sv.vstyle, sv.crTrazo);
      I18N.set('en'); await new Promise(f=>setTimeout(f,400)); o.push([...ui('optCrTrazo').querySelectorAll('button')].map(b=>b.textContent.trim()), ui('optCrRow').querySelector('label').textContent.trim(), ui('optVStyle').querySelector('[data-v="crayon"]').textContent.trim()); I18N.set('es');
      ui('resetOptions').click(); o.push(settings.vstyle, settings.crTrazo); optionsEl.hidden=true; return o; })()""")
    ok(r[0] and r[1]=='0' and r[2]=='crayon' and not r[3] and r[4] and r[5]==['Crayón suave','Crayón fuerte','Dibujo de niño'], '1h al escoger Crayones sale «Tipo de trazo» (Crayón suave, Crayón fuerte, Dibujo de niño); la de pixel no %s'%r[:6])
    ok(r[6]=='crayon' and r[7]=='2' and r[8]==['Soft crayon','Bold crayon',"Kid's drawing"] and r[9]=='Stroke type' and r[10]=='Crayons' and r[11]=='peluche' and r[12]=='0', '1i se guarda el trazo; en inglés %s / %s / %s; «Restablecer» regresa a Peluche %s'%(r[8],r[9],r[10],r[6:8]+r[11:]))

    await ev("startGame()"); await pg.wait_for_timeout(1500)
    await ev("""window.requestAnimationFrame=()=>0; window.__run=(sec)=>{ let t=clock.elapsedTime; for(let i=0;i<Math.round(sec/.05);i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateSky(.05); } };
      window.__hour=f=>{ const k=Math.floor(Date.now()/1000/DAY_LEN)*DAY_LEN; const T0=(k+f*DAY_LEN)*1000; Date.now=()=>T0; __run(.5); return 1; };
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

    r=await ev("(()=>{ const q0=settings.quality, o=[]; for(const q of ['min','low','mid','high']){ settings.quality=q; __shot('neon'); o.push(VSX.quad.material===VSX.mNl ? 'ligero':'completo'); } settings.quality=q0; return o; })()")
    ok(r==['ligero','ligero','completo','completo'], '2f en Mínima y Baja se usa la versión ligera de Caricatura y Neón; en Media y Alta la completa %s'%r)
    R2=json.loads(await ev("JSON.stringify((()=>{ __hour(.92); __tp('feria'); const o={pel:__shot('peluche'), cari:__shot('cari'), q:VSX.mC.uniforms.nightK.value}; __hour(.3); return o; })())"))
    ok(R2['cari']['mean']<=R2['pel']['mean']*1.15+0.01 and R2['q']>0.9, '2g de noche la Caricatura ya no aclara la noche (%s contra %s en Peluche; noche=%s)'%(R2['cari']['mean'],R2['pel']['mean'],round(R2['q'],2)))

    R3=json.loads(await ev("""JSON.stringify((()=>{ __hour(.3); __tp('parque'); const o={}; for(const k of ['0','1','2']){ settings.crTrazo=k; o['t'+k]=__shot('crayon'); } o.pel=__shot('peluche'); const q0=settings.quality; settings.quality='low'; __shot('crayon'); o.lq=VSX.quad.material===VSX.mKl; settings.quality='mid'; __shot('crayon'); o.full=VSX.quad.material===VSX.mK; settings.quality=q0;
      o.hp=[VSX.mE,VSX.mN,VSX.mC,VSX.mK,PX.look,PX.fin].every(m=>m && /HPS sampler2D t(Dep|Ds)/.test(m.fragmentShader) && m.fragmentShader.includes('#define HPS highp')); settings.crTrazo='0'; return o; })())"""))
    print('   ', R3)
    ok(all(R3['t'+k]['err']==0 and R3['t'+k]['sd']>0.03 for k in '012') and len({R3['t0']['mean'],R3['t1']['mean'],R3['t2']['mean']})==3, '2h los 3 trazos de crayón dibujan sin errores y se ven distintos')
    ok(R3['lq'] and R3['full'], '2i Crayones también tiene versión ligera en Baja y completa en Media')
    ok(R3['hp'], '2j las hondas se leen con toda la precisión del teléfono (así no salen rayas horizontales)')
    r=await ev("""(()=>{ settings.vstyle='pixel'; settings.pxSize='2'; const o=[]; let ok=true, lim=true; const q0=camera.quaternion.clone(), p0=camera.position.clone();
      for(let i=0;i<6;i++){ camera.rotation.y+=0.0023; camera.position.x+=0.011; camera.updateMatrixWorld(); const qa=camera.quaternion.clone(), pa=camera.position.clone(); vsRender(scene,camera); if(camera.quaternion.angleTo(qa)>1e-6 || camera.position.distanceTo(pa)>1e-6) ok=false; const f=PX.fin.uniforms.off.value; if(Math.abs(f.x)>1.0001||Math.abs(f.y)>1.0001) lim=false; o.push([+f.x.toFixed(2),+f.y.toFixed(2)]); }
      camera.quaternion.copy(q0); camera.position.copy(p0); camera.updateMatrixWorld(); settings.vstyle='peluche'; return [ok, lim, o]; })()""")
    ok(r[0] and r[1], '2k pixel art: la vista se acomoda de cuadrito en cuadrito (lo que sobra se recorre suave, %s) y la cámara queda como estaba'%r[2][:3])

    # 3. letreros: lo que tiene letras queda marcado (también si se copia a otro dibujo) y entra en la pasada de letras
    r=await ev("""(()=>{ const a=document.createElement('canvas'), q=a.getContext('2d'); window.__vsTxtNew=0; q.fillRect(0,0,4,4); const o=[!!a.__txt, window.__vsTxtNew];
      q.fillText('Hola',1,10); o.push(a.__txt, window.__vsTxtNew); const b=document.createElement('canvas'); b.getContext('2d').drawImage(a,0,0); o.push(b.__txt);
      const c=document.createElement('canvas'); c.getContext('2d').strokeText('x',1,1); o.push(c.__txt);
      __tp('ar_plat'); VSX.nearT=-1e9; VSX.scanT=-1e9; settings.vstyle='pixel'; vsScan(scene); const near=VSX.txt.filter(m=>m.getWorldPosition(new THREE.Vector3()).distanceTo(player.pos)<40);
      o.push(VSX.txt.length, near.length, near.every(m=>(m.layers.mask&4)!==0), vsTxtNear(camera)); return o; })()""")
    ok(r[0]==False and r[1]==0 and r[2]==1 and r[3]==1 and r[4]==1 and r[5]==1, '3a un dibujo con letras queda marcado (y avisa para buscarlo pronto); copiarlo a otro también lo marca; sin letras no %s'%r[:6])
    ok(r[6]>20 and r[7]>=2 and r[8] and r[9], '3b los letreros del minijuego entran en la pasada de letras (se ven nítidos) %s'%r[6:])
    # los carteles de instrucciones se pintan al acercarte: el siguiente vistazo (al segundo) ya los encuentra
    r=await ev("""(()=>{ const tex=[]; scene.traverse(o=>{ const m=o.material; if(o.isMesh && m && !Array.isArray(m) && m.map && m.map.__paint && !m.map.__done) tex.push(o); }); if(!tex.length) return ['ninguno'];
      const o=tex[0], before=VSX.txt.includes(o); o.material.map.__paint(); VSX.scanT=performance.now()-1100; vsScan(scene); return [before, !!o.material.map.image.__txt, VSX.txt.includes(o)]; })()""")
    ok(r==[False,True,True], '3c un cartel de instrucciones recién pintado entra a la pasada de letras al segundo %s'%r)

    r=await ev("""(()=>{ __tp('ar_plat'); __run(6); VSX.scanT=-1e9; vsScan(scene); const v=new THREE.Vector3(); let best=null, bd=40; for(const o of VSX.txt){ if(!o.parent||o.isSprite) continue; const m=o.material; if(m.map&&m.map.__paint) continue; o.getWorldPosition(v); const d=v.distanceTo(player.pos); if(d<bd){ bd=d; best=o; } }
      if(!best) return ['sin letrero']; const box=new THREE.Box3().setFromObject(best), c=box.getCenter(new THREE.Vector3()), sz=box.getSize(new THREE.Vector3()).length(), n=new THREE.Vector3(0,0,1).applyQuaternion(best.getWorldQuaternion(new THREE.Quaternion()));
      camera.position.copy(c).addScaledVector(n,Math.max(1.6,sz*0.9)); camera.lookAt(c); camera.updateMatrixWorld(); VSX.nearT=-1e9;
      const look=st=>{ settings.vstyle=st; const S=scene; for(let k=0;k<2;k++){ if(vsOn()) vsRender(S,camera); else renderer.render(S,camera); } const gl=renderer.getContext(), W=gl.drawingBufferWidth, H=gl.drawingBufferHeight, w=Math.floor(W*.3), h=Math.floor(H*.16), buf=new Uint8Array(4*w*h);
        gl.readPixels(Math.floor(W*.35),Math.floor(H*.42),w,h,gl.RGBA,gl.UNSIGNED_BYTE,buf); const L=[]; for(let i=0;i<buf.length;i+=4) L.push((buf[i]*.2126+buf[i+1]*.7152+buf[i+2]*.0722)/255); L.sort((a,b)=>a-b); return [+L[Math.floor(L.length*.5)].toFixed(2), +L[Math.floor(L.length*.99)].toFixed(2)]; };
      return [look('peluche'), look('neon'), VSX.txtNear]; })()""")
    ok(r[2] and r[0][0]>0.5 and r[1][0]<0.25 and r[1][1]>0.7, '3d en Neón el letrero es de neón: el cartel oscuro y las letras brillan (mitad %s y lo más claro %s; en Peluche el cartel es claro %s)'%(r[1][0],r[1][1],r[0][0]))

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
