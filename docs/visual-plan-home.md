# PLAN VISUAL DE LA PORTADA — XARU HOME
**Fase 3 · Dirección de arte documental** · Rama `agent/real-stock-media-audit` · 31-jul-2026
Insumos: [`visual-audit.md`](visual-audit.md) · [`media-replacement-plan.csv`](media-replacement-plan.csv) · `DERROTERO_MAESTRO_V2.md` §4 (portada de 12 bloques)

> **Este documento no modifica ningún archivo del sitio. Es plan.**

---

## 0. REGLA RECTORA

> El stock real puede representar una **CATEGORÍA** o una **CAPACIDAD**.
> **Nunca** puede representar un **ACTIVO CONCRETO** — con nombre, precio, ubicación, superficie, nº de llaves, licencia, ASHIMA o isla identificable.
> Lo concreto exige **material auténtico** o **bloqueo/teaser confidencial**. Ninguna imagen generada por IA, en ningún bloque.

Estados posibles de cada bloque en este plan:

| Estado | Significado |
|---|---|
| `CATEGORÍA` | Stock documental real admitido, con licencia registrada. |
| `ESPECÍFICO` | Material propio obligatorio. Sin él → bloqueo. |
| `BLOQUEO` | El bloque se publica **sin imagen** (composición tipográfica / velo / teaser) hasta que llegue el material real. |
| `MARCA` | Composición gráfica de marca, sin fotografía. |

---

## 1. PRESUPUESTO VISUAL DE LA PORTADA

Objetivo declarado: **1 vídeo principal + 8-12 imágenes fuertes** en toda la portada. Nada de un vídeo por bloque. Estética editorial, seria, silenciosa.

| Recurso | Cantidad | Dónde |
|---|---:|---|
| Vídeo principal (único de la página) | **1** | Hero, diapositiva 1 |
| Imágenes de categoría (stock documental) | **9** | Mercados ×3, capacidad, doble vía, infraestructura, gobierno, private desk, poster de vídeo |
| Imágenes de material propio (XARU) | **1** | Presencia real (oficina) — hasta que exista, `BLOQUEO` |
| Bloques sin imagen por diseño | **3** | Selector de recorrido, oportunidades destacadas (usa las fichas), insights (usa las portadas de artículo) |
| Bloques bloqueados hasta material real | **3** | Hero slide 2 (Samaná), Hero slide 3 (ASHIMA), ASHIMA |

**Total de medios nuevos en la portada: 1 vídeo + 10 imágenes.** Cualquier propuesta que supere 12 imágenes se rechaza: la portada pierde silencio.

Rendimiento obligatorio para todo lo anterior: AVIF + WebP + JPEG de respaldo, `srcset` con 3 anchos (1920 / 1280 / 828), `loading="lazy"` salvo el hero, y **variante vertical 4:5 propia** para cada imagen a ancho completo (la auditoría §5.2 midió hasta un 74 % de pérdida de encuadre en móvil con recorte automático).

---

## 2. EL HERO — QUÉ NO DEBE MOSTRAR

Prohibiciones explícitas para las tres diapositivas. Cualquier candidata que incumpla una sola se descarta sin discusión:

1. **Un inmueble reconocible y confundible con una oferta.** Si el visitante puede pensar "esa casa está en venta", la imagen está mal. El hero muestra **territorio, escala, luz y estructura**, no producto.
2. **Interiores artificiales** — salones de catálogo, cocinas de showroom, staging de plantilla, renders de interior. Ni un solo interior en el hero.
3. **Lujo ostentoso** — yates, coches deportivos, champán, mármol dorado, joyería, modelos posando en bañador, "lifestyle" de agencia. XARU es rigor corporativo, no revista de estilo de vida.
4. **Texto incrustado en el archivo** — títulos, claims, precios, marcas de agua o "Price upon application" quemados en el píxel. Todo el texto es HTML (por i18n EN/ES/AR/ZH y por accesibilidad).
5. **Logos de terceros** — marcas de hotel, promotor, estudio de arquitectura, aerolínea, coche; y por supuesto la insignia de plantilla `text-logo.svg` ("VISIT OUR LUXURY PROPERTY", C-12 de la auditoría).
6. **Cielos reemplazados, HDR, saturación tropical** y cualquier huella de IA generativa. Ver criterios de rechazo en `media-search-queries.md` §9.
7. **Personas identificables en primer plano.** Si aparece una figura, es a contraluz, de espaldas o a escala mínima; nunca un rostro reconocible sin cesión.

