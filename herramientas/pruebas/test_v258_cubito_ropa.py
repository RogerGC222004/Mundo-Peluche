# v258: la ropa del catálogo para el Cubito, hecha de cubitos (100 de arriba, 100 de abajo, 100 zapatos; mismos precios que el Chibi).
# Revisa: la tienda, que todas las prendas se armen (estilo 1, estilo 2 y de lejos) sin errores y sin pasarse de triangulitos,
# las faldas que se mueven con las piernas (en la tarjeta gráfica, con su sombra), los tenis con luces, las fotos de las prendas,
# que los demás lo vean igual, caminar con falda, y los textos en inglés.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, locale='es-MX'); pg=await ctx.new_page(); errs=[]; cons=[]
    pg.on("pageerror",lambda e:errs.append(str(e))); pg.on("console",lambda m: cons.append(m.text) if m.type in ('error','warning') else None)
    await pg.add_init_script("if(!sessionStorage.getItem('t258')){ sessionStorage.setItem('t258','1'); localStorage.clear(); } localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false, autoRes:false}));")
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
      window.__tri=o=>{ let n=0, tri=0; o.updateMatrixWorld(true); o.traverse(m=>{ if(!m.isMesh) return; for(let q=m;q;q=q.parent) if(!q.visible) return; if(m.material===chHideMat || m.material===tagMat || (m.material && m.material.visible===false)) return; const g=m.geometry; if(!g.attributes.position || !g.attributes.position.count) return; n++; tri+=(g.index?g.index.count:g.attributes.position.count)/3; }); return [n,tri|0]; }; 1""")
    # 1. la tienda: el catálogo copiado del Chibi
    r=await ev("""(()=>{ const out={}; for(const [kc,cc,pre] of [['karriba','carriba','kra_'],['kabajo','cabajo','krb_'],['kzapatos','czapatos','krz_']]){ const K=SHOP.filter(it=>it.cat===kc && it.id.startsWith(pre)), C=SHOP.filter(it=>it.cat===cc);
        out[kc]=[K.length, C.length, K.every((it,i)=>it.name===C[i].name && it.price===C[i].price && it.av==='k' && (it.tk||it.bk||it.sk)===(C[i].tk||C[i].bk||C[i].sk)), K.filter(it=>it.price===0).length, SHOP.filter(it=>it.cat===kc && !it.id.startsWith(pre)).every(it=>it.price===0)]; }
      const nm=SHOP_CATS.filter(c=>c.av==='k').map(c=>c.name); return [out, nm]; })()""")
    o=r[0]; good=all(v[0]==100 and v[1]==100 and v[2] and v[3]==4 and v[4] for v in o.values())
    ok(good and 'Arriba' in r[1] and 'Abajo' in r[1], 'tienda: 100 de arriba, 100 de abajo y 100 zapatos como los del Chibi (mismo nombre, precio y tipo; 4 gratis de cada una), las básicas siguen gratis; secciones %s'%r[1])
    # 2. todos los tipos de prenda tienen su forma de cubitos
    r=await ev("""(()=>{ const T=new Set(SHOP.filter(it=>it.cat==='karriba'&&it.tk).map(it=>it.tk)), B=new Set(SHOP.filter(it=>it.cat==='kabajo'&&it.bk).map(it=>it.bk)), Z=new Set(SHOP.filter(it=>it.cat==='kzapatos'&&it.sk).map(it=>it.sk));
      const src=cbChest.toString()+cbBib.toString()+cbUarm.toString()+cbPelvis.toString()+cbThigh.toString()+cbShin.toString()+cbFoot.toString()+cbSkirtV.toString()+JSON.stringify(CB_SLV)+JSON.stringify(CB_SHAFT), sets=new Set([...CB_HOOD,...CB_RIB,...CB_SKIRT,...CB_SHORT,...CB_UNDER]);
      const miss=[...T,...B,...Z].filter(k=>k!=='tee' && k!=='shorts' && k!=='pants' && k!=='tenis' && !sets.has(k) && !src.includes("'"+k+"'")); return [T.size,B.size,Z.size,miss]; })()""")
    ok(r[0]==20 and r[1]==11 and r[2]==21 and not r[3], 'los %s tipos de arriba, %s de abajo y %s de zapatos tienen su forma (faltan: %s)'%(r[0],r[1],r[2],r[3]))
    # 3. armar todas las prendas: estilo 2, estilo 1 y de lejos (sin errores; triangulitos y tiempo)
    r=await ev("""(()=>{ const u=plush.userData, res={max2:0,max1:0,maxF:0,ms:0,n:0,err:[],big:''}; const items=SHOP.filter(it=>/^kr[abz]_/.test(it.id));
      for(const it of items){ for(const st of ['ke_2','ke_1']){ const t0=performance.now(); try{ wardrobe.eq={body:'av_cubo', kst:st, [it.slot]:it.id}; applyOutfit(plush,wardrobe.eq); }catch(e){ res.err.push(it.id+': '+e.message); continue; }
          res.ms+=performance.now()-t0; res.n++; const t=__tri(plush)[1]; if(st==='ke_2' && t>res.max2){ res.max2=t; res.big=it.id; } if(st==='ke_1') res.max1=Math.max(res.max1,t);
          if(st==='ke_2'){ try{ cbDress(u,u.cbLook,true); res.maxF=Math.max(res.maxF,__tri(plush)[1]); cbDress(u,u.cbLook,false); }catch(e){ res.err.push(it.id+' lejos: '+e.message); } } } }
      res.ms=+(res.ms/res.n).toFixed(1); return res; })()""")
    ok(not r['err'], 'las 300 prendas se arman en estilo 1, estilo 2 y de lejos sin errores %s'%r['err'][:3])
    ok(r['max2']<16000 and r['max1']<45000 and r['maxF']<9000, 'triangulitos de un Cubito: máximo %s cuadrado (%s), %s redondeado, %s de lejos; tarda %s ms en vestirse'%(r['max2'],r['big'],r['max1'],r['maxF'],r['ms']))
    # 4. la falda: pieza aparte que se mueve con las piernas (en la tarjeta gráfica, con su sombra)
    r=await ev("""(()=>{ wardrobe.eq={body:'av_cubo', kbot:'krb_falda', ktop:'kra_vestido'}; applyOutfit(plush,wardrobe.eq); const u=plush.userData, C=u.cb, sk=C.skirt, m=sk.material;
      const a=[sk.visible, !!sk.geometry.attributes.position && sk.geometry.attributes.position.count>0, m!==CB_MAT && !!m.onBeforeCompile, !!sk.customDepthMaterial];
      u.legs[0].rotation.x=-.5; u.legs[0].userData.joint.rotation.x=0; u.legs[1].rotation.x=.4; u.legs[1].userData.joint.rotation.x=.6; sk.onBeforeRender(); const v=sk.material; let U=null; renderer.render(scene,camera); renderer.render(scene,camera);
      const p=renderer.properties.get(m); U=p.uniforms&&p.uniforms.uLeg; const L=U?U.value.toArray().map(x=>+x.toFixed(2)):null;
      wardrobe.eq={body:'av_cubo', kbot:'krb_shorts'}; applyOutfit(plush,wardrobe.eq); const off=!C.skirt.visible;
      return [a, L, off]; })()""")
    ok(all(r[0]) and r[1]==[0.5,0.5,-0.4,-1.0] and r[2], 'la falda va en su pieza, con su material que la mueve con las piernas y su sombra %s; ángulos de las piernas %s; con short no sale %s'%(r[0],r[1],r[2]))
    shader_err=[c for c in cons if 'shader' in c.lower() or 'program' in c.lower()]
    ok(not shader_err, 'la tarjeta gráfica acepta el movimiento de la falda (sin errores al dibujar) %s'%shader_err[:2])
    # 5. caminar y sentarse con falda larga sin errores
    r=await ev("""(()=>{ wardrobe.eq={body:'av_cubo', kbot:'krb_fl_flores', ktop:'kra_cardigan_rosa', kshoe:'krz_sandalia_rosa'}; applyOutfit(plush,wardrobe.eq); player.pos.set(START.x+4,START.top+.05,START.z); let ok=0;
      try{ __run(1.2,()=>{ keys.KeyW=true; }); keys.KeyW=false; renderer.render(scene,camera); ok++; }catch(e){ console.warn(e); }
      try{ cjSitPose(plush,1,.05,0); plush.updateMatrixWorld(true); renderer.render(scene,camera); ok++; }catch(e){ console.warn(e); } __run(.3); return [ok, plush.userData.cb.skirt.visible]; })()""")
    ok(r==[2,True], 'camina y se sienta con falda larga sin errores %s'%r)
    # 6. los tenis con luces brillan
    r=await ev("""(()=>{ wardrobe.eq={body:'av_cubo', kshoe:'krz_luces'}; applyOutfit(plush,wardrobe.eq); const f=plush.userData.cb.shoes[0]; const a=[Array.isArray(f.material) && f.material[1]===CB_GLOW, f.geometry.groups.length];
      wardrobe.eq={body:'av_cubo', kshoe:'krz_tenis'}; applyOutfit(plush,wardrobe.eq); return [...a, plush.userData.cb.shoes[0].material===CB_MAT]; })()""")
    ok(r==[True,2,True], 'los tenis con luces llevan cubitos que brillan; los demás zapatos, el material normal %s'%r)
    # 7. fotos de las prendas (solo la prenda, sin piel ni cabeza)
    r=await ev("""(()=>{ const ids=['kra_sudadera','krb_overol','krz_vaquera','kt_roja_c','krb_tutu']; const out=ids.map(id=>{ const u=itemPhoto(SHOP_BY[id]); return [id, typeof u==='string' && u.length>500]; });
      const R=phRigGet(), C=R.o && R.o.userData.cb; return [out, C?C.head.visible:null, R.o?R.o.userData.avKey:'?']; })()""")
    ok(r[0] and all(x[1] for x in r[0]) and r[1]==True and r[2]==None, 'fotos de prendas del Cubito (sudadera, overol, botas, playera básica, tutú) %s'%r)
    # 8. los demás lo ven igual
    r=await ev("""(()=>{ wardrobe.eq={body:'av_cubo', ktop:'kra_animal_dino', kbot:'krb_tutu_lila', kshoe:'krz_pantuani_rana'}; const ou=outfitList(wardrobe.eq), eq=parseOutfit(ou); const R=makeRemote(3,'Bea'); applyOutfit(R.obj,eq); const L=R.obj.userData.cbLook;
      return [L.top.tk, L.top.ear, L.bot.bk, L.shoe.sk, L.shoe.ear, JSON.stringify(ou).length]; })()""")
    ok(r[:5]==['hoodear','dino','tutu','pantuani','rana'], 'otro jugador lo ve igual: sudadera de dino, tutú y pantuflas de rana (%s letras)'%r[5])
    # 9. inglés
    r=await ev("""(()=>{ I18N.set('en'); const t=['Arriba','Abajo','Sudadera amarilla','Falda a cuadros','Botas vaqueras cafés',NEWS['258'][0],NEWS['258'][1]].map(x=>I18N.t(x)); I18N.set('es'); return t; })()""")
    ok(r[0]!='Arriba' and r[1]!='Abajo' and r[2]!='Sudadera amarilla' and r[5].startswith('The Cubie') and r[6].startswith('Skirts'), 'en inglés: %s'%r)
    ok(not errs, 'sin errores %s'%errs[:3])
    await b.close()
asyncio.run(m())
