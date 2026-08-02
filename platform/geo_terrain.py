# -*- coding: utf-8 -*-
"""Coherencia entre tipología y territorio.

Un portal se juzga por sus disparates. Una isla privada en Quito, un puerto
deportivo en Madrid o un chalet de montaña en Miami destruyen la credibilidad
de todo el inventario que hay alrededor, por bien fotografiado que esté. Este
módulo evita que el sembrador pueda producirlos.

COSTA
-----
`COASTAL` se calcula una sola vez con `global_land_mask` (máscara de tierra a
1/100 de grado): se muestrean tres anillos de puntos alrededor de cada ciudad y
si alguno cae en el mar, la ciudad es costera. De las 293 ciudades del árbol
geográfico, 186 lo son. El cálculo se congela aquí como dato para que sembrar
no dependa de tener el paquete instalado, y para que el resultado sea
reproducible.

MONTAÑA
-------
`MOUNTAIN` es una lista curada: las plazas donde un chalet es lo que se espera
encontrar. No se deriva de altitud porque la altitud sola no distingue una
estación de esquí de una meseta.

Regenerar la tabla de costa:
    python3 platform/geo_terrain.py --recompute
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Ciudades donde un chalet, un refugio o una residencia de estación de esquí
# es la tipología natural. Curada, no derivada.
MOUNTAIN = {
    ("CH", "Zurich"), ("CH", "Geneva"), ("CH", "Zermatt"), ("CH", "St. Moritz"),
    ("CH", "Verbier"), ("CH", "Gstaad"), ("CH", "Davos"), ("CH", "Lausanne"),
    ("AT", "Innsbruck"), ("AT", "Kitzbuhel"), ("AT", "Kitzbühel"), ("AT", "Salzburg"),
    ("FR", "Chamonix"), ("FR", "Courchevel"), ("FR", "Megeve"), ("FR", "Megève"),
    ("FR", "Val d'Isere"), ("FR", "Annecy"), ("FR", "Grenoble"),
    ("IT", "Cortina d'Ampezzo"), ("IT", "Courmayeur"), ("IT", "Bolzano"), ("IT", "Aosta"),
    ("AD", "Andorra la Vella"), ("ES", "Baqueira"), ("ES", "Sierra Nevada"),
    ("SI", "Bled"), ("SI", "Kranjska Gora"),
    ("US", "Aspen"), ("US", "Vail"), ("US", "Park City"), ("US", "Jackson"),
    ("US", "Telluride"), ("US", "Lake Tahoe"), ("US", "Denver"),
    ("CA", "Whistler"), ("CA", "Banff"), ("CA", "Calgary"),
    ("AR", "Bariloche"), ("AR", "Mendoza"), ("CL", "Portillo"), ("CL", "Santiago"),
    ("NZ", "Queenstown"), ("NZ", "Wanaka"),
    ("JP", "Niseko"), ("JP", "Hakuba"), ("JP", "Nagano"),
    ("NP", "Kathmandu"), ("NP", "Pokhara"), ("BT", "Thimphu"),
    ("IN", "Shimla"), ("IN", "Manali"), ("IN", "Srinagar"),
    ("PL", "Zakopane"), ("BG", "Bansko"), ("GE", "Gudauri"), ("GE", "Tbilisi"),
    ("PE", "Cusco"), ("BO", "La Paz"), ("EC", "Quito"), ("CO", "Bogota"), ("CO", "Bogotá"),
    ("MA", "Ifrane"), ("LB", "Faraya"), ("TR", "Bursa"), ("TR", "Erzurum"),
    ("NO", "Lillehammer"), ("SE", "Are"), ("SE", "Åre"), ("FI", "Levi"),
    ("DE", "Garmisch-Partenkirchen"), ("DE", "Munich"),
}


def _recompute():
    """Recalcula el conjunto costero y reescribe la constante de este fichero."""
    import math
    from global_land_mask import globe
    sys.path.insert(0, HERE)
    from geo_world import WORLD

    def is_coastal(lat, lon, km=30):
        for r in (10, 20, km):
            dlat = r / 111.0
            dlon = r / (111.0 * max(0.15, math.cos(math.radians(lat))))
            for i in range(16):
                a = 2 * math.pi * i / 16
                y, x = lat + dlat * math.sin(a), lon + dlon * math.cos(a)
                if abs(y) > 89:
                    continue
                try:
                    if globe.is_ocean(y, ((x + 180) % 360) - 180):
                        return True
                except Exception:
                    pass
        return False

    out = sorted((cc, city) for cc, v in WORLD.items()
                 for (city, lat, lon) in v[5] if is_coastal(lat, lon))
    lines = ["COASTAL = {"]
    for cc, city in out:
        lines.append('    (%r, %r),' % (cc, city))
    lines.append("}")
    print("\n".join(lines))
    print("\n# %d ciudades costeras de %d" %
          (len(out), sum(len(v[5]) for v in WORLD.values())), file=sys.stderr)


# --- generado por --recompute (global_land_mask, 186/293) --------------------
COASTAL = set()


def load_coastal():
    """Devuelve el conjunto costero, calculándolo si el fichero de datos falta."""
    global COASTAL
    if COASTAL:
        return COASTAL
    path = os.path.join(HERE, "coastal_cities.json")
    if os.path.exists(path):
        import json
        COASTAL = set(tuple(x) for x in json.load(open(path, encoding="utf-8")))
    return COASTAL


# ---------------------------------------------------------------- tipologías
# Cada tipología declara el territorio que exige. `any` no exige nada.
COAST_ONLY = {
    "private-island", "waterfront-home", "marina",
    "coastal-land", "island-territory", "hotel-resort-land", "resort",
}
MOUNTAIN_ONLY = {"chalet"}
# Tipologías que piden espacio y no encajan en el centro de una capital.
RURAL_PREFERRED = {
    "estate", "hacienda", "equestrian", "castle", "agricultural-land",
    "forestry-land", "mining-concession", "quarry", "energy-land",
    "city-scale-land", "masterplan-land",
}
# Tipologías netamente urbanas: no se siembran en plazas de menos de peso.
URBAN_ONLY = {
    "whole-floor", "half-floor", "office", "business-centre", "coworking",
    "showroom", "urban-mixed-land",
}


# Tipologias con carga cultural: una hacienda en Kuala Lumpur o un castillo en
# Doha delatan que el inventario esta generado y no seleccionado. Cada una
# queda limitada a las regiones —y, cuando hace falta, a los paises— donde
# realmente existe.
REGION_ONLY = {
    "hacienda":   ({"South America", "Central America", "Caribbean"}, {"ES", "PT", "MX", "PH"}),
    "castle":     ({"Europe"}, {"MA", "JP", "IN"}),
    "chateau":    ({"Europe"}, set()),
    "compound":   ({"Middle East", "Africa"}, {"US", "MX", "BR", "IN", "PK", "ID"}),
    "equestrian": ({"Europe", "North America", "South America", "Middle East", "Oceania"}, set()),
    "riad":       (set(), {"MA", "TN", "DZ"}),
    "labour-camp":({"Middle East", "Asia"}, set()),
    "staff-accommodation": ({"Middle East", "Asia", "Africa"}, set()),
}


def region_ok(cc, region, tslug):
    """Es esta tipologia culturalmente creible en esta region?"""
    rule = REGION_ONLY.get(tslug)
    if not rule:
        return True
    regions, extra_cc = rule
    return region in regions or cc in extra_cc


def allowed(cc, city, tslug, tier, region=None):
    """¿Tiene sentido esta tipología en esta ciudad?"""
    if region is not None and not region_ok(cc, region, tslug):
        return False
    coastal = (cc, city) in load_coastal()
    mountain = (cc, city) in MOUNTAIN
    if tslug in COAST_ONLY:
        return coastal
    if tslug in MOUNTAIN_ONLY:
        return mountain
    if tslug in URBAN_ONLY:
        return tier >= 1.0
    return True


if __name__ == "__main__":
    if "--recompute" in sys.argv:
        _recompute()
    else:
        print("costeras cargadas:", len(load_coastal()), "| montaña:", len(MOUNTAIN))
