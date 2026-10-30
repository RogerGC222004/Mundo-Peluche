import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
pre='<script>window.__off=0; const _dn=Date.now.bind(Date); Date.now=()=>_dn()+window.__off;</script>'
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+pre+open('/home/claude/mundo-peluche.html').read()
html=html.replace("function frame(){","window.__F={useSlot, FI, FI_TARGETS, BL, farm, FARM, P:()=>player, hook, stickTo, bowGo, blEnter, blExit, blActions, farmActions, farmBuy, farmPlant, farmWater, farmHarvest, farmGrow, fiActions, openFishOv, touchHold, stick, FI_BOUNCE, groundAt, get coins(){return coins}, set coins(v){coins=v;}, step:(n,fn)=>{ for(let i=0;i<n;i++){ window.__tt=(window.__tt||100)+.033; if(fn) fn(i); update(.033,window.__tt); } }}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    pg=await b.new_page(viewport={"width":800,"height":450}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheMonedas','200'); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false}))")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__F", timeout=120000); await pg.wait_for_timeout(1500)
    await pg.evaluate("document.getElementById('playBtn').click()"); await pg.wait_for_timeout(1500)
    r=await pg.evaluate("""(()=>{ const F=__F, P=F.P(), out=[];
      // 1) diana: pegar la flecha y subir
      const T=F.FI_TARGETS[0]; P.pos.set(T.c.x+T.n.x*12, F.groundAt(T.c.x+T.n.x*12,T.c.z+T.n.z*12,50), T.c.z+T.n.z*12); F.step(3);
      F.useSlot(1); F.step(2); F.hook.mode=1; F.stickTo({kind:'target', ref:T}, T.c.clone()); out.push(['acciones diana', F.hook.mode, F.hook.kind]);
      F.bowGo(); let k=0; F.step(200,()=>{ k++; }); out.push(['arriba de isla', T.I.id, +P.pos.y.toFixed(2), +T.I.y.toFixed(1), F.hook.mode, Math.hypot(P.pos.x-T.I.x,P.pos.z-T.I.z).toFixed(1)]);
      F.step(30); out.push(['sigue arriba', +P.pos.y.toFixed(2), P.grounded]);
      // 2) hongo que rebota
      const H=F.FI_BOUNCE[0]; P.pos.set(H.x,H.top+3,H.z); P.vy=-1; P.grounded=false; let maxVy=-99; F.step(40,()=>{ maxVy=Math.max(maxVy,P.vy); }); out.push(['rebote hongo vy max', +maxVy.toFixed(1)]);
      // 3) globo
      const B=F.BL[0]; P.pos.set(B.x+1,B.y,B.z); P.vy=0; P.grounded=true; F.step(2); out.push(['acción globo', JSON.stringify((F.blActions()||[])[0]&&F.blActions()[0].label)]);
      F.blEnter(B); const y0=B.y; F.touchHold.up=true; F.step(90); F.touchHold.up=false; const y1=B.y; F.stick.y=-1; const x0=B.x, z0=B.z; F.step(90); F.stick.y=0;
      out.push(['globo sube/avanza', +(y1-y0).toFixed(1), +Math.hypot(B.x-x0,B.z-z0).toFixed(1), +P.pos.y.toFixed(1), +B.y.toFixed(1), JSON.stringify(F.blActions()[0].label)]);
      F.touchHold.down=true; F.step(60); F.touchHold.down=false; out.push(['globo baja', +B.y.toFixed(1)]);
      F.blExit(); F.step(60); out.push(['bajó; globo solo', +B.y.toFixed(1), B.pilot, P.busy, P.balloon]);
      return out; })()""")
    for x in r: print(x)
    # 4) huerto
    r=await pg.evaluate("""(()=>{ const F=__F, P=F.P(), out=[], I=F.FARM.I;
      F.farmBuy({id:'rabano',seed:2,min:3}, 3); out.push(['semillas', JSON.stringify(F.farm.seeds), F.coins]);
      const V=F.FARM.plots[0]; P.pos.set(V.x+.3, V.y+.05, V.z+.3); P.vy=0; P.grounded=true; F.step(3);
      out.push(['acción parcela', JSON.stringify((F.fiActions()||[]).map(a=>a&&a.label))]);
      F.farmPlant(0,'rabano'); out.push(['plantado', JSON.stringify((F.fiActions()||[]).map(a=>a&&a.label))]);
      F.farmWater(0); out.push(['regado', JSON.stringify((F.fiActions()||[]).map(a=>a&&a.label))]);
      return out; })()""")
    for x in r: print(x)
    await pg.evaluate("window.__off+=4*60000"); await pg.wait_for_timeout(1500)
    r=await pg.evaluate("""(()=>{ const F=__F, out=[]; F.farmGrow(Date.now()); F.step(40); out.push(['tras 4 min', +F.farm.plots[0].g.toFixed(2), JSON.stringify((F.fiActions()||[]).map(a=>a&&a.label))]);
      F.farmHarvest(0); out.push(['cosecha', JSON.stringify(F.farm.crop)]);
      // sin regar: se pausa
      F.farmPlant(1,'rabano'); return out; })()""")
    for x in r: print(x)
    await pg.evaluate("window.__off+=10*60000"); 
    r=await pg.evaluate("""(()=>{ const F=__F, out=[]; F.farmGrow(Date.now()); out.push(['sin regar 10 min', +F.farm.plots[1].g.toFixed(2)]);
      const P=F.P(); P.pos.set(F.FARM.vx+1, F.FARM.I.top(F.FARM.vx,F.FARM.vz)+.05, F.FARM.vz+1); F.step(3); out.push(['junto a Fresita', JSON.stringify((F.fiActions()||[]).map(a=>a&&a.label))]);
      F.openFishOv('farm'); return out; })()""")
    for x in r: print(x)
    await pg.wait_for_timeout(600); await pg.screenshot(path='farm_ov.png', timeout=150000)
    await pg.evaluate("[...document.querySelectorAll('#fishBody .chip')][1].click()"); await pg.wait_for_timeout(300)
    print('vender', await pg.evaluate("[document.getElementById('fishSay').textContent, (document.querySelector('.fish-all')||{}).textContent]"))
    await pg.evaluate("document.querySelector('.fish-all').click()"); await pg.wait_for_timeout(300)
    print('monedas', await pg.evaluate("__F.coins"), 'guardado', await pg.evaluate("localStorage.getItem('mundoPelucheHuerto')"))
    print('errores', errs[:5]); await b.close()
asyncio.run(m())
