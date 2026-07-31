# AUDITORÍA DE INTEGRIDAD VISUAL Y DOCUMENTAL — XARU HOME

**Fases 1 y 2 · Inventario exhaustivo + verificación multi-viewport**
Rama: `agent/real-stock-media-audit` · Fecha: 2026-07-31 · Alcance: sitio público completo (EN raíz, `/es/`, `/ar/`, `/zh/`)
Documento asociado: [`media-replacement-plan.csv`](media-replacement-plan.csv)

> **Esta fase no modifica ni un solo archivo HTML/CSS/JS ni borra ninguna imagen. Es auditoría.**

---

## PRINCIPIO RECTOR APLICADO

> Una fotografía de stock puede representar una **CATEGORÍA** o una **CAPACIDAD**, pero **NUNCA** puede hacerse pasar por una propiedad, hotel, terreno o proyecto **CONCRETO**.
> Si un bloque muestra nombre, precio, ubicación, superficie o proyecto específico, necesita **material auténtico del activo**.

Regla operativa derivada, usada para puntuar cada bloque:

| Contexto del bloque | ¿Stock permitido? | ¿Material real obligatorio? |
|---|---|---|
| Pilar / división / capacidad ("Private Real Estate", "Capital & Transactions") | Sí, con licencia documentada | No |
| Ficha con nombre propio, precio, m², dirección o proyecto | **No** | **Sí** |
| Persona nombrada (equipo, agente, cliente, autor) | **No** | **Sí** (+ cesión de imagen) |
| Cualquier imagen generada por IA | **No, en ningún contexto** | — |

---

## 1. RESUMEN EJECUTIVO

### 1.1 Cifras del inventario

| Métrica | Valor |
|---|---|
| Páginas públicas recorridas | **184** (46 por idioma × 4 idiomas) |
| Referencias a medios detectadas (todas las páginas, todos los idiomas) | **2.560** |
| Archivos de medio únicos referenciados | **83** |
| Bloques únicos auditados (contexto EN canónico) | **622** |
| Filas del CSV (622 bloques con medio + 43 secciones vacías `MISSING_MEDIA`) | **665** |
| Archivos en disco bajo `assets/img` + `assets/video` | 198 |
| Archivos **huérfanos** (en disco, no referenciados) | **115** (≈ 4,2 MB) |
| Embeds de terceros | 1 (`youtube.com/embed/1PhiMWjAwcA`, ×5 por página en `single-property-v1`) |

### 1.2 Desglose por origen del material

| Origen | Archivos únicos | Bloques afectados | Conformidad con la nueva biblia |
|---|---|---|---|
| **IA generada (Magnific · modelo Seedream)** — `assets/img/xaru/gen2/` | **15** | 245 | ❌ **NO CONFORME** (prohibición total de IA) |
| **Composición sobre imagen IA** — `assets/img/xaru/og-cover.jpg` | **1** | 24 | ❌ **NO CONFORME** (hereda el original IA) |
| **Vídeo sintetizado con ffmpeg** — `assets/video/xr_ambient.mp4` | **1** | 1 | ❌ **NO CONFORME** (no documental, sin poster) |
| **Stock de plantilla comercial (Xproperty), procedencia NO documentada** | **57** | 130 | ⚠️ `LICENSE_NOT_DOCUMENTED` |
| **Marca propia XARU** (lockup, wordmark, monogramas, favicons) | **9** | 221 | ✅ **CONFORME** (vectorizado del logo del cliente) |
| `<video>` sin poster (defecto estructural, no archivo) | — | 1 | ⚠️ `MISSING_POSTER` |

**17 archivos únicos (270 bloques) son de origen sintético/IA y deben desaparecer del sitio.**
**57 archivos únicos (130 bloques) son stock de plantilla sin licencia trazable.**
**Sólo 9 archivos únicos del sitio (los de marca) están limpios.**

### 1.3 Severidad

| Nivel de riesgo de engaño | Bloques | % |
|---|---|---|
| **Crítico** | **178** | 26,8 % |
| Alto | 136 | 20,5 % |
| Medio | 120 | 18,0 % |
| Bajo (mayoritariamente marca propia e iconos) | 231 | 34,7 % |

- Bloques marcados **`REAL_MEDIA_REQUIRED`** (no admiten stock bajo ningún supuesto): **178**
- Bloques marcados **`needs_replacement = sí`**: **443 de 665** (66,6 %)

### 1.4 Frecuencia de códigos de incidencia

| Código | Bloques |
|---|---|
| `DUPLICATED_MEDIA` | 357 |
| `DECORATIVE_MEDIA_OVERUSE` | 339 |
| `POSSIBLE_AI_MEDIA` (→ IA **confirmada**) | 270 |
| `UNVERIFIED_ASSET_MEDIA` | 270 |
| `WRONG_SUBJECT` | 179 |
| `REAL_MEDIA_REQUIRED` | 178 |
| `TEXT_MEDIA_MISMATCH` | 154 |
| `PERFORMANCE_RISK` | 143 |
| `LICENSE_NOT_DOCUMENTED` | 130 |
| `GENERIC_STOCK` | 120 |
| `LOW_RESOLUTION` | 72 |
| `POOR_MOBILE_CROP` | 62 |
| `MISLEADING_ALT` | 19 |
| `MODEL_RELEASE_REVIEW` | 16 |
| `LOCATION_RELEASE_REVIEW` | 3 |
| `MISSING_POSTER` | 2 |
| `MISSING_MEDIA` (secciones sin ningún medio) | 43 |

> `MISSING_MEDIA` no se debe aquí a rutas rotas: **ningún archivo referenciado falta en disco y ninguna imagen falló al cargar** en los 4 viewports. Las 43 incidencias corresponden a **secciones de más de 380 px de alto sin ningún medio** (§5.4). El problema no es técnico: es documental.

---

## 2. PROBLEMAS CRÍTICOS

### 2.1 Tabla de problemas críticos

