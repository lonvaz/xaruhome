# BIBLIA VISUAL V3 — XARU HOME
### Reconstrucción con fotografía y vídeo real de archivo · catálogo demostrativo completo

> **Innegociable.** Este documento sustituye a cualquier criterio visual anterior. Donde entre en conflicto con `DERROTERO_MAESTRO_V2.md` o con la biblia visual previa, **manda este**.
> Fecha de incorporación: 31-jul-2026. Rama de ejecución: `agent/xaru-stock-media-video-rebuild`.

---

## 0. Cambio de doctrina respecto a la versión anterior

La biblia anterior trataba XARU HOME como un catálogo de activos reales y, en consecuencia, **bloqueaba** secciones a la espera de fotografía propia. Marcaba 178 bloques como `REAL_MEDIA_REQUIRED` y exigía dos jornadas de rodaje antes de poder completar la plataforma.

**Eso queda derogado.** XARU HOME es, en esta fase, **una plataforma educativa y una presentación corporativa demostrativa**. La consecuencia operativa es directa:

| Antes | Ahora |
|---|---|
| Bloquear secciones sin material propio | **Prohibido bloquear.** Toda sección se completa con archivo real |
| Pedir a XARU fotografías de sus activos | **Prohibido pedirlas.** No se solicita material propio |
| Vaciar o neutralizar tarjetas sin foto | **Prohibido.** Ninguna tarjeta vacía, ningún placeholder, ningún degradado |
| Eliminar categorías por falta de imágenes | **Prohibido.** Se amplía el catálogo, no se recorta |
| Nota de procedencia bajo cada ficha | Sustituida por **una sola declaración** en la cabecera del catálogo |

Lo que **no** cambia: sigue prohibido el material generado por IA, y sigue prohibido presentar como real algo que no lo es. La honestidad se resuelve ahora declarando el catálogo como demostrativo **una vez**, no repitiendo advertencias que degradan la percepción de calidad.

---

## 1. Fuentes autorizadas — y sólo estas tres

1. **Magnific** — su banco/biblioteca de fotografía y vídeo real.
2. **Envato Elements** — stock photos y stock footage.
3. **Artlist** — stock footage y stock photography.

### Prohibido como fuente
Freepik · Unsplash · Pexels · Pixabay · Shutterstock · Adobe Stock · Google Images · Pinterest · redes sociales · imágenes tomadas de webs de terceros · cualquier material generado por inteligencia artificial.

### Prohibido dentro de Magnific
Se usa **exclusivamente su banco de archivo**. Quedan fuera todas sus herramientas de creación: generación, reimaginación, creative upscale, relight, expand, generative fill, sustitución de elementos y creación de detalles.

### Nota de precisión sobre la fuente (registro honesto)
La herramienta de banco de Magnific disponible en esta sesión describe su índice como catálogo de Freepik y sirve los ficheros desde dominios de Magnific. **Es el banco de archivo de Magnific**, y es lo que se usa. No se emplea Freepik como plataforma independiente, ni su web, ni su API propia. Queda dicho aquí para que nadie tenga que deducirlo del código.

**Estado real de acceso en esta sesión:** el banco de Magnific responde para foto y vídeo. Envato Elements no tiene conexión disponible. La conexión de Artlist expone únicamente herramientas de generación por IA, que esta biblia prohíbe; su fototeca y su videoteca de archivo no son accesibles por esa vía. Cuando una plataforma pida autenticación se detiene **solo la descarga**, no el trabajo, y se continúa en cuanto haya acceso.

### Registro obligatorio
Todo recurso se anota en `docs/xaru-stock-media-map.csv` con: `asset_id, platform, source_title, source_id, source_url, author, media_type, page, section, category, local_filename, desktop_or_mobile, duration, dimensions, status, notes`.

Nunca se hotlinkea. Los originales se descargan desde las cuentas autorizadas y se guardan en el repositorio.

---

## 2. El significado de XARU HOME

La web se percibía como una empresa que vende casas. Deja de hacerlo desde el primer segundo, **sin dejar de ser inmobiliaria**.

> **XARU HOME es el hogar operativo de activos, proyectos, capital y expansión internacional.**

