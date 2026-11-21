# Junta las traducciones (tr_*.txt) y las mete al juego entre /*I18N-R2-INICIO*/ y /*I18N-R2-FIN*/ (se puede correr muchas veces)
import json, re, glob, os
D=os.path.dirname(os.path.abspath(__file__))   # (en el repo: herramientas/idioma)
GAME='/home/claude/mundo-peluche.html'
def lines(f): return [l for l in open(f,encoding='utf-8').read().split('\n') if l.strip()]
pairs={}   # es -> en
tmpl=[]    # (es, en) con ${...} o {n}
def put(es,en):
    es=es.strip(); en=en.strip()
    if not es or not en or en=='-' or es==en: return
    if '${' in es or re.search(r'\{n\}',es): tmpl.append((es,en)); return
    pairs[es]=en
shop=json.load(open(D+'/shop_u.json',encoding='utf-8'))
for f in sorted(glob.glob(D+'/tr_shop_*.txt')):
    for l in lines(f): i,en=l.split('|',1); put(shop[int(i)],en)
cat=json.load(open(D+'/cat_u.json',encoding='utf-8'))
for f in sorted(glob.glob(D+'/tr_cat_*.txt')):
    for l in lines(f): i,en=l.split('|',1); put(cat[int(i)],en)
for f in sorted(glob.glob(D+'/tr_kv_*.txt'))+[D+'/tr_pf.txt']:
    for l in lines(f): es,en=l.split('|',1); put(es,en)
segs=json.load(open(D+'/segs.json',encoding='utf-8'))
for f in sorted(glob.glob(D+'/tr_seg_*.txt')):
    for l in lines(f): i,en=l.split('|',1); put(segs[int(i)][1],en)
# plantillas → patrones
PH=re.compile(r'\$\{(?:[^{}]|\{[^{}]*\})*\}|\{n\}')
rx=[]
for es,en in tmpl:
    parts=PH.split(es); phs=PH.findall(es)
    if not any(re.search(r'\p{L}' if False else r'[A-Za-zÁ-úñ]',p) for p in parts): continue
    pat='^'+'(.+?)'.join(re.escape(p) for p in parts)+'$'
    pat=pat.replace('/','\\/')
    # en: cada ${...} se cambia por su grupo (mismo texto de expresión, en orden)
    used=[]; segs_en=[]; last=0; js=[]
    for m in PH.finditer(en):
        lit=en[last:m.start()]; last=m.end()
        try: gi=next(k for k,p in enumerate(phs) if p==m.group(0) and k not in used)
        except StopIteration: gi=None
        if gi is None: js.append(json.dumps(lit+m.group(0),ensure_ascii=False)); continue
        used.append(gi); js.append(json.dumps(lit,ensure_ascii=False)); js.append('txl(m[%d])'%(gi+1))
    js.append(json.dumps(en[last:],ensure_ascii=False))
    rx.append('[/%s/, m=>%s]'%(pat,'+'.join(x for x in js if x!='""') or '""'))
man=open(D+'/tr_rx_manual.js',encoding='utf-8').read().strip().rstrip(',')
if man: rx.insert(0,man)
body='I18N.add('+json.dumps(pairs,ensure_ascii=False,indent=0)+');\nI18N.rx([\n'+',\n'.join(rx)+'\n]);\n'
s=open(GAME,encoding='utf-8').read()
A,B='/*I18N-R2-INICIO*/','/*I18N-R2-FIN*/'
blk=A+'\n// v255 rondas 2 y 3: tienda, mascotas, peces, casita, taller, avisos, diálogos, minijuegos (generado)\n'+body+B
if A in s: s=s[:s.index(A)]+blk+s[s.index(B)+len(B):]
else: s=s.replace('I18N.start();',blk+'\nI18N.start();',1)
open(GAME,'w',encoding='utf-8').write(s)
print('pares',len(pairs),'patrones',len(rx))