| # | Problema | Archivo(s) | Dónde | Qué afirma el texto | Qué muestra el medio | Códigos |
|---|---|---|---|---|---|---|
| **C-01** | **Imagen IA presentada como pabellón CONSTRUIDO de ASHIMA** | `gen2/06b_ashima_pavilion.jpg` | `index.html` § `projects` | "The Pavilion — **The first built expression of ASHIMA**, a pavilion raised from local materials and ancestral technique" | Torre cónica de fibra tejida en sabana costera con acacias; estética africana, no oaxaqueña. **No existe tal obra.** | `POSSIBLE_AI_MEDIA` `WRONG_SUBJECT` `REAL_MEDIA_REQUIRED` `TEXT_MEDIA_MISMATCH` |
| **C-02** | **Imagen IA presentada como vista aérea real del territorio de ASHIMA** | `gen2/06_masterplan_ashima.jpg` | `index.html`, `company/`, `developments/land-master-developments/`, `opportunities/lp-ashima-masterplan/` (15 bloques) | "ASHIMA — Ancestral Odyssey · **Oaxaca, México**" · `alt="ASHIMA — aerial view of the territory, Oaxaca, Mexico"` | Colinas de selva bajando a una playa dorada. Sin masterplan, sin trazado, sin arquitectura, sin marcador geográfico de Oaxaca. | `POSSIBLE_AI_MEDIA` `MISLEADING_ALT` `WRONG_SUBJECT` `REAL_MEDIA_REQUIRED` |
| **C-03** | **Hover-flip: toda ficha de propiedad revela una imagen de OTRO inmueble** | `gen2/10_casa_tulum.jpg` (buy/rent), `gen2/09_villa_como.jpg` (search) | `property-listing-buy/rent/search.html` — clase `cs_card_img_back` en **10 fichas × 3 listados × 4 idiomas** | "**The Thames Penthouse** · Westminster, London · **$12,5 M**" / "**Villa Lariana** · Lake Como · **$9,8 M**" / "**Sierra Blanca Residence** · Marbella · **$7,2 M**" | Al pasar el ratón aparece **una casa de selva en Tulum** (o una villa lacustre italiana) en todas ellas. | `WRONG_SUBJECT` `TEXT_MEDIA_MISMATCH` `DUPLICATED_MEDIA` `POSSIBLE_AI_MEDIA` |
| **C-04** | **Un mismo archivo IA para dos propiedades distintas con precios distintos** | `gen2/07_villa_dubai.jpg`, `gen2/08_penthouse_london.jpg`, `gen2/09_villa_como.jpg`, `gen2/10_casa_tulum.jpg` | los 3 listados | `07` → "Serene Palm Villa **$4,8 M** / 1200 sqft" **y** "Palm Crescent Estate **$28 M** / 1600 sqft". `08` → "Thames Penthouse $12,5 M" **y** "Belgravia House $16,4 M". `09` → "Villa Lariana $9,8 M" **y** "Villa Cadenabbia $11,2 M". `10` → "Casa Selva $3,9 M" **y** "Casa Aluxes $4,6 M" | La misma imagen sintética. Dos activos "distintos", mismo inmueble en pantalla. | `WRONG_SUBJECT` `DUPLICATED_MEDIA` `REAL_MEDIA_REQUIRED` |
| **C-05** | **Retratos de stock presentados como el equipo nombrado de XARU** | `team-img-1..6.jpg` | `about-us.html` § equipo, `agents-list.html` | "Alex Carter — Lead Real Estate Agent — (555) 123-4567 — **alex@xaruhome.com**", + Sarah Mitchell, James Thompson, Emily Davis, Daria Pimkina, Caleb Thornton | Seis retratos de estudio de modelos de banco de imágenes. **Ninguno es personal de XARU.** Nombres, teléfonos y correos corporativos ficticios. | `WRONG_SUBJECT` `MODEL_RELEASE_REVIEW` `MISLEADING_ALT` `REAL_MEDIA_REQUIRED` `LICENSE_NOT_DOCUMENTED` |
| **C-06** | **Rostros de stock presentados como clientes reales con testimonio** | `avatar-1/2/3.jpg` | `about-us.html` § testimonios | "Michael Williams — Customer", "Sarah Thomas — Property Investor", "David Martinez — Property Seller" + **el mismo texto de testimonio repetido literalmente en los tres** | Tres miniaturas 90×90 de rostros de stock. Testimonio inventado y clonado. | `WRONG_SUBJECT` `MODEL_RELEASE_REVIEW` `DUPLICATED_MEDIA` `REAL_MEDIA_REQUIRED` |
| **C-07** | **Autor de blog inexistente con retrato de stock** | `post-author.jpg` | `blog-details.html` | "**Ahon Bentham** — Hi, my name is Ahon Bentham. With years of experience in the real estate industry…" | Retrato 150×150 de stock. Autor inexistente firmando contenido editorial de XARU. | `WRONG_SUBJECT` `MODEL_RELEASE_REVIEW` `REAL_MEDIA_REQUIRED` |
| **C-08** | **Fotografía de Dubái ilustrando la localización de un activo que NO está en Dubái** | `city-dubai.jpg` | `property-details.html` § `Location`; `property-listing-search.html`; `contact.html` | "Location — **Full Address: 217 Horizon Heights Road, Silverstone Towers, NY 10022**" · `alt="Location — Dubai, United Arab Emirates"` | Vista urbana de Dubái. La dirección declarada es Nueva York. En `property-listing-search` el mismo archivo acompaña el encabezado "Private Island — Samaná Bay". | `WRONG_SUBJECT` `MISLEADING_ALT` `LOCATION_RELEASE_REVIEW` `TEXT_MEDIA_MISMATCH` |
| **C-09** | **Render/imagen sintética NO identificada como render en fichas de inversión** | los 15 de `gen2/` | 25 fichas de activo y oportunidad | "Territorial Land Holding, **11M+ m²**", "Quarry Licence & Aggregates Production", "Halted Hotel Project Seeking Capital", "Confidential Portfolio — Private Market" | Imágenes generativas sin rótulo "render", "ilustración" ni "imagen orientativa". El inversor las lee como fotografía documental del activo. | `POSSIBLE_AI_MEDIA` `UNVERIFIED_ASSET_MEDIA` `REAL_MEDIA_REQUIRED` |
| **C-10** | **Imagen de un activo distinto al descrito: cantera** | `gen2/03_land_mega.jpg` | `developments/land-master-developments/`, `opportunities/pa-quarry-license/` | "**Quarry Licence & Aggregates Production**" (licencia de cantera y producción de áridos) | Duna/matorral costero árido visto desde el aire. **No hay cantera, ni maquinaria, ni frente de explotación.** El mismo archivo sirve además para "11.000.000+ m²". | `WRONG_SUBJECT` `DUPLICATED_MEDIA` `REAL_MEDIA_REQUIRED` |
| **C-11** | **Imagen de un activo distinto al descrito: hotel urbano** | `gen2/05_hotel_project.jpg` | `property-listing-buy/search`, `ch-hotel-halted/`, `ch-hotel-operational/`, cabecera de `business-infrastructure/` | "**Hotel Project — Urban Flagship**", "Operating Boutique Hotel", "Halted Hotel Project Seeking Capital" | Hotel de acantilado oceánico con terrazas y piscina. **No es urbano, no está parado, no está en obra.** Además ilustra el pilar corporativo de infraestructura empresarial. | `WRONG_SUBJECT` `TEXT_MEDIA_MISMATCH` `DUPLICATED_MEDIA` |
| **C-12** | **Marca de terceros / de la plantilla visible en página pública** | `text-logo.svg` | `single-property-v1.html` (×3 por página, ×4 idiomas) | Héroe "Discover the Perfect Harmony of Luxury and Comfort" | Insignia circular con el texto **"VISIT OUR LUXURY PROPERTY"**: marca gráfica de la plantilla Xproperty, ajena a XARU. | `WRONG_SUBJECT` `LICENSE_NOT_DOCUMENTED` |
| **C-13** | **Contenido de vídeo de terceros presentado como recorrido de propiedad** | `youtube.com/embed/1PhiMWjAwcA` | `single-property-v1.html` § "Virtual Property Tour" | "Virtual Property Tour — You can visit virtually from home" | Vídeo alojado en un canal de YouTube ajeno, de origen y derechos no documentados, presentado como tour de una propiedad de XARU. | `UNVERIFIED_ASSET_MEDIA` `WRONG_SUBJECT` |
| **C-14** | **Página corporativa completa sin ningún material propio** | — | `company/index.html` (10 secciones), `about-us.html` § oficinas | "Who we are", "Team", "**Offices**", "Governance", "Operating model", "Network", "Entities" | **Cero imágenes.** Ninguna oficina, ninguna persona, ningún documento. La única imagen de la página es la cabecera: `gen2/01_hero_v2.jpg`, una **duna costera generada por IA** rotulada "Company". | `MISSING_MEDIA` `WRONG_SUBJECT` `REAL_MEDIA_REQUIRED` |
| **C-15** | **Tarjeta social (OG/Twitter) construida sobre imagen IA** | `xaru/og-cover.jpg` | `og:image` + `twitter:image` de 12 páginas EN × 4 idiomas = **96 declaraciones** | Es la carta de presentación de XARU en LinkedIn, WhatsApp y buscadores | Composición 1200×630 sobre una de las imágenes IA. Es la primera imagen que ve un inversor al recibir un enlace. | `POSSIBLE_AI_MEDIA` `UNVERIFIED_ASSET_MEDIA` |
| **C-16** | **Fichas demo de la plantilla con precios y direcciones ficticias** | `property-img-1..6.jpg`, `property-banner.jpg`, `apartment-7..10.jpg`, `floor-plan.png`, `floor-plan-2.png`, `plan.svg`, `kitchen/bed-room/drowing-room.jpg` | `property-details.html`, `single-property-v1.html` | "Golden Meadows $50.000", "Evergreen Estates $70.000 — 217 Horizon Heights Road, NY 10022", "Maple Ridge Apartments — 382 Blue Sky Boulevard, CO 80202", "Apartment $9.500.000", "20.000 satisfied clients" | Interiores y planos genéricos de la plantilla comercial. **Inventario, direcciones, planos y cifras de reputación completamente ficticios.** | `WRONG_SUBJECT` `GENERIC_STOCK` `LICENSE_NOT_DOCUMENTED` `REAL_MEDIA_REQUIRED` |
| **C-17** | **Vídeo sintético sin poster como firma del bloque "Digital Assets"** | `assets/video/xr_ambient.mp4` | `index.html` § `digital-assets` (4 idiomas) | "Property, Settled with Precision" | Bucle ambiental de 97 KB generado con ffmpeg, sin contenido documental. El `<video>` no declara `poster`: en conexión lenta el bloque queda negro. | `POSSIBLE_AI_MEDIA` `MISSING_POSTER` |

