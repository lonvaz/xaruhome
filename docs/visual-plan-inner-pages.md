# PLAN VISUAL DE PÁGINAS INTERIORES — XARU HOME
**Fase 4 · Dirección de arte documental** (incluye Fase 12 — color y dirección fotográfica · Fase 13 — accesibilidad)
Rama `agent/real-stock-media-audit` · 31-jul-2026
Insumos: [`visual-audit.md`](visual-audit.md) · [`media-replacement-plan.csv`](media-replacement-plan.csv) · `DERROTERO_MAESTRO_V2.md` §3, §5, §6

> **Este documento no modifica ningún archivo del sitio. Es plan.**

---

## 0. REGLA RECTORA APLICADA A LAS INTERIORES

> Stock = **categoría o capacidad**. Nunca un **activo concreto**.
> En cuanto una página nombra, sitúa, mide o pone precio a algo, entra en territorio de **material auténtico obligatorio**.

Matriz de decisión que gobierna todo este documento:

| Tipo de página | Cabecera | Cuerpo | Tarjetas / galería |
|---|---|---|---|
| Página pilar de división | CATEGORÍA (stock permitido) | CATEGORÍA | — |
| Catálogo / listado | CATEGORÍA (hero editorial) | CATEGORÍA | **ESPECÍFICO** por tarjeta |
| Ficha de detalle | **ESPECÍFICO** | **ESPECÍFICO** | **ESPECÍFICO** |
| Proyecto / single-property | **ESPECÍFICO** (foto de sitio) + render **rotulado** | ESPECÍFICO | ESPECÍFICO |
| Company / About | **ESPECÍFICO** (material propio) | ESPECÍFICO o MARCA | — |
| Agents-list | **ESPECÍFICO** (retrato real) — sin excepción | — | — |
| Contact | **ESPECÍFICO** (sede real) | — | — |
| Blog / Insights | CATEGORÍA editorial | CATEGORÍA editorial | CATEGORÍA editorial |
| FAQ | MARCA / 1 editorial máx. | Tipográfico | — |

---

## 1. CATÁLOGOS Y LISTADOS

Alcance: `real-estate/`, `real-estate/private-properties/`, `real-estate/commercial-hospitality/`, `developments/`, `developments/land-master-developments/`, `developments/project-structuring/`, `capital/`, `capital/strategic-partnerships/`, `capital/deal-room/`, `opportunities/`, `business-infrastructure/` (×3), `property-listing-buy|rent|search.html`.

### 1.1 Hero editorial de categoría — **permitido**

Cada catálogo abre con **una** imagen de categoría a ancho completo. No es un activo: es la puerta de una tipología.

| Catálogo | Qué muestra el hero | Qué NO puede mostrar |
|---|---|---|
| **Private Properties** | Volumen residencial en escorzo, sombra arquitectónica, patio, un fragmento de fachada de autor. | Ninguna de las villas del catálogo. Ningún interior. Nada que se pueda confundir con la ficha nº 1. |
| **Commercial & Hospitality** | Operación en curso a media distancia: recepción, office, cambio de turno, terraza antes de la apertura. | Un hotel identificable. **Nunca** el mismo archivo para "hotel operativo" y "hotel parado" (hoy comparten `05_hotel_project.jpg`). |
| **Land & Master Developments** | Territorio, relieve, límite de uso, camino de tierra, línea de costa larga. | Linderos, coordenadas, referencia catastral, superficie sobreimpresa. Nada que insinúe los 11M m². |
| **Project Structuring** | Materia de proyecto: mesa con planos, maqueta, replanteo en campo, andamio. | Un proyecto concreto de XARU. |
| **Capital & Partnerships** | Sala de reuniones vacía, luz de ventana sobre mesa, archivo. | Gráficos bursátiles, monedas, apretones de manos, dinero. |
| **Deal Room** | Umbral, puerta cerrada, pasillo, penumbra. | Una terraza residencial (hoy `08_penthouse_london.jpg` ilustra la sala de operaciones privada). |
| **Trade & Financial Infrastructure** | Terminal de carga, contenedores, cinta de conciliación, sala de servidores. | Nubes con candados, código binario, hologramas, "fintech" ilustrada. |
| **Corporate Services & Relocation** | Ventanilla administrativa, sala de espera institucional, escritorio con expediente, tránsito en aeropuerto de madrugada. | Familias sonrientes de banco de imágenes, pasaportes con datos legibles, banderas. |

