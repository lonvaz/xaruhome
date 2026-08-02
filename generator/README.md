# Generador de XARU HOME

El sitio publicado es HTML estático, pero **no se edita a mano**: se genera
desde aquí. Hasta la auditoría del 2026-08-02 estos ficheros vivían fuera del
repositorio, lo que hacía el build irreproducible para cualquiera que no
tuviera el entorno de trabajo original (CURRENT_STATE.md §2, Sev-1).

## Ejecutar

Desde el directorio que contiene estos módulos:

    python3 gen_i18n.py

Reescribe las 197 páginas de los cuatro idiomas, el sitemap y `llms.txt`. Es
idempotente: dos ejecuciones seguidas producen el mismo árbol.

## Qué hay aquí

| Fichero | Responsabilidad |
|---|---|
| `gen_i18n.py` | orquestador: plantillas, i18n, catálogo, fichas, SEO, sitemap |
| `arch_data.py` | arquitectura de navegación, puertas y páginas pilar |
| `page_dicts.py` | textos por página y sus pares de traducción |
| `seo_meta.py` | title/description/OG/JSON-LD y entradas del sitemap |
| `f2_copy.py` … `f5_articles.py` | copy de las fases 2 a 5 |
| `catalog_*.py` | especificación, geografía y construcción del catálogo demo |

## Dependencias

Python 3.11 y Pillow. Nada más: no hay servidor, base de datos ni bundler.

## Aviso

`gen_i18n.py` reescribe en su sitio las páginas del conjunto `TRANSLATED`
(portada, listados, contacto, faq…). Esos ficheros son a la vez fuente y
salida: editarlos a mano es legítimo, pero el cambio debe sobrevivir a una
regeneración. Todo lo demás se escribe desde cero en cada ejecución.
