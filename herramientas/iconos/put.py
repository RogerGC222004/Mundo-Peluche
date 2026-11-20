# Pone el módulo de íconos (emi_mod.js) al principio del juego (justo después de GAME_VERSION), quitando el anterior
import re
p='/home/claude/mundo-peluche.html'
s=open(p,encoding='utf-8').read(); mod=open('emi_mod.js',encoding='utf-8').read()
h='// ---------------- v242: ÍCONOS DIBUJADOS EN LUGAR DE EMOJIS'
if h in s:
  i=s.index(h); i=s.rindex('// ====',0,i); j=s.index('emiInit();\n',i)+len('emiInit();\n'); s=s[:i]+s[j:]
m=re.search(r"const GAME_VERSION='\d+';\n",s); k=m.end()
s=s[:k]+mod+s[k:]
import os
tmp=p+'.tmp'; open(tmp,'w',encoding='utf-8').write(s); os.replace(tmp,p); print('ok', len(mod))   # (de un jalón: nadie lee el archivo a medias)