Regla añadida: **un hero de categoría no se reutiliza en dos catálogos distintos.** Hoy `05_hotel_project.jpg` encabeza a la vez hospitality y `business-infrastructure/` (comercio, financiación y relocalización): cinco relatos incompatibles con una foto.

### 1.2 Tarjetas individuales — **material auténtico obligatorio**

Toda tarjeta que muestre **nombre propio, ubicación, precio, superficie, nº de llaves, estado operativo o licencia** es ESPECÍFICA.

| Situación | Qué se hace |
|---|---|
| Existe fotografía real del activo | Se usa. Primera foto = exterior o acceso, nunca un detalle. |
| Sólo existe render | Se usa **rotulado** (`RENDER — PROYECTO NO CONSTRUIDO · {estudio} · {año}`), y el rótulo va en `<figcaption>`, no quemado. |
| No existe nada | **Tarjeta teaser**: fondo negro, filete dorado, nombre en Playfair, chip de estado, leyenda `Material fotográfico bajo verificación`. **Sin blur, sin silueta, sin degradado que simule una foto.** |
| El activo es confidencial | Teaser permanente + ruta al Deal Room. Nunca fotografía. |

Reglas duras derivadas de la auditoría:

- **Un archivo = un activo.** Prohibido que dos fichas con precios distintos compartan imagen (C-04: `07_villa_dubai` sirve a "Serene Palm Villa $4,8 M" y a "Palm Crescent Estate $28 M").
- **Se elimina el hover-flip** (`cs_card_img_back`). Una tarjeta jamás revela la imagen de otro inmueble (C-03: una casa de Tulum aparecía al pasar el ratón sobre un ático del Támesis, en 10 fichas × 3 listados × 4 idiomas).
- **Un activo con dos identidades = dos reportajes distintos** (Villa Lariana / Villa Cadenabbia; Casa Selva / Casa Aluxes; Thames Penthouse / Belgravia House).
- La imagen de tarjeta lleva `object-position` **declarado por activo** en `data/opportunities.*`, no un `50% 50%` global. La auditoría midió `cropLoss = 0,44` en tarjetas 4:3.
- Resolución mínima de tarjeta: **1800×1200**. Las actuales de 900×506 se escalan ×2,11 en cabecera a ancho completo.

### 1.3 Separación visual entre catálogos

Los seis universos deben distinguirse **antes de leer una palabra**. La distinción se hace con **encuadre, luz y ritmo de retícula**, nunca con presets de color distintos (prohibido por Fase 12, §8).

| Universo | Encuadre dominante | Luz | Retícula | Acento de interfaz |
|---|---|---|---|---|
| **Residencial** | Escala humana; teleobjetivo corto; verticales rectificadas | Natural lateral, hora dorada baja | 3 columnas, tarjeta 4:3 | Filete marfil |
| **Hospitality** | Media distancia con actividad; profundidad de campo media | Mixta corregida, interiores cálidos neutros | 3 columnas, tarjeta 3:2 | Filete piedra |
| **Comercial (renta)** | Frontal, arquitectura de uso, sin gente | Diurna plana, sin dramatismo | 2 columnas, tarjeta 16:9 | Filete gris acero |
| **Suelo** | Aéreo o gran plano general; horizonte alto | Rasante, mañana o tarde | 2 columnas, tarjeta 21:9 | Filete verde piedra desaturado |
| **Proyectos** | Obra, maqueta, plano; materia | Contraluz de obra, polvo, andamio | 2 columnas, tarjeta 3:2 + banda de fase | Filete dorado (única sección con dorado en tarjeta) |
| **Private market** | **Sin fotografía** | — | 1 columna, bloque tipográfico | Filete negro sobre negro |

---

## 2. FICHAS DE DETALLE

Alcance: `real-estate/private-properties/pp-*`, `real-estate/commercial-hospitality/ch-*`, `opportunities/lp-*|pa-*|cf-*`, `property-details.html`.

### 2.1 Hero de ficha — auténtico, sin excepciones

Una ficha es la afirmación más concreta del sitio: nombre, ubicación, superficie, estado, a menudo precio. **Su cabecera no admite stock ni en modo "ambiental".** Si no hay fotografía del activo, la ficha se publica **sin hero fotográfico** (cabecera tipográfica sobre negro con el chip de estado) o **no se publica**.

