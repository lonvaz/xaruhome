# Decisión de abastecimiento de material visual — REQUIERE DECISIÓN DE XARU

> Estado: **BLOQUEADO A LA ESPERA DE CREDENCIALES O ARCHIVOS.** Auditoría y planes completos; la sustitución no puede ejecutarse sin una fuente de fotografía profesional real.

## Qué se intentó y con qué resultado (evidencia, no opinión)

| Fuente | Acceso desde el entorno | Resultado |
|---|---|---|
| **Envato Elements** | Sin credenciales | No accesible. La plataforma exige cuenta con plan activo. No se ha descargado nada y **no se afirmará lo contrario**. |
| **Artlist** | Sin credenciales | No accesible. Igual que Envato. |
| **Unsplash** | API pública | **HTTP 401** — requiere clave de aplicación (gratuita, registro instantáneo). |
| **Pexels** | API pública | Requiere clave de aplicación (gratuita). |
| **Wikimedia Commons** | Accesible sin clave | **Probado con 26 descargas reales. NO APTO.** Ver más abajo. |

## Por qué Wikimedia Commons queda descartado
Se descargaron 26 imágenes con filtros de resolución (≥2200 px), orientación apaisada y licencia comercial. Revisión visual del resultado:

- `architects_plans` → fotografía en blanco y negro del siglo XIX de un edificio. No hay arquitectos ni planos.
- `casa_tulum` → **grabado antiguo** de ruinas arqueológicas.
- `oaxaca_coast` → mural de grafiti de un pez en una pared.
- `architecture_detail` → fotografía sepia histórica del Louvre.
- `office_meeting` → sala con mantel morado, iluminación fluorescente.
- `resort_beach` → paseo marítimo inglés con noria.
- `hero_coastline` → instantánea de montañas desde una embarcación.

Conclusión: Wikimedia es un **archivo documental enciclopédico**, no una fototeca comercial. Su criterio de admisión es el valor documental, no la calidad editorial. Aproximadamente 4 de 14 imágenes serían utilizables, y ninguna alcanza el estándar visual de Knight Frank / Sotheby's / Engel & Völkers. **Integrarlas degradaría la marca por debajo del estado actual.**

## Opciones para desbloquear (por orden de recomendación)

### Opción A — Clave de API gratuita de Unsplash o Pexels *(recomendada: 3 minutos, coste cero)*
Ambas son fototecas de **fotografía real profesional** (no IA) con licencia de uso comercial.
1. Unsplash: registrarse en `unsplash.com/developers` → "New Application" → copiar el *Access Key*.
2. Pexels: registrarse en `pexels.com/api` → copiar la *API Key*.
Con la clave, la sustitución completa (curaduría, descarga, optimización, integración en 4 idiomas y manifiesto de licencias) se ejecuta sin más intervención.
Precaución aplicable: ambas plataformas admiten hoy contenido generado por IA de forma minoritaria. Se filtrará por metadatos y **cada imagen se revisará visualmente** antes de integrarse, aplicando los criterios de rechazo de la Fase 6.

### Opción B — Envato Elements / Artlist con la cuenta de XARU *(la que exige la biblia)*
Es la vía canónica del documento. Dos formas:
1. **XARU descarga**: se entrega la lista de candidatos por espacio (plataforma, título, autor, ID, URL, motivo, orientación y resolución requeridas) y XARU coloca los originales sin marca de agua en `assets/media/incoming/`. La integración continúa desde ahí.
2. **Sesión asistida en el navegador**: con la sesión de Envato/Artlist abierta, la selección y descarga se realizan a la vista, y los archivos se colocan en `incoming/`.

### Opción C — Material propio de XARU
La vía de mayor valor y la única que resuelve el contenido ESPECÍFICO. Ver `docs/xaru-original-production-shot-list.md` (41 tomas priorizadas; 2 jornadas de rodaje desbloquean la mayoría de los 178 bloques `REAL_MEDIA_REQUIRED`).

## Lo que NO se hará bajo ninguna opción
- Afirmar que se descargó material de una plataforma sin acceso real.
- Usar previews con marca de agua.
- Hotlinkear desde Envato, Artlist u otra plataforma.
- Presentar stock como un activo concreto (propiedad nominada, ASHIMA, isla, hotel o terreno específico).
- Presentar retratos de stock como equipo de XARU ni oficinas de stock como sede de XARU.

## Estado de los entregables ya completos
- `docs/visual-audit.md` — auditoría de 184 páginas, 2.560 referencias, 83 archivos únicos, 178 bloques críticos.
- `docs/media-replacement-plan.csv` — 665 filas con diagnóstico y acción por recurso.
- `docs/visual-plan-home.md` — plan de los 12 bloques de portada.
- `docs/visual-plan-inner-pages.md` — plan de páginas interiores + color y accesibilidad.
- `docs/media-search-queries.md` — 62 consultas descriptivas + criterios de rechazo y evaluación.
- `docs/xaru-original-production-shot-list.md` — 41 tomas corporativas priorizadas.
- `docs/media-license-manifest.csv` — manifiesto vacío con las 33 columnas obligatorias, listo para poblarse.
- `assets/media/**` — estructura de carpetas creada, con `incoming/` a la espera de originales.

**Ningún archivo de imagen del sitio ha sido modificado ni borrado.** El diseño y la web en producción permanecen intactos.
