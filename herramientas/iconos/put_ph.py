# Pone (o cambia) el módulo de fotos de ropa y mascotas en el juego
p='/home/claude/mundo-peluche.html'
s=open(p,encoding='utf-8').read(); mod=open('ph_mod.js',encoding='utf-8').read()
h='// ---------------- v243: FOTOS DE LA ROPA Y LAS MASCOTAS'
if h in s:
  i=s.index(h); i=s.rindex('// ====',0,i); j=s.index('\n// ---- Tienda (menú principal → Personalizar) ----',i); s=s[:i]+mod+s[j:]
else:
  a='applyOutfit(plush, wardrobe.eq);\n'; assert s.count(a)==1; s=s.replace(a,a+mod)
open(p,'w',encoding='utf-8').write(s); print('ok')
