# CURRENT_STATE — XARU HOME

Auditoría de Fase 0 exigida por la Biblia de Real Estate §3 y §32.
Alcance acordado: **sección de real estate**.

- Fecha de la auditoría: 2026-08-02
- Repositorio: `github.com/lonvaz/xaruhome`
- Rama: `main` · commit auditado `d72bd82`
- Árbol de trabajo: limpio en el momento de auditar
- Método: inspección del checkout real y ejecución de comprobaciones. Lo que
  no está confirmado por código o por una prueba ejecutada aparece marcado
  como **hipótesis**.

---

## 1. Stack confirmado

| Capa | Realidad medida | Evidencia |
|---|---|---|
| Generación | Generador estático propio en Python 3.11 (`gen_i18n.py`, 3.863 líneas, + 12 módulos de copy/datos) | `python3 gen_i18n.py` produce las 197 páginas |
| Salida | HTML estático plano, 2.909 ficheros versionados, 840 JPG / 594 WebP / 492 AVIF | `git ls-files` |
| Runtime servidor | **Ninguno.** No hay proceso de servidor, base de datos, API ni autenticación | ausencia de manifiestos y de código de servidor |
| Manifiestos | No hay `package.json`, `requirements.txt`, `pyproject.toml`, `Gemfile` ni `composer.json` | `ls` en la raíz |
| CI/CD | **Ninguno.** No hay `.github/`, `.gitlab-ci.yml`, `Dockerfile`, `docker-compose` | `ls -a` |
| IaC | **Ninguna.** No hay Terraform, Kubernetes ni Helm | `ls -a` |
| Hosting | Cloudflare Pages (o compatible): hay `_redirects`, `_headers`, `CNAME` = `xaruhome.com`, `.nojekyll` | ficheros presentes en la raíz |
| Front | jQuery, Bootstrap, Slick, Tom Select, Swiper + JS propio (`xaru-catalog.js`, `xaru-property-detail.js`, `xaru-effects.js`) | `assets/js/` |
| Datos | Tres paquetes JSON del catálogo (`data/properties/*.json`, 156 activos demo) y `data/opportunities.json` (13 oportunidades) | ficheros leídos |
| i18n | Cuatro idiomas por carpeta: raíz EN, `/es/`, `/ar/` (RTL), `/zh/` | árbol de directorios |

**Conclusión de stack:** XARU HOME es hoy un **sitio estático generado**, no una
aplicación. La Biblia describe una plataforma de marketplace con SSR,
microservicios, PostgreSQL, Elasticsearch, Kafka, Kubernetes y facturación. La
distancia no es de refactor: es de construcción de plataforma. Ver
`GAP_MATRIX.md`.

---

## 2. Hallazgo bloqueante — Sev-1

**El generador no está bajo control de versiones.**

- Raíz del repositorio: `/home/claude/work/site/xaru`
- Generador: `/home/claude/work/site/gen_i18n.py` — **fuera** del repositorio
- Sólo hay 5 `.py` versionados: los cuatro `tools_*.py` y una copia congelada
  en `docs/gen_i18n.py` (3.398 líneas, del 2026-07-31), ya **465 líneas por
  detrás** de la fuente real.

Consecuencia: si se pierde el entorno de trabajo, el sitio sólo puede editarse
como HTML estático y toda la maquinaria de i18n, SEO y catálogo desaparece. La
Biblia §24 exige build reproducible; hoy no lo es para nadie salvo esta sesión.

**Acción exigida antes de cualquier otra fase:** versionar el generador dentro
del repositorio. Se ejecuta en esta entrega.

---

## 3. Estado de la sección real estate

48 páginas HTML bajo `real-estate/` (12 rutas × 4 idiomas):

```
/real-estate/                                    portada de pilar
/real-estate/private-properties/                 catálogo (6 activos)
/real-estate/private-properties/pp-*/            6 fichas
/real-estate/commercial-hospitality/             catálogo (3 activos)
/real-estate/commercial-hospitality/ch-*/        3 fichas
```

Más, fuera del árbol `/real-estate/` pero funcionalmente parte de la sección:

```
/property-listing-buy.html      72 activos residenciales (catálogo demo)
/property-listing-rent.html     51 activos comerciales
/property-listing-search.html   156 activos, todo el portafolio
/property-details.html?id=…     ficha construida en cliente desde JSON
```

### 3.1 Los seis activos de prueba, trazados hasta su fuente

Fuente única: `data/opportunities.json` → clave `opportunities`, registros con
prefijo `pp-`. No existe base de datos ni otra copia.

| id | estado actual | precio | ficha |
|---|---|---|---|
| `pp-samana-island` | `exclusive-mandate` | PoA (USD) | `/real-estate/private-properties/pp-samana-island/` |
| `pp-villa-dubai` | `available` | AED 95.000.000 | `/real-estate/private-properties/pp-villa-dubai/` |
| `pp-penthouse-london` | `exclusive-mandate` | PoA (GBP) | `/real-estate/private-properties/pp-penthouse-london/` |
| `pp-villa-como` | `off-market` | PoA (EUR) | `/real-estate/private-properties/pp-villa-como/` |
| `pp-casa-tulum` | `available` | USD 6.900.000 | `/real-estate/private-properties/pp-casa-tulum/` |
| `pp-villa-marbella` | `under-negotiation` | EUR 18.500.000 | `/real-estate/private-properties/pp-villa-marbella/` |

Superficies donde se renderizan hoy: portada (pestaña *Private* de Featured
Opportunities), `/real-estate/`, `/real-estate/private-properties/` y su ficha
propia — en los cuatro idiomas.

