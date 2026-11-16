# v201 parte 3: botón Gestos + ruedita, atajo del botón Saludar, y las secciones Gestos / Globos de pintura en la tienda.
import asyncio, sys
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":844,"height":390},has_touch=True); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("""if(!sessionStorage.getItem('ya')){ sessionStorage.setItem('ya','1'); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1'); localStorage.setItem('mundoPelucheMonedas','2000');
      localStorage.setItem('mundoPelucheRopa', JSON.stringify({own:['go_roja'],eq:{hat:'go_roja'}})); }""")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(800)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t)
    r=await ev("[wardrobe.gest.join(','), wardrobe.pint.join(','), gestAtajo(), SHOP.filter(i=>i.cat==='gestos').length, SHOP.filter(i=>i.cat==='pinturas').length, SHOP_BY.ge_baile.price, SHOP_BY.gp_estrella.free]")
    ok(r[0]=='saludar,sentarse' and r[1]=='estrella' and r[2]=='saludar','de inicio: Saludar y Sentarse en la ruedita, globo de estrella, atajo = Saludar %s'%r[:3])
    ok(r[3]==13 and r[4]==20,'13 gestos y 20 globos en la tienda (%s, %s); bailecito cuesta %s'%(r[3],r[4],r[5]))
    # empezar a jugar (como jugador real)
    await ev("startGame(); 1"); await pg.wait_for_timeout(1500)
    r=await ev("[state, !!ui('tGest'), ui('tGest').getBoundingClientRect().width>0]"); ok(r[0]=='play' and r[2],'el botón Gestos está en pantalla %s'%r)
    bx=await pg.evaluate("(()=>{ const r=document.getElementById('tGest').getBoundingClientRect(); return [r.x+r.width/2, r.y+r.height/2]; })()")
    await pg.touchscreen.tap(bx[0],bx[1]); await pg.wait_for_timeout(300)
    r=await ev("[GW.open, GW.level, GW.items.map(i=>i.label).join(',')]"); ok(r[0] and r[1]=='root' and r[2]=='Gestos,Pinturas','tocar Gestos abre la ruedita con Gestos y Pinturas %s'%r)
    await pg.screenshot(path=OUT+'/rueda_1.png')
    # tocar la mitad de Gestos (arriba)
    g=await ev("GW.geo"); await pg.touchscreen.tap(g['cx'], g['cy']-(g['r0']+g['r1'])/2); await pg.wait_for_timeout(300)
    r=await ev("[GW.level, GW.items.map(i=>i.label).join(',')]"); ok(r[0]=='gest' and r[1]=='Saludar','luego salen tus gestos (el frijolito no ve Sentarse) %s'%r)
    await pg.screenshot(path=OUT+'/rueda_2.png')
    await pg.touchscreen.tap(g['cx'], g['cy']); await pg.wait_for_timeout(200); r=await ev("[GW.open, GW.level]"); ok(r==[True,'root'],'el centro (Atrás) regresa %s'%r)
    await pg.touchscreen.tap(g['cx'], g['cy']); await pg.wait_for_timeout(200); r=await ev("GW.open"); ok(r==False,'el centro (✕) cierra')
    # escoger Saludar desde la ruedita
    await ev("gwOpen(); GW.level='gest'; gwRender(); 1"); g=await ev("GW.geo"); await pg.touchscreen.tap(g['cx'], g['cy']-(g['r0']+g['r1'])/2); await pg.wait_for_timeout(200)
    r=await ev("[GW.open, player.waveUntil>0, mp.waveStamp>0]"); ok(r==[False,True,True],'tocar Saludar en la ruedita saluda y cierra %s'%r)
    # comprar bailecito y 4 globos: entran solos a la ruedita (hasta 5)
    await ev("['ge_baile','ge_robot','gp_flor','gp_luna','gp_dino','gp_rayo','gp_pez'].forEach(id=>{ coins-=SHOP_BY[id].price; grantItem(SHOP_BY[id]); }); 1")
    r=await ev("[wardrobe.gest.join(','), wardrobe.pint.join(','), wardrobe.own.length]"); ok(r[0]=='saludar,sentarse,baile,robot' and r[1]=='estrella,flor,luna,dino,rayo','lo comprado entra a la ruedita, máximo 5 %s'%r[:2])
    await ev("gwOpen(); GW.level='pint'; gwRender(); 1"); await pg.wait_for_timeout(200); await pg.screenshot(path=OUT+'/rueda_3.png'); await ev("gwClose(); 1")
    # en la tienda: quitar y poner; atajo
    await ev("openShop(); shopCat='gestos'; renderShop(); 1"); await pg.wait_for_timeout(600)
    r=await ev("[!document.getElementById('shopAtajo').hidden, [...document.querySelectorAll('#shopAtajo button')].map(b=>b.textContent).join(',')]"); ok(r[0] and r[1]=='Saludar,Bailecito feliz,Baile robot','fila del atajo con tus gestos %s'%r)
    await pg.screenshot(path=OUT+'/tienda_gestos.png')
    await ev("[...document.querySelectorAll('#shopAtajo button')].find(b=>b.dataset.g==='baile').click(); 1"); r=await ev("[gestAtajo(), ui('tWave').dataset.lbl]"); ok(r==['baile','Bailecito'],'atajo cambiado a Bailecito %s'%r)
    await ev("shopPick(SHOP_BY.ge_robot); 1"); r=await ev("wardrobe.gest.join(',')"); ok(r=='saludar,sentarse,baile','tocar uno puesto lo quita %s'%r)
    await ev("shopCat='pinturas'; renderShop(); 1"); await pg.wait_for_timeout(600); await pg.screenshot(path=OUT+'/tienda_pinturas.png')
    await ev("shopPick(SHOP_BY.gp_pez); 1"); r=await ev("wardrobe.pint.length"); ok(r==5,'con 5 globos no deja poner otro %s'%r)
    await ev("saveWardrobe(); closeShop(); 1"); await pg.reload(); await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(800)
    r=await ev("[wardrobe.gest.join(','), wardrobe.pint.join(','), JSON.stringify(wardrobe.atajo)]"); ok(r==['saludar,sentarse,baile','estrella,flor,luna,dino,rayo','{"f":"baile"}'],'se guarda al volver a abrir %s'%r)
    # Chibi: atajo por defecto Sentarse; su ruedita no muestra Sacar la lengua
    r=await ev("(()=>{ wardrobe.eq.body='av_chibi'; applyOutfit(plush,wardrobe.eq); return [gestAtajo(), ui('tWave').dataset.lbl, gwItems('gest').map(i=>i.gest).join(',')]; })()"); ok(r==['sentarse','Sentarse','saludar,sentarse,baile'],'con el Chibi: atajo Sentarse, y su ruedita sí tiene Sentarse %s'%r)
    r=await ev("LAYOUT_ITEMS.some(x=>x[0]==='tGest')"); ok(r,'el botón está en el editor de botones')
    print('errores', errs[:3]); await b.close()
asyncio.run(m())
