# v261: al volver de 1ª a 3ª persona el peluche se vuelve a ver completo (aunque algo le haya cambiado el material mientras
# estaba escondido, como las manchas), con los 4 avatares; y el Cubito camina recto (sin balancearse de lado).
import asyncio
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    pg=await (await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, locale='es-MX')).new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("if(!sessionStorage.getItem('t261')){ sessionStorage.setItem('t261','1'); localStorage.clear(); } localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false, autoRes:false}));")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=180000)
    await ev("startGame()"); await pg.wait_for_timeout(1500)
    await ev("""window.requestAnimationFrame=()=>0; window.__run=(sec,fn)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); if(fn) fn(i); update(.05,t); fpHide(plush,state==='play' && camMode==='first' && plush.visible); } };
      window.__hid=()=>{ let n=0; plush.traverse(m=>{ if(!m.isMesh||!m.material) return; for(let q=m;q;q=q.parent) if(!q.visible) return; [].concat(m.material).forEach(x=>{ if(x.colorWrite===false && x!==chHideMat && x.visible!==false) n++; }); }); return n; }; 1""")
    # 1. con los 4 avatares: 1ª persona esconde, 3ª persona regresa todo; también si le cambian el material (mancha) mientras está escondido
    r=await ev("""(()=>{ const out={}; for(const body of [undefined,'av_chibi','av_amigu','av_cubo']){ wardrobe.eq=body?{body}:{}; applyOutfit(plush,wardrobe.eq); const u=plush.userData;
        const h0=__hid(); setCam('first'); __run(.5); const h1=__hid();
        const m=u.body.material, st=m.clone(); st.userData.stOrig=m; u.body.material=st; __run(1);   // (algo le cambia el material mientras está escondido)
        setCam('third'); __run(.5); stRestore(plush); out[u.av]=[h0,h1>0,__hid(), u.body.material.colorWrite!==false||u.body.material===chHideMat]; } return out; })()""")
    ok(all(v[0]==0 and v[1] and v[2]==0 and v[3] for v in r.values()), 'en 1ª persona se esconde y al volver a 3ª persona se ve completo (frijolito, Chibi, Amigurumi, Cubito), aunque le hayan cambiado el material %s'%r)
    # 2. varias vueltas de cámara caminando
    r=await ev("""(()=>{ wardrobe.eq={}; applyOutfit(plush,wardrobe.eq); player.pos.set(START.x+4,START.top+.05,START.z); for(let i=0;i<4;i++){ setCam(i%2?'third':'first'); __run(.6,()=>{ keys.KeyW=true; }); } keys.KeyW=false; setCam('third'); __run(.3); return [__hid(), plush.userData.body.visible, plush.userData.eyes.every(e=>e.visible)]; })()""")
    ok(r==[0,True,True], 'caminando y cambiando de cámara 4 veces, al final se ve todo %s'%r)
    # 3. el Cubito camina recto; el frijolito se sigue balanceando
    r=await ev("""(()=>{ const zs=body=>{ wardrobe.eq=body?{body}:{}; applyOutfit(plush,wardrobe.eq); setCam('third'); let mx=0; __run(1.2,()=>{ keys.KeyW=true; mx=Math.max(mx,Math.abs(plush.rotation.z)); }); keys.KeyW=false; return +mx.toFixed(3); };
      const R=makeRemote(5,'Dani'); R.obj.userData; applyOutfit(R.obj,{body:'av_cubo'}); return [zs('av_cubo'), zs(undefined), R.obj.userData.av]; })()""")
    ok(r[0]<.01 and r[1]>.02 and r[2]=='k', 'el Cubito camina recto (se ladea %s), el frijolito se sigue balanceando (%s)'%(r[0],r[1]))
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
