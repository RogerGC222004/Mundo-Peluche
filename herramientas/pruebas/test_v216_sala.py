# v216 en una sala de «Construir con amigos»: límite 500 piezas y 50 con física, el mundo llega completo por partes
# (también las pelotas), 🎨 pintar (cada quien lo suyo), 🌤️ el lugar lo escoge el dueño y lo ven todos, y la presencia
# no pasa del límite aunque la sala esté llena.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; FREE.legacyAim=true; function frame(){",1)
BUS=open('/home/claude/mundo-peluche/herramientas/pruebas/test_v215_amigos.py').read().split('BUS = """',1)[1].split('"""',1)[0]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); ctx=await b.new_context(viewport={"width":560,"height":320})
    await ctx.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'min', qDef:1, hints:false, weather:true})); localStorage.setItem('mundoPelucheEcon124','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await ctx.route("https://**/*", route)
    async def open_game(name):
      pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); await pg.add_init_script(BUS)
      await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
      await pg.evaluate("n=>__T.ev(`profile.name=${JSON.stringify(n)}; window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateRemotes(.05,t); updateSky(.05); } FNET.bT=0; sendPresence(true); }; 1`)", name)
      return pg, errs
    A,ea=await open_game('Ana'); B,eb=await open_game('Beto')
    await B.evaluate("__T.ev('MY_PID=`beto0001`; 1')")
    ev=lambda P,s: asyncio.wait_for(P.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    async def sync(n=10):
      for i in range(n):
        await ev(A,"__S(2); 1"); await A.wait_for_timeout(40); await ev(B,"__S(2); 1"); await B.wait_for_timeout(40)
    # 1. Ana crea la sala y la llena: 495 bloques y 50 pelotas; ya no caben más de 500 y 50
    await ev(A,"fnCreate(true); 1"); await A.wait_for_timeout(1500)
    r=await ev(A,"""(()=>{ const X=FREE.X,Y=FREE.Y,Z=FREE.Z; let n=0, nd=0;
      for(let i=0;i<505;i++){ const o=freeAddStatic({k:'b',a:i%4,b:i%12},X-40+(i%30)*2+.5,Y,Z-40+Math.floor(i/30)*2+.5,i%4,true); if(o){ fnLocalAdd(o); n++; } if(n>=495) break; }
      for(let i=0;i<55;i++){ const o=freeAddDyn(['playa','goma','caja','barril'][i%4],X-36+(i%10)*6,Y+.3,Z+20+Math.floor(i/10)*5,true); if(o){ fnLocalAdd(o); nd++; } }
      const extra=[]; for(let i=0;i<8;i++){ const o=freeAddStatic({k:'b',a:0,b:0},X+30+i*2+.5,Y,Z+30.5,0,true); if(o){ fnLocalAdd(o); extra.push(o); } }
      return [FREE_MAX, FREE_DYN, n, nd, extra.length, freeOwn()]; })()""")
    ok(r==[500,50,495,50,5,500], 'en la sala el límite es 500 piezas y 50 con física (Ana llena la sala) %s'%r)
    await ev(A,"(()=>{ const L=FREE.objs.filter(o=>o.x>FREE.X+29); L.forEach(o=>{ FREE.tgt=o; FREE.del=true; freeRemove(); }); FREE.del=false; return 1; })()")
    # el lugar: nieve, atardecer, nevando
    r=await ev(A,"""(()=>{ freeEnvOpen(); const rows=document.querySelectorAll('#freeEnv .env-row'); [...rows[0].children].find(b=>b.textContent.includes('Nieve')).click(); [...rows[1].children].find(b=>b.textContent.includes('Atardecer')).click(); [...rows[2].children].find(b=>b.textContent.includes('Nieve')).click(); document.querySelector('#freeEnvOk').click(); return JSON.stringify(FREE.env); })()""")
    # 2. Beto entra: le llega todo (por partes) y ve el mismo lugar
    await ev(B,"(async()=>{ ui('freeBtn').click(); await new Promise(r=>setTimeout(r,600)); return 1; })()")
    code=await ev(A,"FNET.code"); await ev(B,"fnJoin(%s); 1"%json.dumps(code)); await B.wait_for_timeout(1500)
    n=0
    for i in range(40):
      await sync(1); n+=1
      if await ev(B,"fnSynced() && FREE.objs.length===495 && FREE.dyn.length===50"): break
    r=await ev(B,"[FREE_MAX, FREE_DYN, FREE.objs.length, FREE.dyn.length, fnSynced(), JSON.stringify(FREE.env), FREE.floor.material[2].map===FREE_FLOOR.nieve, weatherNow.id, ui('freeTxt').textContent]")
    ok(r[0]==500 and r[1]==50 and r[2]==495 and r[3]==50 and r[4] and '"piso":"nieve"' in r[5] and r[6] and r[7]=='snow', 'Beto entra y le llega toda la sala en %s envíos (~%.1f s): 495 piezas, 50 pelotas, piso de nieve y nevando %s'%(n, n*.2, r))
    r=await ev(B,"(()=>{ freeEnvOpen(); const el=document.getElementById('freeEnv'), bs=[...el.querySelectorAll('.env-row button')]; const res=[bs.every(b=>b.disabled), el.querySelector('#freeEnvNote').textContent]; el.querySelector('#freeEnvOk').click(); return res; })()")
    ok(r[0] and 'Ana' in r[1], 'Beto no puede cambiar el lugar: «%s»'%r[1])
    # 3. la presencia no se pasa del límite aunque todo se mueva
    r=await ev(A,"(()=>{ FREE.dyn.forEach((d,i)=>{ freeWake(d); d.v.set(Math.sin(i)*3,2,Math.cos(i)*3); }); __S(1); const P=JSON.parse(mp.lastPayload); return [mp.presBytes, (P.fb||[]).length, JSON.stringify(P.fb||[]).length, (P.fd||[]).length, !!P.ou]; })()")
    ok(r[0]<=3500 and r[1]>=1 and r[3]>=30 and r[4], 'con la sala llena y 50 pelotas volando, lo que manda Ana pesa %s bytes (límite 3500): %s partes del mundo, %s pelotas, y su ropa sigue %s'%(r[0],r[1],r[3],r))
    rB=await ev(B,"mp.presBytes"); ok(rB<=3500, 'lo que manda Beto pesa %s bytes'%rB)
    await sync(12)
    # 4. 🎨 pintar en la sala: Beto pinta lo suyo (Ana lo ve); lo de Ana no; Ana pinta lo suyo (Beto lo ve)
    await ev(A,"(()=>{ const L=FREE.objs.filter(o=>o.x<FREE.X-30).slice(0,6); L.forEach(o=>{ FREE.tgt=o; FREE.del=true; freeRemove(); }); FREE.del=false; return 1; })()"); await sync(8)
    r=await ev(B,"""(()=>{ player.pos.set(FREE.X+33,FREE.Y+.05,FREE.Z+30); player.facing=0; freeSelect({k:'b',a:0,b:0}); freePlace(); freeSelect(null); const o=FREE.objs.find(q=>q.au===MY_PID);
      freePaintSet(true); FREE.pcol=7; FREE.tgt=o; freePaintDo(); const mine=o.sel.b; const theirs=FREE.objs.find(q=>q.au!==MY_PID), b0=theirs.sel.b; FREE.tgt=theirs; freePaintDo(); const msg=ui('toast').textContent; freePaintSet(false);
      window.__mine=o.nid; window.__theirs=theirs.nid; return [mine, theirs.sel.b===b0, msg, FNET.ops.map(x=>x[1]).join('')]; })()""")
    await sync(10)
    r2=await ev(A,"(()=>{ const o=FREE.objs.find(q=>q.au!==MY_PID); return [o&&o.sel.b, FREE.objs.length]; })()")
    ok(r[0]==7 and r[1] and 'solo Ana la puede pintar' in r[2] and r[3]=='ac' and r2[0]==7, 'Beto pinta su bloque (Ana lo ve de ese color) y no puede pintar lo de Ana: «%s» %s %s'%(r[2],r,r2))
    theirs=await ev(B,"window.__theirs")
    await ev(A,"(()=>{ const o=FREE.objs.find(q=>q.nid===%s); freePaintSet(true); FREE.pcol=3; FREE.tgt=o; freePaintDo(); freePaintSet(false); return 1; })()"%json.dumps(theirs)); await sync(10)
    r=await ev(B,"(()=>{ const o=FREE.objs.find(q=>q.nid===window.__theirs); const m=FREE.objs.find(q=>q.nid===window.__mine); return [o&&o.sel.b, m&&m.sel.b, FREE.objs.length]; })()")
    ok(r[0]==3 and r[1]==7, 'Ana pinta su bloque y Beto lo ve; el de Beto sigue como él lo pintó %s'%r)
    # 5. Ana cambia al espacio y quita una pelota: Beto lo ve
    await ev(A,"(()=>{ freeEnvOpen(); const rows=document.querySelectorAll('#freeEnv .env-row'); [...rows[0].children].find(b=>b.textContent.includes('Espacio')).click(); document.querySelector('#freeEnvOk').click(); const d=FREE.dyn[0]; FREE.tgt=d; FREE.del=true; freeRemove(); FREE.del=false; return 1; })()"); await sync(10)
    r=await ev(B,"[FREE.env.piso, FREE.floor.material[2].map===FREE_FLOOR.espacio, sky.dayK<.2, FREE.dyn.length]")
    ok(r==['espacio',True,True,49], 'Ana se va al espacio y quita una pelota: Beto también está en el espacio (de noche) y ve 49 pelotas %s'%r)
    # 6. Beto sale: su propio Modo libre vuelve a 1000 y 100
    r=await ev(B,"(()=>{ ui('toMenuBtn').click(); const ask=!!document.getElementById('fnAsk') && !document.getElementById('fnAsk').hidden; document.getElementById('fnAskN').click(); return [ask, FNET.on, FREE_MAX, FREE_DYN]; })()")
    ok(r==[True,False,1000,100], 'Beto sale (le ofrece copia y dice que no): en su Modo libre vuelven los límites de 1000 y 100 %s'%r)
    ok(not ea and not eb,'sin errores %s %s'%(ea[:3],eb[:3])); await b.close()
asyncio.run(m())
