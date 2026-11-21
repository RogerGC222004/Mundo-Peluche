# v252: la linterna se detiene en paredes y cosas; la lluvia y la nieve no pasan debajo de lo que tiene algo encima
#  A) en el castillo (X -8 · Z 7, donde lo notó Roger) apuntando a la pared, la luz se queda en la pared (antes la atravesaba)
#     y también en 3ª persona; mirando al techo del primer piso la luz se queda abajo del segundo piso
#  B) afuera, apuntando al piso, sigue alumbrando el piso como antes
#  C) árboles, rocas y cosas tapan la luz; lo que está en el segundo piso no tapa la luz del primero
#  D) la lluvia y la nieve no pasan debajo del segundo piso del castillo, pero sí caen afuera y en el campo abierto
#  E) el «mapa de techos»: debajo de una isla flotante y debajo de un bloque del Modo libre no llueve; al quitar el bloque, vuelve a llover
#  (se puede correr con otro archivo del juego: python3 test_v252_linterna_lluvia.py /ruta/al/juego.html)
import asyncio, json, re, sys
from playwright.async_api import async_playwright
JUEGO=sys.argv[1] if len(sys.argv)>1 else '/home/claude/mundo-peluche.html'
REAL=open('threerepo/build/three.min.js').read()
SRC=open(JUEGO, encoding='utf-8').read(); VER=re.search(r"const GAME_VERSION='(\d+)'",SRC).group(1)
pre='<script>window.__off=0; const _dn=Date.now.bind(Date); Date.now=()=>_dn()+window.__off;</script>'
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+pre+SRC.replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
NOCHE="(()=>{ const n=Date.now(); const cur=((n/1000)%DAY_LEN)/DAY_LEN; window.__off+=((.75-cur)*DAY_LEN*1000); return 1; })()"
# gotitas/copos que se dibujan: [x,y,z] de cada una (las escondidas tienen y=-9999)
GOTAS="""(()=>{ const out=[]; if(rainFx.mesh.visible){ const a=rainFx.pos, n=rainFx.mesh.geometry.drawRange.count/2; for(let i=0;i<n;i++) out.push([a[i*6],a[i*6+1],a[i*6+2]]); } return out; })()"""
COPOS="""(()=>{ const out=[]; if(snowFx.mesh.visible){ const a=snowFx.pos, n=snowFx.mesh.geometry.drawRange.count; for(let i=0;i<n;i++) out.push([a[i*3],a[i*3+1],a[i*3+2]]); } return out; })()"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True)
    pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low',qDef:1,hints:false,weather:false})); localStorage.setItem('mundoPelucheEcon124','1'); localStorage.setItem('mundoPelucheNovedades','%s');"%VER)
    async def route(r):
      u=r.request.url
      if u.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in u: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev(NOCHE); await ev("startGame(); selectedSlot=hotbar.indexOf('lamp'); holding=true; applyHeld(); 1"); await pg.wait_for_timeout(1200)
    async def ir(x,z,cam,yw,pt=-.1):
      await ev("(()=>{ const g=groundAt(%f,%f,1); player.pos.set(%f,g,%f); player.vel.set(0,0,0); player.vy=0; setCam('%s'); yaw=%f; pitch=%f; player.facing=yaw+Math.PI; return 1; })()"%(x,z,x,z,cam,yw,pt))
      await pg.wait_for_timeout(900)
    LUZ="""(()=>{ const M=plush.userData.mg, s=M.spot, o=M.org; camera.updateMatrixWorld(); let near=99;
      for(const v of WL.V){ if(v.w<=0) continue; const q=new THREE.Vector3(v.x,v.y,v.z).applyMatrix4(camera.matrixWorld); near=Math.min(near,q.distanceTo(s)); }
      let top=-99; for(const v of WL.V){ if(v.w<=0) continue; const q=new THREE.Vector3(v.x,v.y,v.z).applyMatrix4(camera.matrixWorld); if(Math.hypot(q.x-o.x,q.z-o.z)<12) top=Math.max(top,q.y); }
      return {d:Math.hypot(s.x,s.z), dist:Math.hypot(s.x-o.x,s.y-o.y,s.z-o.z), y:s.y, near, top, inner:CAKE.wallR-CAKE.wallT, H:CAKE.H, lamp:M.lamp.visible}; })()"""

    # A) en el castillo, hacia la pared
    await ir(-8,7,'first',3.14159)
    r=await ev(LUZ)
    ok(r['lamp'] and r['d']<r['inner'] and r['dist']<7, '🔦 1ª persona en X -8 · Z 7 apuntando a la pared: la luz se queda en la pared (a %.1f m de ti, la pared está a %.1f m del centro y la luz a %.1f)'%(r['dist'],r['inner'],r['d']))
    ok(r['near']<.6, '💡 y ahí mismo se pone la luz que alumbra la pared (a %.2f m de donde pega)'%r['near'])
    await ir(-8,7,'third',3.14159)
    r=await ev(LUZ)
    ok(r['d']<r['inner'] and r['dist']<7, '🔦 en 3ª persona también se queda en la pared (a %.1f m)'%r['dist'])
    await ir(-1,-1,'first',0,.9)
    r=await ev("(()=>{ const o=%s; o.piso2=cakeFloorGround(-1,-1,100); return o; })()"%LUZ)
    ok(r['piso2']==r['H'] and r['y']<r['H'] and r['top']<r['H'], '⬆️ en X -1 · Z -1 mirando al techo: la luz se queda abajo del segundo piso (pega a %.1f m de alto, el piso de arriba está a %.1f; luz más alta %.1f)'%(r['y'],r['H'],r['top']))

    # B) afuera, al piso
    await ir(0,30,'first',3.14159,-.4)
    r=await ev("(()=>{ const M=plush.userData.mg, s=M.spot, o=M.org; return [s.y-groundAt(s.x,s.z,s.y+.5), Math.hypot(s.x-o.x,s.z-o.z)]; })()")
    ok(-.05<r[0]<.9 and 1.5<r[1]<6, '🌱 afuera, mirando al piso, la linterna alumbra el piso enfrente (a %.1f m, %.2f m arriba del piso)'%(r[1],r[0]))
    await ir(0,30,'third',3.14159)
    r=await ev("(()=>{ const M=plush.userData.mg, s=M.spot, o=M.org; return [s.y-groundAt(s.x,s.z,s.y+.5), Math.hypot(s.x-o.x,s.z-o.z)]; })()")
    ok(-.05<r[0]<.9 and r[1]>4, '🌱 y en 3ª persona también llega al piso como antes (a %.1f m, %.2f m arriba del piso)'%(r[1],r[0]))

    # C) árboles, rocas y cosas; lo de arriba no tapa lo de abajo
    r=await ev("""(()=>{ let tapa=0, n=0, alto=0, nA=0;
      for(const o of obstacles){ if(o.r<.3) continue; const gb=groundAt(o.x,o.z,o.top-.5), t=terrainH(o.x,o.z); if(o.top-gb<.6) continue;
        if(n<40 && !o.cake){ n++; if(lampBlocked(o.x,Math.min(o.top-.1,gb+.5),o.z)) tapa++; }
        if(!o.cake && gb>t+5 && FI.some(I=>Math.hypot(o.x-I.x,o.z-I.z)<I.R)){ nA++; if(!lampBlocked(o.x,t+1,o.z) && lampBlocked(o.x,o.top-.1,o.z)) alto++; } }
      let muro=0, nM=0; for(const o of obstacles) if(o.cake && o.bot===undefined && Math.abs(Math.hypot(o.x,o.z)-CAKE.wallR)<.5 && o.top>CAKE.H-.1){ nM++; if(lampBlocked(o.x,1.5,o.z)) muro++; }
      return [tapa,n,alto,nA,muro,nM]; })()""")
    ok(r[1]>=20 and r[0]==r[1], '🌳 árboles, rocas y cosas tapan la luz (%d de %d)'%(r[0],r[1]))
    ok(r[3]>0 and r[2]==r[3], '☁️ lo que está en las islas flotantes tapa la luz allá arriba, pero no la de abajo (%d de %d)'%(r[2],r[3]))
    ok(r[5]>100 and r[4]==r[5], '🏰 toda la muralla del castillo tapa la luz (%d de %d pedacitos)'%(r[4],r[5]))

    # D) lluvia y nieve en el castillo (aquí se revisa que quede bien; lo rápido que se arma el mapa se ve aparte)
    r=await ev("[ROOF.per, ROOF.ttl]")
    ok(r[0]==1800 and r[1]==30, '⏱️ el mapa de techos revisa unos %d cuadritos por segundo y cada uno dura %d s'%(r[0],r[1]))
    await ev("settings.weather=true; weatherOfSlot=()=>'rain'; ROOF.per=60000; 1")
    await ir(-8,7,'first',3.14159,0); await pg.wait_for_timeout(3500)
    BAJO="(g=>{ let bajo=0, afuera=0; for(const [x,y,z] of g){ if(y<-9000) continue; const d=Math.hypot(x,z); if(d<CAKE_ST.r0-.6 && !cakeHole(x,z) && y<CAKE.H-.1) bajo++; else afuera++; } return [bajo,afuera,g.length]; })(%s)"
    r=await ev(BAJO%GOTAS)
    ok(r[2]>100 and r[0]==0 and r[1]>40, '🌧️ lloviendo, en el primer piso del castillo no cae lluvia (%d gotitas abajo del segundo piso; %d sí caen afuera o arriba, de %d)'%(r[0],r[1],r[2]))
    await ev("weatherOfSlot=()=>'snow'; 1"); await pg.wait_for_timeout(3500)
    r=await ev(BAJO%COPOS)
    ok(r[2]>100 and r[0]==0 and r[1]>40, '❄️ nevando, tampoco nieva en el primer piso (%d copos abajo; %d sí caen afuera o arriba, de %d)'%(r[0],r[1],r[2]))
    await ev("weatherOfSlot=()=>'rain'; 1")
    await ir(0,30,'third',0); await pg.wait_for_timeout(3000)
    r=await ev("(g=>{ let vis=0, n=0; const d=rainFx.d, cy=camera.position.y, far=CAKE.towerR+2.2*CS+1;"
               +" for(let i=0;i<g.length;i++){ const [x,y,z]=g[i], yy=cy-12+d[i*3+1]; if(Math.hypot(x,z)<=far || yy<=terrainH(x,z)+.1) continue; n++; if(y>-9000) vis++; } return [vis,n]; })(%s)"%GOTAS)
    ok(r[1]>100 and r[0]>=r[1]*.97, '☔ al aire libre sí llueve normal (%d de %d gotitas arriba del pasto se ven)'%(r[0],r[1]))
    await ev("ROOF.per=1800; 1")

    # E) el mapa de techos
    r=await ev("(()=>{ const I=FI[0]; return [roofCalc(I.x,I.z), I.top(I.x,I.z), roofCalc(I.x+I.R+8,I.z)]; })()")
    ok(abs(r[0]-r[1])<.05 and r[2]<r[1]-10, '☁️ debajo de una isla flotante no llueve (techo a %.1f m) y a un lado sí (%.1f m)'%(r[0],r[2]))
    r=await ev("""(()=>{ freeEnter(); for(const o of [...FREE.objs]) freeDrop(o); const x=FREE.X+3.5, z=FREE.Z+3.5; const g0=ROOF.gen;
      const o=freeAddStatic({k:'b',a:0,b:2},x,FREE.Y+3,z,0,true); if(!o) return null; ROOF.bud=50; const con=roofTopAt(x,z), top=o.box.max.y, gen=ROOF.gen>g0;
      freeDrop(o); ROOF.bud=50; const sin=roofTopAt(x,z); return [con,top,sin,FREE.Y,gen]; })()""")
    ok(r and abs(r[0]-r[1])<.05 and r[4], '🧱 Modo libre: debajo de un bloque en el aire no llueve (techo a %.2f, el bloque llega a %.2f)'%(r[0],r[1]) if r else 'Modo libre: no se pudo poner el bloque')
    ok(r and abs(r[2]-r[3])<.05, '🧱 al quitar el bloque vuelve a llover ahí (techo a %.2f, el piso está a %.2f)'%(r[2],r[3]) if r else '')
    # la linterna en el Modo libre: una columna de bloques enfrente y una losa delgada arriba
    await ev("""(()=>{ player.pos.set(FREE.X+.5,FREE.Y+.05,FREE.Z+.5); player.vel.set(0,0,0); player.vy=0; setCam('first'); yaw=3.14159; pitch=0; player.facing=yaw+Math.PI;
      window.__B=[0,1,2].map(k=>freeAddStatic({k:'b',a:0,b:2},FREE.X+.5,FREE.Y+k,FREE.Z+3.5,0,true)); return 1; })()""")
    await pg.wait_for_timeout(900)
    r=await ev("(()=>{ const M=plush.userData.mg, s=M.spot, o=M.org, mz=Math.min(...__B.map(b=>b.box.min.z)); return [s.z, mz, Math.hypot(s.x-o.x,s.z-o.z), o.z]; })()")
    ok(r[0]<r[1] and r[0]>r[3] and r[1]-r[0]<.6, '🧱 la linterna se queda en los bloques del Modo libre (pega a %.2f m antes del bloque)'%(r[1]-r[0]))
    await ev("""(()=>{ for(const o of __B) freeDrop(o); window.__L=freeAddStatic({k:'b',a:FREE_SHAPES.findIndex(f=>f.id==='losa'),b:2},FREE.X+.5,FREE.Y+3,FREE.Z+.5,0,true); pitch=1.3; return 1; })()""")
    await pg.wait_for_timeout(900)
    r=await ev("(()=>{ const M=plush.userData.mg, s=M.spot, b=__L.box; return [s.y, b.min.y, b.max.y-b.min.y, M.org.y]; })()")
    ok(r[0]<r[1] and r[0]>r[3] and r[1]-r[0]<.6, '🪵 y también en una losa delgada (de %.2f m) arriba de ti: la luz se queda abajo (a %.2f m de la losa)'%(r[2],r[1]-r[0]))
    # los muros delgados de las casitas (una casita de prueba con un muro de 30 cm enfrente)
    await ev("(()=>{ freeDrop(__L); freeExit(); return 1; })()")
    r=await ev("""(()=>{ const L={x:50, z:50, y:0, c:Math.cos(.6), s:Math.sin(.6)}; HS.shown.set('__prueba',{L, cols:[[-2,0,-.15,2,3,.15]], doors:[{col:[2,0,-.15,3,2.5,.15], open:0},{col:[-3,0,-.15,-2,2.5,.15], open:1}], floors:new Map([['11,11',[0,3.2]]]), stairs:[]});
      const W=(lx,lz)=>lotW(L,lx,lz), T=(p,q)=>{ const a=W(p[0],p[1]), b=W(q[0],q[1]), dx=b[0]-a[0], dz=b[1]-a[1], n=Math.hypot(dx,dz); return lampBoxT(a[0],1.2,a[1],dx/n,0,dz/n,10); };
      const out=[T([0,-3],[0,3]), T([2.5,-3],[2.5,3]), T([-2.5,-3],[-2.5,3]), T([0,-3],[0,-9])]; const c=W(1,1); out.push(lampBoxT(c[0],1.2,c[1],0,1,0,10)); HS.shown.delete('__prueba'); return out; })()""")
    ok(abs(r[0]-2.85)<.02 and abs(r[1]-2.85)<.02 and r[2]<0 and r[3]<0, '🏠 los muros delgados de las casitas y las puertas cerradas detienen la luz (a %.2f y %.2f m); las puertas abiertas no, ni lo que está atrás de ti'%(r[0],r[1]))
    ok(abs(r[4]-1.82)<.02, '🏠 y el piso de arriba de una casita es techo para la luz de abajo (pega a %.2f m)'%r[4])
    ok(not errs, '🚫 sin errores (%s)'%errs[:3])
    await b.close()
asyncio.run(m())