Jerarquía obligatoria, en este orden:

1. Real estate como puerta de entrada y protagonista visual.
2. Activos y proyectos de gran escala.
3. Capital y estructuración.
4. Expansión internacional.
5. Una sola estructura bajo XARU HOME.

Prohibido convertir la portada en una consultora genérica. Prohibido retirar el protagonismo inmobiliario.

---

## 3. Hero — regla innegociable

El hero tiene **tres diapositivas**. Se conservan **todas menos la última**.

- Diapositivas 1 y 2: **no se tocan los archivos**. Ni recorte, ni proporción, ni corrección de color, ni punto focal.
- Los **textos superpuestos sí** se adaptan a la nueva narrativa.
- La **última diapositiva** pasa de imagen a **vídeo real de archivo**.

### Vídeo de la última diapositiva
Tema: costa internacional, playa de alto nivel, isla, territorio frente al mar, resort integrado en el paisaje, destino costero o vista aérea de un lugar excepcional.

Paleta compatible: negro, marfil, arena, piedra, azul profundo, verde natural, dorado discreto.

Requisitos: real · cinematográfico · de una de las tres plataformas · horizontal · preferiblemente 4K · sin texto incrustado · sin logotipos · sin personas mirando a cámara · sin aspecto publicitario barato · sin elementos generados · 10 a 18 segundos · loop limpio · `muted` · `autoplay` · `playsinline` · póster extraído del propio vídeo.

Si el vídeo no corresponde a un lugar concreto, **el texto no puede nombrar una propiedad concreta**. La última diapositiva apoya la narrativa global, no un activo.

### Narrativa nueva (ES)
- Eyebrow: `REAL ESTATE · PROYECTOS · CAPITAL · EXPANSIÓN`
- H1: **El hogar operativo de activos, proyectos, capital y expansión internacional.**
- Apoyo: *Real estate es el punto de partida. XARU HOME conecta propiedades, desarrollos, capital y expansión internacional bajo una sola estructura.*
- Botón principal: `Explorar oportunidades`
- Botón secundario: `Presentar un activo o proyecto`

### Narrativa nueva (EN)
- Eyebrow: `REAL ESTATE · PROJECTS · CAPITAL · EXPANSION`
- Headline: **The operational home for assets, projects, capital and international expansion.**
- Supporting: *Real estate is the starting point. XARU HOME connects properties, developments, capital and international expansion under one structure.*

Árabe y chino: misma idea, redacción nativa. **Prohibida la traducción literal torpe.**

---

## 4. Metadatos y presencia social

Se actualizan en portada: `<title>`, meta description, `og:title`, `og:description`, `twitter:title`, `twitter:description`, descripción de Organization y de WebSite en JSON-LD, texto breve del footer y texto introductorio de About.

**ES**
- Title: `XARU HOME | Activos, proyectos, capital y expansión internacional`
- Meta: *Real estate es el punto de partida. XARU HOME es el hogar operativo de activos, proyectos, capital y expansión internacional.*
- OG title: `XARU HOME — El hogar operativo de activos, proyectos y capital`
- OG desc: *Real estate como protagonista dentro de una estructura que conecta propiedades, desarrollos, capital y expansión internacional.*
- Twitter title: `XARU HOME | Real estate, proyectos, capital y expansión`
- Twitter desc: *El hogar operativo de activos, proyectos, capital y expansión internacional.*
- Footer: *Real estate, activos, proyectos, capital y expansión internacional bajo una sola estructura.*

No se añaden servicios nuevos. No se inventan cifras. No se elimina la condición de compañía inmobiliaria. **No se tocan** las URLs, canonical ni hreflang ya corregidos. La imagen de Open Graph debe ser fotografía real de archivo.

---

## 5. Vídeo como lenguaje, no como adorno

Mínimos: **5 vídeos visibles en portada**, **1 vídeo principal en cada página pilar**, **entre 10 y 14 únicos** en toda la plataforma. Prohibido repetir el mismo vídeo en todas las páginas.

