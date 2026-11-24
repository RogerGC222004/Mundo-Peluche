# v259: gorros y accesorios del Cubito, hechos de cubitos (los 110 gorros y 110 accesorios del Chibi, mismos precios).
# Revisa: la tienda (con su filtro por lugar), que los 44 tipos de gorro y 57 de accesorio tengan su forma, que todos se armen
# (estilo 1, estilo 2 y de lejos) sin errores y sin agregar dibujos, gorro + 5 accesorios a la vez, que con gorro no salga el chongo,
# los que brillan, la capa que se mueve, que los demás lo vean igual, las fotos de la tienda y los textos en inglés.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, locale='es-MX'); pg=await ctx.new_page(); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("if(!sessionStorage.getItem('t259')){ sessionStorage.setItem('t259','1'); localStorage.clear(); } localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false, autoRes:false}));")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 900)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=180000)
    await ev("startGame()"); await pg.wait_for_timeout(1500)
    await ev("""window.requestAnimationFrame=()=>0; window.__run=(sec,fn)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); if(fn) fn(i); update(.05,t); scene.updateMatrixWorld(); } };
      window.__tri=o=>{ let n=0, tri=0; o.updateMatrixWorld(true); o.traverse(m=>{ if(!m.isMesh) return; for(let q=m;q;q=q.parent) if(!q.visible) return; if(m.material===chHideMat || m.material===tagMat || (m.material && m.material.visible===false)) return; const g=m.geometry; if(!g.attributes.position || !g.attributes.position.count) return; n+=Array.isArray(m.material)?g.groups.length:1; tri+=(g.index?g.index.count:g.attributes.position.count)/3; }); return [n,tri|0]; }; 1""")
    # 1. la tienda
    r=await ev("""(()=>{ const K=c=>SHOP.filter(it=>it.cat===c), G=K('kgorros'), A=K('kaccesorios'), CG=K('cgorros'), CA=K('caccesorios');
      const same=(a,b)=>a.length===b.length && a.every((it,i)=>it.name===b[i].name && it.price===b[i].price && (it.hk||it.ak)===(b[i].hk||b[i].ak) && it.as===b[i].as);
      const slots=[...new Set(A.map(it=>it.slot))].sort(), hs=[...new Set(G.map(it=>it.slot))]; const cats=SHOP_CATS.filter(c=>c.av==='k').map(c=>c.name);
      wardrobe.eq={body:'av_cubo'}; shopCat='kaccesorios'; let chips=0; try{ openShop(); renderShop(); chips=document.querySelectorAll('#shopFilters [data-as], [data-as]').length; closeShop&&closeShop(); }catch(e){ console.warn(e); }
      return [G.length, A.length, same(G,CG), same(A,CA), slots, hs, cats, G.filter(it=>it.price===0).length, chips]; })()""")
    ok(r[0]==110 and r[1]==110 and r[2] and r[3] and r[4]==['kacb','kacc','kacf','kach','kacn'] and r[5]==['khat'] and 'Gorros' in r[6] and 'Accesorios' in r[6] and r[8]>=5,
       'tienda: 110 gorros y 110 accesorios como los del Chibi (mismo nombre, precio, tipo y lugar; %s gratis), un accesorio por lugar %s, filtro por lugar (%s botones)'%(r[7],r[4],r[8]))
    # 2. todos los tipos tienen su forma
    r=await ev("""(()=>{ const H=new Set(SHOP.filter(it=>it.cat==='kgorros').map(it=>it.hk)), A=new Set(SHOP.filter(it=>it.cat==='kaccesorios').map(it=>it.ak));
      const has=k=>!!(CB_ACCH[k]||CB_ACCC[k]||CB_ACCP[k]||CB_ACCS[k]||CB_ACCM[k]); return [H.size, A.size, [...H].filter(k=>!CB_HAT[k]), [...A].filter(k=>!has(k))]; })()""")
    ok(r[0]==44 and r[1]==57 and not r[2] and not r[3], 'los %s tipos de gorro y %s de accesorio tienen su forma de cubitos (faltan: %s %s)'%(r[0],r[1],r[2],r[3]))
    # 3. armar todos: estilo 2, estilo 1 y de lejos; sin dibujos de más (solo la capa usa la pieza de la falda)
    r=await ev("""(()=>{ const u=plush.userData, res={max2:0,max1:0,maxF:0,ms:0,n:0,err:[],big:'',extra:[]}; wardrobe.eq={body:'av_cubo'}; applyOutfit(plush,wardrobe.eq); const base=__tri(plush)[0];
      for(const it of SHOP.filter(it=>/^kr[gc]_/.test(it.id))){ for(const st of ['ke_2','ke_1']){ const t0=performance.now(); try{ wardrobe.eq={body:'av_cubo', kst:st, [it.slot]:it.id}; applyOutfit(plush,wardrobe.eq); }catch(e){ res.err.push(it.id+': '+e.message); continue; }
          res.ms+=performance.now()-t0; res.n++; const [n,t]=__tri(plush); if(st==='ke_2'){ if(t>res.max2){ res.max2=t; res.big=it.id; } const gl=['varita','jetpack','linterna','halo','pastel','astro'].includes(it.ak||it.hk)?1:0; if(n!==base+gl+(it.ak==='capa'?1:0)) res.extra.push(it.id+':'+(n-base)); } else res.max1=Math.max(res.max1,t);
          if(st==='ke_2'){ try{ cbDress(u,u.cbLook,true); res.maxF=Math.max(res.maxF,__tri(plush)[1]); cbDress(u,u.cbLook,false); }catch(e){ res.err.push(it.id+' lejos: '+e.message); } } } }
      res.ms=+(res.ms/res.n).toFixed(1); res.base=base; return res; })()""")
    ok(not r['err'], 'los 220 gorros y accesorios se arman en estilo 1, estilo 2 y de lejos sin errores %s'%r['err'][:3])
    ok(not r['extra'], 'no agregan dibujos: van dentro de las piezas (%s dibujos; solo la capa usa la pieza de la falda y lo que brilla, su material) %s'%(r['base'],r['extra'][:5]))
    ok(r['max2']<12000 and r['max1']<45000 and r['maxF']<12000, 'triangulitos de un Cubito con gorro o accesorio: máximo %s cuadrado (%s), %s redondeado, %s de lejos; tarda %s ms en vestirse'%(r['max2'],r['big'],r['max1'],r['maxF'],r['ms']))
    # 4. gorro + 5 accesorios a la vez; con gorro no sale el chongo
    r=await ev("""(()=>{ const u=plush.userData; wardrobe.eq={body:'av_cubo', khair:'kh_chongo'}; applyOutfit(plush,wardrobe.eq); const g0=u.cb.head.geometry; g0.computeBoundingBox(); const y0=g0.boundingBox.max.y/CB.S;
      wardrobe.eq={body:'av_cubo', khair:'kh_chongo', khat:'krg_boina'}; applyOutfit(plush,wardrobe.eq); const g1=u.cb.head.geometry; g1.computeBoundingBox(); const y1=g1.boundingBox.max.y/CB.S;
      wardrobe.eq={body:'av_cubo', khair:'kh_corto', khat:'krg_boina'}; applyOutfit(plush,wardrobe.eq); const g2=u.cb.head.geometry; g2.computeBoundingBox(); const y2=g2.boundingBox.max.y/CB.S;
      wardrobe.eq={body:'av_cubo', khat:'krg_gorra', kacc:'krc_mono', kacf:'krc_lentes', kacn:'krc_bufanda', kacb:'krc_mochila', kach:'krc_varita'}; applyOutfit(plush,wardrobe.eq); const L=u.cbLook;
      return [+y0.toFixed(1), +y1.toFixed(1), L.hat&&L.hat.hk, Object.keys(L.acc).sort(), Array.isArray(u.cb.hands.find(h=>h.geometry.groups.length).material), +y2.toFixed(1)]; })()""")
    ok(r[0]>24 and r[1]==r[5] and r[2]=='gorra' and r[3]==['cabeza','cara','cuello','espalda','mano'] and r[4], 'con gorro se quita el chongo (alto %s → %s cubitos, igual que con cabello corto: %s); gorro y 5 accesorios a la vez %s; la varita brilla'%(r[0],r[1],r[5],r[3]))
    # 5. la capa se mueve con las piernas; caminar con todo puesto
    r=await ev("""(()=>{ wardrobe.eq={body:'av_cubo', kbot:'krb_shorts', kacb:'krc_capa_roja'}; applyOutfit(plush,wardrobe.eq); const C=plush.userData.cb, on=C.skirt.visible; player.pos.set(START.x+4,START.top+.05,START.z); let ok=0;
      try{ __run(1,()=>{ keys.KeyW=true; }); keys.KeyW=false; renderer.render(scene,camera); ok++; }catch(e){ console.warn(e); } wardrobe.eq={body:'av_cubo'}; applyOutfit(plush,wardrobe.eq); return [on, ok, C.skirt.visible]; })()""")
    ok(r==[True,1,False], 'la capa va en la pieza que se mueve con las piernas, camina sin errores y al quitarla se va %s'%r)
    # 6. los demás lo ven igual
    r=await ev("""(()=>{ wardrobe.eq={body:'av_cubo', khat:'krg_bruja', kacf:'krc_corazon', kacb:'krc_alitas', kach:'krc_globo_azul'}; const ou=outfitList(wardrobe.eq), eq=parseOutfit(ou); const R=makeRemote(4,'Cata'); applyOutfit(R.obj,eq); const L=R.obj.userData.cbLook;
      return [L.hat&&L.hat.hk, L.acc.cara&&L.acc.cara.ak, L.acc.espalda&&L.acc.espalda.ak, L.acc.mano&&L.acc.mano.ak, JSON.stringify(ou).length]; })()""")
    ok(r[:4]==['bruja','corazon','alitas','globo'], 'otro jugador lo ve igual: sombrero de bruja, lentes de corazón, alitas y globo (%s letras)'%r[4])
    # 7. fotos de la tienda (solo el gorro o el accesorio)
    r=await ev("""(()=>{ const ids=['krg_corona','krg_bruja','krc_lentes','krc_bufanda','krc_alitas','krc_varita','krc_globo_azul','krc_capa_roja']; const out=ids.map(id=>{ const u=itemPhoto(SHOP_BY[id]); return typeof u==='string' && u.length>400; });
      const R=phRigGet(), C=R.o && R.o.userData.cb; return [out, C?[C.head.visible,C.face.visible]:null]; })()""")
    ok(all(r[0]) and r[1]==[True,True], 'fotos de gorros y accesorios del Cubito (corona, bruja, lentes, bufanda, alitas, varita, globo, capa) %s; la cabeza y la cara vuelven %s'%(r[0],r[1]))
    # 8. inglés
    r=await ev("""(()=>{ I18N.set('en'); const t=['Gorros','Accesorios','Corona dorada','Alitas de hada','Varita mágica',NEWS['259'][0],NEWS['259'][1],NEWS['259'][2]].map(x=>I18N.t(x)); I18N.set('es'); return t; })()""")
    ok(r[0]!='Gorros' and r[1]!='Accesorios' and r[2]!='Corona dorada' and r[5].startswith('New body type') and r[6].startswith('Choose') and r[7].startswith('Skirts'), 'en inglés: %s'%r[:5])
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
