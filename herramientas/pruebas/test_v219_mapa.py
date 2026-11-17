# v219: el mapa (1) cabe completo en teléfonos acostados (antes el estilo de «Mis creaciones» lo agrandaba y solo se veía
# la parte de arriba) y (2) en el Modo libre enseña tu planicie: tocas donde quieras ir y viajas ahí.
import asyncio
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    async def open_page(w,h,touch):
      ctx=await b.new_context(viewport={"width":w,"height":h}, has_touch=touch); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
      await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'min', qDef:1, hints:false, weather:false})); localStorage.setItem('mundoPelucheEcon124','1');")
      async def route(r):
        if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
        elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
        else: await r.abort()
      await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
      await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
      return ctx, pg, errs
    MAPJS="""(()=>{ %s window.requestAnimationFrame=()=>0; let t=clock.elapsedTime; for(let i=0;i<10;i++){ clock.elapsedTime=(t+=.05); update(.05,t); }
      const i=hotbar.indexOf('map'); selectedSlot=i; holding=true; applyHeld(); renderHotbar(); const c=ui('mapCanvas').getBoundingClientRect();
      return [Math.round(c.width), Math.round(c.top), Math.round(c.bottom), innerHeight, ui('mapTitle').textContent]; })()"""
    # 1. el mapa de la isla cabe completo (Doogee, Huawei y computadora)
    for (w,h,touch,tag) in [(876,393,True,'Doogee'),(780,360,True,'Huawei'),(1280,720,False,'computadora')]:
      ctx,pg,errs=await open_page(w,h,touch); ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 300)
      r=await ev(MAPJS%"startGame();")
      ok(r[0]>=240 and r[1]>=0 and r[2]<=r[3] and r[4]=='Mapa de la isla', 'mapa de la isla en %s (%sx%s): se ve completo (%s px, de %s a %s) %s'%(tag,w,h,r[0],r[1],r[2],r))
      if tag!='Doogee': await ctx.close(); continue
      # 2. «Mis creaciones» se sigue viendo bien
      r=await ev("(()=>{ selectedSlot=0; holding=false; applyHeld(); ui('toMenuBtn').click(); menuModes(true); ui('mapBtn').click(); const k=document.querySelector('#mapList .map-card').getBoundingClientRect(); const v=!ui('mapList').hidden; ui('mapList').hidden=true; return [v, Math.round(k.width), Math.round(k.bottom)<=innerHeight+1]; })()")
      ok(r[0] and r[1]>=500 and r[2], '«Mis creaciones» se sigue viendo como antes %s'%r)
      # 3. en el Modo libre: tu planicie
      r=await ev(MAPJS%"""(()=>{ freeEnter(); const X=FREE.X,Y=FREE.Y,Z=FREE.Z; for(let i=0;i<30;i++) freeAddStatic({k:'b',a:0,b:i%12},X+10+(i%6)+.5,Y,Z+10+Math.floor(i/6)+.5,0,true); freeAddStatic({k:'b',a:0,b:3},X+10.5,Y+1,Z+10.5,0,true); freeAddStatic({k:'n',a:'alberca',b:0},X-20,Y,Z-20,0,true); player.pos.set(X,Y+.05,Z); })();""")
      ok(r[2]<=r[3] and r[4]=='Mapa de tu planicie', 'en el Modo libre el mapa se llama «Mapa de tu planicie» y cabe completo %s'%r)
      r=await ev("""(()=>{ const hide=[getComputedStyle(ui('mapHouses')).display, getComputedStyle(document.querySelector('.map-flags')).display]; const z=+mapView.z.toFixed(1), [mx,my]=toFree(player.pos.x,player.pos.z);
        const near=Math.hypot(mx-mapView.cx,my-mapView.cy)<1; drawMap(true); const px=mctx.getImageData(...toScreen(...toFree(FREE.X+10.5,FREE.Z+10.5)).map(Math.round),1,1).data; return [hide.join(','), z, near, [...px].slice(0,3).join(',')]; })()""")
      ok(r[0]=='none,none' and r[1]==2.4 and r[2] and r[3]!='134,201,90', 'se ve acercado a donde estás, con lo que construiste (y sin las casas ni las banderas de la isla) %s'%r)
      r=await ev("""(()=>{ const [sx,sy]=toScreen(...toFree(FREE.X+10.5,FREE.Z+10.5)); freeMapGo(sx,sy); const a=[+(player.pos.x-FREE.X).toFixed(1), +(player.pos.z-FREE.Z).toFixed(1), +(player.pos.y-FREE.Y).toFixed(2)];
        const [ox,oy]=toScreen(...toFree(FREE.X+90,FREE.Z)); freeMapGo(ox,oy); const msg=ui('toast').textContent, b=+(player.pos.x-FREE.X).toFixed(1);
        mapView.z=1; clampView(); const [wx,wy]=toScreen(...toFree(FREE.X-20,FREE.Z-20)); freeMapGo(wx,wy); let t=clock.elapsedTime; for(let i=0;i<20;i++){ clock.elapsedTime=(t+=.05); update(.05,t); } return [a, msg, b, player.swim]; })()""")
      ok(r[0]==[10.5,10.5,2.05] and 'toca adentro' in r[1] and r[2]==10.5 and r[3], 'tocas el mapa y viajas ahí: arriba de los bloques (2 m), afuera de la planicie no; a la alberca y quedas nadando %s'%r)
      # 4. manejando el carrito también, y jugando un minijuego no se vale
      r=await ev("""(()=>{ const c=freeAddStatic({k:'v',a:'carrito',b:0},FREE.X-5,FREE.Y,FREE.Z+5,0,true); player.swim=false; player.pos.set(FREE.X-5,FREE.Y+.05,FREE.Z+3.9); pqRide(c,0); let t=clock.elapsedTime; for(let i=0;i<4;i++){ clock.elapsedTime=(t+=.05); update(.05,t); }
        const [sx,sy]=toScreen(...toFree(FREE.X+30,FREE.Z)); freeMapGo(sx,sy); return [player.pg, +(player.pos.x-FREE.X).toFixed(1), Math.abs(c.x-(FREE.X-5))<1]; })()""")
      ok(r[0] is None and r[1]==30 and r[2], 'si vas en el carrito, te bajas (se queda estacionado) y viajas %s'%r)
      r=await ev("""(()=>{ selectedSlot=0; holding=false; applyHeld(); ui('toMenuBtn').click(); menuModes(true); ui('mapBtn').click(); mapType='juego'; ui('mapName').value='Pista'; mapCreate(); medDone(); freePlayStart(); const p0=player.pos.clone();
        const i=hotbar.indexOf('map'); selectedSlot=i; holding=true; applyHeld(); const [sx,sy]=toScreen(...toFree(FREE.X+30,FREE.Z+30)); freeMapGo(sx,sy); const msg=ui('toast').textContent; return [player.pos.distanceTo(p0)<.01, msg]; })()""")
      ok(r[0] and 'no se vale' in r[1], 'jugando un minijuego no se vale viajar: «%s»'%r[1])
      # 5. al salir del Modo libre vuelve el mapa de la isla
      r=await ev("""(()=>{ selectedSlot=0; holding=false; applyHeld(); ui('toMenuBtn').click(); startGame(); const i=hotbar.indexOf('map'); selectedSlot=i; holding=true; applyHeld(); return [ui('mapTitle').textContent, document.body.classList.contains('map-free'), placeAt(...toScreen(...toMap(TELEPORTS[0].x,TELEPORTS[0].z)),true)===TELEPORTS[0]]; })()""")
      ok(r==['Mapa de la isla',False,True], 'al volver a la isla el mapa es el de siempre (con sus lugares para viajar) %s'%r)
      ok(not errs,'sin errores %s'%errs[:3]); await ctx.close()
    await b.close()
asyncio.run(m())
