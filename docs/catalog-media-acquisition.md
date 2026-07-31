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

- **Renders 3D** — se cuelan como fotografía. Descartar por título (`3D rendering`,
  `3D visualization`, `illustration`) y por vista.
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