### 2.2 Lo que XARU está afirmando visualmente y no puede sostener

- **25 fichas de activo/oportunidad** con nombre propio, ubicación, precio o superficie están ilustradas exclusivamente con imágenes generadas por IA.
- **11 personas nombradas** (6 agentes, 3 clientes con testimonio, 1 autor de blog, 1 avatar de panel) son rostros de banco de imágenes.
- **1 proyecto insignia (ASHIMA)** se presenta con dos imágenes IA, una de ellas descrita textualmente como *obra ya construida*.
- **0 fotografías** de oficinas, equipo, obra, escritura, plano real o documento de XARU en todo el sitio.

---

## 3. ANÁLISIS POR PÁGINA

Bloques auditados por página (contexto EN; cada fila representa también sus equivalentes `/es/`, `/ar/`, `/zh/`).

| Página | Bloques | Crítico | Alto | Medio | Bajo | Archivos IA distintos | Observación dominante |
|---|---:|---:|---:|---:|---:|---:|---|
| `index.html` | 35 | **17** | 8 | 2 | 8 | **16** | Portada íntegramente IA: 3 diapositivas de héroe, 4 tarjetas de mercado, 8 fichas destacadas, ASHIMA ×2, vídeo sintético, "Nosotros" con la imagen del resort. |
| `property-listing-buy.html` | 32 | **22** | 2 | 1 | 7 | 11 | 10 fichas con precio y ubicación, todas IA + imagen trasera clonada. |
| `property-listing-search.html` | 31 | **21** | 2 | 1 | 7 | 11 | Igual que `buy`, con `09_villa_como` como trasera universal + `city-dubai.jpg` en el buscador. |
| `property-listing-rent.html` | 28 | **18** | 2 | 1 | 7 | 7 | 10 fichas de alquiler con renta mensual, todas IA. |
| `single-property-v1.html` | 34 | 5 | 2 | 13 | 14 | 1 | Demo de plantilla sin adaptar: 4 tipologías con precios ficticios, galería genérica, insignia ajena, YouTube de terceros. |
| `about-us.html` | 24 | **8** | 2 | 4 | 10 | 1 | 5 agentes + 3 testimonios de stock; sin una sola imagen de la empresa real. |
| `property-details.html` | 22 | **9** | 2 | 4 | 7 | 1 | Ficha completa (banner, planos, mapa, propiedades similares) 100 % plantilla, con dirección de Nueva York ilustrada con Dubái. |
| `blog.html` / `blog-details.html` | 20 / 20 | 0 / 1 | 2 / 2 | 11 / 10 | 7 / 7 | 1 | 6 fotos editoriales de stock + autor ficticio; artículos genéricos ajenos a la línea editorial de XARU. |
| `agents-list.html` | 18 | **7** | 2 | 2 | 7 | 1 | 6 agentes de stock con teléfonos y correos `@xaruhome.com`. |
| `real-estate/private-properties/index.html` | 15 | 6 | 4 | 1 | 4 | 6 | Catálogo de 6 residencias nominadas, las 6 IA. |
| `real-estate/index.html` | 14 | 6 | 3 | 1 | 4 | 6 | Pilar + fichas; la cabecera del pilar reutiliza la villa de Dubái. |
| `opportunities/index.html` | 13 | 4 | 4 | 1 | 4 | 3 | 4 oportunidades de inversión nominadas, todas IA. |
| `contact.html` | 13 | 1 | 2 | 3 | 7 | 1 | Fondo de contacto de plantilla + Dubái como imagen de sede. |
| `developments/land-master-developments/index.html` | 12 | **7** | 0 | 1 | 4 | 3 | ASHIMA + 11M m² + cantera + cartera confidencial: cuatro activos, tres imágenes IA. |
| `faq.html` | 12 | 0 | 2 | 3 | 7 | 1 | Ilustración vectorial de plantilla de 310 KB. |
| `insights/index.html` | 12 | 0 | 7 | 1 | 4 | 5 | 4 artículos de análisis ilustrados con las mismas imágenes de las fichas de activo. |
| `real-estate/commercial-hospitality/index.html` | 11 | 3 | 3 | 1 | 4 | 2 | Hotel operativo y hotel parado comparten el mismo archivo. |
| Fichas de activo `pp-*` y `ch-*` (9 páginas) | 10 c/u | 3 c/u | 2 c/u | 1 | 4 | 1 c/u | Cada ficha nominada = 1 imagen IA repetida en cabecera, cuerpo y `og:image`. |
| Fichas `opportunities/lp-*`, `pa-*`, `cf-*` (4 páginas) | 10 c/u | 3–5 | 0–2 | 1 | 4 | 1 c/u | Idéntico patrón. |
| `capital/index.html`, `capital/strategic-partnerships/`, `developments/index.html`, `developments/project-structuring/`, `business-infrastructure/` (×3), `private-enquiry/`, `opportunities/submit/` | 8 c/u | 0 | 3 | 1 | 4 | 1 c/u | **Páginas sin ningún medio en el cuerpo**: sólo cabecera IA + logotipos. Ver §5. |
| `company/index.html` | 9 | 1 | 3 | 1 | 4 | 2 | Ver C-14. |
| `capital/deal-room/index.html` | 9 | 1 | 3 | 1 | 4 | 2 | Terraza londinense IA como imagen de una sala de operaciones privada. |
| Artículos `insights/*` (4 páginas) | 9 c/u | 0 | 4 c/u | 1 | 4 | 1–2 | Cada artículo hereda la imagen de la ficha de activo de la que habla. |

