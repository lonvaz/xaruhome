# GAP_MATRIX — Biblia de Real Estate vs. repositorio real

Formato exigido por §3.3. Alcance: **sección de real estate**.
Base: commit `d72bd82`, auditoría del 2026-08-02.

Leyenda de estado: **E** existe · **P** parcial · **A** ausente.

Riesgo: **B** bloqueante para la Biblia · **M** medio · **L** bajo.

---

## A. Defectos de la superficie actual — ejecutables sobre el stack de hoy

Estos no dependen de infraestructura nueva. Son los que se ejecutan en esta
entrega.

| ID | Capacidad | Estado | Evidencia | Riesgo | Dependencia | Fase | Criterio de aceptación |
|---|---|---|---|---|---|---|---|
| A1 | §1.2 Los seis activos de prueba migrados a `SOLD` | A | 6/6 publicados como activos; el vocabulario no tiene `sold` | B | ninguna | 0 | 6 fichas responden 200 con insignia Vendido; 0 apariciones en resultados por defecto; filtro explícito los recupera; historial de transición registrado |
| A2 | §1.2 CTA comercial bloqueado en vendidos | A | ficha muestra «Enquire privately» | B | A1 | 0 | 0 CTA de compra en las 24 fichas vendidas (6 × 4 idiomas); sustituido por «Buscar propiedades similares» |
| A3 | §5.1 Ruta `/real-estate/sold/` | A | no existe | M | A1 | 0 | 4 rutas 200, listan las 6 operaciones anteriores, enlazadas desde el catálogo |
| A4 | §1.1 Enlaces sociales `#` retirados o resueltos | A | 519 enlaces muertos en 169 páginas | B | URLs reales (Josep) | 0 | 0 `href="#"` en el HTML público |
| A5 | §1.1 `SearchAction` funcional | P | ruta 200 pero ignora `?q=` | B | ninguna | 0 | `?q=término` filtra el catálogo y el contador refleja el resultado |
| A6 | §20.2/§26.3 `index.html` fuera de las URLs públicas | P | `_redirects` cubre los 301; quedan 278 enlaces internos `index.html#ancla` | M | ninguna | 0 | 0 referencias internas con `index.html` |
| A7 | §24 Build reproducible — generador versionado | A | `gen_i18n.py` fuera del repo | B | ninguna | 0 | `git ls-files` incluye el generador y sus 12 módulos |
| A8 | §36 Estado vacío honesto en Featured Opportunities | A | la pestaña *Private* queda vacía al retirar los seis | M | A1 | 0 | estado vacío explicado, con salida al catálogo y a operaciones anteriores |

---

## B. Capacidades de plataforma — requieren infraestructura que hoy no existe

Ninguna es ejecutable sobre hosting estático. Se listan con su dependencia real
para que la decisión sea informada, no para simularlas.