### 2.1 Reglas de las diapositivas del hero

| Regla | Detalle |
|---|---|
| **Máximo 1 diapositiva con vídeo** | Sólo la diapositiva 1. Las demás son imagen fija. Un carrusel de tres vídeos es ruido y coste. |
| **Samaná / ASHIMA → material real o bloqueo** | Cualquier diapositiva cuyo texto nombre **Samaná** o **ASHIMA** (hoy las dos y la tres) requiere fotografía/dron auténtica del territorio, fechada y georreferenciada, o **render oficial rotulado**. Sin ese material, la diapositiva **no se publica**: el carrusel se reduce a las diapositivas disponibles. |
| **Sin transición espectáculo** | Fundido a negro de 900 ms, sin zoom Ken Burns agresivo, sin paralaje sobre el hero. Autoplay pausable, 7 s por diapositiva. |
| **Contraste garantizado** | Overlay obligatorio (véase §4) para que el titular alcance 4,5:1 sobre cualquier fotograma del vídeo, no sólo sobre el poster. |
| **Estado actual (jul-2026)** | Diapositivas 2 y 3 **BLOQUEADAS**. El hero se publica con **una sola diapositiva** hasta que llegue material real. Un hero de una diapositiva es preferible a tres mentiras. |

---

## 3. PLAN BLOQUE A BLOQUE

Referencia de sección en `index.html` entre paréntesis. Los `id` corresponden al DOM actual.

---

### H-01 · Hero inmobiliario (`.cs_hero`, 3 diapositivas)

| Campo | Definición |
|---|---|
| **Qué debe mostrar** | Escala y luz, no producto. Territorio costero o urbano a hora azul/dorada baja, leído desde altura o desde una distancia que impida identificar un inmueble. Movimiento mínimo: agua, nube, sombra. Sensación: *"esto se administra, no se vende"*. |
| **Clasificación** | **CATEGORÍA** (diapositiva 1) · **ESPECÍFICO → BLOQUEO** (diapositivas 2 y 3) |
| **Recurso propuesto** | **V-01** — vídeo documental 16:9, 12-18 s, bucle silencioso, sin música, sin locución, sin corte. Plano aéreo lento (dron a velocidad constante) sobre línea de costa **no identificable** o sobre trama urbana a media distancia. ≤ 4,5 MB en AVIF/H.265, ≤ 2,2 MB en la variante móvil. **I-01** — poster: fotograma real del propio vídeo, 1920×1080, exportado sin retoque diferencial. |
| **Tratamiento** | Overlay duotono negro→azul-noche (`#0B0D0F` → `#12181D`) al 42 % con degradado vertical más denso abajo (60 % en el tercio inferior) para el titular. Sin viñeteado circular. Saturación −12 %, contraste cinematográfico moderado (curva S suave, negros no aplastados). |
| **Foco** | Punto focal en el tercio superior derecho (horizonte); el bloque de texto ocupa el tercio izquierdo. |
| **Recorte móvil** | **Variante vertical propia 9:16 y 4:5** del mismo material, no recorte automático. `object-position: 68% 40%` en la variante vertical. En < 480 px el vídeo se sustituye por el poster estático (`I-01`, versión 4:5) para no gastar datos. |
| **Estado diapositiva 2** (*"A Private Island in Samaná Bay"*) | **BLOQUEADA.** Requiere fotografía o vuelo de dron real de la bahía de Samaná, fechado y georreferenciado, con *property/location release*. Sustituye a `gen2/02_island_rd.jpg`. Hasta entonces la diapositiva se retira del carrusel. |
| **Estado diapositiva 3** (*"Master Developments, From Land to Legacy — ASHIMA, Oaxaca"*) | **BLOQUEADA.** Requiere aérea real del territorio en Oaxaca o **render oficial del masterplan con rótulo permanente "RENDER — PROYECTO NO CONSTRUIDO"** y crédito del estudio. Sustituye a `gen2/06_masterplan_ashima.jpg`. |

**Alt text (diapositiva 1 · el vídeo lleva además `aria-label` y descripción textual, ver `visual-plan-inner-pages.md` §9):**

