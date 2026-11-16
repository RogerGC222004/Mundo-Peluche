# v202: tienda más rápida y con vistas previas.
# - Lo que compras con «Me alcanza» prendido ya no desaparece de la lista.
# - Al tocar, solo cambian las tarjetas (no se rehace la lista) y la lista no brinca hasta arriba.
# - Gestos: tu peluche hace el gesto en la tienda (también sentarse con el Chibi y la lengua con el frijolito).
# - Globos de pintura: pared con el globo que vuela y deja su mancha; tocar la pared lanza otro (máx. 6 manchas).
# - Pantallas de carga: póster en la pared; al tocarlo se ve a pantalla completa.
# - Teléfono acostado: la tienda cabe en la pantalla y la lista usa el alto que queda.
import asyncio, sys
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("""localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');
      localStorage.setItem('mundoPelucheRopa', JSON.stringify({own:['ge_saludar','ge_sentarse'],eq:{},gest:['saludar','sentarse'],pint:[]}));""")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    await ev("""window.__run=(sec)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); update(.05,t); renderStudio(.05); } }; 1""")
    await ev("coins=5000; openShop(); shopCat='gestos'; renderShop(); 1"); await pg.wait_for_timeout(800); await ev("(window.requestAnimationFrame=()=>0, 1)")
    # 1. la tienda cabe en el teléfono acostado y la lista usa el alto
    r=await ev("""(()=>{ const c=document.querySelector('.shop-card').getBoundingClientRect(), g=document.getElementById('shopGrid'), ov=document.getElementById('shop'), cols=getComputedStyle(g).gridTemplateColumns.split(' ').length;
      return [Math.round(c.top), Math.round(c.bottom), innerHeight, Math.round(g.getBoundingClientRect().height), cols, ov.scrollHeight<=ov.clientHeight+1]; })()""")
    ok(r[0]>=0 and r[1]<=r[2] and r[3]>=170 and r[4]>=4 and r[5], 'la tienda cabe en la pantalla (%s a %s de %s), la lista mide %s px con %s columnas y solo ella se desliza'%tuple(r[:5]))
    # 2. tocar no rehace la lista y no la sube hasta arriba
    r=await ev("""(()=>{ const g=document.getElementById('shopGrid'); g.scrollTop=120; const top0=g.scrollTop, first=g.firstElementChild; const it=SHOP.find(i=>i.cat==='gestos' && !owns(i) && i.gest==='baile');
      const t0=performance.now(); shopPick(it); const ms=performance.now()-t0; return [g.firstElementChild===first, g.scrollTop===top0, top0>0, !!document.querySelector('#shopGrid .shop-item.try'), +ms.toFixed(1)]; })()""")
    ok(r[0] and r[1] and r[2] and r[3], 'al tocar solo cambia la tarjeta (misma lista, no brinca) %s ms'%r[4])
    # 3. gesto en la tienda: el peluche lo hace y no se cancela; los letreros van en el estudio
    r=await ev("""(()=>{ const gs=plush.userData.gs; const a=[gs&&gs.id, gs&&gs.fx.parent===studio]; __run(1); const b=plush.userData.gs; return [...a, !!b && !b.kill, plush.parent===studio]; })()""")
    ok(r==['baile',True,True,True], 'tocar Bailecito: tu peluche baila en la tienda %s'%r)
    r=await ev("""(()=>{ __run(4); const a=!plush.userData.gs; shopPick(SHOP_BY.ge_lengua); __run(1.2); const tg=plush.userData.tg, b=[!!tg && tg.want===1, tg && tg.e>.5]; __run(4); const c=!plush.userData.tg || !plush.userData.tg.want; return [a,...b,c]; })()""")
    ok(r==[True,True,True,True], 'el gesto termina solo; Sacar la lengua: sale y se guarda sola %s'%r)
    r=await ev("""(()=>{ const g=document.getElementById('stTip'); return [g.hidden, g.textContent]; })()""")
    ok(r[0] is False and 'otra vez' in r[1], 'letrerito del escenario: %s'%r[1])
    # 4. comprar con «Me alcanza» prendido: se queda en la lista y dice que ya está en tu ruedita
    r=await ev("""(()=>{ shopF.afford=true; renderShop(); const it=SHOP_BY.ge_baile; shopPick(it); const top=document.getElementById('shopGrid').scrollTop; document.getElementById('shopBuyBtn').click();
      const card=[...document.querySelectorAll('#shopGrid .shop-item')].find(b=>b.querySelector('.nm').textContent===it.name); return [!!card, card&&card.querySelector('.st').textContent, owns(it), document.getElementById('shopBuy').hidden]; })()""")
    ok(r[0] and 'ruedita' in r[1] and r[2] and r[3], 'comprado con «Me alcanza»: sigue en la lista %s'%r)
    await ev("shopF.afford=false; 1")
    # 5. Chibi: Sentarse se ve sentado
    r=await ev("""(()=>{ wardrobe.own.push('av_chibi'); shopPick(SHOP_BY.av_chibi); shopCat='gestos'; renderShop(); shopPick(SHOP_BY.ge_sentarse); __run(1); const k=player.sitK; __run(3.5); return [plush.userData.av, +k.toFixed(2), +player.sitK.toFixed(2)]; })()""")
    ok(r[0]=='c' and r[1]>.8 and r[2]<.2, 'Chibi: Sentarse en la tienda la sienta y luego se para %s'%r)
    await ev("delete wardrobe.eq.body; applyOutfit(plush, wardrobe.eq); 1")
    # 6. globos: pared, vuelo y mancha; tocar la pared lanza otro; máximo 6
    r=await ev("""(()=>{ shopCat='pinturas'; renderShop(); __run(.1); const a=[SW.mode, plush.visible, SW.g.visible, SW.posterG.visible]; shopPick(SHOP_BY.gp_flor); const f=SW.fly.length; __run(1); const n=SW.splats.length;
      for(let i=0;i<8;i++){ stageTap(); __run(1); } return [...a, f, n, SW.splats.length, shopTry&&shopTry.id]; })()""")
    ok(r==['paint',False,True,False,1,1,6,'gp_flor'], 'globos: pared en lugar del peluche, el globo vuela y deja su mancha; tocar la pared lanza otro (máx. 6) %s'%r)
    try: await pg.screenshot(path='/tmp/v202_pared.png', timeout=90000)
    except Exception as e: print('(sin foto)', str(e)[:60])
    r=await ev("""(()=>{ stView.yaw=5; stView.dist=.2; studioZoom(1); __run(.1); return [+stView.yaw.toFixed(2), +stView.dist.toFixed(2)]; })()""")
    ok(r[0]<=1.25 and r[1]>=1.25, 'la pared se gira hasta un límite y te acercas hasta 1.25 m %s'%r)
    # 7. pantallas de carga: póster; al tocarlo, pantalla completa
    r=await ev("""(()=>{ shopCat='pcarga'; renderShop(); __run(.1); const a=[SW.mode, SW.posterG.visible, SW.posterId]; shopPick(SHOP_BY.lc_playa); const b=[SW.posterId, !!SW.tex.playa, !document.getElementById('lscrPrev')]; stageTap(); const c=!!document.getElementById('lscrPrev'); document.getElementById('lscrPrev').click(); return [...a,...b,c]; })()""")
    ok(r==['poster',True,'normal','playa',True,True,True], 'pantallas de carga: póster en la pared (la tuya primero), cambia al tocar otra y al tocar el póster se ve completa %s'%r)
    # 8. al cerrar todo regresa
    r=await ev("""(()=>{ shopCat='gestos'; renderShop(); shopPick(SHOP_BY.ge_aplaudir); closeShop(); return [plush.visible, plush.parent===scene, !plush.userData.gs, SW.g.visible, document.getElementById('stTip').hidden]; })()""")
    ok(r==[True,True,True,False,True], 'al cerrar la tienda tu peluche regresa normal %s'%r)
    # 9. ropa: la tarjeta se marca al instante y el peluche se viste después (o al comprar/cerrar)
    r=await ev("""(()=>{ openShop(); shopCat='sudaderas'; renderShop(); const it=SHOP.filter(i=>i.cat==='sudaderas' && !owns(i))[0]; shopPick(it); const a=[!!document.querySelector('#shopGrid .shop-item.try'), plush.userData.outfit.top!==it.id]; shopFlush(); return [...a, plush.userData.outfit.top===it.id]; })()""")
    ok(r==[True,True,True], 'ropa: primero se marca la tarjeta y luego se viste el peluche %s'%r)
    ok(not errs,'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
