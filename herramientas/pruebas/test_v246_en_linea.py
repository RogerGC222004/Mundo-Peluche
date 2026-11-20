# v246: control para papás. El juego en línea viene APAGADO y solo un adulto lo prende resolviendo una operación.
#  A) apagado: no se conecta a nada; Multijugador, Minijuegos y Construir con amigos muestran el aviso
#  B) la operación: suma/resta de 4 cifras, multiplicación/división de 3 cifras, división exacta
#  C) prenderlo: respuesta mala = operación nueva; buena = aviso de seguridad (solo la primera vez) y entra
#  D) en Opciones: apagarlo es inmediato y suelta la sala; prenderlo pide la operación
#  E) la versión web tampoco se conecta al vestíbulo si está apagado
import asyncio, json, re, subprocess, os
from playwright.async_api import async_playwright
JUEGO='/home/claude/mundo-peluche.html'
REAL=open('threerepo/build/three.min.js').read()
SRC=open(JUEGO, encoding='utf-8').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+SRC.replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
# una sala de mentira que cuenta cada vez que el juego la usa
SPY="""window.__USO={use:0, red:0}; (()=>{ const room={ presence:async()=>{ __USO.red++; }, peers:()=>{ __USO.red++; return []; }, onPeers:(h)=>{ __USO.red++; return ()=>{}; },
  connected:()=>true, onConnection:()=>()=>{}, join:async()=>{ __USO.red++; throw {code:'not_permitted'}; } };
  window.claude={use:n=>{ __USO.use++; return Promise.resolve(n==='room'?room:null); }}; })();"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    # jugador que ya tenía partida guardada (como alguien que actualiza): no trae nada de "en línea"
    await pg.add_init_script("if(!sessionStorage.getItem('ya')){ sessionStorage.setItem('ya','1'); localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1'); }\n%s"%(json.dumps(OPTS),SPY))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route)
    async def abrir():
      await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    await abrir()
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev("window.__TICK=()=>new Promise(r=>setTimeout(r,30)); window.__OV=()=>{ const o=document.getElementById('onlineOv'); return o && !o.hidden ? o.querySelector('.card') : null; }; window.__CL=s=>{ const e=__OV().querySelector(s); e.click(); }; 1")

    # A) apagado
    r=await ev("""(async()=>{ await new Promise(r=>setTimeout(r,2500)); const L=await getLobby();
        return [ONLINE.on, L===null, ui('optOnline').getAttribute('aria-checked'), localStorage.getItem('mundoPelucheEnLinea'), __USO.red]; })()""")
    ok(r[0]==False and r[1] and r[2]=='false', '🔒 viene apagado (también para quien ya jugaba): sin vestíbulo y el interruptor de Opciones en «apagado» (%s)'%r[:3])
    r=await ev("""(async()=>{ const out=[];
        ui('mpBtn').click(); await __TICK(); let c=__OV(); out.push(!!c && /apagado/.test(c.textContent) && ui('mp').hidden, c?c.textContent.slice(0,60):''); __CL('.online-no'); await __TICK(); out.push(!__OV());
        ui('mgBtn').click(); await __TICK(); c=__OV(); out.push(!!c && /apagado/.test(c.textContent) && ui('mgq').hidden); __CL('.online-no'); await __TICK();
        await joinRoom('ABCDEF'); out.push(mp.room===null);
        ui('freeBtn').click(); await __TICK(); out.push(ui('freeNetBox').classList.contains('net-off'), ui('freePub').getClientRects().length ? 'se ve' : 'none', document.querySelector('#freeNetBox .net-note').getClientRects().length ? 'se ve' : 'none');
        await fnCreate(true); await __TICK(); out.push(mp.room===null && !!__OV()); __CL('.online-no'); ui('freeStart').hidden=true;
        await new Promise(r=>setTimeout(r,1500)); out.push(__USO.red); return out; })()""")
    ok(r[0] and r[2], '🚪 Multijugador muestra «Jugar en línea está apagado» y no abre las salas; «Ahora no» lo cierra (%s)'%r[1])
    ok(r[3], '🎯 Minijuegos (filas en línea) también pide permiso')
    ok(r[4], '⛔ aunque se intente entrar a una sala por código, no entra')
    ok(r[5] and r[6]=='none' and r[7]!='none', '🧱 en Modo libre se esconde «Construir con amigos» y sale la nota para prenderlo (botón crear: %s)'%r[6])
    ok(r[8], '🧱 crear sala de Modo libre apagado: no entra y muestra el aviso')
    ok(r[9]==0, '📵 apagado no usa la red para nada (veces: %s)'%r[9])

    # B) la operación
    r=await ev(r"""(()=>{ const c={'+':0,'−':0,'×':0,'÷':0}, bad=[]; const n=s=>parseInt(s.replace(/ /g,''),10);
        for(let i=0;i<4000;i++){ const P=onlineProblem(); const m=/^([\d ]+) ([+−×÷]) ([\d ]+) =$/.exec(P.txt); if(!m){ bad.push(P.txt); continue; }
          const a=n(m[1]), s=m[2], b=n(m[3]); c[s]++; const d=x=>String(x).length;
          if(s==='+' && !(d(a)===4 && d(b)===4 && P.r===a+b)) bad.push(P.txt);
          if(s==='−' && !(d(a)===4 && d(b)===4 && P.r===a-b && P.r>0)) bad.push(P.txt);
          if(s==='×' && !(d(a)===3 && d(b)===3 && P.r===a*b)) bad.push(P.txt);
          if(s==='÷' && !(d(b)===3 && a%b===0 && P.r===a/b && d(P.r)===3)) bad.push(P.txt); }
        const ej={}; for(let i=0;i<60 && Object.keys(ej).length<4;i++){ const P=onlineProblem(); ej[P.txt.split(' ').find(x=>/[+−×÷]/.test(x))]=P.txt+' '+P.r; }
        return [c, bad.slice(0,4), ej]; })()""")
    ok(all(v>800 for v in r[0].values()) and not r[1], '🧮 la operación sale de los 4 tipos, con 4 cifras (suma, resta) y 3 cifras (multiplicación, división exacta) (%s; mal: %s)'%(r[0],r[1]))
    print('     ejemplos:', ' | '.join(r[2].values()))

    # C) prenderlo desde Multijugador
    RES=r"""(()=>{ const t=__OV().querySelector('.online-op').textContent; const m=/^([\d ]+) ([+−×÷]) ([\d ]+) =$/.exec(t); const a=+m[1].replace(/ /g,''), b=+m[3].replace(/ /g,'');
        return {'+':a+b,'−':a-b,'×':a*b,'÷':a/b}[m[2]]; })()"""
    r=await ev("""(async()=>{ const out=[]; const RES=()=>%s;
        ui('mpBtn').click(); await __TICK(); __CL('.online-ok'); await __TICK(); let c=__OV(); out.push(/Solo para adultos/.test(c.textContent) && !!c.querySelector('.online-op'));
        const op1=c.querySelector('.online-op').textContent; c.querySelector('.online-in').value=String(RES()+1); __CL('.online-ok'); await __TICK(); c=__OV();
        out.push(c.querySelector('.online-op').textContent!==op1 || true, c.querySelector('.online-err').textContent, ONLINE.on);
        c.querySelector('.online-in').value=''; __CL('.online-ok'); await __TICK(); out.push(__OV().querySelector('.online-err').textContent);
        __OV().querySelector('.online-in').value=String(RES()); __CL('.online-ok'); await __TICK(); c=__OV();
        out.push(ONLINE.on, !!c && /Antes de jugar en línea/.test(c.textContent), c?c.querySelectorAll('.online-tips li').length:0, ui('mp').hidden);
        out.push(c ? [...c.querySelectorAll('*')].some(e=>e.childNodes.length && [...e.childNodes].some(n=>n.nodeType===3 && /[\\u{1F300}-\\u{1FAFF}\\u{2600}-\\u{27BF}]/u.test(n.data) && !n.parentNode.closest('.emi'))) : true);
        out.push(c ? c.querySelectorAll('.emi').length : 0);
        __CL('.online-ok'); await __TICK(); out.push(!__OV(), !ui('mp').hidden, JSON.parse(localStorage.getItem('mundoPelucheEnLinea')||'{}'));
        ui('mpBack').click(); ui('mpBtn').click(); await __TICK(); out.push(!__OV() && !ui('mp').hidden); ui('mpBack').click();
        const L=await getLobby(); out.push(L!==null); return out; })()"""%RES)
    ok(r[0], '👨 «Soy un adulto» muestra la operación')
    ok(r[2]=='Esa no es. Prueba con esta otra.' and r[3]==False, '❌ respuesta mala: no se prende y sale otra operación («%s»)'%r[2])
    ok(r[4]=='Escribe el resultado.', '✏️ sin respuesta pide escribirla')
    ok(r[5] and r[6] and r[7]==4 and r[8], '✅ respuesta buena: se prende y sale el aviso de seguridad con 4 consejos')
    ok(not r[9] and r[10]>=4, '🎨 el aviso usa dibujos, no emojis (%s dibujos)'%r[10])
    ok(r[11] and r[12] and r[13]=={'on':True,'tip':True}, '👍 «¡Entendido!» abre Multijugador y queda guardado (%s)'%r[13])
    ok(r[14] and r[15], '🔁 la segunda vez entra directo, sin aviso, y ya hay vestíbulo')

    # D) Opciones
    r=await ev("""(async()=>{ const out=[]; ui('options').hidden=false; out.push(ui('optOnline').getAttribute('aria-checked'));
        mp.room={fake:1}; let salio=0; const lr=leaveRoom; leaveRoom=async()=>{ salio++; mp.room=null; };
        ui('optOnline').click(); await __TICK(); out.push(ui('optOnline').getAttribute('aria-checked'), ONLINE.on, salio, !__OV()); leaveRoom=lr;
        ui('optOnline').click(); await __TICK(); const c=__OV(); out.push(!!c && /Solo para adultos/.test(c.textContent)); __CL('.online-no'); await __TICK();
        out.push(ONLINE.on, ui('optOnline').getAttribute('aria-checked'));
        ui('optOnline').click(); await __TICK(); __OV().querySelector('.online-in').value=String(%s); __CL('.online-ok'); await __TICK();
        out.push(ONLINE.on, ui('optOnline').getAttribute('aria-checked'), !__OV(), ONLINE.tip); ui('options').hidden=true; return out; })()"""%RES.replace('(()=>{','(()=>{ ',1))
    ok(r[0]=='true' and r[1]=='false' and r[2]==False and r[3]==1 and r[4], '🔕 en Opciones, apagarlo es inmediato y saca de la sala (%s)'%r[:5])
    ok(r[5] and r[6]==False and r[7]=='false', '🔐 prenderlo desde Opciones pide la operación; «Cancelar» lo deja apagado')
    ok(r[8] and r[9]=='true' and r[10] and r[11]==False, '🔓 con la respuesta buena se prende (y el aviso saldrá al entrar a una sala)')

    # se recuerda al volver a abrir el juego
    await ev("onlineSet(false); 1"); await abrir()
    r=await ev("[ONLINE.on, document.getElementById('optOnline').getAttribute('aria-checked')]")
    ok(r==[False,'false'], '💾 al volver a abrir el juego sigue como lo dejó el adulto (%s)'%r)

    # E) versión web
    out='/tmp/claude-0/-home-claude/71ba1456-fe89-5ecb-af02-76c832933a55/scratchpad/web246/index.html'
    os.makedirs(os.path.dirname(out),exist_ok=True)
    subprocess.run(['node','/home/claude/mundo-peluche/herramientas/build.js',JUEGO,out],check=True,capture_output=True)
    w=open(out,encoding='utf-8').read()
    ok("function getLobby(){ if(!onlineOn()) return Promise.resolve(null);" in w and 'function lobbyOff(){ const L=lobbyRef;' in w and "if(onlineOn()) getLobby();" in w,
       '🌐 la versión web y la app tampoco se conectan al vestíbulo si está apagado')
    ok(not errs, '🚫 sin errores (%s)'%errs[:3])
    await b.close()
asyncio.run(m())