| Idioma | Texto |
|---|---|
| EN | `Aerial view of a coastline at low light, seen from height; no buildings identifiable.` |
| ES | `Vista aérea de una línea de costa con luz baja, tomada desde altura; ningún edificio identificable.` |
| AR | `منظر جوي لخط ساحلي في ضوء منخفض، ملتقط من ارتفاع؛ لا تظهر أي مبانٍ يمكن تحديدها.` |
| ZH | `低光下从高空拍摄的海岸线航拍画面，画面中无可辨识的建筑。` |

---

### H-02 · Selector de recorrido (`#journey` — *"What brings you to XARU?"*)

| Campo | Definición |
|---|---|
| **Qué debe mostrar** | **Nada fotográfico.** Es un cruce de caminos: seis intenciones (busco propiedad / vendo activo / tengo proyecto / busco capital / quiero invertir / me establezco). Cualquier foto aquí sesga la elección hacia una vía. |
| **Clasificación** | **MARCA** |
| **Recurso propuesto** | Sin imagen. Fondo marfil `#F4F1EA` o negro, retícula de 6 tarjetas con **pictograma lineal monocromo** (1 px, esquinas vivas, sin relleno) y regla dorada de 2 px como acento de estado activo. Este bloque cierra 1 de las 9 secciones vacías detectadas en `index.html` (§5.4 de la auditoría) **sin añadir stock decorativo**. |
| **Tratamiento** | Sin overlay. Tipografía Playfair para el enunciado, Poppins para las opciones. Separadores de 1 px `rgba(0,0,0,.12)`. |
| **Recorte móvil** | 6 tarjetas → 1 columna, alto mínimo 88 px, área táctil ≥ 44 px. |
| **Alt** | Pictogramas decorativos → `alt=""` + `aria-hidden="true"`. El texto de la tarjeta ya es el enlace accesible. |

---

### H-03 · Tres mercados inmobiliarios (`#markets`)

Tres entradas: **Private Real Estate · Commercial & Hospitality · Land & Master Developments**. Son **categorías**, no activos: aquí el stock documental es legítimo y necesario. Es el bloque donde más se juega la credibilidad del sitio, porque hoy lo ilustran `07_villa_dubai`, `05_hotel_project` y `03_land_mega` — los tres archivos IA que además venden activos concretos con precio.

| | H-03a · Private Real Estate | H-03b · Commercial & Hospitality | H-03c · Land & Master Developments |
|---|---|---|---|
| **Qué debe mostrar** | Arquitectura residencial de autor vista **desde fuera y en escorzo**: un volumen, una sombra, una pieza de fachada, un patio. Sin interior, sin piscina, sin lujo declarado. | Un activo que **funciona**: recepción en operación real a media distancia, cocina de servicio, cambio de turno, pasillo de servicio, terraza a primera hora sin huéspedes. La categoría es "renta", no "vacaciones". | Territorio a escala: extensión, relieve, límite entre uso agrícola y monte, camino de tierra, línea de costa larga. **Sin masterplan dibujado, sin coordenadas, sin linderos.** |
| **Clasificación** | CATEGORÍA | CATEGORÍA | CATEGORÍA |
| **Recurso** | **I-02** — 2400×1600 mín., horizontal 3:2, luz natural lateral. | **I-03** — 2400×1600 mín., horizontal 3:2, interior con luz mixta corregida. | **I-04** — 3000×2000 mín., aérea baja o plano general desde tierra. |
| **Tratamiento** | Duotono suave negro/marfil al 18 % en reposo, a color pleno en `:hover`/`:focus`. Contraste moderado, negros al 8 %. | Igual duotono. Balance de blancos neutro; **prohibido el filtro dorado global** (§12). | Igual duotono. Saturación de vegetación −15 % para evitar el verde tropical artificial. |
| **Foco** | Volumen arquitectónico centrado a 1/3 desde la izquierda. | Persona/actividad a escala pequeña, nunca rostro en primer plano. | Horizonte en el tercio superior; el terreno domina. |
| **Recorte móvil** | Variante 4:5. `object-position: 50% 45%`. | Variante 4:5. `object-position: 40% 50%`. | Variante 4:5. `object-position: 50% 60%` (conservar el terreno, no el cielo). |

**Alt text:**

