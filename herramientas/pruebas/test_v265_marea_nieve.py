# v265: nieve y lluvia parejas (sin cuadros) con hoyitos al hacer bolas o muñecos, la marea de tormenta ya no tapa las entradas,
# el Modo libre más alto que las olas y ¡Al número! con portada y rondas de 30 segundos.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
SEED="""localStorage.clear(); localStorage.setItem('mundoPelucheEcon124','1');
localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'low', qDef:1, hints:false, weather:false, autoRes:false}));"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    pg=await (await b.new_context(viewport={"width":844,"height":390}, has_touch=True, is_mobile=True, locale='es-MX')).new_page(); errs=[]; cerr=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console",lambda msg: cerr.append(msg.text[:200]) if msg.type=='error' and ('Shader' in msg.text or 'WebGL' in msg.text or 'GL_' in msg.text) else None)
    await pg.add_init_script(SEED)
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=180000)


    # 1. ¡Al número!: portada en la lista y rondas de 30 segundos
    r=await ev("""(async()=>{ ONLINE.on=false; ui('mgBtn').click(); await new Promise(f=>setTimeout(f,300)); const cards=[...ui('mgqList').querySelectorAll('.mgq-g')];
      const c=cards.find(c=>c.textContent.includes('número')), pic=c&&c.querySelector('.pic'); const sinPortada=cards.filter(c=>{ const p=c.querySelector('.pic'); return p && !p.style.backgroundImage; }).length;
      return [!!c, !!pic && pic.style.backgroundImage.startsWith('url("data:image/webp'), pic?pic.textContent:'', sinPortada, NUMG.Q, NUMG.DUR>=NUMG.RND*(NUMG.Q+NUMG.DROP+NUMG.PAUSE), true]; })()""")
    ok(r[0] and r[1] and r[2]=='' and r[3]==0 and r[4]==30000 and r[5] and 'Tienes 30 segundos' in html and 'Tienes 10 segundos' not in html, '1 ¡Al número! tiene portada (ya ninguno sale sin foto) y cada ronda dura 30 s %s'%r)
    await ev("ui('mgqClose')&&ui('mgqClose').click(); 1")
    await ev("startGame()"); await pg.wait_for_timeout(1500)
    await ev("""(()=>{ window.requestAnimationFrame=()=>0; window.__run=(sec)=>{ let t=clock.elapsedTime; for(let i=0;i<Math.round(sec/.05);i++){ clock.elapsedTime=(t+=.05); update(.05,t); } }; __run(1); return 1; })()""")

    # 2. la nieve: hoyito solo donde se hizo la bola o el muñeco, y se vuelve a llenar
    r=await ev("""(()=>{ for(const h of WXU.H) h.w=0; wxDig(10,20,1.3); wxDig(30,20,.6); const a=WXU.H.filter(h=>h.w>0).map(h=>[h.x,h.y,h.z,h.w]);
      for(let i=0;i<10;i++) wxDig(i*5,0,1); const n8=WXU.H.filter(h=>h.w>0).length; wxHolesTick(20); const half=WXU.H[0].w; wxHolesTick(30); const after=WXU.H.filter(h=>h.w>0).length;
      return [JSON.stringify(a), n8, +half.toFixed(2), after]; })()""")
    ok(r[0]=='[[10,20,1.3,1],[30,20,0.6,1]]' and r[1]==8 and .4<r[2]<.75 and r[3]==0, '2 hacer nieve deja un hoyito en ese lugar (máximo 8 a la vez) y se rellena en 45 s %s'%r)
    # el techo: al poner o quitar algo (ROOF.gen cambia) lo que ya se sabía se sigue usando, sin quitar la nieve por cuadros
    r=await ev("""(()=>{ ROOF.bud=1e6; const P=player.pos, h0=roofTopAt(P.x+3,P.z+3); ROOF.gen++; ROOF.bud=0; const h1=roofTopAt(P.x+3,P.z+3), far=roofTopAt(P.x+5000,P.z+5000); return [Math.abs(h0-h1)<=1e-3*Math.max(1,Math.abs(h0)), far, h0, h1]; })()""")
    ok(r[0] and r[1]>1e8, '2b después de poner o quitar algo, el techo que ya se conocía se sigue usando (la nieve no se borra por cuadros) %s'%r)

    # 3. la marea de tormenta: sube en el mar, entra solo unos metros en la arena y nunca en las entradas
    r=await ev("""(()=>{ weatherOfSlot=()=>'storm'; __run(2); TIDE.h=1.3; for(let i=0;i<400 && !TIDE.cur;i++) tideTick(0); TIDE.h=1.3;
      const sp=TELEPORTS.filter(T=>/^ar_|^muelle$|^cohete$/.test(T.id)).map(T=>[T.id, +tideAt(T.x,T.z).toFixed(2)]);
      const dry=sp.filter(s=>s[1]>.02); let sea=0, open=0; for(let a=0;a<6.28;a+=.5){ const x=Math.cos(a)*1500, z=Math.sin(a)*1500; open++; if(tideAt(x,z)>1.25) sea++; }
      // tierra adentro (2 m o más sobre el mar) nunca le llega
      let inl=0, inN=0; for(let x=-600;x<=600;x+=40) for(let z=-600;z<=600;z+=40){ if(terrainH(x,z)>SEA_Y+2){ inN++; if(tideAt(x,z)>.01) inl++; } }
      return [JSON.stringify(dry), sea, open, inl, inN, !!TIDE.cur, TIDE.m.value===TIDE.cur.tex, sp.length]; })()""")
    ok(r[0]=='[]' and r[1]==r[2] and r[3]==0 and r[4]>50 and r[5] and r[6] and r[7]>=16, '3 con tormenta la marea sube 1.3 m en el mar, pero las entradas de los minijuegos, el muelle y el cohete quedan secos y tierra adentro no llega %s'%r)
    # en la arena: cerca del mar sí entra un poco (unos metros), pero nunca a tierra alta
    r=await ev("""(()=>{ let wet=0, far=0, mx=0; for(let a=0;a<6.283;a+=.13){ const sea=[], W=[]; for(let d=300; d<1400; d+=3){ const x=Math.cos(a)*d, z=Math.sin(a)*d, th=terrainH(x,z), t=tideAt(x,z);
        if(th<SEA_Y) sea.push(d); else if(SEA_Y+t>th+.02) W.push(d); }
        for(const d of W){ wet++; let m=1e9; for(const q of sea) m=Math.min(m,Math.abs(q-d)); mx=Math.max(mx,m); if(m>45) far++; } }
      return [wet, far, mx]; })()""")
    ok(r[0]>20 and r[1]==0, '3b con tormenta el mar sí se mete un poco en la arena (%d puntos mojados), a lo mucho %s m desde la orilla %s'%(r[0],r[2],r))
    # 4. el Modo libre: la planicie más alta que las olas más grandes (y el bloque llega hasta el mar)
    await ev("(()=>{ weatherOfSlot=()=>'storm'; ui('toMenuBtn').click(); return 1; })()"); await pg.wait_for_timeout(500)
    await ev("menuModes(true); ui('freeBtn').click(); 1"); await pg.wait_for_timeout(300)
    await ev("ui('freeSolo').click(); 1"); await pg.wait_for_timeout(1500); await ev("(__run(3), 1)")
    r=await ev("""(()=>{ const F=FREE.floor, bb=new THREE.Box3().setFromObject(F); let mx=0; for(const w of WAVES) mx+=Math.abs(w[4]); const top=SEA_Y+mx*(.22+.3+.15)*(1+.6+.6)+.1;   /* (las olas más grandes: viento, lluvia y tormenta al máximo) */
      return [FREE.on, FREE.Y, +bb.max.y.toFixed(2), +bb.min.y.toFixed(2), +top.toFixed(2), +player.pos.y.toFixed(2), player.swim, tideAt(FREE.X,FREE.Z), +WATER.seaA.toFixed(2)]; })()""")
    ok(r[0] and r[1]>=2 and abs(r[2]-r[1])<.01 and r[3]<-1.5 and r[4]<r[1]-1 and abs(r[5]-r[1])<.1 and not r[6] and r[7]==0, '4 Modo libre: la planicie (a %s m) queda más de 1 m arriba de las olas de tormenta (%s m), llega hasta abajo del mar y entras parado %s'%(r[1],r[4],r))
    # lo guardado se guarda relativo a la planicie: al subirla, todo sube con ella
    r=await ev("""(()=>{ for(const o of [...FREE.objs]) freeDrop(o); const X=FREE.X+3, Z=FREE.Z+3; freeAddStatic({k:'b',a:0,b:1},X,FREE.Y,Z,0); freeSave(); const S=JSON.parse(localStorage.getItem('mundoPelucheLibre')); const e=S.s[S.s.length-1]; return [e[3],e[4],e[5]]; })()""")
    ok(r==[3,0,3], '4b lo que pones se guarda contando desde la planicie (así sube junto con ella) %s'%r)

    ok(not errs and not cerr, 'sin errores %s %s'%(errs[:3],cerr[:3]))
    await b.close()
asyncio.run(m())
