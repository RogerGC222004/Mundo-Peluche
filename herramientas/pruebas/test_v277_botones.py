# v277 (ronda B, punto 7): lo que traes en la mano manda (botón grande) y las acciones del lugar van en botoncitos redondos con dibujito junto a Gestos (pantalla táctil, horizontal)
import asyncio, os, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>[hidden]{display:none!important}</style>'+open(os.environ.get('JUEGO','/home/claude/mundo-peluche.html')).read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ctx=await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, locale='es-MX'); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, autoRes:false}));")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000); await pg.wait_for_timeout(800)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    await ev("window.requestAnimationFrame=()=>0; window.__run=(sec)=>{ let t=clock.elapsedTime; const n=Math.round(sec/.05); for(let i=0;i<n;i++){ clock.elapsedTime=(t+=.05); update(.05,t); updateSky(.05); } }; startGame(); 1"); await pg.wait_for_timeout(1200); await ev("__run(1); 1")
    SNAP="""const big=ui('actions').hidden?[]:[...document.querySelectorAll('#actions .act')].filter(b=>!b.hidden).map(b=>b.textContent.trim()), ic=[...document.querySelectorAll('#pacts .pact')].map(b=>b.textContent.trim()), pr=ui('pacts').getBoundingClientRect(), gr=ui('tGest').getBoundingClientRect(), jr=ui('tJump').getBoundingClientRect(), dr=ui('tDive').getBoundingClientRect();
      const ov=(a,c)=>a.left<c.right && c.left<a.right && a.top<c.bottom && c.top<a.bottom, P=[...document.querySelectorAll('#pacts .pact')].map(b=>b.getBoundingClientRect()), wr=ui('tWave').getBoundingClientRect(), hr=ui('hotbar').getBoundingClientRect();
      const s={big, ic, istouch:isTouch, row:!ui('pacts').classList.contains('col'), choca:P.some(p=>ov(p,gr)||ov(p,jr)||ov(p,dr)||ov(p,wr)||ov(p,hr))||P.some((p,i)=>P.some((q,j)=>j>i&&ov(p,q))), dentro:P.every(p=>p.left>=0 && p.top>=0 && p.bottom<=innerHeight), lay:ui('touch').classList.contains('lay277'), s2:P.length>1?[Math.round(dr.left-P[1].right), Math.round(P[1].top-dr.top)]:null};"""
    print(await ev("JSON.stringify([isTouch, innerWidth, innerHeight])"))
    # 1. con nieve y el arco en la mano: «Disparar» en el botón grande; la bola y el muñeco en botoncitos
    r=json.loads(await ev("""(()=>{ window.__wos=weatherOfSlot; weatherOfSlot=k=>'snow'; arWarp(0,groundAt(0,30,999)+.1,30,0); for(let i=0;i<40;i++) __run(.5); if(!bowHeld()) useSlot(1); hook.mode=0; __run(.2); scanActions(); %s return JSON.stringify({...s, ws:+WX.s.toFixed(2)}); })()"""%SNAP))
    ok(r['istouch'] and r['big']==['Disparar'] and r['ic']==['Hacer bola','Hacer muñeco'], 'con nieve y el arco: «Disparar» en el botón grande y la nieve en botoncitos %s'%[r['big'],r['ic'],r['ws']])
    ok(r['lay'] and not r['choca'] and r['dentro'] and r['s2'] and 0<=r['s2'][0]<20 and r['s2'][1]<40, 'acomodo nuevo: el 1º botoncito a la izquierda de Saludar y el 2º junto a Tirarse, sin tapar ningún botón ni la barra %s'%[r['lay'],r['choca'],r['dentro'],r['s2']])
    # 2. con nieve y sin nada en la mano: el centro queda libre; tocar el botoncito hace la bola
    r=json.loads(await ev("""(()=>{ holding=false; applyHeld(); renderHotbar(); __run(.2); scanActions(); %s const b=document.querySelector('#pacts .pact'); b.dispatchEvent(new PointerEvent('pointerdown',{pointerType:'touch',bubbles:true})); __run(.1); scanActions(); const big2=[...document.querySelectorAll('#actions .act')].filter(b=>!b.hidden && !ui('actions').hidden).map(b=>b.textContent.trim());
      return JSON.stringify({...s, ball:!!WI2.ball, big2}); })()"""%SNAP))
    ok(r['big']==[] and r['ic']==['Hacer bola','Hacer muñeco'], 'con nieve y sin nada en la mano no hay botón grande en medio, solo los botoncitos %s'%[r['big'],r['ic']])
    ok(r['ball'] and len(r['big2'])==1 and 'Lanzar bola de nieve' in r['big2'][0], 'al tocar el botoncito haces la bola y «Lanzar» pasa al botón grande %s'%[r['ball'],r['big2']])
    # 3. junto al camello: botoncito con su dibujito; montado: botón grande para bajarte
    r=json.loads(await ev("""(()=>{ weatherOfSlot=window.__wos; WI2.ball=false; WX.s=0; const K=DES.camel; arWarp(K.x+1.6,groundAt(K.x+1.6,K.z,999)+.1,K.z,0); __run(.5); scanActions(); %s const ico=[...document.querySelectorAll('#pacts .pact use')].map(u=>u.getAttribute('href'));
      desCamelStart(); __run(1); scanActions(); const big2=[...document.querySelectorAll('#actions .act')].filter(b=>!b.hidden && !ui('actions').hidden).map(b=>b.textContent.trim()), ic2=document.querySelectorAll('#pacts .pact').length; stopPlay(); __run(1);
      return JSON.stringify({...s, ico, big2, ic2}); })()"""%SNAP))
    ok(r['big']==[] and r['ic']==['Montar el camello'] and r['ico']==['#emi-huella'], 'junto al camello sale el botoncito «Montar el camello» con su dibujito %s'%[r['big'],r['ic'],r['ico']])
    ok(r['big2']==['Bajarse del camello'] and r['ic2']==0, 'montado en el camello, «Bajarse» va en el botón grande como siempre %s'%[r['big2'],r['ic2']])
    # 4. al cambiar de idioma los botoncitos también cambian
    r=json.loads(await ev("""(async()=>{ weatherOfSlot=k=>'snow'; arWarp(0,groundAt(0,30,999)+.1,30,0); for(let i=0;i<10;i++) __run(.5); scanActions(); I18N.set('en'); await new Promise(r=>setTimeout(r,150)); scanActions(); const en=[...document.querySelectorAll('#pacts .pact')].map(b=>b.textContent.trim()); I18N.set('es'); await new Promise(r=>setTimeout(r,150)); scanActions(); const es=[...document.querySelectorAll('#pacts .pact')].map(b=>b.textContent.trim()); weatherOfSlot=window.__wos; return JSON.stringify({en,es}); })()"""))
    ok(len(r['en'])==2 and r['en']!=r['es'] and r['es']==['Hacer bola','Hacer muñeco'], 'los botoncitos se traducen y regresan a español %s'%r)
    # 5. la ruedita de gestos a la medida de la pantalla; el acomodo nuevo de fábrica y quien ya movió sus botones conserva el suyo
    r=json.loads(await ev("""(()=>{ gwOpen(); const r1=GW.geo.r1, r0=GW.geo.r0; gwClose(); const def=ui('touch').classList.contains('lay277');
      settings.layout={land:{tJump:{x:-.02,y:0,s:1}}}; applyLayout(); const mine=ui('touch').classList.contains('lay277'); settings.layout={}; applyLayout(); const back=ui('touch').classList.contains('lay277');
      return JSON.stringify({r1, r0, H:innerHeight, def, mine, back}); })()"""))
    ok(abs(r['r1']-r['H']*.3)<2 and r['r0']<44, 'la ruedita de gestos mide 30 %% del alto de la pantalla (antes casi todo el alto) %s'%r)
    ok(r['def'] and not r['mine'] and r['back'], 'el acomodo nuevo es el de fábrica; si ya moviste tus botones se queda el tuyo; «Restablecer» vuelve al nuevo %s'%r)
    print('errores', len(errs)); [print('  E:',e[:300]) for e in dict.fromkeys(errs)]
    await b.close()
asyncio.run(m())
