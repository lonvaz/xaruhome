# -*- coding: utf-8 -*-
"""Construye data/properties/*.json desde catalog_spec + catalog_i18n (Biblia Visual V3 §10)."""
import json, os, re, unicodedata
import catalog_spec as S
import catalog_i18n as I
import catalog_geo as G

LANGS = ("en","es","ar","zh")
OUT = "xaru/data/properties"

def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii","ignore").decode()
    return re.sub(r"[^a-z0-9]+","-", t.lower()).strip("-")

def money(v): return f"USD {v:,.0f}".replace(",", ",")

# --- plantillas de descripción por categoría, en los 4 idiomas -------------
D = {
"contemporary-houses": I.T(
 "A contemporary house of {built} m² in {city}, {country}, on a plot of {land} m², with {beds} bedrooms.",
 "Casa contemporánea de {built} m² en {city}, {country}, sobre una parcela de {land} m², con {beds} dormitorios.",
 "منزل معاصر بمساحة {built} م² في {city}، {country}، على قطعة أرض {land} م²، ويضم {beds} غرف نوم.",
 "位于{country}·{city}的当代住宅，建筑面积 {built} 平方米，地块 {land} 平方米，{beds} 间卧室。"),
"branded-residences": I.T(
 "A branded residence of {built} m² in {city}, {country}, with {beds} bedrooms and full hotel service.",
 "Residencia de marca de {built} m² en {city}, {country}, con {beds} dormitorios y servicio hotelero completo.",
 "مسكن بعلامة تجارية بمساحة {built} م² في {city}، {country}، ويضم {beds} غرف نوم وخدمة فندقية كاملة.",
 "位于{country}·{city}的品牌住宅，建筑面积 {built} 平方米，{beds} 间卧室，配备完整酒店服务。"),
"city-apartments": I.T(
 "A luxury apartment of {built} m² in {city}, {country}, with {beds} bedrooms.",
 "Apartamento de lujo de {built} m² en {city}, {country}, con {beds} dormitorios.",
 "شقة فاخرة بمساحة {built} م² في {city}، {country}، وتضم {beds} غرف نوم.",
 "位于{country}·{city}的豪华公寓，建筑面积 {built} 平方米，{beds} 间卧室。"),
"villas": I.T(
 "A {built} m² villa in {city}, {country}, set on {land} m² of grounds, with {beds} bedrooms and {baths} bathrooms.",
 "Villa de {built} m² en {city}, {country}, sobre {land} m² de terreno, con {beds} dormitorios y {baths} baños.",
 "فيلا بمساحة {built} م² في {city}، {country}، على أرض {land} م²، بـ {beds} غرف نوم و{baths} حمامات.",
 "位于{country}·{city}的别墅，建筑面积 {built} 平方米，占地 {land} 平方米，{beds} 间卧室、{baths} 间浴室。"),
"mansions": I.T(
 "A principal residence of {built} m² in {city}, {country}, on {land} m², with {beds} bedrooms.",
 "Residencia principal de {built} m² en {city}, {country}, sobre {land} m², con {beds} dormitorios.",
 "مسكن رئيسي بمساحة {built} م² في {city}، {country}، على {land} م²، ويضم {beds} غرف نوم.",
 "位于{country}·{city}的主宅，建筑面积 {built} 平方米，占地 {land} 平方米，{beds} 间卧室。"),
"castles-chateaux": I.T(
 "A historic property of {built} m² in {city}, {country}, with {land_ha} hectares of land and {beds} bedrooms.",
 "Propiedad histórica de {built} m² en {city}, {country}, con {land_ha} hectáreas de terreno y {beds} dormitorios.",
 "عقار تاريخي بمساحة {built} م² في {city}، {country}، مع {land_ha} هكتاراً من الأرض و{beds} غرفة نوم.",
 "位于{country}·{city}的历史建筑，建筑面积 {built} 平方米，土地 {land_ha} 公顷，{beds} 间卧室。"),
"haciendas": I.T(
 "A working hacienda of {built} m² in {city}, {country}, with {land_ha} hectares of land.",
 "Hacienda en explotación de {built} m² en {city}, {country}, con {land_ha} hectáreas de terreno.",
 "حاسيندا عاملة بمساحة {built} م² في {city}، {country}، مع {land_ha} هكتاراً من الأرض.",
 "位于{country}·{city}的运营中庄园，建筑面积 {built} 平方米，土地 {land_ha} 公顷。"),
"estates": I.T(
 "An estate of {land_ha} hectares in {city}, {country}, with a principal house of {built} m².",
 "Finca de {land_ha} hectáreas en {city}, {country}, con casa principal de {built} m².",
 "ضيعة بمساحة {land_ha} هكتاراً في {city}، {country}، مع منزل رئيسي {built} م².",
 "位于{country}·{city}的地产，占地 {land_ha} 公顷，主宅 {built} 平方米。"),
"penthouses": I.T(
 "A {built} m² penthouse in {city}, {country}, with {beds} bedrooms and {baths} bathrooms.",
 "Penthouse de {built} m² en {city}, {country}, con {beds} dormitorios y {baths} baños.",
 "بنتهاوس بمساحة {built} م² في {city}، {country}، بـ {beds} غرف نوم و{baths} حمامات.",
 "位于{country}·{city}的顶层公寓，{built} 平方米，{beds} 间卧室、{baths} 间浴室。"),
"waterfront": I.T(
 "A waterfront residence of {built} m² in {city}, {country}, on {land} m², with {beds} bedrooms.",
 "Residencia frente al mar de {built} m² en {city}, {country}, sobre {land} m², con {beds} dormitorios.",
 "مسكن على الواجهة البحرية بمساحة {built} م² في {city}، {country}، على {land} م²، بـ {beds} غرف نوم.",
 "位于{country}·{city}的海滨住宅，建筑面积 {built} 平方米，占地 {land} 平方米，{beds} 间卧室。"),
"equestrian": I.T(
 "An equestrian property in {city}, {country}, with {land_ha} hectares, stabling and a residence of {built} m².",
 "Propiedad ecuestre en {city}, {country}, con {land_ha} hectáreas, cuadras y vivienda de {built} m².",
 "عقار للخيول في {city}، {country}، بمساحة {land_ha} هكتاراً وإسطبلات ومسكن {built} م².",
 "位于{country}·{city}的马术地产，占地 {land_ha} 公顷，含马厩与 {built} 平方米住宅。"),
"private-islands": I.T(
 "A private island of {land_ha} hectares in {city}, {country}.",
 "Isla privada de {land_ha} hectáreas en {city}, {country}.",
 "جزيرة خاصة بمساحة {land_ha} هكتاراً في {city}، {country}.",
 "位于{country}·{city}的私人岛屿，面积 {land_ha} 公顷。"),
}
DH = I.T(
 "{extra}. {keys_txt}Built area {built} m² on a site of {land} m², in {city}, {country}.",
 "{extra}. {keys_txt}Superficie construida de {built} m² sobre una parcela de {land} m², en {city}, {country}.",
 "{extra}. {keys_txt}مساحة مبنية {built} م² على موقع {land} م²، في {city}، {country}.",
 "{extra}。{keys_txt}建筑面积 {built} 平方米，用地 {land} 平方米，位于{country}{city}。")