---

## 4. ANÁLISIS DE REPETICIONES

Regla aplicada: un mismo archivo usado en **secciones que explican servicios, activos o categorías DIFERENTES** es `DUPLICATED_MEDIA`, y la severidad crece con la distancia semántica entre esos contextos.

| Archivo | Usos en todo el sitio | Contextos distintos (EN) | Severidad | Contextos incompatibles entre sí |
|---|---:|---:|---|---|
| `gen2/10_casa_tulum.jpg` | **144** | **28** | **Crítica** | Ficha "Beachfront Residence, Tulum" · cabecera de `insights/` · **imagen trasera de las 10 fichas de `buy` y las 10 de `rent`** (Londres, Dubái, Como, Marbella, CDMX…). Una casa de selva representa un ático del Támesis. |
| `gen2/09_villa_como.jpg` | **108** | **20** | **Crítica** | Ficha "Lakefront Estate, Lake Como" · portada de `private-properties` · **trasera de las 10 fichas de `search`**, incluidas Casa Selva (Tulum), Polanco (CDMX) y Palm Crescent (Dubái). |
| `gen2/05_hotel_project.jpg` | **116** | **18** | **Crítica** | "Operating Boutique Hotel" (activo en explotación) · "Halted Hotel Project Seeking Capital" (activo parado) · "Hotel Project — Urban Flagship" (urbano) · categoría "Commercial & Hospitality" · **cabecera del pilar `business-infrastructure/` (servicios corporativos y comercio)** · artículo de hostelería operativa. Cinco relatos incompatibles con una sola foto. |
| `gen2/03_land_mega.jpg` | **116** | **18** | **Crítica** | "Territorial Land Holding, 11M+ m²" · **"Quarry Licence & Aggregates Production"** · pilar `developments/` · portada de `opportunities/` · artículo "Territorial land" · ficha "Coastal Development Land". Terreno, cantera y categoría con la misma duna. |
| `gen2/08_penthouse_london.jpg` | **92** | **17** | **Crítica** | "Penthouse, Central London" · "The Thames Penthouse $12,5 M" · "The Belgravia House $16,4 M" · **`capital/deal-room/` (sala de operaciones)** · **`business-infrastructure/corporate-services/` (relocalización y servicios corporativos)** · artículo de establecimiento internacional. |
| `gen2/13_investment_bg.jpg` | **92** | **15** | **Alta** | Pilar `capital/` · `capital/strategic-partnerships/` · **ficha nominada "Confidential Portfolio — Private Market"** · `private-enquiry/` · artículo de capital. Un fondo decorativo se convierte en la imagen de un activo concreto. |
| `gen2/07_villa_dubai.jpg` | **72** | **14** | **Crítica** | Categoría "Private Real Estate" · ficha "Signature Villa, Dubai" · **"Serene Palm Villa $4,8 M"** · **"Palm Crescent Estate $28 M"** · cabecera del pilar `real-estate/`. Dos precios, un inmueble. |
| `gen2/04_resort_dev.jpg` | 48 | 11 | **Crítica** | **`index.html` § "Nosotros / One Structure, Built on Five Pillars"** (bloque corporativo: 20 años de trayectoria, estructura NEXARU) · ficha "Beach Resort, Development Stage" · ficha "Resort Development — Turnkey" · cabecera de `developments/project-structuring/`. **La foto que ilustra "quiénes somos" es la misma que vende un resort concreto.** |
| `gen2/06_masterplan_ashima.jpg` | 40 | 13 | **Crítica** | Proyecto ASHIMA (4 contextos) · categoría "Land & Master Developments" · diapositiva de héroe "Master Developments, From Land to Legacy" · `company/` § proyectos. |
| `gen2/02_island_rd.jpg` | 32 | 10 | **Alta** | Diapositiva de héroe · ficha "Private Island, Samaná Bay" · ficha de listado · cabecera de `pp-samana-island/`. |
| `xaru/og-cover.jpg` | **96** | 12 | **Alta** | `og:image` + `twitter:image` de 12 páginas EN de temáticas completamente distintas (portada, blog, FAQ, contacto, listados, ficha). Sin diferenciación social por página. |
| `footer-bg-1.svg` | **196** | 46 | Media (rendimiento) | Pie de página de **las 184 páginas públicas**. SVG de **926 KB** descargado en cada visita. |
| `city-dubai.jpg` | 12 | 3 | **Crítica** | Sede de contacto · localización de una ficha con dirección en Nueva York · buscador junto a "Private Island — Samaná Bay". |
| `team-img-5.jpg` | 12 | 3 | **Crítica** | "Daria Pimkina, Real Estate Agent" en `about-us` **y** en `agents-list`, **y además** como avatar de la usuaria "Amanda Jones" en la barra de perfil. Una cara, tres identidades. |
| `post-img-2.jpg` / `post-img-3.jpg` | 20 c/u | 5 c/u | Media | Cada una ilustra **dos artículos con títulos distintos** dentro de la misma página de blog, más la barra lateral. |

