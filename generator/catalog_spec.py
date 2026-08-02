# -*- coding: utf-8 -*-
"""Especificación del catálogo demostrativo (Biblia Visual V3 §8).
Cada tupla: (variant_key, título propio, país, región, ciudad, precio USD, métricas...)
Las métricas se interpretan según la categoría; None = no aplica."""

# ---------- PRIVATE REAL ESTATE : 10 categorías x 6 variantes ----------
# (variant, title, country, region, city, price, beds, baths, built_m2, land_m2)
RESIDENTIAL = {
"contemporary-houses": [
 ("urban",        "Casa Serrano",        "Spain",       "Catalonia",        "Barcelona",     4_200_000, 5, 5,  620, 1_100),
 ("mountain",     "Haus Arlberg",        "Austria",     "Tyrol",            "Lech",          8_900_000, 6, 6,  740, 2_400),
 ("tropical",     "Casa Palmar",         "Costa Rica",  "Guanacaste",       "Nosara",        3_400_000, 4, 5,  510, 3_800),
 ("lakefront",    "Villa Seeblick",      "Switzerland", "Lucerne",          "Weggis",       12_500_000, 5, 6,  830, 2_900),
 ("golf",         "The Fairway House",   "Portugal",    "Algarve",          "Quinta do Lago",6_100_000, 5, 5,  690, 2_100),
 ("desert",       "Casa Cardón",         "Mexico",      "Baja California Sur","San José del Cabo",5_500_000,4,5, 580, 4_600),
],
"villas": [
 ("beachfront",   "Villa Alba",          "Greece",      "Cyclades",         "Paros",        11_800_000, 6, 7,  880, 5_200),
 ("mountain",     "Chalet Bellevue",     "France",      "Auvergne-Rhône-Alpes","Megève",     16_400_000, 7, 8, 1_050, 3_100),
 ("mediterranean","Villa Faro",          "Spain",       "Balearic Islands", "Ibiza",        14_200_000, 6, 7,  940, 6_400),
 ("tropical",     "Villa Ubud Sari",     "Indonesia",   "Bali",             "Ubud",          4_900_000, 5, 6,  720, 4_100),
 ("urban",        "Villa Recoleta",      "Argentina",   "Buenos Aires",     "Buenos Aires",  3_800_000, 5, 5,  660, 1_400),
 ("resort",       "Villa Anantara Bay",  "Thailand",    "Phuket",           "Phuket",        9_600_000, 5, 6,  810, 3_300),
],
"mansions": [
 ("waterfront",   "Bayshore House",      "United States","Florida",         "Miami Beach",  38_500_000, 8, 10, 1_640, 4_200),
 ("urban",        "Kensington House",    "United Kingdom","London",          "London",       62_000_000, 9, 11, 1_850, 1_900),
 ("mediterranean","Villa Corallo",       "Italy",       "Liguria",          "Portofino",    27_400_000, 8, 9, 1_420, 5_800),
 ("tropical",     "Casa Bougainvillea",  "Dominican Republic","La Altagracia","Punta Cana",  14_900_000, 7, 8, 1_180, 8_600),
 ("historic",     "Palazzo Vendramin",   "Italy",       "Veneto",           "Venice",       46_000_000, 10,11, 2_100, 2_400),
 ("gated",        "Hacienda del Bosque", "Mexico",      "Ciudad de México", "Ciudad de México",18_700_000,7, 8, 1_290, 3_500),
],
"castles-chateaux": [
 ("medieval",     "Château de Vaubrun",  "France",      "Occitanie",        "Carcassonne",  22_000_000, 14,12, 3_200, 180_000),
 ("french-chateau","Château de Laroche", "France",      "Centre-Val de Loire","Amboise",     31_500_000, 18,14, 4_100, 260_000),
 ("restored",     "Schloss Falkenstein", "Germany",     "Bavaria",          "Füssen",       27_800_000, 16,13, 3_600, 145_000),
 ("vineyard",     "Castello di Vernazza","Italy",       "Tuscany",          "Montalcino",   48_000_000, 20,16, 4_800, 420_000),
 ("rural-palace", "Palacio de Almenara", "Spain",       "Castile and León", "Segovia",      19_400_000, 15,12, 3_400, 210_000),
 ("fortress",     "Castelo do Cabo",     "Portugal",    "Alentejo",         "Évora",       112_000_000, 24,20, 6_200, 680_000),
],
"haciendas": [
 ("colonial",     "Hacienda San Rafael", "Mexico",      "Yucatán",          "Mérida",        6_800_000, 9, 8, 1_650, 240_000),
 ("coffee",       "Hacienda La Esperanza","Colombia",   "Quindío",          "Salento",       4_200_000, 8, 7, 1_180, 380_000),
 ("equestrian",   "Hacienda Los Robles", "Spain",       "Andalusia",        "Jerez",        12_400_000, 10, 9, 1_920, 560_000),
 ("agricultural", "Hacienda El Trapiche","Guatemala",   "Sacatepéquez",     "Antigua",       3_600_000, 7, 6, 1_040, 720_000),
 ("vineyard",     "Hacienda Valle Alto", "Chile",       "Valparaíso",       "Casablanca",   16_900_000, 11, 9, 2_100, 940_000),
 ("tropical",     "Hacienda Cayo Verde", "Dominican Republic","Samaná",     "Las Terrenas",  8_100_000, 8, 8, 1_380, 310_000),
],
"estates": [
 ("equestrian",   "Ballycroy Estate",    "Ireland",     "County Wicklow",   "Wicklow",      14_600_000, 9, 8, 1_540, 480_000),
 ("mountain",     "Val Sereno Estate",   "Switzerland", "Grisons",          "Klosters",     34_000_000, 10,10, 1_980, 260_000),
 ("hunting",      "Glenmoor Estate",     "United Kingdom","Scotland",       "Perthshire",   21_800_000, 12,10, 2_240, 1_600_000),
 ("olive-grove",  "Tenuta degli Ulivi",  "Italy",       "Apulia",           "Ostuni",        9_400_000, 8, 7, 1_310, 620_000),
 ("vineyard",     "Domaine de Roquevert","France",      "Provence",         "Aix-en-Provence",28_500_000,11, 9, 1_870, 840_000),
 ("tropical",     "Rio Verde Estate",    "Brazil",      "Bahia",            "Trancoso",     11_200_000, 9, 8, 1_460, 720_000),
],
"penthouses": [
 ("dubai",        "Marina Sky Penthouse","United Arab Emirates","Dubai",    "Dubai",        41_000_000, 5, 6,  920, None),
 ("oceanfront",   "Ocean Crest Penthouse","United States","Florida",        "Miami",        26_500_000, 4, 5,  740, None),
 ("urban",        "Reforma Sky Residence","Mexico",     "Ciudad de México", "Ciudad de México",7_900_000,4, 4,  610, None),
 ("historic",     "Attico Barberini",    "Italy",       "Lazio",            "Rome",         18_200_000, 4, 5,  580, None),
 ("duplex",       "The Ashworth Duplex", "United Kingdom","London",         "London",       33_400_000, 5, 6,  810, None),
 ("panoramic",    "Ático Diagonal Mar",  "Spain",       "Catalonia",        "Barcelona",     9_600_000, 4, 4,  520, None),
],
"waterfront": [
 ("beach-house",  "Casa Ola",            "Mexico",      "Oaxaca",           "Puerto Escondido",3_900_000,4, 4,  480, 2_400),
 ("clifftop",     "Villa Acantilado",    "Portugal",    "Algarve",          "Lagos",        13_700_000, 5, 6,  760, 3_900),
 ("island",       "Villa Coralina",      "Bahamas",     "Exuma",            "Great Exuma",  24_800_000, 6, 7,  980, 12_400),
 ("caribbean",    "Villa Marigot",       "Saint Barthélemy","Saint Barthélemy","Gustavia",  46_000_000, 6, 7, 1_040, 6_800),
 ("mediterranean","Villa Cap Ferrat",    "France",      "Provence-Alpes-Côte d'Azur","Saint-Jean-Cap-Ferrat",58_000_000,7,8,1_240,9_200),
 ("asian-tropical","Villa Bulan Biru",   "Indonesia",   "Bali",             "Uluwatu",       7_400_000, 5, 6,  820, 4_600),
],
"equestrian": [
 ("stables",      "Highfield Stud",      "United Kingdom","Newmarket",      "Newmarket",    18_900_000, 8, 7, 1_420, 1_200_000),
 ("riding-centre","Centro Ecuestre Doñana","Spain",     "Andalusia",        "Seville",      12_100_000, 7, 6, 1_180, 860_000),
 ("competition",  "Haras de Bellevue",   "France",      "Normandy",         "Deauville",    26_400_000, 9, 8, 1_640, 1_400_000),
 ("hacienda",     "Hacienda El Potrero", "Mexico",      "Jalisco",          "Guadalajara",   9_700_000, 8, 7, 1_320, 940_000),
 ("polo",         "Estancia La Martina", "Argentina",   "Buenos Aires",     "Pilar",        16_800_000, 9, 8, 1_510, 2_100_000),
 ("rural",        "Quinta dos Cavalos",  "Portugal",    "Alentejo",         "Estremoz",      6_200_000, 7, 6, 1_060, 680_000),
],
"private-islands": [
 ("caribbean",    "Cayo Sirena",         "Bahamas",     "Exuma",            "Exuma Cays",   68_000_000, 6, 7, 1_200, 340_000),
 ("mediterranean","Isola del Faro",      "Italy",       "Sicily",           "Aeolian Islands",42_000_000,5, 6,  980, 180_000),
 ("asian-tropical","Pulau Selatan",      "Indonesia",   "Raja Ampat",       "Raja Ampat",   31_500_000, 4, 5,  740, 620_000),
 ("with-resort",  "Isla Bonita Resort Island","Belize", "Stann Creek",      "Placencia",   145_000_000, None,None,None,1_240_000),
 ("undeveloped",  "Cayo Esmeralda",      "Dominican Republic","Samaná",     "Samaná Bay",   26_000_000, None,None,None,1_860_000),
 ("archipelago",  "Archipiélago Las Ánimas","Panama",   "Guna Yala",        "Guna Yala",   410_000_000, None,None,None,7_400_000),
],
# Anadido 1-ago-2026: el buscador ofrece de 1 a 7 dormitorios pero la cartera
# empezaba en 4, asi que los filtros de 1, 2 y 3 no podian devolver nada. Estas
# dos categorias los llenan sin bajar del millon: residencias de marca y
# apartamentos urbanos de lujo, de 1 a 3 dormitorios.
"branded-residences": [
 ("one-bed-tower",  "The Aurelia Residences One", "United Arab Emirates","Dubai","Dubai",       2_400_000, 1, 2,  118, None),
 ("two-bed-skyline","Solaris Tower Two",          "Singapore",    "Singapore",  "Singapore",    4_100_000, 2, 3,  186, None),
 ("three-bed-duplex","Maison Verde Duplex",       "United Kingdom","London",    "London",       8_900_000, 3, 4,  312, None),
 ("two-bed-beachfront","Costa Marfil Residences", "Spain",        "Balearic Islands","Palma",   3_600_000, 2, 3,  164, None),
 ("three-bed-golf", "Fairway House Residences",   "Portugal",     "Algarve",    "Quinta do Lago",5_200_000,3, 4,  248, None),
 ("one-bed-marina", "Puerto Azul Residences One", "United Arab Emirates","Dubai","Dubai Marina", 1_950_000, 1, 2,  104, None),
],
"city-apartments": [
 ("one-bed-historic","Palazzo Vitale Uno",        "Italy",        "Lazio",      "Rome",         1_850_000, 1, 1,   96, None),
 ("two-bed-loft",   "The Foundry Loft Two",       "United States","New York",   "New York",     4_800_000, 2, 2,  178, None),
 ("three-bed-family","Jardines del Retiro Tres",  "Spain",        "Madrid",     "Madrid",       3_200_000, 3, 3,  226, None),
 ("one-bed-waterfront","Riva Uno",                "Switzerland",  "Ticino",     "Lugano",       2_100_000, 1, 2,  110, None),
 ("two-bed-panoramic","Cielo Dos",                "Mexico",       "Ciudad de México","Ciudad de México",2_650_000,2,2, 158, None),
 ("three-bed-garden","Villa Jardin Tres",         "France",       "Provence-Alpes-Côte d'Azur","Nice",6_400_000,3,3, 265, None),
],
}

