# Mundo Peluche · Ficha de Google Play

Todo lo que hay que copiar y pegar en Play Console. Las imágenes están en `tienda/capturas/` y `tienda/destacado.png`.

## Datos de la app
- **Nombre de la app** (máx. 30): `Mundo Peluche`
- **Idioma predeterminado:** Español (Latinoamérica) – es-419
- **App o juego:** Juego · **Gratis o de pago:** Gratis
- **Categoría:** Aventura (otra buena opción: Casual)
- **Etiquetas sugeridas:** Mundo abierto, Para la familia, Multijugador, Casual, Aventura
- **Correo de contacto:** lo escribe Roger en Play Console (su correo nuevo del juego)
- **Sitio web:** https://rogergc222004.github.io/Mundo-Peluche/
- **Política de privacidad:** https://rogergc222004.github.io/Mundo-Peluche/privacidad.html
- **Paquete de la app:** `com.rogergc.mundopeluche` (no se puede cambiar después)

## Descripción breve (máx. 80)
```
Explora una isla de peluche: pesca, mina, huerto, globos, feria y mucho más.
```

## Descripción completa (máx. 4000) · sin emojis (Google Play no los quiere en la ficha)
```
¡Bienvenido a Mundo Peluche! Eres un peluchito suave y cosido a mano que vive en una isla enorme llena de cosas por hacer.

UNA ISLA PARA EXPLORAR
Camina, nada y escala montañas nevadas. Sigue el río hasta la cascada, recorre la meseta con sus cañones, descubre cuevas escondidas y sube a los miradores. Hay día y noche, lluvia, nieve y atardeceres.

PESCA, MINA Y HUERTO
- Pesca en el muelle y vende tus peces a Tortu.
- Baja a la mina con tu linterna, rompe rocas y consigue mejores picos para llegar más hondo.
- Siembra, riega y cosecha en el huerto de Fresita, en una isla que flota en el cielo.

ISLAS FLOTANTES Y AVENTURAS
Sube en globo o con el arco a las islas flotantes, maneja coches, vuela en avión o helicóptero, súbete al cohete y visita planetas para descubrir especies nuevas.

FERIA Y MINIJUEGOS
Rueda de la fortuna, carrusel, canasta, bateo, hockey, topos, carreras y más. Gana monedas en cada uno.

CREA Y PERSONALIZA
Cientos de prendas: sudaderas, gorras, lentes, zapatos y más. Adopta una mascota y ponle nombre. Inventa tus propias criaturas y objetos, y construye lo que quieras en tu propia planicie del Modo libre.

JUEGA CON AMIGOS (CON PERMISO DE UN ADULTO)
El juego en línea viene apagado. Un adulto lo puede prender en Opciones, en la sección Para papás. Después se pueden crear salas con código, entrar a salas públicas, hacer fila para minijuegos y construir juntos. No hay chat y los apodos pasan por un filtro.

PENSADO PARA TODA LA FAMILIA
- Sin compras dentro del juego.
- Los anuncios solo salen si tú quieres: un botón opcional te deja ganar un premio extra. Nunca interrumpen el juego.
- Control para papás: el juego en línea solo se prende con permiso de un adulto.
- Funciona sin internet (el juego en línea sí necesita conexión).
- Va bien en teléfonos sencillos: tiene un modo ultra ligero.
```

## Imágenes
- **Ícono (512×512):** `herramientas/web/icono-512.png`
- **Gráfico de funciones (1024×500):** `tienda/destacado.png`
- **Capturas de teléfono (mínimo 2, recomendado 4 a 8):** `tienda/capturas/*.png` (8 capturas, 1920×1080, versión 246)

## Cuestionarios de Play Console (respuestas sugeridas)

### Público objetivo y contenido
- **Edades:** marca 6–8, 9–12, 13–15, 16–17 y 18 o más (es para toda la familia).
- ¿La app podría atraer a niños? **Sí** → aplica la política de Familias. Ya está hecho lo que pide:
  anuncios de AdMob (SDK certificado para familias), marcados para niños, contenido G, sin anuncios personalizados y sin identificador de publicidad.
- **Anuncios:** Sí, contiene anuncios.

### Clasificación de contenido (cuestionario IARC)
- Categoría: **Juego**.
- Violencia: no (el arco se usa para dar a dianas; no se lastima a nadie).
- Miedo, sexo, lenguaje grosero, drogas, apuestas: **no**.
- **Interacción entre usuarios: sí** (juego en línea, apagado hasta que un adulto lo prende). Chat: **no**. Comparte la ubicación real: **no**.
- Compras digitales: **no**.

### Seguridad de los datos
- ¿La app recopila o comparte datos? **Sí** (por el SDK de anuncios de Google AdMob).
- ¿Se cifran en tránsito? **Sí**. ¿Se pueden borrar? Los datos del juego viven en el teléfono; al desinstalar se borran.
- Tipos de datos (los que declara Google para AdMob):
  - **Ubicación aproximada** (por la IP) → compartida · publicidad, prevención de fraude.
  - **Información y rendimiento de la app** (fallos, diagnósticos) → recopilada · análisis, publicidad.
  - **ID de dispositivo u otros** (ID del conjunto de apps) → recopilada y compartida · publicidad, prevención de fraude, análisis.
- Antes de enviar, revisar la guía oficial de Google: https://developers.google.com/admob/android/privacy/play-data-disclosure

### Funciones sociales (política de Familias)
Lo que pide Google para juegos para niños con juego en línea, y dónde está en Mundo Peluche:
- **Recordatorio de seguridad antes de jugar con otros:** sí, la primera vez que se entra a una sala sale «Antes de jugar en línea» con 4 consejos.
- **Acción de un adulto antes de prenderlo:** sí, hay que resolver una operación (suma o resta de 4 cifras, multiplicación o división de 3 cifras).
- **Un adulto lo puede apagar:** sí, en Opciones → Para papás → Jugar en línea.
- **Sin chat ni mensajes libres;** apodos y nombres con filtro de groserías.
- Si Play Console pregunta «¿Tu app permite que los usuarios interactúen?»: **Sí**, y en la descripción: «Juego en línea opcional sin chat; viene apagado y solo un adulto lo prende resolviendo una operación. Muestra consejos de seguridad antes de entrar.»

### Permisos de servicio en primer plano
Desde la versión 246 la app ya **no** pide ese permiso (lo traía una librería de los anuncios y el juego no lo usa). Si Play Console todavía lo pregunta por una versión vieja, sube la nueva y responde que **no usa servicios en primer plano**.

### Seguridad de los datos (agregar a lo de arriba)
- **Datos que ven otros jugadores en línea:** apodo y peluche. Viajan directo de teléfono a teléfono, cifrados de punta a punta (WebRTC), y no se guardan en ningún servidor. Google no pide declarar datos cifrados de punta a punta que solo leen quien los manda y quien los recibe. Si aun así prefieres declararlo: **«Otro contenido generado por el usuario» · compartido · funcionalidad de la app · opcional**.

### Otros
- Acceso a la app: **toda la app está disponible sin restricciones**.
- App gubernamental: no · Funciones financieras: no · Salud: no.