Requisitos del hero: ≥ 3000 px de lado largo · **una toma 16:9 y una 4:5 del mismo activo captadas en rodaje** · autor, fecha y ubicación en la ficha de procedencia · *property release* firmado.

### 2.2 Galería — orden fijo y umbrales de confidencialidad

Orden canónico de la galería (se omiten los tramos que la confidencialidad impida, **nunca se rellenan**):

| # | Tramo | Contenido | Mínimo | Umbral de confidencialidad |
|---|---|---|---|---|
| 1 | **Exterior** | Acceso, fachada principal, volumen, entorno inmediato | 2 fotos | Público salvo off-market extremo |
| 2 | **Interiores** | Estancias principales en su estado real, sin *staging* | 4 fotos | Público |
| 3 | **Contexto** | Calle, pueblo, acceso rodado, relación con el entorno | 1 foto | Se retira si revela la localización exacta de un activo off-market |
| 4 | **Vistas** | Lo que se ve desde el activo | 1 foto | Se retira si la vista identifica la parcela |
| 5 | **Detalles** | Material, carpintería, herraje, suelo, cantería | 2 fotos | Siempre publicable |
| 6 | **Dron** | Implantación, parcela, relación con la costa/ciudad | 1 foto | **Se retira en off-market**: un vuelo identifica coordenadas |
| 7 | **Plano** | Planta esquemática, superficies | 1 pieza | En off-market: **plano sin cotas ni orientación** |
| 8 | **Vídeo** | Recorrido continuo, sin música, sin locución comercial | 0-1 | Nunca embebido de un canal de terceros (C-13) |
| 9 | **Mapa** | Ubicación | 1 pieza | Público: dirección · Off-market: **sólo región**, sin marcador de punto |

### 2.3 Prohibición central

> **Está PROHIBIDO completar una galería incompleta con stock.**

Una galería de 4 fotos reales es honesta. Una galería de 12 con 8 de banco de imágenes es fraude documental. Si faltan tramos:

- Se publica lo que hay, en el orden canónico.
- Se declara la carencia con una nota sobria: `Reportaje fotográfico en curso — material adicional disponible bajo solicitud.`
- **Ni una sola imagen de "ambiente", "estilo de vida", "zona" o "inspiración"** rellenando huecos.
- Prohibido repetir la misma foto en dos posiciones de la galería para inflar el contador.
- Prohibido usar en la galería una foto que ya ilustre otra ficha, aunque sea del mismo edificio.

### 2.4 Casos a retirar, no a re-ilustrar

`property-details.html` y `single-property-v1.html` (los 4 idiomas) son demos de plantilla con inventario, direcciones (Nueva York, Colorado), planos y cifras ficticias, más un skyline de Dubái ilustrando una dirección de Manhattan (C-08) y la insignia ajena "VISIT OUR LUXURY PROPERTY" (C-12). **La acción no es cambiar la foto: es retirar o reconstruir la página sobre un activo real.**

---

## 3. SINGLE-PROPERTY / PROYECTOS

Alcance: `single-property-v1.html` reconvertido, `opportunities/lp-ashima-masterplan/`, `developments/project-structuring/`, `ch-resort-development/`, `ch-hotel-halted/`.

Un proyecto mezcla cuatro naturalezas de imagen que **jamás pueden presentarse juntas sin distinción**. La separación es visual, no sólo textual.

| Naturaleza | Qué es | Tratamiento visual obligatorio | Rótulo |
|---|---|---|---|
| **Fotografía del sitio** | El terreno, el edificio o la obra **como está hoy** | A color natural, sin filtro, marco limpio | `FOTOGRAFÍA DEL EMPLAZAMIENTO · {fecha}` |
| **Renders oficiales** | Imagen del estudio de arquitectura de algo **no construido** | Banda inferior sólida de ≥ 28 px, opacidad 100 %, presente en todos los breakpoints | **`RENDER — PROYECTO NO CONSTRUIDO · {estudio} · {año}`** |
| **Planos** | Plantas, secciones, alzados | Fondo marfil, trazo negro, escala gráfica visible | `PLANO · {fase} · {fecha}` |
| **Masterplan** | Zonificación y fases del territorio | Documento vectorial, leyenda obligatoria, norte marcado | `MASTERPLAN · {versión} · {fecha}` |
| **Progreso de obra** | Avance real, fechado | Foto fechada, mismo punto de vista entre capturas | `OBRA · {fecha}` — serie cronológica, nunca una foto suelta |

