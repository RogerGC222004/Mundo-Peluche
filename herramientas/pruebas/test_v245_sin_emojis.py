# v245: el escáner de emojis. Meta: 0 emojis en el juego.
#  A) en el código: cada emoji que se puede mostrar tiene su dibujo (fuera de comentarios y de la tabla de dibujos)
#  B) en la página, después de recorrer muchas pantallas: ningún emoji sin dibujar (ni en textos de ayuda, títulos ni listas)
#  C) en los letreros pintados (canvas): los emojis se pintan con su dibujo
import asyncio, json, re
from playwright.async_api import async_playwright
JUEGO='/home/claude/mundo-peluche.html'
REAL=open('threerepo/build/three.min.js').read()
SRC=open(JUEGO, encoding='utf-8').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+SRC.replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
TEXTO_OK='●▮▯↔'   # (símbolos de texto, no emojis: se quedan como letras)
EMO=re.compile('(?:[\u2190-\u21ff\u2300-\u23ff\u2460-\u24ff\u25a0-\u27bf\u2900-\u2bff\U0001F000-\U0001FAFF][\uFE0F\U0001F3FB-\U0001F3FF]*)(?:\u200D[\u2600-\u27bf\U0001F000-\U0001FAFF]\uFE0F?)*|[\u00a9\u00ae\u203c\u2049\u2122\u2139]\uFE0F')
STEP=r"""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.033); update(.033,t); } };
  window.__TICK=()=>new Promise(r=>setTimeout(r,0));
  window.__RE=/[\u{2190}-\u{21FF}\u{2300}-\u{23FF}\u{2460}-\u{24FF}\u{25A0}-\u{27BF}\u{2900}-\u{2BFF}\u{1F000}-\u{1FAFF}]/u;
  window.__OK=t=>t.replace(/[●▮▯↔]/g,'');
  window.__SCAN=()=>{ const out=[]; const w=document.createTreeWalker(document.body,4); let n;
    while((n=w.nextNode())){ const p=n.parentNode; if(!p || p.closest('.emi,script,style,[data-noic]')) continue; if(p.namespaceURI!=='http://www.w3.org/1999/xhtml'){ if(__RE.test(__OK(n.data))) out.push('svg: '+n.data.trim().slice(0,40)); continue; } if(__RE.test(__OK(n.data))) out.push((p.tagName==='OPTION'?'lista: ':p.tagName==='TEXTAREA'?'caja: ':'')+n.data.trim().slice(0,40)); }
    for(const el of document.querySelectorAll('[placeholder],[title],[aria-label],[alt],input[type=button],input[type=submit]')) for(const a of ['placeholder','title','aria-label','alt','value']){ const v=el.getAttribute(a); if(v && __RE.test(__OK(v)) && !(a==='value' && el.matches('input[type=text],input[type=search],textarea,#saveCode'))) out.push(a+': '+v.slice(0,40)); }
    if(__RE.test(__OK(document.title))) out.push('título: '+document.title); return [...new Set(out)]; }; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)

    # A) el código
    a=SRC.index('// ---------------- v242: ÍCONOS DIBUJADOS'); a=SRC.rindex('// ====',0,a); z=SRC.index('emiInit();\n',a)
    tabla=json.loads(re.search(r'const EMI_EMO=(\{.*?\});',SRC[a:z]).group(1)); src=SRC[:a]+SRC[z:]
    falta={}
    for i,l in enumerate(src.split('\n')):
      for mm in EMO.finditer(l):
        e=mm.group().replace('\uFE0F','')
        pre=l[:mm.start()]
        com=l.lstrip().startswith('//') or (bool(re.search(r'(^|[^:\'"\\])//',pre)) and pre.count("'")%2==0 and pre.count('`')%2==0 and pre.count('"')%2==0)
        if not com and '/*' in pre and '*/' not in pre[pre.rindex('/*'):]: com=True
        if com or e in tabla or e in TEXTO_OK: continue
        falta.setdefault(e,[]).append(i+1)
    ok(not falta, '🔍 en el código, todos los emojis que se pueden ver tienen su dibujo (%s dibujos para %s emojis; sin dibujo: %s)'%(len(set(tabla.values())),len(tabla),{k:v[:3] for k,v in list(falta.items())[:8]}))

    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 900)
    await ev(STEP)

    # B) recorrido por muchas pantallas
    r=await ev(r"""(async()=>{ const hechos=[], fallos=[]; const T=async(n,f)=>{ try{ await f(); await __TICK(); hechos.push(n); }catch(e){ fallos.push(n+': '+String(e).slice(0,60)); } };
        await T('menú', ()=>{});
        await T('modos', ()=>{ try{ menuModes(true); }catch(e){} });
        await T('opciones', ()=>{ ui('options').hidden=false; });
        await T('controles', ()=>{ ui('controls').hidden=false; });
        await T('mi progreso', ()=>{ ui('saveBtn').click(); });
        await T('minijuegos', ()=>openMgq());
        await T('tienda (todas las pestañas)', async()=>{ openShop(); for(const body of [null,'av_chibi','av_amigu']){ if(body) wardrobe.eq.body=body; else delete wardrobe.eq.body; for(const c of SHOP_CATS){ shopCat=c.id; renderShop(); await __TICK(); } } delete wardrobe.eq.body; });
        await T('accesorios con filtros', async()=>{ wardrobe.eq.body='av_chibi'; shopCat='caccesorios'; renderShop(); await __TICK(); delete wardrobe.eq.body; });
        await T('crear criatura', async()=>{ crOpen(); for(const [id] of CR_TABS){ CR.tab=id; crRender(); await __TICK(); } crClose(false); });
        await T('crear objeto', async()=>{ obOpen(); for(const [id] of OB_TABS){ CR.tab=id; crRender(); await __TICK(); } crClose(false); });
        await T('mis creaciones', async()=>{ for(const t of ['mapa','criatura','objeto']){ try{ mapType=t; renderMaps(); }catch(e){} await __TICK(); } });
        await T('modo libre', async()=>{ freeEnter(); __S(10); });
        await T('caja de piezas (todas)', async()=>{ ui('freeBox').hidden=false; for(const [id] of mapTabs()){ FREE.tab=id; FREE.sub=''; freeRenderBox(); await __TICK(); for(const s of [...ui('freeSubs').querySelectorAll('.fchip')]){ s.click(); await __TICK(); } } ui('freeBox').hidden=true; });
        await T('tu planicie', async()=>{ freeEnvOpen(); await __TICK(); const e=document.querySelector('#freeEnvOk'); if(e) e.click(); });
        await T('máquina de sustancias', async()=>{ const o=freeAddStatic({k:'p',a:'fuentes',b:FU_DEF},FREE.X+3,FREE.Y,FREE.Z+3,0,true); __S(2); for(let i=0;i<4;i++){ FU.tab=i; fuOpen(o); await __TICK(); } });
        await T('pausa', ()=>show('pause'));
        await T('jugar', ()=>show('play'));
        await T('avisos con todos los dibujos', async()=>{ flashNote(Object.keys(EMI_EMO).join(' ')); await __TICK(); });
        return [hechos, fallos, __SCAN()]; })()""")
    ok(len(r[1])==0, '🧭 se recorrieron %s pantallas (fallaron: %s)'%(len(r[0]),r[1][:4]))
    ok(len(r[2])==0, '🚫 en la página no queda ningún emoji sin dibujo, ni en textos de ayuda, títulos o listas (quedan: %s)'%r[2][:8])

    # C) letreros pintados
    r=await ev(r"""(()=>{ const c=document.createElement('canvas'); c.width=c.height=120; const g=c.getContext('2d'); g.font='800 60px sans-serif'; g.textAlign='center'; g.textBaseline='middle'; const n0=EMI_CV; g.fillText('🍎',60,60);
        const d=g.getImageData(0,0,120,120).data; let cafe=0, rojo=0; for(let i=0;i<d.length;i+=4){ if(d[i+3]<200) continue; const R=d[i],G=d[i+1],B=d[i+2]; if(Math.abs(R-90)<25 && Math.abs(G-68)<25 && Math.abs(B-38)<25) cafe++; if(R>200 && G<110 && B<100) rojo++; }
        const c2=document.createElement('canvas'), g2=c2.getContext('2d'); g2.font='40px sans-serif'; g2.__noic=true; const n1=EMI_CV; g2.fillText('🍎 Ana',10,30);
        return [EMI_CV>n0, cafe, rojo, EMI_CV===n1, n0]; })()""")
    ok(r[0] and r[1]>40 and r[2]>200, '🎨 un emoji pintado en un letrero sale con su dibujo (contorno café: %s puntos, rojo: %s)'%(r[1],r[2]))
    ok(r[3], '🙋 lo que escribe un jugador (su apodo) se pinta tal cual')
    ok(r[4]>0, '🪧 los letreros del mundo ya usan los dibujos (%s letreros con dibujo al cargar)'%r[4])

    ok(not errs, '🚫 sin errores (%s)'%errs[:3])
    await b.close()
asyncio.run(m())
