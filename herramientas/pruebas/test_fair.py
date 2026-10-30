import asyncio, re, sys
src0=open('test_real_mp.py').read()
exec(src0.split('async def open_game')[0])
STUB2=STUB2.replace("setScalar(s){return this.set(s,s,s)}}","setScalar(s){return this.set(s,s,s)} sub(v){this.x-=v.x;this.y-=v.y;this.z-=v.z;return this} normalize(){const l=this.length()||1;return this.multiplyScalar(1/l)} distanceTo(v){return Math.hypot(this.x-v.x,this.y-v.y,this.z-v.z)} divideScalar(s){return this.multiplyScalar(1/s)} dot(v){return this.x*v.x+this.y*v.y+this.z*v.z} applyMatrix4(){return this} applyQuaternion(){return this} negate(){return this.multiplyScalar(-1)} setLength(l){return this.normalize().multiplyScalar(l)}}")
src=open('/home/claude/mundo-peluche.html').read()
src=src.replace('const myStain=newStain();','const myStain=newStain(); window.__P=()=>player; window.__mp=()=>mp;')
src=src.replace('const MINIS=[];','const MINIS=[]; window.__MG={MINIS, get M(){return player.mg}, start:d=>startMini(d), input:(k,d)=>mgInput(k,d), coins:()=>coins, bW:(e,a,b,c)=>bW(e,a,b,c), acts:()=>{const a=mgActions(); return a&&a[0]&&a[0].label;}};')
page_html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+src
exec('async def open_game'+src0.split('async def open_game')[1].split('async def m():')[0])
which=sys.argv[1] if len(sys.argv)>1 else 'all'
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(); ctx=await b.new_context(viewport={"width":1000,"height":700})
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=page_html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=STUB2, content_type="application/javascript")
      else: await r.abort()
    await ctx.route("https://**/*", route)
    A,ea=await open_game(ctx,'Ana'); await A.evaluate("document.getElementById('mpCreate').click()"); await A.wait_for_timeout(500)
    await A.evaluate("document.activeElement&&document.activeElement.blur(); 1")
    # placa: pararse y ver el botón
    for i,name in enumerate(['canasta','bateo','baile','topos','hockey','rueda']):
      lab=await A.evaluate(f"(()=>{{const d=__MG.MINIS[{i}]; const pd=d.pads[0]; const p=__MG.bW(d.e,pd[0],0,pd[1]); __P().pos.set(p.x,0,p.z); return 1;}})()")
      await A.wait_for_timeout(250); print('placa', name, '→', await A.evaluate("__MG.acts()"))
    if which in ('all','canasta'):
      await A.evaluate("__MG.start(__MG.MINIS[0])")
      shots=0
      for _ in range(4000):
        st=await A.evaluate("(()=>{const M=__MG.M; if(!M||M.over) return null; const p=.5+.5*Math.sin(M.t*2.7); return [p, M.data.time];})()")
        if not st: break
        if abs(st[0]-.62)<.04: await A.evaluate("__MG.input('shoot',true)"); shots+=1; await A.wait_for_timeout(500)
        else: await A.wait_for_timeout(25)
      await A.wait_for_timeout(1500)
      print('tiros', shots, await A.evaluate("JSON.stringify(__MG.M&&{d:__MG.M.data,over:__MG.M.over})"))
      print('canasta:', await A.text_content('#mgResText'), '| monedas', await A.evaluate("__MG.coins()"))
      await A.evaluate("document.getElementById('mgDone').click()")
    if which in ('all','bateo'):
      await A.evaluate("__MG.start(__MG.MINIS[1])")
      for _ in range(1200):
        st=await A.evaluate("(()=>{const M=__MG.M; if(!M||M.over) return null; const b=M.data.ball; return b&&!b.hit?[b.p.z,b.v.z]:0;})()")
        if st is None: break
        if st and st[0]<.25-st[1]*0.13 and st[0]>0: await A.evaluate("__MG.input('swing',true)"); await A.wait_for_timeout(300)
        else: await A.wait_for_timeout(15)
      await A.wait_for_timeout(800)
      print('bateo:', await A.text_content('#mgResText'), '| monedas', await A.evaluate("__MG.coins()"))
      await A.evaluate("document.getElementById('mgDone').click()")
    if which in ('all','baile'):
      await A.evaluate("""(()=>{ __MG.start(__MG.MINIS[2]); const M=__MG.M; const go=()=>{ if(!__MG.M||__MG.M.over) return; const T=M.t; for(const n of M.data.notes) if(!n.done && Math.abs(n.t-T)<.03) __MG.input(n.lane,true); requestAnimationFrame(go); }; go(); })()""")
      await A.wait_for_timeout(36500)
      print('baile:', await A.text_content('#mgResText'), '| monedas', await A.evaluate("__MG.coins()"))
      await A.evaluate("document.getElementById('mgDone').click()")
    if which in ('all','topos'):
      await A.evaluate("""(()=>{ __MG.start(__MG.MINIS[3]); const iv=setInterval(()=>{ const M=__MG.M; if(!M||M.over){ clearInterval(iv); return; } for(let k=0;k<9;k++) __MG.input(k,true); },350); })()""")
      await A.wait_for_timeout(32000)
      print('topos:', await A.text_content('#mgResText'), '| monedas', await A.evaluate("__MG.coins()"))
      await A.evaluate("document.getElementById('mgDone').click()")
    print('errores:', ea[:4] or 'ninguno'); await b.close()
asyncio.run(m())
