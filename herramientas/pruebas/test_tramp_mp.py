import asyncio, re, sys, json
exec(open('test_book_mp.py').read().split('async def m():')[0])
page_html=page_html.replace("function frame(){","window.__TR={TR, trZip, trDoor, P:()=>player, trClimb, rem:()=>[...mp.remotes.values()].map(r=>[r.name,r.tz])}; function frame(){",1)
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
    await A.evaluate("__TR.trZip(false)"); await B.wait_for_timeout(5000)
    print('B: red abierta?', await B.evaluate("__TR.TR.open"), await B.evaluate("JSON.stringify(__TR.rem())"))
    await B.evaluate("__TR.trZip(true)"); await A.wait_for_timeout(5000)
    print('A: red abierta?', await A.evaluate("__TR.TR.open"))
    print('errores', ea[:3], eb[:3]); await b.close()
asyncio.run(m())
