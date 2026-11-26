# v267: Pogo saltarín: brinca en tu pogo de plataforma en plataforma (salen de la semilla, iguales para todos); gana quien llegue más alto
# en 3 minutos; plataformas que se mueven o se rompen (para todos), trampolines, resortes, nubes y globos; tú solo, CPU o jugadores.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
SEED="""localStorage.clear(); localStorage.setItem('mundoPelucheEcon124','1');
localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false, autoRes:false}));"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    pg=await (await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, locale='es-MX')).new_page(); errs=[]; cerr=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console",lambda msg: cerr.append(msg.text[:200]) if msg.type=='error' and ('Shader' in msg.text or 'WebGL' in msg.text or 'GL_' in msg.text) else None)
    await pg.add_init_script(SEED)
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=180000)




    # 1. en la lista de minijuegos: con portada y Tú solo, CPU y Jugadores
    r=await ev("""(async()=>{ ONLINE.on=false; ui('mgBtn').click(); await new Promise(f=>setTimeout(f,300)); const c=[...ui('mgqList').querySelectorAll('.mgq-g')].find(c=>c.textContent.includes('Pogo')); const pic=c&&c.querySelector('.pic');
      const b=c?[...c.querySelectorAll('.mgq-b')].map(b=>b.classList.contains('solo')?'S':b.classList.contains('cpu')?'C':'J').join(''):''; ui('mgqClose')&&ui('mgqClose').click(); return [!!c, !!pic && pic.style.backgroundImage.startsWith('url("data:image/webp'), b, AR_SPOTS[POGI].name, POGI, AR_SPOTS[13].id]; })()""")
    ok(r==[True,True,'SCJ','Pogo saltarín',14,'numero'], '1 «Pogo saltarín» sale en la lista de minijuegos con su portada: tú solo, CPU o jugadores %s'%r)
    await ev("startGame()"); await pg.wait_for_timeout(1500)
    await ev("""(()=>{ window.requestAnimationFrame=()=>0; window.__run=(sec,fn)=>{ let t=clock.elapsedTime; for(let i=0;i<Math.round(sec/.05);i++){ clock.elapsedTime=(t+=.05); if(fn && fn(i)===true) return true; update(.05,t); } }; __run(1); weatherOfSlot=()=>'clear';
      window.__drive=()=>{ const P=player.pos, T=pogoT(); const c=POG.L[Math.max(0,POG.cur)]; let ti=POG.cur<=0?POG.starts[0]:(c.nx>=0?c.nx:c.alt); let g=0; while(ti>=0 && POG.broken.has(ti) && g++<5) ti=POG.L[ti].nx>=0?POG.L[ti].nx:POG.L[ti].alt; const tg=ti>=0?POG.L[ti]:null; if(!tg) return; const [ox,oz]=pogoOff(tg,T), dx=POGG.x+tg.x+ox-P.x, dz=POGG.z+tg.z+oz-P.z, d=Math.hypot(dx,dz); yaw=Math.PI; const k=Math.min(1,d/2); stick.y=d>.2?-dz/d*k:0; stick.x=d>.2?-dx/d*k:0; keys.Space=true; };
      window.__stop=()=>{ stick.x=0; stick.y=0; keys.Space=false; }; return 1; })()""")

    # 2. las plataformas: al azar en cada partida pero iguales para todos (salen de la semilla); de 2 a 4 caminos con cruces, alcanzables y cada vez más difíciles
    r=await ev("""(()=>{ const A=pogoGen(777), a=A.L, b=pogoGen(777).L, c=pogoGen(778).L; const same=JSON.stringify(a)===JSON.stringify(b), diff=JSON.stringify(a)!==JSON.stringify(c);
      const nps=new Set(); let alts=0, brs=0; for(let sd=1;sd<=40;sd++){ const g=pogoGen(sd*7919); nps.add(g.nP); alts+=g.L.filter(p=>p.alt>=0).length>40?1:0; brs+=g.L.some(p=>p.bridge)?1:0; }
      let mx=0, mr=0; for(const p of a){ if(p.i===0 || p.pa<0 || p.nx<0) continue; const q=a[p.nx]; mx=Math.max(mx,Math.hypot(q.x-p.x,q.z-p.z)); mr=Math.max(mr,q.y-p.y); }
      const lv=p=>p.y-a[0].y, early=a.filter(p=>lv(p)<12 && p.i>0), firstMov=a.find(p=>p.k===1), firstBrk=a.find(p=>p.k===2), sorted=a.every((p,i)=>i===0||p.y>=a[i-1].y);
      return [same, diff, [...nps].sort().join(''), alts, brs, +mx.toFixed(1), +mr.toFixed(2), early.every(p=>p.k!==1 && p.k!==2), +lv(firstMov).toFixed(0), +lv(firstBrk).toFixed(0), a.filter(p=>p.h===1).length, a.filter(p=>p.h===2).length, a.filter(p=>p.k===3).length, A.B.length, Math.max(...a.slice(1).map(p=>Math.hypot(p.x,p.z)+p.w/2)).toFixed(1), sorted]; })()""")
    ok(r[0] and r[1] and r[2]=='234' and r[3]>=35 and r[4]>=15 and r[5]<=8.6 and r[6]<=6.8 and r[7] and r[8]>=12 and r[9]>=35 and r[10]>5 and r[11]>3 and r[12]>5 and r[13]>10 and float(r[14])<26 and r[15], '2 la torre sale al azar en cada partida (iguales para todos): de 2 a 4 caminos con cruces y puentes, siempre alcanzables, cada vez más difícil %s'%r)

    # 3. tú solo: empiezas en la plataforma redonda y brincas solito; manteniendo Saltar brincas más alto
    r=await ev("""(()=>{ const A=AR_SPOTS[POGI], [px,pz]=A.plate; player.pos.set(px,terrainH(px,pz)+.05,pz); __run(.6); const lab=(arenaActions()||[])[0]; cpuStart(POGI,0,1); __run(25,()=>AR.G[POGI].ph===3);
      const G=AR.G[POGI], onBase=Math.hypot(player.pos.x-POGG.x,player.pos.z-POGG.z)<6; const jump=(hold)=>{ let pv=POG.vy, land=null, mx=0; keys.Space=hold; __run(3,()=>{ if(POG.vy>pv+5) land=player.pos.y; pv=POG.vy; if(land!==null) mx=Math.max(mx,player.pos.y-land); }); keys.Space=false; return mx; }; const lo=jump(false), hi=jump(true);
      return [lab&&lab.label, G.ph, G.pl.length, onBase, +lo.toFixed(1), +hi.toFixed(1), !!POG.stick && POG.stick.visible && POG.stick.parent===plush, ui('arTxt').textContent.startsWith('⬆')]; })()""")
    ok(r[0]=='🤖 Jugar contra la CPU' and r[1]==3 and r[2]==1 and r[3] and 5<r[4]<6.4 and r[5]>8.5 and r[6] and r[7], '3 tú solo: empiezas en la plataforma redonda con tu pogo; brincas solito (%s m) y manteniendo Saltar, más alto (%s m) %s'%(r[4],r[5],r))
    r=await ev("""(()=>{ const L=[]; __run(40,i=>{ __drive(); if(i%160===0) L.push(+POG.best.toFixed(0)); }); __stop(); return [L.join(' '), +POG.best.toFixed(1), AR.me.st, ui('arTxt').textContent]; })()""")
    ok(r[1]>40 and r[2]==2, '3b muévete en el aire y vas subiendo de plataforma en plataforma (en 40 s, %s m) %s'%(r[1],r))
    r=await ev("""(()=>{ const y0=player.pos.y, b0=POG.best; __run(4); const fell=player.pos.y<y0-1; return [AR.me.st, POG.best>=b0, fell||true, AR.G[POGI].el.length]; })()""")
    ok(r[0]==2 and r[1] and r[3]==0, '3c si te caes no pierdes: cuenta lo más alto que llegaste %s'%r)

    # 4. trampolín, resorte, nube, globo y plataformas que se mueven o se rompen
    r=await ev("""(()=>{ const T=POG.L.find(p=>p.h===1 && !POG.broken.has(p.i)); player.pos.set(POGG.x+T.x,T.y+POG_TIP+1.2,POGG.z+T.z); POG.vy=-2; let mx=0; __run(3.5,()=>{ mx=Math.max(mx,player.pos.y-POG_TIP-T.y); });
      const S=POG.L.find(p=>p.h===2 && !POG.broken.has(p.i)); player.pos.set(POGG.x+S.x,S.y+POG_TIP+1.2,POGG.z+S.z); POG.vy=-2; let ms=0; __run(3,()=>{ ms=Math.max(ms,player.pos.y-POG_TIP-S.y); });
      return [+mx.toFixed(1), +ms.toFixed(1)]; })()""")
    ok(r[0]>20 and 11<r[1]<18, '4 el trampolín te avienta altísimo (%s m) y el resorte alto (%s m)'%(r[0],r[1]))
    r=await ev("""(()=>{ const B=POG.B.find(b=>!POG.used.has(b.i)); player.pos.set(POGG.x+B.x,B.y-1,POGG.z+B.z); POG.vy=0; __run(.1); const lift=POG.lift>0; let y0=player.pos.y; __run(1.5); return [lift, +(player.pos.y-y0).toFixed(1), POG.used.has(B.i)]; })()""")
    ok(r[0] and r[1]>5 and r[2], '4b el globo te jala para arriba un buen tramo (%s m) %s'%(r[1],r))
    r=await ev("""(()=>{ const M=POG.L.find(p=>p.k===1); const a=pogoOff(M,100), b=[100.7,101.5,102.4,103.3].map(t=>pogoOff(M,t)).reduce((m,q)=>Math.hypot(q[0]-a[0],q[1]-a[1])>Math.hypot(m[0]-a[0],m[1]-a[1])?q:m); const K=POG.L.find(p=>p.k===2 && !POG.broken.has(p.i)); const [ox,oz]=pogoOff(K,pogoT()); player.pos.set(POGG.x+K.x+ox,K.y+POG_TIP+.6,POGG.z+K.z+oz); POG.vy=-3; POG.lift=0;
      const n0=POG.mine.length; __run(.4); const br=POG.broken.has(K.i), pb=arenaPresence().pb; __run(1); const again=pogoLand(POGG.x+K.x+ox,POGG.z+K.z+oz,K.y+.3,K.y-.3); return [Math.hypot(a[0]-b[0],a[1]-b[1])>.3, br, POG.mine.length-n0, !!pb && pb[0]===POG.gid && pb.includes(K.i), again===null || again.i!==K.i]; })()""")
    ok(r==[True,True,1,True,True], '4c unas plataformas se mueven y otras se rompen después de un brinco (y se avisa a todos) %s'%r)
    r=await ev("""(()=>{ const K=POG.L.find(p=>p.k===2 && !POG.broken.has(p.i)); const fake={uid:'zzz9', name:'Ana', pos:new THREE.Vector3(), target:new THREE.Vector3(), obj:new THREE.Object3D(), facing:0}; pogoParse(fake,{pb:[POG.gid,K.i]}); const a=POG.broken.has(K.i); const K2=POG.L.find(p=>p.k===2 && !POG.broken.has(p.i)); pogoParse(fake,{pb:['otra',K2.i]}); return [a, POG.broken.has(K2.i)]; })()""")
    ok(r==[True,False], '4d la que rompe otro jugador también se rompe para ti (solo si es de la misma partida) %s'%r)

    # 5. al terminar los 3 minutos: tu altura y tu récord; bajas al pasto
    r=await ev("""(()=>{ __drive(); __run(3,()=>{ __drive(); }); __stop(); const best=POG.best; AR.G[POGI].ms=100; __run(2,()=>AR.G[POGI].ph===4); __run(.5); const rec=JSON.parse(localStorage.getItem('mundoPelucheSoloRec')||'{}');
      return [AR.G[POGI].ph, ui('arResTitle').textContent, ui('arResText').textContent, +best.toFixed(1), rec.pogo, player.pos.y<POG.base+3, POG.stick.visible]; })()""")
    ok(r[0]==4 and r[1]=='¡Récord nuevo!' and 'Altura' in r[2] and abs(r[4]-r[3])<.11 and r[5] and not r[6], '5 al acabar el tiempo: «¡Récord nuevo!» con tu altura (%s m) y bajas al pasto %s'%(r[3],r))
    await ev("(()=>{ __run(8); arLeave(); __run(.5); return 1; })()")

    # 6. contra la CPU: también brincan y suben; el que llegue más alto gana
    r=await ev("""(()=>{ cpuStart(POGI,3,2); __run(25,()=>AR.G[POGI].ph===3); __run(30); const B=cpuBots().map(r=>r.az[2]); const seen=cpuBots().every(r=>POG.rem.has(r) && POG.rem.get(r).visible);
      AR.G[POGI].ms=100; __run(2,()=>AR.G[POGI].ph===4); const rk=ui('arResRank').textContent; return [B.length, B.every(h=>h>5), seen, rk.includes(' m'), (rk.match(/⬆/g)||[]).length]; })()""")
    ok(r[0]==3 and r[1] and r[2] and r[3] and r[4]==4, '6 contra la CPU: los peluches de la CPU brincan en su pogo y suben; al final, la tabla con las alturas %s'%r)
    await ev("(()=>{ __run(8); arLeave(); __run(.5); return 1; })()")

    # 7. se atraviesan: otro jugador en el pogo no te empuja
    r=await ev("""(()=>{ const src=[...document.scripts].map(s=>s.text).join(''); return [src.includes("(r.az&&r.az[0]===POGI&&r.az[1]===2)"), typeof arPogo]; })()""")
    ok(r[0], '7 los jugadores en el pogo se atraviesan (nadie tumba a nadie) %s'%r)

    # 8. v267: se escoge cuánto dura (3, 5 o 10 min) ANTES de empezar; récord aparte para cada tiempo
    r=await ev("""(()=>{ localStorage.removeItem('mundoPelucheSoloRec'); localStorage.removeItem('mpPogoMin'); ui('toMenuBtn').click(); __run(.3); openMgq(); mgqKey=''; mgqRender();
      const card=[...ui('mgqList').children].find(b=>b.querySelector('b').textContent.includes('Pogo')); card.querySelector('.mgq-b.solo').click();
      const ov=!cpuOv.hidden, tt=ui('cpuTitle').textContent, rows=[ui('cpuN').hidden, ui('cpuD').hidden, ui('cpuT').hidden], btn=[...ui('cpuT').querySelectorAll('button')].map(b=>b.textContent).join(',');
      [...ui('cpuT').querySelectorAll('button')].find(b=>b.textContent==='10 min').click(); ui('cpuGo').click(); __run(.5);
      const hud=ui('arTxt').textContent, noOpt=!document.getElementById('arOpt');
      let ms=null; __run(15,()=>{ if(AR.G[POGI].ph===3){ ms=AR.G[POGI].ms; return true; } }); const dm=arenaPresence().ag.dm;
      POG.best=50; AR.G[POGI].ms=0; __run(1.5); const rec=JSON.stringify(soloRecs()), txt=ui('arResText').textContent; __run(8); arLeave(); __run(.5);
      const r={}; parseArena(r,{ag:{a:POGI,ph:3,ms:1000,gid:'x',pl:[],el:[],dm:5}}); const r2={}; parseArena(r2,{ag:{a:POGI,ph:3,ms:1000,gid:'x',pl:[],el:[],dm:7}});
      return [ov, tt, rows.join(), btn, hud, noOpt, ms, dm, rec, txt, r.ag.dm, r2.ag.dm, pogoGen(77).L.slice(-1)[0].y>2500, localStorage.getItem('mpPogoMin')]; })()""")
    ok(r[0] and r[1]=='🙂 Tú solo' and r[2]=='true,true,false' and r[3]=='3 min,5 min,10 min' and '⏱ 10 min' in r[4] and r[5] and r[6]==600000 and r[7]==10 and r[8]=='{"pogo10":50}' and '(10 min)' in r[9] and r[10]==5 and r[11]==3 and r[12] and r[13]=='10', '8 desde el menú, «Tú solo» pregunta primero cuánto dura (3, 5 o 10); récord aparte para cada tiempo %s'%r)
    r=await ev("""(()=>{ mgqCpu(POGI); const a=[ui('cpuTitle').textContent, ui('cpuN').hidden, ui('cpuT').hidden, [...ui('cpuT').querySelectorAll('button[aria-pressed=true]')].map(b=>b.textContent).join()];
      [...ui('cpuT').querySelectorAll('button')].find(b=>b.textContent==='5 min').click(); CPU.pick.n=1; ui('cpuGo').click(); let ms=null; __run(25,()=>{ if(AR.G[POGI].ph===3){ ms=AR.G[POGI].ms; return true; } });
      ui('toMenuBtn').click(); __run(1); const after=[AR.me.a, CPU.on, cpuBots().length]; closeMgq(); menuModes(false); startGame(); __run(1);
      mgqCpu(7); const other=ui('cpuT').hidden; ui('cpuCancel').click(); closeMgq(); startGame(); __run(.5);
      return [...a, ms, after.join(), other]; })()""")
    ok(r[0]=='🤖 Jugar contra la CPU' and r[1]==False and r[2]==False and r[3]=='10 min' and r[4]==300000 and r[5]=='-1,false,0' and r[6], '8b contra la CPU: en la misma ventana se escoge el tiempo; con «<» al menú la partida se acaba de verdad %s'%r)

    # 9. v268: los animalitos de las islas (monitos, tucanes, ranitas, pingüinos) salen en su isla desde que se arman (antes esperaban en el inicio)
    r=await ev("""(()=>{ const base=new Set(); scene.traverse(o=>base.add(o.uuid));
      if(!JI.done){ const g=jiBuildGen(); while(!g.next().done){} JI.done=true; } if(!WI.done){ const g=wiBuildGen(); while(!g.next().done){} WI.done=true; }
      const b=new THREE.Box3(), c=new THREE.Vector3(); let n=0; scene.children.forEach(o=>{ if(base.has(o.uuid) || !o.visible || !o.children.length) return; b.setFromObject(o); if(b.isEmpty()) return; b.getCenter(c); if(Math.hypot(c.x-START.x,c.z-START.z)<20) n++; });
      return [n, JI2.animals.length, WI2.peng.length]; })()""")
    ok(r[0]==0 and r[1]>10 and r[2]==9, '9 los monitos y pingüinos de las islas ya no aparecen en el inicio %s'%r)

    ok(not errs and not cerr, 'sin errores %s %s'%(errs[:3],cerr[:3]))
    await b.close()
asyncio.run(m())
