import asyncio, re, sys, json
exec(open('test_book_mp.py').read().split('async def m():')[0])
page_html=page_html.replace("function pierFallback(){","window.__PI={PIER, pW, CU, P:()=>player, setDoor:pierDoor, takeBucket, startFishing, rem:()=>[...mp.remotes.values()].map(r=>[r.name, r.pz, !!(r.pzBucket&&r.pzBucket.visible), r.pzHand&&r.pzHand.id]), rodPos:i=>PIER.rods[i].pos.toArray().map(v=>+v.toFixed(1)), feedCuco}; function pierFallback(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); ctx=await b.new_context(viewport={"width":500,"height":300}); await ctx.add_init_script("window.__NOR=true;")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=page_html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await ctx.route("https://**/*", route)
    A,ea=await open_game(ctx,'Ana'); await A.evaluate("document.getElementById('mpCreate').click()"); await A.wait_for_timeout(500)
    code=re.search(r'Código (\w{6})', await A.text_content('#roomDiag')).group(1)
    B,eb=await open_game(ctx,'Beto'); await B.wait_for_selector('#mpCode',state='visible',timeout=120000); await B.fill('#mpCode',code,timeout=120000); await B.evaluate("document.getElementById('mpJoin').click()"); await B.wait_for_timeout(2500)
    for X in (A,B): await X.evaluate("(()=>{ const [x,z]=__PI.pW(0,40); __PI.P().pos.set(x,__PI.PIER.Y,z); })()")
    await A.evaluate("__PI.takeBucket(__PI.PIER.buckets[0])"); await A.evaluate("__PI.P().hand=5")
    await A.evaluate("__PI.startFishing(__PI.PIER.rods[2])"); await A.evaluate("__PI.setDoor(true)")
    await B.wait_for_timeout(6000)
    print('B ve', await B.evaluate("JSON.stringify(__PI.rem())"), 'puerta B', await B.evaluate("__PI.PIER.door.open"), 'corcho 2 en B', await B.evaluate("JSON.stringify(__PI.rodPos(2))"), 'en A', await A.evaluate("JSON.stringify(__PI.rodPos(2))"))
    print('diag', await B.text_content('#roomDiag'))
    print('errores', ea[:3], eb[:3]); await b.close()
asyncio.run(m())