# ---------- COMMERCIAL & HOSPITALITY : 8 categorías x 6 ----------
# (variant, title, country, region, city, price, keys, built_m2, land_m2, extra)
#   extra = dato distintivo (amarres, avance %, componentes...)
HOSPITALITY = {
"operating-hotels": [
 ("city-5star",     "Hotel Almirante",        "Spain","Andalusia","Seville",        48_000_000, 142, 11_400,  4_200, "5-star, city centre"),
 ("beach-resort",   "Playa Dorada Hotel",     "Dominican Republic","Puerto Plata","Puerto Plata",96_000_000, 310, 28_600, 62_000, "5-star, 480 m beachfront"),
 ("mountain",       "Alpenhof Grand",         "Austria","Tyrol","Kitzbühel",        62_500_000, 118,  9_800, 12_400, "Ski-in, ski-out"),
 ("historic",       "Palazzo Reale Hotel",    "Italy","Campania","Naples",          74_000_000,  96, 12_900,  3_100, "Listed 18th-c building"),
 ("airport",        "Aerotower Business Hotel","United Arab Emirates","Dubai","Dubai",83_000_000, 264, 19_700,  8_600, "Airport corridor"),
 ("island",         "Isla Azul Hotel",        "Greece","Cyclades","Santorini",      57_400_000,  84,  6_900, 14_800, "Caldera frontage"),
],
"boutique-hotels": [
 ("design",         "Casa Nueve",             "Mexico","Oaxaca","Oaxaca de Juárez", 14_800_000,  32,  3_400,  1_900, "Design-led, 32 keys"),
 ("heritage",       "Riad Assafar",           "Morocco","Marrakech-Safi","Marrakech",9_600_000,  24,  2_800,  1_400, "Restored riad"),
 ("vineyard",       "Bodega Hotel Valdemar",  "Spain","La Rioja","Haro",            18_200_000,  28,  4_100, 86_000, "Working winery"),
 ("jungle",         "Selva Lodge",            "Costa Rica","Puntarenas","Osa",      12_400_000,  26,  2_600, 240_000, "Private reserve"),
 ("coastal",        "Casa del Acantilado",    "Portugal","Algarve","Sagres",        21_600_000,  34,  3_900,  6_200, "Clifftop"),
 ("urban-loft",     "The Foundry Rooms",      "United Kingdom","Greater Manchester","Manchester",16_900_000,41,4_600,1_800,"Converted industrial"),
],
"resorts": [
 ("all-inclusive",  "Bahía Serena Resort",    "Mexico","Quintana Roo","Riviera Maya",184_000_000, 486, 62_000, 148_000, "1.1 km beachfront"),
 ("wellness",       "Aqua Sana Retreat",      "Thailand","Krabi","Krabi",           68_000_000, 124, 18_400,  92_000, "Wellness programme"),
 ("golf",           "Costa Verde Golf Resort","Portugal","Algarve","Vilamoura",     142_000_000, 268, 41_000, 620_000, "18-hole championship"),
 ("eco",            "Selva Viva Eco Resort",  "Belize","Stann Creek","Placencia",   46_500_000,  72, 11_200, 340_000, "Off-grid, certified"),
 ("ski",            "Val Blanche Resort",     "France","Auvergne-Rhône-Alpes","Tignes",118_000_000,196, 32_400,  74_000, "Ski-in, ski-out"),
 ("island",         "Coral Cay Resort",       "Maldives","Baa Atoll","Baa Atoll",   246_000_000,  96, 14_800, 210_000, "Overwater villas"),
],
"serviced-residences": [
 ("corporate",      "Marina Residences DIFC", "United Arab Emirates","Dubai","Dubai",112_000_000, 184, 26_800, 6_400, "Corporate long-stay"),
 ("family",         "Jardines Aparthotel",    "Spain","Community of Madrid","Madrid",54_000_000, 126, 17_200, 4_100, "Family serviced"),
 ("beach",          "Costa Azul Suites",      "Mexico","Nayarit","Punta Mita",      39_600_000,  88, 12_400, 18_600, "Beachfront suites"),
 ("student-adjacent","Campus View Residences","United Kingdom","Scotland","Edinburgh",31_800_000,142, 9_800,  2_900, "Institutional lease"),
 ("branded",        "The Wynford Residences", "Singapore","Singapore","Singapore",  168_000_000, 96, 21_400,  3_800, "Branded operator"),
 ("medical",        "Clinica Park Residences","Germany","Bavaria","Munich",         42_000_000,  74, 11_600,  5_200, "Medical-adjacent"),
],
"marinas-beach-clubs": [
 ("superyacht",     "Puerto Alcazaba Marina", "Spain","Andalusia","Marbella",       210_000_000, None, 8_400, 168_000, "412 berths, to 80 m"),
 ("island-marina",  "Cayo Norte Marina",      "Dominican Republic","La Altagracia","Cap Cana",96_000_000,None,4_600,94_000,"186 berths"),
 ("beach-club",     "Bahía Beach Club",       "Greece","Cyclades","Mykonos",        34_500_000, None, 2_900,  14_000, "620 m² beach frontage"),
 ("river-marina",   "Douro River Marina",     "Portugal","Norte","Porto",           41_200_000, None, 3_400,  62_000, "204 berths"),
 ("resort-marina",  "Laguna Marina Resort",   "Turkey","Muğla","Bodrum",            78_000_000, None, 6_100, 118_000, "268 berths + resort"),
 ("urban-waterfront","Waterfront Club Bahía", "Panama","Panamá","Panama City",      52_400_000, None, 4_800,  38_000, "City waterfront"),
],
"parks-entertainment": [
 ("theme-park",     "Parque Aventura Caribe", "Dominican Republic","La Altagracia","Punta Cana",320_000_000,None,68_000,1_240_000,"Theme park, 12 attractions"),
 ("water-park",     "Aqua Mundo Park",        "Spain","Valencian Community","Benidorm",96_000_000,None,24_000, 320_000, "Water park"),
 ("eco-park",       "Bosque Vivo Eco Park",   "Costa Rica","Alajuela","La Fortuna", 58_000_000, None, 9_400, 2_600_000, "Eco-adventure park"),
 ("cultural",       "Distrito Cultural Sur",  "Mexico","Jalisco","Guadalajara",     124_000_000,None, 42_000,  180_000, "Cultural district"),
 ("marine-park",    "Océano Marine Park",     "Bahamas","New Providence","Nassau",  186_000_000,None, 31_000,  420_000, "Marine attraction"),
 ("resort-entertainment","Isla Fiesta Entertainment","Panama","Panamá","Panama City",78_500_000,None,18_600, 240_000, "Entertainment complex"),
],
"mixed-use": [
 ("waterfront",     "Puerto Nuevo District",  "Panama","Panamá","Panama City",      420_000_000,None, 186_000, 320_000, "Retail, office, residential"),
 ("downtown",       "Torre Central Complex",  "Mexico","Ciudad de México","Ciudad de México",268_000_000,None,124_000,42_000,"Office + retail + hotel"),
 ("transit",        "Estación Norte Quarter", "Spain","Community of Madrid","Madrid",194_000_000,None, 96_000,  38_000, "Transit-oriented"),
 ("resort-mixed",   "Bahía Blanca Village",   "Dominican Republic","Samaná","Las Terrenas",112_000_000,None,48_000,186_000,"Resort + residences"),
 ("industrial-conv","The Docklands Works",    "United Kingdom","England","Liverpool",86_400_000,None, 62_000,  74_000, "Industrial conversion"),
 ("business-park",  "Gateway Business Quarter","United Arab Emirates","Abu Dhabi","Abu Dhabi",236_000_000,None,108_000,96_000,"Business quarter"),
],
"halted-projects": [
 ("hotel-70",       "Proyecto Costa Azul",    "Panama","Panamá","Panama City",      42_000_000, 218, 34_000,  18_000, "≈70% complete, halted 2023"),
 ("resort-45",      "Resort Bahía Larga",     "Dominican Republic","Puerto Plata","Puerto Plata",58_000_000,340,52_000,124_000,"≈45% complete"),
 ("tower-85",       "Torre Marina Sur",       "Mexico","Quintana Roo","Cancún",     36_500_000, 164, 28_400,   9_600, "≈85% complete"),
 ("mixed-30",       "Distrito Puerta Real",   "Spain","Andalusia","Málaga",         74_000_000, None, 61_000,  42_000, "≈30% complete"),
 ("boutique-60",    "Hotel Miradouro",        "Portugal","Norte","Porto",           19_800_000,  62,  8_900,   3_400, "≈60% complete"),
 ("marina-40",      "Marina Vista Proyecto",  "Turkey","Muğla","Marmaris",          46_200_000, None,  7_400,  86_000, "≈40% complete, 180 berths"),
],
}

