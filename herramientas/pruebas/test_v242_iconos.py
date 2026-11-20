# v242 (ronda 1 de íconos): los emojis de los botones de acción, los de arriba, la pausa y el menú se cambian por dibujos
# con el estilo de la barra del Modo libre. El emoji queda escondido dentro del dibujo (el texto por dentro no cambia).
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.033); update(.033,t); petsUpdate(.033,t); } };
  window.__LEFT=()=>{ const w=document.createTreeWalker(document.body,4), L=[]; let n; while((n=w.nextNode())){ const p=n.parentNode; if(!p || p.namespaceURI!=='http://www.w3.org/1999/xhtml' || p.closest('.emi,[data-noic],script,style,textarea,option,title,noscript')) continue; if(emiRe().test(n.data)) L.push(n.data.trim().slice(0,30)); } return L; };
  window.__TICK=()=>new Promise(r=>setTimeout(r,0)); 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev(STEP)

    # 1. la biblioteca de dibujos está cargada
    r=await ev("""(()=>{ const S=[...document.querySelectorAll('symbol[id^="emi-"]')]; const vac=S.filter(s=>!s.firstElementChild).length; const falt=Object.values(EMI_EMO).filter(n=>!document.getElementById('emi-'+n)).length; return [S.length, vac, falt, Object.keys(EMI_SVG).length]; })()""")
    ok(r[0]==r[3] and r[0]>=50 and r[1]==0 and r[2]==0, '🎨 los %s dibujos están cargados (vacíos: %s, emojis sin dibujo: %s)'%(r[0],r[1],r[2]))

    # 2. el menú principal: sin emojis de la lista, y el texto por dentro igual
    r=await ev("""(async()=>{ await __TICK(); const b=document.getElementById('modesBack'); return [__LEFT(), document.querySelectorAll('.emi').length, b?b.textContent.trim():'', b?b.querySelectorAll('.emi').length:0]; })()""")
    ok(len(r[0])==0 and r[1]>5, '🏠 en el menú ya no quedan emojis de la lista (quedan: %s) y hay %s dibujos'%(r[0][:5],r[1]))
    ok(r[2]=='← Volver' and r[3]==1, '← el botón Volver tiene su flecha dibujada y su texto sigue igual (“%s”)'%r[2])

    # 3. avisos y botones de acción
    r=await ev("""(async()=>{ flashNote('💧 Prueba ⭐ lista'); await __TICK(); const t=document.getElementById('toast'); const a=[t.querySelectorAll('.emi').length, t.textContent];
        setActions({label:'🎒 Abrir', run(){}}, {label:'⬆️ Saltar', run(){}}); await __TICK(); const b=[act1.querySelectorAll('.emi').length, act2.querySelectorAll('.emi').length, act1.textContent.trim(), act2.textContent.trim()];
        const w=act1.querySelector('.emi').getBoundingClientRect(), fs=parseFloat(getComputedStyle(act1).fontSize);
        setActions({label:'Sin emoji', run(){}}, null); await __TICK(); const c=act1.querySelectorAll('.emi').length; return [a,b,c,+(w.width/fs).toFixed(2), +(w.height/fs).toFixed(2)]; })()""")
    ok(r[0][0]==2 and r[0][1]=='💧 Prueba ⭐ lista', '📝 un aviso con emojis los muestra dibujados (%s) y su texto no cambia'%r[0][0])
    ok(r[1][0]==1 and r[1][1]==1 and r[1][2].startswith('🎒 Abrir') and r[1][3].startswith('⬆️ Saltar'), '🎒 los botones de acción también (%s, %s) y su texto por dentro queda igual, aun con ⬆️'%(r[1][0],r[1][1]))
    ok(r[2]==0, '🧹 al cambiar el botón a otro texto no queda dibujo viejo')
    ok(1.0<r[3]<1.4 and 1.0<r[4]<1.4, '📏 el dibujo mide como una letra grande (%s × %s)'%(r[3],r[4]))

    # 4. lo que no se toca: apodos (data-noic), listas desplegables y textos dentro de dibujos
    r=await ev("""(async()=>{ const d=document.createElement('div'); d.innerHTML='<span data-noic>⭐Rogi⭐</span><select><option>💧 agua</option></select><textarea>🚀</textarea>'; document.body.appendChild(d); await __TICK();
        const x=[d.querySelectorAll('.emi').length, d.querySelector('option').textContent, d.querySelector('[data-noic]').textContent]; d.remove(); return x; })()""")
    ok(r[0]==0 and r[1]=='💧 agua' and r[2]=='⭐Rogi⭐', '🙋 lo que escribe un jugador y las listas no se tocan')

    # 5. no se queda dando vueltas: después de convertir no hay más trabajo
    r=await ev("""(async()=>{ await __TICK(); const a=EMI_N; await __TICK(); await __TICK(); return [a, EMI_N]; })()""")
    ok(r[0]==r[1], '🔁 no se queda convirtiendo sin parar (%s → %s)'%(r[0],r[1]))

    # 6. el centrado de botones no borra los dibujos
    r=await ev("""(async()=>{ const a=document.querySelectorAll('.emi').length; centerAllText(); await __TICK(); return [a, document.querySelectorAll('.emi').length, __LEFT().length]; })()""")
    ok(r[1]>=r[0] and r[2]==0, '🎯 al recentrar los botones los dibujos siguen ahí (%s → %s)'%(r[0],r[1]))

    # 7. jugando en el Modo libre: sin emojis de la lista y casi sin trabajo por cuadro
    r=await ev("""(async()=>{ freeEnter(); __S(30); await __TICK(); let rec=0; const ob=new MutationObserver(R=>rec+=R.length); ob.observe(document.body,{childList:true,subtree:true,characterData:true});
        const n0=EMI_N, t0=performance.now(); for(let i=0;i<10;i++){ __S(6); await __TICK(); } const ms=performance.now()-t0; ob.disconnect(); return [__LEFT(), EMI_N-n0, rec]; })()""")
    ok(len(r[0])==0, '🧸 en el Modo libre tampoco quedan emojis de la lista (quedan: %s)'%r[0][:5])
    ok(r[1]<=6, '⚡ casi no hay que redibujar mientras juegas (%s conversiones en 60 cuadros; %s cambios en la página)'%(r[1],r[2]))

    # 8. pausa
    r=await ev("""(async()=>{ show('pause'); await __TICK(); const a=__LEFT(); show('play'); await __TICK(); return [a, __LEFT()]; })()""")
    ok(len(r[0])==0 and len(r[1])==0, '⏸️ en la pausa tampoco (quedan: %s / %s)'%(r[0][:5],r[1][:5]))

    ok(not errs, '🚫 sin errores (%s)'%errs[:3])
    await b.close()
asyncio.run(m())
