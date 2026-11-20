# v244 (ronda 3 de íconos): Modo libre, tu planicie, máquina de sustancias, editores y Mis creaciones con íconos dibujados;
# en Crear criatura y Crear objeto cada opción se ve con la foto de tu criatura/objeto de verdad (sin fondo).
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.033); update(.033,t); } };
  window.__TICK=()=>new Promise(r=>setTimeout(r,0));
  window.__FLUSH=()=>{ for(let k=0;k<600 && SHOP_THQ.length;k++){ const [g,sw,f]=SHOP_THQ.shift(); if(g===shopThGen && sw.isConnected){ const v=f(); if(v!==undefined) sw.style.background=v; } } };
  window.__EMO=el=>{ const w=document.createTreeWalker(el,4), L=[]; let n; const re=/[\\u{1F300}-\\u{1FAFF}\\u{2600}-\\u{27BF}\\u{2B50}\\u{2B55}\\u{2190}-\\u{21FF}\\u{25A0}-\\u{25FF}]/u; while((n=w.nextNode())){ const p=n.parentNode; if(!p || p.closest('.emi,script,style,textarea,option,title')) continue; const t=n.data.replace(/[▮▯●•]/g,''); if(re.test(t)) L.push(t.trim().slice(0,30)); } return L; };
  window.__PH=el=>{ const S=[...el.querySelectorAll('.sw.ph')]; return [S.length, S.filter(s=>/data:image\\/(png|webp)/.test(s.style.backgroundImage)).length, new Set(S.map(s=>s.style.backgroundImage)).size]; }; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type in ('warning','error') and ('foto' in m.text or 'criatura' in m.text) else None)
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 900)
    await ev(STEP)

    r=await ev("""(()=>{ const S=[...document.querySelectorAll('symbol[id^="emi-"]')]; return [S.length, Object.keys(EMI_SVG).length, S.filter(s=>!s.firstElementChild).length, S.filter(s=>/[~¤§]/.test(s.innerHTML)).length]; })()""")
    ok(r[0]==r[1] and r[0]>=140 and r[2]==0 and r[3]==0, '🎨 los %s dibujos están completos (vacíos: %s, mal armados: %s)'%(r[0],r[2],r[3]))

    # 1. Crear criatura: las opciones con foto y las de “cómo se porta” con dibujo
    r=await ev("""(async()=>{ const out={}; crOpen(); await __TICK(); for(const t of ['cuerpo','orejas','cola','alas','patas']){ CR.tab=t; crRender(); __FLUSH(); await __TICK(); out[t]=__PH(ui('crGrid')); }
        const ic={}; for(const t of ['tam','porta']){ CR.tab=t; crRender(); await __TICK(); ic[t]=[ui('crGrid').querySelectorAll('.shop-item').length, ui('crGrid').querySelectorAll('.shop-item .emi use').length]; }
        const em=__EMO(crEl); return [out, ic, em]; })()""")
    ok(all(v[0]>=4 and v[1]==v[0] and v[2]==v[0] for v in r[0].values()), '🐾 en Crear criatura cada opción tiene la foto de tu criatura con esa opción, todas distintas (%s)'%r[0])
    ok(all(v[1]>=v[0]-1 and v[0]>=4 for v in r[1].values()), '🦘 tamaño, cómo se porta y velocidad tienen su dibujo (%s)'%r[1])
    ok(len(r[2])==0, '🚫 sin emojis en Crear criatura (quedan: %s)'%r[2][:4])

    # 2. la foto cambia con tus colores
    r=await ev("""(async()=>{ CR.tab='orejas'; crRender(); __FLUSH(); const a=ui('crGrid').querySelector('.sw.ph').style.backgroundImage; CR.d.c1=(CR.d.c1+3)%FREE_COLS.length; crRender(); __FLUSH(); const b=ui('crGrid').querySelector('.sw.ph').style.backgroundImage; return [a.length>100, a!==b]; })()""")
    ok(r[0] and r[1], '🎨 si cambias el color de tu criatura, las fotos de las opciones también cambian')

    # 3. Crear objeto
    r=await ev("""(async()=>{ crClose(false); obOpen(); await __TICK(); const out={}; for(const t of ['pieza','mango','adorno']){ CR.tab=t; crRender(); __FLUSH(); await __TICK(); out[t]=__PH(ui('crGrid')); }
        CR.tab='hace'; crRender(); await __TICK(); const h=[ui('crGrid').querySelectorAll('.shop-item').length, ui('crGrid').querySelectorAll('.shop-item .emi use').length]; const em=__EMO(crEl); crClose(false); return [out,h,em]; })()""")
    ok(all(v[0]>=4 and v[1]==v[0] and v[2]==v[0] for v in r[0].values()), '🍩 en Crear objeto la pieza, el mango y el adorno se ven con foto (%s)'%r[0])
    ok(r[1][0]==4 and r[1][1]==4, '🤲 “qué hace” tiene sus 4 dibujos')
    ok(len(r[2])==0, '🚫 sin emojis en Crear objeto (quedan: %s)'%r[2][:4])

    # 4. Modo libre: caja de piezas, tu planicie, máquina de sustancias
    r=await ev("""(async()=>{ freeEnter(); __S(10); freeOpenBox(); await __TICK(); const box=ui('freeBox'), out={}; for(const t of mapTabs().map(x=>x[0])){ FREE.tab=t; FREE.sub=''; freeRenderBox(); await __TICK(); const e=__EMO(box); if(e.length) out[t]=e; }
        const tabs=[...ui('freeTabs').children], ti=tabs.filter(x=>x.querySelector('.emi')).length; box.hidden=true;
        freeEnvOpen(); await __TICK(); const env=document.querySelector('.env-card'), ee=env?__EMO(env.parentNode):['sin panel'], ei=env?env.querySelectorAll('.emi').length:0; if(env) env.querySelector('#freeEnvOk').click();
        const o=freeAddStatic({k:'p',a:'fuentes',b:FU_DEF},FREE.X+3,FREE.Y,FREE.Z+3,0,true); __S(2); let fe=['sin máquina'], fi=0; try{ fuOpen(o); await __TICK(); const pn=document.querySelector('.fu-card')||document.querySelector('#fuOv')||document.querySelector('[id^="fu"]:not([hidden])'); fe=__EMO(ui('freeBubOv')); fi=ui('freeBubOv').querySelectorAll('.emi use[href="#emi-prendido"],.emi use[href="#emi-apagado"]').length; }catch(e){ fe=[String(e)]; }
        return [out, tabs.length, ti, ee, ei, fe, fi]; })()""")
    ok(len(r[0])==0, '🧱 en la caja de piezas del Modo libre no quedan emojis (%s)'%r[0])
    ok(r[1]>=6 and r[2]==r[1], '🗂️ las %s pestañas del Modo libre tienen su dibujo'%r[1])
    ok(len(r[3])==0 and r[4]>=10, '🌤️ Tu planicie (piso, hora y clima) con %s dibujos y sin emojis (%s)'%(r[4],r[3][:3]))
    ok(len(r[5])==0 and r[6]>=4, '⛲ la máquina de sustancias con sus dibujos (prendida/apagada: %s) y sin emojis (%s)'%(r[6],r[5][:3]))

    ok(not errs, '🚫 sin errores (%s)'%errs[:3])
    await b.close()
asyncio.run(m())
