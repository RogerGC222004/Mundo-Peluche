# Reemplaza el módulo de íconos dentro del juego por emi_mod.js
p='/home/claude/mundo-peluche.html'
s=open(p,encoding='utf-8').read(); mod=open('emi_mod.js',encoding='utf-8').read()
h='// ---------------- v242: ÍCONOS DIBUJADOS EN LUGAR DE EMOJIS'
i=s.index(h); i=s.rindex('// ====',0,i); j=s.index('emiInit();\n',i)+len('emiInit();\n')
s=s[:i]+mod+s[j:]; open(p,'w',encoding='utf-8').write(s); print('ok', len(mod))
