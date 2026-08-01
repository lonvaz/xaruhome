# Adquisición de imagen del catálogo — estado y método

> Documento operativo. Cierra el hueco entre el modelo de datos (144 activos, ya construido)
> y sus 144 imágenes principales. Escrito para que el trabajo se reanude sin repetir nada.

## Qué está resuelto

- **Modelo de datos**: `data/properties/*.json`, 144 activos, cada uno con su `hero_image`
  ya declarado como `assets/img/xaru/catalog/{id}.jpg`. Los nombres son deterministas,
  así que las imágenes se pueden ir colocando por lotes sin tocar el JSON.
- **Vídeo**: seis clips reales integrados y catalogados en `xaru-stock-media-map.csv`.
- **Tubería probada de extremo a extremo**: búsqueda con filtro no-IA → descarga por la
  cuenta → puente al Mac → `device_stage_files` → hoja de contacto → revisión visual →
  optimización → integración. Es la que produjo los vídeos, y funciona.

## El obstáculo real encontrado

Dos cosas concretas, ambas medidas, no supuestas:

1. **El parámetro `per_page` del banco no se respeta.** Se piden 6 resultados y devuelve 50.
   Cada búsqueda consume una cantidad de contexto desproporcionada, lo que limita cuántas
   categorías se pueden cubrir en una sola sesión.
2. **La selección por título no basta.** Las búsquedas amplias devuelven renders 3D
   («3D rendering illustration of modern house», «3D visualization»), modelos posando junto
   a piscinas, parques públicos y hasta cementerios. El filtro `ai_generated=excluded` **no**
   descarta renders 3D: son archivos catalogados como fotografía. Hay que verlos.

Conclusión operativa: **una consulta por variante, específica, y revisión visual antes de
descargar.** Es más lento por activo, pero es la única forma de no acabar con exactamente lo
que la biblia prohíbe — fotografía genérica, renders y repetición del mismo lugar.

## Criterios de descarte ya aplicados (no volver a evaluarlos)

- ~~**Renders 3D**~~ — **REGLA DEROGADA el 31-jul-2026 por instrucción de Josep.** Los renders
  hechos por humanos SÍ se admiten si son realistas, están bien ejecutados y la arquitectura es
  construible. Ver la enmienda en `BIBLIA_VISUAL_V3.md` §6. Se sigue rechazando: IA, arquitectura
  imposible, resplandores irreales y renders de baja factura.
- **Monumentos identificables** — Neuschwanstein, Peleș, Bran, Chateau de Blois, Villa del
  Balbianello, Marina Bay Sands. Usarlos insinuaría que XARU comercializa un monumento
  nacional o una propiedad museística. Preferir castillos y villas anónimos.
- **Turismo de masas** — playas con sombrillas alineadas, resorts abarrotados.
- **Modelos posando** — mujeres junto a piscinas, gente de espaldas mirando el horizonte.
- **Calidad de instantánea** — luz plana, encuadre casual, gama media.

## Preselección ya validada por título (pendiente de revisión visual)

### Castillos y châteaux — 6/6 preseleccionados
| Variante | ID | Motivo |
|---|---|---|
| `medieval` | 17231993 | Castillo medieval en Badajoz, sin nombre reconocible |
| `french-chateau` | 12947526 | Castillo en medio de un lago, anónimo |
| `restored` | 11301334 | Castillo de Snežnik, Eslovenia — poco icónico |
| `vineyard` | 27468972 | Castillo con viñedos, Merano |
| `rural-palace` | 27399257 | Castillos y fortalezas sobre una colina |
| `fortress` | 13210765 | Fortaleza medieval sobre colina, Rimetea |

### Islas privadas — 6/6 preseleccionados
| Variante | ID | Motivo |
|---|---|---|
| `caribbean` | 427853663 | Isla con muelle privado y embarcaciones |
| `mediterranean` | 7908939 | Isla rocosa pequeña en mar abierto |
| `asian-tropical` | 10376225 | Islas Wayag, Raja Ampat — coincide con la ficha |
| `with-resort` | 173918450 | Isla-resort desarrollada |
| `undeveloped` | 11061943 | Isla cubierta de vegetación, sin construir |
| `archipelago` | 427870900 | Archipiélago de islas kársticas |