Reglas:

1. **Los cuatro grupos van en pestañas o secciones separadas**, con encabezado propio. Nunca en un carrusel único donde una foto real y un render se suceden sin corte.
2. El rótulo del render va en **HTML (`<figcaption>` + `aria-describedby`)**, no quemado en el píxel, para que se traduzca a EN/ES/AR/ZH y lo lea un lector de pantalla.
3. El render **nunca** ocupa el hero de la ficha si existe fotografía del emplazamiento. La realidad va primero.
4. Licencia de uso del render cedida por el estudio autor, registrada en la hoja de control.
5. **Progreso de obra**: mínimo 3 capturas desde el mismo punto en fechas distintas, o no se publica la sección. Una foto suelta de andamio no es progreso, es decorado.
6. Se retira el embed de YouTube de terceros presentado como "Virtual Property Tour" (C-13). Un tour es material propio o no existe.

---

## 4. COMPANY / ABOUT

Alcance: `company/index.html` (9 secciones sin ningún medio), `about-us.html`.

### 4.1 Material propio: lo que debe entrar

| Sección | Material | Prioridad |
|---|---|---|
| `who-we-are` | Fachada o interior de la oficina principal | P1 |
| `operating-model` | Equipo trabajando, revisión de documentación, pizarra de proceso | P1 |
| `offices` | 1 fotografía por sede declarada: exterior + recepción | P1 |
| `team` | Retratos reales (§5) | P1 |
| `entities` | Diagrama vectorial de estructura societaria (NEXARU GLOBAL) — pieza gráfica, no foto | P2 |
| `governance` | Documentación corporativa con datos ilegibles, o composición tipográfica | P2 |
| `network` | Mapa vectorial monocromo de mercados activos | P2 |
| `values` | Tipográfico. Sin fotografía. | P3 |
| `contact` | Ver §6 | P1 |

### 4.2 Si el material propio no existe

> **NO se usa una oficina de stock fingiendo que es XARU.** Es exactamente el mismo delito documental que un retrato de stock con nombre y correo corporativo.

Dos alternativas admitidas, ambas marcadas `REAL_MEDIA_REQUIRED` en el CSV hasta su sustitución:

**A · Arquitectura urbana editorial.** Fotografía de la **ciudad** donde XARU declara sede — trama urbana, distrito financiero, calle, luz de mañana — **sin interior, sin puerta, sin recepción y sin nada que insinúe "esta es nuestra oficina"**. El alt lo dice explícitamente: *"Vista del distrito de {ciudad}, donde XARU HOME tiene presencia"*, nunca *"nuestra oficina"*.

**B · Composición gráfica.** Bloque tipográfico sobre marfil o negro: cifras sobrias (jurisdicciones, mercados activos, años), diagrama de entidades, mapa vectorial. Cero fotografía.

Regla de alt en el caso A: si el alt no puede escribirse sin mentir, la imagen no sirve. Es la prueba más rápida de este documento.

### 4.3 Bloques a retirar

- **Testimonios** (`avatar-1/2/3.jpg`): tres rostros de stock con nombre y el mismo texto repetido literalmente en los tres. **Se retira el bloque completo** hasta disponer de clientes reales con autorización escrita.
- **"20.000 clientes satisfechos"** y cifras de reputación de la plantilla: fuera.
- `04_resort_dev.jpg` ilustrando *"más de 20 años… estructura NEXARU"*: la foto que dice quiénes somos es la misma que vende un resort concreto. Fuera.

---

## 5. AGENTS-LIST

Alcance: `agents-list.html`, sección de equipo de `about-us.html`, avatar de perfil.

### 5.1 Regla absoluta

> **Sólo retratos reales.** Una persona con nombre, cargo, teléfono y correo `@xaruhome.com` ilustrada con un modelo de banco de imágenes es suplantación. Hoy son 6 agentes + 3 testimonios + 1 autor de blog = **11 identidades falsas**, y `team-img-5.jpg` es simultáneamente "Daria Pimkina, agente" y la usuaria "Amanda Jones" del panel de perfil.

**Si no hay retrato real, NO se usa una persona de stock.** Alternativas, por orden:

1. Ficha sin imagen: iniciales en monograma tipográfico sobre marfil, con la regla dorada de marca.
2. Silueta vectorial neutra de marca (misma para todos, evidentemente gráfica).
3. Retirar la persona del directorio hasta la sesión de fotos.

