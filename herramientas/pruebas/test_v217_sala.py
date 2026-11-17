# v217 en una sala de «Construir con amigos»: los juegos que se mueven van a la misma hora para los dos, si Beto se
# sube al columpio Ana lo ve sentado y columpiándose, los dominós que Beto empuja se caen para los dos (y quedan igual),
# la torre se derrumba para los dos y «Volver a pararlos» de Beto los para para todos.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
BUS=open('/home/claude/mundo-peluche/herramientas/pruebas/test_v215_amigos.py').read().split('BUS = """',1)[1].split('"""',1)[0]
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
      await pg.evaluate("n=>__T.ev(`profile.name=${JSON.stringify(n)}; window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateRemotes(.05,t); } scene.updateMatrixWorld(); FNET.bT=0; sendPresence(true); }; window.__do=(lab)=>{ const a=freeActions()||[]; const x=a.find(q=>q&&q.label===lab); if(x) x.run(); return !!x; }; 1`)", name)
      return pg, errs
    A,ea=await open_game('Ana'); B,eb=await open_game('Beto')
    # (los relojes de las dos páginas no empiezan igual: Beto va 37 s adelantado)
    await B.evaluate("__T.ev('MY_PID=`beto0001`; clock.elapsedTime+=37; 1')")
    ev=lambda P,s: asyncio.wait_for(P.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    async def sync(n=10):
      for i in range(n):
        await ev(A,"__S(2); 1"); await A.wait_for_timeout(40); await ev(B,"__S(2); 1"); await B.wait_for_timeout(40)
    # 1. Ana pone juegos y juguetes en su sala
    await ev(A,"fnCreate(true); 1"); await A.wait_for_timeout(1500)
    r=await ev(A,"""(()=>{ const X=FREE.X,Y=FREE.Y,Z=FREE.Z; const put=(sel,x,z,f)=>{ player.pos.set(X+x,Y+.05,Z+z); player.facing=f||0; freeSelect(sel); freePlace(); freeSelect(null); };
      put({k:'v',a:'columpio',b:5},-10,-10); put({k:'v',a:'carrusel',b:0},0,-10); put({k:'v',a:'elevador',b:7},10,-10); put({k:'t',a:'fila',b:11},-10,6); put({k:'t',a:'torre',b:0},6,6);
      player.pos.set(X,Y+.05,Z+20); return [FREE.pqv.length, FREE.toys.length]; })()""")
    code=await ev(A,"FNET.code"); await ev(B,"(async()=>{ ui('freeBtn').click(); await new Promise(r=>setTimeout(r,600)); return 1; })()")
    await ev(B,"fnJoin(%s); 1"%json.dumps(code)); await B.wait_for_timeout(1500)
    for i in range(30):
      await sync(1)
      if await ev(B,"fnSynced() && (FREE.toys||[]).length===9 && (FREE.pqv||[]).length===3"): break
    await ev(B,"player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+20); 1"); await sync(3)
    r=await ev(B,"[(FREE.pqv||[]).length, (FREE.toys||[]).length, fnSynced()]")
    ok(r==[3,9,True], 'Beto entra y ve los 3 juegos y los 9 juguetes de Ana %s'%r)
    # 2. la misma hora: el elevador y el carrusel van igual para los dos
    rA=await ev(A,"(()=>{ const e=FREE.pqv.find(q=>q.pq==='elevador'), c=FREE.pqv.find(q=>q.pq==='carrusel'); return [pqElevY(e,pqClock()), c.root.userData.pq.mov.rotation.y%(Math.PI*2), clock.elapsedTime]; })()")
    rB=await ev(B,"(()=>{ const e=FREE.pqv.find(q=>q.pq==='elevador'), c=FREE.pqv.find(q=>q.pq==='carrusel'); return [pqElevY(e,pqClock()), c.root.userData.pq.mov.rotation.y%(Math.PI*2), clock.elapsedTime]; })()")
    da=abs(((rA[1]-rB[1]+3.1416)%6.2832)-3.1416)
    ok(abs(rA[0]-rB[0])<.6 and da<.4, 'el elevador y el carrusel van igual para los dos aunque sus relojes no (elevador %.2f/%.2f m, carrusel %.2f rad de diferencia)'%(rA[0],rB[0],da))
    # 3. Beto se sube al columpio: Ana lo ve sentado ahí y el columpio se mueve también para ella
    r=await ev(B,"""(()=>{ const o=FREE.pqv.find(q=>q.pq==='columpio'), a=o.r*Math.PI/2; player.pos.set(o.x+Math.sin(a)*.6,FREE.Y+.05,o.z+Math.cos(a)*.6); player.vel.set(0,0,0); __S(2); const ok=__do('Columpiarse'); return [ok, player.pg&&player.pg.k, fnPresence().fm===o.nid]; })()""")
    await sync(14)
    r2=await ev(A,"""(()=>{ const o=FREE.pqv.find(q=>q.pq==='columpio'); const rr=[...mp.remotes.values()][0]; const occ=pqAnyOcc(o); return [occ, +o.ride.amp.toFixed(2), rr && rr.pl && PG_KINDS[rr.pl[0]], rr && +Math.hypot(rr.pos.x-o.x,rr.pos.z-o.z).toFixed(2), rr && +(rr.pos.y-FREE.Y).toFixed(2)]; })()""")
    ok(r[0] and r[1]=='fmv' and r[2] and r2[0] and r2[1]>.2 and r2[2]=='fmv' and r2[3]<1.5 and r2[4]<1.5, 'Beto se columpia: Ana lo ve sentado en el columpio y el columpio se mueve también para ella %s %s'%(r,r2))
    await ev(B,"(()=>{ __do('Bajarse'); player.pos.set(FREE.X,FREE.Y+.05,FREE.Z+20); return 1; })()"); await sync(3)
    # 4. Beto empuja el primer dominó: se caen para los dos y quedan igual
    r=await ev(B,"""(()=>{ const D=FREE.toys.filter(o=>o.pq==='domino').sort((a,b)=>a.x-b.x||a.z-b.z); const f=D[0], a=f.r*Math.PI/2, ax=Math.sin(a), az=Math.cos(a);
      const end=D.reduce((m,o)=>((o.x-f.x)*ax+(o.z-f.z)*az)<((m.x-f.x)*ax+(m.z-f.z)*az)?o:m,f); player.pos.set(end.x-ax*1.3,FREE.Y+.05,end.z-az*1.3); player.facing=Math.atan2(ax,az); player.vel.set(0,0,0); __S(1); return __do('Empujar'); })()""")
    await sync(30)
    rA=await ev(A,"FREE.toys.filter(o=>o.pq==='domino').map(o=>o.toy.st+':'+Math.round(o.toy.th*100))")
    rB=await ev(B,"FREE.toys.filter(o=>o.pq==='domino').map(o=>o.toy.st+':'+Math.round(o.toy.th*100))")
    ok(r and all(x.startswith('2:') for x in rA) and sorted(rA)==sorted(rB), 'Beto empuja un dominó: se caen los 8 para los dos y quedan igual %s %s'%(rA,rB))
    # 5. Ana tira la torre: se derrumba también para Beto
    await ev(A,"(()=>{ const o=FREE.toys.find(q=>q.pq==='torre'); pqKnock(o,1,0,4,.8); return 1; })()"); await sync(12)
    r=await ev(B,"(()=>{ const o=FREE.toys.find(q=>q.pq==='torre'); const U=o.root.userData.pq; return [o.toy.st, U.blocks.filter(b=>b.loose).length, +Math.max(...U.blocks.filter(b=>b.loose).map(b=>b.m.position.x-o.x)).toFixed(1)]; })()")
    ra=await ev(A,"(()=>{ const o=FREE.toys.find(q=>q.pq==='torre'); return o.root.userData.pq.blocks.filter(b=>b.loose).length; })()")
    ok(r[0]>=1 and r[1]==ra and r[1]>=8 and r[2]>.5, 'Ana tira la torre y Beto la ve derrumbarse para el mismo lado (%s bloques) %s'%(r[1],r))
    # 6. Beto: «Volver a pararlos» → parados para todos
    await ev(B,"(()=>{ const T=FREE.toys; const cx=T.reduce((s,o)=>s+o.x,0)/T.length, cz=T.reduce((s,o)=>s+o.z,0)/T.length; player.pos.set(cx,FREE.Y+.05,cz-2); __S(1); return __do('Volver a pararlos'); })()"); await sync(14)
    r=[await ev(P,"FREE.toys.filter(o=>o.toy.st).length") for P in (A,B)]
    if r!=[0,0]: print('DBG', await ev(B,"FREE.toys.filter(o=>o.toy.st).map(o=>[o.pq,o.toy.st,o.nid,o.bk,!!o.toy.net,FNET.gh[o.bk]])"), await ev(A,"FREE.toys.filter(o=>o.pq==='torre').map(o=>[o.nid,o.bk,FNET.bk[o.bk].h,FNET.bk[o.bk].s.split(',').filter(e=>e.startsWith(o.nid))])"))
    ok(r==[0,0], 'Beto toca «Volver a pararlos» y quedan parados para los dos %s'%r)
    rp=await ev(A,"mp.presBytes"); ok(rp<=3500, 'lo que manda Ana pesa %s bytes'%rp)
    ok(not ea and not eb,'sin errores %s %s'%(ea[:3],eb[:3])); await b.close()
asyncio.run(m())
