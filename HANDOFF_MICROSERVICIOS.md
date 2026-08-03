# XARU HOME — cómo enganchar los microservicios

Este documento es para el equipo que va a poner backend real detrás del portal.
Dice exactamente qué hay hoy, dónde están las costuras y en qué orden conviene
sustituirlas. No hay que leer todo el código: hay que tocar nueve constantes y
una función.

---

## La idea en un párrafo

El portal ya está construido **como si el backend existiera**. No consulta una
base de datos ni tiene lógica de negocio dentro: consume una API REST versionada
en `/data/api/v1/`. Lo que pasa es que hoy esa API son ficheros JSON servidos
por el mismo CDN que el sitio. La **forma** de los datos es la definitiva, no la
de un apaño. Por eso migrar no es reescribir el front: es cambiar la URL base.

El contrato está en `data/api/openapi.json` (OpenAPI 3.1) y **se genera de los
payloads reales**, no se escribe a mano:

```bash
python3 platform/gen_openapi.py
```

Si al regenerarlo el diff no está vacío, es que ha cambiado el contrato. Eso es
justo lo que se quiere ver en una revisión.

---

## Qué endpoints hay que servir

| Ruta | Qué es | Quién lo consume |
|---|---|---|
| `GET /meta.json` | Taxonomías: tipos, amenidades, categorías, monedas, anchos de imagen | Todas las vistas |
| `GET /locations.json` | Países y ciudades con inventario y recuento | Buscador, selectores |
| `GET /search-index.json` | Índice completo del inventario publicado (841 KB, 911 registros) | Marketplace, ficha, directorios, consolas |
| `GET /listings/{publicId}.json` | Ficha completa de un activo | Página de detalle |
| `GET /agents.json` | Directorio de asesores | Directorios |
| `GET /agencies.json` | Directorio de agencias | Directorios |
| `GET /projects.json` | Promociones sobre plano | Directorios, obra nueva |
| `GET /market.json` | Medianas por ciudad, país, tipología y categoría | Bloque de precios y tendencias |
| `GET /stats.json` | Contadores globales | Portada de Real Estate |
| `GET /b2b.json` | Embudo profesional por etapa | Panel B2B |
| `GET /admin.json` | Cola de revisión, estados y transiciones | Consola de operación |

Las formas exactas, con campos obligatorios y opcionales, están en el OpenAPI.
Merece la pena mirarlo antes de implementar: el generador fusiona cien fichas
reales, así que distingue lo que viene siempre de lo que viene a veces. Por
ejemplo `priceDropPercent` es opcional, y once de los cuarenta y dos campos del
índice de búsqueda tampoco están en todos los registros.

---

## Las costuras: qué se toca y qué no

### 1. La URL base — nueve constantes, una por módulo

```
assets/js/xaru-account.js:26          var API = R + "data/api/v1/";
assets/js/xaru-console.js:32          var API = R + "data/api/v1/";
assets/js/xaru-directory.js:25        var API = R + "data/api/v1/";
assets/js/xaru-marketplace.js:32      var API = "data/api/v1/";
assets/js/xaru-mp-home.js:24          var API = R + "data/api/v1/";
assets/js/xaru-projects.js:24         var API = R + "data/api/v1/";
assets/js/xaru-property-detail.js:36  var API = R + "data/api/v1/";
```

Apuntándolas a `https://api.xaruhome.com/v1/` y sirviendo el mismo contrato, el
portal funciona contra el backend real sin tocar una línea más. Recomendación:
sustituirlas por una única constante global inyectada en la plantilla, para no
tener que editar siete ficheros cada vez.

### 2. La búsqueda — **una sola función**

Hoy el front se descarga `search-index.json` entero y filtra en memoria. Todo
ese filtrado vive en un único sitio:

```
assets/js/xaru-marketplace.js  ->  function query(state, items)
```

Está marcada en el código con el comentario que dice que es la única función que
cambia. Recibe el estado de la búsqueda y devuelve la lista filtrada. El día que
exista el Search Service pasa a ser:

```js
fetch(API + "search/listings", {method: "POST", body: JSON.stringify(state)})
```