Ninguna de las tres permite un rostro humano fotográfico que no sea el de la persona nombrada.

### 5.2 Dirección fotográfica común de los retratos

Una sola sesión, un solo criterio. Si un retrato se hizo antes con otro criterio, se repite: la inconsistencia de retratos es la señal más visible de un equipo inventado.

| Parámetro | Especificación |
|---|---|
| **Fondo** | Neutro y liso: marfil `#F4F1EA`, gris piedra `#D8D4CC` o negro `#0B0D0F`. Uno solo para todo el equipo. **Sin fondos generados, sin desenfoque artificial de retrato, sin oficina de fondo.** |
| **Luz** | Natural de ventana con rebote, o estudio de una sola fuente suave a 45° + rebote de relleno. Ratio 3:1. Sin luz de recorte azul, sin claves duras. |
| **Encuadre** | Plano medio corto, ojos en el tercio superior, mismo tamaño de cabeza en todos (±5 %), misma altura de cámara (a la altura de los ojos), mismo objetivo (85 mm equivalente). |
| **Orientación** | Vertical 4:5 nativo + recorte cuadrado 1:1 derivado del mismo original. |
| **Resolución** | ≥ 2000×2500 px. Se sirve a 2× (las actuales son 504×585). |
| **Pose y vestuario** | De pie o sentado, frontal o 3/4, sin brazos cruzados, sin apoyar la barbilla. Vestuario sobrio en la paleta corporativa. Sin objetos en la mano. |
| **Retoque** | Limpieza de imperfecciones temporales únicamente. **Prohibido**: suavizado de piel, adelgazamiento, cambio de forma de ojos/mandíbula, blanqueo de dientes, ojos "realzados", eliminación de arrugas y canas. Una piel de plástico es la firma visual de la IA. |
| **Derechos** | **Cesión de imagen firmada** por cada persona, con alcance (web, 4 idiomas, redes, duración) y fecha. Sin cesión no se publica. |
| **Metadatos** | Nombre real, cargo real, fecha, autor. El correo y el teléfono publicados deben existir. |

---

## 6. CONTACT

Alcance: `contact.html`, sección de contacto de `company/`.

| Elemento | Requisito |
|---|---|
| **Imagen principal** | **Fachada real de la sede** o interior de recepción real. ESPECÍFICO. Hoy se usa `city-dubai.jpg` (456×550, escalado ×2,11) como imagen de sede, y el mismo archivo ilustra una dirección de Nueva York en `property-details` (C-08). |
| **Skyline de la sede** | Permitido como imagen secundaria **sólo si la ciudad es realmente sede declarada** y el alt lo dice: *"Distrito de {ciudad}, sede de XARU HOME"*. Un skyline de una ciudad donde XARU no está es falso, aunque sea bonito. |
| **Mapa** | Mapa real de la dirección publicada, con marcador en la dirección correcta. Estilo monocromo de marca. **Prohibido** un mapa de una ciudad distinta a la dirección del bloque. |
| **Ubicación** | Si hay varias sedes, una fila por sede: fachada + dirección + mapa. Nunca una sola foto genérica para todas. |
| **Fondo de formulario** | Sin fotografía. Fondo plano marfil o negro: un formulario sobre foto reduce el contraste y no aporta nada. Se retira `contact-bg.jpg` (pierde el 83 % del encuadre en móvil). |

**Si no hay fotografía de la sede:** bloque tipográfico con dirección, horario y mapa. Sin foto. Nunca un edificio de oficinas de stock.

---

## 7. BLOG / INSIGHTS

Alcance: `blog.html`, `blog-details.html`, `insights/index.html` y los 4 artículos.

### 7.1 Reglas

1. **Stock editorial permitido.** Insights es análisis sectorial: la ilustración de categoría es legítima y esperable.
2. **Cada imagen debe coincidir con el tema EXACTO del artículo.** No con su sector, no con su "ambiente": con su tesis.
3. **Prohibido repetir portada entre artículos.** Hoy `post-img-2.jpg` y `post-img-3.jpg` ilustran cada una **dos artículos distintos** dentro de la misma página de blog.
4. **Una portada de Insights nunca puede ser la foto de un activo del catálogo de XARU.** Hoy los 4 artículos heredan la imagen de la ficha del activo del que hablan: el análisis se lee como publicidad. Correspondencia 2, riesgo alto.
5. **Autoría.** Se retira el autor ficticio "Ahon Bentham" con retrato de stock (C-07). Firma: persona real con retrato real y cesión, o firma institucional **"XARU HOME Research"** sin retrato.
6. Formato: portada 3:2, ≥ 2400×1600; miniatura derivada del mismo original; **variante 4:5** para móvil y para compartir.
7. `og:image` **propia por artículo**. Hoy 12 páginas de temáticas distintas comparten `og-cover.jpg` construida sobre una imagen IA (C-15).

