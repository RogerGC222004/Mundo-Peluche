import sys, importlib, asyncio
sys.path.insert(0, sys.argv[1] if len(sys.argv)>1 else '.')
mod = importlib.import_module(sys.argv[2] if len(sys.argv)>2 else 'ic_r1')
out = sys.argv[3] if len(sys.argv)>3 else 'hoja_r1.png'
title = sys.argv[4] if len(sys.argv)>4 else 'Ronda 1'
I, E = mod.I, mod.E
NOM = getattr(mod, 'NOM', {})
# un emoji por ícono (el primero que lo usa) + los demás que comparten ícono
by = {}
for e, n in E.items(): by.setdefault(n, []).append(e)
cells = []
for n, svg in I.items():
    em = ' '.join(by.get(n, ['—']))
    cells.append(f'<div class="c"><div class="e">{em}</div><div class="ar">→</div>'
                 f'<svg viewBox="0 0 40 40" class="big">{svg}</svg>'
                 f'<div class="sm"><svg viewBox="0 0 40 40">{svg}</svg><span class="btn"><svg viewBox="0 0 40 40">{svg}</svg> Ejemplo</span></div>'
                 f'<div class="n">{NOM.get(n, n)}</div></div>')
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#fbf4e6;font-family:"Noto Sans",sans-serif;color:#5a4426;width:1500px}}
h1{{font-size:30px;margin:18px 24px 4px}} p{{margin:0 24px 14px;font-size:17px}}
.g{{display:grid;grid-template-columns:repeat(7,1fr);gap:10px;padding:0 18px 18px}}
.c{{background:#fff;border-radius:16px;border:2px solid #ead9b8;padding:8px 6px 6px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;justify-items:center;row-gap:4px}}
.e{{font-family:"Noto Color Emoji";font-size:38px;line-height:1;white-space:nowrap}} .ar{{font-size:20px;opacity:.5}}
.big{{width:60px;height:60px}}
.sm{{grid-column:1/4;display:flex;gap:8px;align-items:center}} .sm>svg{{width:29px;height:29px}}
.btn{{background:#ffe9b8;border:2px solid #5a4426;border-radius:10px;padding:2px 8px;font-weight:700;font-size:15px;display:flex;align-items:center;gap:4px}}
.btn svg{{width:1.25em;height:1.25em}}
.n{{grid-column:1/4;font-size:14px;font-weight:700}}
</style></head><body><h1>Íconos nuevos — {title}</h1>
<p>Izquierda: el emoji de hoy. Derecha: el ícono dibujado. Abajo: tamaño real en la barra y dentro de un botón.</p>
<div class="g">{''.join(cells)}</div></body></html>'''
open(out.replace('.png', '.html'), 'w').write(html)
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1500,'height':800}, device_scale_factor=2)
        await pg.set_content(html); await pg.wait_for_timeout(300)
        await pg.screenshot(path=out, full_page=True); await b.close()
asyncio.run(main())
print('ok', out)