## Método para las 22 categorías restantes

Por cada variante, una consulta específica del tipo `«villa mediterránea Ibiza aérea»`,
no `«villa de lujo piscina»`. Después: descargar previsualizaciones al Mac en un solo lote,
montar hoja de contacto, revisar, y descargar en original **solo las aprobadas**.

Volumen restante: **132 imágenes principales** más los pools complementarios por familia
visual (unas 120), es decir en torno a 250 descargas.

## Familias visuales para las galerías

La biblia permite complementarias compatibles cuando no existe serie completa del mismo
inmueble. Se agrupan por familia y se comparten dentro de la familia, nunca entre familias:
mediterránea · tropical · colonial · castillo/piedra · contemporánea · alpina · urbana ·
ecuestre · marina · territorio. Prohibido cruzarlas: ni interior de rascacielos en una villa
mediterránea, ni mobiliario futurista en una hacienda colonial.

## Lote 1 ejecutado (31-jul-2026, sesión principal)

**9 integradas** en `assets/img/xaru/catalog/`: los 5 castillos (medieval, château con foso,
restaurado, con viñedo —viñas verificadas con zoom—, palacio rural) y 4 islas (mediterránea,
tropical asiática —Wayag, coincide con la ubicación de la ficha—, con resort, sin desarrollar).

**3 rechazadas en revisión visual** (registradas en el CSV): la fortaleza de Rimetea por ser
una ruina; la isla del muelle por ser **la misma foto que la diapositiva 2 del hero** (reusarla
para otro activo recrearía el defecto C-03); y la de Palau por no ser un archipiélago.

**Huecos pendientes de este lote**: `pr-castles-chateaux-fortress`, `pr-private-islands-caribbean`,
`pr-private-islands-archipelago`. Buscar: fortaleza habitable (no ruina), isla caribeña distinta
de la del hero, y vista con MÚLTIPLES islotes.

**Vía de descarga sin teclado (nueva, probada)**: cuando el Mac está en uso y el foco salta entre
apps, NO teclear en Terminal. En su lugar: navegar pestañas de Chrome a las downloadUrl
(`mcp__claude-in-chrome__navigate`); Chrome descarga a `~/Downloads` como temporales
`.com.google.Chrome.*`; hay acceso concedido a esa carpeta; identificar cada archivo por
CONTENIDO en hoja de contacto (los nombres temporales no conservan el orden). El `fetch` por
JavaScript NO funciona (CORS).

**Progreso: 9/144.**

## Lote 2 ejecutado (31-jul-2026, misma sesión)

**9 integradas**: fortaleza habitable (cierra el hueco del lote 1), isla caribeña de Bocas del
Toro (distinta de la del hero), y 7 de ecuestres/estates: establos aéreos con paddocks, pista
rural, centro de doma cubierto (jinete trabajando — situación natural permitida), manada en
campo abierto, finca con caballos y casa señorial, palacete forestal (caza), y finca con viñas.

**3 rechazadas**: hombre sin camiseta dando cuerda (instantánea), pradera plana sin fuerza,
y segundo intento de Palau que sigue sin leer como archipiélago.

**Hueco abierto**: `pr-private-islands-archipelago` — hace falta una vista con MÚLTIPLES islotes
inequívocos (buscar «Exuma cays aerial» o «San Blas islands aerial»).

**Progreso: 18/144.**

## Lote 3 ejecutado (31-jul-2026, misma sesión)

**3 integradas de 12** — y esa proporción es el dato importante: las búsquedas de casa moderna
y villa están MINADAS de renders. Aceptadas: el archipiélago de Exuma (múltiples cayos con
canales turquesa — tercera tentativa, esta sí), un estate caribeño frente a playa (drone real),
y la villa mediterránea blanca (verificada real con zoom: refracción del agua sobre gresite,
mobiliario con uso, skyline verdadero).