**Portada**
1. Última diapositiva del hero — costa, isla, playa o territorio internacional.
2. Private Real Estate — recorrido cinematográfico por villa, mansión o residencia excepcional.
3. Commercial & Hospitality — hotel o resort en funcionamiento.
4. Land & Master Developments — territorio, costa o masterplan desde drone.
5. Projects, Capital & Expansion — arquitectura, planificación, construcción, skyline.
6. (opcional) Corporate Services · Financial Infrastructure · Company · CTA final.

**Interiores** — al menos un vídeo real en cada una: Private Real Estate · Commercial & Hospitality · Land & Master Developments · Project Structuring · Capital & Partnerships · Trade & Financial Infrastructure · Corporate Services & Relocation · Company.

Usos válidos: hero de página, bloque editorial a todo ancho, composición partida vídeo/texto, fondo de sección, cabecera de categoría, destacado con póster. **No convertir todas las tarjetas en vídeo.** El vídeo aporta escala y movimiento, no ruido.

---

## 6. Criterio de selección visual

**Buscar:** luz natural · arquitectura real · materiales auténticos · paisaje real · escala · profundidad · movimiento de cámara profesional · drone cinematográfico · interiores habitables · oficinas contemporáneas · personas en situaciones naturales · hoteles en operación · construcción real · reuniones reales · actividad empresarial real.

**Rechazar:** apariencia generada · arquitectura imposible · mansiones artificiales · exceso de HDR · cielos irreales · personas plásticas · hologramas · monedas flotando · robots · lujo de champán, joyas y coches · gente posando de millonario · apretones de manos como única idea empresarial · pantallas financieras falsas · ambientes vacíos sin vida · fotografía demasiado genérica · repetición del mismo edificio, la misma modelo o el mismo lugar.

---

## 7. Sustitución del material generado

Se auditan `assets/img/xaru/` y `assets/img/xaru/gen2/`. Son candidatas todas las imágenes generadas o creadas para simular villas, mansiones, islas, hoteles, resorts, oficinas, personas, terrenos, arquitectura, ASHIMA, activos digitales, reuniones, desarrollos y ciudades.

**Se conserva únicamente:** logos, monogramas, identidad gráfica, favicons, iconos, las dos imágenes protegidas del hero y el material que sea claramente fotografía real y siga siendo coherente.

Nomenclatura clara, sin arrastrar nombres antiguos confusos:
`xaru-villa-beachfront-01.jpg` · `xaru-castle-france-01.jpg` · `xaru-hacienda-colonial-01.jpg` · `xaru-hotel-operating-01.jpg` · `xaru-land-coastal-01.jpg` · `xaru-office-international-01.jpg` · `xaru-capital-project-review-01.jpg` · `xaru-relocation-city-01.jpg`

---

## 8. Catálogo demostrativo — profundidad obligatoria

### 8.1 Private Real Estate — 10 categorías × 6 = **60 mínimo**
Casas contemporáneas · Villas · Mansiones · Castillos y châteaux · Haciendas · Fincas y estates · Penthouses · Residencias frente al mar · Propiedades ecuestres · Islas privadas.

**Variantes obligatorias por categoría** (una por cada una de las seis):

- **Casas contemporáneas:** urbana · montaña · tropical · frente al lago · golf · desierto
- **Villas:** frente al mar · montaña · mediterránea · tropical · urbana · dentro de resort
- **Mansiones:** waterfront · urbana · mediterránea · tropical · histórica · en comunidad privada
- **Castillos:** medieval · château francés · restaurado · con viñedo · palacio rural · fortaleza convertida
- **Haciendas:** colonial · cafetera · ecuestre · agrícola · con viñedo · tropical
- **Fincas y estates:** ecuestre · montaña · caza · olivar · viñedo · tropical
- **Penthouses:** Dubái · frente al mar · urbano contemporáneo · histórico europeo · dos niveles · terraza panorámica
- **Frente al mar:** casa de playa · sobre acantilado · en isla · villa caribeña · mediterránea · tropical asiática
- **Ecuestres:** con establos · centro residencial · finca de competición · hacienda ecuestre · polo · rural con pistas
- **Islas privadas:** caribeña · mediterránea · tropical asiática · con resort · sin desarrollar · archipiélago

