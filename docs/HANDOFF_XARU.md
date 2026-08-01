# TRASPASO — XARU HOME · continuar en sesión nueva
> Para retomar: adjunta este archivo y di **"continúa XARU HOME desde este traspaso"**.
> **BIBLIA innegociable:** `XARU_HOME/DERROTERO_MAESTRO_V2.md` (+ `AUDITORIA_COMPETITIVA.md`). Leerlos es obligatorio.

## Estado (31-jul-2026) — RE-ARQUITECTURA EMPRESARIAL COMPLETA
Sitio **en vivo**: https://xaruhome.com · HTTPS ✓ · 4 idiomas (EN raíz, /es/, /ar/ RTL, /zh/) · Repo `lonvaz/xaruhome` (GitHub Pages).

**Fases 1-6 ejecutadas y publicadas** (según la biblia PDF "Problema configuración web"):
- **F1 Arquitectura ✔** — Mega-menú de **4 puertas** (Real Estate · Developments · Capital & Transactions · Business Infrastructure) + Company + Insights, con paneles mega; móvil = acordeón + selector de idioma; RTL correcto. Rutas semánticas limpias. `data/opportunities.json` (modelo de datos separado del HTML) + `data/SCHEMA.md` con los **15 estados obligatorios**. Formularios intake doble vía.
- **F2 Núcleo inmobiliario ✔** — **Portada de 12 bloques** (§4: hero, selector de recorrido, 3 mercados, oportunidades por pestañas, Acquire→Expand, doble vía, ASHIMA, infraestructura, presencia real, gobierno, insights, private desk). **3 catálogos** que renderizan el JSON con filtros propios y badges de estado. **5 modelos de ficha** (residencial, comercial/hotelero con teaser P&L, suelo/desarrollo, teaser confidencial, activo productivo).
- **F3 Desarrollo y capital ✔** — Project Structuring (proceso visible de **12 pasos**, fórmula de roles obligatoria, fideicomiso, metodología ASHIMA), Capital & Partnerships (**doble vía A/B** + proceso de 14 ítems, "no somos matchmaker"), **Private Deal Room** (ruta privada de **9 pasos** + qué se protege + request access).
- **F4 Infraestructura empresarial ✔** — Trade & Financial Infrastructure (subdivisión A commodities/offtake, B infra financiera; **fórmula correcta**: "XARU diseña, integra y coordina… con entidades y proveedores autorizados"; **cero menciones a BMP/VAIHOK/CoreFlex**), Corporate Services & Relocation (ciclo de 10 etapas, **2 recorridos**: Corporate Landing / Private & Family Landing).
- **F5 Confianza institucional ✔** — `/company/` completa (3 niveles, **5 valores corporativos** separados de los pilares narrativos de ASHIMA, modelo operativo, oficinas, equipo por especialidad, **entidades con ambigüedad legal literal**, gobernanza, casos, red internacional). `/insights/` hub de 7 sectores + **4 artículos fundacionales**.
- **F6 Cierre técnico SEO ✔** — 136 páginas nuevas con SEO; **197 titles únicos sitewide, 0 duplicados**; **468 bloques JSON-LD válidos**; sitemap **176 URLs**; `llms.txt` reescrito a la nueva arquitectura; QA sitewide: **0 enlaces rotos, 0 [PENDING]**, 16 [PHASE 0] legítimos.

## Reglas permanentes de Josep
- **Ambigüedad legal SIEMPRE** en público (NEXARU GLOBAL, licencia EAU; nunca números ni razones sociales). La Capability & License Matrix es **interna, nunca se publica**.
- Compliance cripto/financiero literal (canales regulados, KYC/AML). Nunca "somos una entidad financiera global".
- **No romper el diseño** (negro/marfil/dorado, Playfair+Poppins, parallax, editorial). Todo en los 4 idiomas vía generador.
- Modo director: auditar con datos/capturas antes de entregar. Operarios desechables para el trabajo pesado.

