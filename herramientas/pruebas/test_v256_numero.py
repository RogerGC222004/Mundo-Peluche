# v256: ¡Al número! — piscina de pelotitas con 10×10 casillas; la pantalla enseña una operación y desaparecen las incorrectas.
# Revisa: el lugar (placa, teletransporte, piso, escaleras), las operaciones (fáciles, enteras, varios bloques correctos),
# una partida tú solo (aciertas, fallas, caes a las pelotitas y te quedas ahí, récord y monedas), el «techo» de la piscina,
# lanzar pelotitas, una partida contra 3 de la CPU, las paredes invisibles solo arriba, los textos en inglés y los dibujos.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, locale='es-MX'); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("if(!sessionStorage.getItem('t256')){ sessionStorage.setItem('t256','1'); localStorage.clear(); } localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false, autoRes:false}));")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=180000)
    await ev("startGame()"); await pg.wait_for_timeout(1500)
    await ev("""window.requestAnimationFrame=()=>0; window.__run=(sec,fn)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); if(fn && fn(i)===true) return true; update(.05,t); scene.updateMatrixWorld(); } return false; };
      window.__G=()=>AR.G[NUMI]; window.__S=()=>numStage(AR.G[NUMI]); window.__on=k=>{ const w=numTileW(k); player.pos.set(w.x,NUMG.Y+.02,w.z); player.vel.set(0,0,0); player.vy=0; player.grounded=true; };
      window.__good=(G,S)=>{ const D=numRound(G.sd,S.r); for(let k=44;k<144;k++) if(numOk(D,k%100)) return k%100; return -1; };
      window.__bad=(G,S)=>{ const D=numRound(G.sd,S.r); for(let k=44;k<144;k++) if(!numOk(D,k%100)) return k%100; return -1; };
      window.__until=(f,sec)=>__run(sec||60,()=>!!f()); 1""")
    # 1. el lugar
    r=await ev("""(()=>{ const A=AR_SPOTS[NUMI], tp=TELEPORTS.find(t=>t.id==='ar_numero'), H=NUMG.N*NUMG.T/2;
      const tile=groundAt(...(w=>[w.x,w.z])(numTileW(55)),NUMG.Y+.3), pool=groundAt(...(w=>[w.x,w.z])(arW(A,3,-4,0)),1.2);
      const st=[...Array(8)].map((_,i)=>{ const w=arW(A,-17.6+i*.9,0,0); return +groundAt(w.x,w.z,NUMG.Y+1).toFixed(2); });
      const ps=[...Array(5)].map((_,i)=>{ const w=arW(A,0,12.9-i*.62,0); return +groundAt(w.x,w.z,2).toFixed(2); });
      const pz=A.plate, ph=terrainH(pz[0],pz[1]);
      return [NUMI, A.id, A.name, !!tp, +tile.toFixed(2), +pool.toFixed(2), st, ps, +ph.toFixed(2), CPU_AI[NUMI]===numBot]; })()""")
    ok(r[1]=='numero' and r[3] and abs(r[4]-5)<.01 and abs(r[5]-.4)<.05 and r[6]==sorted(r[6]) and r[6][-1]>4 and r[6][0]<1.4 and max(r[7])>=1.35 and r[9], 'el lugar: minijuego %s «%s», teletransporte, casilla a %s m, piscina a %s m, la escalera grande sube %s, la escalerita %s, placa a %s m, con CPU'%(r[0],r[2],r[4],r[5],r[6],r[7],r[8]))
    # 2. las operaciones
    r=await ev("""(()=>{ let bad=[], n=0, ops={}, minC=99, sizes={}, maxDiv=0;
      for(let sd=1;sd<=80;sd++) for(let rd=0;rd<12;rd++){ const D=numRound(sd*7919,rd); n++; ops[D.op]=(ops[D.op]||0)+1;
        const real=D.op==='+'?D.a+D.b:D.op==='−'?D.a-D.b:D.op==='×'?D.a*D.b:D.a/D.b; if(real!==D.ans || !Number.isInteger(D.ans) || D.ans<0) bad.push('res '+D.text);
        if(D.op==='÷'){ maxDiv=Math.max(maxDiv,D.a); if(D.b<1||D.b>10||D.ans<1||D.ans>10||D.a>30) bad.push('div '+D.text); } else if(D.a<1||D.a>10||D.b<1||D.b>10) bad.push('num '+D.text);
        if(D.op==='−' && D.ans<1) bad.push('resta '+D.text);
        const cov=new Set(); let nc=0; for(let k=0;k<100;k++){ if(D.own[k]<0) bad.push('hueco'); cov.add(D.own[k]); }
        for(const B of D.blocks){ sizes[B.w+'x'+B.h]=(sizes[B.w+'x'+B.h]||0)+1; if(B.v===D.ans) nc++; else if(B.v<0||B.v>100) bad.push('mal '+B.v); }
        minC=Math.min(minC,nc); if(cov.size!==D.blocks.length) bad.push('bloques'); }
      return [n, bad.slice(0,5), ops, minC, sizes, maxDiv]; })()""")
    big=r[4].get('3x3',0)+r[4].get('2x2',0); tot=sum(r[4].values())
    ok(not r[1] and r[3]>=3 and len(r[2])==4 and big/tot>.6, 'operaciones: %d rondas revisadas, todas exactas y con números del 1 al 10 (divisiones hasta %d); al menos %d bloques correctos; tipos %s; bloques %s'%(r[0],r[5],r[3],r[2],r[4]))
    # 3. tú solo: aciertas 2, fallas la 3ª, caes a las pelotitas y te quedas ahí
    r=await ev("""(()=>{ const A=AR_SPOTS[NUMI]; const [px,pz]=A.plate; player.pos.set(px,terrainH(px,pz)+.05,pz); __run(.2);
      const acts=arenaActions(); cpuOpen(NUMI); const solo=!ui('cpuSolo').hidden; CPU.pick.n=0; ui('cpuGo').onclick(); __until(()=>__G().ph===3,20);
      const st0=[AR.me.st, __G().pl.length, Math.abs(player.pos.y-NUMG.Y)<.2], seen=[];
      for(let rd=0;rd<3;rd++){ __until(()=>{ const S=__S(); return S && S.k==='q' && S.r===rd; },30); const G=__G(), S=__S(); __on(rd<2?__good(G,S):__bad(G,S)); __run(.3); seen.push(ui('arTxt').textContent);
        __until(()=>{ const S=__S(); return !S || S.k!=='q'; },15); __run(2); seen.push([AR.me.st, +player.pos.y.toFixed(1)]); }
      __run(2); const inPool=player.pos.y<2 && Math.abs(arL(A,player.pos.x,player.pos.z)[0])<11;
      __until(()=>__G().ph===4,10); const res=[ui('arResTitle').textContent, ui('arResText').textContent, ui('arResCoins').textContent];
      const rec=localStorage.getItem('mundoPelucheNumRec'); __until(()=>__G().ph===0,15); __run(1);
      return [acts&&acts[0]&&acts[0].label, solo, st0, seen, inPool, res, rec, AR.me.a]; })()""")
    ok(r[0]=='🤖 Jugar contra la CPU' and r[1] and r[2]==[2,1,True], 'tú solo: desde la placa «Jugar contra la CPU» → «Solo yo»; empiezas arriba de las casillas %s'%r[2])
    ok(r[3][1][0]==2 and r[3][3][0]==2 and r[3][5][0]==3 and r[3][5][1]<1.5 and r[4], 'aciertas 2 rondas (sigues arriba), en la 3ª fallas y caes a las pelotitas (y te quedas en la piscina) %s'%r[3])
    ok('🔢' in r[3][0] and 'Aciertos: 0' in r[3][0] and 'Aciertos: 2' in r[3][4], 'el letrero de arriba enseña la operación y tus aciertos «%s» · «%s»'%(r[3][0],r[3][4]))
    ok(r[5][0]=='¡Récord nuevo!' and 'Aciertos: 2' in r[5][1] and r[5][2]=='+4' and r[6]=='2' and r[7]==-1, 'al final: %s · «%s» · %s monedas; se guarda el récord (%s) y sales de la partida'%(r[5][0],r[5][1],r[5][2],r[6]))
    # 4. desde la piscina nadie llega a las casillas; y se pueden lanzar pelotitas (no suben más que las casillas)
    r=await ev("""(()=>{ const A=AR_SPOTS[NUMI], w=arW(A,2,-3,0); player.pos.set(w.x,NUMG.h+.05,w.z); player.vel.set(0,0,0); __run(.5); let top=0;
      __run(3,i=>{ if(i%6===0){ player.vy=14; player.grounded=false; } top=Math.max(top,player.pos.y); });
      __run(1.5); const lab=(numActions()||[])[0]; const t0=NUM.balls.out.reduce((a,b)=>a+b,0); let hi=0; camera.position.set(w.x,1,w.z); camera.lookAt(w.x+.3,30,w.z+.3); camera.updateMatrixWorld(); numThrow(); const t1=NUM.balls.out.reduce((a,b)=>a+b,0);
      __run(4,()=>{ for(const f of NUM.fly) hi=Math.max(hi,f.m.position.y); }); const t2=NUM.balls.out.reduce((a,b)=>a+b,0);
      return [+top.toFixed(2), lab&&lab.label, t0, t1, +hi.toFixed(2), t2, NUM.fly.length]; })()""")
    ok(r[0]<5-1.9 and r[1]=='🔴 Lanzar pelotita' and r[3]==1 and r[4]<5-.7 and r[5]==0, 'en la piscina: brincando llegas máximo a %s m (las casillas están a 5 m); «Lanzar pelotita» la avienta hacia arriba (hasta %s m) y cae de nuevo a la piscina %s'%(r[0],r[4],r))
    # 5. paredes invisibles: durante una partida solo arriba (la piscina es de todos)
    r=await ev("""(()=>{ const A=AR_SPOTS[NUMI], c=arW(A,0,0,0); return [arInZone(NUMI,c.x,NUMG.Y+.1,c.z), arInZone(NUMI,c.x,NUMG.h+.1,c.z), arInZone(NUMI,c.x,NUMG.h+2.5,c.z)]; })()""")
    ok(r==[True,False,False], 'paredes invisibles de la partida: arriba sí, en la piscina no %s'%r)
    # 6. contra 3 de la CPU (difícil): tú fallas en la 1ª; ellos siguen; los que caen se quedan en las pelotitas; resultados
    r=await ev("""(()=>{ const A=AR_SPOTS[NUMI]; const [px,pz]=A.plate; player.pos.set(px,terrainH(px,pz)+.05,pz); __run(.2); cpuStart(NUMI,3,2); __until(()=>__G().ph===3,20);
      const n=__G().pl.length; __until(()=>{ const S=__S(); return S && S.k==='q'; },10); const G=__G(); __on(__bad(G,__S()));
      let outBots=[], maxR=0; __until(()=>{ const S=__S(); if(S) maxR=Math.max(maxR,S.r); for(const r of cpuBots()) if(r.az[1]===3 && !outBots.some(x=>x.startsWith(r.uid+':'))){ outBots.push(r.uid+':'+r.pos.y.toFixed(1)); } return __G().ph===4; },240);
      const G2=__G(), sc=G2.rk.map(u=>numScoreOf(G2,u)); return [n, AR.me.st, maxR, outBots, G2.rk.length, sc, G2.tie, ui('arResRank').textContent, ui('arResTitle').textContent]; })()""")
    ok(r[0]==4 and r[1] in (3,0) and r[4]==4 and r[5]==sorted(r[5],reverse=True) and r[5][-1]==0, 'contra 3 de la CPU: 4 jugadores; fallas en la 1ª; llegan hasta la ronda %d; puntos %s · «%s» · %s'%(r[2]+1,r[5],r[7],r[8]))
    ok(all(float(x.split(':')[-1])<1.5 for x in r[3]), 'los de la CPU que caen se quedan en las pelotitas %s'%r[3])
    await ev("__until(()=>__G().ph===0,20); arLeave(); 1")
    # 7. inglés
    r=await ev("""(()=>{ I18N.set('en'); const t=[I18N.t('¡Al número!'), I18N.t('Ronda 3 de 12'), I18N.t('Aciertos: 4'), I18N.t('Quedan 2 · 🔢 7 × 8 = ? · 6 s'), I18N.t('🔴 Lanzar pelotita'), I18N.t('¡A las pelotitas! 🎈'), I18N.t('Solo yo'), I18N.t(NEWS['256'][0])]; I18N.set('es'); return t; })()""")
    ok(r[0]=='Number Jump' and r[1]=='Round 3 of 12' and r[2]=='Correct: 4' and r[3].startswith('2 left') and 'Throw' in r[4] and 'ball pit' in r[5] and r[6]=='Just me' and 'Number Jump' in r[7], 'en inglés: %s'%r)
    # 8. dibujos cerca (de lejos se salta todo)
    r=await ev("""(()=>{ const tp=TELEPORTS.find(t=>t.id==='ar_numero'); teleportTo(tp); __run(2); renderer.render(scene,camera); const near=renderer.info.render.calls, tri=renderer.info.render.triangles;
      teleportTo(TELEPORTS.find(t=>t.id==='inicio')); __run(2); return [near, tri]; })()""")
    ok(r[0]<600, 'viendo la piscina desde la placa (dibujo directo, sin el recorte de zonas): %d dibujos, %dk triángulos'%(r[0],r[1]//1000))
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
