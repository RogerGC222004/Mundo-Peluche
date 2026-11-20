# v231: en el menú principal se ve «¡Instala el juego!», pero al escoger el modo de juego se esconde (tapaba «Volver»).
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, device_scale_factor=2); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheEnLinea','{\"on\":true,\"tip\":true}'); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'min',qDef:1,hints:false,weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    BOX="""(()=>{ const r=e=>{ const q=ui(e).getBoundingClientRect(); return [q.left,q.top,q.right,q.bottom]; }, vis=e=>getComputedStyle(ui(e)).display!=='none' && !ui(e).hidden && ui(e).offsetParent!==null; const I=r('installBtn'); let over=[]; for(const id of %s){ if(!vis(id)) continue; const B=r(id); if(I[0]<B[2] && I[2]>B[0] && I[1]<B[3] && I[3]>B[1]) over.push(id); } return [vis('installBtn'), over]; })()"""
    await ev("(()=>{ ui('installBtn').hidden=false; return 1; })()")
    a=await ev(BOX%json.dumps(['playBtn','shopBtn','saveBtn','optionsBtn','controlsBtn']))
    await ev("(()=>{ ui('playBtn').click(); return 1; })()"); await pg.wait_for_timeout(400)
    c=await ev(BOX%json.dumps(['soloBtn','mpBtn','mgBtn','freeBtn','mapBtn','modesBack'])); await pg.screenshot(path='/tmp/claude-0/-home-claude/71ba1456-fe89-5ecb-af02-76c832933a55/scratchpad/perf/f231_menu_modos.png')
    await ev("(()=>{ ui('modesBack').click(); return 1; })()"); await pg.wait_for_timeout(400); d=await ev(BOX%json.dumps(['playBtn']))
    ok(a[0] and not a[1], 'en el menú principal se ve «¡Instala el juego!» sin taparle nada a los botones %s'%a)
    ok(not c[0], 'al escoger el modo de juego se esconde y deja libre «Volver» %s'%c)
    ok(d[0], 'al volver al menú principal aparece otra vez %s'%d)
    ok(not errs,'sin errores %s'%errs[:3]); await b.close()
asyncio.run(m())
