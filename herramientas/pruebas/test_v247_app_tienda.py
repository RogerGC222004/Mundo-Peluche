# v247: la app para Play Store sin herramientas de prueba ni actualizaciones por fuera de Play, y con los anuncios apagados.
#  A) app con anuncios apagados (window.__MP_APP.pruebas): sin «Actualizar el juego», sin consultar GitHub, sin «Copiar ubicación»,
#     sin «Mostrar coordenadas», sin botones ▶ (tienda, ¿el doble?, piezas de vehículos y de casitas)
#  B) web: todo sigue igual
#  C) app con anuncios prendidos + modo de prueba (5 toques a la versión): nunca pide un anuncio real
import asyncio, json
from playwright.async_api import async_playwright
JUEGO='/home/claude/mundo-peluche.html'
REAL=open('threerepo/build/three.min.js').read()
SRC=open(JUEGO, encoding='utf-8').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+SRC.replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False,"coords":True,"coordsDef":1}
async def abrir(b, pre):
  ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True, user_agent="Mozilla/5.0 (Linux; Android 10) Chrome/120 Mobile")
  pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); gh=[]
  await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');\n%s"%(json.dumps(OPTS),pre))
  async def route(r):
    u=r.request.url
    if 'api.github.com' in u: gh.append(u); await r.abort()
    elif u.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
    elif "three" in u: await r.fulfill(body=REAL, content_type="application/javascript")
    else: await r.abort()
  await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
  await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
  return pg, errs, gh, ctx
VIS="""window.__V=id=>{ const e=document.getElementById(id); return !!e && e.getClientRects().length>0 && !e.closest('[hidden]'); }; 1"""
ESTADO=r"""(async()=>{ const T=()=>new Promise(r=>setTimeout(r,60)); const o={};
  o.install=!document.getElementById('installBtn').hidden;
  show('pause'); await T(); o.copyLoc=!ui('copyLocBtn').hidden; o.diag=!ui('diagBtn').hidden; show('menu'); await T();
  const oc=ui('optCoords').closest('.opt'); o.coordsRow=!oc.hidden; o.coordsOn=!!settings.coords;
  o.adsOk=ADS.ok();
  openShop(); shopCat='gorras'; renderShop(); await T(); const it=SHOP.find(x=>x.cat==='gorras' && x.price>coins+5) || SHOP.find(x=>x.price>0); try{ shopAdRender('r:'+it.id, it.price); }catch(e){} o.shopAd=!ui('shopAdBtn').hidden; o.shopShort=shopShort(it.price,'r:'+it.id); ui('shop').hidden=true;
  ui('adOffer').hidden=true; adOffer(20); o.offer=!ui('adOffer').hidden; ui('adOffer').hidden=true;
  return o; })()"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)

    # A) app, anuncios apagados
    pg,errs,gh,ctx=await abrir(b,"window.__MP_APP={premio:'x', pruebas:true};")
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await pg.wait_for_timeout(1500); r=await ev(ESTADO)
    ok(not r['install'] and not gh, '📲 en la app no hay «Actualizar el juego» ni se consulta GitHub (botón: %s, consultas: %s)'%(r['install'],len(gh)))
    ok(not r['copyLoc'] and not r['diag'], '📍 en la app no están «Copiar ubicación» ni «Ver diagnóstico de conexión»')
    ok(not r['coordsRow'] and not r['coordsOn'], '🧭 en la app no está «Mostrar coordenadas» (y quedan apagadas aunque estuvieran prendidas)')
    ok(not r['adsOk'] and not r['shopAd'] and not r['offer'] and 'anuncio' not in r['shopShort'], '▶ con los anuncios apagados no hay botones de anuncio: tienda, «¿el doble?» ni avisos («%s»)'%r['shopShort'])
    r2=await ev(r"""(async()=>{ const n0=ADS.left(); const v=await ADS.show(); return [v, ADS.left()===n0]; })()""")
    pie=SRC[SRC.index("function vehUI(){"):SRC.index("function vehOpen(){")]
    ok("(ADS.ok()?'<button class=\"vh-btn ad\"" in pie and "viendo un anuncio':'con monedas'" in pie and r2[0]==False and r2[1], '🚗 tampoco en las piezas de vehículos, y pedir un anuncio no hace nada (%s)'%r2)
    r3=await ev("(()=>{ const a=ui('verMenu'); for(let i=0;i<5;i++) a.click(); return [ADS.test, a.textContent]; })()")
    ok(r3[0]==False, '🔢 los 5 toques a la versión no prenden nada con los anuncios apagados (%s)'%r3[1])
    ok(not errs, '🚫 app sin errores (%s)'%errs[:3]); await ctx.close()

    # B) web
    pg,errs,gh,ctx=await abrir(b,"")
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await pg.wait_for_timeout(1500); r=await ev(ESTADO)
    ok(r['copyLoc'] and r['coordsRow'] and r['adsOk'] and r['offer'], '🌐 en la web todo sigue igual: copiar ubicación, coordenadas y botones ▶ (%s)'%r)
    ok(not errs, '🚫 web sin errores (%s)'%errs[:3]); await ctx.close()

    # C) app con anuncios prendidos: el modo de prueba de tu teléfono nunca pide un anuncio real
    pg,errs,gh,ctx=await abrir(b,"window.__MP_APP={premio:'x', pruebas:false}; window.__REAL=0; window.MundoAds={show(){ window.__REAL++; return Promise.resolve(true); }};")
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await pg.wait_for_timeout(1500)
    r=await ev(r"""(async()=>{ const o={ok:ADS.ok()}; await ADS.show(); o.real1=window.__REAL;
        const a=ui('verMenu'); for(let i=0;i<5;i++) a.click(); o.test=ADS.test;
        const pr=ADS.show(); await new Promise(r=>setTimeout(r,300)); const ov=document.getElementById('hadOv'); o.ratito=!!ov && !ov.hidden; try{ ov.querySelector('.skip').click(); }catch(e){} await pr; o.real2=window.__REAL; return o; })()""")
    ok(r['ok'] and r['real1']==1, '📺 con los anuncios prendidos, el botón ▶ pide un anuncio real (%s)'%r)
    ok(r['test'] and r['ratito'] and r['real2']==1, '🧪 con 5 toques a la versión tu teléfono queda en modo prueba: sale el ratito de juego y nunca un anuncio real')
    ok(not errs, '🚫 sin errores (%s)'%errs[:3])
    await b.close()
asyncio.run(m())
