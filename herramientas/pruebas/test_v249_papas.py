# v249: herramientas para papás (Opciones → Para papás)
#  A) se ve el tiempo jugado y las opciones vienen: descanso apagado, sin límite, anuncios prendidos
#  B) cambiar algo pide la operación de adulto (con la mala no cambia) y queda guardado
#  C) aviso de 5 minutos antes del límite (una vez)
#  D) el límite espera a que termines (minijuego/fila) y luego sale; sin botón para cerrarlo; pausa el juego
#  E) «dar más tiempo» solo con la operación: +15 min deja seguir 15 minutos
#  F) a medianoche empieza de cero; si abres el juego con el límite ya cumplido, sale en el menú
#  G) recordatorio de descanso (y si dejaste el juego 5 minutos, cuenta como descanso)
#  H) anuncios apagados: ningún botón ▶ (tienda, «¿el doble?»)
import asyncio, json
from playwright.async_api import async_playwright
JUEGO='/home/claude/mundo-peluche.html'
REAL=open('threerepo/build/three.min.js').read()
SRC=open(JUEGO, encoding='utf-8').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+SRC.replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
async def abrir(b, pre):
  ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True, user_agent="Mozilla/5.0 (Linux; Android 10) Chrome/120 Mobile")
  pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
  await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1'); localStorage.setItem('mundoPelucheNovedades','249');\n%s"%(json.dumps(OPTS),pre))
  async def route(r):
    u=r.request.url
    if u.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
    elif "three" in u: await r.fulfill(body=REAL, content_type="application/javascript")
    else: await r.abort()
  await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
  await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
  return pg, errs, ctx
