import asyncio, base64, json, sys, io, os
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw
REAL=open('threerepo/build/three.min.js').read()
SRC=sys.argv[1]; PREFIX=sys.argv[2]; FILTER=sys.argv[3] if len(sys.argv)>3 else ''
S=int(os.environ.get('SZ','220'))
pre='<script>window.__off=0; const _dn=Date.now.bind(Date); Date.now=()=>_dn()+window.__off; const _raf=window.requestAnimationFrame.bind(window); window.requestAnimationFrame=f=>window.__stop?0:_raf(f);</script>'
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+pre+open(SRC).read()
html=html.replace("function frame(){","window.__T={ev(s){ return eval(s); }}; function frame(){",1)
VIEWS=json.loads(os.environ.get('VIEWS','[[0,0.12,1],[0.9,0.1,1],[3.14,0.15,1],[0,0.9,1]]'))
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=await b.new_page(viewport={"width":S,"height":S}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.add_init_script("localStorage.setItem('mundoPelucheOpciones', JSON.stringify({quality:'high', qDef:1, hints:false, weather:false, shadows:false}))")
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=120000); await pg.wait_for_timeout(2000)
    await pg.evaluate("document.getElementById('playBtn').click()"); await pg.wait_for_timeout(1500)
    ev=lambda s: pg.evaluate("s=>__T.ev(s)", s)
    await ev("(()=>{ const n=Date.now(); const cur=((n/1000)%DAY_LEN)/DAY_LEN; window.__off+=((0.2-cur)*DAY_LEN*1000); window.__stop=true; return 1; })()")
    await pg.wait_for_timeout(300)
    if os.environ.get('SETUP'): print('setup', await ev(os.environ['SETUP']))
    # representantes: uno por forma distinta
    reps=await ev("""(()=>{ const seen={}, out=[]; for(const it of SHOP){ if(!it.k) continue; const sig=[it.k,it.ears,it.print,it.num?'n':'',it.zip,it.rev,it.len,it.animal,it.deco,it.scarf].join('|'); if(seen[sig]) continue; seen[sig]=1; out.push([it.id,it.slot,it.cat,it.name]); } return out; })()""")
    if FILTER:
      F=FILTER.split(','); reps=[r for r in reps if r[2] in F or r[0] in F or any(f.endswith('*') and r[0].startswith(f[:-1]) for f in F)]
    print('representantes', len(reps), flush=True)
    sheets={}
    for (iid,slot,cat,name) in reps:
      ims=[]
      for (ang,el,rk) in VIEWS:
        d=await ev(f"""(()=>{{ applyOutfit(plush,{{{slot}:'{iid}'}}); for(let i=0;i<3;i++) update(.016,300+i*.016);
          const P=player.pos, f=player.facing, C=camera, r={os.environ.get('CR','2.4')}*{rk}, a=f+{ang}, cy=P.y+{os.environ.get('CY','1.35')};
          C.position.set(P.x+Math.sin(a)*Math.cos({el})*r, cy+Math.sin({el})*r, P.z+Math.cos(a)*Math.cos({el})*r); C.lookAt(P.x,cy,P.z); C.updateMatrixWorld(true);
          renderer.render(scene,C); return canvas.toDataURL('image/png'); }})()""")
        ims.append(Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB'))
      w,h=ims[0].size; row=Image.new('RGB',(w*len(ims),h+16),'white'); dr=ImageDraw.Draw(row); dr.text((4,2),f'{iid} · {name}',fill=(0,0,0))
      for i,im in enumerate(ims): row.paste(im,(i*w,16))
      sheets.setdefault(cat,[]).append(row)
    for cat,rows in sheets.items():
      for k in range(0,len(rows),6):
        part=rows[k:k+6]; W=part[0].size[0]; H=sum(r.size[1] for r in part); c=Image.new('RGB',(W,H),'white'); y=0
        for r in part: c.paste(r,(0,y)); y+=r.size[1]
        c.save(f'{PREFIX}_{cat}_{k//6}.png')
    print('errores', errs[:4]); await b.close()
asyncio.run(m())
