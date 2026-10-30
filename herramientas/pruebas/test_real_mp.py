import asyncio
src=open('test_dive.py').read()
exec(src.split('async def m():')[0])
# Vestíbulo compartido entre ventanas (BroadcastChannel): cada ventana publica su presencia y recibe la de todas
BUS = """
(()=>{
  const me='p'+Math.random().toString(36).slice(2,8), bc=new BroadcastChannel('vestibulo'); const peers=new Map(); const hs=new Set();
  let mine={};
  const snap=()=>[...peers.entries()].map(([k,pr])=>({peer:k, sameTab:k===me, isMe:k===me, kind:'viewer', guest:false, by:null, presence:pr, updatedAt:Date.now()}));
  const emitAll=()=>{ const ps=snap(); hs.forEach(h=>h({peers:ps, joined:[], left:[], updated:[]})); };
  bc.onmessage=e=>{ const d=e.data; if(d.t==='p'){ peers.set(d.k,d.pr); emitAll(); } if(d.t==='hello'){ bc.postMessage({t:'p',k:me,pr:mine}); } };
  peers.set(me,mine);
  const room={ presence:async(patch)=>{ mine={...mine}; for(const k in patch){ if(patch[k]===null) delete mine[k]; else mine[k]=patch[k]; } peers.set(me,mine); bc.postMessage({t:'p',k:me,pr:mine}); emitAll(); },
    peers:()=>snap(), onPeers:(h)=>{ hs.add(h); setTimeout(()=>h({peers:snap(),joined:[],left:[],updated:[]})); return ()=>hs.delete(h); },
    connected:()=>true, onConnection:(h)=>{ setTimeout(()=>h(true)); return ()=>{}; }, join:async()=>{ throw {code:'not_permitted'}; } };
  bc.postMessage({t:'hello'});
  window.claude={use:n=>Promise.resolve(n==='room'?room:null)};
})();
"""
async def open_game(ctx,name):
  pg=await ctx.new_page(); errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
  await pg.add_init_script(BUS)
  await pg.goto("https://test.local/"); await pg.wait_for_timeout(300)
  await pg.evaluate(f"document.getElementById('mpBtn').click()"); await pg.fill('#mpName', name)
  return pg, errs
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(); ctx=await b.new_context(viewport={"width":1000,"height":700})
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=page_html, content_type="text/html")
      elif "three" in r.request.url: await r.fulfill(body=STUB2, content_type="application/javascript")
      else: await r.abort()
    await ctx.route("https://**/*", route)
    A,ea=await open_game(ctx,'Ana'); await A.click('#mpCreate'); await A.wait_for_timeout(500)
    code=__import__('re').search(r'Código (\w{6})', await A.text_content('#roomDiag')).group(1); print("Ana creó la sala", code)
    B,eb=await open_game(ctx,'Beto'); await B.fill('#mpCode',code); await B.click('#mpJoin')
    C,ec=await open_game(ctx,'Caro'); await C.fill('#mpCode','ZZZ999'); await C.click('#mpJoin')
    await A.wait_for_timeout(5000)
    for pg,n in [(A,'Ana'),(B,'Beto'),(C,'Caro')]:
      await pg.keyboard.press('KeyP'); await pg.wait_for_timeout(150)
      print(f"  {n:5s} → {await pg.text_content('#roomLabel')}  |  {await pg.text_content('#roomDiag')}")
      await pg.click('#resumeBtn')
    # Beto camina; Ana debe ver que se mueve
    await B.keyboard.down('KeyW'); await B.wait_for_timeout(1500); await B.keyboard.up('KeyW'); await A.wait_for_timeout(500)
    print("errores:", (ea+eb+ec) or "ninguno")
    await b.close()
asyncio.run(m())