**Conclusión de repeticiones:** 357 de 622 bloques (57 %) reutilizan un archivo ya empleado en otro contexto semántico. El sitio da la impresión de un catálogo amplio con **11 fotografías sintéticas** girando en bucle.

---

## 5. CAMPOS VISUALES VACÍOS Y HALLAZGOS DE LA VERIFICACIÓN MULTI-VIEWPORT

Verificación con Chromium (Playwright) en **1440×900, 1920×1080, 768×1024 y 390×844**, sobre 18 páginas representativas de los 4 idiomas.

### 5.1 Lo que NO falla

- **0 medios que no cargan.** Ninguna ruta rota, ningún `naturalWidth = 0`.
- **0 imágenes deformadas.** Todos los `<img>` con contenido usan `object-fit: cover`; no hay estiramientos.

### 5.2 Recortes malos y foco perdido (`POOR_MOBILE_CROP` / `WRONG_CROP`)

| Elemento | Nativo | Contenedor a 390×844 | Pérdida | Efecto |
|---|---|---|---|---|
| Héroe de portada — `01_hero_v2`, `02_island_rd`, `06_masterplan_ashima` | 1920×1080 (ratio 1,78) | 603×1305 (**ratio 0,46**) | **≈ 74 % del encuadre horizontal** | En móvil sólo se ve un fragmento de duna/arena. Se pierden la costa, la línea de agua y la lectura aérea que justifica cada diapositiva. Confirmado en la captura `mv_home_390.jpg`. |
| Bloque CTA — `14_cta_bg` | 1920×1080 | 366×624 (ratio 0,59) | ≈ 67 % | La piscina infinita queda reducida a una banda de agua sin horizonte. |
| Contacto — `contact-bg.jpg` | template | 390×1279 (**ratio 0,30**) | ≈ 83 % | El fondo pierde todo contenido reconocible. |
| Fichas de listado — `07/08/09/10/11/12` | 900×506 | tarjeta 4:3 a 768 y 390 px | **`cropLoss = 0,44`** | Se amputa el 44 % del encuadre; en varias fichas desaparece el elemento que daba sentido a la imagen (piscina, fachada, línea de costa). |

Todos los fondos usan `background-position: 50% 50%` sin punto focal por breakpoint: no hay `object-position` ni variantes verticales del recurso.

### 5.3 Baja resolución efectiva

- `city-dubai.jpg` (456×550) se muestra a 963 px de ancho en 1920×1080 → **escalado ×2,11** (`LOW_RESOLUTION`).
- Las 6 imágenes de residencias de `gen2/` son **900×506** pero se usan también como **fondo a ancho completo** en cabeceras de ficha (`cs_page_header`) y en secciones de 1920 px → 72 bloques marcados `LOW_RESOLUTION`.
- Los retratos de equipo (504×585) se sirven sin variante retina.

### 5.4 Campos visuales vacíos (`MISSING_MEDIA`)

Secciones de más de 380 px de alto **sin ninguna imagen, vídeo ni fondo**:

| Página | Secciones vacías | Alto acumulado (1440×900) |
|---|---|---|
| `company/index.html` | `who-we-are`, `values`, `operating-model`, `entities`, `governance`, `team`, `offices`, `network`, `contact` (**9**) | ≈ 5.700 px |
| `index.html` (los 4 idiomas) | `journey`, `capability`, `dual`, `infra`, `presence`, `governance`, `insights-home`, `private-desk` + 1 bloque gris (**9**) | ≈ 5.900 px |
| `real-estate/index.html` | `s02`, `s03`, `s06`, `s11`, `s12` (+ `s01`, `s05`, `s07`, `s08`, `s10` sólo en móvil) | ≈ 2.200 px |
| `business-infrastructure/index.html` | `divisions`, `governance` + 2 bloques sin id | ≈ 1.800 px |
| `developments/index.html` | `chain`, `divisions` + 2 bloques sin id | ≈ 1.700 px |
| `capital/index.html` | `two-way`, `cs_gray2_bg` + 1 bloque | ≈ 1.500 px |
| `opportunities/submit/index.html` | 3 bloques (uno de 1.560 px) | ≈ 2.800 px |
| `private-enquiry/index.html` | 1 bloque de 896 px | 896 px |
| `about-us.html` | `cs_gray2_bg` (940 px; **1.735 px en móvil**) | 940 px |
| `contact.html` | 1 bloque de 659 px | 659 px |
| `insights/index.html` | `sectors` (856 px; **1.979 px en móvil**) | 856 px |