# ---------- LAND & MASTER DEVELOPMENTS : 6 categorías x 6 ----------
# (variant, title, country, region, city, price, hectares, use, access)
LAND = {
"coastal-land": [
 ("beachfront-km",  "Costa Larga",            "Dominican Republic","Samaná","Samaná",     84_000_000, 1_240, "Resort / residential", "Paved road + 42 km airport"),
 ("clifftop",       "Acantilados de Nazaré",  "Portugal","Centro","Nazaré",                26_500_000,   186, "Boutique resort",      "National road frontage"),
 ("bay",            "Bahía Escondida",        "Mexico","Oaxaca","Huatulco",                48_000_000,   640, "Integrated resort",    "Highway + 28 km airport"),
 ("peninsula",      "Península Verde",        "Panama","Bocas del Toro","Bocas del Toro",  62_000_000,   980, "Mixed resort",         "Marine + airstrip"),
 ("dune-coast",     "Dunas del Norte",        "Spain","Andalusia","Huelva",                31_400_000,   214, "Low-density resort",   "Coastal highway"),
 ("reef-front",     "Arrecife Sur",           "Belize","Stann Creek","Placencia",          38_900_000,   410, "Eco-resort",           "Coastal road + marina"),
],
"hotel-resort-land": [
 ("beach-parcel",   "Parcela Playa Grande",   "Mexico","Quintana Roo","Tulum",              54_000_000,   68, "Hotel, up to 320 keys","Federal highway"),
 ("island-parcel",  "Cayo Hotelero",          "Bahamas","Exuma","Exuma",                    72_000_000,  124, "Resort, up to 180 keys","Marine + airstrip"),
 ("lakefront",      "Terreno Lago Azul",      "Italy","Lombardy","Lake Como",               46_500_000,   32, "Boutique hotel",       "Provincial road"),
 ("mountain",       "Meseta Andina",          "Chile","Los Lagos","Puerto Varas",           28_400_000,  186, "Mountain resort",      "Route 5 + 34 km airport"),
 ("desert",         "Reserva del Desierto",   "United Arab Emirates","Dubai","Dubai",       96_000_000,  240, "Desert resort",        "E611 corridor"),
 ("golf-resort",    "Campo Verde Resort Land","Portugal","Algarve","Silves",                41_800_000,  310, "Golf resort",          "A22 motorway"),
],
"masterplan-land": [
 ("new-town",       "Ciudad Nueva Norte",     "Panama","Panamá Oeste","Arraiján",          186_000_000, 1_840, "Master-planned town",  "Pan-American Highway"),
 ("coastal-master", "Masterplan Costa Sur",   "Dominican Republic","La Altagracia","Miches",124_000_000, 1_120, "Coastal masterplan",  "Coastal highway"),
 ("resort-city",    "Distrito Turístico Sur", "Mexico","Oaxaca","Puerto Escondido",         98_000_000,   860, "Resort district",     "Highway 200 + airport"),
 ("eco-master",     "Reserva Integrada Verde","Costa Rica","Guanacaste","Liberia",          76_500_000, 1_460, "Eco masterplan",      "Route 21 + airport"),
 ("island-master",  "Archipiélago Plan Maestro","Indonesia","Riau Islands","Batam",         142_000_000, 2_100, "Island masterplan",   "Ferry + airstrip"),
 ("border-logistics","Corredor Frontera Norte","Mexico","Nuevo León","Monterrey",           64_000_000,   680, "Logistics masterplan","Federal highway + rail"),
],
"urban-mixed-land": [
 ("downtown",       "Solar Centro Histórico", "Spain","Community of Madrid","Madrid",        58_000_000,   4.2, "Mixed use",           "Metro + arterial"),
 ("waterfront-urban","Frente Portuario",      "Portugal","Lisbon","Lisbon",                  86_000_000,  11.4, "Waterfront mixed",    "Ring road + port"),
 ("transit",        "Nodo Estación Sur",      "Mexico","Ciudad de México","Ciudad de México",42_500_000,   6.8, "Transit-oriented",    "Metro interchange"),
 ("business-dist",  "Parcela Distrito Negocios","United Arab Emirates","Abu Dhabi","Abu Dhabi",134_000_000,18.6,"Business district",  "E10 + metro corridor"),
 ("regeneration",   "Zona Regeneración Este", "United Kingdom","England","Birmingham",       38_900_000,  22.4, "Urban regeneration",  "Motorway + rail"),
 ("suburban-growth","Corredor Norte Residencial","Colombia","Cundinamarca","Bogotá",         31_200_000,  46.0, "Residential growth",  "Autopista Norte"),
],
"agricultural-estate-land": [
 ("vineyard",       "Viñedos Alto Valle",     "Argentina","Mendoza","Mendoza",               34_000_000, 1_240, "Vineyard estate",     "Ruta 40"),
 ("olive",          "Olivar de Jaén",         "Spain","Andalusia","Jaén",                    22_400_000,   860, "Olive estate",        "A-44 motorway"),
 ("coffee",         "Finca Cafetera Alta",    "Colombia","Huila","Neiva",                    18_600_000, 1_040, "Coffee estate",       "National road"),
 ("cattle",         "Estancia Los Llanos",    "Uruguay","Durazno","Durazno",                 29_800_000, 4_600, "Cattle estate",       "Route 5"),
 ("agroforestry",   "Reserva Agroforestal Sur","Brazil","Bahia","Ilhéus",                    26_400_000, 3_200, "Agroforestry",        "BR-101 + port"),
 ("irrigated",      "Valle Irrigado Norte",   "Mexico","Sinaloa","Culiacán",                 24_100_000, 2_400, "Irrigated cropland",  "Federal highway + rail"),
],
"island-territories": [
 ("undeveloped-isl","Isla Sin Desarrollar Norte","Panama","Guna Yala","Guna Yala",           38_000_000,   420, "Undeveloped island",  "Marine access only"),
 ("multi-island",   "Grupo Insular Esmeralda","Indonesia","Raja Ampat","Raja Ampat",          92_000_000, 1_860, "Island group",        "Marine + airstrip"),
 ("lagoon-island",  "Isla Laguna Interior",   "Belize","Belize District","Belize City",       27_500_000,   240, "Lagoon island",       "Marine access"),
 ("reef-island",    "Cayo Arrecife",          "Bahamas","Exuma","Exuma",                      64_000_000,   180, "Reef island",         "Marine + airstrip"),
 ("volcanic",       "Isla Volcánica Sur",     "Greece","South Aegean","Aegean",               46_800_000,   310, "Volcanic island",     "Marine access"),
 ("mangrove",       "Territorio Manglar",     "Mexico","Nayarit","San Blas",                  33_200_000,   680, "Protected coastal",   "Coastal road + marine"),
],
}
