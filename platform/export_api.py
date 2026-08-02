# -*- coding: utf-8 -*-
"""Publica la base de datos como API estática.

En modo simulación no hay servidor: las respuestas de la API se escriben como
ficheros JSON con **exactamente la forma que tendrá la API real** (§10 de la
biblia). El frontend consume `/data/api/v1/...` hoy y `https://api.xaruhome.com
/api/v1/...` el día que exista el backend, cambiando una constante.

Salidas:
    data/api/v1/meta.json              taxonomías, amenidades, monedas
    data/api/v1/locations.json         árbol geográfico con conteos
    data/api/v1/search-index.json      proyección ligera para la búsqueda
    data/api/v1/listings/{public_id}.json  ficha completa
    data/api/v1/listings/{ref_heredada}.json  alias del catálogo antiguo
    data/api/v1/agents.json            directorio de agentes
    data/api/v1/agencies.json          directorio de agencias
    data/api/v1/projects.json          proyectos off-plan
    data/api/v1/stats.json             contadores para la portada

Y, por compatibilidad con las páginas que ya existen:
    data/properties/{categoria}.json   forma heredada del catálogo
"""
import json, os, sqlite3, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from geo_world import WORLD  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(HERE, "xaru.db")
API = os.path.join(ROOT, "data", "api", "v1")
LOCALES = ("en", "es", "ar", "zh")