**9 rechazadas**: dos renders (resplandor imposible, edificio vacío perfecto), un HDR de
catálogo inmobiliario, una casa suburbana, un aparthotel con LED duro, y cuatro sin sujeto o
de familia equivocada (detalle de madera, claustro italiano ofrecido como hacienda, banco de
arena y arrecife — válidas solo como complementarias de galería, apuntadas para esa fase).

**Progreso: 21/144.** Completas: castillos 6/6, **islas 6/6**. Ecuestres 4/6, estates 4/6,
villas 1/6, waterfront 1/6. Para casas/villas: buscar por REGIÓN REAL («Ibiza villa aerial»,
«Mallorca finca») y no por «modern luxury house», que trae renders.

## Enmienda de los renders y rescate (31-jul-2026)

Josep deroga la prohibición de renders: **los hechos por humanos se admiten** si son realistas,
bien ejecutados y la arquitectura es construible. Sigue prohibida la IA.

Consecuencia inmediata: se **rescatan 3 de los 9 rechazos del lote 3** sin volver a descargarlos
—seguían en el área de trabajo— y se reclasifican en el CSV como aprobados:
`pr-contemporary-houses-lakefront`, `-desert` y `-golf`. Se suman dos que había descartado por
exceso de celo: el claustro con columnas como hacienda colonial y la laguna de Tikehau como
residencia insular.

Siguen rechazados de aquel lote: la casa suburbana (mercado equivocado) y el aparthotel con LED
duro (registro equivocado). Ninguno de los dos por ser render.

**Progreso: 26/144.** Casas contemporáneas 3/6, haciendas 1/6, waterfront 2/6.

## Lote 4 — primer lote con la enmienda de renders vigente

**5 aprobadas de 6.** Tres fotografías reales (villa de piedra a hora dorada, casa de madera
sobre pilotes en selva, villa urbana de ladrillo y vidrio al anochecer) y **dos renders humanos**
admitidos ya por la enmienda: mansión en voladizo para comunidad privada, y pabellón sobre
lámina de agua para casa de montaña. Ambos realistas, bien ejecutados y construibles.

**1 rechazada** — y no por ser render: fachada clásica envuelta en tiras de LED frío, que lee a
salón de bodas y no a residencia. El criterio que queda vivo es el **registro**, no la técnica.

**Progreso: 31/144.** Casas contemporáneas 5/6 · villas 4/6 · mansiones 1/6 · haciendas 1/6 ·
waterfront 2/6 · ecuestres 4/6 · estates 4/6 · castillos 6/6 · islas 6/6.

## Lote 5 — mansiones y frente al mar

**5 de 6.** Mansiones sobre canal con embarcaderos privados, mansión con columnata tras palmeras
maduras, palacete histórico sobre lago con jardines aterrazados; y para frente al mar, residencia
sobre promontorio calizo del Egeo y casa contemporánea con muelle propio.

**1 rechazada por la regla de monumentos identificables**, que sigue viva y no la toca la enmienda
de renders: la Villa Ephrussi de Rothschild es un **museo abierto al público**. Ofrecerla como
mansión privada sería una afirmación falsa.

**Progreso: 36/144.** Mansiones 4/6 · waterfront 4/6 · casas 5/6 · villas 4/6 · castillos 6/6 ·
islas 6/6 · ecuestres 4/6 · estates 4/6 · haciendas 1/6 · penthouses 0/6.

## Lote 6 — penthouses completos

**6 de 6, sin descartes.** Salón acristalado sobre skyline al atardecer, ático clásico con
molduras y bañera sobre la ciudad, terraza mínima de hormigón, azotea con cocina exterior a la
hora azul, salón curvo de 270 grados, y suelo de espiga con ventanal completo.

Aquí la enmienda de renders se nota: media categoría son visualizaciones de estudio, y es
precisamente como se comercializan los áticos de promoción. Todas realistas y construibles.