Estas zonas son la oportunidad de sustitución: **es donde debe entrar material real de XARU, no donde hay que meter más stock decorativo.**

### 5.5 Rendimiento (`PERFORMANCE_RISK`)

- `footer-bg-1.svg` — **926 KB**, cargado en las **184 páginas públicas**. Mayor coste unitario del sitio.
- `illustartion.svg` — 310 KB en `faq.html`.
- 7 imágenes IA por encima de 400 KB (`03_land_mega` 582 KB, `04_resort_dev` 515 KB, `05_hotel_project` 502 KB, `06_masterplan_ashima` 458 KB, `02_island_rd` 414 KB…), sin variantes WebP/AVIF ni `srcset`.
- **115 archivos huérfanos (≈ 4,2 MB)** siguen en el repositorio, entre ellos **los 13 archivos IA de la primera tanda** (`assets/img/xaru/gen/`) y **8 logotipos de marcas de terceros** (`lamborghini-logo.svg`, `moser.svg`, `zima.svg`, `realme-logo.svg`, `moode.svg`, `google.svg`, `logo.svg`, `logo-2.svg`). No se publican, pero se distribuyen con el sitio: deben eliminarse en la fase de limpieza.

### 5.6 Evidencias capturadas

| Archivo | Viewport | Qué demuestra |
|---|---|---|
| `/home/claude/work/site/audit/media/mv_home_1440.jpg` | 1440×900 | Héroe de portada: la imagen IA (duna costera) es todo el mensaje visual de "Exceptional Properties. Projects of Scale." |
| `/home/claude/work/site/audit/media/mv_home_390.jpg` | 390×844 | Recorte móvil del mismo héroe: sólo arena, sin costa ni horizonte. `POOR_MOBILE_CROP` confirmado. |
| `/home/claude/work/site/audit/media/mv_listing_768.jpg` | 768×1024 | Listado "Private Islands & Luxury Property for Sale": la parte alta es un formulario de filtros sin ninguna imagen; el catálogo empieza por debajo del pliegue. |
| `/home/claude/work/site/audit/media/mv_company_1440.jpg` | 1440×900 | Página `Company`: cabecera con imagen IA de playa + primer bloque corporativo completamente vacío de medios. |

---

## 6. TABLA DE CORRESPONDENCIA TEXTO ↔ MEDIO — LOS PEORES CASOS

Escala `correspondence_0_5`: **0** = el medio contradice o suplanta al texto · **5** = el medio documenta el texto.

| Bloque | Qué afirma el texto | Qué muestra realmente el medio | Corr. | Riesgo |
|---|---|---|---|---|
| `index.html` § projects — `06b_ashima_pavilion.jpg` | "La **primera expresión construida** de ASHIMA — un pabellón levantado con materiales locales y técnica ancestral" | Torre cónica tejida generada por IA, en una sabana con acacias. Obra inexistente. | **0** | Crítico |
| `index.html` § projects — `06_masterplan_ashima.jpg` (`alt` = "aerial view of the territory, Oaxaca, Mexico") | "ASHIMA — Ancestral Odyssey · Oaxaca, México. Master development a escala santuario" | Selva y playa genéricas generadas por IA. Ni masterplan, ni Oaxaca, ni territorio identificable. | **0** | Crítico |
| `property-listing-buy` § The Thames Penthouse — trasera `10_casa_tulum.jpg` | "The Thames Penthouse · Westminster, London · **$12,5 M** · 1300 sqft" | Casa de selva tropical en Tulum. | **0** | Crítico |
| `property-listing-buy` § Palm Crescent Estate — `07_villa_dubai.jpg` | "**$28 M** · 1600 sqft · Palm Jumeirah" | La **misma** imagen que ilustra "Serene Palm Villa · $4,8 M · 1200 sqft". | **0** | Crítico |
| `about-us` / `agents-list` § equipo — `team-img-1..6.jpg` | "Alex Carter — Lead Real Estate Agent — alex@xaruhome.com" (+5 más) | Seis modelos de banco de imágenes. | **0** | Crítico |
| `about-us` § testimonios — `avatar-1/2/3.jpg` | "Michael Williams, Customer" / "Sarah Thomas, Property Investor" / "David Martinez, Property Seller" + testimonio idéntico ×3 | Tres rostros de stock de 90×90. | **0** | Crítico |
| `property-details` § Location — `city-dubai.jpg` | "Full Address: 217 Horizon Heights Road, Silverstone Towers, **NY 10022**" | Skyline de **Dubái**. | **0** | Crítico |
| `opportunities/pa-quarry-license` — `03_land_mega.jpg` | "Quarry Licence & **Aggregates Production**" | Duna costera árida sin cantera, sin maquinaria, sin frente de explotación. | **0** | Crítico |
| `property-listing-buy` § Hotel Project — `05_hotel_project.jpg` | "Hotel Project — **Urban Flagship** · estructuración llave en mano" | Hotel de acantilado sobre el océano. | **0** | Crítico |
| `blog-details` § autor — `post-author.jpg` | "Ahon Bentham — con años de experiencia en el sector inmobiliario…" | Retrato de stock; autor inexistente. | **0** | Crítico |
| `index.html` § about — `04_resort_dev.jpg` | "Más de **20 años** guiando a clientes privados… XARU HOME reúne esa experiencia en una estructura — una marca NEXARU" | Palapas de un resort de playa generado por IA; el **mismo** archivo que vende el activo "Beach Resort, Development Stage". | **1** | Alto |
| `company/index.html` § cabecera — `01_hero_v2.jpg` | "Company — De la estructura corporativa a la operación" | Duna de playa generada por IA. Bajo ella, 9 secciones corporativas sin ninguna imagen. | **1** | Alto |
| `capital/deal-room` § cabecera — `08_penthouse_london.jpg` | "**Private Deal Room** — acceso restringido a operaciones confidenciales" | Terraza residencial londinense con sofás y olivos. | **1** | Alto |
| `business-infrastructure/index` § cabecera — `05_hotel_project.jpg` | "Business Infrastructure — comercio, financiación, servicios corporativos y relocalización" | Hotel de acantilado. | **1** | Alto |
| `opportunities/lp-land-11m` — `03_land_mega.jpg` | "Territorial Land Holding, **11.000.000+ m²** listos para masterplan, República Dominicana" | Fragmento de duna sin escala, sin linderos, sin referencia catastral. | **1** | Alto |
| `real-estate/private-properties/pp-villa-marbella` — `11_villa_marbella.jpg` | "Villa, **Milla de Oro de Marbella**" | Villa blanca mediterránea genérica de IA. | **1** | Alto |
| `single-property-v1` § tipologías — `apartment-7..10.jpg` | "Apartment $9.500.000 / Duplex $9.700.000 / Penthouse $9.800.000 / Bungalow $9.900.000" | Cuatro interiores de la plantilla comercial. Inventario y precios inexistentes. | **1** | Alto |
| `index.html` § digital-assets — `xr_ambient.mp4` | "Property, Settled with Precision" | Bucle sintético de 97 KB generado con ffmpeg, sin poster. | **0** | Alto |
| `insights/*` (4 artículos) | Análisis de mercado sobre suelo, hostelería, capital y establecimiento internacional | Cada artículo reutiliza la imagen IA de la ficha de activo correspondiente: el análisis parece publicidad del activo. | **2** | Alto |
| `faq.html`, `blog.html`, `contact.html` (fondos y post) | Contenido corporativo propio | Stock de plantilla sin licencia documentada. Aceptable como *categoría*, no documentado. | **2** | Medio |