### 7.2 Mapeo tema → imagen de los 4 artículos existentes

| Artículo | Tesis del texto | Imagen: qué debe mostrar | Qué NO puede mostrar | Ref. |
|---|---|---|---|---|
| **`insights/operational-hospitality`**<br>*"Operational hospitality: the asset that earns before it sells"* — el hotel operativo se valora por su P&L, no por su postal | **La operación, no el producto.** Cocina de servicio en plena mañana, pasillo de office con carros de lencería, cambio de turno en recepción, tablero de ocupación, escalera de servicio. Personas a media distancia, sin rostro protagonista. | Piscina infinita, atardecer, huéspedes en bata, cóctel, suite vacía perfecta, **cualquier hotel del catálogo de XARU** (hoy usa `05_hotel_project.jpg`). | **I-11a** |
| **`insights/territorial-land`**<br>*"Territorial land: when scale is the thesis"* — a cierta escala la pregunta deja de ser qué se construye y pasa a ser qué se funda | **Escala y tiempo geográfico.** Aérea alta de un territorio extenso con cambio de uso visible (monte → cultivo → camino), o plano general desde tierra con horizonte muy lejano y una única referencia de escala (un vehículo, un poste). | Duna sin escala, playa dorada, masterplan dibujado, linderos, cifras sobreimpresas, **el terreno de 11M m² de XARU** (hoy usa `03_land_mega.jpg`). | **I-11b** |
| **`insights/capital-halted-projects`**<br>*"Private capital and halted projects: the opportunity in restructuring"* — un proyecto parado rara vez es mal proyecto, suele ser estructura rota | **La detención, literal.** Estructura de hormigón inacabada con vegetación creciendo, grúa inmóvil, andamio sin operarios, cerramiento provisional, vallado con óxido. Luz plana, gris, sin dramatismo. | Gráficos financieros, dinero, apretones de manos, edificios terminados y brillantes, **el hotel parado de XARU** (hoy usa `05_hotel_project.jpg` — un hotel de acantilado terminado, que contradice la palabra "halted"). | **I-11c** |
| **`insights/international-establishment`**<br>*"Establishing internationally: from the entity to residency"* — funciona cuando entidad, familia y operación se estructuran como una sola cosa | **El trámite, no el destino.** Ventanilla o sala de espera institucional, sello sobre expediente, mostrador de registro, tránsito de aeropuerto de madrugada con poca gente. Sobrio, administrativo. | Familia sonriente con maletas, pasaporte con datos legibles, banderas, skyline de Dubái como "sitio bonito", **el ático de Londres de XARU** (hoy usa `08_penthouse_london.jpg`). | **I-11d** |

**Alt text de las cuatro portadas:**

| Ref. | EN | ES | AR | ZH |
|---|---|---|---|---|
| I-11a | `Hotel service kitchen during a working shift.` | `Cocina de servicio de un hotel durante un turno de trabajo.` | `مطبخ خدمة في فندق أثناء وردية عمل.` | `酒店后厨在工作班次中的场景。` |
| I-11b | `High aerial view of extensive terrain with a change of land use.` | `Vista aérea alta de un terreno extenso con un cambio de uso del suelo.` | `منظر جوي مرتفع لأرض شاسعة يظهر فيها تغيّر في استخدام الأرض.` | `广阔地块的高空航拍，可见土地用途的变化。` |
| I-11c | `Unfinished concrete structure with a stationary crane and no workers.` | `Estructura de hormigón sin terminar con una grúa detenida y sin operarios.` | `هيكل خرساني غير مكتمل مع رافعة متوقفة وبدون عمال.` | `未完工的混凝土结构，塔吊静止，现场无工人。` |
| I-11d | `Waiting area of an administrative office with a service counter.` | `Sala de espera de una oficina administrativa con un mostrador de atención.` | `صالة انتظار في مكتب إداري مع منضدة خدمة.` | `行政办事处的等候区与服务柜台。` |