| Bloque | EN | ES | AR | ZH |
|---|---|---|---|---|
| H-03a | `Exterior of a contemporary private residence in side light.` | `Exterior de una residencia privada contemporánea con luz lateral.` | `واجهة خارجية لمسكن خاص معاصر بإضاءة جانبية.` | `侧光下的当代私人住宅外观。` |
| H-03b | `Hotel reception in operation, seen from a distance.` | `Recepción de hotel en funcionamiento, vista a distancia.` | `مكتب استقبال فندقي أثناء التشغيل، من مسافة.` | `远景拍摄的运营中酒店前台。` |
| H-03c | `Wide undeveloped terrain with a dirt track and a distant horizon.` | `Terreno extenso sin urbanizar con un camino de tierra y horizonte lejano.` | `أرض واسعة غير مطوّرة مع طريق ترابي وأفق بعيد.` | `一片未开发的广阔土地，有一条土路和远处的地平线。` |

---

### H-04 · Oportunidades destacadas (`#featured`, pestañas Private / Commercial / Land / Projects / Private Market)

| Campo | Definición |
|---|---|
| **Qué debe mostrar** | Cada tarjeta nombra un activo con ubicación y a menudo precio: *Private Island Samaná Bay · Signature Villa Dubai · Penthouse Central London · Lakefront Estate Como · Beachfront Residence Tulum · Villa Marbella · Operating Boutique Hotel · Halted Hotel Project · Beach Resort · Territorial Land 11M m² · ASHIMA · Confidential Portfolio.* **Todas son ESPECÍFICAS. Ninguna admite stock.** |
| **Clasificación** | **ESPECÍFICO** (11 tarjetas) + **BLOQUEO/TEASER** (1: Confidential Portfolio) |
| **Recurso propuesto** | **Ningún recurso nuevo de stock.** Cada tarjeta usa la primera fotografía real del activo cuando exista. Mientras no exista: **tarjeta en modo teaser** — fondo negro `#0B0D0F`, filete dorado de 1 px, tipografía Playfair con el nombre del activo, chip de estado (*Off-market · En validación · Buscando capital · Mandato exclusivo*) y sello `Material fotográfico bajo verificación`. |
| **Tratamiento** | El teaser **no simula** una imagen borrosa de un inmueble: no hay blur de foto, no hay silueta. Es un bloque tipográfico. Un desenfoque sugiere que hay una foto detrás y eso vuelve a ser una promesa falsa. |
| **Confidential Portfolio — Private Market** | **Nunca** recibe fotografía, ni siquiera cuando llegue material: es teaser confidencial permanente (composición tipográfica/documental) con acceso vía Deal Room. Sustituye a `gen2/13_investment_bg.jpg`. |
| **Regla anti-C-03/C-04** | Se elimina el `cs_card_img_back` (hover-flip): una tarjeta **jamás** revela la imagen de otro activo. Y **un archivo = un activo**: prohibido reutilizar una foto entre dos fichas con precios distintos. |
| **Recorte móvil** | Tarjeta 4:3 en desktop, 1:1 en móvil, con `object-position` declarado **por activo** en el JSON de datos (`data/opportunities.*`), no global. |

**Alt text (patrón obligatorio por tarjeta; se rellena con datos reales del activo, nunca con adjetivos):**

| Idioma | Patrón |
|---|---|
| EN | `{Asset name}, {location}: {what the photograph actually shows}.` |
| ES | `{Nombre del activo}, {ubicación}: {lo que la fotografía muestra realmente}.` |
| AR | `{اسم الأصل}، {الموقع}: {ما تُظهره الصورة فعليًا}.` |
| ZH | `{资产名称}，{地点}：{照片实际呈现的内容}。` |

Alt de la tarjeta teaser (sin foto): `alt=""` — es un bloque tipográfico, no una imagen informativa.

---

### H-05 · Más allá de la intermediación · Acquire → Expand (`#capability`)

Seis pasos: **Acquire · Structure · Finance · Develop · Operate · Expand.**

| Campo | Definición |
|---|---|
| **Qué debe mostrar** | Continuidad y proceso, no seis fotos. **Una sola banda horizontal** que atraviesa el bloque: una mesa de trabajo real con planos, un edificio en fase intermedia de obra con andamio, o una sala de reunión en penumbra. La secuencia de seis pasos se lee en tipografía y en una línea de tiempo de 1 px con nodos dorados. |
| **Clasificación** | **CATEGORÍA** (la banda) · los seis pasos son **MARCA** (pictograma + número) |
| **Recurso** | **I-05** — 3200×1200, panorámica 8:3, plano fijo, luz de tarde. |
| **Tratamiento** | Duotono negro/piedra al 55 %, la banda funciona como fondo detrás de la línea de tiempo. Sin degradado dorado. Sin blur. |
| **Foco** | Composición horizontal legible con el 55 % de opacidad de overlay: sin sujeto central que compita con los números. |
| **Recorte móvil** | La banda **se retira** por debajo de 768 px (`display:none`, no recorte): a esa anchura una panorámica 8:3 no comunica nada. Queda la línea de tiempo vertical sobre fondo plano. |