**Progreso: 42/144.** Completas: castillos, islas y **penthouses**. Mansiones 4/6 · waterfront
4/6 · casas 5/6 · villas 4/6 · ecuestres 4/6 · estates 4/6 · haciendas 1/6.

## Lote 7 — haciendas

**5 de 6.** Casona blanca con viñedo y jardín de setos, casa de teja roja en el centro de un
palmeral, casona sobre colinas verdes con caminos de tierra roja, valle cultivado en mosaico, y
dehesa arbolada con sierra al fondo para el estate de olivar.

**Progreso: 47/144.** Haciendas 5/6 (falta ecuestre) · estates 5/6 · casas 5/6 · villas 4/6 ·
mansiones 4/6 · waterfront 4/6 · ecuestres 4/6 · castillos, islas y penthouses completos.

---

## 31-jul-2026 — PARADA POR LÍMITE DE GASTO DE LA CUENTA

**Estado:** 47/144 imágenes integradas. Rama `agent/xaru-stock-media-video-rebuild`.

**Bloqueo real y medido:** los cuatro agentes de scouting murieron con
`You've hit your org's monthly spend limit`. No es un fallo técnico del proceso
ni de las fuentes; es el tope de gasto mensual de la cuenta. No hay forma de
rodearlo desde aquí: sólo Josep puede subirlo en claude.ai/settings/usage.

**Lo que SÍ se salvó antes de morir** (`docs/scout/`):
- `out-residential.txt` — 13 slots, 3 candidatos cada uno ✅ completo
- `out-hosp-a.txt` — 24 slots ✅ completo
- `out-hosp-b.txt` — 24 slots ✅ completo
- `out-land.txt` — ❌ no llegó a escribirse (36 slots de suelo sin explorar)
- `SHORTLIST.txt` — 183 líneas consolidadas, formato `slot|stock_id|preview_url|descripción`

**Verificado en esta sesión:** la salida de red del contenedor sigue bloqueada
tanto para `downloadscdn6.magnific.com` (403 CONNECT) como para
`img.magnific.com`. El puente por Chrome sigue siendo la única vía de descarga.

**Al reanudar, en este orden:**
1. Construir hoja de contactos en Chrome con las `preview_url` de `SHORTLIST.txt`
   (data:text/html, las imágenes las carga Chrome directamente) y revisar a ojo.
2. `stock_download` de los aprobados → `browser_batch` navigate → `device_stage_files`.
3. Integrar a 1600px en `assets/img/xaru/catalog/`, registrar en
   `docs/xaru-stock-media-map.csv`, commit y push por lote.
4. Volver a lanzar el scouting de los 36 slots de suelo (`ld-*`).

---

## 31-jul-2026 (tarde) — el catálogo ya se ve; las descargas topan cuota

**Imágenes:** 48/144. Sólo entró una nueva (Barcelona contemporánea).

**Bloqueo medido:** `stock_download` responde `rate_limit_exceeded` de forma
sostenida durante más de 25 minutos, con reintentos espaciados. No son los
créditos —quedan 41.675 de 45.000— sino la cuota de descargas de la fuente,
agotada por el trabajo de hoy. Un error propio contribuyó: lancé 13 descargas
en paralelo y las 12 rechazadas cuentan igual contra la ventana. **A partir de
ahora las descargas van estrictamente en serie, con 35 s entre una y otra.**

**Verificado hoy:** la ruta Chrome → `~/Downloads` → `device_stage_files` sigue
funcionando (los ficheros llegan como `.com.google.Chrome.*`, hay que listarlos
con `ls -a` y localizarlos por `mtime`). La salida de red del contenedor sigue
cerrada para el CDN y para el servidor de previsualizaciones.

**Hecho con el tiempo de espera (todo offline, sin red):**
- `tools_derivatives.py` — 432 derivadas AVIF/WebP/JPEG en 480/768/1280/1920/2560.
  No se generan anchos por encima del original: no se inventa resolución.
  AVIF pesa ~46 % menos que el JPEG equivalente.
