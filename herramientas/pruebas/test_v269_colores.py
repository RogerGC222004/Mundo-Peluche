# v269: «Sigue los colores»: un puente de baldosas de colores; el camino bueno se ilumina y se apaga, todos cruzan; si pisas mal
# caes a las pelotitas y quedas fuera; la siguiente vuelta es de regreso y más difícil; 30 s sin avanzar = fuera; CPU y tú solo.
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
    await ev("""(()=>{ startGame(); window.requestAnimationFrame=()=>0; window.__run=(sec,fn)=>{ let t=clock.elapsedTime; for(let i=0;i<Math.round(sec/.05);i++){ clock.elapsedTime=(t+=.05); if(fn && fn(i)===true) return true; update(.05,t); updateRemotes(.05,t); updateSky(.05); scene.updateMatrixWorld(); } }; __run(1);
      window.__walk=(bad)=>{ const G=AR.G[COLI], S=colStage(G); if(!S||S.k!=='c') return 'no'; const D=colRound(G.sd,S.r), BL=colBL()/2, order=[...Array(COLG.R).keys()]; if(D.dir<0) order.reverse();
        const W=[]; let c=colL(player.pos.x,player.pos.z)[1], n=0; for(const i of order){ const s=-BL+(i+.5)*COLG.RS; if(D.good[i]>=0){ let j=D.good[i]; if(n===bad) j=j<COLG.C-1?j+1:j-1; c=(j-(COLG.C-1)/2)*COLG.CS; if(n===0) W.unshift([-D.dir*(BL+.8),c]); n++; } W.push([s,c]); } W.push([D.dir*(BL+2.5),c]);
        for(let q=W.length-2;q>=0;q--){ const i=colRowAt(W[q][0]); if(i<0||i>=COLG.R||D.good[i]<0) W[q][1]=W[q+1][1]; }
        let k=0; for(let t=0;t<900;t++){ const [s0,c0]=colL(player.pos.x,player.pos.z), [ts,tc]=W[k], ds=ts-s0, dc=tc-c0, d=Math.hypot(ds,dc); if(d<.15){ k++; if(k>=W.length) break; continue; }
          const st=Math.min(d,.2), w=colW(s0+ds/d*st,c0+dc/d*st,player.pos.y); player.pos.x=w.x; player.pos.z=w.z; __run(.05); if(AR.me.st!==2 || COL.falling>=0) break; }
        __run(1.5); return [AR.me.st, COL.done, COL.falling]; };
      window.__waitC=r=>__run(60,()=>{ const G=AR.G[COLI], S=colStage(G); return G.ph>3 || G.ph===0 || (S && S.k==='c' && S.r===r); }); return 1; })()""")
    # 1. en la lista y en la isla
    r=await ev("""(async()=>{ ONLINE.on=false; ui('mgBtn').click(); await new Promise(f=>setTimeout(f,300)); const c=[...ui('mgqList').querySelectorAll('.mgq-g')].find(c=>c.textContent.includes('Sigue los colores')); const pic=c&&c.querySelector('.pic');
      const b=c?[...c.querySelectorAll('.mgq-b')].map(x=>x.className.includes('solo')?'S':x.className.includes('cpu')?'C':'J').join(''):''; closeMgq(); menuModes(false); startGame();
      return [!!c, !!(pic && pic.style.backgroundImage.includes('webp')), b, AR_SPOTS[COLI].name, COLI, !!HOWTO.G.colores, typeof DRAW!=='undefined'||true]; })()""")
    ok(r[0] and r[1] and r[2]=='SCJ' and r[3]=='Sigue los colores' and r[4]==15 and r[5], '1 «Sigue los colores» sale en la lista con su portada: tú solo, CPU y jugadores; tiene sus carteles de cómo se juega %s'%r)
    # 2. las vueltas salen de la semilla: 12 filas, cada vez más de colores y menos tiempo; el camino siempre se puede seguir
    r=await ev("""(()=>{ const L=[]; let okAdj=true; for(let r=0;r<12;r++){ const D=colRound(777,r); let prev=-1; for(let i=0;i<12;i++){ const g=D.good[i]; if(g<0) continue; if(prev>=0 && Math.abs(g-prev)>1) okAdj=false; prev=g; } L.push([D.nc, D.lit, D.dir]); }
      const same=JSON.stringify([...colRound(777,3).good])===JSON.stringify([...colRound(777,3).good]); COL.rd.clear(); const again=JSON.stringify([...colRound(777,3).good]);
      return [L.map(x=>x[0]).join(','), L[0][1], L[11][1], L.map(x=>x[2]).join(','), okAdj, same]; })()""")
    ok(r[0]=='6,7,8,9,10,11,12,12,12,12,12,12' and r[1]==6000 and r[2]==2500 and r[3].startswith('1,-1,1,-1') and r[4] and r[5], '2 cada vuelta: más filas de colores (6 → 12), se ilumina menos (6 s → 2.5 s), una de ida y otra de regreso; el camino bueno va de baldosa en baldosa vecina %s'%r)
    # 3. tú solo: empiezas en la plataforma; mientras se ilumina no se puede pisar el puente
    r=await ev("""(()=>{ mgqLocal(COLI,0,1); __run(20,()=>AR.G[COLI].ph===3); __run(8,()=>(colStage(AR.G[COLI])||{}).k==='l'); __run(1.8);
      const onA=colL(player.pos.x,player.pos.z)[0]<-colBL()/2, glow=COL.glow.count; for(let i=0;i<40;i++){ const [s,c]=colL(player.pos.x,player.pos.z), w=colW(s+.3,c,player.pos.y); player.pos.x=w.x; player.pos.z=w.z; __run(.05); }
      const still=colL(player.pos.x,player.pos.z)[0]<-colBL()/2, hud=ui('arTxt').textContent; __waitC(0); return [onA, glow, still, hud, COL.glow.count, +player.pos.y.toFixed(1)]; })()""")
    ok(r[0] and r[1]>0 and r[2] and 'Mira el camino' in r[3] and r[4]==0 and r[5]==6, '3 empiezas en tu plataforma; el camino brilla (%s baldosas) y no te deja pisar el puente hasta «¡Crucen!»; luego se apaga %s'%(r[1],r))
    # 4. cruzas por el camino bueno (en diagonal de una a la vecina no te caes) y la siguiente vuelta es de regreso
    r=await ev("(()=>{ const a=__walk(-1); return [...a, ui('arTxt').textContent]; })()")
    ok(r[0]==2 and r[1]==0 and r[2]==-1 and ('Llegaste' in r[3] or 'Siguiente' in r[3]), '4 cruzas por el camino bueno y llegas al otro lado: «%s» %s'%(r[3],r))
    r=await ev("(()=>{ __waitC(1); const s=colL(player.pos.x,player.pos.z)[0]; const a=__walk(-1); return [s>colBL()/2, colRound(AR.G[COLI].sd,1).dir, ...a]; })()")
    ok(r[0] and r[1]==-1 and r[2]==2 and r[3]==1, '4b la siguiente vuelta empieza del otro lado y se cruza de regreso %s'%r)
    # 5. en el puente no se brinca (no se vale saltarse filas)
    r=await ev("""(()=>{ __waitC(2); const D=colRound(AR.G[COLI].sd,2), BL=colBL()/2; let i0=D.dir>0?0:11; while(D.good[i0]<0 && i0>=0 && i0<12) i0+=D.dir; const c=(D.good[i0]-(COLG.C-1)/2)*COLG.CS, w=colW(-BL+(i0+.5)*COLG.RS,c,COLG.Y); player.pos.set(w.x,w.y,w.z); __run(.3);
      player.vy=9; let top=0; for(let k=0;k<20;k++){ __run(.05); top=Math.max(top,player.pos.y); } return [+(top-COLG.Y).toFixed(2), AR.me.st]; })()""")
    ok(r[0]<=.5 and r[1]==2, '5 en el puente no se brinca: subes %s m como mucho %s'%(r[0],r))
    # 6. si pisas una equivocada: se hunde, caes a las pelotitas y quedas fuera; tu récord en vueltas
    r=await ev("(()=>{ const a=__walk(1); const g=COL.gone.size; __run(4); return [a[2]>=0, g, AR.me.st, ui('arResTitle').textContent, ui('arResText').textContent, JSON.stringify(soloRecs())]; })()")
    ok(r[0] and 'Vueltas: 2' in r[4] and '"colores":2' in r[5], '6 si pisas un color equivocado se hunde y caes a las pelotitas: quedas fuera (récord: %s) %s'%(r[4],r))
    await ev("(()=>{ __run(8); arLeave(); __run(.5); return 1; })()")
    # 7. 30 s sin avanzar: a los 20 te anima, a los 30 quedas fuera (sin regaños)
    r=await ev("""(()=>{ mgqLocal(COLI,0,1); __run(20,()=>AR.G[COLI].ph===3); __waitC(0); const L=[]; __run(21); L.push(ui('arTxt').textContent, COL.warned); __run(10); L.push(AR.me.st); return L; })()""")
    ok('⏱' in r[0] and r[1] and r[2]==3, '7 si te quedas quieto: a los 20 s «¿Cuál era el camino? ¡Inténtalo! 🙂» y cuenta regresiva; a los 30 s quedas fuera %s'%r)
    await ev("(()=>{ __run(8); arLeave(); __run(.5); return 1; })()")
    # 8. contra la CPU: también cruzan; si uno pisa mal, la baldosa se hunde para todos; tabla con las vueltas
    r=await ev("""(()=>{ mgqLocal(COLI,3,0); __run(25,()=>AR.G[COLI].ph===3); let sank=0, crossed=0; for(let r=0;r<6 && AR.G[COLI].ph===3;r++){ __waitC(r); if(AR.G[COLI].ph!==3) break; __walk(-1); __run(30,()=>{ const G=AR.G[COLI], S=colStage(G); return G.ph!==3 || (S && S.k!=='c'); });
        sank=Math.max(sank,COL.gone.size); crossed=Math.max(crossed,...cpuBots().map(b=>b.az[2]*10+b.az[3])); if(AR.me.st!==2) break; }
      const out=cpuBots().filter(b=>b.az[1]===3).length; if(AR.G[COLI].ph===3){ AR.G[COLI].ms=0; } __run(3); const rk=ui('arResRank').textContent; return [crossed, out, rk, (rk.match(/🌈/g)||[]).length]; })()""")
    ok(r[0]>=1 and r[3]==4, '8 los peluches de la CPU cruzan (y a veces se caen: %s); al final, la tabla con las vueltas de cada quien: %s'%(r[1],r[2]))
    await ev("(()=>{ __run(8); arLeave(); __run(.5); return 1; })()")
    # 9. los jugadores se atraviesan en el puente; en inglés
    r=await ev("(()=>{ const src=[...document.scripts].map(s=>s.text).join(''); return [src.includes('arCol()||(r.az&&r.az[0]===COLI&&r.az[1]===2)'), I18N.t('Sigue los colores'), I18N.t('¡Buen intento!')]; })()")
    await ev("(()=>{ I18N.set('en'); return 1; })()"); r2=await ev("I18N.t('Sigue los colores')"); await ev("(()=>{ I18N.set('es'); return 1; })()")
    ok(r[0] and r2=='Follow the Colors', '9 en el puente los jugadores se atraviesan (nadie tumba a nadie); en inglés se llama «%s»'%r2)
    ok(not errs and not cerr, 'sin errores %s %s'%(errs[:3],cerr[:3]))
    await b.close()
asyncio.run(m())
