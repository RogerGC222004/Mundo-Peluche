# v201: cara nueva del Chibi. Ojos de corazón retirados: se devuelven las monedas una sola vez y se ven ojos café;
# ojos de chico en la tienda; el cabello va pegadito con gorro y vuelve a su volumen sin gorro.
import asyncio, sys
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":844,"height":390}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("""if(!sessionStorage.getItem('ya')){ sessionStorage.setItem('ya','1');
      localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1'); localStorage.setItem('mundoPelucheMonedas','100');
      localStorage.setItem('mundoPelucheRopa', JSON.stringify({own:['co_corazones','co2_h_rojos','co_azul'],eq:{body:'av_chibi',ceyes:'co_corazones'}})); }""")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(1000)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t)
    r=await ev("[coins, wardrobe.own.join(','), wardrobe.eq.ceyes||'', !!SHOP_BY.co_corazones, !!SHOP_BY.co2_h_rojos, window.__eyeRefund]")
    ok(r[0]==128,'monedas devueltas: 100 + 14 + 14 = %s'%r[0]); ok(r[1]=='co_azul','ya no tiene ojos de corazón: %s'%r[1]); ok(r[2]=='','ya no los trae puestos'); ok(not r[3] and not r[4],'ya no están en la tienda')
    # otra vez (recargar): no se devuelve dos veces
    await ev("saveWardrobe(); 1"); await pg.reload(); await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(800)
    r=await ev("coins"); ok(r==128,'al volver a abrir no se devuelven otra vez: %s'%r)
    # alguien de una versión vieja con ojos de corazón: se le ven ojos café
    r=await ev("(()=>{ const o=makePlush(0); applyOutfit(o,{body:'av_chibi',ceyes:'co_corazones'}); const C=o.userData.ch; return [C.face.visible, Object.keys(CH_FACE_MAT).some(k=>k.startsWith('cafe|'))]; })()")
    ok(r[0] and r[1],'ojos de corazón de otro jugador → se ven café %s'%r)
    r=await ev("SHOP.filter(i=>i.id.startsWith('co3_ch_')).map(i=>i.price+(i.free?'g':''))"); ok(len(r)==5 and r[0]=='0g','5 ojos de chico (el café gratis): %s'%r)
    r=await ev("(()=>{ const o=makePlush(0); applyOutfit(o,{body:'av_chibi',chair:'hp_picudo',chat:'rg_gorra'}); const C=o.userData.ch, g1=C.hair.geometry; applyOutfit(o,{body:'av_chibi',chair:'hp_picudo'}); const g2=C.hair.geometry; return [g1===CH_HAIR.picudo.geo2ch, g2===CH_HAIR.picudo.geo2c, !!C.hairSh, !!C.hairUn, C.g.children.filter(m=>m===C.hairSh).length]; })()")
    ok(all(r[:4]) and r[4]==1,'cabello pegadito con gorra y normal sin gorra; sombrita y capa de abajo: %s'%r)
    r=await ev("(()=>{ const o=makePlush(0); applyOutfit(o,{body:'av_chibi',chair:'hp_coletas'}); applyOutfit(o,{body:'av_chibi',chair:'hp_largo'}); const C=o.userData.ch; return [C.g.children.filter(m=>m.material===CH_HAIR_SHMAT).length, (C.hairX||[]).length]; })()")
    ok(r[0]==1 and r[1]==0,'al cambiar de peinado no se quedan piezas viejas: %s'%r)
    r=await ev("(()=>{ const o=makePlush(0); applyOutfit(o,{body:'av_amigu',ahair:'hp_coletas'}); const A=o.userData.am; return [A.hair.geometry===CH_HAIR.coletas.geoa, A.hairX.some(p=>p.children.some(m=>m.geometry===CH_XG.sw))]; })()")
    ok(r[0] and not r[1],'el Amigurumi sigue con su cabello de antes: %s'%r)
    print('errores', errs[:3]); await b.close()
asyncio.run(m())