El `state` ya viaja en la URL con nombres estables (`type`, `cc`, `city`, `am`,
`bedsMin`, `priceMax`, `offering`, `category`, `sort`, `page`…), así que sirve
tal cual como cuerpo de la petición. **Ese contrato de filtros ya está probado
en producción por las URL compartibles del portal**: cualquier búsqueda que hoy
funcione en el navegador es una petición válida para el servicio.

Ojo con dos cosas que hoy resuelve el front y tendrá que resolver el servicio:

- las **facetas con recuento** (`paintTypes`) se calculan excluyendo el propio
  filtro de tipología, que es como debe comportarse una faceta;
- el **orden** (`sortItems`) incluye "recomendados", que no es un campo sino una
  combinación de promoción, verificación y antigüedad.

### 3. La escritura — hoy no existe

Favoritos, vistos recientemente e idioma van a `localStorage` a través de un
adaptador llamado `Store`, presente en el marketplace y en la ficha. Las claves
son `xaru_favorites`, `xaru_viewed` y `xaru_lang`. Ese adaptador es el hueco
donde entra el Engagement Service cuando haya cuentas de usuario: mismo interfaz,
otra implementación.

### 4. El origen del dato

```
platform/schema.sql       DDL portable a PostgreSQL
platform/xaru.db          SQLite con el inventario de muestra
platform/export_api.py    vuelca la base a los JSON de /data/api/v1
```

`schema.sql` está escrito para migrar a PostgreSQL sin reescribirlo. El día que
el inventario viva en la base real, `export_api.py` deja de usarse y su papel lo
hacen los servicios. Mientras tanto es la referencia de qué tabla alimenta qué
campo del contrato.

**El inventario actual es de muestra y está marcado como tal.** Cada registro
lleva `demo: true` y el portal lo enseña con su etiqueta. No es decorativo: es
lo que separa "esto es una demostración de plataforma" de "esto es un anuncio
inmobiliario real", y con las normas de publicidad inmobiliaria de EAU y de la
UE esa diferencia tiene consecuencias legales. Cuando entre inventario real,
entra con `demo: false` y la etiqueta desaparece sola.

---

## Orden recomendado de migración

1. **Catálogo maestro** (`meta`, `locations`). Son pequeños, casi estáticos y no
   rompen nada si fallan: el front ya los trata como opcionales.
2. **Ficha** (`listings/{id}`). Endpoint sencillo por clave primaria, y valida
   el modelo de datos completo de una sola vez.
3. **Búsqueda** (`POST /search/listings`). Es el trabajo de verdad: facetas,
   orden y paginación. Hasta que esté, el índice estático sigue sirviendo.
4. **Directorios y estadística** (`agents`, `agencies`, `projects`, `market`,
   `stats`).
5. **Consolas** (`b2b`, `admin`) y con ellas la escritura y las cuentas.

Cada paso es independiente: se puede tener la ficha en el servicio real mientras
la búsqueda sigue contra el índice estático. El front no se entera.

---

## Cómo levantar el proyecto

```bash
git clone https://github.com/lonvaz/xaruhome.git
cd xaruhome
python3 -m pip install pillow numpy opencv-python scipy
cd generator && python3 gen_i18n.py      # reconstruye las 409 páginas
cd .. && python3 -m http.server 8899     # y se abre en localhost:8899
```

El generador es **idempotente**: compilar dos veces seguidas produce ficheros
byte a byte idénticos. Si un diff aparece de la nada, es un fallo real, no ruido.

Para regenerar la API desde la base de muestra:

```bash
python3 platform/export_api.py
python3 platform/gen_openapi.py
```

---

## Qué NO tocar sin hablarlo

- **La etiqueta de inventario de muestra.** Ver arriba: no es cosmética.
- **Los topónimos.** Los nombres de lugar no cambian entre los cuatro idiomas, a
  propósito: un activo en Marbella se llama Marbella también en árabe y en chino.
- **La idempotencia del generador.** La portada no se genera de cero, se parchea
  sobre sí misma. Cualquier parche nuevo tiene que poder aplicarse dos veces sin
  duplicar nada. Ya pasó una vez: se acumularon 110 copias del mismo listener y
  112 atributos repetidos antes de que nadie lo notara.