**Alt:** decorativa en desktop → `alt=""`. Si se decide informativa: EN `Construction site at an intermediate stage, seen frontally.` · ES `Obra en fase intermedia, vista frontal.` · AR `موقع بناء في مرحلة متوسطة، بمنظور أمامي.` · ZH `正面视角下处于中间阶段的施工现场。`

---

### H-06 · Proyectos y capital · doble vía (`#dual` — *"A two-way structure"*)

| Campo | Definición |
|---|---|
| **Qué debe mostrar** | La dualidad **Present a project ↔ Deploy capital** como dos mitades del mismo bloque. Izquierda (proyecto): materia — hormigón, plano desplegado, maqueta, replanteo. Derecha (capital): abstracción — superficie de mesa de reuniones, luz de ventana sobre documento, sala vacía. **Ni gráficos bursátiles, ni monedas, ni apretones de manos, ni "hombre de negocios mirando la ciudad".** |
| **Clasificación** | **CATEGORÍA** |
| **Recurso** | **I-06** — díptico: dos archivos 1600×2000 (4:5 cada mitad) o un único 3200×2000 partido por CSS. |
| **Tratamiento** | La mitad "proyecto" a color natural desaturado −20 %; la mitad "capital" en duotono negro/marfil casi monocromo. El contraste entre ambas mitades **es** el mensaje. Separación por una regla dorada vertical de 2 px. |
| **Foco** | Cada mitad con su sujeto a 1/3 del borde exterior, dejando limpio el centro donde se cruzan los dos CTA. |
| **Recorte móvil** | Se apilan: proyecto arriba, capital abajo, cada una en 4:5 nativo. Nunca se recorta un díptico horizontal a móvil. |

**Alt:** EN `Left: unrolled architectural drawings on a work table. Right: an empty meeting room lit by a window.` · ES `Izquierda: planos de arquitectura desplegados sobre una mesa de trabajo. Derecha: una sala de reuniones vacía iluminada por una ventana.` · AR `يسارًا: مخططات معمارية مبسوطة على طاولة عمل. يمينًا: قاعة اجتماعات فارغة يضيئها ضوء النافذة.` · ZH `左侧：工作台上摊开的建筑图纸。右侧：由窗光照亮的空会议室。`

---

### H-07 · Caso emblemático — ASHIMA (`#projects`)

| Campo | Definición |
|---|---|
| **Qué debe mostrar** | Visión, escala, modelo territorial, gobernanza, fases y ejecución de ASHIMA — **no una foto bonita**. El derrotero es explícito: *"no solo foto"*. |
| **Clasificación** | **ESPECÍFICO — el más sensible del sitio.** |
| **Estado actual** | **BLOQUEO TOTAL.** Se retiran `gen2/06_masterplan_ashima.jpg` (C-02) y `gen2/06b_ashima_pavilion.jpg` (C-01). Este último ilustra el texto *"the first built expression of ASHIMA"* con una obra que **no existe**: es el peor caso de la auditoría (correspondencia 0). |
| **Recurso propuesto (una vez llegue el material)** | En este orden de preferencia: **(1)** aérea real fechada y georreferenciada del territorio en Oaxaca; **(2)** masterplan oficial (zonificación y fases) tratado como **documento**, no como paisaje; **(3)** render oficial del estudio **con rótulo permanente**. |
| **Rotulación obligatoria de renders** | Banda inferior fija, no eliminable por CSS responsivo, alto ≥ 28 px: `RENDER — PROYECTO NO CONSTRUIDO · {Estudio autor} · {año}`. En las 4 lenguas. El rótulo va en HTML (`<figcaption>`), no quemado en el píxel. |
| **Mientras dure el bloqueo** | Bloque tipográfico sobre negro con las 6 fases del proyecto y un diagrama vectorial de zonificación **declarado como diagrama**. Corregir además el texto: retirar *"first built expression"* o acompañarlo del render rotulado. |
| **Tratamiento (cuando haya foto real)** | Sin duotono, sin filtro. El territorio se muestra como es. Máximo: corrección de balance de blancos y +6 % de contraste. |
| **Recorte móvil** | Variante vertical dedicada, capturada en rodaje (no recorte). Si el material sólo existe en 16:9, se presenta en 16:9 **con banda**, nunca recortado al 46 % de su encuadre. |

