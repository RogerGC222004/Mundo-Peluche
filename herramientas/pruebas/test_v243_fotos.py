# v243: en la tienda cada prenda y cada mascota se ve con su foto de verdad (sin el peluche y sin fondo), y las pestañas
# tienen íconos dibujados (ronda 2 de íconos).
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0;
  window.__TICK=()=>new Promise(r=>setTimeout(r,0));
  window.__FLUSH=()=>{ for(let k=0;k<600 && SHOP_THQ.length;k++){ const [g,sw,f]=SHOP_THQ.shift(); if(g===shopThGen && sw.isConnected){ const v=f(); if(v!==undefined) sw.style.background=v; } } };
  window.__LEFT=()=>{ const w=document.createTreeWalker(document.body,4), L=[]; let n; while((n=w.nextNode())){ const p=n.parentNode; if(!p || p.namespaceURI!=='http://www.w3.org/1999/xhtml' || p.closest('.emi,[data-noic],script,style,textarea,option,title,noscript')) continue; if(emiRe().test(n.data)) L.push(n.data.trim().slice(0,30)); } return L; };
  window.__PIX=url=>new Promise(res=>{ const im=new Image(); im.onload=()=>{ const c=document.createElement('canvas'); c.width=im.width; c.height=im.height; const g=c.getContext('2d'); g.drawImage(im,0,0); res({w:im.width,h:im.height,d:g.getImageData(0,0,im.width,im.height).data}); }; im.onerror=()=>res(null); im.src=url; }); 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type in ('warning','error') and ('foto' in m.text or 'ropa' in m.text or 'shader' in m.text.lower()) else None)
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 900)
    await ev(STEP)

    # 1. todas las prendas y todas las mascotas tienen foto
    r=await ev("""(()=>{ const rt0=renderer.getRenderTarget(), ca0=renderer.getClearAlpha(), gl0=GOOGLY.list.length, t0=performance.now(); const L=SHOP.filter(phIsCloth), vac=[];
        for(const it of L) if(!itemPhoto(it)) vac.push(it.name); const ms=(performance.now()-t0)/L.length; let pv=[]; for(const p of PETS) if(!petPhoto(p.id)) pv.push(p.name);
        let kb=0; for(const v of PH_CACHE.values()) kb+=v.length/1024; const t1=performance.now(); itemPhoto(L[L.length-1]); const again=performance.now()-t1;
        return [L.length, vac.slice(0,8), vac.length, PETS.length, pv, +ms.toFixed(1), [Math.round(kb), PH_CACHE.size, PH_MAX, +(kb/PH_CACHE.size).toFixed(1), /^data:image\\/webp/.test(PH_CACHE.values().next().value)], +again.toFixed(2), renderer.getRenderTarget()===rt0, renderer.getClearAlpha()===ca0, GOOGLY.list.length===gl0,
          [...new Set(L.map(it=>it.av))].join('')]; })()""")
    ok(r[2]==0 and r[0]>300, '📸 las %s prendas (Frijolito, Chibi y Amigurumi: %s) tienen su foto (sin foto: %s %s)'%(r[0],r[11],r[2],r[1]))
    ok(len(r[4])==0, '🐾 las %s mascotas tienen su foto (sin foto: %s)'%(r[3],r[4]))
    ok(r[5]<40 and r[7]<1, '⏱️ cada foto tarda ~%s ms (aquí sin tarjeta de video) y la segunda vez es al instante (%s ms)'%(r[5],r[7]))
    ok(r[6][1]<=r[6][2] and r[6][3]<9 and r[6][0]<4000, '💾 se guardan las últimas %s fotos (%s KB, ~%s KB cada una, en webp: %s)'%(r[6][1],r[6][0],r[6][3],r[6][4]))
    ok(r[8] and r[9] and r[10], '🎬 tomar fotos no le cambia nada al juego (pantalla, fondo y ojitos de las mascotas)')

    # 2. la foto es solo la prenda: fondo transparente y nada del peluche verde
    r=await ev("""(async()=>{ const out=[]; const L=[SHOP.find(x=>x.slot==='hat' && /^Gorra roja$/i.test(x.name))||SHOP.find(x=>x.slot==='hat'), SHOP.find(x=>x.slot==='top'), SHOP.find(x=>x.slot==='chat'), SHOP.find(x=>x.slot==='ashoe')];
        for(const it of L){ if(!it) continue; const P=await __PIX(itemPhoto(it)); if(!P) continue; let verde=0, vis=0, n=P.w*P.h;
          for(let i=0;i<n;i++){ const a=P.d[i*4+3]; if(a<128) continue; vis++; const R=P.d[i*4], G=P.d[i*4+1], B=P.d[i*4+2]; if(G>150 && R>120 && R<200 && B<110) verde++; }
          out.push([it.av+' '+it.name, P.w, P.h, P.d[3], vis, verde]); } return out; })()""")
    ok(len(r)==4 and all(x[3]==0 for x in r), '🫥 el fondo de la foto es transparente (%s)'%[(x[0],x[3]) for x in r])
    ok(len(r)==4 and all(x[5]<x[4]*.03 for x in r[:2]), '🧸 en la foto no sale el peluche verde, solo la prenda (%s)'%[(x[0],x[5],x[4]) for x in r[:2]])
    ok(len(r)==4 and r[0][1]>r[0][2], '🧢 la foto tiene la forma de la prenda (la gorra es más ancha que alta: %s×%s)'%(r[0][1],r[0][2]))

    # 3. la tienda: tarjetas con foto, sin iconito de emoji, pestañas con dibujos
    r=await ev("""(async()=>{ const t0=performance.now(); openShop(); shopCat='gorras'; renderShop(); const ms=performance.now()-t0; await __TICK(); __FLUSH(); await __TICK();
        const cards=[...document.querySelectorAll('#shopGrid .shop-item')], ph=cards.filter(b=>{ const s=b.querySelector('.sw.ph'); return s && /data:image\\/(png|webp)/.test(s.style.backgroundImage); }).length;
        const tabs=[...document.querySelectorAll('#shopTabs .shop-tab')], ti=tabs.filter(t=>t.querySelector('.emi')).length;
        return [cards.length, ph, document.querySelectorAll('#shopGrid .sw .ic').length, tabs.length, ti, __LEFT(), +ms.toFixed(0)]; })()""")
    ok(r[0]>5 and r[1]==r[0], '🛍️ en la tienda las %s gorras se ven con su foto (%s con foto)'%(r[0],r[1]))
    ok(r[2]==0, '🏷️ ya no sale el iconito de emoji en la esquina')
    ok(r[3]>3 and r[4]==r[3], '🗂️ las %s pestañas tienen su ícono dibujado'%r[3])
    ok(len(r[5])==0, '🚫 no queda ningún emoji de la lista en la tienda (quedan: %s)'%r[5][:5])
    ok(r[6]<400, '⚡ abrir la lista es rápido: las fotos se toman después, poco a poco (%s ms)'%r[6])

    r=await ev("""(async()=>{ shopCat='mascotas'; renderShop(); __FLUSH(); await __TICK(); const cards=[...document.querySelectorAll('#shopGrid .shop-item')]; const ph=cards.filter(b=>{ const s=b.querySelector('.sw.ph'); return s && /data:image\\/(png|webp)/.test(s.style.backgroundImage); }).length;
        return [cards.length, ph, document.querySelector('#shopGrid').textContent.match(/[\\u{1F400}-\\u{1F43F}\\u{1F980}-\\u{1F9AF}]/u)]; })()""")
    ok(r[0]>=20 and r[1]==r[0] and not r[2], '🐶 las mascotas se ven con su foto de verdad, sin emoji (%s de %s)'%(r[1],r[0]))

    # 4. con el Chibi y el Amigurumi también
    for body,cat in [('av_chibi','carriba'),('av_amigu','azapatos')]:
      r=await ev("""(async()=>{ wardrobe.eq.body='%s'; applyOutfit(plush, wardrobe.eq); shopCat='%s'; renderShop(); __FLUSH(); await __TICK(); const cards=[...document.querySelectorAll('#shopGrid .shop-item')];
          const ph=cards.filter(b=>{ const s=b.querySelector('.sw.ph'); return s && /data:image\\/(png|webp)/.test(s.style.backgroundImage); }).length; return [shopCat, cards.length, ph]; })()"""%(body,cat))
      ok(r[0]==cat and r[1]>3 and r[2]==r[1], '👕 con el %s: %s de %s prendas de “%s” con foto'%('Chibi' if 'chibi' in body else 'Amigurumi',r[2],r[1],cat))
    await ev("(()=>{ delete wardrobe.eq.body; applyOutfit(plush, wardrobe.eq); return 1; })()")

    # 5. probarse algo sigue funcionando y la foto no cambia tu peluche
    r=await ev("""(async()=>{ shopCat='gorras'; renderShop(); __FLUSH(); const b=document.querySelector('#shopGrid .shop-item'); b.click(); await __TICK(); shopFlush(); const has=(plush.userData.cloth||[]).length;
        const it=SHOP.find(x=>x.slot==='hat' && x.id!==(shopTry&&shopTry.id)); itemPhoto(it); PH_CACHE.delete('i'+it.id); itemPhoto(it); return [!!shopTry, has, (plush.userData.cloth||[]).length, plush.parent===studio]; })()""")
    ok(r[0] and r[1]>0 and r[1]==r[2], '🎩 al tocar una gorra te la pruebas, y tomar fotos no le quita ni le pone nada a tu peluche (%s → %s piezas)'%(r[1],r[2]))

    ok(not errs, '🚫 sin errores (%s)'%errs[:3])
    await b.close()
asyncio.run(m())