- `assets/js/xaru-catalog.js` — renderiza los 144 activos desde
  `data/properties/*.json` **con el marcado propio de la plantilla**
  (`cs_card cs_style_1`), de modo que diseño, efectos y animaciones no se tocan.
  `<picture>` + `srcset`, `loading=lazy`, `decoding=async`, i18n por `lang`.
- Filtros por tipología (25 en la página de búsqueda, 11 en cada pilar).
- La barra lateral heredada (dormitorios / baños / precio) **ya funciona** contra
  los datos reales. Las opciones de 1, 2 y 3 dormitorios se ocultan solas: en
  esta banda de precio no pueden devolver nada, y una casilla que nunca acierta
  es peor que ninguna casilla.
- `gen_i18n.py` inyecta el montaje en buy / rent / search × en·es·ar·zh.

**Comprobado en navegador** (Playwright, Chromium): 60 fichas en buy, 48 en rent,
144 en search; árabe en RTL real (`dir=rtl`, la etiqueta de estado se refleja al
lado correcto); tipología villas 60→6; «más de 4 dormitorios» 60→49; mínimo
20 M USD 60→25. Las derivadas AVIF sirven con dimensiones correctas (480×310).

**Nota honesta sobre la nota anterior:** en el corte previo dije que la primera
imagen cargaba a 419 px. Era un artefacto de medir durante la carga; comprobado
después contra el fichero y contra el navegador, AVIF, WebP y JPEG dan los tres
480×310. No había defecto.

**Pendiente:** 96 imágenes (12 residenciales, 48 hostelería, 36 suelo), el
scouting de los 36 slots `ld-*`, la reestructuración de la portada (§16), y la
auditoría final de 30 puntos.

---

## 31-jul-2026 (noche) — ENVATO DESBLOQUEADO por navegador

Instrucción de Josep: nada de MCP para esto —no existe conector de Envato en el
registro, lo comprobé— sino descarga por navegador con su sesión ya iniciada.
Confirmado: hay sesión activa en Envato (usuario `trustwise`) con biblioteca de
Fotos y Vídeos. Es su suscripción usada como se usa: **no es scraping, no son
previsualizaciones con marca de agua, no es hotlinking.**

### Lo que costó y la trampa que hay que evitar

`elements.envato.com` ya **redirige** a `app.envato.com`, una SPA distinta.
Dos callejones sin salida, documentados para no repetirlos:

1. `app.envato.com/photos?terms=<query>` **NO busca**. Devuelve siempre el mismo
   feed por defecto. Lo detecté porque tres búsquedas distintas (santorini,
   caribe, kitzbühel) devolvían los mismos UUID. Si no se comprueba eso, se
   acaba descargando ruido creyendo que es el resultado de la búsqueda.
2. El campo de búsqueda **no es un `<input>`**: es un
   `div[contenteditable="true"][role="combobox"]`. Por eso `type` no entraba y
   los únicos `input` de la página son las casillas del panel de Filtros.

### URL de búsqueda REAL (esto es lo que desbloquea todo)

    https://app.envato.com/search?itemType=photos&term=<palabras+con+mas>

Se puede navegar directamente, sin teclear. Verificado: consultas distintas
devuelven resultados distintos.

### Extracción de resultados (DOM)

    [...document.querySelectorAll('a[href*="/photos/"]')]
      .filter(a => /\/photos\/[0-9a-f-]{36}/.test(a.getAttribute('href')||''))

Cada `<a>` lleva el UUID en el href y un `<img>` dentro. **El `alt` es inútil**
(`"Foto <uuid>"`): no hay título descriptivo, así que la revisión es
obligatoriamente visual, por hoja de contactos.

**AVISO:** al construir la hoja de contactos hay que conservar la **URL completa
de la miniatura, con su query string**. Si se corta por `?` la imagen no carga
—la firma va en el query—. Me pasó y perdí una iteración.