**Alt (para la aérea real, cuando exista):** EN `ASHIMA: aerial photograph of the project territory in Oaxaca, Mexico, taken on {date}.` · ES `ASHIMA: fotografía aérea del territorio del proyecto en Oaxaca, México, tomada el {fecha}.` · AR `أشيما: صورة جوية لأرض المشروع في واخاكا، المكسيك، التُقطت في {التاريخ}.` · ZH `ASHIMA：{日期}拍摄的墨西哥瓦哈卡州项目用地航拍照片。`
**Alt (para render rotulado):** EN `Official render of the ASHIMA masterplan — unbuilt project, by {studio}.` · ES `Render oficial del masterplan de ASHIMA — proyecto no construido, de {estudio}.` · AR `صورة تخيلية رسمية للمخطط العام لأشيما — مشروع غير مُنفَّذ، من إعداد {الاستوديو}.` · ZH `ASHIMA总体规划官方效果图——未建成项目，由{事务所}制作。`

---

### H-08 · Infraestructura empresarial (`#infra`)

Cuatro tarjetas: **Corporate Services · Compliance & Governance · Financial Infrastructure · Trade & Relocation.**

| Campo | Definición |
|---|---|
| **Qué debe mostrar** | Una sola imagen de fondo para el bloque: **infraestructura física real**, no metáfora digital. Un centro de datos visto desde el pasillo frío, una terminal de carga al amanecer, una sala de operaciones con pantallas apagadas, un archivo documental. **Prohibido**: nubes con candados, redes de puntos azules, código binario, hologramas, manos tocando pantallas flotantes. Hoy este bloque hereda `05_hotel_project.jpg` (un hotel de acantilado ilustrando "comercio, financiación y relocalización"). |
| **Clasificación** | **CATEGORÍA** |
| **Recurso** | **I-07** — 2800×1400, horizontal 2:1. Las 4 tarjetas encima llevan pictograma lineal, no foto. |
| **Tratamiento** | Duotono negro/azul-acero al 70 % (es fondo, no protagonista). Grano fino 2 % para evitar el banding en el degradado. Acento dorado sólo en el filete superior de la tarjeta activa. |
| **Foco** | Perspectiva de fuga centrada; las tarjetas se apoyan sobre el tercio inferior. |
| **Recorte móvil** | Variante 4:5. Si el degradado no garantiza 4,5:1 sobre el texto de tarjeta en móvil, el fondo pasa a negro plano: **la legibilidad gana siempre a la fotografía**. |

**Alt:** EN `Interior corridor of a logistics or data facility, artificial lighting.` · ES `Pasillo interior de una instalación logística o de datos, con iluminación artificial.` · AR `ممر داخلي لمنشأة لوجستية أو مركز بيانات بإضاءة صناعية.` · ZH `物流或数据设施的内部通道，人工照明。`

---

### H-09 · Presencia real (`#presence`)

| Campo | Definición |
|---|---|
| **Qué debe mostrar** | Oficinas, entidades, mercados activos, equipo, capacidades internas y red internacional. Es literalmente el bloque de **"el poder se demuestra, no se dice"** (derrotero §8). Ilustrarlo con stock lo destruye. |
| **Clasificación** | **ESPECÍFICO** |
| **Recurso propuesto** | **R-01** — fotografía real de una oficina de XARU: fachada o interior de trabajo, horizontal 3:2, ≥ 3000 px. Ver `xaru-original-production-shot-list.md` §1 (ítems OF-01, OF-05, OF-08). Junto a ella, cifras sobrias en tipografía: nº de oficinas, jurisdicciones, mercados activos. |
| **Estado actual** | **BLOQUEO.** La auditoría constata **0 fotografías** de oficina, equipo, obra o documento de XARU en todo el sitio (C-14). Hasta que exista R-01: bloque tipográfico con un mapa vectorial monocromo de mercados activos **sin fotografía de oficina de stock**. Un despacho de banco de imágenes fingiendo ser XARU es exactamente lo que esta auditoría existe para impedir. |
| **Tratamiento** | Material propio: sin duotono, sin filtro de marca. Corrección de color neutra, verticales rectificadas. Es documento. |
| **Foco** | Composición frontal o de un punto de fuga; nada de picados dramáticos. |
| **Recorte móvil** | Capturar en rodaje una toma vertical dedicada del mismo espacio. |

