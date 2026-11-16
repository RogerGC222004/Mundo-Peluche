# v201 parte 4: los gestos se mueven, se cancelan al caminar, van en la presencia y se ven en los demás.
import asyncio, sys
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":844,"height":390}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false}));")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(800)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t)
    run="(sec)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); update(.05,t); } }"
    await ev("window.__run="+run+"; startGame(); 1"); await pg.wait_for_timeout(1200); await ev("__run(1); 1")
    r=await ev("(()=>{ playGesture('baile'); __run(.6); const gs=plush.userData.gs; return [!!gs, gs&&gs.id, gestPresence(), plush.userData.arms[0].rotation.z.toFixed(2)]; })()")
    ok(r[0] and r[1]=='baile' and r[2] and r[2].startswith('3.'),'el bailecito empieza y va en la presencia %s'%r)
    r=await ev("(()=>{ const gs=plush.userData.gs; if(gs) gs.t0-=3.3; __run(.8); return [!!plush.userData.gs, scene.children.filter(c=>c.userData && c.userData.noBatch && c.type==='Group' && !c.children.length).length]; })()")
    ok(r[0]==False,'termina solo y quita sus adornos %s'%r)
    r=await ev("(()=>{ playGesture('comer'); __run(1); const a=!!plush.userData.gs; keys.KeyW=true; try{ __run(.6); }finally{ keys.KeyW=false; } return [a, !!plush.userData.gs]; })()")
    ok(r==[True,False],'caminar cancela el gesto %s'%r)
    r=await ev("(()=>{ player.swim=true; playGesture('aplaudir'); const g=!!plush.userData.gs; player.swim=false; return g; })()"); ok(r==False,'nadando no se puede')
    r=await ev("(()=>{ __run(.5); playGesture('lengua'); return !!plush.userData.gs; })()"); ok(r==False,'sacar la lengua todavía no (va en la parte 5)')
    # otro jugador
    r=await ev("(()=>{ const rr=makeRemote(1,'Ana'); gestParse(rr,{ge:'4.555'}); const a=rr.obj.userData.gs&&rr.obj.userData.gs.id; gestParse(rr,{ge:'4.555'}); const same=rr.obj.userData.gs.t0; gestParse(rr,{ge:'9.777'}); const b=rr.obj.userData.gs.id; gestParse(rr,{ge:'abc'}); return [a,b,!!same]; })()")
    ok(r==['aplaudir','pensar',True],'se ve el gesto de otro jugador (y no se repite con la misma presencia) %s'%r)
    r=await ev("(()=>{ wardrobe.eq.body='av_chibi'; applyOutfit(plush,wardrobe.eq); __run(.2); wave(); const a=plush.userData.av==='c' && player.sitF; wave(); playGesture('saludar'); __run(.5); const s=plush.userData.gs&&plush.userData.gs.id; return [a,s]; })()")
    ok(r==[True,'saludar'],'Chibi: el atajo la sienta; Saludar ahora sí mueve el brazo %s'%r)
    r=await ev("[SHOP_BY.ge_baile.price, SHOP_BY.gp_flor.price, SHOP_BY.ge_pensar.price, SHOP_BY.gp_dino.price]"); ok(r==[300,150,180,210],'precios ×3: %s'%r)
    print('errores', errs[:3]); await b.close()
asyncio.run(m())