## Método técnico
- **Publicar** = `git push` desde `/home/claude/work/site/xaru` (main → GitHub Pages, ~1-2 min). Token fine-grained `xaru-publisher` vive en el entorno de ESTA sesión (caduca 28-oct-2026); en sesión nueva hay que regenerarlo por el navegador (usuario GitHub: **lonvaz**).
- **Generador** (fuente única, NO editar HTML a mano): `gen_i18n.py` + `page_dicts.py` + `seo_meta.py` + `arch_data.py` + `f3_copy.py` + `f4_copy.py` + `f5_copy.py` + `f5_articles.py`. Notas: `I18N_NOTES.md`.
- Puente al Mac: solo `mcp__remote-devices__applescript__*`; shell = base64→clipboard→Terminal. Capturas >~1.2MB o >8000px: comprimir antes de SendUserFile.
- DNS en Wix (4 registros A GitHub + CNAME www). **Cloudflare: PAUSADO** — Wix bloquea DNSSEC y nameservers; solo se destraba con soporte de Wix o transfiriendo el dominio. No es urgente: el sitio ya vuela y el canonical resuelve el index.html.

## PENDIENTE — FASE 0 (única bloqueada, depende de Josep)
Datos reales para la capa de credibilidad (§12 del derrotero): entidades/jurisdicciones por capacidad · oficinas nombrables · equipo (áreas/bios autorizadas) · proyectos verificables además de ASHIMA · qué es directo vs coordinado · red internacional confirmada. Hoy marcados como **[PHASE 0]** (16 puntos) en Company y portada.

## Otros pendientes
PR #1 (`agent/clean-home-urls-seo`) sigue **abierto sin fusionar** en GitHub. · Artículos de los 3 sectores restantes de Insights. · Backend real de formularios + CRM. · Revisión nativa del árabe y el chino antes de promocionar. · CoreFlex Card Banks EN PAUSA (ver `HANDOFF_COREFLEX.md`; siguiente: plantilla 08).

## SISTEMA VISUAL — FOTOGRAFIA REAL INTEGRADA (31-jul-2026) · PR #2 ABIERTO SIN FUSIONAR
Rama `agent/real-stock-media-audit` · PR **#2 "Rebuild XARU HOME visual system with verified real media"** — **NO fusionar** (orden de Josep).

**Desbloqueo:** la fuente autorizada es el **catalogo de stock de Freepik via la API de la cuenta conectada** (no scraping — la biblia lo prohibe expresamente). Busquedas con `ai_generated=excluded`, pero **el filtro NO se dio por bueno**: un resultado traia "Generative AI" en su propio titulo. Se descargaron previews de las 85 candidatas, se montaron 5 hojas de contacto y **se revisaron una a una**. 24 aprobadas, 59 descartadas. Originales de 7 a 41 MP, sin marca de agua.

**Corregido (critico):** `08_penthouse_london.jpg` tenia **una casa de Tulum** servida en **44 paginas de Londres**. Ahora es la City de Londres. Todas las geografias verificadas: Dubai = Palm Jumeirah, Como = lago de Como, Marbella = Puerto Banus, Tulum = Quintana Roo, CDMX = Paseo de la Reforma.

**Regla de honestidad aplicada en producto:** el stock representa **categoria**, nunca **activo concreto**. Bajo cada imagen de ficha, en los 4 idiomas: *"Imagen de referencia de categoria. Fotografia de stock con licencia — no corresponde a este activo concreto."* Bajo ASHIMA, distinta: *"Imagen ilustrativa — referencia geografica y ambiental de la region. No representa el proyecto construido."* Clase `.xr_img_note` clonada de `.xr_phase0`: **una sola regla CSS, diseno intacto, RTL sin cambios**.

**Cambios:** 15 imagenes sustituidas con el mismo nombre (cero churn en 2.560 referencias) + 9 nuevas → cabeceras **16/16 unicas** (antes 5 duplicadas). 92 HTML regenerados en EN/ES/AR/ZH. **0 imagenes rotas, 0 titles duplicados.** Verificado con capturas: portada EN, ficha EN, ficha AR en RTL.

**Manifiesto:** `docs/media-license-manifest.csv` **poblado — 24 filas x 33 columnas, 0 celdas vacias**.