H=r"""window.__OV=()=>document.getElementById('onlineOv'); window.__CARD=()=>{ const o=__OV(); return o && !o.hidden ? o.textContent : ''; };
window.__RES=()=>{ const t=__OV().querySelector('.online-op').textContent; const m=/^([\d ]+) ([+−×÷]) ([\d ]+) =$/.exec(t); const a=+m[1].replace(/ /g,''), z=+m[3].replace(/ /g,'');
  return m[2]==='+'?a+z: m[2]==='−'?a-z: m[2]==='×'?a*z: a/z; };
window.__ADULT=(ok)=>{ const c=__OV(); c.querySelector('.online-in').value=String(ok?__RES():__RES()+1); c.querySelector('.online-ok').click(); };
window.__W=()=>new Promise(r=>setTimeout(r,80)); 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    pg,errs,ctx=await abrir(b,"")
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev(H); await pg.wait_for_timeout(1500)

    # A
    r=await ev(r"""(async()=>{ ui('options').hidden=false; parSync(); await __W(); const g=ui('papTime').closest('.opt-group');
      const pr=id=>[...ui(id).querySelectorAll('button')].find(b=>b.getAttribute('aria-pressed')==='true').dataset.v;
      return {papas:/Para papás/.test(g.textContent), txt:ui('papTime').textContent, rest:pr('papRest'), lim:pr('papLimit'), ads:ui('papAds').getAttribute('aria-checked'), adsOk:ADS.ok()}; })()""")
    ok(r['papas'] and r['txt'].startswith('Hoy:') and 'Últimos 7 días' in r['txt'], '⏱️ en Para papás se ve el tiempo jugado («%s»)'%r['txt'])
    ok(r['rest']=='0' and r['lim']=='0' and r['ads']=='true' and r['adsOk'], '🆕 al instalar: descanso apagado, sin límite y anuncios con premio prendidos')

    # B
    r=await ev(r"""(async()=>{ const o={}; ui('papLimit').querySelector('[data-v="30"]').click(); await __W(); o.ask=/Solo para adultos/.test(__CARD());
      __ADULT(false); await __W(); o.malo=PAR.limit===0 && /Solo para adultos/.test(__CARD());
      __ADULT(true); await __W(); o.bien=PAR.limit===30 && JSON.parse(localStorage.getItem('mundoPeluchePapas')).limit===30 && !__CARD();
      ui('papRest').querySelector('[data-v="45"]').click(); await __W(); __ADULT(true); await __W(); o.rest=PAR.rest;
      ui('options').hidden=true; return o; })()""")
    ok(r['ask'] and r['malo'], '🔒 cambiar el límite pide la operación de adulto; con la respuesta mala no cambia')
    ok(r['bien'] and r['rest']==45, '💾 con la buena queda guardado (límite 30 min, descanso 45 min)')

    # C: aviso de 5 minutos
    await ev("startGame(); 1"); await pg.wait_for_timeout(800)
    r=await ev(r"""(async()=>{ const o={}; PARS.rest=0; TT.d[ttDay()]=30*60-280; parTick(); await __W(); o.c1=__CARD(); __OV().querySelector('.par-ok').click(); await __W();
      parTick(); await __W(); o.c2=__CARD(); return o; })()""")
    ok('5 minutos' in r['c1'] and not r['c2'], '⭐ 5 minutos antes avisa «Te quedan 5 minutos», una sola vez')

    # D: el límite espera a que termines
    r=await ev(r"""(async()=>{ const o={}; MGQ.a=0; TT.d[ttDay()]=30*60+5; for(let i=0;i<3;i++) parTick(); await __W(); o.esperando=!__CARD() && state==='play';
      MGQ.a=-1; parTick(); await __W(); o.card=__CARD(); o.pausa=state; o.sinCerrar=!__OV().querySelector('.par-ok') && !!__OV().querySelector('.par-more');
      onlineClose(); parTick(); await __W(); o.vuelve=/Por hoy es todo/.test(__CARD()); return o; })()""")
    ok(r['esperando'], '🎮 si el tiempo se acaba en un minijuego (o en la fila), espera a que termines')
    ok('Por hoy es todo' in r['card'] and r['pausa']=='pause', '🌙 al terminar sale «¡Por hoy es todo!» y el juego queda en pausa')
    ok(r['sinCerrar'] and r['vuelve'], '🚪 no tiene botón para cerrarse, y si se esconde vuelve a salir')
    r=await ev(r"""(async()=>{ PARS.lim=false; onlineClose(); MGQ.a=0; PARS.busy=600.5; parTick(); await __W(); const c=__CARD(); MGQ.a=-1; return c; })()""")
    ok('Por hoy es todo' in r, '⌛ si lo que haces dura mucho (más de 10 min de espera), sale de todos modos')

    # E: dar más tiempo
    r=await ev(r"""(async()=>{ const o={}; __OV().querySelector('.par-more').click(); await __W(); __ADULT(false); await __W(); o.malo=/Solo para adultos/.test(__CARD());
      __ADULT(true); await __W(); o.op=/\+15 min/.test(__CARD()); __OV().querySelector('[data-x="15"]').click(); await __W();
      o.cerrada=!__CARD(); o.left=ttLeft(); parTick(); await __W(); o.noVuelve=!__CARD(); return o; })()""")
    ok(r['malo'] and r['op'], '🔑 «Soy adulto: dar más tiempo» pide la operación y ofrece +15, +30 o sin límite hoy')
    ok(r['cerrada'] and r['noVuelve'] and 14*60 <= r['left'] <= 16*60, '➕ con +15 min se puede seguir jugando 15 minutos (quedan %d s)'%r['left'])
    ok(not errs, '🚫 sin errores (%s)'%errs[:3]); await ctx.close()

    # F: medianoche y abrir con el límite cumplido
    from datetime import date, timedelta
    hoy=date.today().isoformat(); ayer=(date.today()-timedelta(days=1)).isoformat()
    pre="localStorage.setItem('mundoPeluchePapas', JSON.stringify({rest:0,limit:30,ads:true})); localStorage.setItem('mundoPelucheTiempo', JSON.stringify({d:{'%s':4000},xd:'%s',x:-1,w:0}));"%(ayer,ayer)
    pg,errs,ctx=await abrir(b,pre); ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600); await ev(H); await pg.wait_for_timeout(2500)
    r=await ev("(()=>({left:ttLeft(), x:ttExtra(), card:__CARD(), week:ttWeek()}))()")
    ok(1700 <= r['left'] <= 1800 and r['x']==0 and not r['card'] and r['week']>=4000, '🕛 al día siguiente empieza de cero (el «sin límite hoy» de ayer ya no cuenta; la semana sí suma)')
    await ctx.close()
    pre="localStorage.setItem('mundoPeluchePapas', JSON.stringify({rest:0,limit:30,ads:true})); localStorage.setItem('mundoPelucheTiempo', JSON.stringify({d:{'%s':1900},xd:'%s',x:0,w:1800}));"%(hoy,hoy)
    pg,errs,ctx=await abrir(b,pre); ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600); await ev(H); await pg.wait_for_timeout(3000)
    r=await ev("(()=>[__CARD(), state])()")
    ok('Por hoy es todo' in r[0] and r[1]=='menu', '📵 si abres el juego con el límite ya cumplido, sale en el menú')
    ok(not errs, '🚫 sin errores (%s)'%errs[:3]); await ctx.close()

    # G: descanso
    pg,errs,ctx=await abrir(b,"localStorage.setItem('mundoPeluchePapas', JSON.stringify({rest:30,limit:0,ads:true}));"); ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600); await ev(H); await pg.wait_for_timeout(1500)
    r=await ev(r"""(async()=>{ const o={}; startGame(); await __W(); PARS.rest=29*60; parTick(); await __W(); o.antes=__CARD();
      PARS.rest=30*60; MGQ.a=0; parTick(); await __W(); o.ocupado=__CARD(); MGQ.a=-1; parTick(); await __W(); o.card=__CARD(); o.st=state;
      __OV().querySelector('.par-ok').click(); await __W(); o.cero=PARS.rest<5;
      PARS.rest=20*60; PARS.hid=301; parTick(); o.descanso=PARS.rest<5; return o; })()""")
    ok(not r['antes'] and not r['ocupado'] and 'descanso' in r['card'].lower() and r['st']=='pause', '🧸 a los 30 min (y en un momento tranquilo) sale «¡Hora de un descanso!»')
    ok(r['cero'] and r['descanso'], '💧 al cerrarlo vuelve a contar desde cero; dejar el juego 5 minutos cuenta como descanso')
    ok(not errs, '🚫 sin errores (%s)'%errs[:3]); await ctx.close()

    # H: anuncios apagados
    pg,errs,ctx=await abrir(b,""); ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600); await ev(H); await pg.wait_for_timeout(1500)
    r=await ev(r"""(async()=>{ const o={}; o.antes=ADS.ok(); ui('papAds').click(); await __W(); __ADULT(true); await __W(); o.ok=ADS.ok(); o.sw=ui('papAds').getAttribute('aria-checked');
      openShop(); shopCat='gorras'; renderShop(); await __W(); const it=SHOP.find(x=>x.cat==='gorras' && x.price>coins+5) || SHOP.find(x=>x.price>0); try{ shopAdRender('r:'+it.id, it.price); }catch(e){}
      o.shopAd=!ui('shopAdBtn').hidden; o.short=shopShort(it.price,'r:'+it.id); ui('shop').hidden=true;
      ui('adOffer').hidden=true; adOffer(20); o.offer=!ui('adOffer').hidden; ui('adOffer').hidden=true;
      o.guardado=JSON.parse(localStorage.getItem('mundoPeluchePapas')).ads; return o; })()""")
    ok(r['antes'] and not r['ok'] and r['sw']=='false' and r['guardado']==False, '📺 un adulto puede apagar los anuncios con premio (queda guardado)')
    ok(not r['shopAd'] and not r['offer'] and 'anuncio' not in r['short'], '🚫 con los anuncios apagados no hay ningún botón ▶ (tienda, «¿el doble?», avisos)')
    ok(not errs, '🚫 sin errores (%s)'%errs[:3]); await ctx.close()
    await b.close()
asyncio.run(m())
