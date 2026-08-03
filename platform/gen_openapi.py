# -*- coding: utf-8 -*-
"""Genera el contrato OpenAPI a partir de los payloads REALES de data/api/v1.

POR QUE GENERADO Y NO ESCRITO A MANO
------------------------------------
Un contrato escrito a mano se desincroniza del dato a la primera semana y
entonces es peor que no tenerlo: el equipo de microservicios implementa contra
un papel y el front espera otra cosa. Aqui el esquema se infiere de los ficheros
que el front consume HOY, asi que por construccion describe lo que de verdad
circula. Se regenera con:

    python3 platform/gen_openapi.py

y si el resultado cambia, es que ha cambiado el contrato: eso es exactamente lo
que se quiere ver en un diff.

QUE ES ESTA API
---------------
Hoy es estatica: ficheros JSON servidos por el mismo CDN que el sitio. Pero su
FORMA es la del servicio que vendra detras, no la de un apaño. El dia que exista
el backend real, el front no cambia de contrato: cambia la base de la URL y, en
el caso de la busqueda, una unica funcion —query() en xaru-marketplace.js— pasa
de filtrar en memoria a hacer POST. Esa costura esta marcada en el codigo.
"""
import json
import os
import glob
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
API = os.path.join(ROOT, 'data', 'api', 'v1')
OUT = os.path.join(ROOT, 'data', 'api', 'openapi.json')

DESCRIPCIONES = {
    'meta.json': ('Taxonomias y catalogos maestros',
                  'Tipos de propiedad, amenidades, categorias de negocio, monedas y los anchos '
                  'de imagen disponibles por fichero. Es lo primero que carga cualquier vista.'),
    'locations.json': ('Arbol geografico',
                       'Paises y ciudades con inventario, con su recuento. Alimenta los selectores '
                       'y el autocompletado jerarquico.'),
    'search-index.json': ('Indice de busqueda',
                          'Todo el inventario publicado en forma compacta. Hoy el front lo descarga '
                          'entero y filtra en memoria; manana este endpoint desaparece y lo sustituye '
                          'POST /search/listings.'),
    'listings/{id}.json': ('Ficha completa de un activo',
                           'Todo lo que necesita la pagina de detalle: precio e historico, medios, '
                           'espacios, amenidades, asesor, agencia y estado.'),
    'agents.json': ('Directorio de asesores', 'Perfil publico y cartera de cada asesor.'),
    'agencies.json': ('Directorio de agencias', 'Oficinas y su inventario asociado.'),
    'projects.json': ('Promociones sobre plano', 'Proyectos en desarrollo con sus unidades.'),
    'market.json': ('Estadistica de mercado',
                    'Medianas de precio por ciudad, pais, tipologia y categoria. Alimenta los '
                    'bloques de precios y tendencias de la ficha.'),
    'stats.json': ('Contadores globales', 'Totales de inventario, geografia y red comercial.'),
    'b2b.json': ('Embudo profesional', 'Oportunidades por etapa para el panel B2B.'),
    'admin.json': ('Consola de operacion',
                   'Cola de revision, estados del ciclo de vida y transiciones permitidas. '
                   'Solo lectura mientras la plataforma este en simulacion.'),
}


def esquema(v, prof=0):
    """Infiere el esquema de un valor. En listas mira varios elementos, no solo
    el primero: si el primer anuncio no trae plano y el septimo si, el contrato
    debe recogerlo o el equipo implementa un campo de menos."""
    if v is None:
        return {'nullable': True}
    if isinstance(v, bool):
        return {'type': 'boolean'}
    if isinstance(v, int):
        return {'type': 'integer'}
    if isinstance(v, float):
        return {'type': 'number'}
    if isinstance(v, str):
        return {'type': 'string'}
    if isinstance(v, list):
        if not v:
            return {'type': 'array', 'items': {}}
        return {'type': 'array', 'items': fusiona([esquema(x, prof + 1) for x in v[:60]])}
    if isinstance(v, dict):
        # Un diccionario con muchas claves y valores homogeneos NO es un objeto
        # con esos campos: es un mapa indexado por clave —anchos de imagen por
        # fichero, medianas por ciudad—. Enumerar sus claves engorda el contrato
        # (181 KB en la primera version) y ademas miente: manana habra otras
        # ciudades y otras imagenes, y el contrato seguiria siendo el mismo.
        if len(v) > 12:
            hijos = [esquema(x, prof + 1) for x in list(v.values())[:60]]
            tipos = {json.dumps(h, sort_keys=True) for h in hijos}
            if len(tipos) <= 3:
                return {'type': 'object', 'additionalProperties': fusiona(hijos),
                        'description': 'Mapa indexado por clave (%d entradas en el volcado actual)' % len(v)}
        props = OrderedDict((k, esquema(x, prof + 1)) for k, x in v.items())
        return {'type': 'object', 'properties': props,
                'required': [k for k, x in v.items() if x is not None]}
    return {}


