# v257: el Cubito (otro tipo de cuerpo, todo de cubitos). Revisa: la tienda (cuerpo y sus 8 secciones, gratis), vestirlo y cambiar
# de estilo, regresar a los otros cuerpos sin que quede nada del Cubito, los pies en el suelo, de lejos cuadrado, que los demás lo
# vean igual (presencia), poses (caminar, sentarse, coche, nadar), miniaturas de la tienda y los textos en inglés.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, locale='es-MX'); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("if(!sessionStorage.getItem('t257')){ sessionStorage.setItem('t257','1'); localStorage.clear(); } localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false, autoRes:false}));")
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
    await ev("""window.requestAnimationFrame=()=>0; window.__run=(sec,fn)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); if(fn) fn(i); update(.05,t); scene.updateMatrixWorld(); } };
      window.__vis=o=>{ let n=0, tri=0; const bb=new THREE.Box3(); o.updateMatrixWorld(true); o.traverse(m=>{ if(!m.isMesh) return; for(let q=m;q;q=q.parent) if(!q.visible) return; if(m.material && m.material.visible===false) return; n++; const g=m.geometry; tri+=(g.index?g.index.count:(g.attributes.position?g.attributes.position.count:0))/3; if(g.attributes.position && g.attributes.position.count) bb.expandByObject(m); }); return {n, tri:tri|0, lo:+(bb.min.y-o.position.y).toFixed(2), hi:+(bb.max.y-o.position.y).toFixed(2)}; }; 1""")
    # 1. la tienda
    r=await ev("""(()=>{ const body=SHOP_BY.av_cubo, cats=SHOP_CATS.filter(c=>c.av==='k').map(c=>c.id), n=c=>SHOP.filter(it=>it.cat===c).length, allFree=SHOP.filter(it=>it.av==='k' && !/^kr[abzgc]_/.test(it.id)).every(it=>it.free && it.price===0);   // (v258: el catálogo copiado del Chibi tiene precio; lo básico sigue gratis)
      wardrobe.eq={body:'av_cubo'}; const vis=SHOP.filter(it=>diShopVis(it) && it.av==='k').length; return [!!body && body.free===1, cats, cats.map(n), allFree, myAv(), vis]; })()""")
    ok(r[0] and len(r[1])==10 and r[3] and r[4]=='k' and r[5]==sum(r[2]), 'tienda: «Cubito» en Cuerpo (gratis) y 10 secciones solo del Cubito (v259: con gorros y accesorios) %s, con %s cosas, las básicas gratis'%(r[1],r[2]))
    # 2. vestirlo, estilo 1 y 2, pies en el suelo
    r=await ev("""(()=>{ wardrobe.eq={body:'av_cubo'}; applyOutfit(plush,wardrobe.eq); plush.position.set(0,0,0); poseLimbs(plush,0,.05,0,false,0,false,null,0,0,false); const a=__vis(plush), u=plush.userData;
      wardrobe.eq={body:'av_cubo', kst:'ke_1', kface:'kf_sorprendido', khair:'kh_colitas', khcol:'kc_7', ktop:'kt_rosa_l', kbot:'kb_morada_c', kshoe:'ks_blanca', kskin:'kp_4'}; applyOutfit(plush,wardrobe.eq); const b=__vis(plush), L=u.cbLook;
      return [u.av, a, b, L.st, L.face, L.hs, L.top.slv, L.bot.len, u.body.material===chHideMat]; })()""")
    ok(r[0]=='k' and r[3]==1 and r[4]=='sorprendido' and r[5]=='colitas' and r[6]=='larga' and r[7]=='corto' and r[8], 'se viste: estilo 1, cara sorprendido, colitas, manga larga y short %s'%r[3:8])
    ok(abs(r[1]['lo'])<.04 and 2.1<r[1]['hi']<2.4 and r[2]['tri']>r[1]['tri'], 'pies en el suelo (%s m), mide %s m; el estilo 1 redondeado lleva más triangulitos (%s) que el cuadrado (%s), %s piezas'%(r[1]['lo'],r[1]['hi'],r[2]['tri'],r[1]['tri'],r[1]['n']))
    # 3. de lejos, cuadrado (y regresa)
    r=await ev("""(()=>{ const u=plush.userData, g0=u.cb.head.geometry; u.lodFar=false; camera.position.set(plush.position.x+30,plush.position.y+2,plush.position.z); plushLod(plush); const far=u.cbFar, g1=u.cb.head.geometry;
      camera.position.set(plush.position.x+3,plush.position.y+2,plush.position.z); plushLod(plush); return [far, g1!==g0, u.cbFar, u.cb.head.geometry===g0, g1.attributes.position.count<g0.attributes.position.count]; })()""")
    ok(r==[True,True,False,True,True], 'de lejos el Cubito se dibuja cuadrado (menos puntos) y de cerca regresa a su estilo %s'%r)
    # 4. regresar a los otros cuerpos: nada del Cubito se queda
    r=await ev("""(()=>{ const out=[]; for(const body of [undefined,'av_chibi','av_amigu','av_cubo',undefined]){ wardrobe.eq=body?{body}:{}; applyOutfit(plush,wardrobe.eq); const u=plush.userData;
        out.push([u.av, u.cb?u.cb.g.visible:null, u.cb?u.cb.hands.some(h=>h.visible):null, u.legs.every(l=>!l.userData.foot || l.userData.foot.visible===(u.av!=='k'))]); } return out; })()""")
    ok(json.dumps(r)==json.dumps([['f',False,False,True],['c',False,False,True],['a',False,False,True],['k',True,True,True],['f',False,False,True]]), 'cambiar de cuerpo ida y vuelta (frijolito, Chibi, Amigurumi, Cubito, frijolito): no queda nada del Cubito y los pies vuelven %s'%r)
    # 5. los demás lo ven igual (presencia)
    r=await ev("""(()=>{ wardrobe.eq={body:'av_cubo', kst:'ke_1', kface:'kf_guino', khair:'kh_chongo', khcol:'kc_4', ktop:'kt_amarilla_c', kbot:'kb_negra_l', kshoe:'ks_azul', kskin:'kp_6'}; const ou=outfitList(wardrobe.eq), eq=parseOutfit(ou);
      const r=makeRemote(2,'Ana'); applyOutfit(r.obj,eq); const L=r.obj.userData.cbLook; const sz=JSON.stringify(ou).length; removeRemote&&0; return [r.obj.userData.av, L.face, L.hs, L.st, L.top.c, ou.length, sz]; })()""")
    ok(r[0]=='k' and r[1]=='guino' and r[2]=='chongo' and r[3]==1, 'otro jugador lo ve igual: Cubito, guiño, chongo, estilo 1 (lo que se manda: %s cosas, %s letras)'%(r[5],r[6]))
    # 6. poses (caminar, sentarse, en coche, nadar, saludar) sin errores
    r=await ev("""(()=>{ wardrobe.eq={body:'av_cubo'}; applyOutfit(plush,wardrobe.eq); player.pos.set(START.x+4,START.top+.05,START.z); let ok=0; const e0=0;
      try{ __run(.6,()=>{ keys.KeyW=true; }); keys.KeyW=false; ok++; }catch(e){}
      try{ cjSitPose(plush,1,.05,0); carRiderPose(plush,1,.05); poseLimbs(plush,1,.05,0,true,0,false,1.2); ok++; }catch(e){ console.warn(e); }
      try{ doWave&&doWave(); }catch(e){} __run(.5); return ok; })()""")
    ok(r==2, 'poses: camina, se sienta, maneja y nada sin errores')
    # 7. miniaturas de la tienda (caras, peinados y estilos)
    r=await ev("""(()=>{ wardrobe.eq={body:'av_cubo'}; const its=['kf_feliz','kf_dormilon','kh_largo','kh_rapado','ke_1'].map(id=>SHOP_BY[id]); const bg=its.map(it=>chSwatch(it)||''); return bg.map(x=>/^url\\(/.test(x)); })()""")
    ok(all(r), 'miniaturas de la tienda: caras en pixel art grande y retratos de peinados y estilos %s'%r)
    # 8. inglés
    r=await ev("""(()=>{ I18N.set('en'); const t=['Cubito','Estilo','Estilo 1: redondeado','Cara','Enojado tierno','Playera roja de manga corta','Pantalón azul','Short verde','Tenis negros','Piel verde frijolito','Cabello pelirrojo','Colitas'].map(x=>I18N.t(x)); I18N.set('es'); return t; })()""")
    ok(r[0]=='Cubie' and r[1]=='Style' and r[5]=='Red T-shirt, short sleeves' and r[6]=='Blue pants' and r[7]=='Green shorts' and r[9]=='Beanlet green skin' and r[11]=='Pigtails', 'en inglés: %s'%r)
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
