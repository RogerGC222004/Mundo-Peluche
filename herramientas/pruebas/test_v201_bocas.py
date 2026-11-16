# v201 parte 2: boquita hundida del Frijolito (forma compartida + sombrita del pliegue) y bocas abiertas 3D del Chibi.
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
    r=await ev("(()=>{ const a=makePlush(0), b=makePlush(2); return [a.userData.body.geometry===b.userData.body.geometry, a.userData.body.geometry.attributes.position.count, a.userData.crease.visible, a.userData.crease.parent===a.userData.body]; })()")
    ok(r[0] and r[2] and r[3],'frijolitos comparten la forma con boquita (%d puntos) y llevan su sombrita'%r[1])
    r=await ev("(()=>{ const o=makePlush(0), u=o.userData; applyOutfit(o,{body:'av_chibi'}); const c1=u.crease.visible; applyOutfit(o,{}); return [c1,u.crease.visible]; })()")
    ok(r==[False,True],'la sombrita se esconde en el Chibi y regresa en el frijolito: %s'%r)
    r=await ev("['bo_sorpresa','bo_risa','bo_dientes','bo2_abierta_roja','bo2_sorpresa_cafe','bo2_dientes_rosa','bo_sonrisa','bo_lengua','bo2_lengua_rosa','bo_beso',''].map(id=>chMouth3Kind(id && SHOP_BY[id] ? SHOP_BY[id].mo : null))")
    ok(r==['sorpresa','risa','dientes','risa','sorpresa','dientes',None,None,None,None,None],'qué bocas van en 3D: %s'%r)
    r=await ev("(()=>{ const o=makePlush(0), C=()=>o.userData.ch; const E={body:'av_chibi',cmouth:'bo_dientes'}; applyOutfit(o,E); const a=[C().m3Kind, !!C().m3, C().m3.children.length, C().skinned[1].geometry!==chGeos().head];"
                 +" applyOutfit(o,{...E,cmouth:'bo_sonrisa'}); const b=[C().m3Kind, !!C().m3, C().skinned[1].geometry===chGeos().head, C().skinned[1].material===C().skinned[0].material];"
                 +" applyOutfit(o,{...E,cmouth:'bo_risa',cskin:'cp_cacao'}); const c=[C().m3Kind, C().skinned[1].material!==C().skinned[0].material, C().g.children.filter(x=>x===C().m3).length]; return [a,b,c]; })()")
    ok(r[0]==['dientes',True,3,True],'con dientes: hueco, bolsita, lengua y dientes %s'%r[0])
    ok(r[1]==[None,False,True,True],'al cambiar a sonrisa se quita todo %s'%r[1])
    ok(r[2][0]=='risa' and r[2][1] and r[2][2]==1,'risa con otro tono de piel %s'%r[2])
    # que se dibuje sin errores en la escena del juego (frijolito y Chibi con boca 3D)
    r=await ev("(()=>{ const o=makePlush(0), q=makePlush(1); applyOutfit(q,{body:'av_chibi',cmouth:'bo_sorpresa'}); o.position.copy(player.pos); q.position.copy(player.pos).add(new THREE.Vector3(1,0,0)); scene.add(o,q); renderer.render(scene,camera); scene.remove(o,q); return renderer.info.render.calls>0; })()")
    ok(r,'se dibujan en la escena del juego')
    print('errores', errs[:3]); await b.close()
asyncio.run(m())
