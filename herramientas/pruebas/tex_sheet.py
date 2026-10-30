import asyncio, sys, base64
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
src, out = sys.argv[1], sys.argv[2]
hook='''<script>window.__texs=[];</script>'''
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open(src).read()
# hook after three loads
html=html.replace('<script>\n(() => {', '<script>{ const CT=THREE.CanvasTexture; THREE.CanvasTexture=class extends CT{ constructor(c,...a){ super(c,...a); try{ const st=(new Error().stack||"").split("\\n")[2]||""; const m=st.match(/:(\\d+):\\d+\\)?$/); (window.__texs=window.__texs||[]).push([c, m?+m[1]:0]); }catch(e){} } }; }</script>\n<script>\n(() => {',1)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    pg=await b.new_page(viewport={"width":800,"height":450}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_timeout(12000)
    await pg.evaluate("document.getElementById('playBtn')&&document.getElementById('playBtn').click()"); await pg.wait_for_timeout(4000)
    data=await pg.evaluate("""(()=>{ const T=window.__texs.filter(([c])=>c && c.width>=16 && c.getContext); const seen=new Set(); const L=[]; for(const t of T){ if(seen.has(t[0])) continue; seen.add(t[0]); L.push(t); }
      const S=150, cols=8, rows=Math.ceil(L.length/cols); const out=document.createElement('canvas'); out.width=cols*S; out.height=rows*(S+14); const g=out.getContext('2d'); g.fillStyle='#777'; g.fillRect(0,0,out.width,out.height);
      L.forEach(([c,ln],i)=>{ const x=(i%cols)*S, y=Math.floor(i/cols)*(S+14); const k=Math.min(S/c.width,S/c.height); g.drawImage(c,x,y,c.width*k,c.height*k); g.fillStyle='#000'; g.font='11px sans-serif'; g.fillText(ln+' '+c.width+'x'+c.height,x+2,y+S+11); });
      return [out.toDataURL(), L.length]; })()""")
    open(out,'wb').write(base64.b64decode(data[0].split(',')[1])); print('n',data[1],'errs',errs[:3])
    await b.close()
asyncio.run(m())