### 8.2 Commercial & Hospitality — 8 categorías × 6 = **48 mínimo**
Hoteles operativos · Boutique hotels · Resorts · Apartahoteles y serviced residences · Marinas y beach clubs · Parques temáticos y destinos · Uso mixto · Proyectos hoteleros detenidos o incompletos.

Métricas propias por tipo: **hoteles** llaves, categoría, estado operativo, superficie · **resorts** llaves, extensión, frente de playa, amenidades · **marinas** amarres, infraestructura, superficie · **parques** área, tipo, estado, componentes · **incompletos** porcentaje de avance, uso previsto, área, capital estimado, precio de oportunidad.

### 8.3 Land & Master Developments — 6 categorías × 6 = **36 mínimo**
Suelo costero · Terrenos para hoteles y resorts · Terrenos para masterplan · Suelo urbano y uso mixto · Grandes terrenos agrícolas o de estate · Territorios insulares.

**Sin dormitorios ni baños.** Muestran: área en m² o hectáreas, país o región, tipo de suelo, uso proyectado, acceso, infraestructura, estado, precio y tipo de oportunidad.

Prohibido usar una villa para representar un terreno, o un resort terminado para representar suelo sin desarrollar.

### 8.4 Precios
**Todos por encima de USD 1.000.000.** Son demostrativos, pero razonables por tipología:

| Tipología | Rango USD |
|---|---|
| Casas contemporáneas | 1,2 M – 18 M |
| Villas | 2 M – 40 M |
| Mansiones | 5 M – 90 M |
| Castillos y châteaux | 4 M – 120 M |
| Haciendas | 2 M – 45 M |
| Fincas y estates | 2 M – 65 M |
| Penthouses | 2 M – 75 M |
| Frente al mar | 2,5 M – 60 M |
| Ecuestres | 3 M – 55 M |
| Islas privadas | 12 M – 450 M |

### 8.5 Coherencia de galería
Cada ficha: imagen principal **distinta** más 4 a 8 complementarias. Prohibido mezclar seis propiedades dentro de una ficha. Cuando exista serie completa del mismo inmueble, se usa esa serie. Cuando no, se combinan imágenes compatibles en arquitectura, clima, materiales y estilo. Nunca una villa mediterránea con interior de rascacielos, ni un château con interior tropical, ni una hacienda colonial con mobiliario futurista, ni una isla caribeña con paisaje mediterráneo seco.

---

## 9. Carácter demostrativo

Una sola declaración, discreta, en la cabecera general del catálogo:

> **Portafolio demostrativo para presentación.**

No se repite en cada tarjeta. No se convierte en banner. No se rebaja la sensación de calidad. Cada registro lleva `demo: true` para poder separarlo de futuros activos reales.

---

## 10. Modelo de datos

Prohibido escribir cientos de tarjetas repetidas a mano en el HTML. Sistema reutilizable en:

```
data/properties/private-real-estate.json
data/properties/commercial-hospitality.json
data/properties/land-developments.json
```

Campos: `id · demo · category · subcategory · variant · title · country · region · city · price_usd · currency · bedrooms · bathrooms · built_area_m2 · land_area_m2 · hectares · hotel_keys · status · short_description · long_description · features · hero_image · gallery · video · video_poster · featured · language_content · source_media_ids`

`null` para lo que no aplique. **Dormitorios y baños no son métrica universal.**

---

## 11. Filtros del catálogo

Fuera los genéricos de plantilla.

- **Private:** casas · villas · mansiones · castillos · haciendas · fincas · penthouses · frente al mar · ecuestres · islas privadas
- **Hospitality:** hoteles operativos · boutique · resorts · apartahoteles · marinas · beach clubs · parques y entretenimiento · uso mixto · proyectos incompletos
- **Land:** costa · resort · masterplan · urbano · uso mixto · agrícola · insular
- **Transversales:** país · región · precio · área · estado · tipo de oportunidad · destacado · con vídeo

---

## 12. Optimización técnica

**Imagen.** Se conservan los originales. Derivados AVIF, WebP y JPEG de respaldo a 480, 768, 1280, 1920 y 2560 px cuando el original lo permita. `<picture>`, `srcset`, `sizes`, `width`, `height`, lazy bajo el primer viewport, `decoding="async"`, `fetchpriority="high"` sólo en la principal, recortes específicos para móvil cuando haga falta. **Sin comprimir tanto que la fotografía pierda categoría.**

