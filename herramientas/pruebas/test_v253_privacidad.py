# v253: aviso de privacidad para anuncios
#  A) web: Opciones → Para papás → «Privacidad y anuncios» pide la operación de adulto y explica los anuncios con palabras simples;
#     «Leer la política» abre la página de privacidad; en la web no hay botón de opciones de Google
#  B) app con anuncios apagados (pruebas): dice que todavía no hay anuncios
#  C) app con anuncios prendidos y Google pidiendo opciones de privacidad: sale el botón y abre las opciones de Google
#  D) el puente de la app (con un AdMob de mentiritas): primero la herramienta de privacidad (marcada para menores), luego AdMob;
#     si Google pide el formulario lo muestra; si la herramienta falla, sigue; sin permiso no pide anuncios; cada anuncio va sin personalizar
import asyncio, json, os, re, subprocess
from playwright.async_api import async_playwright
JUEGO='/home/claude/mundo-peluche.html'
REAL=open('threerepo/build/three.min.js').read()
SRC=open(JUEGO, encoding='utf-8').read(); VER=re.search(r"const GAME_VERSION='(\d+)'",SRC).group(1)
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+SRC.replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
PUENTE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','app','puente.js')
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
async def abrir(b, pre):
  ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True)
  pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
  await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1'); localStorage.setItem('mundoPelucheNovedades','%s'); window.__fbNoNav=true;\n%s"%(json.dumps(OPTS),VER,pre))
  async def route(r):
    u=r.request.url
    if u.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
    elif "three" in u: await r.fulfill(body=REAL, content_type="application/javascript")
    else: await r.abort()
  await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
  await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
  return pg, errs, ctx
TARJETA=r"""(async()=>{ const T=()=>new Promise(r=>setTimeout(r,80)); const OV=()=>document.getElementById('onlineOv'); const o={};
  ui('options').hidden=false; await T(); const b=ui('papPrivacy'); o.vis=b.getClientRects().length>0 && /Para papás/.test(b.closest('.opt-group').textContent);
  b.click(); await T(); let c=OV(); o.adult=!c.hidden && /Solo para adultos/.test(c.textContent);
  const m=/^([\d ]+) ([+−×÷]) ([\d ]+) =$/.exec(c.querySelector('.online-op').textContent), a=+m[1].replace(/ /g,''), z=+m[3].replace(/ /g,'');
  c.querySelector('.online-in').value=String(m[2]==='+'?a+z: m[2]==='−'?a-z: m[2]==='×'?a*z: a/z); c.querySelector('.online-ok').click(); await T(); c=OV();
  o.txt=c.hidden?'':c.textContent; o.btn=!!c.querySelector('.pv-opt'); o.go=!!c.querySelector('.pv-go'); return o; })()"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    # A) web
    pg,errs,ctx=await abrir(b,"")
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    r=await ev(TARJETA)
    ok(r['vis'] and r['adult'], '🔒 «Privacidad y anuncios» está en Para papás y primero pide la operación de adulto')
    t=r['txt']
    ok('nunca personalizados' in t and 'Máximo 10' in t and 'identificador de publicidad' in t and 'Anuncios con premio' in t, '📄 explica con palabras simples: solo con ▶, máximo 10, nunca personalizados, sin identificador, y cómo apagarlos')
    ok('(web)' in t and not r['btn'], '🌐 en la web dice que no hay anuncios de verdad y no sale el botón de opciones de Google')
    r=await ev("(()=>{ document.querySelector('#onlineOv .pv-go').click(); return [window.__pvLast, document.getElementById('onlineOv').hidden]; })()")
    ok(r[0]=='https://rogergc222004.github.io/Mundo-Peluche/privacidad.html' and r[1], '🔗 «Leer la política» abre la página de privacidad del juego')
    ok(not errs, '🚫 sin errores (%s)'%errs[:3]); await ctx.close()
    # B) app con anuncios apagados
    pg,errs,ctx=await abrir(b,"window.__MP_APP={premio:'x', pruebas:true};")
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    r=await ev(TARJETA)
    ok('todavía no muestra anuncios' in r['txt'] and not r['btn'], '📱 en la app con los anuncios apagados dice que todavía no hay anuncios')
    await ctx.close()
    # C) app con anuncios prendidos y Google pidiendo opciones
    pg,errs,ctx=await abrir(b,"window.__MP_APP={premio:'x', pruebas:false}; window.__pvOpen=0; window.MundoPriv={need:true, status:'NOT_REQUIRED', done:true, open(){ window.__pvOpen++; return Promise.resolve(); }};")
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    r=await ev(TARJETA)
    ok('prendidos' in r['txt'] and r['btn'], '⚙️ con anuncios prendidos dice «prendidos» y, si Google lo pide, sale «Opciones de privacidad de anuncios»')
    r=await ev("(async()=>{ document.querySelector('#onlineOv .pv-opt').click(); await new Promise(r=>setTimeout(r,80)); return [window.__pvOpen, document.getElementById('onlineOv').hidden]; })()")
    ok(r==[1,True], '👉 ese botón abre las opciones de privacidad de Google')
    r=await ev("(()=>{ PAR.ads=false; return privacyState(); })()")
    ok('apagados por un adulto' in r, '🙅 si un adulto apagó los anuncios, lo dice')
    ok(not errs, '🚫 sin errores (%s)'%errs[:3]); await ctx.close(); await b.close()
  # D) el puente con un AdMob de mentiritas (en Node)
  js=r"""
