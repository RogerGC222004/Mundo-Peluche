# Herramientas de Mundo Peluche

- `../fuente/mundo-peluche.html` — el juego (fuente). Es lo que se publica como Artifact en claude.ai.
- `build.js` + `net_peer.js` — generan la versión web (`../index.html`, con salas por PeerJS):
  `node herramientas/build.js fuente/mundo-peluche.html index.html`
- `pruebas/` — pruebas automáticas con Playwright (Chromium con SwiftShader, sin tarjeta de video).
  - Necesitan three.js r128 en `threerepo/build/three.min.js` junto a los scripts
    (`npm pack three@0.128.0` y copiar `build/three.min.js`).
  - Leen el juego desde `/home/claude/mundo-peluche.html` (cambiar la ruta si hace falta).
  - Multijugador: `test_real_mp.py` define la sala simulada (BUS); `test_fair.py` y `test_book_mp.py` la reutilizan.
  - Por zona: `test_pier`, `test_feed`, `test_pier_mp`, `test_pets`, `test_pets_mp`, `test_fi` (islas, globo, huerto),
    `test_bl_mp` (globos en sala), `test_race`, `test_cuco2`, `test_tramp2`, `test_loader`.
  - Capturas: `shot_tx.py '[["nombre",hora0a1,[camx,camy,camz],[mirax,miray,miraz],["low"]]]' juego.html prefijo`.
