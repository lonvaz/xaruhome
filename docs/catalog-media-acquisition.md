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