El vocabulario de estados del fichero tiene 15 valores y **no incluye
`sold`**. `closed` existe pero no se usa en ningún registro y no tiene el
tratamiento público que exige §1.2.

---

## 4. Defectos verificados en la superficie pública

Todos medidos sobre el HTML generado, no inferidos.

| # | Defecto | Medida | Referencia |
|---|---|---|---|
| D1 | Enlaces muertos `href="#"` | **739** en 178 páginas vivas; 519 son los tres iconos sociales (LinkedIn, Instagram, YouTube) repetidos en 169 páginas | §1.1, §0.5 |
| D2 | `SearchAction` apunta a una página que ignora el término | JSON-LD declara `/{lang}/property-listing-search.html?q={search_term_string}`; la página existe (200) pero `xaru-catalog.js` no lee `location.search` en ninguna línea | §1.1 |
| D3 | Enlaces internos con `index.html` | **278** referencias, todas del tipo `index.html#ancla` | §20.2, §26.3 |
| D4 | Los seis activos de prueba se publican como disponibles | 6 de 6 con estado activo; contador «Showing 6 of 6» | §1.2, §31 |
| D5 | Filtrado de catálogo en el navegador | `catalog_block` inyecta todas las tarjetas y las oculta con `style.display`; `xaru-catalog.js` renderiza los 156 activos en el cliente | §31 «filtrar miles de resultados en el navegador» |
| D6 | Sin estado de resultados vacíos indexable ni control de facetas | no hay `noindex` por faceta ni URL reproducible de búsqueda | §20.3, §5.3 |

`_redirects` **sí** cubre ya los 301 de `index.html` por idioma y el blog
heredado. No hay cadenas ni bucles detectados.

`canonical`, `robots=index,follow` y `hreflang` (en/es/ar/zh + x-default)
están presentes y correctos en las rutas de real estate comprobadas.

---

## 5. Deuda que bloquea la Biblia

| Bloqueo | Qué impide |
|---|---|
| No hay servidor ni runtime | SSR/ISR (§20.1), API (§10), autenticación (§18), paneles B2B (§5.8) y Super Admin (§5.9) |
| No hay base de datos | Modelo canónico (§6), máquina de estados persistida (§7), CRM (§9.10), ledger (§17.3) |
| No hay Elasticsearch | Búsqueda, facetas, autocompletado y mapa (§13) |
| No hay bus de eventos | Los 33 eventos de §11, outbox/inbox, DLQ |
| No hay CI ni IaC | Todo §21, §22, §24 |
| Generador fuera de git | Build reproducible (§24), cualquier trabajo en equipo |

**Coste de entrada realista** (hipótesis, para dimensionar la decisión): la
Biblia describe entre 18 y 20 servicios, cinco motores de persistencia
administrados y un clúster Kubernetes. Es un programa de varios equipos y
varios meses, con coste de infraestructura recurrente. No es ejecutable dentro
de una sesión de trabajo ni sobre hosting estático.

---

## 6. Riesgos de seguridad y privacidad

- No hay superficie de autenticación, luego no hay riesgo de fuga entre
  tenants **hoy** — pero tampoco hay aislamiento que probar.
- `_headers` aporta `X-Content-Type-Options`, `X-Frame-Options`,
  `Referrer-Policy` y `Permissions-Policy`. **Falta CSP y HSTS** (§19).
- No hay documentos regulatorios ni PII en el repositorio. Verificado: no hay
  correos ni teléfonos privados en JSON-LD.
- El token de GitHub aparece embebido en la URL del remoto local. No está
  versionado, pero conviene rotarlo y usar credencial externa.

---

## 7. Accesibilidad

- Contraste del hook corregido en esta sesión (titulares `h2` de las
  diapositivas 2 y 3 heredaban color oscuro sobre foto oscura).
- 739 enlaces `href="#"` son también un defecto de accesibilidad: un enlace sin
  destino es un objetivo de foco que no hace nada.
- Pendiente de auditoría formal WCAG 2.2 AA sobre rutas críticas (§25.5).

---

## 8. Cambios locales del usuario que deben preservarse

- `assets/js/xaru-property-detail.js` tiene ediciones locales posteriores a mi
  última escritura. Se conservan íntegras; ninguna tarea de esta entrega lo
  reescribe.

---

## 9. Secretos e integraciones requeridos (inventario, sin valores)

| Integración | Necesaria para | Estado |
|---|---|---|
| Proveedor de mapas (Mapbox/Google) | §5.3 vista mapa, clusters, polígono | no configurada |
| Proveedor de pagos (Stripe/Checkout.com) | §17.2 | no configurada |
| Proveedor de email/SMS/WhatsApp | §9.11 notificaciones y leads | no configurada |
| Cuenta cloud (AWS de referencia) | §21 completo | no configurada |
| URLs reales de redes sociales | §1.1 D1 | **pendiente de Josep** |

---

## 10. Baseline ejecutada

```
python3 gen_i18n.py            → 197 páginas, sitemap 164 URLs, sin error
referencias rotas              → 0   (comprobador propio sobre todo el HTML)
auditoría headless 22 rutas    → 0 incidencias (404, H1, desbordamiento)
duplicados de imagen           → 0   (MD5 + hash perceptual sobre 184 fotos)
peso portada                   → 6,3 MB · interiores ≈ 2,8 MB
```

No existen pruebas unitarias, de integración, de contrato ni E2E. Cobertura: 0 %.