### 7.3 Artículos futuros

El derrotero prevé Insights por sector: *Luxury residential · Hospitality · Land · Capital · Development · Commodities · International establishment.* **Una imagen nueva por artículo**, registrada en la hoja de licencias, con su propia `og:image`. Ninguna reutilización entre artículos, ni siquiera del mismo sector.

---

## 8. FAQ

| Regla | Detalle |
|---|---|
| **Máximo 1 imagen editorial** en toda la página, y sólo si aporta. Por defecto: **ninguna**. |
| **Página principalmente tipográfica.** Jerarquía por tamaño, peso e interlineado. Acordeones con regla de 1 px y acento dorado en el ítem abierto. |
| **Se retira `illustartion.svg`** (310 KB): ilustración vectorial de la plantilla, ajena a la marca y cara. |
| Si se usa la única imagen permitida, es de **categoría neutra** (escritorio, documento, sala) y va al final, como cierre, no en cabecera. |
| Las FAQ por división (derrotero §6, punto 11) heredan el mismo criterio: cero imágenes por división. |

---

## 9. FASE 12 — COLOR Y DIRECCIÓN FOTOGRÁFICA

Aplica a **todo** el material del sitio: stock, propio, renders y vídeo.

### 9.1 Paleta admitida

| Familia | Uso | Referencia |
|---|---|---|
| **Negro** | Fondos, overlays, secciones de confidencialidad | `#0B0D0F` |
| **Marfil** | Fondos claros, fondo de retrato, papel | `#F4F1EA` |
| **Piedra** | Grises cálidos naturales, hormigón, cantería | `#D8D4CC` → `#6E6A63` |
| **Madera** | Tonos cálidos medios naturales, carpintería, mobiliario | tal como aparezca en la escena |
| **Vegetación real** | Verdes tal como los da la luz del lugar, saturación ≤ +0 % | — |
| **Dorado** | **Sólo como acento de interfaz**: filete, subrayado, icono activo, borde de estado. **Nunca como filtro sobre fotografía.** | `#C8A860` |

### 9.2 Dirección fotográfica

- **Tonos naturales.** El balance de blancos se corrige a neutro; a partir de ahí, la escena manda.
- **Contraste cinematográfico moderado.** Curva S suave. Negros con detalle (nivel 6-10, no 0). Altas luces sin recorte.
- **Saturación global entre −20 % y 0 %.** Nunca positiva.
- **Grano fino admitido** (≤ 3 %) para evitar banding en degradados oscuros. Nunca como efecto "analógico".
- **Un solo criterio para todo el sitio.** La diferencia entre secciones se hace con encuadre, luz y retícula (§1.3), no con color.
- **Verticales rectificadas** en toda arquitectura. Una fachada convergente es amateur.

### 9.3 Lista de prohibiciones (Fase 12)

| Prohibido | Por qué |
|---|---|
| **Teal & orange extremo** | Firma de trailer comercial. Destruye la piedra, la madera y la piel. |
| **Filtro dorado global** | Convierte el acento de marca en un baño de color; hace parecer publicidad de fondo de inversión. |
| **Sepia** | Falsifica antigüedad. |
| **HDR / tone mapping agresivo** | Halos, cielos morados, texturas de cómic. Firma inmediata de imagen manipulada. |
| **Cielos reemplazados** | Es una falsificación documental, no una corrección. |
| **Saturación tropical artificial** | Turquesas y verdes imposibles. Es lo que hoy delata las imágenes IA del sitio. |
| **Presets distintos por sección** | Rompe la unidad; hace que el sitio parezca ensamblado con material de orígenes distintos, que es precisamente el problema que se está corrigiendo. |
| Viñeteado marcado, blur selectivo artificial, glow, destellos añadidos | Ruido de plantilla. |

### 9.4 Control de calidad de color

Antes de publicar cualquier tanda: montar las imágenes candidatas en una única tira de contacto y verificar que **pertenecen al mismo mundo**. Si una salta, se corrige o se descarta. Es la prueba que hoy fallaría el sitio entero.

---

## 10. FASE 13 — ACCESIBILIDAD

### 10.1 Texto alternativo

