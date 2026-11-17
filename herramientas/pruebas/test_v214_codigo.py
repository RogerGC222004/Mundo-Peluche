# v214: tus creaciones (mapas, criaturas, objetos, Modo libre, favoritas y barra) van en tu código de progreso y en la copia de seguridad; al juntar dos guardados no se pierde nada.
import asyncio
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("if(!sessionStorage.getItem('t214')){ sessionStorage.setItem('t214','1'); localStorage.clear(); } localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route)
    async def load():
      await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    await load()
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    r=await ev("""(async()=>{ crOpen(null); ui('crName').value='Michi'; crClose(true); obOpen(null); ui('crName').value='Varita'; crClose(true); ui('mapList').hidden=true; barSave();
      mapsStore([{id:'m1',n:'Obby',t:'juego',s:[['g','inicio',0,0,0,8,2]],d:[],best:9000}]); localStorage.setItem('mundoPelucheLibre',JSON.stringify({v:1,s:[['b',0,1,0,0,3,0]],d:[]}));
      const code=await encodeSave(saveSnapshot()); const o=await decodeSave(code); window.__code=code;
      return [code.slice(0,4), ['Libre','Mapas','Criaturas','Objetos','Barra'].every(k=>typeof o[k]==='string'), sumText(saveSummary(o)), code.length]; })()""")
    ok(r[0]=='MP1-' and r[1] and '3 creaciones' in r[2], 'el código de progreso ya trae Modo libre, mapas, criaturas, objetos y la barra (%s · %s letras) %s'%(r[2],r[3],r[:3]))
    r=await ev("""(()=>{ const a=saveSnapshot(), b={v:1,e:124, Mapas:JSON.stringify({v:1,maps:[{id:'m1',n:'Viejo',t:'juego',s:[],d:[]},{id:'m2',n:'Otro',t:'mundo',s:[],d:[]}]}), Criaturas:JSON.stringify({v:1,list:[{id:'cX',n:'Pato'}]}), MapFav:JSON.stringify(['g:meta:0'])};
      const m=mergeSaves(a,b), M=JSON.parse(m.Mapas).maps, C=JSON.parse(m.Criaturas).list; return [M.map(x=>x.n).join(','), C.map(x=>x.n).join(','), !!m.Objetos, !!m.Libre, m.MapFav]; })()""")
    ok(r[0]=='Obby,Otro' and r[1]=='Michi,Pato' and r[2] and r[3] and 'g:meta:0' in r[4], 'al juntar dos guardados se combinan tus mapas y criaturas sin repetir (y se queda tu versión) %s'%r)
    # en otro teléfono: pegar el código
    await ev("(()=>{ localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false})); return 1; })()")
    await ev("(async()=>{ applySave(await decodeSave(__code)); return 1; })()")
    await load()
    r=await ev("[mapsLoad().length, mapsLoad()[0].best, crLoad()[0]&&crLoad()[0].n, obLoad()[0]&&obLoad()[0].n, inventory.includes('o:'+obLoad()[0].id), JSON.parse(localStorage.getItem('mundoPelucheLibre')).s.length]")
    ok(r==[1,9000,'Michi','Varita',True,1], 'al pegar el código en otro teléfono regresan tus mapas (con récord), criaturas, objetos y Modo libre %s'%r)
    ok(not errs,'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
