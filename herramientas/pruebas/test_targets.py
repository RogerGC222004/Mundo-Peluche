import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read()
html=html.replace("function frame(){","window.__F={bowHeld, FI, FI_TARGETS, P:()=>player, hook, bowShoot, bowGo, useSlot, groundAt, terrainH, SEA_Y, camera, step:(n,fn)=>{ for(let i=0;i<n;i++){ window.__tt=(window.__tt||100)+.033; if(fn) fn(i); update(.033,window.__tt); } }}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    pg=await b.new_page(viewport={"width":400,"height":240}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("window.__NOR=true; localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false}))")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__F", timeout=120000); await pg.wait_for_timeout(1500)
    await pg.evaluate("document.getElementById('playBtn').click()"); await pg.wait_for_timeout(1500)
    n=await pg.evaluate("__F.FI_TARGETS.length")
    for i in range(n):
      r=await pg.evaluate("""(i=>{ const F=__F, P=F.P(), T=F.FI_TARGETS[i], I=T.I, hx=T.n.x, hz=T.n.z, hl=Math.hypot(hx,hz);
        // lugar para disparar: hacia afuera de la diana, en tierra seca, a unos 14-40 m
        let sx=0, sz=0, ok=false; for(let d=12; d<=60; d+=1){ const x=T.c.x+hx/hl*d, z=T.c.z+hz/hl*d; if(F.terrainH(x,z)>F.SEA_Y+.3){ sx=x; sz=z; ok=true; if(d>=14) break; } }
        if(!ok) return [I.id, 'sin lugar en tierra'];
        if(!F.bowHeld()) F.useSlot(1); P.pos.set(sx,F.groundAt(sx,sz,99),sz); P.vel.set(0,0,0); P.vy=0; P.grounded=true; F.hook.mode=0; F.step(4);
        // la cámara mira a la diana (como cuando apuntas con la mira)
        const C=F.camera; C.position.set(sx+(sx-T.c.x)*.06, P.pos.y+2.2, sz+(sz-T.c.z)*.06); C.lookAt(T.c); C.updateMatrixWorld(true);
        F.bowShoot(); let st=0; for(let k=0;k<120 && F.hook.mode===1;k++){ F.step(1); st++; }
        const hit=[F.hook.mode, F.hook.kind, F.hook.ref===T];
        if(F.hook.kind!=='target') return [I.id, i, 'NO PEGÓ', hit, 'dist', +Math.hypot(sx-T.c.x,P.pos.y+1.5-T.c.y,sz-T.c.z).toFixed(1)];
        F.bowGo(); F.step(260); const on=Math.hypot(P.pos.x-I.x,P.pos.z-I.z)<I.R && Math.abs(P.pos.y-I.top(P.pos.x,P.pos.z))<.3;
        return [I.id, i, 'pegó', 'arriba:', on, 'dist', +Math.hypot(sx-T.c.x,P.pos.y-T.c.y,sz-T.c.z).toFixed(1)]; })(%d)"""%i)
      print(r)
    print('errores', errs[:3]); await b.close()
asyncio.run(m())
