# v226 (Modo libre): 13 cosas nuevas — balón de básquet y canasta, portería, campana, globo de agua, banda transportadora,
# teletransportador, catapulta, molino, piano de piso, caja sorpresa con pollito, saco de boxeo y máquina de burbujas
# (tamaño, forma y color; la gigante te mete adentro y te eleva; sales con «Reventar burbuja» o «Tirarse»).
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); } };
  window.__CLR=()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); FREE.hold=null; freeSelect(null); freeBubClear(); FREE.soft=0; FREE.fling=null; };
  window.__AT=(x,z)=>{ player.pos.set(FREE.X+x,FREE.Y+.05,FREE.Z+z); player.vel.set(0,0,0); player.vy=0; player.facing=0; yaw=Math.PI; __S(2); };
  window.__ST=(id,x,z,r)=>freeAddStatic({k:'p',a:id,b:0},FREE.X+x,FREE.Y,FREE.Z+z,r||0);
  window.__TN=[]; { const o=freeTone; freeTone=function(f){ __TN.push(Math.round(f)); return o.apply(this,arguments); }; } 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True, device_scale_factor=2); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300)
    await ev("(()=>{ freeEnter(); return 1; })()"); await ev(STEP)
    r=await ev("(()=>{ __CLR(); const ids=['basket','agua','canasta','porteria','campana','banda','tele','catapulta','molino','piano','sorpresa','burbujas','saco']; const bad=ids.filter(id=>{ const m=freeMake({k:'p',a:id,b:0}); return !m || !m.children.length; }); return [bad, FREE_PHYS.filter(P=>!P.hid).length]; })()")
    ok(not r[0] and r[1]==37, 'las 13 cosas nuevas se arman; en «Física» hay %s'%r[1])
    # canasta y portería
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const c=__ST('canasta',0,0,0); const [hx,hz]=freeW(c,0,.3); const d=freeAddDyn('basket',hx,FREE.Y+4,hz); d.root.position.set(hx,FREE.Y+3.6,hz); d.v.set(0,0,0); __S(20); const can=(c.cT||0)>0;
      __CLR(); const g=__ST('porteria',0,0,0); const e=freeAddDyn('balon',FREE.X,FREE.Y,FREE.Z+4); __S(4); e.v.set(0,0,-9); __S(30); return [can, (g.gT||0)>0, +(e.root.position.z-FREE.Z).toFixed(2)]; })()""")
    ok(r[0] and r[1] and -1.05<r[2]<0, 'canasta: el balón que pasa por el aro hace «¡Canasta!»; portería: el balón entra, «¡Gol!» y se queda en la red (z %s)'%r[2])
    # campana, saco, sorpresa
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); __TN.length=0; const bl=__ST('campana',0,0,0); const [bx,bz]=freeW(bl,0,.2); const d=freeAddDyn('goma',bx,FREE.Y,bz-2); d.root.position.set(bx,FREE.Y+2,bz-2); d.v.set(0,1,8); __S(10); const ring=__TN.includes(1318);
      __CLR(); const s=__ST('saco',0,0,0); const e=freeAddDyn('boliche',FREE.X,FREE.Y,FREE.Z-3); e.root.position.y=FREE.Y+1.4; e.v.set(0,1,10); __S(8); const sw=Math.abs(s.baz||0)+Math.abs(s.bax||0);
      __CLR(); const q=__ST('sorpresa',0,0,0); __AT(-3,0); __S(2); const before=q.popT||0; __AT(-.9,0); __S(6); return [ring, +sw.toFixed(3), before, q.popT>0, q.root.userData.chick.visible]; })()""")
    ok(r[0] and r[1]>.01 and r[2]==0 and r[3] and r[4], 'campana: suena al pegarle una pelota; saco: se mece (%s); caja sorpresa: al acercarte sale el pollito %s'%(r[1],r[3:]))
    # banda, teletransportador, catapulta, molino
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const bd=__ST('banda',0,0,0); const d=freeAddDyn('caja',FREE.X,FREE.Y+.3,FREE.Z-1); __S(30); const box=+(d.root.position.z-FREE.Z+1).toFixed(2);
      player.pos.set(FREE.X,bd.box.max.y+.02,FREE.Z-1); player.vy=0; __S(10); const me=+(player.pos.z-FREE.Z+1).toFixed(2);
      __CLR(); const a=__ST('tele',0,0,0), c=__ST('tele',8,6,0); __AT(-3,-3); __AT(0,0); __S(2); const tp=[+(player.pos.x-FREE.X).toFixed(1), +(player.pos.z-FREE.Z).toFixed(1)];
      __CLR(); const k=__ST('catapulta',0,0,0); const [cx,cz]=freeW(k,0,.78); const ball=freeAddDyn('goma',cx,FREE.Y+.5,cz); __S(6); const [lx,lz]=freeW(k,.85,-.4); __AT(-3,-3); player.pos.set(lx,FREE.Y+.05,lz); __S(3); const fly=[+ball.v.y.toFixed(1), +(ball.root.position.y-FREE.Y).toFixed(1)];
      __CLR(); __ST('molino',0,0,0); const p0=[]; let moved=0; for(let i=0;i<20;i++){ player.pos.set(FREE.X+1.4,FREE.Y+.05,FREE.Z); player.vy=0; const x0=player.pos.x, z0=player.pos.z; __S(1); moved=Math.max(moved,Math.hypot(player.pos.x-x0,player.pos.z-z0)); }
      return [box, me, tp, fly, +moved.toFixed(2)]; })()""")
    ok(r[0]>1 and r[1]>.5, 'banda: lleva la caja (%s m) y a ti (%s m) hacia adelante'%(r[0],r[1]))
    ok(abs(r[2][0]-8)<.3 and abs(r[2][1]-6.9)<.3, 'teletransportador: entras por uno y sales junto al otro %s'%r[2])
    ok(r[3][0]>5 or r[3][1]>1.5, 'catapulta: al pisar la palanca avienta la pelota %s'%r[3])
    ok(r[4]>.03, 'molino: sus aspas te empujan (%s m en un cuadro)'%r[4])
    # piano
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const pn=__ST('piano',0,0,0); __TN.length=0; for(let x=-3.5;x<=3.5;x+=.5){ player.pos.set(FREE.X+x,FREE.Y+.05,FREE.Z); player.vy=0; __S(1); } return __TN.filter(f=>f>250 && f<530); })()""")
    ok(len(r)==8 and r==sorted(r), 'piano: caminando por encima suenan las 8 notas en orden %s'%r)
    # globo de agua
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const d=freeAddDyn('agua',FREE.X,FREE.Y,FREE.Z); __S(5); const quiet=FREE.dyn.includes(d); d.root.position.y=FREE.Y+6; d.v.set(0,-12,0); d.sleep=false; __S(14); return [quiet, FREE.dyn.includes(d)]; })()""")
    ok(r[0] and not r[1], 'globo de agua: puesto suavecito no se revienta; aventado contra el piso sí %s'%r)
    # máquina de burbujas
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const o=__ST('burbujas',0,0,0); __S(60); const small=BUB.L.length; __AT(0,-1.5); __S(1); const A=freeActions(), lab=A&&A[0]&&A[0].label; A[0].run(); const open=!ui('freeBubOv').hidden;
      const card=ui('freeBubOv').querySelector('.card'), btn=t=>[...card.querySelectorAll('button')].find(x=>x.textContent===t); btn('Gigante').click(); btn('Corazón').click(); btn('Morado').click(); btn('Listo').click(); const cfg=bubCfg(o);
      freeBubClear(); __AT(-10,-10); __S(100); const g=BUB.L.find(b=>b.giant), heart=g && g.m.geometry===bubGeo(2);
      const gp=g.m.position; player.pos.set(gp.x,gp.y-1.1,gp.z); __S(1); const inn=FREE.ride===g, y0=player.pos.y; __S(40); const rose=+(player.pos.y-y0).toFixed(1); const B=freeActions(), bl=B&&B[0]&&B[0].label;
      B[0].run(); const out=FREE.ride===null; let vmin=0; for(let i=0;i<60 && !player.grounded;i++){ __S(1); vmin=Math.min(vmin,player.vy); }
      __S(100); const g2=BUB.L.find(b=>b.giant); if(g2){ const q=g2.m.position; player.pos.set(q.x,q.y-1.1,q.z); __S(1); } const in2=!!FREE.ride; startDive(); const out2=!FREE.ride;
      freeSave(); const k=Object.keys(localStorage).find(k=>/libre|free/i.test(k) && localStorage.getItem(k).includes('burbujas')); const J=k?JSON.parse(localStorage.getItem(k)):null; const saved=J?(J.s||[]).find(e=>e[1]==='burbujas'):null;
      return [small, lab, open, cfg, heart, inn, rose, bl, out, +vmin.toFixed(1), in2, out2, saved&&saved[2]]; })()""")
    ok(r[0]>=3 and r[1]=='⚙️ Configurar burbujas' and r[2], 'burbujas: la máquina suelta burbujas (%s) y de cerca se configura'%r[0])
    ok(r[3]=={'size':3,'shape':2,'col':5} and r[4] and r[12]==3|(2<<2)|(5<<4), 'burbujas: tamaño gigante, corazón y morado (se guarda) %s'%r[3])
    ok(r[5] and r[6]>1 and r[7]=='🫧 Reventar burbuja' and r[8] and r[9]>=-4.6, 'burbuja gigante: te metes, te eleva (%s m), «Reventar burbuja» te saca y caes suavecito (vel. %s)'%(r[6],r[9]))
    ok(r[10] and r[11], 'burbuja gigante: «Tirarse» también te saca %s'%r[10:12])
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close(); await b.close()
asyncio.run(m())
