import asyncio, re, sys, json
exec(open('test_book_mp.py').read().split('async def m():')[0])
page_html=page_html.replace("function frame(){","window.__PE={pets, savePets, P:()=>player, myPet, rem:()=>[...mp.remotes.values()].map(r=>[r.name, r.pet?r.pet.id:null, r.pet?r.pet.name:null, r.pet?r.pet.P.root.visible:null, r.pet?+Math.hypot(r.pet.x-r.pos.x,r.pet.z-r.pos.z).toFixed(2):null]), pres:()=>JSON.stringify(petPresence()), bytes:()=>mp.presBytes}; function frame(){",1)
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
    await A.evaluate("(()=>{ __PE.pets.own=['pt_dragon','pt_gato']; __PE.pets.eq='pt_dragon'; __PE.pets.names={pt_dragon:'Chispitas'}; __PE.savePets(); })()")
    await B.wait_for_timeout(5000)
    print('A manda', await A.evaluate("__PE.pres()"), 'bytes', await A.evaluate("__PE.bytes()"))
    print('B ve', await B.evaluate("JSON.stringify(__PE.rem())"))
    await A.evaluate("(()=>{ __PE.pets.eq='pt_gato'; __PE.pets.names.pt_gato='Pelusa'; __PE.savePets(); })()"); await B.wait_for_timeout(5000)
    print('cambió', await B.evaluate("JSON.stringify(__PE.rem())"))
    await A.evaluate("(()=>{ __PE.pets.eq=''; __PE.savePets(); })()"); await B.wait_for_timeout(5000)
    print('sin mascota', await B.evaluate("JSON.stringify(__PE.rem())"))
    print('errores', ea[:3], eb[:3]); await b.close()
asyncio.run(m())
