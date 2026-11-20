# Genera el módulo de íconos para el juego a partir de los archivos ic_r*.py
import sys, importlib, json
sys.path.insert(0, '.')
mods = sys.argv[1:] or ['ic_r1']
I, E = {}, {}
for m in mods:
    x = importlib.import_module(m); I.update(x.I); E.update(x.E)
assert all(v in I for v in E.values())
import re as _re
from ic_r1 import O as _O, HL as _HL
def _pack(v):   # (las partes que se repiten mucho van abreviadas y se arman al cargar)
    v=_re.sub(r'stroke="'+_O+r'" stroke-width="([\d.]+)" stroke-linejoin="round" stroke-linecap="round"', r'~\1~', v)
    return v.replace(_HL,'¤').replace('stroke="'+_O+'"','stroke="§"').replace('fill="'+_O+'"','fill="§"')
svg = ','.join(f"{k}:'{_pack(v)}'" for k, v in I.items())
emo = json.dumps(E, ensure_ascii=False, separators=(',', ':'))
js = f'''// ======================================================================================
// ---------------- v242: ÍCONOS DIBUJADOS EN LUGAR DE EMOJIS ----------------
// Cada emoji de la lista se cambia, donde aparezca en la pantalla, por un dibujo hecho a mano con el mismo estilo de la barra
// del Modo libre (contorno café, colores planos y un brillito). El emoji queda escondido dentro del dibujo, así el texto
// "por dentro" no cambia y todo lo que compara textos sigue igual. Lo que escribe un jugador (data-noic) no se toca.
// ======================================================================================
const EMI_SVG={{{svg}}};
const EMI_EMO={emo};
const EMI_HL='{_HL}';
let EMI_RE=null, EMI_N=0;
function emiRe(){{ if(!EMI_RE) EMI_RE=new RegExp('('+Object.keys(EMI_EMO).sort((a,b)=>b.length-a.length).join('|')+')\\uFE0F?','gu'); EMI_RE.lastIndex=0; return EMI_RE; }}
const EMI_TPL={{}};   // (cada dibujo se arma una vez y luego se copia: es más rápido)
function emiSpan(e,full){{ let t=EMI_TPL[full]; if(!t){{ const n=EMI_EMO[e]; t=EMI_TPL[full]=document.createElement('span'); t.className='emi'; t.setAttribute('aria-hidden','true');
    t.innerHTML='<svg class="emi-g" viewBox="0 0 40 40"><use class="emi-u" href="#emi-'+n+'"/></svg><span class="emi-t">'+full+'</span>'; }} return t.cloneNode(true); }}   // (adentro queda el emoji tal cual, con su variante)
function emiHtml(n){{ return '<span class="emi" aria-hidden="true"><svg class="emi-g" viewBox="0 0 40 40"><use class="emi-u" href="#emi-'+n+'"/></svg></span>'; }}   // (un dibujo por su nombre, sin emoji adentro)
function emiSkip(p){{ if(!p || p.namespaceURI!=='http://www.w3.org/1999/xhtml') return true; const t=p.tagName; if(t==='SCRIPT'||t==='STYLE'||t==='TEXTAREA'||t==='OPTION'||t==='TITLE'||t==='NOSCRIPT') return true; return !!p.closest('.emi,[data-noic]'); }}
function emiText(n){{ const d=n.data; if(!d || !emiRe().test(d)) return; const p=n.parentNode; if(emiSkip(p)) return; const re=emiRe(), f=document.createDocumentFragment(); let a=0, m;
  while((m=re.exec(d))){{ if(m.index>a) f.appendChild(document.createTextNode(d.slice(a,m.index))); f.appendChild(emiSpan(m[1],m[0])); a=m.index+m[0].length; }}
  if(a<d.length) f.appendChild(document.createTextNode(d.slice(a))); EMI_N++; p.replaceChild(f,n); }}
function emiTree(el){{ if(!el || el.nodeType!==1 || el.classList.contains('emi') || !emiRe().test(el.textContent)) return; const w=document.createTreeWalker(el,4), L=[]; let n; while((n=w.nextNode())) if(emiRe().test(n.data)) L.push(n); for(const t of L) emiText(t); }}
function emiNode(n){{ if(!n || !n.isConnected) return; if(n.nodeType===3) emiText(n); else emiTree(n); }}
function emiInit(){{ const st=document.createElement('style'); st.textContent='.emi{{display:inline-block;position:relative;width:1.2em;height:1.2em;vertical-align:-.22em;line-height:0;}} .emi-g{{width:100%;height:100%;display:block;overflow:visible;}} .emi-t{{position:absolute;left:0;top:0;font-size:0;opacity:0;pointer-events:none;}}';
  document.head.appendChild(st);
  const lib=document.createElementNS('http://www.w3.org/2000/svg','svg'); lib.setAttribute('aria-hidden','true'); lib.setAttribute('style','position:absolute;width:0;height:0;overflow:hidden');
  lib.innerHTML=Object.keys(EMI_SVG).map(k=>'<symbol id="emi-'+k+'" viewBox="0 0 40 40">'+EMI_SVG[k].replace(/~([\\d.]+)~/g,'stroke="§" stroke-width="$1" stroke-linejoin="round" stroke-linecap="round"').replace(/¤/g,EMI_HL).replace(/§/g,'#5a4426')+'</symbol>').join(''); document.body.insertBefore(lib,document.body.firstChild);
  emiTree(document.body);
  new MutationObserver(R=>{{ for(const r of R){{ if(r.type==='characterData') emiNode(r.target); else for(const n of r.addedNodes) emiNode(n); }} }}).observe(document.body,{{childList:true,subtree:true,characterData:true}}); }}
emiInit();
'''
open('emi_mod.js', 'w').write(js)
print(len(js), 'bytes;', len(I), 'iconos;', len(E), 'emojis')