DL = I.T(
 "{hectares} hectares in {city}, {country}. Projected use: {use}. Access: {access}.",
 "{hectares} hectáreas en {city}, {country}. Uso proyectado: {use}. Acceso: {access}.",
 "{hectares} هكتاراً في {city}، {country}. الاستخدام المتوقع: {use}. الوصول: {access}.",
 "{hectares} 公顷，位于{country}{city}。规划用途：{use}。交通：{access}。")
KEYS_TXT = I.T("{k} keys. ", "{k} llaves. ", "{k} مفتاحاً. ", "{k} 间客房。")

STATUS_CYCLE_R = ["available","exclusive-mandate","off-market","under-negotiation","available","exclusive-mandate"]
STATUS_CYCLE_H = ["operational","available","seeking-operator","under-negotiation","operational","exclusive-mandate"]
STATUS_CYCLE_L = ["development-ready","available","in-validation","exclusive-mandate","development-ready","off-market"]

def CT(name): return {lg: G.loc(name, lg, G.COUNTRY) for lg in LANGS}
def CY(name): return {lg: G.loc(name, lg, G.CITY) for lg in LANGS}
def PH(txt): return {lg: G.phrase(txt, lg) for lg in LANGS}

def L(d, **kw): return {lg: d[lg].format(**{k:(v if not isinstance(v,dict) else v[lg]) for k,v in kw.items()}) for lg in LANGS}