---

## 7. QUÉ MATERIAL REAL DEBE ENTREGAR XARU

Lista accionable. Cada entrada indica el material mínimo para levantar el bloqueo de los bloques marcados `REAL_MEDIA_REQUIRED` (**178 bloques**).

### 7.1 Por activo inmobiliario nominado
*Sin este material, la ficha debe retirarse o despublicarse — no puede sustituirse por stock.*

Para **cada uno** de los activos siguientes:

1. **8–15 fotografías originales del inmueble** (exterior, acceso, estancias principales, vistas), en ≥ 3000 px de lado largo.
2. **1 imagen apaisada 16:9 y 1 vertical 4:5** del mismo activo (para héroe desktop y móvil, evitando el recorte del 74 %).
3. **Ficha de procedencia**: autor, fecha de captura, ubicación GPS o dirección, y **property release** firmado por el titular.
4. Si sólo existe proyecto: **render oficial** + obligación de rotularlo visiblemente como *RENDER / IMAGEN DE PROYECTO*.

| Activo | Páginas afectadas | Sustituye a |
|---|---|---|
| **Isla privada, bahía de Samaná** (Rep. Dominicana) | `pp-samana-island/`, `real-estate/`, `private-properties/`, portada, 2 listados | `gen2/02_island_rd.jpg` |
| **Suelo territorial 11.000.000+ m²** (Rep. Dominicana) — se requiere además **ortofoto o vuelo de dron con linderos y plano catastral** | `opportunities/lp-land-11m/`, `developments/`, `land-master-developments/`, `opportunities/`, artículo `territorial-land`, 2 listados | `gen2/03_land_mega.jpg` |
| **Licencia de cantera y producción de áridos** — se requiere **fotografía del frente de explotación, maquinaria y copia de la licencia** | `opportunities/pa-quarry-license/`, `land-master-developments/` | `gen2/03_land_mega.jpg` |
| **Resort en desarrollo (Caribe)** — fotografía de obra fechada + plano de fase | `ch-resort-development/`, `project-structuring/`, portada, 2 listados | `gen2/04_resort_dev.jpg` |
| **Hotel boutique en explotación** — fotografía del hotel real + acreditación de operación | `ch-hotel-operational/`, `commercial-hospitality/`, portada | `gen2/05_hotel_project.jpg` |
| **Proyecto hotelero parado (urbano)** — fotografía del edificio parado en su estado actual | `ch-hotel-halted/`, `commercial-hospitality/`, portada, 2 listados | `gen2/05_hotel_project.jpg` |
| **Villa Dubái / Palm Jumeirah** | `pp-villa-dubai/`, `real-estate/`, portada, 3 listados ("Serene Palm Villa", "Palm Crescent Estate") | `gen2/07_villa_dubai.jpg` |
| **Ático Central London / Thames** y **Belgravia House** (dos activos → **dos reportajes distintos**) | `pp-penthouse-london/`, portada, 3 listados | `gen2/08_penthouse_london.jpg` |
| **Villa Lariana** y **Villa Cadenabbia**, lago de Como (**dos reportajes distintos**) | `pp-villa-como/`, `private-properties/`, portada, 3 listados | `gen2/09_villa_como.jpg` |
| **Casa Selva** y **Casa Aluxes**, Tulum (**dos reportajes distintos**) | `pp-casa-tulum/`, portada, 3 listados | `gen2/10_casa_tulum.jpg` |
| **Sierra Blanca Residence**, Marbella | `pp-villa-marbella/`, `real-estate/`, portada, 3 listados | `gen2/11_villa_marbella.jpg` |
| **Polanco Sky Residence**, Ciudad de México | 3 listados | `gen2/12_atico_cdmx.jpg` |
| **Cartera confidencial — mercado privado** | `cf-confidential-portfolio/`, `deal-room/`, `opportunities/`, `land-master-developments/`, portada | `gen2/13_investment_bg.jpg` — si la confidencialidad impide mostrar los activos, **sustituir por una composición tipográfica/documental, nunca por una foto que insinúe un activo** |

### 7.2 Proyecto ASHIMA (prioridad máxima)

