# v254 (rondas B y C): la lluvia moja y la nieve se junta, en tu planicie y en la isla
#  A) los materiales del juego ya traen la nieve y lo mojado (sin errores); los peluches no se cubren; las nubes y el agua tampoco
#  B) Modo libre: con «Nieve» se va cubriendo; bola de nieve (se agarra, se lanza y se deshace) y muñeco de nieve; al quitar la nieve se derrite
#  C) Modo libre: con «Lluvia» el agua de verdad se junta en el piso (en lo bajito) y al parar se seca
#  D) el mapa de techos: bajo un techo no hay nieve ni mojado
#  E) la isla: lo mismo para todos (se calcula con el clima de las últimas horas); charquitos al aire libre (no bajo el segundo piso del castillo) que salpican
#  F) la isla con nieve: bola de nieve y muñeco; huellas al caminar
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
SRC=open('/home/claude/mundo-peluche.html',encoding='utf-8').read()
pre='<script>window.__off=0; const _dn=Date.now.bind(Date); Date.now=()=>_dn()+window.__off;</script>'
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+pre+SRC.replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":True}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k,dt)=>{ dt=dt||.05; let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=dt); window.__off+=dt*1000; update(Math.min(dt,.05),t); updateSky(dt); try{ wlUpdate(); }catch(e){} } };
  window.__CLR=()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); FREE.hold=null; FREE.chg=null; freeSelect(null); suClear(); };
  window.__AT=(x,z,f)=>{ player.pos.set(FREE.X+x,FREE.Y+.05,FREE.Z+z); player.vel.set(0,0,0); player.vy=0; player.facing=f||0; yaw=player.facing+Math.PI; __S(3); };
  window.__ENV=c=>{ FREE.env={piso:'pasto',hora:'dia',clima:c}; freeEnvApply(); }; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1'); localStorage.setItem('mundoPelucheNovedades','999');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300); await ev(STEP)
    # A) los materiales
    r=await ev("""(()=>{ const L=THREE.ShaderLib; const ok=['lambert','standard','phong'].every(k=>L[k].fragmentShader.includes('wxV[0]') && L[k].vertexShader.includes('vWxP')); startGame(); __S(4);
      let pl=0, n=0; wxNoWxTick(9); plush.traverse(m=>{ if(m.isMesh){ n++; if([].concat(m.material).every(x=>x.defines && 'NO_WX' in x.defines)) pl++; } });
      return {ok, pl, n, nube:'NO_WX' in (cloudMat.defines||{})}; })()""")
    ok(r['ok'], '🎨 los materiales del juego ya saben pintar la nieve y lo mojado')
    ok(r['n']>10 and r['pl']==r['n'] and r['nube'], '🧸 tu peluche no se cubre de nieve ni se moja (%d de %d piezas), y las nubes tampoco'%(r['pl'],r['n']))
    # B) Modo libre con nieve
    await ev("(()=>{ freeEnter(); __CLR(); __AT(0,0,0); __ENV('snow'); WX.fs=0; WX.s=0; return 1; })()")
    r=await ev("(()=>{ const out=[]; for(let i=0;i<6;i++){ __S(10,3); out.push(+WX.s.toFixed(2)); } return out; })()")
    ok(r[0]<r[2]<r[5] and r[5]>.8, '❄️ Modo libre con «Nieve»: la nieve se va juntando poco a poco %s'%r)
    r=await ev("""(()=>{ __S(4); const a=freeActions(); return [a&&a[0]&&a[0].label, a&&a[1]&&a[1].label, +WXU.V[0].x.toFixed(2)]; })()""")
    ok(r[0]=='❄️ Hacer bola de nieve' and r[1]=='❄️ Hacer muñeco de nieve' and r[2]>.8, '⛄ con nieve: «%s» y «%s»'%(r[0],r[1]))
    r=await ev("""(()=>{ freeActions()[0].run(); __S(3); const d=FREE.hold, held=!!d && d.P.id==='bolanieve'; freeThrowStart(); FREE.chg.t-=900; freeThrowEnd(); let gone=false; for(let i=0;i<80 && !gone;i++){ __S(1); gone=!FREE.dyn.includes(d); }
      return [held, gone]; })()""")
    ok(r[0] and r[1], '🤾 la bola de nieve se agarra, se lanza y se deshace al pegar fuerte %s'%r)
    r=await ev("""(()=>{ __AT(0,0,0); freeActions()[1].run(); __S(2); const o=FREE.objs.find(q=>q.sel.a==='muneco'); const n0=!!o; __ENV('clear'); let gone=false, t=0; for(let i=0;i<120 && !gone;i++){ __S(5,2); t+=10; gone=!FREE.objs.some(q=>q.sel.a==='muneco'); } return [n0, gone, t, +WX.s.toFixed(2)]; })()""")
    ok(r[0] and r[1], '🌞 el muñeco de nieve sale enfrente, y cuando se va la nieve se derrite (a los %d s)'%r[2])
    # C) Modo libre con lluvia: agua de verdad
    r=await ev("""(()=>{ __CLR(); __AT(0,0,0); __ENV('rain'); WX.fw=0; WX.w=0; WX.fwVol=0; for(let i=0;i<40;i++) __S(10,.5); const v=SU.vol, n=SU.list.length; return [+WX.w.toFixed(2), +v.toFixed(3), n, +WX.fwVol.toFixed(3)]; })()""")
    ok(r[0]>.9 and r[1]>.05 and r[3]>.05 and r[3]<=1.25, '🌧️ Modo libre con «Lluvia»: se moja y el agua de verdad se junta en el piso (%.2f m³)'%r[1])
    r=await ev("""(()=>{ __ENV('clear'); const v0=SU.vol; for(let i=0;i<40;i++) __S(10,1.5); return [+v0.toFixed(3), +SU.vol.toFixed(3), +WX.fwVol.toFixed(3), +WX.w.toFixed(2)]; })()""")
    ok(r[1]<r[0]*.5 and r[3]<r[0]+1, '☀️ al parar de llover el agua se va secando (%.3f → %.3f m³)'%(r[0],r[1]))
    # D) el mapa de techos en la textura
    r=await ev("""(()=>{ __CLR(); __AT(0,-3,0); const S=FREE_SHAPES.findIndex(s=>s.id==='losa'); const o=freeAddStatic({k:'b',a:S,b:0},FREE.X,FREE.Y+3,FREE.Z+2,0,true); __ENV('snow'); WX.fs=1; ROOF.gen++; ROOF.per=60000; for(let i=0;i<20;i++) __S(1); ROOF.per=1800; WX.rT=0; __S(2);
      const V=WXU.V[1], D=WX_TEX.image.data, at=(x,z)=>{ const i=Math.floor(x-V.x), j=Math.floor(z-V.y); return V.w+D[(j*WX_N+i)*4]/255*WX_RANGE; }; return [+(at(FREE.X+.2,FREE.Z+2.2)-FREE.Y).toFixed(2), +(at(FREE.X+6.5,FREE.Z+6.5)-FREE.Y).toFixed(2)]; })()""")
    ok(r[0]>2.5 and r[1]<.6, '🏠 el mapa de techos sabe dónde hay techo: debajo de la losa a %.1f m (ahí no nieva) y al aire libre %.1f m'%(r[0],r[1]))
    await ev("(()=>{ __CLR(); freeExit(); return 1; })()")
    # E) la isla: igual para todos
    r=await ev("""(()=>{ weatherOfSlot=k=>'snow'; const now=Date.now()/1000, slot=Math.floor(now/WEATHER_SLOT), a=wxDet(slot*WEATHER_SLOT+30), b=wxDet(slot*WEATHER_SLOT+600); weatherOfSlot=k=>k%2?'rain':'clear'; const c=wxDet((slot|1)*WEATHER_SLOT+40), d=wxDet(((slot|1)+1)*WEATHER_SLOT+150);
      return [a[0],b[0],c[1],d[1]].map(v=>+v.toFixed(2)); })()""")
    ok(r[1]==1 and r[2]>.3 and 0<r[3]<1, '🕐 en la isla la nieve y lo mojado salen del clima de las últimas horas (igual en todos los teléfonos) %s'%r)
    r=await ev("""(()=>{ weatherOfSlot=k=>'rain'; const g=groundAt(-8,7,1); player.pos.set(-8,g,7); player.vel.set(0,0,0); setCam('third'); ROOF.per=60000; for(let i=0;i<40;i++) __S(1,.5); for(let i=0;i<30;i++) __S(1,.1); ROOF.per=1800;
      const L=WX.pud.L, inC=L.filter(q=>Math.hypot(q.x,q.z)<CAKE_ST.r0-.5 && !cakeHole(q.x,q.z)).length; return [+WX.w.toFixed(2), L.length, inC, WX.pud.m.count]; })()""")
    ok(r[0]>.9 and r[1]>=8 and r[3]>=8, '💧 con lluvia aparecen charquitos alrededor (%d)'%r[1])
    ok(r[2]==0, '🏰 y ninguno debajo del segundo piso del castillo')
    r=await ev("""(()=>{ const q=WX.pud.L[0]; player.pos.set(q.x,q.y,q.z); player.vel.set(3,0,0); player.grounded=true; WX.pud.spT=0; let s=0; const _s=splashBurst; splashBurst=(...a)=>{ s++; return _s(...a); }; wxPudTick(.05); splashBurst=_s; return s; })()""")
    ok(r>=1, '💦 al pasar corriendo por un charquito salpica')
    # F) la isla con nieve
    r=await ev("""(()=>{ weatherOfSlot=k=>'snow'; const g=groundAt(0,30,1); player.pos.set(0,g,30); player.vel.set(0,0,0); player.grounded=true; for(let i=0;i<40;i++) __S(1,.5); for(let i=0;i<20;i++) __S(1,.1);
      scanActions(); const a=wxActions(); const l=[a&&a[0]&&a[0].label, a&&a[1]&&a[1].label]; a[1].run(); const sm=WX.sm.length; a[0].run(); const b2=wxThrowActions(); const lt=b2&&b2[0].label; b2[0].run(); const balls=WI2.balls.length; return [l, sm, lt, balls, +WX.s.toFixed(2)]; })()""")
    ok(r[0]==['❄️ Hacer bola de nieve','❄️ Hacer muñeco de nieve'], '⛄ en la isla con nieve: %s'%r[0])
    ok(r[1]==1 and r[2]=='❄️ Lanzar bola de nieve' and r[3]>=1, '❄️ se hace el muñeco y la bola se lanza como en la Isla Invierno')
    r=await ev("""(()=>{ const n0=WX.prints.L.length; for(let i=0;i<30;i++){ player.pos.x+=.1; player.pos.y=groundAt(player.pos.x,player.pos.z,player.pos.y+.3); player.grounded=true; wxPrintsTick(.05); } return [n0, WX.prints.L.length]; })()""")
    ok(r[1]>=5, '👣 al caminar en la nieve quedan huellas (%d)'%r[1])
    r=await ev("""(()=>{ weatherOfSlot=k=>'clear'; WX.s=0; WX.w=0; for(let i=0;i<10;i++) __S(1,.5); return [WX.sm.length, WXU.V[0].x]; })()""")
    ok(r[0]==0 and r[1]==0, '🌤️ sin nieve, el muñeco se derrite y todo vuelve a como estaba')
    ok(not errs, '🚫 sin errores (%s)'%errs[:3])
    await b.close()
asyncio.run(m())
