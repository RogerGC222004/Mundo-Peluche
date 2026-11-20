# Hojas para revisar todos los íconos: grande, tamaño real en botones claros, verdes y oscuros
import sys, asyncio, importlib
sys.path.insert(0,'.')
mods=[importlib.import_module(m) for m in ('ic_r1','ic_r2','ic_r3','ic_r4')]
I={}; NOM={}; E={}
for m in mods: I.update(m.I); NOM.update(getattr(m,'NOM',{})); E.update(m.E)
by={}
for e,n in E.items(): by.setdefault(n,[]).append(e)
names=list(I.keys())
PER=48
from playwright.async_api import async_playwright
def page(chunk,k):
    cells=''
    for n in chunk:
        svg=I[n]; em=' '.join(by.get(n,[]))
        cells+=(f'<div class="c"><svg viewBox="0 0 40 40" class="big">{svg}</svg>'
                f'<div class="row"><span class="b1"><svg viewBox="0 0 40 40">{svg}</svg> Aa</span><span class="b2"><svg viewBox="0 0 40 40">{svg}</svg></span><span class="b3"><svg viewBox="0 0 40 40">{svg}</svg></span><svg viewBox="0 0 40 40" class="tiny">{svg}</svg></div>'
                f'<div class="n">{NOM.get(n,n)} <i>{em}</i></div></div>')
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#fbf4e6;font-family:sans-serif;color:#5a4426;width:1600px}} h1{{font-size:22px;margin:10px 16px}}
.g{{display:grid;grid-template-columns:repeat(8,1fr);gap:8px;padding:0 12px 12px}}
.c{{background:#fff;border:2px solid #ead9b8;border-radius:14px;padding:6px;text-align:center}}
.big{{width:96px;height:96px}} .row{{display:flex;gap:5px;justify-content:center;align-items:center;margin-top:4px}}
.row span{{display:flex;align-items:center;gap:3px;border-radius:9px;padding:3px 6px;font-weight:800;font-size:14px}}
.b1{{background:#fffdf6;border:2px dashed #c9bfa3}} .b2{{background:#a6d64a}} .b3{{background:#2f3a52}}
.row svg{{width:21px;height:21px}} .tiny{{width:16px;height:16px}} .n{{font-size:12px;font-weight:700;margin-top:3px}} .n i{{font-style:normal;font-family:"Noto Color Emoji"}}
</style></head><body><h1>Revisión de íconos — hoja {k+1}</h1><div class="g">{cells}</div></body></html>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1600,'height':800}, device_scale_factor=1.5)
        for k in range(0,len(names),PER):
            await pg.set_content(page(names[k:k+PER],k//PER)); await pg.wait_for_timeout(200)
            await pg.screenshot(path=f'rev_{k//PER+1}.png', full_page=True)
        await b.close()
asyncio.run(main()); print(len(names),'íconos en',(len(names)+PER-1)//PER,'hojas')