1. **Masterplan oficial** (plano general, zonificación, fases) en calidad de publicación.
2. **Renders oficiales** del estudio de arquitectura, con **rótulo obligatorio "RENDER — PROYECTO NO CONSTRUIDO"** y crédito del autor.
3. **Fotografía aérea real del territorio en Oaxaca**, fechada y georreferenciada.
4. **Del pabellón**: si está construido, reportaje fotográfico de obra; si no lo está, **retirar la afirmación "first built expression"** del texto o acompañarla del render rotulado.
5. Licencia de uso de los renders cedida por el estudio autor.

### 7.3 Corporativo y personas

| Necesidad | Detalle | Desbloquea |
|---|---|---|
| **Retratos reales del equipo** | Sesión corporativa de las personas que realmente trabajan en XARU HOME, con nombre, cargo y contacto verdaderos + **cesión de imagen firmada** por cada una | `about-us.html`, `agents-list.html` (11 retratos falsos) |
| **Fotografía de las oficinas reales** | Sedes declaradas en `company/§offices` y `contact.html`: exterior, recepción, sala de reuniones | `company/`, `contact.html`, `about-us.html`; llena 9 secciones vacías |
| **Testimonios verificables** | Clientes reales con autorización escrita, o **eliminar el bloque de testimonios** | `about-us.html` (3 testimonios clonados) |
| **Autoría editorial real** | Firma y retrato del autor real de cada artículo, o firma institucional "XARU HOME" | `blog-details.html`, artículos de `insights/` |
| **Documentación corporativa** | Certificados de constitución, licencias, membresías, organigrama de entidades (NEXARU GLOBAL) — material visual verificable para `governance`, `entities`, `operating-model` | `company/` (9 secciones vacías), `about-us.html` |
| **Trayectoria demostrable** | Fotografías de operaciones cerradas o proyectos entregados que respalden "más de 20 años" | `index.html § about`, `about-us.html` |

### 7.4 Marca y piezas técnicas

| Necesidad | Detalle |
|---|---|
| **Tarjeta social (OG) sin IA** | Nueva `og-cover` 1200×630 sobre fondo de marca/tipografía o fotografía documental con licencia. Idealmente, una por pilar (real estate, developments, capital, business infrastructure). |
| **Variantes de recorte por breakpoint** | Para cada imagen de héroe y cabecera: versión 16:9 (desktop) y 4:5 o 9:16 (móvil), o definición de punto focal (`object-position` / `background-position`) por activo. |
| **Resolución mínima** | 1920 px de ancho para fondos a ancho completo; 2× para retratos y tarjetas. Las actuales de 900×506 son insuficientes. |
| **Poster de vídeo** | Fotograma documental para el `<video>` de `index § digital-assets`, o retirada del bloque junto con `xr_ambient.mp4`. |
| **Registro de licencias** | Hoja de control (recurso · proveedor · nº de licencia · factura · fecha · alcance) para los 57 archivos de plantilla que se decida conservar. Sin ella, todos permanecen en `LICENSE_NOT_DOCUMENTED`. |
| **Limpieza del repositorio** | Eliminar los 115 huérfanos (4,2 MB), incluidos los 13 archivos IA de `assets/img/xaru/gen/` y los 8 logotipos de terceros que se distribuyen sin usarse. |
| **Optimización** | Sustituir `footer-bg-1.svg` (926 KB × 184 páginas) e `illustartion.svg` (310 KB); generar WebP/AVIF y `srcset` para todo el material nuevo. |

### 7.5 Contenido de plantilla que debe eliminarse, no reemplazarse

Estas páginas son demos de la plantilla comercial con inventario, direcciones, planos y cifras ficticias. **La recomendación no es cambiar la foto: es retirar la página o reconstruirla sobre un activo real.**

- `single-property-v1.html` (4 idiomas) — 4 tipologías con precios inventados, insignia "VISIT OUR LUXURY PROPERTY" de la plantilla, embed de YouTube de terceros, "20.000 clientes satisfechos".
- `property-details.html` (4 idiomas) — "Evergreen Estates", direcciones de Nueva York y Colorado, planos genéricos, Dubái como mapa.
- `blog.html` / `blog-details.html` (4 idiomas) — 6 artículos genéricos de real estate estadounidense firmados por un autor inexistente.
- `agents-list.html` (4 idiomas) — directorio de agentes que no existen.

---

## 8. METODOLOGÍA

**Fase 1 — Inventario.** Script `audit/extract_media.py` (BeautifulSoup + lxml) sobre las 184 páginas públicas de los 4 idiomas. Extrae `<img src|data-src|srcset|alt>`, `<source>`, `<video src|poster>`, `data-background`, `data-src` (fondos diferidos de la plantilla, `cs_bg_filed`), `background-image` en `style` en línea y en bloques `<style>` de página, `og:image`, `twitter:image` y `<link rel="icon|apple-touch-icon">`. Cada referencia se ancla a su sección contenedora (`<section>/<header>/<footer>/<article>`, por `id` o clase) y al encabezado más próximo dentro del bloque, junto con el texto acompañante. Dimensiones y peso leídos con Pillow desde disco.

**Fase 2 — Verificación visual.** Script `audit/f7_viewports.py` (Playwright + Chromium de `/opt/pw-browsers`) sobre 18 páginas en 4 viewports (1440×900, 1920×1080, 768×1024, 390×844), con scroll completo para forzar la carga diferida. Mide por elemento: carga efectiva (`naturalWidth`), deformación (relación de aspecto nativa vs. renderizada según `object-fit`), pérdida por recorte en `cover`, factor de escalado, y detecta secciones de más de 380 px de alto sin ningún medio. **No se ha modificado ningún archivo del sitio.**

**Colapso de idiomas.** Las 4 variantes lingüísticas son estructuralmente idénticas en cuanto a medios. El CSV emite una fila por bloque **canónico en inglés** (622 filas con medio + 43 filas `MISSING_MEDIA` = 665) con la columna `languages = en|es|ar|zh`; la columna `repetition_count` cuenta las ocurrencias **en todo el sitio, los 4 idiomas incluidos** (por eso `10_casa_tulum.jpg` marca 144), y `distinct_contexts` cuenta los contextos semánticos diferentes en la versión inglesa.

**Artefactos de la auditoría** (fuera del sitio publicado, en `/home/claude/work/site/audit/`): `media_inventory.json` (2.560 referencias en bruto), `viewport_report.json` (medidas por elemento y viewport), `rows.json`, `usage_en.txt`, y las capturas en `media/`.
