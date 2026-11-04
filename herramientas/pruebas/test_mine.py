import asyncio, sys, base64, io, json, os
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw
REAL=open('threerepo/build/three.min.js').read()
pre='<script>window.__off=0; const _dn=Date.now.bind(Date); Date.now=()=>_dn()+window.__off; const _raf=window.requestAnimationFrame.bind(window); window.requestAnimationFrame=f=>window.__stop?0:_raf(f);</script>'
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+pre+open(sys.argv[1] if len(sys.argv)>1 else '/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
SHOTS=os.environ.get('SHOTS','1')=='1'
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":480,"height":300}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'high', qDef:1, hints:false, weather:false, shadows:true}))")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=120000); await pg.wait_for_timeout(2000)
    await pg.evaluate("document.getElementById('playBtn').click()"); await pg.wait_for_timeout(1500)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    print('errores al cargar', errs[:3])
    await ev("(()=>{ const n=Date.now(); const cur=((n/1000)%DAY_LEN)/DAY_LEN; window.__off+=((0.2-cur)*DAY_LEN*1000); window.__stop=true; return 1; })()")
    await pg.wait_for_timeout(300)
    async def run(sec, keys=None):
      for i in range(int(sec/.05)):
        await ev("update(.05,performance.now()/1000)")
    shots=[]
    async def shot(lab):
      if not SHOTS: return
      d=await ev("(()=>{ updateSky(.05); caveUpdate(.016,performance.now()/1000); renderer.render(scene,camera); return canvas.toDataURL('image/png'); })()")
      im=Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB'); ImageDraw.Draw(im).text((4,4),lab,fill=(255,255,0)); shots.append(im)
    st=lambda: ev("JSON.stringify({p:[player.pos.x,player.pos.y,player.pos.z].map(v=>+v.toFixed(1)), inW:player.inWater, sw:player.swim, act:[document.getElementById('act1').hidden?'':document.getElementById('act1').textContent, document.getElementById('act2').hidden?'':document.getElementById('act2').textContent], cam:[camera.position.y.toFixed(1)], zone:MS.zone, mine:{pick:mine.pick, ores:mine.ores, open:mine.open}})")
    # afuera
    await ev("(()=>{ player.pos.set(ME.x+ME.ox*3.4, ME.y+1, ME.z+ME.oz*3.4); player.facing=Math.atan2(-ME.ox,-ME.oz); yaw=Math.atan2(ME.ox,ME.oz); return 1; })()"); await run(1.0)
    await ev("scanActions()"); print('afuera', await st()); await shot('entrada')
    await ev("(()=>{ yaw=Math.atan2(ME.ox,ME.oz)+1.2; return 1; })()"); await run(.5); await shot('entrada lado')
    await ev("(()=>{ player.pos.set(ME.x+ME.ox*1.4, ME.y+.5, ME.z+ME.oz*1.4); return 1; })()"); await run(.5); await ev("scanActions()"); print('en la boca', await st())
    # entrar
    await ev("caveEnter()"); await pg.wait_for_timeout(500); await run(1.5); await ev("scanActions()"); print('adentro', await st()); await shot('piso 1 entrada')
    # ir al cuarto central y mirar
    await ev("(()=>{ const h=CZ[0].R.hub; player.pos.set(h.x+CV.x+2,cvY(0)+.5,h.z+CV.z+2); return 1; })()"); await run(1.0); await shot('piso 1 centro')
    await ev("yaw+=1.6"); await run(.4); await shot('piso 1 centro 2')
    await ev("yaw+=1.6"); await run(.4); await shot('piso 1 centro 3')
    # picar una veta
    v=await ev("(()=>{ const v=CV_VEINS.find(v=>v.k===0); player.pos.set(v.sx,v.y,v.sz); yaw=Math.atan2(v.x-v.sx,v.z-v.sz)+.5; return v.id; })()"); await run(.8); await ev("scanActions()"); print('junto a veta', v, await st()); await shot('veta')
    for i in range(6):
      await ev("(()=>{ const a=mineActions(); if(a&&a[0]&&!a[0].disabled) a[0].run(); return 1; })()"); await run(.6)
    await ev("scanActions()"); print('tras picar', await st()); await shot('veta picada')
    # roca de la rampa sin pico
    await ev("(()=>{ const B=CV_ROCK[0]; const A=CZ[0].R.cout; const dx=B.x-(A.x+CV.x), dz=B.z-(A.z+CV.z), l=Math.hypot(dx,dz); player.pos.set(B.x-dx/l*3.1,cvY(0)+.5,B.z-dz/l*3.1); yaw=Math.atan2(-dx,-dz); return 1; })()"); await run(1); await ev("scanActions()"); print('roca sin pico', await st()); await shot('roca')
    await ev("(()=>{ mine.pick=1; return 1; })()")
    for i in range(6):
      await ev("(()=>{ const a=mineActions(); if(a&&a[0]&&!a[0].disabled) a[0].run(); return 1; })()"); await run(.6)
    await ev("scanActions()"); print('roca rota', await st())
    # bajar la rampa caminando
    await ev("(()=>{ const B=CZ[1].R.cin; window.__tg=[B.x+CV.x,B.z+CV.z]; return 1; })()")
    for i in range(80):
      await ev("(()=>{ const dx=__tg[0]-player.pos.x, dz=__tg[1]-player.pos.z, l=Math.hypot(dx,dz); if(l>1){ player.pos.x+=dx/l*.4; player.pos.z+=dz/l*.4; player.facing=Math.atan2(dx,dz); yaw=player.facing+Math.PI; } update(.05,performance.now()/1000); return 1; })()")
      if i==35: await shot("rampa")
      if i%10==0: print("  camino", await ev("[player.pos.x.toFixed(1),player.pos.y.toFixed(1),player.pos.z.toFixed(1), cvField(player.pos.x-CV.x,player.pos.z-CV.z,{}).d.toFixed(2)]"))
    print('abajo piso 2', await st()); await shot('piso 2')
    # elevador
    await ev("(()=>{ const E=CV_ELEV[1]; player.pos.set(E.x,E.y+.5,E.z); return 1; })()"); await run(.6); await ev("scanActions()"); print('elevador', await st()); await shot('elevador')
    await ev("openFishOv('elev')"); await pg.wait_for_timeout(200); print('elev ov', await pg.evaluate("[...document.querySelectorAll('#fishBody .fish-row')].map(r=>r.textContent)"))
    await ev("elevTo(0)"); await pg.wait_for_timeout(500); await run(1); print('tras elevador', await st())
    # salir
    await ev("(()=>{ player.pos.set(CV_EXIT.x,CV_EXIT.y+.3,CV_EXIT.z); return 1; })()"); await run(.5); await ev("scanActions()"); print('salida', await st()); await shot('salida')
    await ev("caveLeave()"); await pg.wait_for_timeout(500); await run(1.2); print('afuera otra vez', await st()); await shot('fuera')
    await ev("openFishOv('mine')"); await pg.wait_for_timeout(200); print('topo', await pg.evaluate("[document.getElementById('fishSay').textContent, ...[...document.querySelectorAll('#fishBody .fish-row')].map(r=>r.textContent)]"))
    print('errores', errs[:5])
    if shots:
      w,h=shots[0].size; cols=3; rows=(len(shots)+cols-1)//cols; c=Image.new('RGB',(w*cols,h*rows))
      for i,im in enumerate(shots): c.paste(im,((i%cols)*w,(i//cols)*h))
      c.save('mine_test.png')
    await b.close()
asyncio.run(m())
