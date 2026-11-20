# v229: salas del Modo libre — (1) al crear la sala se avisa en el vestíbulo que es de Modo libre (en la web ese aviso estaba
# tapado por un comentario y nadie podía entrar: «Esa sala no es de Modo libre»); (2) la burbuja va en «fw» (chocaba con «fb»,
# la lista de bloques del dueño); (3) si arriba no cabe la barra (medidor, coordenadas…) baja a su propio renglón y se ve completa;
# (4) el letrero de la sala ya no sale encima de los Ajustes ni de la pausa.
import asyncio, json, re, os, subprocess, tempfile
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
SRC=open('/home/claude/mundo-peluche.html').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+SRC.replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
BUS = """
(()=>{
  const me='p'+Math.random().toString(36).slice(2,8), bc=new BroadcastChannel('vestibulo'); const peers=new Map(); const hs=new Set();
  let mine={};
  const snap=()=>[...peers.entries()].map(([k,pr])=>({peer:k, sameTab:k===me, kind:'viewer', presence:pr}));
  const emitAll=()=>{ const ps=snap(); hs.forEach(h=>h({peers:ps})); };
  bc.onmessage=e=>{ const d=e.data; if(d.t==='p'){ peers.set(d.k,d.pr); emitAll(); } if(d.t==='x'){ peers.delete(d.k); emitAll(); } if(d.t==='hello'){ bc.postMessage({t:'p',k:me,pr:mine}); } };
  peers.set(me,mine);
  const room={ presence:async(patch)=>{ mine={...mine}; for(const k in patch){ if(patch[k]===null) delete mine[k]; else mine[k]=patch[k]; } peers.set(me,mine); bc.postMessage({t:'p',k:me,pr:JSON.parse(JSON.stringify(mine))}); emitAll(); },
    peers:()=>snap(), onPeers:(h)=>{ hs.add(h); setTimeout(()=>h({peers:snap()})); return ()=>hs.delete(h); },
    connected:()=>true, onConnection:(h)=>{ setTimeout(()=>h(true)); return ()=>{}; } };
  bc.postMessage({t:'hello'});
  window.claude={use:n=>Promise.resolve(n==='room'?room:null)};
})();
"""
ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
# 0. en la versión web, el aviso al vestíbulo (con fz=1) ya no está dentro de un comentario
line=[l for l in SRC.split('\n') if 'async function fnCreate' in l or ('fnHostInit();' in l and 'FNET.host=true' in l)]
L=[l for l in line if 'fnHostInit();' in l][0]; cpos=L.find('//')
ok('lobbyAnnounce()' in L and (cpos<0 or L.find('lobbyAnnounce()')<cpos) and 'sendPresence(true)' in L[:cpos if cpos>=0 else None], 'al crear la sala se avisa a todos que es de Modo libre (el aviso ya no queda dentro de un comentario)')
d=tempfile.mkdtemp(); subprocess.run(['node','/home/claude/mundo-peluche/herramientas/build.js','/home/claude/mundo-peluche.html',os.path.join(d,'index.html')],check=True,capture_output=True)
W=open(os.path.join(d,'index.html')).read(); m=re.search(r"function lobbyAnnounce\(\)\{[^\n]*fz:\(typeof FNET!=='undefined'&&FNET\.on&&FNET\.host\)\?1:null",W)
L2=[l for l in W.split('\n') if 'fnHostInit();' in l and 'FNET.host=true' in l][0]; c2=L2.find('//')
ok(bool(m) and L2.find('lobbyAnnounce()')>0 and (c2<0 or L2.find('lobbyAnnounce()')<c2), 'versión web: el vestíbulo anuncia fz=1 y fnCreate sí lo llama')
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); ctx=await b.new_context(viewport={"width":820,"height":360}, has_touch=True)
    await ctx.add_init_script("localStorage.setItem('mundoPelucheEnLinea','{\"on\":true,\"tip\":true}'); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1'); localStorage.setItem('mundoPelucheFreeIco','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await ctx.route("https://**/*", route)
    async def open_game(name):
      pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); await pg.add_init_script(BUS)
      await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
      await pg.evaluate("n=>__T.ev(`profile.name=${JSON.stringify(n)}; window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateRemotes(.05,t); } FNET.bT=0; sendPresence(true); }; 1`)", name)
      return pg, errs
    A,ea=await open_game('Ana'); B,eb=await open_game('Beto')
    await B.evaluate("__T.ev('MY_PID=`beto0001`; 1')")
    ev=lambda P,s: asyncio.wait_for(P.evaluate("s=>__T.ev(s)", s), 300)
    async def sync(n=10):
      for i in range(n):
        await ev(A,"__S(2); 1"); await A.wait_for_timeout(40); await ev(B,"__S(2); 1"); await B.wait_for_timeout(40)
    # 1. Ana crea la sala: el aviso al vestíbulo sale ya como sala de Modo libre; Beto entra con el código
    await ev(A,"window.__LA=[]; { const o=lobbyAnnounce; lobbyAnnounce=function(){ __LA.push([FNET.on,FNET.host]); return o.apply(this,arguments); }; } fnCreate(false); 1"); await A.wait_for_timeout(1500)
    r=await ev(A,"[__LA, FNET.on, FNET.host, FNET.code]"); code=r[3]
    ok([True,True] in r[0], 'Ana crea una sala privada y avisa en el vestíbulo ya como dueña de Modo libre %s'%r[0])
    await sync(3)
    await ev(B,"window.__N=[]; { const o=flashNote; flashNote=function(t){ __N.push(String(t)); return o.apply(this,arguments); }; } fnJoin(%s); 1"%json.dumps(code)); await B.wait_for_timeout(1500); await sync(10)
    r=await ev(B,"[FNET.on, FNET.host, FREE.ctx, FNET.hostName, __N.filter(t=>/no es de Modo libre/.test(t)).length]")
    ok(r[0] and not r[1] and r[2]=='net' and r[3]=='Ana' and r[4]==0, 'Beto entra con el código a la sala de Ana (sin «no es de Modo libre») %s'%r)
    # 2. la burbuja de Ana se ve desde Beto y la lista de bloques de Ana sigue llegando
    r=await ev(A,"(()=>{ const o=freeAddStatic({k:'p',a:'burbujas',b:0},FREE.X+6,FREE.Y,FREE.Z+6,0); o.sel.b=3; __S(100); const g=BUB.L.find(b=>b.giant); if(!g) return [false]; const q=g.m.position; player.pos.set(q.x,q.y-1.1,q.z); __S(1); const P=fnPresence(); return [!!FREE.ride, P.fw, Array.isArray(P.fb)]; })()")
    ok(r[0] and r[1]>0 and r[2], 'la burbuja del dueño va en «fw» y su lista de bloques sigue en «fb» %s'%r)
    await sync(4)
    r=await ev(B,"(()=>{ const R=[...mp.remotes.values()].find(x=>x.fz===1); return [R && R.fw, !!(R && R._bub && R._bub.visible)]; })()")
    ok(r[0] and r[0]>0 and r[1], 'Beto ve a Ana adentro de su burbuja %s'%r)
    await ev(A,"freeBubbleExit(false); 1")
    # 3. la barra del Modo libre siempre completa: con medidor y coordenadas baja a su renglón; sin ellos, arriba
    async def bar(P,fps,coords):
      return await ev(P,"""(async()=>{ settings.fps=%s; settings.coords=%s; applySettings(); ui('fps').textContent='58 FPS · lógica 3 · dibujo 6 ms\\n29 dib · 41k ▲ · peor 70 ms (dibujo) hace 9 s'; ui('coordsEl').textContent='X 8969 · Y 1 · Z 5\\nMar abierto · v229'; ui('freeLegend').hidden=true; freeRenderHud(); await new Promise(r=>setTimeout(r,120)); freeHudFit(); await new Promise(r=>setTimeout(r,60));
        const H=ui('freeHud'), r=H.getBoundingClientRect(), T=ui('freeTxt').getBoundingClientRect(), row=ui('hud').firstElementChild.getBoundingClientRect(), cam=ui('camChip').getBoundingClientRect();
        const icons=[...H.querySelectorAll('button')].filter(b=>!b.hidden && b.offsetParent); const vis=icons.filter(b=>{ const q=b.getBoundingClientRect(); return q.left>=r.left-1 && q.right<=r.right+1 && q.right<=innerWidth; }).length;
        return [document.body.classList.contains('free-2row'), H.scrollWidth<=H.clientWidth+1 && cam.right<=innerWidth+1, vis, icons.length, Math.round(r.top), Math.round(r.bottom), Math.round(T.top), Math.round(row.bottom), r.right<=cam.left+1 || r.top>=cam.bottom-1, ui('freeTxt').textContent.slice(0,22)]; })()"""%('true' if fps else 'false','true' if coords else 'false'))
    r=await bar(A,True,True)
    ok(r[0] and r[1] and r[2]==r[3] and r[4]>=r[7] and r[6]>=r[5] and r[8], 'con medidor y coordenadas la barra baja a su renglón y se ven sus %s botones; el letrero de la sala va abajo de ella %s'%(r[3],r))
    r=await bar(A,True,False)
    ok(r[1] and r[2]==r[3] and r[8], 'solo con el medidor también se ve completa %s'%r)
    r=await bar(A,False,False)
    ok(not r[0] and r[1] and r[2]==r[3], 'sin medidor ni coordenadas se queda arriba, completa %s'%r)
    # 4. el letrero de la sala no sale encima de la pausa ni de los Ajustes
    r=await ev(A,"""(async()=>{ settings.fps=true; settings.coords=true; applySettings(); show('pause'); await new Promise(r=>setTimeout(r,60)); const a=getComputedStyle(ui('freeTxt')).display; show('play'); await new Promise(r=>setTimeout(r,60)); const b=getComputedStyle(ui('freeTxt')).display; return [a,b]; })()""")
    ok(r[0]=='none' and r[1]=='block', 'el letrero de la sala se esconde en la pausa y los Ajustes, y vuelve al jugar %s'%r)
    # 5. al salir del Modo libre no queda nada movido
    r=await ev(A,"(()=>{ freeExit(); return [document.body.classList.contains('free-2row'), ui('freeHud').style.top, ui('freeTxt').style.top]; })()")
    ok(not r[0] and r[1]=='' and r[2]=='', 'al salir del Modo libre la barra vuelve a la normalidad %s'%r)
    ok(not ea and not eb, 'sin errores %s %s'%(ea[:2],eb[:2])); await b.close()
asyncio.run(m())