| ID | Capacidad | Estado | Evidencia | Riesgo | Dependencia | Fase | Criterio de aceptación |
|---|---|---|---|---|---|---|---|
| B1 | §20.1 SSR/ISR del portal | A | sitio estático pregenerado | B | Next.js + hosting con runtime | 1 | contenido principal renderizado en servidor sin JS |
| B2 | §6 Modelo canónico `Listing` (≈120 campos) | P | 24 campos en JSON plano | B | PostgreSQL | 2 | esquema migrado, constraints, dinero sin float |
| B3 | §7 Máquina de estados de 17 estados | A | campo `status` de texto libre | B | B2 | 2 | transiciones sólo por comando autorizado, con auditoría |
| B4 | §13 Motor de búsqueda | A | filtrado en el navegador (D5) | B | Elasticsearch | 4 | facetas coherentes, `search_after`, p95 ≤ 250 ms |
| B5 | §5.3 PLP con mapa, polígono y URL reproducible | A | no existe | B | B4 + MapProvider | 4 | filtros sincronizados con URL, mapa con clusters |
| B6 | §5.4 PDP con los 23 bloques | P | 8 de 23 (estado, ubicación, precio, hab., baños, superficies, estilo, galería única) | B | B2 | 4 | ocultación condicional, JSON-LD completo |
| B7 | §18 Identidad, sesiones, MFA | A | no hay autenticación | B | Identity Service | 1 | login, rotación de refresh, aislamiento por tenant probado |
| B8 | §5.7 Panel de comprador | A | no existe | B | B7 | 5 | favoritos, búsquedas guardadas, alertas |
| B9 | §5.8 Panel B2B | A | no existe | B | B7 + B2 | 2/5 | inventario, CRM, métricas, facturación |
| B10 | §5.9 Super Admin y moderación | A | no existe | B | B7 | 3 | cola con SLA, decisiones auditadas, doble aprobación |
| B11 | §9 Los 18 microservicios | A | no existe ninguno | B | Kubernetes | 1–8 | cada servicio propietario de sus datos, desplegable solo |
| B12 | §11 Los 33 eventos versionados | A | no existe bus | B | Kafka | 1 | outbox transaccional, consumidores idempotentes, DLQ |
| B13 | §14 Pipeline multimedia asíncrono | P | derivadas AVIF/WebP/JPEG generadas en build; sin antivirus, EXIF, hash perceptual en producción ni watermark | M | Media Service | 3 | 14 pasos del §14.2 con evento por fichero |
| B14 | §17 Facturación, créditos y promociones | A | no existe | B | B7 + pasarela | 7 | pago idempotente y conciliable, ledger inmutable |
| B15 | §5.5 Proyectos off-plan | A | no existe | M | B2 | 6 | planes de pago que suman 100 %, progreso con fuente |
| B16 | §5.6 Agentes y agencias | A | retirados en esta sesión por ser personas inventadas | M | B7 | 4 | perfiles reales con licencia verificable |
| B17 | §9.15 Datos de mercado | A | no existe | M | fuente autorizada | 8 | provenance, fecha, metodología, supresión de muestra |
| B18 | §21/§22 Infraestructura y observabilidad | A | no existe | B | cuenta cloud | 1 | Terraform, SLOs, trazas, alertas por burn-rate |
| B19 | §25 Estrategia de pruebas | A | 0 % cobertura, sin tests | B | ninguna técnica; sí tiempo | 1 | unit, integración, contrato, E2E críticos en verde |
| B20 | §23 Capacidad para 1 M de listings | A | 156 activos demo | M | B4 + B18 | 9 | pruebas de carga dentro de SLO |

---

## C. Decisión requerida antes de la Fase 1

La Biblia §29 me autoriza a no pedir confirmación por decisiones técnicas
reversibles, y me obliga a detenerme cuando falta una decisión comercial. Aquí
falta una:

**El bloque B no es un refactor del sitio actual: es la construcción de una
plataforma nueva en paralelo** (§4.1 lo dice explícitamente: «si el repositorio
actual no es Next.js, no ejecutes un rewrite de un solo golpe; crea la nueva
aplicación en paralelo»). Requiere:

1. una cuenta cloud con presupuesto recurrente,
2. credenciales de mapas, pagos y notificaciones,
3. inventario real que publicar — sin inventario, un marketplace es una
   vitrina vacía, y §31 prohíbe expresamente publicar propiedades de prueba
   como disponibles,
4. una decisión sobre operación: moderadores, SLA y soporte (§37).

Sin esas cuatro, cualquier «entrega» del bloque B sería exactamente lo que la
Biblia prohíbe en §31: microservicios simulados, datos inventados y un «listo»
sin pruebas.

**Recomendación:** ejecutar el bloque A ahora — que es real, verificable y
elimina los defectos que la propia Biblia señala en §1.1 y §1.2 — y abrir el
bloque B como programa con presupuesto, empezando por A7 (versionar el
generador) y B19 (pruebas), que son los dos cimientos que no dependen de
infraestructura.
