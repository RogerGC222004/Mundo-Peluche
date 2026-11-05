# Herramientas de Mundo Peluche

- `../fuente/mundo-peluche.html` — el juego (fuente). Es lo que se publica como Artifact en claude.ai.
- `build.js` + `net_peer.js` — generan la versión web (`../index.html`, con salas por PeerJS):
  `node herramientas/build.js fuente/mundo-peluche.html index.html`
- `web/` — íconos del juego (`icono.svg` es el original; los `.png` salen de él). Desde v125 `build.js` también escribe
  junto a `index.html` el `manifest.webmanifest`, el `sw.js` y los íconos: la versión web se puede instalar como app
  y abre sin internet (el multijugador sí necesita internet). El `sw.js` cambia de nombre de caché con cada versión.
- Anuncios (v125): el juego nunca muestra anuncios solo. Hay botones ▶ opcionales en la tienda (llevarte algo sin monedas;
  1 anuncio hasta 100 monedas, 2 hasta 200, 3 hasta 300 y 4 si cuesta más; el avance se guarda) y «¿El doble?» después de
  abrir un cofre o de «Vender todo». Máximo 10 al día. Solo aparecen si la app define
  `window.MundoAds = { show: () => Promise<boolean> }` (true = el anuncio terminó y se da el premio).
  Para probarlos sin la app: `?anuncios=prueba` en la dirección, o tocar 5 veces la versión en el menú.
- `pruebas/` — pruebas automáticas con Playwright (Chromium con SwiftShader, sin tarjeta de video).
  - Necesitan three.js r128 en `threerepo/build/three.min.js` junto a los scripts
    (`npm pack three@0.128.0` y copiar `build/three.min.js`).
  - Leen el juego desde `/home/claude/mundo-peluche.html` (cambiar la ruta si hace falta).
  - Multijugador: `test_real_mp.py` define la sala simulada (BUS); `test_fair.py` y `test_book_mp.py` la reutilizan.
  - Por zona: `test_pier`, `test_feed`, `test_pier_mp`, `test_pets`, `test_pets_mp`, `test_fi` (islas, globo, huerto),
    `test_bl_mp` (globos en sala), `test_race`, `test_cuco2`, `test_tramp2`, `test_loader`.
  - Capturas: `shot_tx.py '[["nombre",hora0a1,[camx,camy,camz],[mirax,miray,miraz],["low"]]]' juego.html prefijo`.
- `relieve/` — el relieve de la isla grande (v119): montañas, meseta con cañones, colinas y el río con su cascada.
  - Las alturas van ya calculadas dentro del juego (`RL_DATA`, comprimidas), así carga rápido en teléfonos lentos.
  - Si se cambian las montañas, cañones o llanos (`relieve/relief_gen.js`) o el bloque «Relieve (v119)» del juego,
    hay que volver a generar: `node herramientas/relieve/gen.js fuente/mundo-peluche.html` (reescribe RL_DATA, RL_BED y RL_PLUNGE).

## App de Android (v127)
- `../app/` — Mundo Peluche como app (Capacitor 8, Android 16 / API 36). No se arma aquí: lo hace GitHub Actions
  (`.github/workflows/app-android.yml`) cada vez que cambia `fuente/`, `app/` o la versión web.
  - `construir.js` arma `app/www/` (el juego con three.js, PeerJS y letras dentro de la app).
  - `preparar-android.js` ajusta el proyecto que crea `npx cap add android`: AdMob en modo niños (sin identificador de
    publicidad), pantalla completa, pantalla encendida, orientación, íconos (`recursos/res/`), versión = GAME_VERSION y firma.
  - `puente.js` conecta los botones ▶ con AdMob (`window.MundoAds`) y el botón atrás de Android con `window.mundoAtras`.
  - `config.json`: códigos de AdMob (`pruebas: true` usa los anuncios de prueba de Google) y la orientación.
  - Firma: `llave/subida.p12` (protegida con contraseña). Si el repositorio tiene el secreto `LLAVE_CLAVE`, el armado
    genera el APK y el AAB firmados; si no, un APK de prueba.
  - El resultado queda en Releases (`app-v<versión>`). Si el armado falla, el registro se guarda en la rama `registro-app`.
  - La versión de la app (versionCode) es GAME_VERSION: para subir otra versión a Play hay que subir GAME_VERSION.
- `../tienda/` — textos de la ficha de Google Play, respuestas de los cuestionarios y capturas.
- `../privacidad.html` — política de privacidad (se publica con GitHub Pages).
