import asyncio, re, sys, json
exec(open('test_book_mp.py').read().split('async def m():')[0])
page_html=page_html.replace("function frame(){","window.__B={BL, blEnter, blExit, blActions, P:()=>player, touchHold, stick, rem:()=>[...mp.remotes.values()].map(r=>[r.name, r.bl?r.bl[0]:null, +r.pos.y.toFixed(1)]), st:i=>{ const b=BL[i]; return [+b.x.toFixed(1),+b.y.toFixed(1),+b.z.toFixed(1), b.pilot, !!b.remote]; }}; function frame(){",1)
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
    await A.evaluate("(()=>{ const b=__B.BL[2]; __B.P().pos.set(b.x+1,b.y,b.z); __B.blEnter(b); __B.touchHold.up=true; })()")
    await A.wait_for_timeout(6000); await A.evaluate("__B.touchHold.up=false; __B.stick.y=-1"); await A.wait_for_timeout(4000); await A.evaluate("__B.stick.y=0")
    await B.wait_for_timeout(3000)
    print('A globo', await A.evaluate("JSON.stringify(__B.st(2))"), 'B ve globo', await B.evaluate("JSON.stringify(__B.st(2))"), 'B ve a Ana', await B.evaluate("JSON.stringify(__B.rem())"))
    print('B puede subir al 2?', await B.evaluate("(()=>{ const b=__B.BL[2]; __B.P().pos.set(b.x+1,b.y,b.z); return JSON.stringify(__B.blActions()); })()"))
    await A.evaluate("__B.blExit()"); await A.wait_for_timeout(8000); await B.wait_for_timeout(1000)
    print('tras bajarse A', await A.evaluate("JSON.stringify(__B.st(2))"), 'B', await B.evaluate("JSON.stringify(__B.st(2))"), 'B ve a Ana', await B.evaluate("JSON.stringify(__B.rem())"))
    print('errores', ea[:3], eb[:3]); await b.close()
asyncio.run(m())