def build_residential():
    out=[]
    for cat, rows in S.RESIDENTIAL.items():
        for i,(variant,title,country,region,city,price,beds,baths,built,land) in enumerate(rows):
            aid=f"pr-{slug(cat)}-{slug(variant)}"
            ha = round(land/10000,1) if land else None
            desc = L(D[cat], city=CY(city), country=CT(country), built=f"{built:,}" if built else "-",
                     land=f"{land:,}" if land else "-", land_ha=f"{ha:,}" if ha else "-",
                     beds=beds or "-", baths=baths or "-")
            out.append({
              "id":aid,"demo":True,"category":"private-real-estate","subcategory":cat,"variant":variant,
              "title":title,"country":country,"region":region,"city":city,
              "price_usd":price,"currency":"USD",
              "bedrooms":beds,"bathrooms":baths,"built_area_m2":built,
              "land_area_m2":land,"hectares":ha,"hotel_keys":None,"berths":None,
              "status":STATUS_CYCLE_R[i],
              "short_description":desc,"long_description":desc,
              "features":[],"hero_image":f"assets/img/xaru/catalog/{aid}.jpg","gallery":[],
              "video":None,"video_poster":None,"featured":(i==0),
              "language_content":{"category":I.CATEGORY[cat],"variant":I.VARIANT[variant],"status":I.STATUS[STATUS_CYCLE_R[i]]},
              "source_media_ids":[]})
    return out

def build_hospitality():
    out=[]
    for cat, rows in S.HOSPITALITY.items():
        for i,(variant,title,country,region,city,price,keys,built,land,extra) in enumerate(rows):
            aid=f"ch-{slug(cat)}-{slug(variant)}"
            kt = {lg: (KEYS_TXT[lg].format(k=keys) if keys else "") for lg in LANGS}
            desc = L(DH, extra=extra, keys_txt=kt, built=f"{built:,}", land=f"{land:,}", city=CY(city), country=CT(country))
            berths=None
            m=re.search(r"(\d+)\s+berths", extra)
            if m: berths=int(m.group(1))
            out.append({
              "id":aid,"demo":True,"category":"commercial-hospitality","subcategory":cat,"variant":variant,
              "title":title,"country":country,"region":region,"city":city,
              "price_usd":price,"currency":"USD",
              "bedrooms":None,"bathrooms":None,"built_area_m2":built,
              "land_area_m2":land,"hectares":round(land/10000,1),"hotel_keys":keys,"berths":berths,
              "status":STATUS_CYCLE_H[i],
              "short_description":desc,"long_description":desc,
              "features":[],"hero_image":f"assets/img/xaru/catalog/{aid}.jpg","gallery":[],
              "video":None,"video_poster":None,"featured":(i==0),
              "language_content":{"category":I.CATEGORY[cat],"variant":I.VARIANT.get(variant, I.T(variant,variant,variant,variant)),"status":I.STATUS[STATUS_CYCLE_H[i]]},
              "source_media_ids":[]})
    return out

def build_land():
    out=[]
    for cat, rows in S.LAND.items():
        for i,(variant,title,country,region,city,price,hectares,use,access) in enumerate(rows):
            aid=f"ld-{slug(cat)}-{slug(variant)}"
            desc = L(DL, hectares=f"{hectares:,}", city=CY(city), country=CT(country), use=PH(use), access=PH(access))
            out.append({
              "id":aid,"demo":True,"category":"land-developments","subcategory":cat,"variant":variant,
              "title":title,"country":country,"region":region,"city":city,
              "price_usd":price,"currency":"USD",
              "bedrooms":None,"bathrooms":None,"built_area_m2":None,
              "land_area_m2":int(hectares*10000),"hectares":hectares,"hotel_keys":None,"berths":None,
              "status":STATUS_CYCLE_L[i],
              "projected_use":use,"access":access,
              "short_description":desc,"long_description":desc,
              "features":[],"hero_image":f"assets/img/xaru/catalog/{aid}.jpg","gallery":[],
              "video":None,"video_poster":None,"featured":(i==0),
              "language_content":{"category":I.CATEGORY[cat],"variant":I.VARIANT.get(variant, I.T(variant,variant,variant,variant)),"status":I.STATUS[STATUS_CYCLE_L[i]]},
              "source_media_ids":[]})
    return out

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, rows, label in (("private-real-estate.json", build_residential(), "private-real-estate"),
                            ("commercial-hospitality.json", build_hospitality(), "commercial-hospitality"),
                            ("land-developments.json", build_land(), "land-developments")):
        doc = {"$schema":"../SCHEMA.md","version":3,"demo":True,
               "note":"Demonstrative portfolio built per docs/BIBLIA_VISUAL_V3.md. Names, locations and figures are illustrative.",
               "demo_note":I.UI["demo_note"],"ui":I.UI,"catalog":label,"items":rows}
        with open(os.path.join(OUT,fn),"w",encoding="utf-8") as f:
            json.dump(doc,f,ensure_ascii=False,indent=1)
        print(f"{fn:32s} {len(rows):3d} activos")