| Regla | Correcto | Incorrecto |
|---|---|---|
| **El alt describe lo que la imagen realmente muestra**, no lo que la página quiere vender | `Cocina de servicio de un hotel durante un turno de trabajo.` | `Hotel de lujo de alta rentabilidad` |
| **Prohibido "imagen de lujo"** y todo adjetivo comercial | `Exterior de una residencia contemporánea con luz lateral.` | `Impresionante propiedad de lujo exclusiva` |
| **Prohibido el keyword stuffing** | `Terreno extenso sin urbanizar con un camino de tierra.` | `terreno venta inversión real estate caribe oportunidad suelo` |
| **Prohibido el alt que contradice la imagen** | — | `alt="ASHIMA — vista aérea del territorio, Oaxaca"` sobre una selva genérica (C-02) |
| **Prohibido el alt que nombra a quien no aparece** | — | `alt="Alex Carter"` sobre un modelo de stock (C-05) |
| Longitud | ≤ 125 caracteres. Si hace falta más, va en `<figcaption>` o `aria-describedby`. | Párrafos en el `alt`. |
| Idioma | El `alt` se traduce a EN/ES/AR/ZH por el generador. **Nunca queda en inglés en `/es/`, `/ar/` o `/zh/`.** | — |
| Renders | El `alt` **debe** empezar por `Render:` / `Render:` / `صورة تخيلية:` / `效果图：` | Un render descrito como fotografía. |

### 10.2 Imágenes decorativas

- Toda imagen puramente decorativa (fondos de sección, texturas, pictogramas junto a texto que ya lo dice, filetes) lleva **`alt=""`** y `aria-hidden="true"` si es `<img>`.
- Un `alt=""` es una decisión declarada, no un olvido. Un `<img>` **sin atributo `alt`** es un error: el lector de pantalla lee el nombre del archivo.
- Los fondos `data-background` de la plantilla no generan `<img>`: no necesitan alt, pero **sí** necesitan que el texto encima cumpla contraste sobre el punto más claro del fondo.

### 10.3 Vídeo

| Requisito | Especificación |
|---|---|
| **Texto alternativo del vídeo informativo** | `aria-label` breve + descripción textual visible o en `aria-describedby` que cuente lo que se ve. Un vídeo sin equivalente textual es contenido perdido para quien no puede verlo. |
| **Poster significativo** | Fotograma real del propio vídeo, no una imagen distinta. Obligatorio: hoy `xr_ambient.mp4` no declara `poster` y el bloque queda negro en conexión lenta (C-17, `MISSING_POSTER`). |
| **Controles** | Visibles y operables por teclado: play/pausa, silencio, barra de progreso. Foco visible. |
| **Autoplay** | Sólo si es `muted`, sin audio y **pausable**; respeta `prefers-reduced-motion: reduce` → se sirve el poster estático. |
| **Sin audio comercial** | Sin música ni locución. Si algún vídeo llevara voz, subtítulos en los 4 idiomas. |
| **Sin texto quemado** | Todo rótulo va en HTML sobre el vídeo, por i18n y por accesibilidad. |
| **Vídeo decorativo** | `aria-hidden="true"` + sin controles + sin sonido, y **no puede portar información** que no esté en el texto. |

### 10.4 Verificación

Contraste ≥ 4,5:1 (texto normal) y ≥ 3:1 (texto grande y elementos de interfaz), medido **sobre el punto más claro del área ocupada por el texto** y sobre el fotograma real del vídeo, no sobre una media. Si el overlay no lo garantiza en algún breakpoint, el fondo pasa a color plano.

---

## 11. CRITERIOS DE ACEPTACIÓN DE LA FASE 4

1. Ninguna tarjeta, ficha, retrato o mapa con dato concreto está ilustrado con stock.
2. Ninguna galería se ha completado con material que no sea del activo.
3. Todo render lleva rótulo en `<figcaption>`, traducido, visible en los 4 breakpoints.
4. Ningún archivo aparece en dos contextos semánticos distintos.
5. Los seis universos de catálogo se distinguen por encuadre, luz y retícula — **no** por color.
6. Los 4 artículos de Insights tienen portada propia, distinta entre sí y distinta de cualquier activo del catálogo.
7. Todos los `alt` describen lo que se ve, en el idioma de la página, sin adjetivos comerciales.
8. Todo `<video>` tiene poster, controles accesibles y equivalente textual.
9. Company, Contact y agents-list no contienen ni una sola persona, oficina o sede que no sea de XARU.
