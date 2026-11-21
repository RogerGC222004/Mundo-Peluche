# v251: 1ª persona (linterna y sombra) y cartel de misiones de dulce
#  A) en 1ª persona tu peluche sigue en el mundo (visible, hace sombra) pero la cámara no lo pinta (copias de material sin color)
#  B) al volver a 3ª persona regresan sus materiales de siempre (y no se tocan los de los peluches de los demás)
#  C) la linterna en 1ª persona sigue a tu cámara (se mueve contigo y alumbra hacia donde miras)
#  D) el cartel: texto centrado y que cabe; los 3 estilos se arman sin errores
import asyncio, json, re
from playwright.async_api import async_playwright
JUEGO='/home/claude/mundo-peluche.html'
REAL=open('threerepo/build/three.min.js').read()
SRC=open(JUEGO, encoding='utf-8').read(); VER=re.search(r"const GAME_VERSION='(\d+)'",SRC).group(1)
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+SRC.replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True)
    pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low',qDef:1,hints:false,weather:false})); localStorage.setItem('mundoPelucheEcon124','1'); localStorage.setItem('mundoPelucheNovedades','%s');"%VER)
    async def route(r):
      u=r.request.url
      if u.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in u: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev("startGame(); selectedSlot=hotbar.indexOf('lamp'); holding=true; applyHeld(); 1"); await pg.wait_for_timeout(1500)
    MATS="(()=>{ let n=0,hid=0,sh=0; plush.traverse(m=>{ if(!m.isMesh) return; n++; const M=[].concat(m.material); if(M.every(x=>x.colorWrite===false)) hid++; if(m.castShadow) sh++; }); return {n,hid,sh}; })()"
    t3=await ev(MATS)
    await ev("window.__M0=new Map(); plush.traverse(m=>{ if(m.isMesh) __M0.set(m,m.material); }); 1")
    await ev("setCam('first'); 1"); await pg.wait_for_timeout(1200)
    f=await ev("(()=>{ const o="+MATS+"; o.vis=plush.visible; let shared=0; const mine=new Set(); plush.traverse(m=>{ if(m.isMesh) [].concat(m.material).forEach(x=>mine.add(x)); }); for(const r of [feltM('#8a5a34')]) if(mine.has(r)) shared++; o.shared=shared; return o; })()")
    ok(f['vis'] and f['hid']==f['n'] and f['n']>10, '👻 en 1ª persona tu peluche sigue en el mundo, pero la cámara no lo pinta (%d piezas)'%f['n'])
    ok(f['sh']>=t3['sh']*0.8 and f['sh']>5, '🌤️ y sus piezas siguen haciendo sombra (%d con sombra)'%f['sh'])
    r=await ev("(async()=>{ const W=()=>new Promise(r=>setTimeout(r,500)); const M=plush.userData.mg; const o={lamp:M&&M.lamp.visible}; const s0=[M.spot.x,M.spot.z]; player.pos.x+=6; await W(); const s1=[M.spot.x,M.spot.z];"
               +" yaw+=Math.PI/2; await W(); const s2=[M.spot.x,M.spot.z]; o.mueve=Math.abs(s1[0]-s0[0])>4; o.gira=Math.hypot(s2[0]-s1[0],s2[1]-s1[1])>2;"
               +" camera.getWorldDirection(_lw); const dx=M.spot.x-camera.position.x, dz=M.spot.z-camera.position.z, L=Math.hypot(dx,dz)||1; o.mira=(dx*_lw.x+dz*_lw.z)/L/Math.hypot(_lw.x,_lw.z); return o; })()")
    ok(r['lamp'] and r['mueve'] and r['gira'], '🔦 la linterna en 1ª persona se mueve contigo y gira con la cámara (ya no se queda donde cambiaste)')
    ok(r['mira']>0.9, '👀 alumbra hacia donde miras (%.2f)'%r['mira'])
    await ev("setCam('third'); 1"); await pg.wait_for_timeout(1200)
    t=await ev(MATS)
    same=await ev("(()=>{ let d=0; for(const [m,mt] of __M0) if(m.parent && m.material!==mt) d++; return d; })()")
    ok(t['hid']==0 and same==0, '🧸 al volver a 3ª persona se ve normal otra vez (regresan sus materiales de siempre)')
    r=await ev("(()=>{ const o={}; o.estilo=QB.st; const g=QB.cv.getContext('2d'); const Q=qList(); let max=0; for(const q of Q){ qFit(g,q.t,370,26,'800','Nunito, sans-serif'); max=Math.max(max,g.measureText(q.t).width); } qFit(g,'⭐ Misiones del día ⭐',370,42,'800','Sniglet, Nunito, sans-serif'); o.tit=g.measureText('⭐ Misiones del día ⭐').width; o.max=max;"
               +" o.largo=0; for(const P of QPOOL) for(const n of P[1]){ const t=P[2].replace('{n}',lgFmtN(P[0],n)); qFit(g,t,370,26,'800','Nunito, sans-serif'); o.largo=Math.max(o.largo,g.measureText(t).width); } return o; })()")
    ok(r['tit']<=372 and r['max']<=372 and r['largo']<=372, '📏 el título y todas las misiones posibles caben con margen (título %d px, la más larga %d px de 512)'%(r['tit'],r['largo']))
    r=await ev("(()=>{ const out=[]; for(const st of ['a','b','c']){ scene.remove(QB.g); QB.g=null; qBoardBuild(st); out.push(QB.g.children.length); } scene.remove(QB.g); QB.g=null; qBoardBuild(); return [out, QB.st]; })()")
    ok(all(0<n<=6 for n in r[0]), '🍭 los 3 estilos del cartel se arman y sus piezas se juntan (%s piezas)'%r[0])
    ok(not errs, '🚫 sin errores (%s)'%errs[:3])
    await b.close()
asyncio.run(m())
