# Plataforma XARU HOME — modo simulación

Aquí vive la arquitectura de datos real de la plataforma inmobiliaria. No hay
servidor todavía: la base de datos es SQLite y la API se publica como ficheros
JSON estáticos. **La forma de los datos y de las respuestas es la definitiva**,
de modo que el día que se contraten PostgreSQL, Elasticsearch y el backend, se
cambia el origen y no el frontend.

## Piezas

| Fichero | Qué hace |
|---|---|
| `schema.sql` | esquema canónico: 30 tablas y una vista pública. SQL portable a PostgreSQL |
| `geo_world.py` | árbol geográfico: 130 países, 293 ciudades con coordenadas |
| `seed.py` | construye y llena `xaru.db` |
| `export_api.py` | publica la base de datos como API estática en `data/api/v1/` |

## Reconstruir todo

    python3 platform/seed.py        # base de datos desde cero
    python3 platform/export_api.py  # API estática

## Qué hay dentro

- 911 activos publicados en 130 países y 372 ciudades
- 48 tipologías: residencial, comercial y suelo — incluidas concesiones
  mineras, canteras, territorio de escala urbana, islas y castillos
- 48 amenidades administrables
- 6 agencias de prueba, 22 agentes de prueba, 12 compradores de prueba
- 5 promotoras con proyectos off-plan y planes de pago que suman 100 %
- 140 leads en las siete etapas del pipeline
- favoritos, búsquedas guardadas y alertas por comprador
- casos de moderación, ledger de créditos y suscripciones

## Inventario de muestra frente a inventario real

Todo lo sembrado lleva `is_demo = 1` y la etiqueta pública `PLATFORM DEMO`.
**No se borra nunca.** Cuando entre inventario real convivirán en la misma
tabla y el filtro por `is_demo` decide qué se publica. Ese es el camino de
muestra a producción: cargar lo real, no rehacer la plataforma.

## De simulación a producción

1. `schema.sql` se ejecuta sobre PostgreSQL (cambian los tipos marcados `-- PG:`).
2. `seed.py` deja de sembrar y se conserva sólo para entornos de prueba.
3. `export_api.py` se sustituye por los servicios reales; las rutas
   `/data/api/v1/...` pasan a `https://api.xaruhome.com/api/v1/...`.
4. El frontend cambia una constante de base URL. Nada más.