**Alt:** EN `XARU HOME office in {city}: {what the photograph shows}.` · ES `Oficina de XARU HOME en {ciudad}: {lo que muestra la fotografía}.` · AR `مكتب XARU HOME في {المدينة}: {ما تُظهره الصورة}.` · ZH `XARU HOME 位于{城市}的办公室：{照片所呈现的内容}。`

---

### H-10 · Gobierno y confianza (`#governance`)

Confidencialidad · due diligence · mandatos · compliance · protección de información · coordinación legal y fiscal · alcance regulatorio.

| Campo | Definición |
|---|---|
| **Qué debe mostrar** | **Materia documental**, en macro y a contraluz: papel con sello en relieve, canto de un expediente, carpeta cerrada, superficie de mesa de junta vacía, luz de persiana sobre un documento del que **no se lee ni una palabra**. Nada de martillos de juez, balanzas, candados, escudos ni columnas clásicas. |
| **Clasificación** | **CATEGORÍA** (materia genérica; ningún documento real de XARU debe ser legible en una imagen pública) |
| **Recurso** | **I-08** — 2400×1600, macro o plano cenital, profundidad de campo corta. |
| **Tratamiento** | Prácticamente monocromo: duotono negro/marfil al 30 %, contraste alto en la textura, saturación −60 %. Acento dorado sólo en la regla del titular. |
| **Foco** | El sujeto en el tercio inferior derecho; el texto de gobernanza ocupa la mitad izquierda. |
| **Recorte móvil** | Variante 1:1. Una macro tolera bien el recorte cuadrado, pero se declara `object-position` explícito sobre el punto de enfoque. |
| **Regla de confidencialidad** | Si en cualquier momento se usa un documento real de XARU, **ningún nombre, número, importe ni firma puede ser legible** ni recuperable por ampliación. Verificar a 400 %. |

**Alt:** EN `Close-up of a closed paper file on a dark table, side light.` · ES `Primer plano de un expediente de papel cerrado sobre una mesa oscura, con luz lateral.` · AR `لقطة قريبة لملف ورقي مغلق على طاولة داكنة بإضاءة جانبية.` · ZH `深色桌面上一份合拢的纸质档案特写，侧光。`

---

### H-11 · Insights (`#insights-home` — *"Perspective, by sector"*)

| Campo | Definición |
|---|---|
| **Qué debe mostrar** | Las **portadas de los cuatro artículos existentes**, cada una distinta y cada una coincidente con el tema exacto de su artículo. No una imagen nueva para el bloque. |
| **Clasificación** | **CATEGORÍA** (stock editorial permitido en Insights) — pero heredada, no nueva. |
| **Recurso** | Reutiliza I-11a/b/c/d definidas en `visual-plan-inner-pages.md` §7 (operational-hospitality, territorial-land, capital-halted-projects, international-establishment). **Coste visual de este bloque en la portada: 0 imágenes nuevas.** |
| **Regla crítica** | Hoy cada artículo hereda la imagen IA de la ficha del activo del que habla: el análisis parece publicidad del activo (correspondencia 2, riesgo alto). **Una portada de Insights nunca puede ser la foto de un activo del catálogo de XARU.** La independencia editorial se ve antes de leerse. |
| **Tratamiento** | Miniaturas 3:2 con duotono al 20 %, a color pleno en `:hover`/`:focus`. Sin texto quemado. |
| **Recorte móvil** | Carrusel de 1,15 tarjetas visibles, ratio 3:2 mantenido. |

**Alt:** el alt de cada artículo, definido en `visual-plan-inner-pages.md` §7. Nunca `alt="artículo de análisis"`.

---

### H-12 · Private Desk (`#private-desk` — *"One conversation. One structure. Total confidentiality."*)

