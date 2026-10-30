import asyncio, json, sys
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read()
html=html.replace("function pierFallback(){","window.__PI={setDoor:pierDoor, go:()=>{ updateMyFishing(.0); let n=0; while(player.fish && player.fish.ph!=='bite' && n<800){ updateMyFishing(.05); n++; } if(!player.fish) return 'sin pesca'; const N=player.fish.N; for(let i=0;i<N;i++) reelFish(); for(let i=0;i<30;i++) updateMyFishing(.05); return n; }, PIER, pW, pL, FDEX, P:()=>player, CU, acts:()=>{ actKey=''; scanActions(); return [actA&&actA.label, actB&&actB.label]; }, run:k=>{ const a=k?actB:actA; if(a&&!a.disabled) a.run(); return a&&a.label; }, step:n=>{ for(let i=0;i<n;i++){ updateMyFishing(.05); updateFeed(.05); cucoFeedAnim(.05,i*.05); } }, bu:i=>PIER.buckets[i].items.slice(), cam:camera, show}; function pierFallback(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":720,"height":400}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console", lambda m: errs.append('console:'+m.text) if m.type in ('error','warning') else None)
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); 
    try: await pg.wait_for_function("window.__PI", timeout=120000)
    except Exception as e: print('NO CARGA', errs[:5]); await b.close(); return
    await pg.wait_for_timeout(2500)
    await pg.evaluate("document.getElementById('playBtn').click()"); await pg.wait_for_timeout(1500)
    print('rods', await pg.evaluate("JSON.stringify(__PI.PIER.rods.map(r=>[r.sd,+r.u.toFixed(1)]))"))
    # caminar desde la playa al muelle
    await pg.evaluate("(()=>{ const [x,z]=__PI.pW(0,-26); __PI.P().pos.set(x, 0.3, z); __PI.P().facing=__PI.PIER.th; })()"); await pg.wait_for_timeout(600); await pg.evaluate("(()=>{ window.__yawSet && 0; })()")
    await pg.keyboard.down('KeyW'); await pg.wait_for_timeout(5000); await pg.keyboard.up('KeyW')
    print('caminando', await pg.evaluate("JSON.stringify([__PI.pL(__PI.P().pos.x,__PI.P().pos.z).map(v=>+v.toFixed(1)), +__PI.P().pos.y.toFixed(2)])"))
    await pg.screenshot(timeout=120000, path='pier_walk.png')
    # junto a la primera caña
    await pg.evaluate("(()=>{ const r=__PI.PIER.rods[0]; const [x,z]=__PI.pW(...r.stand); __PI.P().pos.set(x, __PI.PIER.Y, z); })()"); await pg.wait_for_timeout(800)
    print('acciones caña', await pg.evaluate("JSON.stringify(__PI.acts())"))
    for k in range(5):
      await pg.evaluate("__PI.run(0)"); await pg.wait_for_timeout(200)
      print(' pesca', await pg.evaluate("__PI.go()"), await pg.evaluate("JSON.stringify([__PI.bu(0), document.getElementById('toast').textContent])"))
    await pg.screenshot(timeout=120000, path='pier_fish.png')
    # carnada pez pequeño -> mediano
    print('acciones', await pg.evaluate("JSON.stringify(__PI.acts())"))
    await pg.evaluate("__PI.run(1)"); print('carnada', await pg.evaluate("JSON.stringify(__PI.acts())"))
    await pg.evaluate("__PI.run(0)"); print(' go', await pg.evaluate("__PI.go()"))
    print('mediano', await pg.evaluate("JSON.stringify([__PI.bu(0), document.getElementById('toast').textContent])"))
    # tomar balde
    await pg.evaluate("(()=>{ const b=__PI.PIER.buckets[0]; __PI.P().pos.set(b.pos.x+.5, __PI.PIER.Y, b.pos.z); })()"); await pg.wait_for_timeout(600)
    print('junto al balde', await pg.evaluate("JSON.stringify(__PI.acts())"))
    await pg.evaluate("__PI.run(0)"); await pg.wait_for_timeout(600); print('cargando', await pg.evaluate("JSON.stringify([__PI.P().bucket, __PI.acts()])"))
    await pg.screenshot(timeout=120000, path='pier_carry.png')
    # sacar un pez
    await pg.evaluate("__PI.run(0)"); await pg.wait_for_timeout(500); print('ventana', await pg.evaluate("document.getElementById('fishTitle').textContent+' | '+document.getElementById('fishBody').innerText.slice(0,200)"))
    await pg.screenshot(timeout=120000, path='pier_bucketui.png')
    await pg.evaluate("document.querySelector('#fishBody .sbtn') && document.querySelector('#fishBody .sbtn').click()"); await pg.wait_for_timeout(500); print('en la mano', await pg.evaluate("__PI.P().hand"))
    # ir a la puerta
    await pg.evaluate("(()=>{ const [x,z]=__PI.pW(0,__PI.PIER.HZ-__PI.PIER.HH-1.6); __PI.P().pos.set(x, __PI.PIER.Y, z); __PI.P().facing=__PI.PIER.th; })()"); await pg.wait_for_timeout(700)
    print('puerta', await pg.evaluate("JSON.stringify(__PI.acts())"))
    await pg.evaluate("__PI.run(0)"); await pg.wait_for_timeout(2500); await pg.screenshot(timeout=120000, path='pier_door.png')
    print('abierta', await pg.evaluate("JSON.stringify([__PI.PIER.door.open, __PI.acts()])"))
    await pg.keyboard.down('KeyW'); await pg.wait_for_timeout(4000); await pg.keyboard.up('KeyW')
    print('adentro', await pg.evaluate("JSON.stringify(__PI.pL(__PI.P().pos.x,__PI.P().pos.z).map(v=>+v.toFixed(1)))"))
    await pg.screenshot(timeout=120000, path='pier_inside.png')
    await pg.evaluate("(()=>{ const [x,z]=__PI.pW(0,__PI.PIER.HZ+__PI.PIER.HH-2.8); __PI.P().pos.set(x, __PI.PIER.Y, z); __PI.P().facing=__PI.PIER.th; })()"); await pg.wait_for_timeout(1500)
    print('tortu', await pg.evaluate("JSON.stringify(__PI.acts())"))
    await pg.screenshot(timeout=120000, path='pier_tortu.png')
    await pg.evaluate("__PI.run(0)"); await pg.wait_for_timeout(800); print('tienda', await pg.evaluate("document.getElementById('fishSay').textContent"))
    await pg.screenshot(timeout=120000, path='pier_shop.png')
    await pg.evaluate("document.querySelector('#fishTabs [data-tab=dex]').click()"); await pg.wait_for_timeout(800); await pg.screenshot(timeout=120000, path='pier_dex.png')
    await pg.evaluate("document.querySelector('#fishTabs [data-tab=sell]').click()"); await pg.wait_for_timeout(300)
    print('monedas antes', await pg.evaluate("document.getElementById('coinN').textContent"))
    await pg.evaluate("document.querySelector('.fish-all') && document.querySelector('.fish-all').click()"); await pg.wait_for_timeout(500)
    print('monedas después', await pg.evaluate("document.getElementById('coinN').textContent"), await pg.evaluate("JSON.stringify([__PI.bu(0), __PI.P().hand])"))
    await pg.evaluate("document.getElementById('fishClose').click()")
    print('errores', errs[:8]); await b.close()
asyncio.run(m())
