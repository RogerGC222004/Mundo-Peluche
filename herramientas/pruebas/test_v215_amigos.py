# v215: Construir con amigos en el Modo libre — dos jugadores de verdad en una sala (sala simulada con BroadcastChannel):
# el mundo es del dueño, todo se ve en vivo, cada pieza recuerda quién la puso, cada quien quita solo lo suyo, pelotas
# compartidas, criaturas con su diseño, se guarda en el Modo libre del dueño, copia para el invitado, sala llena (6).
import asyncio, json, re
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
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
  window.__bye=()=>bc.postMessage({t:'x',k:me});
  bc.postMessage({t:'hello'});
  window.claude={use:n=>Promise.resolve(n==='room'?room:null)};
})();
"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); ctx=await b.new_context(viewport={"width":560,"height":320})
    await ctx.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'min', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
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
    await B.evaluate("__T.ev('MY_PID=`beto0001`; 1')")   # (en la prueba los dos comparten el almacenamiento; en dos teléfonos cada quien tiene su número)
    ev=lambda P,s: asyncio.wait_for(P.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    async def sync(n=10):
      for i in range(n):
        await ev(A,"__S(2); 1"); await A.wait_for_timeout(40); await ev(B,"__S(2); 1"); await B.wait_for_timeout(40)
    # 0. el Modo libre de Ana ya tiene cosas
    await ev(A,"localStorage.setItem('mundoPelucheLibre', JSON.stringify({v:1, s:[['b',0,0,0,0,4.5,0],['b',0,2,1,0,4.5,0],['b',3,5,-3,0,-2.5,1]], d:[['playa',3,0,3]]})); 1")
    # 1. Ana crea una sala pública; Beto la ve en la lista del Modo libre y entra
    await ev(A,"fnCreate(true); 1"); await A.wait_for_timeout(1500)
    r=await ev(A,"[FNET.on, FNET.host, FREE.on, FREE.ctx, FREE.objs.length, FREE.dyn.length, FNET.code]")
    ok(r[0] and r[1] and r[2] and r[3]=='net' and r[4]==0 and r[5]==0 and len(r[6])==6, 'Ana crea la sala: la planicie empieza vacía (su Modo libre no se carga) %s'%r)
    await ev(A,"(()=>{ for(const [x,c] of [[0,0],[1,2],[-3,5]]){ player.pos.set(FREE.X+x+.2,FREE.Y+.05,FREE.Z+2); player.facing=0; freeSelect({k:'b',a:0,b:c}); freePlace(); } player.pos.set(FREE.X+3,FREE.Y+.05,FREE.Z); freeSelect({k:'p',a:'playa',b:0}); freePlace(); freeSelect(null); return [FREE.objs.length, FREE.dyn.length]; })()")
    code=r[6]; await sync(3)
    r=await ev(B,"(async()=>{ ui('freeBtn').click(); await new Promise(r=>setTimeout(r,600)); fnRooms(); await new Promise(r=>setTimeout(r,300)); return ui('freeRooms').textContent; })()")
    ok('Sala de Ana' in r and '/6' in r and 'Unirse' in r, 'Beto ve la sala en «Construir con amigos»: %s'%r)
    await ev(B,"fnJoin(%s); 1"%json.dumps(code)); await B.wait_for_timeout(1500); await sync(14)
    r=await ev(B,"[FNET.on, FNET.host, FREE.ctx, FREE.objs.length, FREE.dyn.length, FNET.hostName, fnSynced(), FREE.objs.every(o=>o.au===FNET.hostPid), ui('freeTxt').textContent, !ui('freeCopy').hidden]")
    ok(r[0] and not r[1] and r[2]=='net' and r[3]==3 and r[4]==1 and r[5]=='Ana' and r[6] and r[7] and 'sala de Ana' in r[8] and r[9], 'Beto entra: ve lo que Ana ya puso (3 bloques y la pelota), dice «sala de Ana» y tiene 📥 Copia %s'%r)
    # 2. Beto pone un bloque y una criatura: Ana los ve, con su autor
    await ev(B,"crOpen(null); ui('crName').value='Pato'; crSet('cuerpo','caja'); crSet('c1',2); CR.open=false; crSave(); crEl.hidden=true; SW.mode=''; menuEl.hidden=true; ui('mapList').hidden=true; 1")
    r=await ev(B,"(()=>{ player.pos.set(FREE.X+6,FREE.Y+.05,FREE.Z); player.facing=0; freeSelect({k:'b',a:0,b:6}); freePlace(); player.pos.set(FREE.X+10,FREE.Y+.05,FREE.Z); freeSelect({k:'c',a:crLoad()[0].id,b:0}); freePlace(); freeSelect(null); return [FREE.objs.length, FNET.ops.length, FNET.ops[1][2].split('~')[2].length]; })()")
    await sync(10)
    r2=await ev(A,"(()=>{ const mine=FREE.objs.filter(o=>o.au!==MY_PID); return [FREE.objs.length, mine.length, mine.map(o=>o.sel.k).sort().join(''), fnName(mine[0]&&mine[0].au), !!mine.find(o=>o.sel.k==='c' && o.cr!==undefined)]; })()")
    ok(r[0]==5 and r[2]==13 and r2[0]==5 and r2[1]==2 and r2[2]=='bc' and r2[3]=='Beto', 'Beto pone un bloque y su criatura (viaja con su diseño): Ana los ve y sabe que los puso Beto %s %s'%(r,r2))
    r=await ev(B,"FREE.objs.length"); ok(r==5,'a Beto no se le duplican sus piezas (%s)'%r)
    # 3. cada quien solo quita lo suyo (también la dueña)
    r=await ev(B,"(()=>{ const o=FREE.objs.find(q=>q.au===FNET.hostPid); FREE.tgt=o; FREE.del=true; freeRemove(); return [FREE.objs.includes(o), ui('toast').textContent]; })()")
    ok(r[0] and 'Ana' in r[1], 'Beto NO puede quitar lo de Ana: «%s»'%r[1])
    r=await ev(A,"(()=>{ const o=FREE.objs.find(q=>q.au!==MY_PID); FREE.tgt=o; FREE.del=true; freeRemove(); return [FREE.objs.includes(o), ui('toast').textContent]; })()")
    ok(r[0] and 'Beto' in r[1], 'Ana (la dueña) tampoco puede quitar lo de Beto: «%s»'%r[1])
    await ev(B,"(()=>{ const o=FREE.objs.find(q=>q.au===MY_PID && q.sel.k==='b'); FREE.tgt=o; FREE.del=true; freeRemove(); FREE.del=false; return 1; })()"); await sync(10)
    r=[await ev(A,"FREE.objs.length"), await ev(B,"FREE.objs.length")]
    ok(r==[4,4], 'Beto quita su bloque y se quita para los dos %s'%r)
    # 4. la pelota es la misma para los dos: Beto la avienta con su objeto y Ana la ve moverse
    r0=await ev(A,"(()=>{ const d=FREE.dyn[0]; return [d.root.position.x, d.root.position.z]; })()")
    await ev(B,"(()=>{ const d=FREE.dyn[0]; fnKick(d,6,3,0); return 1; })()"); await sync(14)
    r1=await ev(A,"(()=>{ const d=FREE.dyn[0]; return [d.root.position.x, d.root.position.z]; })()"); rb=await ev(B,"(()=>{ const d=FREE.dyn[0]; return [d.root.position.x, d.root.position.z]; })()")
    ok(r1[0]-r0[0]>1 and abs(rb[0]-r1[0])<1.2, 'la pelota se mueve para los dos (Ana: %.1f m; Beto la ve a %.1f m de donde la ve Ana)'%(r1[0]-r0[0], abs(rb[0]-r1[0])))
    # 5. se guarda en el Modo libre de Ana (con quién lo puso); Beto se lleva una copia
    r=await ev(A,"(()=>{ freeSave(); const o=JSON.parse(localStorage.getItem('mundoPelucheLibre')); return o.s.length; })()")
    ok(r==3, 'la sala no se guarda en el Modo libre de Ana (sigue con sus 3 bloques de antes) %s'%r)
    r=await ev(A,"(()=>{ fnCopy(); const M=mapsLoad().find(m=>m.n==='Con mis amigos'); return [!!M, M&&M.s.length]; })()")
    ok(r==[True,4], 'Ana también se lleva su copia («Con mis amigos») %s'%r)
    r=await ev(B,"(()=>{ const before=localStorage.getItem('mundoPelucheLibre'); fnCopy(); const M=mapsLoad().find(m=>m.n==='Con Ana'); return [!!M && M.n, M && M.s.length, M && M.d.length, localStorage.getItem('mundoPelucheLibre')===before]; })()")
    ok(r==['Con Ana',4,1,True], 'Beto se lleva una copia a sus mapas («Con Ana») y su propio Modo libre no se toca %s'%r)
    # 6. si Ana se va, a Beto le avisa y le ofrece la copia
    await ev(A,"leaveRoom(); window.__bye(); 1"); await ev(B,"FNET.hostSeen-=20000; __S(2); 1")
    r=await ev(B,"[!!document.getElementById('fnAsk') && !document.getElementById('fnAsk').hidden, (document.getElementById('fnAskT')||{}).textContent]")
    ok(r[0] and 'Ana' in r[1], 'Ana se fue: a Beto le avisa «%s» y le ofrece la copia'%r[1])
    await ev(B,"document.getElementById('fnAskN').click(); 1")
    r=await ev(B,"[FREE.on, FNET.on, state]"); ok(r==[False,False,'menu'], 'Beto sale al menú %s'%r)
    # 7. sala llena: con 6 ya no se puede entrar
    r=await ev(B,"(async()=>{ const old=fnPeersIn; fnPeersIn=async()=>[1,2,3,4,5,6].map(i=>({presence:{fz:i===1?1:2, rm:'ABCDEF'}})); await fnJoin('ABCDEF'); fnPeersIn=old; return [ui('toast').textContent, !!mp.room]; })()")
    ok('llena' in r[0] and not r[1], 'sala llena: «%s»'%r[0])
    ok(not ea and not eb, 'sin errores %s %s'%(ea[:3],eb[:3])); await b.close()
asyncio.run(m())