def w(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
    return os.path.getsize(path)


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    total = 0

    # ---------------------------------------------------------- meta
    types = [dict(r) for r in cur.execute(
        "SELECT slug, business_category, name_en, name_es, name_ar, name_zh "
        "FROM property_types WHERE is_active=1 ORDER BY sort_order")]
    amen = [dict(r) for r in cur.execute(
        "SELECT slug, category, name_en, name_es, name_ar, name_zh "
        "FROM amenities WHERE is_active=1 ORDER BY sort_order")]
    total += w(os.path.join(API, "meta.json"), {
        "version": "v1", "mode": "simulation",
        "notice": {
            "en": "Platform demo inventory. Records are test data of the XARU HOME platform.",
            "es": "Inventario de muestra de la plataforma. Los registros son datos de prueba de XARU HOME.",
            "ar": "مخزون تجريبي للمنصة. السجلات بيانات اختبارية لمنصة XARU HOME.",
            "zh": "平台演示资产。记录为 XARU HOME 平台的测试数据。",
        },
        "propertyTypes": types, "amenities": amen,
        "offeringTypes": ["sale", "rent"],
        "businessCategories": ["residential", "commercial", "land"],
        "currencies": ["USD", "EUR", "AED", "GBP"],
    })

    # ---------------------------------------------------------- geografía
    countries = []
    # El cursor se materializa antes de entrar al bucle: reutilizar el mismo
    # cursor dentro reinicia la iteracion y solo salia el primer pais. Lo mismo
    # ocurria con los proyectos. Un fallo silencioso: el fichero se escribia
    # bien formado, con un unico registro dentro.
    _countries = [r for r in cur.execute(
        "SELECT * FROM locations WHERE level='country' AND listing_count>0 "
        "ORDER BY listing_count DESC, name_en")]
    for r in _countries:
        cities = [{"id": c["id"], "slug": c["slug"], "name": c["name_en"],
                   "lat": c["latitude"], "lon": c["longitude"], "count": c["listing_count"]}
                  for c in cur.execute("SELECT * FROM locations WHERE parent_id=? AND listing_count>0 "
                                       "ORDER BY listing_count DESC", (r["id"],))]
        countries.append({"id": r["id"], "code": r["country_code"], "slug": r["slug"],
                          "name": {"en": r["name_en"], "es": r["name_es"],
                                   "ar": r["name_ar"], "zh": r["name_zh"]},
                          "count": r["listing_count"], "cities": cities})
    total += w(os.path.join(API, "locations.json"), {"countries": countries})

    # ---------------------------------------------------------- índice de búsqueda
    tr = {}
    for r in cur.execute("SELECT listing_id, locale, title FROM listing_translations"):
        tr.setdefault(r["listing_id"], {})[r["locale"]] = r["title"]
    amen_by_listing = {}
    for r in cur.execute("SELECT listing_id, amenity_id FROM listing_amenities"):
        amen_by_listing.setdefault(r["listing_id"], []).append(r["amenity_id"][3:])
    media = {r["id"]: r["storage_key"] for r in cur.execute("SELECT id, storage_key FROM media")}
    tname = {r["id"]: dict(r) for r in cur.execute("SELECT * FROM property_types")}
    agents = {r["id"]: dict(r) for r in cur.execute("SELECT * FROM agents")}
    orgs = {r["id"]: dict(r) for r in cur.execute("SELECT * FROM organizations")}

    rows = [dict(r) for r in cur.execute("SELECT * FROM v_public_listings")]
    index = []
    for r in rows:
        pt = tname.get(r["property_type_id"], {})
        ag = agents.get(r["agent_id"]) or {}
        og = orgs.get(r["org_id"]) or {}
        index.append({
            "id": r["public_id"],
            "t": {l: (tr.get(r["id"], {}).get(l) or tr.get(r["id"], {}).get("en") or "") for l in LOCALES},
            "cat": r["business_category"], "off": r["offering_type"],
            "type": pt.get("slug"),
            "typeName": {l: pt.get("name_" + l) or pt.get("name_en") for l in LOCALES},
            "cc": r["country_code"], "city": r["city"],
            "lat": r["latitude"], "lon": r["longitude"],
            "bd": r["bedrooms"], "ba": r["bathrooms"],
            "area": r["built_area_sqm"], "plot": r["plot_area_sqm"], "ha": r["hectares"],
            "keys": r["hotel_keys"], "berths": r["berths"],
            "cur": r["currency"],
            "p": (r["price_minor"] // 100) if r["price_minor"] else None,
            "poa": bool(r["price_on_application"]),
            "freq": r["rent_frequency"],
            "ppa": (r["price_per_sqm_minor"] // 100) if r["price_per_sqm_minor"] else None,
            "comp": r["completion_status"], "ver": r["verification_status"] == "verified",
            "q": r["quality_score"], "promo": r["promotion_tier"],
            "img": media.get(r["hero_media_id"], ""),
            "pub": r["published_at"], "st": r["lifecycle_status"],
            "am": amen_by_listing.get(r["id"], []),
            "ag": ag.get("slug"), "agName": ag.get("display_name"),
            "og": og.get("slug"), "ogName": og.get("trade_name"),
            "demo": bool(r["is_demo"]),
        })
    index.sort(key=lambda x: (x["promo"] != "featured", -(x["q"] or 0)))
    total += w(os.path.join(API, "search-index.json"),
               {"count": len(index), "mode": "simulation", "items": index})

    # ---------------------------------------------------------- directorios
    ags = []
    for a in agents.values():
        n = cur.execute("SELECT COUNT(*) FROM listings WHERE agent_id=? AND lifecycle_status='PUBLISHED'",
                        (a["id"],)).fetchone()[0]
        og = orgs.get(a["org_id"]) or {}
        ags.append({"slug": a["slug"], "name": a["display_name"], "title": a["job_title"],
                    "languages": (a["languages"] or "").split(","), "agency": og.get("trade_name"),
                    "agencySlug": og.get("slug"), "licence": a["licence_number"],
                    "verified": a["verification_status"] == "verified", "listings": n,
                    "phone": a["phone"], "whatsapp": a["whatsapp"], "email": a["email"],
                    "photo": media.get(a["photo_media_id"], ""),
                    "bio": a["bio"],
                    "specialities": (a["specialities"] or "").split(",") if a["specialities"] else [],
                    "serviceAreas": (a["service_areas"] or "").split(",") if a["service_areas"] else [],
                    "responseMinutes": a["response_minutes_p50"],
                    "rating": a["rating_avg"], "ratingCount": a["rating_count"],
                    "demo": bool(a["is_demo"])})
    total += w(os.path.join(API, "agents.json"), {"count": len(ags), "items": ags})

    ogs = []
    for o in orgs.values():
        if o["kind"] not in ("agency", "developer"):
            continue
        n = cur.execute("SELECT COUNT(*) FROM listings WHERE org_id=? AND lifecycle_status='PUBLISHED'",
                        (o["id"],)).fetchone()[0]
        ogs.append({"slug": o["slug"], "name": o["trade_name"], "legalName": o["legal_name"],
                    "kind": o["kind"], "country": o["country_code"], "city": o["city"],
                    "licence": o["licence_number"], "verified": o["verification_status"] == "verified",
                    "listings": n, "website": o["website"], "phone": o["phone"],
                    "email": o["email"], "description": o["description"],
                    "plan": o["plan_code"], "quota": o["listing_quota"],
                    "demo": bool(o["is_demo"])})
    total += w(os.path.join(API, "agencies.json"), {"count": len(ogs), "items": ogs})

    # Etiquetas de hito y nombres de tipo de unidad en los cuatro idiomas. La
    # base guarda la version del promotor; aqui se traduce lo que es vocabulario
    # comun del sector. Lo que no esta en la tabla se deja tal cual llego.
    MILE_L = {
        "reservation":         {"en": "Reservation", "es": "Reserva",
                                "ar": "الحجز", "zh": "预订"},
        "during construction": {"en": "During construction", "es": "Durante la obra",
                                "ar": "أثناء الإنشاء", "zh": "施工期间"},
        "on handover":         {"en": "On handover", "es": "En la entrega",
                                "ar": "عند التسليم", "zh": "交付时"},
        "post-handover":       {"en": "Post-handover", "es": "Tras la entrega",
                                "ar": "بعد التسليم", "zh": "交付后"},
    }
    UNIT_L = {
        "studio":    {"en": "Studio", "es": "Estudio", "ar": "استوديو", "zh": "开间"},
        "1 bedroom": {"en": "1 bedroom", "es": "1 dormitorio", "ar": "غرفة نوم واحدة", "zh": "一居"},
        "2 bedroom": {"en": "2 bedroom", "es": "2 dormitorios", "ar": "غرفتا نوم", "zh": "两居"},
        "3 bedroom": {"en": "3 bedroom", "es": "3 dormitorios", "ar": "ثلاث غرف نوم", "zh": "三居"},
        "4 bedroom": {"en": "4 bedroom", "es": "4 dormitorios", "ar": "أربع غرف نوم", "zh": "四居"},
        "penthouse": {"en": "Penthouse", "es": "Ático", "ar": "بنتهاوس", "zh": "顶层公寓"},
        "townhouse": {"en": "Townhouse", "es": "Adosado", "ar": "تاون هاوس", "zh": "联排别墅"},
        "villa":     {"en": "Villa", "es": "Villa", "ar": "فيلا", "zh": "别墅"},
    }

    def i18n(table, txt):
        d = table.get(str(txt or "").strip().lower())
        return d if d else {lo: txt for lo in LOCALES}

    prjs = []
    for p in [r for r in cur.execute("SELECT * FROM projects")]:
        d = cur.execute("SELECT name, slug FROM developers WHERE id=?", (p["developer_id"],)).fetchone()
        units = [dict(u) for u in cur.execute("SELECT * FROM unit_types WHERE project_id=?", (p["id"],))]
        plan = cur.execute("SELECT id, name FROM payment_plans WHERE project_id=?", (p["id"],)).fetchone()
        miles = [dict(m) for m in cur.execute(
            "SELECT label, percent, trigger_event FROM payment_plan_milestones WHERE plan_id=? "
            "ORDER BY sort_order", (plan["id"],))] if plan else []
        prjs.append({"slug": p["slug"], "name": p["name"], "status": p["status"],
                     "developer": d["name"] if d else None,
                     "developerSlug": d["slug"] if d else None,
                     "handover": {"quarter": p["handover_quarter"], "year": p["handover_year"]},
                     "progress": p["construction_progress_percent"],
                     "progressSource": p["progress_source"],
                     "priceFrom": (p["price_min_minor"] or 0) // 100,
                     "priceTo": (p["price_max_minor"] or 0) // 100,
                     "currency": p["currency"], "unitsTotal": p["units_total"],
                     "unitsAvailable": p["units_available"],
                     "unitTypes": [{"name": u["name"], "nameI18n": i18n(UNIT_L, u["name"]),
                                    "bedrooms": u["bedrooms"],
                                    "areaMin": u["area_min_sqm"], "areaMax": u["area_max_sqm"],
                                    "priceFrom": (u["price_min_minor"] or 0) // 100}
                                   for u in units],
                     "paymentPlan": {"name": plan["name"] if plan else None,
                                     "milestones": [dict(m, labelI18n=i18n(MILE_L, m["label"]))
                                                    for m in miles]},
                     "demo": bool(p["is_demo"])})
    total += w(os.path.join(API, "projects.json"), {"count": len(prjs), "items": prjs})

    # ---------------------------------------------------------- estadísticas
    def one(q, *a):
        return cur.execute(q, a).fetchone()[0]
    stats = {
        "listings": one("SELECT COUNT(*) FROM listings WHERE lifecycle_status='PUBLISHED'"),
        "countries": one("SELECT COUNT(*) FROM locations WHERE level='country' AND listing_count>0"),
        "cities": one("SELECT COUNT(*) FROM locations WHERE level='city' AND listing_count>0"),
        "agents": one("SELECT COUNT(*) FROM agents WHERE status='active'"),
        "agencies": one("SELECT COUNT(*) FROM organizations WHERE kind='agency'"),
        "developers": one("SELECT COUNT(*) FROM developers"),
        "projects": one("SELECT COUNT(*) FROM projects"),
        "leads": one("SELECT COUNT(*) FROM leads"),
        "forSale": one("SELECT COUNT(*) FROM listings WHERE offering_type='sale' AND lifecycle_status='PUBLISHED'"),
        "forRent": one("SELECT COUNT(*) FROM listings WHERE offering_type='rent' AND lifecycle_status='PUBLISHED'"),
        "residential": one("SELECT COUNT(*) FROM listings WHERE business_category='residential' AND lifecycle_status='PUBLISHED'"),
        "commercial": one("SELECT COUNT(*) FROM listings WHERE business_category='commercial' AND lifecycle_status='PUBLISHED'"),
        "land": one("SELECT COUNT(*) FROM listings WHERE business_category='land' AND lifecycle_status='PUBLISHED'"),
        "mode": "simulation",
    }
    total += w(os.path.join(API, "stats.json"), stats)

    # ---------------------------------------------------------- fichas
    nfich = 0
    nalias = 0
    country_names = {}
    for cc, v in WORLD.items():
        country_names[cc] = {"en": v[0], "es": v[1], "ar": v[2], "zh": v[3]}
    # La vista pública no expone `external_reference` —es dato interno—, así que
    # el alias se consulta aparte contra la tabla, sin tocar la frontera.
    legacy_ref = {r["id"]: r["external_reference"] for r in cur.execute(
        "SELECT id, external_reference FROM listings WHERE external_reference IS NOT NULL")}
    for r in rows:
        pt = tname.get(r["property_type_id"], {})
        ag = agents.get(r["agent_id"]) or {}
        og = orgs.get(r["org_id"]) or {}
        desc = {}
        for lo in LOCALES:
            row = cur.execute("SELECT description FROM listing_translations WHERE listing_id=? AND locale=?",
                              (r["id"], lo)).fetchone()
            if row and row["description"]:
                desc[lo] = row["description"]
        doc = {
            "publicId": r["public_id"], "mode": "simulation", "demo": bool(r["is_demo"]),
            "demoLabel": r["demo_label"],
            "title": {l: (tr.get(r["id"], {}).get(l) or "") for l in LOCALES},
            "description": desc,
            "businessCategory": r["business_category"], "offeringType": r["offering_type"],
            "inventoryType": r["inventory_type"],
            "propertyType": {"slug": pt.get("slug"),
                             "name": {l: pt.get("name_" + l) or pt.get("name_en") for l in LOCALES}},
            "location": {"countryCode": r["country_code"], "city": r["city"],
                         # El nombre del pais va en los cuatro idiomas; el de la
                         # ciudad no se traduce nunca —es la regla de la casa—,
                         # asi que la direccion se compone en el cliente.
                         "country": country_names.get(r["country_code"], {}),
                         "displayAddress": r["public_display_address"],
                         "precision": r["location_precision"],
                         "lat": r["latitude"], "lon": r["longitude"]},
            "spaces": {"bedrooms": r["bedrooms"], "bathrooms": r["bathrooms"],
                       "parking": r["parking_spaces"], "builtAreaSqm": r["built_area_sqm"],
                       "plotAreaSqm": r["plot_area_sqm"], "hectares": r["hectares"],
                       "hotelKeys": r["hotel_keys"], "berths": r["berths"]},
            "price": {"currency": r["currency"],
                      "amount": (r["price_minor"] // 100) if r["price_minor"] else None,
                      "onApplication": bool(r["price_on_application"]),
                      "frequency": r["rent_frequency"],
                      "perSqm": (r["price_per_sqm_minor"] // 100) if r["price_per_sqm_minor"] else None},
            "condition": {"furnishing": r["furnishing"], "completion": r["completion_status"],
                          "ownership": r["ownership_type"],
                          "handover": {"quarter": r["handover_quarter"], "year": r["handover_year"]}},
            "amenities": amen_by_listing.get(r["id"], []),
            "media": [{"kind": "photo", "url": media.get(r["hero_media_id"], "")}],
            "trust": {"verified": r["verification_status"] == "verified",
                      "qualityScore": r["quality_score"], "promotion": r["promotion_tier"]},
            "agent": {"slug": ag.get("slug"), "name": ag.get("display_name"),
                      "licence": ag.get("licence_number"),
                      "verified": ag.get("verification_status") == "verified"},
            "agency": {"slug": og.get("slug"), "name": og.get("trade_name"),
                       "licence": og.get("licence_number")},
            "status": r["lifecycle_status"],
            "publishedAt": r["published_at"], "updatedAt": r["updated_at"],
        }
        total += w(os.path.join(API, "listings", r["public_id"] + ".json"), doc)
        nfich += 1
        # Alias por referencia heredada: los enlaces del catálogo antiguo
        # (pp-samana-island, pr-villas-tropical…) siguen resolviendo. Un
        # identificador publicado no se retira nunca; se le da destino.
        ext = legacy_ref.get(r["id"])
        if ext and ext != r["public_id"] and not str(ext).startswith("XH-"):
            total += w(os.path.join(API, "listings", str(ext) + ".json"), doc)
            nalias += 1

    con.close()
    print("API estática escrita en data/api/v1/")
    print("  listings en índice : %d" % len(index))
    print("  fichas             : %d" % nfich)
    print("  alias heredados    : %d" % nalias)
    print("  países con stock   : %d" % stats["countries"])
    print("  ciudades con stock : %d" % stats["cities"])
    print("  peso total         : %.1f MB" % (total / 1048576.0))


if __name__ == "__main__":
    main()
