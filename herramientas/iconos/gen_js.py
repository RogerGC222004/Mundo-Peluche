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
function emiExpand(n){{ return EMI_SVG[n].replace(/~([\\d.]+)~/g,'stroke="§" stroke-width="$1" stroke-linejoin="round" stroke-linecap="round"').replace(/¤/g,EMI_HL).replace(/§/g,'#5a4426'); }}
// ---- v245: los mismos dibujos dentro de letreros pintados (canvas). Se pintan al momento con las mismas figuras, sin esperar imágenes ----
const EMI_OPS={{}};
function emiOps(n){{ if(EMI_OPS[n]) return EMI_OPS[n]; const ops=[];
  try{{ const doc=new DOMParser().parseFromString('<svg xmlns="http://www.w3.org/2000/svg">'+emiExpand(n)+'</svg>','image/svg+xml');
    const walk=(el,st,tf,op)=>{{ for(const c of el.children){{ const s2={{...st}}; for(const a of ['fill','stroke','stroke-width','stroke-linecap','stroke-linejoin','stroke-dasharray','font-size','font-weight','text-anchor']) if(c.hasAttribute(a)) s2[a]=c.getAttribute(a);
        const o2=op*(c.hasAttribute('opacity')?+c.getAttribute('opacity'):1), t2=c.hasAttribute('transform')?tf.concat([c.getAttribute('transform')]):tf, tag=c.tagName, A=k=>+c.getAttribute(k)||0;
        if(tag==='g'){{ walk(c,s2,t2,o2); continue; }} let p=null;
        if(tag==='path') p=new Path2D(c.getAttribute('d'));
        else if(tag==='circle'){{ p=new Path2D(); p.arc(A('cx'),A('cy'),A('r'),0,Math.PI*2); }}
        else if(tag==='ellipse'){{ p=new Path2D(); p.ellipse(A('cx'),A('cy'),A('rx'),A('ry'),0,0,Math.PI*2); }}
        else if(tag==='rect'){{ p=new Path2D(); const x=A('x'),y=A('y'),w=A('width'),h=A('height'),r=Math.min(A('rx'),w/2,h/2); if(r>0){{ p.moveTo(x+r,y); p.arcTo(x+w,y,x+w,y+h,r); p.arcTo(x+w,y+h,x,y+h,r); p.arcTo(x,y+h,x,y,r); p.arcTo(x,y,x+w,y,r); p.closePath(); }} else p.rect(x,y,w,h); }}
        else if(tag==='text'){{ ops.push({{txt:c.textContent,x:A('x'),y:A('y'),s:s2,t:t2,op:o2}}); continue; }}
        if(p) ops.push({{p,s:s2,t:t2,op:o2}}); }} }};
    walk(doc.documentElement,{{fill:'#000'}},[],1); }}catch(e){{}}
  return EMI_OPS[n]=ops; }}
function emiTf(g,t){{ const re=/(translate|scale|rotate)\\(([^)]*)\\)/g; let m; while((m=re.exec(t))){{ const v=m[2].split(/[\\s,]+/).filter(Boolean).map(Number);
    if(m[1]==='translate') g.translate(v[0]||0,v[1]||0); else if(m[1]==='scale') g.scale(v[0],v.length>1?v[1]:v[0]); else {{ const a=(v[0]||0)*Math.PI/180; if(v.length>2){{ g.translate(v[1],v[2]); g.rotate(a); g.translate(-v[1],-v[2]); }} else g.rotate(a); }} }} }}
function emiDraw(g,n,x,y,s){{ const ops=emiOps(n); if(!ops.length) return; g.save(); g.translate(x,y); g.scale(s/40,s/40); const a0=g.globalAlpha;
  for(const o of ops){{ g.save(); for(const t of o.t) emiTf(g,t); g.globalAlpha=a0*o.op; const st=o.s, f=st.fill, k=st.stroke;
    if(o.txt!==undefined){{ if(f!=='none'){{ g.fillStyle=f; g.font=(st['font-weight']||'700')+' '+(st['font-size']||12)+'px sans-serif'; g.textAlign=st['text-anchor']==='middle'?'center':st['text-anchor']==='end'?'right':'left'; g.textBaseline='alphabetic'; EMI_FT.call(g,o.txt,o.x,o.y); }} g.restore(); continue; }}
    if(f!=='none'){{ g.fillStyle=f; g.fill(o.p); }}
    if(k && k!=='none'){{ g.strokeStyle=k; g.lineWidth=+st['stroke-width']||1; g.lineCap=st['stroke-linecap']||'butt'; g.lineJoin=st['stroke-linejoin']||'miter'; g.setLineDash(st['stroke-dasharray']?st['stroke-dasharray'].split(/[\\s,]+/).map(Number):[]); g.stroke(o.p); }}
    g.restore(); }}
  g.restore(); }}