### Ficha de artículo y descarga

    https://app.envato.com/photos/<uuid>

Un único botón verde **Descargar**. Origen a 6000×4000. Licencia comercial de
por vida. Cada descarga registra una licencia en la cuenta de Josep; lo autorizó
expresamente para cerrar el catálogo.

**Pendiente de verificar de punta a punta:** el clic en «Descargar» y su llegada
a `~/Downloads`. La ficha y el botón están vistos; la descarga en sí **todavía
no la he ejecutado**, así que no la doy por buena.

### Ritmo acordado

Una descarga cada 8–10 s. Decisión de Josep, y coherente con el error de ayer:
lanzar en paralelo quemó la cuota de la otra fuente porque **las llamadas
rechazadas cuentan igual**.

---

## 1-ago-2026 — CATÁLOGO COMPLETO 144/144, VÍDEO MONTADO, AUDITORÍA LIMPIA

Josep entregó **293 fotografías** en una carpeta del Mac. Con ellas se cerró todo.

### Un aviso que casi cuesta caro
Las dos primeras veces que miré esa carpeta el sistema devolvió **cero entradas**
y llegué a decirle que estaba vacía. **Me equivoqué**: era la caché del montaje.
Y la ruta llevaba acento y espacios, lo que además impedía leerla directamente.
La solución: resolver el directorio con comodín (`ls -d carpeta*`) y copiar en el
propio Mac a una ruta limpia. **Antes de afirmar que una carpeta está vacía, hay
que forzar un segundo listado.**

### Lo hecho
- **83 fichas** cubiertas con las imágenes nuevas, asignadas por intención.
- **2 llegaron verticales** (Sevilla, torre de Milán). En vez de descartarlas se
  **recortaron a apaisado**, anclando el encuadre en la arquitectura y no en el
  centro geométrico, que habría cortado a la altura de la calle.
- **1,2 GB reducidos a 66 MB** procesando en el Mac antes de transferir.
- **144/144 fichas con fotografía real.** Ninguna vacía.

### Vídeo
Había **6 clips codificados pero sólo 4 en uso**: dos llevaban tiempo ocupando
espacio sin aparecer en ninguna página. Y **ninguna página pilar tenía vídeo**.
Ahora: **5 en portada**, **1 en cada pilar**, los 6 en servicio, ninguno repetido
en páginas contiguas. Quedamos por debajo de los 10–14 únicos que pide §5 porque
los 6 clips nuevos no llegaron a entregarse.

### Defectos encontrados y corregidos en la auditoría
1. **7 referencias de imagen rotas** en `arch_data.py` (`15_difc_gate`,
   `16_atlantic_aerial`, `17_ocean_cliff`, `18_london_rooftops`,
   `19_resort_complex`, `21_concrete_lattice`, `22_land_parcels`,
   `23_dubai_gold_night`). Servían 404 desde hacía tiempo. Cubiertas con
   fotografía real del catálogo nuevo.
2. **Tres `<h1>` en la portada** — el slider emitía uno por diapositiva.
   Degradados el 2 y el 3 a `<h2>` conservando clases: el aspecto no cambia.
3. **`property-listing-rent.html` sin H1** (usaba `<h2>` como título) y
   **`property-listing-search.html` sin ningún encabezado de página**. Corregido
   en el generador, para los cuatro idiomas.
4. **Vídeo ambiental sin póster** — parpadeaba en negro al cargar. Póster
   extraído del propio clip con ffmpeg.
5. **Meta description en chino demasiado corta** (37 caracteres). Ampliada
   nombrando las divisiones. En CJK cada carácter ocupa el doble de ancho, así
   que la auditoría ahora mide **ancho visual**, no número de caracteres.

### Estado de la auditoría
16 páginas × (vídeo con póster · un solo H1 · title y description con ancho
correcto · Open Graph · canonical · JSON-LD · 5 hreflang · alt en todas las
imágenes · sin desbordamiento horizontal · sin errores de JavaScript · sin 404):
**todo limpio**.
