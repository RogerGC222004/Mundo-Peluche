# v250: «Solo salas privadas», «Ocultar apodos de otros», Logros (botón del menú) y Misiones del día (cartel del castillo)
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
  await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1'); localStorage.setItem('mundoPelucheNovedades','250');\n%s"%(json.dumps(OPTS),pre))
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
window.__W=(t)=>new Promise(r=>setTimeout(r,t||80)); window.__NOTES=[]; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    pg,errs,ctx=await abrir(b,"localStorage.setItem('mundoPeluchePeces', JSON.stringify({0:6,1:5,2:2}));")
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev(H); await pg.wait_for_timeout(2500)
    await ev("const _fn=flashNote; flashNote=function(t){ __NOTES.push(String(t)); return _fn.apply(this,arguments); }; 1")

    # A) solo salas privadas
    r=await ev(r"""(async()=>{ const o={}; o.def=!PAR.priv && !PAR.hideN; ui('options').hidden=false; await __W();
      ui('papPriv').click(); await __W(); __ADULT(false); await __W(); o.malo=!PAR.priv; __ADULT(true); await __W(); o.on=PAR.priv && JSON.parse(localStorage.getItem('mundoPeluchePapas')).priv===true;
      ui('options').hidden=true; openMp(); await __W(); o.salas=document.querySelector('#mp .mp-rooms').hidden; o.privada=isPrivateChoice();
      ui('mpPrivate').click(); await __W(); o.noCambia=isPrivateChoice();
      let args=null; const _j=joinRoom; joinRoom=(c,pub)=>{ args=[c,pub]; }; ui('mpCreate').click(); joinRoom=_j; o.pub=args&&args[1];
      ui('mp').hidden=true; onlineSet(true); ONLINE.tip=true; const nb=__NOTES.length; ui('mgBtn').click(); await __W(); ui('mgqList').querySelector('.mgq-b.jug').click(); await __W(); o.filas=MGQ.a<0; o.aviso=__NOTES.slice(nb).join(' '); closeMgq();   /* v264: la lista se abre (Tú solo y CPU); «Jugadores» no deja entrar a la fila y avisa por qué */
      fnRooms(); o.libre=/privadas/.test(ui('freeRooms').textContent) && ui('freePub').hidden; return o; })()""")
    ok(r['def'], '🆕 al instalar «Solo salas privadas» y «Ocultar apodos» vienen apagados')
    ok(r['malo'] and r['on'], '🔒 prenderlo pide la operación de adulto (con la mala no cambia) y queda guardado')
    ok(r['salas'] and r['privada'] and r['noCambia'] and r['pub']==False, '🚪 en Multijugador: no se ven las salas públicas y la sala que creas es privada sí o sí')
    ok(r['filas'] and 'privadas' in r['aviso'], '🎮 las filas de minijuegos con desconocidos no se abren: «Jugadores» avisa por qué (Tú solo y CPU sí)')
    ok(r['libre'], '🏗️ en el Modo libre tampoco hay salas públicas ni botón para crear una pública')

    # B) ocultar apodos
    r=await ev(r"""(async()=>{ const o={}; ui('papNames').click(); await __W(); __ADULT(true); await __W(); o.on=PAR.hideN;
      o.a=parName('Juanito','uidA'); o.b=parName('Pepe','uidB'); o.a2=parName('Juanito','uidA');
      const L=roomsFromPeers([{peer:'x', presence:{rm:'ABC123', pub:1, n:'Juanito'}}]); o.sala=L[0].names.join(',');
      ui('papNames').click(); await __W(); __ADULT(true); await __W(); o.off=parName('Juanito','uidA'); return o; })()""")
    ok(r['on'] and r['a']=='Peluche 1' and r['b']=='Peluche 2' and r['a2']=='Peluche 1', '🙈 con «Ocultar apodos» los demás se ven como «Peluche 1», «Peluche 2» (siempre el mismo número)')
    ok(r['sala']=='Peluche' and r['off']=='Juanito', '📋 tampoco se ven en la lista de salas; al apagarlo vuelven los apodos')

    # C) logros
    r=await ev(r"""(async()=>{ const o={}; lgFirst(); lgDerive(); lgBadge(); o.peces=lgVal('peces'); o.dot=ui('lgDot').hidden?'':ui('lgDot').textContent;
      o.btnMenu=!!ui('lgBtn').closest('#menuMain'); o.n=LOGROS.length; lgOpen(); await __W(); o.rows=ui('lgList').querySelectorAll('.lg-row').length;
      const b=ui('lgList').querySelector('.lg-claim[data-id="pesca"]'); o.btn=b?b.textContent:''; const c0=coins, m0=LG.s.monedas||0; b.click(); await __W();
      o.gano=coins-c0; o.noCuenta=(LG.s.monedas||0)===m0; o.med=LG.c.pesca; o.otra=!ui('lgList').querySelector('.lg-claim[data-id="pesca"]'); lgClaim('pesca'); o.doble=coins-c0;
      o.guardado=JSON.parse(localStorage.getItem('mundoPelucheLogros')).c.pesca; ui('lgOv').hidden=true; return o; })()""")
    ok(r['btnMenu'] and r['n']==25 and r['rows']==25, '🏆 el botón «Logros» está en el menú principal y muestra los 25 logros')
    ok(r['peces']==13 and r['dot']=='1', '🐟 lo que ya tenías cuenta (13 peces ya atrapados) y el botón marca 1 logro para reclamar')
    ok(r['btn']=='Reclamar +50' and r['gano']==50 and r['med']==1 and r['otra'] and r['doble']==50 and r['guardado']==1, '🥉 «Reclamar» da 50 monedas una sola vez y guarda la medalla de bronce')
    ok(r['noCuenta'], '🪙 las monedas de premio no cuentan para el logro «Ahorrador»')
    r=await ev(r"""(async()=>{ const o={}; startGame(); await __W(300); const nb=__NOTES.length; addCoins(30); o.mon=LG.s.monedas;
      LG.s.mineral=10; for(let i=0;i<6;i++) lgTick(); o.aviso=__NOTES.slice(nb).find(t=>/Minero/.test(t))||''; o.hud=ui('lgBtn').getClientRects().length===0; return o; })()""")
    ok(r['mon']==30, '➕ lo que ganas jugando sí cuenta para «Ahorrador» (+30)')
    ok('Minero' in r['aviso'] and 'menú' in r['aviso'], '🔔 al ganar una medalla jugando sale un avisito pequeño: «%s»'%r['aviso'])
    ok(r['hud'], '🎮 dentro de la partida no hay botón de Logros (solo en el menú)')

    # D) misiones del día
    r=await ev(r"""(async()=>{ const o={}; const a=qToday('2026-11-20'), a2=qToday('2026-11-20'); o.igual=JSON.stringify(a)===JSON.stringify(a2); o.tres=new Set(a.map(q=>q.k)).size===3;
      let dif=0; for(let d=1;d<=10;d++) if(JSON.stringify(qToday('2026-12-'+String(d).padStart(2,'0')))!==JSON.stringify(a)) dif++; o.dif=dif;
      const Q=qList(); LG.dd.k[Q[0].k]=Q[0].n; const nb=__NOTES.length; for(let i=0;i<6;i++) lgTick(); o.aviso=__NOTES.slice(nb).find(t=>/Misión cumplida/.test(t))||'';
      qOpen(); await __W(); o.claim=!!__OV().querySelector('.q-claim[data-i="0"]') && !__OV().querySelector('.q-claim[data-i="1"]');
      const c0=coins, mi=LG.s.mision||0; __OV().querySelector('.q-claim').click(); await __W(); o.gano=coins-c0; o.r=Q[0].r; o.mis=(LG.s.mision||0)-mi; o.ok=/Reclamada/.test(__CARD());
      qClaim(0); o.doble=coins-c0; onlineClose(); return o; })()""")
    ok(r['igual'] and r['tres'] and r['dif']>=8, '📅 las 3 misiones salen de la fecha: iguales para todos ese día, distintas y cambian de un día a otro')
    ok('Misión cumplida' in r['aviso'] and 'castillo' in r['aviso'], '⭐ al cumplir una misión avisa que la reclames en el cartel del castillo')
    ok(r['claim'] and r['gano']==r['r'] and r['ok'] and r['doble']==r['r'] and r['mis']==1, '🎁 en el cartel se reclama la cumplida (una vez) y suma al logro «Cumplidor»')
    r=await ev(r"""(()=>{ const d0=LG.s.dias||0; LG.dd.day='2000-01-01'; LG.dd.k={pez:9}; qDay(); return {nuevo:LG.dd.day===ttDay() && !LG.dd.k.pez && LG.dd.cl.every(x=>!x), dias:(LG.s.dias||0)-d0}; })()""")
    ok(r['nuevo'] and r['dias']==1, '🕛 al cambiar el día empiezan misiones nuevas desde cero (y cuenta un día jugado)')
    r=await ev(r"""(async()=>{ const o={}; o.cartel=!!QB.g && Math.hypot(QB.x,QB.z)<CAKE_ST.r0;
      player.pos.set(QB.x-Math.cos(QB.a)*1.4, QB.y+.1, QB.z-Math.sin(QB.a)*1.4); player.vel.set(0,0,0); await __W(400); scanActions(); o.cerca=(actA&&actA.label)||(PA[0]&&PA[0].label)||'';   /* v277: en pantalla táctil las acciones del lugar van en botoncitos */
      player.pos.set(0,.12,0); await __W(400); scanActions(); o.lejos=![actA,...PA].some(x=>x && /Misiones|misiones/.test(x.label)); return o; })()""")
    ok(r['cartel'] and 'Misiones' in r['cerca'] and r['lejos'], '🪧 el cartel está dentro del castillo y al acercarte sale el botón «%s»'%r['cerca'])

    # E) viaja con el código de «Mi progreso»
    r=await ev(r"""(()=>{ lgSave(); const s=saveSnapshot(); const a={...s}, b={...s, Logros:JSON.stringify({s:{mineral:99}, c:{pesca:2}, m:{}, nt:{}, fi:['x'], dd:{}})}; const M=JSON.parse(mergeSaves(a,b).Logros);
      return {en:!!s.Logros, min:M.s.mineral, med:M.c.pesca, fi:M.fi.includes('x')}; })()""")
    ok(r['en'] and r['min']==99 and r['med']==2 and r['fi'], '🔑 los logros viajan con el código de progreso (al juntar se queda lo mayor)')
    ok(not errs, '🚫 sin errores (%s)'%errs[:3]); await ctx.close()
    await b.close()
asyncio.run(m())
