# Íconos dibujados (en lugar de emojis)

- `ic_r1.py` (y luego `ic_r2.py`…): cada dibujo (`I`, SVG de 40×40 con el estilo de la barra del Modo libre),
  qué emoji reemplaza (`E`) y su nombre en español (`NOM`).
- `gen_js.py ic_r1 [ic_r2 …]`: arma `emi_mod.js` (el módulo que va en el juego).
- `put.py`: cambia el módulo dentro de `/home/claude/mundo-peluche.html`.
- `hoja.py . ic_r1 hoja_r1.png "Ronda 1"`: hoja para comparar emoji y dibujo.

Correr desde esta carpeta (o una copia).