**Lo que sigue pendiente y NO se disimula:**
- Ninguna de las 24 muestra un activo real de XARU. Los **178 bloques `REAL_MEDIA_REQUIRED`** siguen exigiendo produccion propia (`docs/xaru-original-production-shot-list.md`, 41 tomas, 2 jornadas).
- **ASHIMA sin material real**; la imagen actual va declarada como referencia geografica.
- **Ningun retrato de stock como equipo XARU** ni oficina de stock como sede — depende de Fase 0.
- **Nada descargado de Envato ni Artlist** (sin credenciales) y asi queda escrito.
- **AVIF/WebP** generados en el script pero **no cableados**: son `background-image` de CSS y pasar a `image-set()` exige prueba aparte. No se toca sin verificar.

**Metodo del puente al Mac (mejorado):** ya NO hace falta base64 → portapapeles. Ahora: `SendUserFile` → `device_commit_files` escribe el fichero en `/Users/joseilc/XARU_HOME/` → se teclea una orden corta en Terminal → `device_stage_files` devuelve resultados al contenedor. Mucho mas fiable. Ojo: si el Terminal se queda ocupado, abrir ventana nueva con Cmd+N.

## RECONSTRUCCION VISUAL V3 (31-jul-2026) — rama `agent/xaru-stock-media-video-rebuild`
**Biblia nueva e innegociable: `docs/BIBLIA_VISUAL_V3.md`.** Prevalece sobre el derrotero.
Deroga la regla de bloquear secciones: XARU HOME es plataforma demostrativa/educativa,
nada se bloquea, nada se vacia, todo se completa con archivo real.

**Fuentes.** Solo Magnific (banco de archivo), Envato Elements y Artlist. Prohibido Freepik,
Unsplash, Pexels, IA y las herramientas de generacion de Magnific. **Estado real de acceso:**
el banco de Magnific responde para foto y video; Envato no tiene conexion; Artlist solo expone
generacion por IA (prohibida). Aviso de precision: la herramienta de banco de Magnific describe
su indice como catalogo de Freepik y sirve desde dominios de Magnific — es el banco de Magnific,
y asi queda escrito en la biblia.

**Commits hechos (4):**
1. `Audit current visual system and media inventory` — biblia V3 incorporada.
2. `Reposition XARU HOME hero and social metadata` — diapositivas 1 y 2 intactas; la 3ª pasa a
   video real 4K; nueva narrativa "hogar operativo de activos, proyectos, capital y expansion
   internacional" + title/meta/OG/Twitter en 4 idiomas. Una sola regla CSS.
3. `Expand luxury real estate demo catalog to a real data model` — `data/properties/*.json`,
   **144 activos** (60 residenciales/10 cat, 48 hospitality/8, 36 suelo/6), seis por categoria y
   cada uno una variante distinta. Metricas por tipo (llaves, amarres, % de avance, hectareas),
   todos los precios sobre 1M USD, `demo: true`, copia en 4 idiomas con toponimos traducidos.
4. `Add cinematic video system across public pages` — **6 videos reales 4K**, carga diferida por
   IntersectionObserver, pausa fuera de viewport, poster propio, respeto a prefers-reduced-motion.

**PENDIENTE principal: las 144 imagenes del catalogo.** Ver `docs/catalog-media-acquisition.md`
(estado, obstaculos medidos, criterios de descarte ya aplicados y 12 preselecciones validadas).
Dos hallazgos que ahorran tiempo: el `per_page` del banco NO se respeta (devuelve 50 siempre,
consume mucho contexto), y el filtro anti-IA **no descarta renders 3D**, que hay que ver y tirar.

**Tambien pendiente:** portada en 10 bloques, filtros por tipologia, derivados AVIF/WebP con
`<picture>`/`srcset`, sustitucion de las 15 imagenes gen2 restantes (fuera del hero, que esta
protegido), auditoria de 30 puntos y PR "Rebuild XARU HOME with real stock imagery, cinematic
video and complete demo inventory" **sin fusionar**.

**Aviso de la sesion:** en un momento el Mac tenia WhatsApp en primer plano y algunas pulsaciones
fueron ahi. Comprobar SIEMPRE `system_get_frontmost_app` antes de teclear en Terminal.
