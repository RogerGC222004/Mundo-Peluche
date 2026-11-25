# v262: regalar cosas — en una sala, lo que tiras al piso lo ven todos y cualquiera lo puede recoger (sala simulada con BroadcastChannel).
# Ana tira 5 rubíes y su objeto; Beto los ve, los recoge y le llegan; Ana ya no los tiene en el piso. Lo que trae en la mano se ve.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
BUS = open('test_v215_amigos.py').read().split('BUS = """')[1].split('"""')[0]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); ctx=await b.new_context(viewport={"width":560,"height":320})
    await ctx.add_init_script("localStorage.setItem('mundoPelucheEnLinea','{\"on\":true,\"tip\":true}'); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'min', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await ctx.route("https://**/*", route)
    async def open_game(name):
      pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); await pg.add_init_script(BUS)
      await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
      await pg.evaluate("n=>__T.ev(`profile.name=${JSON.stringify(n)}; window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateRemotes(.05,t); } sendPresence(true); }; 1`)", name)
      return pg, errs
    A,ea=await open_game('Ana'); B,eb=await open_game('Beto')
    ev=lambda P,s: asyncio.wait_for(P.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    async def sync(n=10):
      for i in range(n):
        await ev(A,"__S(2); 1"); await A.wait_for_timeout(40); await ev(B,"__S(2); 1"); await B.wait_for_timeout(40)
    # los dos comparten el almacenamiento en la prueba: cada uno arranca con su inventario en memoria
    await ev(A,"joinRoom('REGALO',false); 1"); await A.wait_for_timeout(800); await ev(B,"joinRoom('REGALO',false); 1"); await B.wait_for_timeout(800)
    for P,dx in ((A,0),(B,3)): await ev(P,"player.pos.set(START.x+%d,START.top+.05,START.z+8); player.vel.set(0,0,0); 1"%dx)
    await sync(6)
    r=await ev(A,"[mp.remotes.size, [...mp.remotes.values()].map(r=>r.name)]"); ok(r[0]==1 and r[1]==['Beto'], 'Ana ve a Beto en la sala %s'%r)
    # 1. Ana trae rubíes en la mano: Beto lo ve
    await ev(A,"invAdd('mi:rubi',8); const i=INV.findIndex(S=>S && S.k==='mi:rubi'); invMove(i,2); useSlot(2); 1"); await sync(4)
    r=await ev(B,"(()=>{ const r=[...mp.remotes.values()][0]; return [r.itK, !!(r.obj.userData.itH && r.obj.userData.itH.holder.visible)]; })()")
    ok(r==['mi:rubi',True], '1 Beto ve los rubíes en la mano de Ana %s'%r)
    # 2. Ana tira 5 rubíes y un objeto suyo cerca de Beto
    await ev(A,"""(()=>{ const L=obLoad(); L.push({id:'oana1', n:'Estrellita', ...obClean({pieza:'estrella', c1:3})}); obStore(L); obSyncInv(); invAdd('o:oana1',1);
      player.facing=Math.PI/2; invDrop(2,5); player.facing=-Math.PI/2; const j=INV.findIndex(S=>S && S.k==='o:oana1'); invDrop(j,1); return 1; })()""")
    await sync(6)
    r=await ev(B,"(()=>{ const r=[...mp.remotes.values()][0]; return [(r.drops||[]).map(d=>d.k+'*'+d.n), DR.vis.size, (r.drops||[]).some(d=>d.d && d.nm==='Estrellita')]; })()")
    ok(r[0]==['mi:rubi*5','o:oana1*1'] and r[1]>=2 and r[2], '2 Beto ve en el piso lo que tiró Ana (5 rubíes y «Estrellita») %s'%r)
    # 3. Beto camina hasta los rubíes: los pide, Ana los quita y a Beto le llegan
    await ev(B,"(()=>{ INV.fill(null); INV[0]={k:'map',n:1}; invChanged(); const r=[...mp.remotes.values()][0]; const d=r.drops.find(d=>d.k==='mi:rubi'); player.pos.set(d.x,d.y+.05,d.z); player.vel.set(0,0,0); return 1; })()")
    await sync(10)
    r=await ev(B,"[invCount('mi:rubi'), DR.claim, [...mp.remotes.values()][0].drops.map(d=>d.k)]")
    ra=await ev(A,"[DR.mine.map(d=>d.k), invCount('mi:rubi')]")
    ok(r[0]==5 and r[1] is None and r[2]==['o:oana1'] and ra[0]==['o:oana1'] and ra[1]==3, '3 Beto recoge los 5 rubíes de Ana (le llegan a su inventario; Ana ya no los tiene en el piso y le quedan 3) B=%s A=%s'%(r,ra))
    # 4. Beto recoge el objeto: le queda una copia en sus objetos y en su inventario
    await ev(B,"(()=>{ OB_CACHE=null; localStorage.setItem('mundoPelucheObjetos', JSON.stringify({v:1, list:[]})); obSyncInv(); const r=[...mp.remotes.values()][0]; const d=r.drops.find(d=>d.k==='o:oana1'); player.pos.set(d.x,d.y+.05,d.z); return 1; })()")
    await sync(10)
    r=await ev(B,"(()=>{ const L=obLoad(); const O=L.find(o=>o.n==='Estrellita'); return [!!O, O && INV.some(S=>S && S.k==='o:'+O.id), O && O.pieza, drAll().filter(e=>!e.own).length, [...mp.remotes.values()].map(r=>[r.name,(r.drops||[]).map(d=>d.k),!!r.goneAt])]; })()")
    ra=await ev(A,"[DR.mine.length, INV.some(S=>S && S.k==='o:oana1'), !!obById('oana1')]")
    ok(r[:4]==[True,True,'estrella',0] and r[4]==[['Ana',[],False]] and ra==[0,False,True], '4 Beto recoge «Estrellita»: le llega una copia (sus objetos e inventario); Ana ya no la trae pero conserva su diseño B=%s A=%s'%(r,ra))
    # 5. si Beto tiene el inventario lleno, no la pide
    await ev(A,"invAdd('fr:coco',2); const i=INV.findIndex(S=>S && S.k==='fr:coco'); invDrop(i,2); 1"); await sync(4)
    await ev(B,"(()=>{ for(let i=0;i<INV_N;i++) INV[i]={k:'mi:carbon',n:99}; INV[0]={k:'map',n:1}; invChanged(); const r=[...mp.remotes.values()][0]; const d=r.drops.find(d=>d.k==='fr:coco'); player.pos.set(d.x,d.y+.05,d.z); return 1; })()")
    await sync(6)
    r=await ev(B,"[invCount('fr:coco'), DR.claim, [...mp.remotes.values()][0].drops.map(d=>d.k)]")
    ok(r[0]==0 and r[1] is None and r[2]==['fr:coco'], '5 con el inventario lleno no se recoge (se queda en el piso) %s'%r)
    r=await ev(A,"mp.presBytes"); ok(r<3500, '6 la presencia cabe (%s bytes)'%r)
    ok(not ea and not eb, 'sin errores %s %s'%(ea[:3],eb[:3]))
    await b.close()
asyncio.run(m())