// un texto con emojis en un letrero: las letras como siempre y cada emoji de la lista con su dibujo, en el mismo lugar
const EMI_FT=CanvasRenderingContext2D.prototype.fillText, EMI_ST=CanvasRenderingContext2D.prototype.strokeText;
let EMI_CV=0;
function emiCanvasText(g,s,x,y,mw,stroke){{ EMI_CV++; const fs=parseFloat((String(g.font).match(/([\\d.]+)px/)||[0,16])[1])||16, re=emiRe(), seg=[]; let a=0, m;
  while((m=re.exec(s))){{ if(m.index>a) seg.push({{t:s.slice(a,m.index)}}); seg.push({{n:EMI_EMO[m[1]],e:m[0]}}); a=m.index+m[0].length; }} if(a<s.length) seg.push({{t:s.slice(a)}});
  const ta=g.textAlign; g.textAlign='left'; let W=0; for(const q of seg){{ q.w=q.t!==undefined ? g.measureText(q.t).width : (()=>{{ const w=g.measureText(q.e).width; return w>fs*.8 ? w : fs*1.15; }})(); W+=q.w; }}
  const k=mw>0 && W>mw ? mw/W : 1, bl=g.textBaseline, cy=bl==='middle' ? y : (bl==='top'||bl==='hanging') ? y+fs*.55 : (bl==='bottom'||bl==='ideographic') ? y-fs*.45 : y-fs*.33;
  let cx=ta==='center' ? x-W*k/2 : (ta==='right'||ta==='end') ? x-W*k : x;
  for(const q of seg){{ const w=q.w*k; if(q.t!==undefined){{ const f=stroke?EMI_ST:EMI_FT; if(k<1) f.call(g,q.t,cx,y,w); else f.call(g,q.t,cx,y); }} else if(!stroke){{ const sz=Math.min(fs*1.12,w*1.05); emiDraw(g,q.n,cx+(w-sz)/2,cy-sz/2,sz); }} cx+=w; }}
  g.textAlign=ta; }}
CanvasRenderingContext2D.prototype.fillText=function(s,x,y,mw){{ if(this.__noic || typeof s!=='string' || !emiRe().test(s)) return arguments.length>3 ? EMI_FT.call(this,s,x,y,mw) : EMI_FT.call(this,s,x,y); emiCanvasText(this,s,x,y,mw,false); }};
CanvasRenderingContext2D.prototype.strokeText=function(s,x,y,mw){{ if(this.__noic || typeof s!=='string' || !emiRe().test(s)) return arguments.length>3 ? EMI_ST.call(this,s,x,y,mw) : EMI_ST.call(this,s,x,y); emiCanvasText(this,s,x,y,mw,true); }};
function emiInit(){{ const st=document.createElement('style'); st.textContent='.emi{{display:inline-block;position:relative;width:1.2em;height:1.2em;vertical-align:-.22em;line-height:0;}} .emi-g{{width:100%;height:100%;display:block;overflow:visible;}} .emi-t{{position:absolute;left:0;top:0;font-size:0;opacity:0;pointer-events:none;}}';
  document.head.appendChild(st);
  const lib=document.createElementNS('http://www.w3.org/2000/svg','svg'); lib.setAttribute('aria-hidden','true'); lib.setAttribute('style','position:absolute;width:0;height:0;overflow:hidden');
  lib.innerHTML=Object.keys(EMI_SVG).map(k=>'<symbol id="emi-'+k+'" viewBox="0 0 40 40">'+emiExpand(k)+'</symbol>').join(''); document.body.insertBefore(lib,document.body.firstChild);
  emiTree(document.body);
  new MutationObserver(R=>{{ for(const r of R){{ if(r.type==='characterData') emiNode(r.target); else for(const n of r.addedNodes) emiNode(n); }} }}).observe(document.body,{{childList:true,subtree:true,characterData:true}}); }}
emiInit();
'''
open('emi_mod.js', 'w').write(js)
print(len(js), 'bytes;', len(I), 'iconos;', len(E), 'emojis')
