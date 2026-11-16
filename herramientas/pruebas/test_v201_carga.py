# v201 parte 7: pantallas de carga: se compran en la tienda, se guardan y salen al abrir el juego (con el peluchito de tu color).
import asyncio, sys
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":844,"height":390}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("""if(!sessionStorage.getItem('ya')){ sessionStorage.setItem('ya','1'); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1'); localStorage.setItem('mundoPelucheMonedas','3000'); }""")
    slow={'on':False}
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url:
        if slow['on']: await asyncio.sleep(6)
        await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(800)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t)
    r=await ev("[SHOP.filter(i=>i.cat==='pcarga').length, SHOP_BY.lc_normal.free, SHOP_BY.lc_isla.price, SHOP_BY.lc_playa.price, Object.keys(window.LC_BG).length]")
    ok(r[0]==15 and r[1] and r[2]==150 and r[3]==120 and r[4]>=15,'15 pantallas en la tienda (clásica gratis; isla %s, playa %s)'%(r[2],r[3]))
    await ev("show('menu'); openShop(); shopCat='pcarga'; renderShop(); 1"); await pg.wait_for_timeout(1500)
    try: await pg.screenshot(path=OUT+'/tienda_carga.png', timeout=90000)
    except Exception as e: print('(sin foto)', str(e)[:60])
    r=await ev("(()=>{ shopPick(SHOP_BY.lc_isla); const prev=!!document.getElementById('lscrPrev'); document.getElementById('lscrPrev').click(); const gone=!document.getElementById('lscrPrev'); return [prev, gone, shopTry&&shopTry.id]; })()")
    ok(r==[True,True,'lc_isla'],'tocar una que no tienes: vista previa a pantalla completa (toca para cerrar) %s'%r)
    r=await ev("(()=>{ coins-=SHOP_BY.lc_isla.price; grantItem(SHOP_BY.lc_isla); profile.color=3; saveLoadPref(); return [wardrobe.carga, localStorage.getItem('mundoPelucheCarga')]; })()")
    ok(r[0]=='isla' and '"t":"isla"' in r[1],'al comprarla queda escogida y guardada %s'%r)
    # abrir el juego otra vez: la pantalla de carga sale con la isla (se tarda el motor 3D para poder verla)
    slow['on']=True; await pg.goto("https://test.local/", wait_until='domcontentloaded'); await pg.wait_for_timeout(1500)
    r=await pg.evaluate("[!!document.querySelector('#loader .ld-bg'), document.getElementById('loader').className, document.querySelector('.ld-hop g').getAttribute('fill')]")
    ok(r[0] and 'ld-mapa' in r[1],'al abrir: fondo de la isla, logo en la esquina %s'%r[:2])
    ok(r[2] and r[2].lower()!='#a6d24f','el peluchito que brinca es de tu color %s'%r[2])
    try: await pg.screenshot(path=OUT+'/carga_isla.png', timeout=60000)
    except Exception as e: print('(sin foto)', str(e)[:60])
    await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(800)
    for t in ['espacio','castillo','normal']:
      await ev("(()=>{ if(!wardrobe.own.includes('lc_%s')) wardrobe.own.push('lc_%s'); wardrobe.carga='%s'; saveWardrobe(); return 1; })()"%(t,t,t))
      await pg.goto("https://test.local/", wait_until='domcontentloaded'); await pg.wait_for_timeout(1500)
      r=await pg.evaluate("[!!document.querySelector('#loader .ld-bg'), document.getElementById('loader').className]")
      if t=='normal': ok(not r[0],'la clásica se ve como siempre %s'%r)
      else: ok(r[0] and (('ld-dark' in r[1])==(t=='espacio')),'%s: fondo %s'%(t,r))
      if t!='normal':
        try: await pg.screenshot(path=OUT+'/carga_%s.png'%t, timeout=60000)
        except Exception as e: print('(sin foto)', str(e)[:60])
      await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(500)
    r=await ev("(()=>{ const w=JSON.parse(localStorage.getItem('mundoPelucheRopa')); w.carga='isla'; w.own=w.own.filter(x=>x!=='lc_isla'); localStorage.setItem('mundoPelucheRopa',JSON.stringify(w)); return 1; })()")
    await pg.reload(); await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(500)
    r=await ev("wardrobe.carga"); ok(r=='','si no es tuya, no se puede escoger a mano %s'%r)
    print('errores', errs[:3]); await b.close()
asyncio.run(m())