const src=require('fs').readFileSync(process.argv[1],'utf8');
function corre(conf){ return new Promise(fin=>{ const log=[]; const L={}; let tmo=[];
  const AdMob={ requestConsentInfo:o=>{ log.push(['consent',o]); return conf.fail?Promise.reject(new Error('x')):Promise.resolve(conf.info); },
    showConsentForm:()=>{ log.push(['form']); return Promise.resolve(Object.assign({},conf.info,{status:'OBTAINED'})); },
    showPrivacyOptionsForm:()=>{ log.push(['opciones']); return Promise.resolve(); },
    initialize:o=>{ log.push(['init',o]); return Promise.resolve(); },
    addListener:(ev,f)=>{ L[ev]=f; return {remove(){}}; },
    prepareRewardVideoAd:o=>{ log.push(['prep',o]); return Promise.resolve(); },
    showRewardVideoAd:()=>{ log.push(['show']); setTimeout(()=>L.onRewardedVideoAdDismissed&&L.onRewardedVideoAdDismissed(),10); return Promise.resolve({amount:1,type:'x'}); } };
  const window={ __MP_APP:{premio:'p', pruebas:false}, Capacitor:{ isNativePlatform:()=>true, Plugins:{AdMob, App:null} } };
  const setTimeout_=(f,ms)=>{ if(ms===4000) f(); else if(ms<10000) setTimeout(f,ms); return 0; };
  new Function('window','setTimeout',src)(window,setTimeout_);
  setTimeout(()=>{ const P=window.MundoPriv; const r={log:log.map(x=>x[0]), first:log[0], init:(log.find(x=>x[0]==='init')||[])[1], need:P&&P.need, done:P&&P.done};
    window.MundoAds.show().then(v=>{ r.prize=v; r.prep=(log.find(x=>x[0]==='prep')||[])[1]||null; r.log2=log.map(x=>x[0]); fin(r); }); },50); }); }
(async()=>{ const out={};
  out.normal=await corre({info:{status:'NOT_REQUIRED', canRequestAds:true, privacyOptionsRequirementStatus:'NOT_REQUIRED', isConsentFormAvailable:false}});
  out.form=await corre({info:{status:'REQUIRED', canRequestAds:true, privacyOptionsRequirementStatus:'REQUIRED', isConsentFormAvailable:true}});
  out.falla=await corre({fail:true});
  out.sin=await corre({info:{status:'REQUIRED', canRequestAds:false, privacyOptionsRequirementStatus:'NOT_REQUIRED', isConsentFormAvailable:false}});
  console.log(JSON.stringify(out)); })();
"""
  o=json.loads(subprocess.run(['node','-e',js,PUENTE],capture_output=True,text=True,timeout=60).stdout)
  n=o['normal']
  ok(n['first'][0]=='consent' and n['first'][1]=={'tagForUnderAgeOfConsent':True} and n['log'].index('consent')<n['log'].index('init'), '🛡️ la app primero revisa la privacidad con Google (marcada para menores) y después prepara AdMob')
  ok(n['init']['tagForChildDirectedTreatment'] and n['init']['tagForUnderAgeOfConsent'] and n['init']['maxAdContentRating']=='General' and 'form' not in n['log'] and n['need'] is False, '🧒 AdMob sigue marcado para niños y todo público; sin formulario para el jugador')
  ok(n['prize'] is True and n['prep']['npa'] is True, '🎁 cada anuncio se pide sin personalizar y da su premio')
  f=o['form']
  ok('form' in f['log'] and f['need'] is True, '📋 si Google pidiera el formulario lo muestra, y avisa al juego que hace falta el botón de opciones')
  x=o['falla']
  ok('init' in x['log'] and x['done'] is True and x['prize'] is True, '🧯 si la herramienta de privacidad falla, el juego sigue (los anuncios ya van para niños y sin personalizar)')
  s=o['sin']
  ok(s['prize'] is False and s['prep'] is None, '✋ si Google dice que no se pueden pedir anuncios, no se pide ninguno (y no hay premio)')
  pv=open(os.path.join(os.path.dirname(PUENTE),'..','privacidad.html'),encoding='utf-8').read()
  ok('herramienta de privacidad de Google' in pv and 'Privacidad y anuncios' in pv, '📜 la política de privacidad lo explica')
asyncio.run(m())