| Campo | Definición |
|---|---|
| **Qué debe mostrar** | Silencio. Una habitación con una sola luz, un pasillo hacia una puerta cerrada, una mesa con dos sillas, una ventana de noche. **Sin personas, sin pantallas, sin teléfono, sin gráfico.** El bloque debe leerse como una puerta que se abre, no como un anuncio. |
| **Clasificación** | **CATEGORÍA** |
| **Recurso** | **I-09** — 2800×1750, horizontal 8:5, exposición baja, ISO limpio. |
| **Tratamiento** | El más oscuro de la portada: duotono negro puro al 78 %, negros con detalle (no aplastados), única fuente de luz cálida en el punto donde arranca el CTA. Sin grano añadido. |
| **Foco** | Fuente de luz alineada con el botón *Private Enquiry*: la imagen conduce al clic sin decirlo. |
| **Recorte móvil** | Variante 4:5. Mantener la fuente de luz dentro del encuadre en todos los breakpoints — es el único elemento con contenido. |

**Alt:** EN `A dimly lit room with a single door and a table, no people.` · ES `Una sala en penumbra con una sola puerta y una mesa, sin personas.` · AR `غرفة خافتة الإضاءة بها باب واحد وطاولة، بلا أشخاص.` · ZH `一间光线昏暗的房间，只有一扇门和一张桌子，画面中没有人。`

---

## 4. TABLA RESUMEN DE LA PORTADA

| # | Bloque | Clasificación | Recurso | Tratamiento | Estado |
|---|---|---|---|---|---|
| H-01 | Hero | CATEGORÍA + 2 BLOQUEOS | V-01 + I-01 (poster) | Duotono noche 42 %, degradado inferior 60 % | Publicable con 1 diapositiva |
| H-02 | Selector de recorrido | MARCA | — | Pictogramas lineales, acento dorado | Publicable |
| H-03 | Tres mercados | CATEGORÍA ×3 | I-02, I-03, I-04 | Duotono 18 %, color en hover | Publicable |
| H-04 | Oportunidades destacadas | ESPECÍFICO ×11 + teaser | Material real por activo | Teaser tipográfico sobre negro | **Bloqueado** |
| H-05 | Acquire → Expand | CATEGORÍA | I-05 | Duotono piedra 55 %, banda 8:3 | Publicable |
| H-06 | Doble vía proyectos/capital | CATEGORÍA | I-06 (díptico) | Color/monocromo contrapuestos | Publicable |
| H-07 | ASHIMA | ESPECÍFICO | Aérea real / masterplan / render rotulado | Sin filtro; rótulo obligatorio | **Bloqueado** |
| H-08 | Infraestructura empresarial | CATEGORÍA | I-07 | Duotono acero 70 % | Publicable |
| H-09 | Presencia real | ESPECÍFICO | R-01 (oficina XARU) | Sin filtro, verticales rectificadas | **Bloqueado** |
| H-10 | Gobierno y confianza | CATEGORÍA | I-08 | Casi monocromo, saturación −60 % | Publicable |
| H-11 | Insights | CATEGORÍA (heredada) | I-11a…d | Duotono 20 %, color en hover | Publicable |
| H-12 | Private Desk | CATEGORÍA | I-09 | Duotono negro 78 % | Publicable |

**8 de 12 bloques publicables de inmediato. 4 bloqueados hasta recibir material auténtico** (las tres diapositivas y bloques que hoy concentran 17 de los 17 problemas críticos de la portada).

---

## 5. CRITERIOS DE ACEPTACIÓN DE LA FASE 3

Un bloque se da por resuelto cuando cumple **todos** los puntos:

1. Su clasificación (CATEGORÍA / ESPECÍFICO / BLOQUEO / MARCA) está declarada y respetada.
2. Ningún activo con nombre, precio, ubicación, superficie, nº de llaves o licencia está ilustrado con stock.
3. El recurso existe en **3 anchos** y con **variante vertical propia** (no recorte automático).
4. `object-position` / `background-position` declarado por breakpoint, con pérdida de encuadre en móvil **< 25 %**.
5. Alt text en EN/ES/AR/ZH, descriptivo de lo que la imagen muestra, sin adjetivos comerciales ni acumulación de palabras clave.
6. Licencia registrada en la hoja de control (recurso · proveedor · nº · factura · fecha · alcance).
7. Contraste del texto sobre la imagen ≥ 4,5:1 medido **sobre el fotograma real**, no sobre una media.
8. Ningún archivo se repite en dos bloques con significados distintos.
9. Total de la página: **1 vídeo y ≤ 12 imágenes**.