def fusiona(esquemas):
    """Une los esquemas de varios elementos de una lista. Un campo que no aparece
    en todos deja de ser obligatorio; eso es informacion, no ruido."""
    if not esquemas:
        return {}
    tipos = {e.get('type') for e in esquemas if e.get('type')}
    if len(tipos) > 1:
        return {'oneOf': [{'type': t} for t in sorted(tipos)]}
    base = dict(esquemas[0])
    if base.get('type') == 'object':
        props = OrderedDict()
        req = None
        for e in esquemas:
            for k, s in (e.get('properties') or {}).items():
                props.setdefault(k, s)
            r = set(e.get('required') or [])
            req = r if req is None else (req & r)
        base['properties'] = props
        base['required'] = sorted(req or [])
    elif base.get('type') == 'array':
        base['items'] = fusiona([e.get('items', {}) for e in esquemas if e.get('items')])
    return base


def main():
    rutas = OrderedDict()
    ficheros = ['meta.json', 'locations.json', 'search-index.json', 'agents.json',
                'agencies.json', 'projects.json', 'market.json', 'stats.json',
                'b2b.json', 'admin.json']
    for f in ficheros:
        p = os.path.join(API, f)
        if not os.path.exists(p):
            continue
        titulo, desc = DESCRIPCIONES.get(f, (f, ''))
        rutas['/' + f] = {
            'get': {
                'summary': titulo, 'description': desc,
                'operationId': f.replace('.json', '').replace('-', '_'),
                'responses': {'200': {
                    'description': titulo,
                    'content': {'application/json': {
                        'schema': esquema(json.load(open(p, encoding='utf-8')))}}}}}}

    fichas = sorted(glob.glob(os.path.join(API, 'listings', '*.json')))
    if fichas:
        # Se fusionan cien fichas: una sola no revela los campos opcionales.
        muestras = [esquema(json.load(open(x, encoding='utf-8'))) for x in fichas[:100]]
        titulo, desc = DESCRIPCIONES['listings/{id}.json']
        rutas['/listings/{publicId}.json'] = {
            'get': {
                'summary': titulo, 'description': desc, 'operationId': 'listing',
                'parameters': [{'name': 'publicId', 'in': 'path', 'required': True,
                                'schema': {'type': 'string'},
                                'description': 'Identificador publico del activo'}],
                'responses': {'200': {'description': titulo,
                                      'content': {'application/json': {'schema': fusiona(muestras)}}},
                              '404': {'description': 'No existe o no esta publicado'}}}}

    doc = {
        'openapi': '3.1.0',
        'info': {
            'title': 'XARU HOME — API de inventario',
            'version': '1.0.0',
            'description': (
                'Contrato de datos del portal XARU HOME.\n\n'
                'Hoy se sirve como ficheros JSON estaticos desde el mismo CDN que el sitio. '
                'La FORMA es la del servicio definitivo, no la de un apaño: cuando existan los '
                'microservicios, el front no cambia de contrato, solo de URL base.\n\n'
                'La unica excepcion es la busqueda. Hoy el front descarga search-index.json '
                'entero y filtra en memoria dentro de query(), en assets/js/xaru-marketplace.js. '
                'Ese es el punto exacto —y el unico— que pasa a ser POST /search/listings.\n\n'
                'Este documento se GENERA de los payloads reales con '
                'platform/gen_openapi.py. No se edita a mano.'),
        },
        'servers': [
            {'url': 'https://xaruhome.com/data/api/v1', 'description': 'Hoy: estatico sobre CDN'},
            {'url': 'https://api.xaruhome.com/v1', 'description': 'Manana: microservicios'},
        ],
        'paths': rutas,
    }
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    print('%s  ->  %.0f KB, %d rutas' % (OUT, os.path.getsize(OUT) / 1024, len(rutas)))


if __name__ == '__main__':
    main()