**Vídeo.** Descarga en máxima calidad. MP4 H.264 + WebM + póster WebP/AVIF, versión desktop y móvil cuando el encuadre lo exija. Todo vídeo: póster, `muted`, `playsinline`, `loop` si es decorativo, carga diferida fuera del primer viewport, pausa lejos del viewport, respeto a `prefers-reduced-motion` mostrando el póster. El hero puede cargar de inmediato; el resto al aproximarse. Nunca todos a la vez. Nunca audio automático.

---

## 13. Multiidioma

Los cuatro idiomas comparten los mismos medios físicos: **no se duplican imágenes ni vídeos por idioma**. Se localizan títulos, descripciones, alt text, botones, categorías, filtros, metadatos, Open Graph, Twitter y JSON-LD. Inglés, español, árabe y chino simplificado. RTL correcto en árabe. Una imagen no cambia al cambiar de idioma salvo que contenga texto, lo cual debe evitarse.

---

## 14. Estado visual exigido

**Debe dejar de parecer:** plantilla sin terminar · inmobiliaria con tres propiedades · colección de imágenes generadas · web sin actividad · presentación con categorías vacías · catálogo sin profundidad.

**Debe parecer:** plataforma con inventario · inmobiliaria internacional · catálogo de lujo profundo · estructura con hoteles, resorts y terrenos · plataforma con proyectos y capital · compañía con presencia visual · experiencia audiovisual · presentación corporativa completa · ecosistema con distintas entradas.

---

## 15. Auditoría final — 30 comprobaciones

Resoluciones: 1920×1080 · 1440×900 · 768×1024 · 390×844.

1. El hero conserva sus imágenes protegidas · 2. Sólo la última pasó a vídeo · 3. El vídeo respeta la paleta · 4. El nuevo slogan aparece de inmediato · 5. Real estate sigue siendo protagonista · 6. Open Graph transmite la nueva identidad · 7. Todo lo generado fuera del hero fue reemplazado · 8. Sólo fuentes autorizadas · 9. Cinco vídeos o más en portada · 10. Entre diez y catorce en la plataforma · 11. Seis opciones mínimo por categoría · 12. Todos los precios sobre USD 1 M · 13. Cada tipología con variantes · 14. Ninguna tarjeta vacía · 15. Ningún placeholder · 16. Ninguna marca de agua · 17. Ninguna ruta rota · 18. Ningún vídeo sin póster · 19. Sin repetición excesiva · 20. Sin filtros genéricos antiguos · 21. Cuatro idiomas operativos · 22. Catálogo usable en móvil · 23. Galerías coherentes · 24. Rendimiento sano · 25. Sin errores de consola · 26. Sin 404 · 27. OG con fotografía real · 28. Footer con la nueva narrativa · 29. About explica el significado ampliado · 30. La experiencia se siente completa.

Capturas antes y después de: hero · Private Real Estate · castillos · villas · mansiones · Commercial & Hospitality · Land & Developments · Projects & Capital · Financial Infrastructure · Corporate Services · About · home móvil · catálogo móvil.

---

## 16. Entrega

Commits: `Audit current visual system and media inventory` → `Reposition XARU HOME hero and social metadata` → `Replace AI imagery with licensed real stock` → `Add cinematic video system across public pages` → `Expand luxury real estate demo catalog` → `Expand hospitality and development opportunities` → `Optimize responsive media and multilingual content` → `Validate visual consistency performance and mobile UX`.

Pull request hacia `main`, título **Rebuild XARU HOME with real stock imagery, cinematic video and complete demo inventory**, con narrativa del hero, nuevo Open Graph, imágenes conservadas, última diapositiva en vídeo, número de imágenes sustituidas, vídeos añadidos, plataformas, propiedades creadas, categorías, hoteles y resorts, terrenos y proyectos, mejoras de filtros, móvil y rendimiento, capturas antes y después, archivos de datos creados y validaciones. **No fusionar automáticamente.**
