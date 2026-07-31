# Decisión de abastecimiento de material visual — RESUELTA

> Estado: **DESBLOQUEADO Y EJECUTADO** (31-jul-2026). Fuente autorizada encontrada, 24 imágenes reales integradas, manifiesto de licencias completo.

## Resolución

El bloqueo se resolvió por una vía que cumple la biblia sin excepciones: **el catálogo de stock de Freepik, accesible mediante la cuenta conectada del usuario a través de su API autorizada.**

Esto importa por tres razones:

1. **Es acceso autorizado, no scraping.** La biblia prohíbe expresamente descargar material «mediante scraping, bots o métodos que violen las condiciones de las plataformas». La vía anterior que se estaba explorando —extraer identificadores de fotografía del HTML de páginas de búsqueda— habría violado esa regla. La API de la cuenta no.
2. **Tiene filtro nativo anti-IA.** Las búsquedas se ejecutaron con el parámetro `ai_generated=excluded`. Ese filtro no es infalible: en una de las búsquedas apareció un resultado cuyo propio título contenía «Generative AI». Por eso **no se confió en el filtro**: se descargaron previsualizaciones de las 85 candidatas, se montaron cinco hojas de contacto y **se revisaron una a una visualmente** antes de elegir.
3. **Entrega originales, no previews.** Los 24 archivos finales llegaron entre 7 MP y 41 MP, sin marca de agua. No se ha usado ninguna previsualización marcada.

## Proceso ejecutado (auditable)

| Paso | Resultado |
|---|---|
| Búsquedas curadas por hueco, con filtro no-IA y orientación apaisada | 85 candidatas preseleccionadas por título |
| Descarga de previsualizaciones + 5 hojas de contacto | 83 revisadas visualmente al 100% |
| Selección en modo director | 24 aprobadas · 59 descartadas |
| Descarga de originales con licencia | 24 archivos, 7–41 MP, sin marca de agua |
| Verificación final del original (2 hojas de contacto) | 0 marcas de agua · 0 artefactos de IA · geografía correcta |
| Optimización | fichas 1600 px · fondos 2200 px · JPEG progresivo q72–84 |
| Integración | 15 sustituciones + 9 altas, 4 idiomas, 0 referencias rotas |

### Motivos de rechazo aplicados (ejemplos reales)
- **`426493597`** (torre de cristal al anochecer) — rechazada por **leer como render 3D/CGI**, no como fotografía.
- **`25592699`** (Marina Bay Sands) — rechazada por ser un **edificio icónico e identificable**: usarla insinuaría que XARU tiene relación con ese activo concreto.
- **`50321835`** (Villa del Balbianello) — rechazada por el mismo motivo: es una propiedad museística conocida.
- **`427586279`** (resort de Phuket con la playa llena de sombrillas) — rechazada por **leer como turismo de masas**, no como lujo.
- **`9655216`, `30415102`, `23873827`, `21739285`** — rechazadas por **calidad de instantánea** o gama media.
- **`25_reforma_towers`** — descargada y **descartada en integración** por ser casi idéntica a `12_atico_cdmx` (misma escena, mismo autor): habría reintroducido el problema de duplicación que la auditoría señalaba.

## Regla de honestidad visual aplicada en el producto

La biblia es literal: el stock puede representar una **categoría**, nunca un **activo concreto**. Como las fichas nombran y ponen precio a activos («Penthouse, Central London», «EUR 18.500.000»), no bastaba con elegir bien la imagen. Se ha añadido, en los cuatro idiomas y bajo cada imagen de ficha:

> *Imagen de referencia de categoría. Fotografía de stock con licencia — no corresponde a este activo concreto.*

Y bajo el bloque de ASHIMA, con redacción distinta porque el problema es distinto:

> *Imagen ilustrativa — referencia geográfica y ambiental de la región. No representa el proyecto construido.*

La marca tipográfica reutiliza el estilo existente (`xr_phase0`), de modo que la nota es discreta y **no altera el diseño**.

## Hallazgo crítico corregido

`08_penthouse_london.jpg` contenía **una casa de Tulum** y se servía en **44 páginas de Londres**. Ahora contiene el skyline de la City de Londres a la hora azul. Todas las geografías se han verificado imagen por imagen: Dubái es Dubái, Como es Como, Marbella es Puerto Banús, Tulum es Quintana Roo, CDMX es Paseo de la Reforma.

## Lo que sigue sin resolverse (y no se disimula)

- **El material ESPECÍFICO sigue pendiente.** Ninguna de estas 24 imágenes muestra un activo real de XARU. Los 178 bloques marcados `REAL_MEDIA_REQUIRED` en `visual-audit.md` siguen requiriendo producción propia: ver `docs/xaru-original-production-shot-list.md` (41 tomas; dos jornadas de rodaje desbloquean la mayoría).
- **ASHIMA no tiene todavía material real.** La imagen actual es referencia geográfica declarada como tal.
- **Retratos de equipo y oficinas:** no se ha integrado ningún retrato de stock como equipo de XARU ni ninguna oficina de stock como sede. Sigue pendiente de la Fase 0.
- **Derivados AVIF/WebP:** generados en el script de construcción pero **no integrados**, porque las imágenes se sirven como `background-image` en CSS y el cambio a `image-set()` requiere una prueba aparte. No se toca sin verificar: la regla de no romper el diseño manda.

## Lo que no se ha hecho bajo ninguna circunstancia
- Afirmar que se descargó material de Envato o Artlist. **No se descargó nada de esas plataformas**: no hay credenciales y así queda dicho.
- Usar previsualizaciones con marca de agua.
- Hotlinkear desde ninguna plataforma: los 24 archivos se sirven desde el propio repositorio.
- Presentar stock como un activo concreto sin decirlo.
- Presentar retratos de stock como equipo de XARU.

## Sobre Wikimedia Commons (descartada previamente, se mantiene el registro)
Se probaron 26 descargas con filtros de resolución y licencia comercial. Revisión visual: `architects_plans` era una fotografía en blanco y negro del siglo XIX; `casa_tulum`, un grabado antiguo de ruinas; `oaxaca_coast`, un grafiti de un pez; `architecture_detail`, una foto sepia del Louvre. Aproximadamente 4 de 14 resultaban utilizables y ninguna alcanzaba el estándar de Knight Frank / Sotheby's / Engel & Völkers. Es un archivo documental enciclopédico, no una fototeca comercial. **No se integró ninguna.**
