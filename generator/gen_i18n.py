#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""XARU HOME — Phase 5 i18n generator.
Builds /es/index.html and /ar/index.html from the English root index.html.
- fixes relative asset paths (assets/ -> ../assets/)
- points cross-page links to the English pages (../page.html)
- swaps the language switcher for real per-folder links
- rewrites head meta / hreflang / canonical / og:url per language
- applies a patrimonial-quality translation dictionary
- AR: sets dir=rtl, links xaru-rtl.css, sets hero swiper dir=rtl
"""
import re, os, json

SRC = "/home/claude/work/site/xaru/index.html"
OUT = {"es": "/home/claude/work/site/xaru/es/index.html",
       "ar": "/home/claude/work/site/xaru/ar/index.html"}

with open(SRC, encoding="utf-8") as f:
    BASE = f.read()

# ---------------------------------------------------------------- helpers
def ws(pat):
    """Turn an English fragment into a whitespace-tolerant regex."""
    toks = pat.split()
    return r"\s+".join(re.escape(t) for t in toks)

def apply(html, pairs):
    for en, tr in pairs:
        html = re.sub(ws(en), lambda m, tr=tr: tr, html)
    return html

# ---------------------------------------------------------------- switcher
# Real 4-language switcher (EN root · /es/ · /ar/ · /zh/). Every version now
# offers all four with live links to their equivalent page; the current page's
# language carries aria-current and shows its own flag by default. ZH is active
# (no more "soon" placeholder).
FLAG   = {"en": "flag-icon-us", "es": "flag-icon-es", "ar": "flag-icon-sa", "zh": "flag-icon-cn"}
DLCODE = {"en": "EN",  "es": "ES",  "ar": "AR",    "zh": "ZH"}
LABEL3 = {"en": "ENG", "es": "ESP", "ar": "ARB",   "zh": "ZHO"}
HREFL  = {"en": "en",  "es": "es",  "ar": "ar",    "zh": "zh-CN"}
# Clean, root-relative home of each language. The language switcher (desktop +
# mobile) and the logo always point here — never to an index.html filename.
HOME   = {"en": "/",   "es": "/es/", "ar": "/ar/",  "zh": "/zh/"}

def _lang_href(cur, target, fname):
    """Path from the CURRENT language page to the TARGET language equivalent."""
    if target == cur:
        return fname
    if cur == "en":                       # root -> subfolder
        return "%s/%s" % (target, fname)
    if target == "en":                    # subfolder -> root
        return "../%s" % fname
    return "../%s/%s" % (target, fname)   # subfolder -> other subfolder

def switcher(lang, fname="index.html"):
    def row(t):
        cur = ' aria-current="true"' if t == lang else ''
        return (f'<a href="{HOME[t]}" hreflang="{HREFL[t]}" data-lang="{DLCODE[t]}"{cur}>\n'
                f'                      <span class="flag-btn flag-icon {FLAG[t]}"></span>\n'
                f'                      <span>{LABEL3[t]}</span>\n'
                f'                    </a>')
    rows = "\n                    ".join(row(t) for t in ("en", "es", "ar", "zh"))
    return f'''<li class="cs_language_select">
                  <div class="cs_language_switcher" role="button" tabindex="0" aria-label="{{lbl}}" aria-haspopup="true">
                    <span class="flag-btn flag-icon {FLAG[lang]}" data-lang="{DLCODE[lang]}"></span>
                  </div>
                  <div class="cs_language_dropdown">
                    {rows}
                  </div>
                </li>'''

SW_LABEL = {"es": "Seleccionar idioma", "ar": "اختر اللغة", "zh": "选择语言", "en": "Select language"}

# ---------------------------------------------------------------- mobile language row
# The desktop switcher lives in the header; on mobile it was missing. This block
# is injected INSIDE the slide-out menu (.cs_nav_list_wrap), after the nav list,
# so the four languages are reachable from the hamburger menu too. It is hidden
# on desktop via CSS (only visible at the mobile-menu breakpoint, <=1199px) and
# mirrors correctly under RTL through xaru-rtl.css. Same hrefs as the desktop
# switcher; the active language carries aria-current and an .is-active class.
def mobile_switcher(lang, fname="index.html"):
    def row(t):
        cur = ' aria-current="true"' if t == lang else ''
        active = ' is-active' if t == lang else ''
        return (f'<a href="{HOME[t]}" hreflang="{HREFL[t]}" data-lang="{DLCODE[t]}" class="cs_mobile_lang_item{active}"{cur}>\n'
                f'                      <span class="flag-btn flag-icon {FLAG[t]}"></span>\n'
                f'                      <span>{DLCODE[t]}</span>\n'
                f'                    </a>')
    rows = "\n                    ".join(row(t) for t in ("en", "es", "ar", "zh"))
    return (f'<!-- xaru-mobile-lang -->\n'
            f'                  <div class="cs_mobile_lang" role="group" aria-label="{{lbl}}">\n'
            f'                    {rows}\n'
            f'                  </div>\n'
            f'                  <!-- /xaru-mobile-lang -->')

def strip_mobile_lang(h):
    """Remove any previously injected mobile-language block (idempotency)."""
    return re.sub(r'[ \t]*<!-- xaru-mobile-lang -->.*?<!-- /xaru-mobile-lang -->\s*\n?',
                  '', h, flags=re.S)

def inject_mobile_lang(h, lang, fname):
    """Insert the mobile language row at the end of the slide-out nav."""
    h = strip_mobile_lang(h)
    block = mobile_switcher(lang, fname).replace("{lbl}", SW_LABEL[lang])
    return h.replace('<span class="cs_close_nav"></span>',
                     block + '\n                  <span class="cs_close_nav"></span>', 1)

def inject_head_extras(h):
    """Link the client-side language auto-detector in <head>, once, as early as
    possible (right after the viewport meta) without blocking heavy render.
    Idempotent: skipped if already present. Asset path is written as
    'assets/js/...'; finish() rewrites it to '../assets/js/...' for subfolders."""
    if "xaru-lang-detect.js" in h:
        return h
    tag = '\\1\n    <!-- language auto-detect (client-side, SEO-safe) -->\n    <script src="assets/js/xaru-lang-detect.js"></script>'
    return re.sub(r'(<meta name="viewport"[^>]*>)', tag, h, count=1)

# ---------------------------------------------------------------- head meta
HEAD = {
 "es": {
  "title": "XARU HOME — Bienes raíces globales a la mayor escala",
  "desc": "XARU HOME — Bienes raíces globales a la mayor escala. Una marca de NEXARU GLOBAL: islas privadas, desarrollos maestros, hoteles y las propiedades más excepcionales del mundo.",
  "ogdesc": "Una marca de NEXARU GLOBAL. Islas privadas, desarrollos maestros y las propiedades más excepcionales del mundo — una sola estructura, en todo el mundo.",
  "twdesc": "Una marca de NEXARU GLOBAL. Islas privadas, desarrollos maestros y las propiedades más excepcionales del mundo.",
  "url": "https://xaruhome.com/es/",
 },
 "ar": {
  "title": "XARU HOME — عقارات عالمية على أرفع مستوى",
  "desc": "XARU HOME — عقارات عالمية على أرفع مستوى. علامة من NEXARU GLOBAL: جزر خاصة، ومشاريع تطوير كبرى، وفنادق، وأكثر عقارات العالم تميّزاً.",
  "ogdesc": "علامة من NEXARU GLOBAL. جزر خاصة ومشاريع تطوير كبرى وأكثر عقارات العالم تميّزاً — كيان واحد، حول العالم.",
  "twdesc": "علامة من NEXARU GLOBAL. جزر خاصة ومشاريع تطوير كبرى وأكثر عقارات العالم تميّزاً.",
  "url": "https://xaruhome.com/ar/",
 },
 "zh": {
  "title": "XARU HOME — 臻于至高格局的全球房产",
  "desc": "XARU HOME — 臻于至高格局的全球房产。NEXARU GLOBAL 旗下品牌：私人岛屿、大型综合开发项目、酒店，以及世界上最卓越的房产。",
  "ogdesc": "NEXARU GLOBAL 旗下品牌。私人岛屿、大型开发项目，以及世界上最卓越的房产——单一架构，遍及全球。",
  "twdesc": "NEXARU GLOBAL 旗下品牌。私人岛屿、大型开发项目，以及世界上最卓越的房产。",
  "url": "https://xaruhome.com/zh/",
 },
}

EN_TITLE = "XARU HOME — Global Real Estate at Its Highest Scale"
EN_DESC = "XARU HOME — Global real estate at its highest scale. A NEXARU GLOBAL brand: private islands, master developments, hotels and the world’s most exceptional properties."
EN_OGDESC = "A NEXARU GLOBAL brand. Private islands, master developments and the world's most exceptional properties — one structure, worldwide."
EN_TWDESC = "A NEXARU GLOBAL brand. Private islands, master developments and the world's most exceptional properties."

# ---------------------------------------------------------------- ES dict
ES = [
 # ---- description / og handled via head block below (title etc) ----
 # NAV
 (">Opportunities</a>", ">Oportunidades</a>"),
 (">Properties</a>", ">Propiedades</a>"),
 (">Investment</a>", ">Inversión</a>"),
 (">Developers</a>", ">Promotores</a>"),
 (">Relocation</a>", ">Relocalización</a>"),
 (">Projects</a>", ">Proyectos</a>"),
 (">About</a>", ">Nosotros</a>"),
 (">Contact</a>", ">Contacto</a>"),
 ("<span>Private Enquiry</span>", "<span>Consulta Privada</span>"),
 # PRELOADER
 ('data-text="XARU HOME | Global Luxury | Loading"', 'data-text="XARU HOME | Lujo global | Cargando"'),
 ('alt="XARU HOME monogram"', 'alt="Monograma de XARU HOME"'),
 # HERO
 ("<h1>Global Real Estate <br />at Its Highest Scale.</h1>", "<h1>Bienes raíces globales <br />a la mayor escala.</h1>"),
 ("A NEXARU GLOBAL brand — private islands, master developments, and the world&rsquo;s most exceptional properties.",
  "Una marca de NEXARU GLOBAL — islas privadas, desarrollos maestros y las propiedades más excepcionales del mundo."),
 ('data-text="Private Islands | Master Developments | Hotels &amp; Resorts | Exceptional Homes"',
  'data-text="Islas privadas | Desarrollos maestros | Hoteles y resorts | Residencias excepcionales"'),
 (">Private Islands</span", ">Islas privadas</span"),
 ("Explore Opportunities", "Explorar oportunidades"),
 ("Private Enquiry", "Consulta privada"),
 ("<h2>A Private Island &mdash; <br />Isola del Faro.</h2>", "<h2>Una isla privada &mdash; <br />Isola del Faro.</h2>"),
 ("Whole island under a single title &middot; $42,000,000",
  "Isla completa bajo un único título &middot; $42,000,000"),
 ("View the Asset", "Ver el activo"),
 ("<h1>Master Developments, <br />From Land to Legacy.</h1>", "<h1>Desarrollos maestros, <br />del suelo al legado.</h1>"),
 ("ASHIMA — Ancestral Odyssey · Oaxaca, M&eacute;xico", "ASHIMA — Odisea ancestral · Oaxaca, México"),
 ("Discover the Project", "Descubrir el proyecto"),
 ('<span class="xr_social_title">Social Media</span>', '<span class="xr_social_title">Redes sociales</span>'),
 ('aria-label="Previous slide">Prev<', 'aria-label="Diapositiva anterior">Ant<'),
 ('aria-label="Next slide">Next<', 'aria-label="Diapositiva siguiente">Sig<'),
 ('<span class="xr_hero_scroll">Scroll</span>', '<span class="xr_hero_scroll">Desliza</span>'),
 # SECTION 01
 ("Land &amp; <span>Large-Scale Developments</span>", "Suelo y <span>desarrollos a gran escala</span>"),
 ("Opportunities Measured <br /> in Kilometers, Not Meters", "Oportunidades medidas <br /> en kilómetros, no en metros"),
 (">View the Full Portfolio<", ">Ver el portafolio completo<"),
 (">Private Island</span>", ">Isla privada</span>"),
 ("<h3>Private Island — Saman&aacute; Bay</h3>", "<h3>Isla privada — bahía de Samaná</h3>"),
 (">Dominican Republic</p>", ">República Dominicana</p>"),
 ("Kilometers of pristine beachfront held in a single title — a generational asset of a scale that rarely reaches the market.",
  "Kilómetros de costa virgen reunidos en un solo título — un activo generacional de una escala que rara vez llega al mercado."),
 (">Development Land</span>", ">Suelo urbanizable</span>"),
 ("<h3>Coastal Development Land</h3>", "<h3>Suelo costero urbanizable</h3>"),
 ("11,000,000+ m&sup2; — Dominican Republic", "11,000,000+ m&sup2; — República Dominicana"),
 ("Over eleven million square meters of coastal territory, master-plan ready — for institutions building at the scale of entire destinations.",
  "Más de once millones de metros cuadrados de territorio costero, listos para plan maestro — para instituciones que construyen a la escala de destinos enteros."),
 (">Resorts &amp; Hotels</span>", ">Resorts y hoteles</span>"),
 ("<h3>Resort &amp; Hotel Developments</h3>", "<h3>Desarrollos de resorts y hoteles</h3>"),
 (">Turnkey structuring</p>", ">Estructuración llave en mano</p>"),
 ("From land acquisition to operating brand — hospitality developments structured end to end with our capital and operating partners.",
  "De la adquisición del suelo a la marca operadora — desarrollos hoteleros estructurados de principio a fin con nuestros socios de capital y de operación."),
 (">Price upon application<", ">Precio a consultar<"),
 (">Enquire</a>", ">Consultar</a>"),
 # SECTION 02
 ("Properties — <span>Buy &amp; Sell</span>", "Propiedades — <span>compra y venta</span>"),
 ("A Curated Portfolio of <br /> Exceptional Homes", "Una selección curada de <br /> residencias excepcionales"),
 ("<span>View All Properties</span>", "<span>Ver todas las propiedades</span>"),
 ('alt="Property Image"', 'alt="Imagen de la propiedad"'),
 (">Serene Palm Villa</a", ">Villa Palma Serena</a"),
 (">The Thames Penthouse</a", ">Ático del Támesis</a"),
 (">Villa Lariana</a", ">Villa Lariana</a"),
 (">Casa Selva</a", ">Casa Selva</a"),
 (">Villa Alborada</a", ">Villa Alborada</a"),
 (">Ático Reforma</a", ">Ático Reforma</a"),
 ("Palm Jumeirah, Dubai, United Arab Emirates", "Palm Jumeirah, Dubái, Emiratos Árabes Unidos"),
 ("Westminster, London, United Kingdom", "Westminster, Londres, Reino Unido"),
 ("Lake Como, Lombardy, Italy", "Lago de Como, Lombardía, Italia"),
 ("Tulum, Quintana Roo, México", "Tulum, Quintana Roo, México"),
 ("Golden Mile, Marbella, Spain", "Milla de Oro, Marbella, España"),
 ("Polanco, Mexico City, México", "Polanco, Ciudad de México, México"),
 (">Bed 3<", ">3 dorm.<"), (">Bed 4<", ">4 dorm.<"), (">Bed 5<", ">5 dorm.<"), (">Bed 6<", ">6 dorm.<"),
 (">Bath 3<", ">3 baños<"), (">Bath 4<", ">4 baños<"), (">Bath 7<", ">7 baños<"),
 (">1200 Sqft<", ">1200 pie²<"), (">1300 Sqft<", ">1300 pie²<"), (">1500 Sqft<", ">1500 pie²<"),
 (">2100 Sqft<", ">2100 pie²<"), (">1800 Sqft<", ">1800 pie²<"),
 ("<span>View Details</span>", "<span>Ver detalles</span>"),
 # SECTION 03
 ("Investment &amp; <span>Funds</span>", "Inversión y <span>fondos</span>"),
 ("Structured Routes for Investors <br /> and Institutional Capital", "Vías estructuradas para inversores <br /> y capital institucional"),
 (">Investment Routes</h3>", ">Vías de inversión</h3>"),
 ("Access curated real estate opportunities across prime global markets, from single assets to diversified income portfolios.",
  "Acceda a oportunidades inmobiliarias seleccionadas en los principales mercados globales, desde activos individuales hasta carteras de renta diversificadas."),
 ("Fund &amp; Vehicle Structuring", "Estructuración de fondos y vehículos"),
 ("Design of investment vehicles and holding structures aligned with each mandate, jurisdiction and governance requirement.",
  "Diseño de vehículos de inversión y estructuras de holding alineados con cada mandato, jurisdicción y requisito de gobernanza."),
 (">Institutional Advisory</h3>", ">Asesoría institucional</h3>"),
 ("Discreet, end-to-end advisory for family offices and funds — sourcing, due diligence, execution and asset stewardship.",
  "Asesoría discreta e integral para family offices y fondos — originación, diligencia debida, ejecución y custodia de activos."),
 # SECTION 04
 ("For <span>Developers</span>", "Para <span>promotores</span>"),
 ("Capital and Articulation <br /> for Ambitious Projects", "Capital y articulación <br /> para proyectos ambiciosos"),
 ("We connect developers with the capital, partners and expertise required to take a project from land to landmark — structuring, positioning and international distribution under one roof.",
  "Conectamos a los promotores con el capital, los socios y la experiencia necesarios para llevar un proyecto del suelo a hito — estructuración, posicionamiento y distribución internacional bajo un mismo techo."),
 ("<span>Present Your Project</span>", "<span>Presente su proyecto</span>"),
 (">Capital Structuring</h3>", ">Estructuración de capital</h3>"),
 ("Equity, debt and hybrid structures matched to the profile and stage of each development.",
  "Estructuras de capital, deuda e híbridas ajustadas al perfil y la etapa de cada desarrollo."),
 (">Project Articulation</h3>", ">Articulación de proyectos</h3>"),
 ("Concept, partners, licensing and delivery coordinated across every phase of the project.",
  "Concepto, socios, licencias y entrega coordinados en cada fase del proyecto."),
 (">Global Distribution</h3>", ">Distribución global</h3>"),
 ("International sales positioning through our network across four continents.",
  "Posicionamiento de ventas internacional a través de nuestra red en cuatro continentes."),
 # SECTION 05
 ("Relocation &amp; <span>Corporate Services</span>", "Relocalización y <span>servicios corporativos</span>"),
 ("Arrive as a Guest. <br /> Settle as a Resident.", "Llegue como huésped. <br /> Establézcase como residente."),
 (">Corporate Service Providers</h3>", ">Proveedores de servicios corporativos</h3>"),
 ("Company set-up, banking introductions and ongoing corporate administration through trusted providers in each jurisdiction.",
  "Constitución de sociedades, presentaciones bancarias y administración corporativa continua a través de proveedores de confianza en cada jurisdicción."),
 ("Migration &amp; Residency", "Migración y residencia"),
 ("Guidance across residency and visa pathways, coordinated with specialised legal counsel from application to approval.",
  "Acompañamiento en las vías de residencia y visado, coordinado con asesoría legal especializada desde la solicitud hasta la aprobación."),
 (">Complete Installation</h3>", ">Instalación completa</h3>"),
 ("Home search, schooling, staff and lifestyle management — a full landing service for families and executives.",
  "Búsqueda de vivienda, escolarización, personal y gestión del estilo de vida — un servicio integral de aterrizaje para familias y ejecutivos."),
 # SECTION 06
 ("Signature <span>Projects</span>", "Proyectos <span>emblemáticos</span>"),
 ("Master Developments in Motion", "Desarrollos maestros en marcha"),
 ('alt="ASHIMA — aerial view of the territory, Oaxaca, Mexico"', 'alt="ASHIMA — vista aérea del territorio, Oaxaca, México"'),
 ("Ancestral Odyssey — Oaxaca, M&eacute;xico", "Odisea ancestral — Oaxaca, México"),
 ("A sanctuary-scale master development where ancestral local culture meets contemporary design — private residences conceived around wellness, community and the living heritage of Oaxaca.",
  "Un desarrollo maestro a escala de santuario donde la cultura local ancestral se encuentra con el diseño contemporáneo — residencias privadas concebidas en torno al bienestar, la comunidad y el patrimonio vivo de Oaxaca."),
 (">Health &amp; Wellness</span>", ">Salud y bienestar</span>"),
 (">Ancestral Local Culture</span>", ">Cultura local ancestral</span>"),
 (">Eco-Friendly</span>", ">Ecológico</span>"),
 (">Innovation</span>", ">Innovación</span>"),
 (">Sustainable Development</span>", ">Desarrollo sostenible</span>"),
 ("<span>Request the Private Brief</span>", "<span>Solicite el dossier privado</span>"),
 (">The Pavilion</span>", ">El pabellón</span>"),
 ("Architecture That Belongs <br /> to Its Territory", "Arquitectura que pertenece <br /> a su territorio"),
 ("The first built expression of ASHIMA — a pavilion raised from local materials and ancestral technique, setting the standard for every residence that follows.",
  "La primera expresión construida de ASHIMA — un pabellón levantado con materiales locales y técnica ancestral, que marca el estándar para cada residencia que le sigue."),
 (">See the Full Project<", ">Ver el proyecto completo<"),
 ('alt="ASHIMA pavilion — architectural detail"', 'alt="Pabellón ASHIMA — detalle arquitectónico"'),
 # SECTION 07 — Digital Assets (compliance, exact rigor)
 ("Digital <span>Assets</span>", "Activos <span>digitales</span>"),
 ('alt="XARU monogram"', 'alt="Monograma XARU"'),
 ("Property, Settled with Precision", "Propiedad, liquidada con precisión"),
 ("For qualifying clients, our specialized team facilitates property acquisition using digital assets (USDC, USDT, BTC) exclusively through regulated channels, with full KYC/AML verification and legal counsel in every jurisdiction.",
  "Para clientes que cumplen los requisitos, nuestro equipo especializado facilita la adquisición de propiedades mediante activos digitales (USDC, USDT, BTC) exclusivamente a través de canales regulados, con verificación KYC/AML completa y asesoría legal en cada jurisdicción."),
 # SECTION 08 — About
 ("About — <span>The Company</span>", "Nosotros — <span>la compañía</span>"),
 ("One Structure, <br /> Built on Five Pillars", "Una sola estructura, <br /> sobre cinco pilares"),
 ("<span>Learn More</span>", "<span>Saber más</span>"),
 ('alt="About XARU HOME"', 'alt="Acerca de XARU HOME"'),
 ("For more than <strong>20 years</strong>, our team has guided private clients, families and institutions through significant real estate decisions. XARU HOME brings that experience into one structure — a NEXARU GLOBAL brand connecting acquisition, investment, development and relocation, worldwide.",
  "Durante más de <strong>20 años</strong>, nuestro equipo ha acompañado a clientes privados, familias e instituciones en decisiones inmobiliarias significativas. XARU HOME reúne esa experiencia en una sola estructura — una marca de NEXARU GLOBAL que conecta adquisición, inversión, desarrollo y relocalización, en todo el mundo."),
 ("Our network spans the United Arab Emirates and the Middle East, China, India, Pakistan, Europe, the United States and Latin America.",
  "Nuestra red abarca los Emiratos Árabes Unidos y Oriente Medio, China, India, Pakistán, Europa, Estados Unidos y América Latina."),
 (">UAE</span>", ">EAU</span>"), (">Middle East</span>", ">Oriente Medio</span>"),
 (">China</span>", ">China</span>"), (">India</span>", ">India</span>"),
 (">Pakistan</span>", ">Pakistán</span>"), (">Europe</span>", ">Europa</span>"),
 (">USA</span>", ">EE. UU.</span>"), (">LatAm</span>", ">Latinoamérica</span>"),
 (">Years of Experience</span>", ">Años de experiencia</span>"),
 (">Continents Covered</span>", ">Continentes cubiertos</span>"),
 (">Land Under Structuring</span>", ">Suelo en estructuración</span>"),
 (">Founding Pillars</span>", ">Pilares fundacionales</span>"),
 (">Health &amp; Wellness</h3>", ">Salud y bienestar</h3>"),
 ("Spaces designed for wellbeing, from concept to daily life.", "Espacios diseñados para el bienestar, del concepto a la vida cotidiana."),
 (">Ancestral Local Culture</h3>", ">Cultura local ancestral</h3>"),
 ("Projects rooted in the heritage of the places they inhabit.", "Proyectos arraigados en el patrimonio de los lugares que habitan."),
 (">Eco-Friendly</h3>", ">Ecológico</h3>"),
 ("Responsible materials, energy and construction practices.", "Materiales, energía y prácticas de construcción responsables."),
 (">Innovation</h3>", ">Innovación</h3>"),
 ("Technology and design at the service of timeless living.", "Tecnología y diseño al servicio de un vivir atemporal."),
 (">Sustainable Development</h3>", ">Desarrollo sostenible</h3>"),
 ("Long-term value for owners, communities and the land.", "Valor a largo plazo para propietarios, comunidades y territorio."),
 # SECTION 09 — CTA
 ("Begin with <span style=\"color:#C9A876\">XARU</span>", "Comience con <span style=\"color:#C9A876\">XARU</span>"),
 ("Begin the Conversation, <br /> in Complete Confidence.", "Inicie la conversación, <br /> con total confidencialidad."),
 ("<span>Contact Us</span>", "<span>Contáctenos</span>"),
 # FOOTER
 ("Global luxury real estate, one structure — from acquisition to relocation, worldwide.",
  "Bienes raíces de lujo globales, una sola estructura — de la adquisición a la relocalización, en todo el mundo."),
 ("> Explore </h3>", ">Explorar</h3>"),
 (">Investment &amp; Funds</a>", ">Inversión y fondos</a>"),
 ("> Company </h3>", ">Compañía</h3>"),
 (">Digital Assets</a>", ">Activos digitales</a>"),
 ("> Newsletter </h3>", ">Boletín</h3>"),
 ('placeholder="Enter Email Address"', 'placeholder="Introduzca su correo electrónico"'),
 ("XARU HOME — a NEXARU GLOBAL brand. Licensed in the United Arab Emirates.",
  "XARU HOME — una marca de NEXARU GLOBAL. Con licencia en los Emiratos Árabes Unidos."),
 # ARIA labels
 ('aria-label="Nav link"', 'aria-label="Enlace de navegación"'),
 ('aria-label="Home page link"', 'aria-label="Enlace a la página de inicio"'),
 ('aria-label="Contact page link"', 'aria-label="Enlace a la página de contacto"'),
 ('aria-label="Contact link"', 'aria-label="Enlace de contacto"'),
 ('aria-label="Private enquiry link"', 'aria-label="Enlace de consulta privada"'),
 ('aria-label="Explore opportunities link"', 'aria-label="Enlace para explorar oportunidades"'),
 ('aria-label="View land and developments link"', 'aria-label="Enlace para ver suelo y desarrollos"'),
 ('aria-label="Enquire link"', 'aria-label="Enlace para consultar"'),
 ('aria-label="View property details link"', 'aria-label="Enlace para ver los detalles de la propiedad"'),
 ('aria-label="View all property link"', 'aria-label="Enlace para ver todas las propiedades"'),
 ('aria-label="View projects link"', 'aria-label="Enlace para ver los proyectos"'),
 ('aria-label="Gallery link"', 'aria-label="Enlace de la galería"'),
 ('aria-label="About page link"', 'aria-label="Enlace a la página Nosotros"'),
 ('aria-label="View contact page link"', 'aria-label="Enlace a la página de contacto"'),
 ('aria-label="Footer menu link"', 'aria-label="Enlace del menú del pie de página"'),
]

# ---------------------------------------------------------------- AR dict
AR = [
 (">Opportunities</a>", ">الفرص</a>"),
 (">Properties</a>", ">العقارات</a>"),
 (">Investment</a>", ">الاستثمار</a>"),
 (">Developers</a>", ">المطوّرون</a>"),
 (">Relocation</a>", ">الانتقال</a>"),
 (">Projects</a>", ">المشاريع</a>"),
 (">About</a>", ">من نحن</a>"),
 (">Contact</a>", ">اتصل بنا</a>"),
 ("<span>Private Enquiry</span>", "<span>استفسار خاص</span>"),
 ('data-text="XARU HOME | Global Luxury | Loading"', 'data-text="XARU HOME | فخامة عالمية | جارٍ التحميل"'),
 ('alt="XARU HOME monogram"', 'alt="شعار XARU HOME"'),
 ("<h1>Global Real Estate <br />at Its Highest Scale.</h1>", "<h1>عقارات عالمية <br />على أرفع مستوى.</h1>"),
 ("A NEXARU GLOBAL brand — private islands, master developments, and the world&rsquo;s most exceptional properties.",
  "علامة من NEXARU GLOBAL — جزر خاصة ومشاريع تطوير كبرى وأكثر عقارات العالم تميّزاً."),
 ('data-text="Private Islands | Master Developments | Hotels &amp; Resorts | Exceptional Homes"',
  'data-text="جزر خاصة | مشاريع تطوير كبرى | فنادق ومنتجعات | منازل استثنائية"'),
 (">Private Islands</span", ">جزر خاصة</span"),
 ("Explore Opportunities", "استكشف الفرص"),
 ("Private Enquiry", "استفسار خاص"),
 ("<h2>A Private Island &mdash; <br />Isola del Faro.</h2>", "<h2>جزيرة خاصة &mdash; <br /><span dir=\"ltr\">Isola del Faro.</span></h2>"),
 ("Whole island under a single title &middot; $42,000,000",
  "جزيرة كاملة بسند ملكية واحد &middot; <span dir=\"ltr\">$42,000,000</span>"),
 ("View the Asset", "عرض الأصل"),
 ("<h1>Master Developments, <br />From Land to Legacy.</h1>", "<h1>مشاريع كبرى، <br />من الأرض إلى الإرث.</h1>"),
 ("ASHIMA — Ancestral Odyssey · Oaxaca, M&eacute;xico", "ASHIMA — رحلة الأجداد · واخاكا، المكسيك"),
 ("Discover the Project", "اكتشف المشروع"),
 ('<span class="xr_social_title">Social Media</span>', '<span class="xr_social_title">وسائل التواصل</span>'),
 ('aria-label="Previous slide">Prev<', 'aria-label="الشريحة السابقة">السابق<'),
 ('aria-label="Next slide">Next<', 'aria-label="الشريحة التالية">التالي<'),
 ('<span class="xr_hero_scroll">Scroll</span>', '<span class="xr_hero_scroll">مرِّر</span>'),
 ("Land &amp; <span>Large-Scale Developments</span>", "الأراضي و<span>المشاريع الكبرى</span>"),
 ("Opportunities Measured <br /> in Kilometers, Not Meters", "فرص تُقاس <br /> بالكيلومترات، لا بالأمتار"),
 (">View the Full Portfolio<", ">استعرض المحفظة كاملةً<"),
 (">Private Island</span>", ">جزيرة خاصة</span>"),
 ("<h3>Private Island — Saman&aacute; Bay</h3>", "<h3>جزيرة خاصة — خليج سامانا</h3>"),
 (">Dominican Republic</p>", ">جمهورية الدومينيكان</p>"),
 ("Kilometers of pristine beachfront held in a single title — a generational asset of a scale that rarely reaches the market.",
  "كيلومترات من الشاطئ البِكر ضمن سند ملكية واحد — أصل يُورَّث عبر الأجيال بحجم نادراً ما يصل إلى السوق."),
 (">Development Land</span>", ">أرض للتطوير</span>"),
 ("<h3>Coastal Development Land</h3>", "<h3>أرض تطوير ساحلية</h3>"),
 ("11,000,000+ m&sup2; — Dominican Republic", "+11,000,000 m&sup2; — جمهورية الدومينيكان"),
 ("Over eleven million square meters of coastal territory, master-plan ready — for institutions building at the scale of entire destinations.",
  "أكثر من أحد عشر مليون متر مربع من الأراضي الساحلية، جاهزة للمخطط الرئيسي — لمؤسسات تبني على مقياس وجهات بأكملها."),
 (">Resorts &amp; Hotels</span>", ">منتجعات وفنادق</span>"),
 ("<h3>Resort &amp; Hotel Developments</h3>", "<h3>تطوير المنتجعات والفنادق</h3>"),
 (">Turnkey structuring</p>", ">هيكلة متكاملة جاهزة</p>"),
 ("From land acquisition to operating brand — hospitality developments structured end to end with our capital and operating partners.",
  "من شراء الأرض إلى العلامة المُشغِّلة — مشاريع ضيافة مُهيكَلة من البداية إلى النهاية مع شركائنا في رأس المال والتشغيل."),
 (">Price upon application<", ">السعر عند الطلب<"),
 (">Enquire</a>", ">استفسر</a>"),
 ("Properties — <span>Buy &amp; Sell</span>", "العقارات — <span>بيع وشراء</span>"),
 ("A Curated Portfolio of <br /> Exceptional Homes", "مجموعة منتقاة من <br /> المنازل الاستثنائية"),
 ("<span>View All Properties</span>", "<span>عرض جميع العقارات</span>"),
 ('alt="Property Image"', 'alt="صورة العقار"'),
 (">Serene Palm Villa</a", ">فيلا النخيل الهادئة</a"),
 (">The Thames Penthouse</a", ">بنتهاوس التايمز</a"),
 (">Villa Lariana</a", ">فيلا لاريانا</a"),
 (">Casa Selva</a", ">كازا سيلفا</a"),
 (">Villa Alborada</a", ">فيلا ألبورادا</a"),
 (">Ático Reforma</a", ">أتيكو ريفورما</a"),
 ("Palm Jumeirah, Dubai, United Arab Emirates", "نخلة جميرا، دبي، الإمارات العربية المتحدة"),
 ("Westminster, London, United Kingdom", "وستمنستر، لندن، المملكة المتحدة"),
 ("Lake Como, Lombardy, Italy", "بحيرة كومو، لومبارديا، إيطاليا"),
 ("Tulum, Quintana Roo, México", "تولوم، كوينتانا رو، المكسيك"),
 ("Golden Mile, Marbella, Spain", "الميل الذهبي، ماربيا، إسبانيا"),
 ("Polanco, Mexico City, México", "بولانكو، مكسيكو سيتي، المكسيك"),
 (">Bed 3<", ">3 غرف نوم<"), (">Bed 4<", ">4 غرف نوم<"), (">Bed 5<", ">5 غرف نوم<"), (">Bed 6<", ">6 غرف نوم<"),
 (">Bath 3<", ">3 حمّامات<"), (">Bath 4<", ">4 حمّامات<"), (">Bath 7<", ">7 حمّامات<"),
 (">1200 Sqft<", ">1200 قدم²<"), (">1300 Sqft<", ">1300 قدم²<"), (">1500 Sqft<", ">1500 قدم²<"),
 (">2100 Sqft<", ">2100 قدم²<"), (">1800 Sqft<", ">1800 قدم²<"),
 ("<span>View Details</span>", "<span>عرض التفاصيل</span>"),
 ("Investment &amp; <span>Funds</span>", "الاستثمار و<span>الصناديق</span>"),
 ("Structured Routes for Investors <br /> and Institutional Capital", "مسارات مُهيكَلة للمستثمرين <br /> ورأس المال المؤسسي"),
 (">Investment Routes</h3>", ">مسارات الاستثمار</h3>"),
 ("Access curated real estate opportunities across prime global markets, from single assets to diversified income portfolios.",
  "الوصول إلى فرص عقارية منتقاة في أبرز الأسواق العالمية، من الأصول الفردية إلى محافظ الدخل المتنوّعة."),
 ("Fund &amp; Vehicle Structuring", "هيكلة الصناديق والأوعية الاستثمارية"),
 ("Design of investment vehicles and holding structures aligned with each mandate, jurisdiction and governance requirement.",
  "تصميم أوعية استثمارية وهياكل قابضة تتوافق مع كل تفويض وولاية قضائية ومتطلبات الحوكمة."),
 (">Institutional Advisory</h3>", ">الاستشارات المؤسسية</h3>"),
 ("Discreet, end-to-end advisory for family offices and funds — sourcing, due diligence, execution and asset stewardship.",
  "استشارات متكاملة وسرّية للمكاتب العائلية والصناديق — التوريد والعناية الواجبة والتنفيذ ورعاية الأصول."),
 ("For <span>Developers</span>", "لـ<span>المطوّرين</span>"),
 ("Capital and Articulation <br /> for Ambitious Projects", "رأس المال والتنسيق <br /> للمشاريع الطموحة"),
 ("We connect developers with the capital, partners and expertise required to take a project from land to landmark — structuring, positioning and international distribution under one roof.",
  "نربط المطوّرين برأس المال والشركاء والخبرة اللازمة لنقل المشروع من الأرض إلى معلَم بارز — الهيكلة والتموضع والتوزيع الدولي تحت سقف واحد."),
 ("<span>Present Your Project</span>", "<span>قدّم مشروعك</span>"),
 (">Capital Structuring</h3>", ">هيكلة رأس المال</h3>"),
 ("Equity, debt and hybrid structures matched to the profile and stage of each development.",
  "هياكل ملكية ودَين وهجينة تُواءَم مع طبيعة كل مشروع ومرحلته."),
 (">Project Articulation</h3>", ">تنسيق المشاريع</h3>"),
 ("Concept, partners, licensing and delivery coordinated across every phase of the project.",
  "المفهوم والشركاء والتراخيص والتسليم بتنسيق عبر كل مرحلة من مراحل المشروع."),
 (">Global Distribution</h3>", ">التوزيع العالمي</h3>"),
 ("International sales positioning through our network across four continents.",
  "تموضع مبيعات دولي عبر شبكتنا في أربع قارات."),
 ("Relocation &amp; <span>Corporate Services</span>", "الانتقال و<span>الخدمات المؤسسية</span>"),
 ("Arrive as a Guest. <br /> Settle as a Resident.", "تصل ضيفاً. <br /> وتستقرّ مقيماً."),
 (">Corporate Service Providers</h3>", ">مزوّدو الخدمات المؤسسية</h3>"),
 ("Company set-up, banking introductions and ongoing corporate administration through trusted providers in each jurisdiction.",
  "تأسيس الشركات والتعريف المصرفي والإدارة المؤسسية المستمرة عبر مزوّدين موثوقين في كل ولاية قضائية."),
 ("Migration &amp; Residency", "الهجرة والإقامة"),
 ("Guidance across residency and visa pathways, coordinated with specialised legal counsel from application to approval.",
  "إرشاد عبر مسارات الإقامة والتأشيرات، بالتنسيق مع مستشارين قانونيين متخصّصين من التقديم حتى الموافقة."),
 (">Complete Installation</h3>", ">استقرار متكامل</h3>"),
 ("Home search, schooling, staff and lifestyle management — a full landing service for families and executives.",
  "البحث عن السكن والتعليم والطاقم وإدارة نمط الحياة — خدمة استقبال متكاملة للعائلات والتنفيذيين."),
 ("Signature <span>Projects</span>", "مشاريع <span>مميّزة</span>"),
 ("Master Developments in Motion", "مشاريع كبرى قيد التنفيذ"),
 ('alt="ASHIMA — aerial view of the territory, Oaxaca, Mexico"', 'alt="ASHIMA — منظر جوي للأرض، واخاكا، المكسيك"'),
 ("Ancestral Odyssey — Oaxaca, M&eacute;xico", "رحلة الأجداد — واخاكا، المكسيك"),
 ("A sanctuary-scale master development where ancestral local culture meets contemporary design — private residences conceived around wellness, community and the living heritage of Oaxaca.",
  "مشروع تطوير كبير بمقياس محمية، حيث تلتقي الثقافة المحلية العريقة بالتصميم المعاصر — مساكن خاصة صُمِّمت حول العافية والمجتمع والتراث الحي لواخاكا."),
 (">Health &amp; Wellness</span>", ">الصحة والعافية</span>"),
 (">Ancestral Local Culture</span>", ">ثقافة محلية عريقة</span>"),
 (">Eco-Friendly</span>", ">صديق للبيئة</span>"),
 (">Innovation</span>", ">الابتكار</span>"),
 (">Sustainable Development</span>", ">تنمية مستدامة</span>"),
 ("<span>Request the Private Brief</span>", "<span>اطلب الملف الخاص</span>"),
 (">The Pavilion</span>", ">الجناح</span>"),
 ("Architecture That Belongs <br /> to Its Territory", "عمارة تنتمي <br /> إلى أرضها"),
 ("The first built expression of ASHIMA — a pavilion raised from local materials and ancestral technique, setting the standard for every residence that follows.",
  "أول تعبير مبني عن ASHIMA — جناح شُيِّد من مواد محلية وتقنية عريقة، يرسي المعيار لكل مسكن يليه."),
 (">See the Full Project<", ">شاهد المشروع كاملاً<"),
 ('alt="ASHIMA pavilion — architectural detail"', 'alt="جناح ASHIMA — تفصيل معماري"'),
 ("Digital <span>Assets</span>", "الأصول <span>الرقمية</span>"),
 ('alt="XARU monogram"', 'alt="شعار XARU"'),
 ("Property, Settled with Precision", "تملّك يُسوّى بدقّة"),
 ("For qualifying clients, our specialized team facilitates property acquisition using digital assets (USDC, USDT, BTC) exclusively through regulated channels, with full KYC/AML verification and legal counsel in every jurisdiction.",
  "للعملاء المؤهّلين، يُيسّر فريقنا المتخصّص شراء العقارات باستخدام الأصول الرقمية (USDC، USDT، BTC) حصراً عبر قنوات مُنظَّمة، مع التحقّق الكامل وفق معايير “اعرف عميلك” ومكافحة غسل الأموال (KYC/AML) واستشارة قانونية في كل ولاية قضائية."),
 ("About — <span>The Company</span>", "من نحن — <span>الشركة</span>"),
 ("One Structure, <br /> Built on Five Pillars", "كيان واحد، <br /> يقوم على خمس ركائز"),
 ("<span>Learn More</span>", "<span>اعرف المزيد</span>"),
 ('alt="About XARU HOME"', 'alt="عن XARU HOME"'),
 ("For more than <strong>20 years</strong>, our team has guided private clients, families and institutions through significant real estate decisions. XARU HOME brings that experience into one structure — a NEXARU GLOBAL brand connecting acquisition, investment, development and relocation, worldwide.",
  "لأكثر من <strong>20 عاماً</strong>، رافق فريقنا عملاء من الأفراد والعائلات والمؤسسات في قرارات عقارية بالغة الأهمية. تجمع XARU HOME هذه الخبرة في كيان واحد — علامة من NEXARU GLOBAL تربط بين الاقتناء والاستثمار والتطوير والانتقال، حول العالم."),
 ("Our network spans the United Arab Emirates and the Middle East, China, India, Pakistan, Europe, the United States and Latin America.",
  "تمتدّ شبكتنا عبر الإمارات العربية المتحدة والشرق الأوسط والصين والهند وباكستان وأوروبا والولايات المتحدة وأمريكا اللاتينية."),
 (">UAE</span>", ">الإمارات</span>"), (">Middle East</span>", ">الشرق الأوسط</span>"),
 (">China</span>", ">الصين</span>"), (">India</span>", ">الهند</span>"),
 (">Pakistan</span>", ">باكستان</span>"), (">Europe</span>", ">أوروبا</span>"),
 (">USA</span>", ">الولايات المتحدة</span>"), (">LatAm</span>", ">أمريكا اللاتينية</span>"),
 (">Years of Experience</span>", ">سنوات من الخبرة</span>"),
 (">Continents Covered</span>", ">قارات نغطّيها</span>"),
 (">Land Under Structuring</span>", ">أراضٍ قيد الهيكلة</span>"),
 (">Founding Pillars</span>", ">ركائز تأسيسية</span>"),
 (">Health &amp; Wellness</h3>", ">الصحة والعافية</h3>"),
 ("Spaces designed for wellbeing, from concept to daily life.", "مساحات مُصمَّمة للعافية، من الفكرة إلى الحياة اليومية."),
 (">Ancestral Local Culture</h3>", ">ثقافة محلية عريقة</h3>"),
 ("Projects rooted in the heritage of the places they inhabit.", "مشاريع متجذّرة في تراث الأماكن التي تقوم فيها."),
 (">Eco-Friendly</h3>", ">صديق للبيئة</h3>"),
 ("Responsible materials, energy and construction practices.", "مواد وطاقة وممارسات بناء مسؤولة."),
 (">Innovation</h3>", ">الابتكار</h3>"),
 ("Technology and design at the service of timeless living.", "تقنية وتصميم في خدمة حياة خالدة."),
 (">Sustainable Development</h3>", ">تنمية مستدامة</h3>"),
 ("Long-term value for owners, communities and the land.", "قيمة طويلة الأمد للمُلّاك والمجتمعات والأرض."),
 ("Begin with <span style=\"color:#C9A876\">XARU</span>", "ابدأ مع <span style=\"color:#C9A876\">XARU</span>"),
 ("Begin the Conversation, <br /> in Complete Confidence.", "ابدأ الحوار، <br /> بسريّة تامة."),
 ("<span>Contact Us</span>", "<span>تواصل معنا</span>"),
 ("Global luxury real estate, one structure — from acquisition to relocation, worldwide.",
  "عقارات فاخرة عالمية، كيان واحد — من الاقتناء إلى الانتقال، حول العالم."),
 ("> Explore </h3>", ">استكشف</h3>"),
 (">Investment &amp; Funds</a>", ">الاستثمار والصناديق</a>"),
 ("> Company </h3>", ">الشركة</h3>"),
 (">Digital Assets</a>", ">الأصول الرقمية</a>"),
 ("> Newsletter </h3>", ">النشرة البريدية</h3>"),
 ('placeholder="Enter Email Address"', 'placeholder="أدخل بريدك الإلكتروني"'),
 ("XARU HOME — a NEXARU GLOBAL brand. Licensed in the United Arab Emirates.",
  "XARU HOME — علامة من NEXARU GLOBAL. مرخّصة في الإمارات العربية المتحدة."),
 ('aria-label="Nav link"', 'aria-label="رابط التنقّل"'),
 ('aria-label="Home page link"', 'aria-label="رابط الصفحة الرئيسية"'),
 ('aria-label="Contact page link"', 'aria-label="رابط صفحة الاتصال"'),
 ('aria-label="Contact link"', 'aria-label="رابط الاتصال"'),
 ('aria-label="Private enquiry link"', 'aria-label="رابط الاستفسار الخاص"'),
 ('aria-label="Explore opportunities link"', 'aria-label="رابط استكشاف الفرص"'),
 ('aria-label="View land and developments link"', 'aria-label="رابط عرض الأراضي والمشاريع"'),
 ('aria-label="Enquire link"', 'aria-label="رابط الاستفسار"'),
 ('aria-label="View property details link"', 'aria-label="رابط عرض تفاصيل العقار"'),
 ('aria-label="View all property link"', 'aria-label="رابط عرض جميع العقارات"'),
 ('aria-label="View projects link"', 'aria-label="رابط عرض المشاريع"'),
 ('aria-label="Gallery link"', 'aria-label="رابط المعرض"'),
 ('aria-label="About page link"', 'aria-label="رابط صفحة من نحن"'),
 ('aria-label="View contact page link"', 'aria-label="رابط صفحة الاتصال"'),
 ('aria-label="Footer menu link"', 'aria-label="رابط قائمة التذييل"'),
]

# ---------------------------------------------------------------- ZH dict
ZH = [
 (">Opportunities</a>", ">机遇</a>"),
 (">Properties</a>", ">房产</a>"),
 (">Investment</a>", ">投资</a>"),
 (">Developers</a>", ">开发商</a>"),
 (">Relocation</a>", ">移居</a>"),
 (">Projects</a>", ">项目</a>"),
 (">About</a>", ">关于我们</a>"),
 (">Contact</a>", ">联系我们</a>"),
 ("<span>Private Enquiry</span>", "<span>私人咨询</span>"),
 ('data-text="XARU HOME | Global Luxury | Loading"', 'data-text="XARU HOME | 全球奢华 | 加载中"'),
 ('alt="XARU HOME monogram"', 'alt="XARU HOME 标识"'),
 ("<h1>Global Real Estate <br />at Its Highest Scale.</h1>", "<h1>全球房产 <br />臻于至高格局。</h1>"),
 ("A NEXARU GLOBAL brand — private islands, master developments, and the world&rsquo;s most exceptional properties.",
  "NEXARU GLOBAL 旗下品牌——私人岛屿、大型综合开发项目，以及世界上最卓越的房产。"),
 ('data-text="Private Islands | Master Developments | Hotels &amp; Resorts | Exceptional Homes"',
  'data-text="私人岛屿 | 大型开发项目 | 酒店与度假村 | 卓越宅邸"'),
 (">Private Islands</span", ">私人岛屿</span"),
 ("Explore Opportunities", "探索机遇"),
 ("Private Enquiry", "私人咨询"),
 ("<h2>A Private Island &mdash; <br />Isola del Faro.</h2>", "<h2>私人岛屿 &mdash; <br />Isola del Faro。</h2>"),
 ("Whole island under a single title &middot; $42,000,000",
  "整岛单一产权 &middot; $42,000,000"),
 ("View the Asset", "查看资产"),
 ("<h1>Master Developments, <br />From Land to Legacy.</h1>", "<h1>大型开发项目， <br />从土地到传世之作。</h1>"),
 ("ASHIMA — Ancestral Odyssey · Oaxaca, M&eacute;xico", "ASHIMA — 先祖之旅 · 墨西哥瓦哈卡"),
 ("Discover the Project", "了解该项目"),
 ('<span class="xr_social_title">Social Media</span>', '<span class="xr_social_title">社交媒体</span>'),
 ('aria-label="Previous slide">Prev<', 'aria-label="上一张幻灯片">上一张<'),
 ('aria-label="Next slide">Next<', 'aria-label="下一张幻灯片">下一张<'),
 ('<span class="xr_hero_scroll">Scroll</span>', '<span class="xr_hero_scroll">滚动</span>'),
 ("Land &amp; <span>Large-Scale Developments</span>", "土地与<span>大型开发项目</span>"),
 ("Opportunities Measured <br /> in Kilometers, Not Meters", "以公里计， <br /> 而非以米计的机遇"),
 (">View the Full Portfolio<", ">查看完整项目组合<"),
 (">Private Island</span>", ">私人岛屿</span>"),
 ("<h3>Private Island — Saman&aacute; Bay</h3>", "<h3>私人岛屿——萨马纳湾</h3>"),
 (">Dominican Republic</p>", ">多米尼加共和国</p>"),
 ("Kilometers of pristine beachfront held in a single title — a generational asset of a scale that rarely reaches the market.",
  "数公里原生海岸线归于单一产权之下——一项世代传承的资产，其规模在市场上极为罕见。"),
 (">Development Land</span>", ">开发用地</span>"),
 ("<h3>Coastal Development Land</h3>", "<h3>沿海开发用地</h3>"),
 ("11,000,000+ m&sup2; — Dominican Republic", "11,000,000+ m&sup2; — 多米尼加共和国"),
 ("Over eleven million square meters of coastal territory, master-plan ready — for institutions building at the scale of entire destinations.",
  "逾一千一百万平方米的沿海土地，已具备总体规划条件——面向以整座目的地为尺度进行建设的机构。"),
 (">Resorts &amp; Hotels</span>", ">度假村与酒店</span>"),
 ("<h3>Resort &amp; Hotel Developments</h3>", "<h3>度假村与酒店开发</h3>"),
 (">Turnkey structuring</p>", ">交钥匙式架构</p>"),
 ("From land acquisition to operating brand — hospitality developments structured end to end with our capital and operating partners.",
  "从土地收购到运营品牌——酒店业开发项目由我们的资本与运营伙伴全程架构。"),
 (">Price upon application<", ">价格面议<"),
 (">Enquire</a>", ">咨询</a>"),
 ("Properties — <span>Buy &amp; Sell</span>", "房产——<span>买卖</span>"),
 ("A Curated Portfolio of <br /> Exceptional Homes", "精选的 <br /> 卓越宅邸组合"),
 ("<span>View All Properties</span>", "<span>查看全部房产</span>"),
 ('alt="Property Image"', 'alt="房产图片"'),
 (">Serene Palm Villa</a", ">静谧棕榈别墅</a"),
 (">The Thames Penthouse</a", ">泰晤士顶层公寓</a"),
 (">Villa Lariana</a", ">拉里安纳别墅</a"),
 (">Casa Selva</a", ">丛林之宅</a"),
 (">Villa Alborada</a", ">晨曦别墅</a"),
 (">Ático Reforma</a", ">改革大道顶层公寓</a"),
 ("Palm Jumeirah, Dubai, United Arab Emirates", "朱美拉棕榈岛，迪拜，阿拉伯联合酋长国"),
 ("Westminster, London, United Kingdom", "威斯敏斯特，伦敦，英国"),
 ("Lake Como, Lombardy, Italy", "科莫湖，伦巴第，意大利"),
 ("Tulum, Quintana Roo, México", "图卢姆，金塔纳罗奥州，墨西哥"),
 ("Golden Mile, Marbella, Spain", "黄金一英里，马贝拉，西班牙"),
 ("Polanco, Mexico City, México", "波兰科，墨西哥城，墨西哥"),
 (">Bed 3<", ">3 卧室<"), (">Bed 4<", ">4 卧室<"), (">Bed 5<", ">5 卧室<"), (">Bed 6<", ">6 卧室<"),
 (">Bath 3<", ">3 卫浴<"), (">Bath 4<", ">4 卫浴<"), (">Bath 7<", ">7 卫浴<"),
 (">1200 Sqft<", ">1200 平方英尺<"), (">1300 Sqft<", ">1300 平方英尺<"), (">1500 Sqft<", ">1500 平方英尺<"),
 (">2100 Sqft<", ">2100 平方英尺<"), (">1800 Sqft<", ">1800 平方英尺<"),
 ("<span>View Details</span>", "<span>查看详情</span>"),
 ("Investment &amp; <span>Funds</span>", "投资与<span>基金</span>"),
 ("Structured Routes for Investors <br /> and Institutional Capital", "面向投资者 <br /> 与机构资本的结构化路径"),
 (">Investment Routes</h3>", ">投资路径</h3>"),
 ("Access curated real estate opportunities across prime global markets, from single assets to diversified income portfolios.",
  "于全球核心市场获取精选房产机遇，从单一资产到多元化收益组合。"),
 ("Fund &amp; Vehicle Structuring", "基金与投资载体架构"),
 ("Design of investment vehicles and holding structures aligned with each mandate, jurisdiction and governance requirement.",
  "依据各项委托、司法管辖区及治理要求，设计投资载体与控股架构。"),
 (">Institutional Advisory</h3>", ">机构顾问</h3>"),
 ("Discreet, end-to-end advisory for family offices and funds — sourcing, due diligence, execution and asset stewardship.",
  "为家族办公室与基金提供审慎、全程的顾问服务——项目寻源、尽职调查、执行及资产托管。"),
 ("For <span>Developers</span>", "致<span>开发商</span>"),
 ("Capital and Articulation <br /> for Ambitious Projects", "为宏图之作 <br /> 提供资本与统筹"),
 ("We connect developers with the capital, partners and expertise required to take a project from land to landmark — structuring, positioning and international distribution under one roof.",
  "我们为开发商对接将项目从土地打造为地标所需的资本、伙伴与专业能力——架构、定位与国际分销，皆汇于一处。"),
 ("<span>Present Your Project</span>", "<span>呈递您的项目</span>"),
 (">Capital Structuring</h3>", ">资本架构</h3>"),
 ("Equity, debt and hybrid structures matched to the profile and stage of each development.",
  "依据各开发项目的特性与阶段，匹配股权、债权及混合架构。"),
 (">Project Articulation</h3>", ">项目统筹</h3>"),
 ("Concept, partners, licensing and delivery coordinated across every phase of the project.",
  "概念、伙伴、许可与交付，贯穿项目各阶段协同推进。"),
 (">Global Distribution</h3>", ">全球分销</h3>"),
 ("International sales positioning through our network across four continents.",
  "通过遍及四大洲的网络进行国际销售定位。"),
 ("Relocation &amp; <span>Corporate Services</span>", "移居与<span>企业服务</span>"),
 ("Arrive as a Guest. <br /> Settle as a Resident.", "以宾客之姿抵达， <br /> 以居民之身安居。"),
 (">Corporate Service Providers</h3>", ">企业服务供应商</h3>"),
 ("Company set-up, banking introductions and ongoing corporate administration through trusted providers in each jurisdiction.",
  "通过各司法管辖区的可信供应商，提供公司设立、银行引荐及持续的企业行政管理。"),
 ("Migration &amp; Residency", "移民与居留"),
 ("Guidance across residency and visa pathways, coordinated with specialised legal counsel from application to approval.",
  "就居留与签证路径提供指导，并与专业法律顾问协同，从申请到获批全程相伴。"),
 (">Complete Installation</h3>", ">全面安置</h3>"),
 ("Home search, schooling, staff and lifestyle management — a full landing service for families and executives.",
  "觅居、就学、家政人员与生活方式管理——为家庭与高管提供的一站式落地服务。"),
 ("Signature <span>Projects</span>", "标志性<span>项目</span>"),
 ("Master Developments in Motion", "进行中的大型开发项目"),
 ('alt="ASHIMA — aerial view of the territory, Oaxaca, Mexico"', 'alt="ASHIMA — 领地鸟瞰，墨西哥瓦哈卡"'),
 ("Ancestral Odyssey — Oaxaca, M&eacute;xico", "先祖之旅——墨西哥瓦哈卡"),
 ("A sanctuary-scale master development where ancestral local culture meets contemporary design — private residences conceived around wellness, community and the living heritage of Oaxaca.",
  "一处圣境规模的大型开发项目，先祖本土文化于此邂逅当代设计——私人宅邸围绕康养、社群及瓦哈卡的鲜活传承而构想。"),
 (">Health &amp; Wellness</span>", ">健康与康养</span>"),
 (">Ancestral Local Culture</span>", ">先祖本土文化</span>"),
 (">Eco-Friendly</span>", ">生态友好</span>"),
 (">Innovation</span>", ">创新</span>"),
 (">Sustainable Development</span>", ">可持续发展</span>"),
 ("<span>Request the Private Brief</span>", "<span>索取私人简报</span>"),
 (">The Pavilion</span>", ">展亭</span>"),
 ("Architecture That Belongs <br /> to Its Territory", "归属于其 <br /> 土地的建筑"),
 ("The first built expression of ASHIMA — a pavilion raised from local materials and ancestral technique, setting the standard for every residence that follows.",
  "ASHIMA 首个落成的实体呈现——一座以本土材料与先祖工艺筑就的展亭，为其后每一座宅邸树立标准。"),
 (">See the Full Project<", ">查看完整项目<"),
 ('alt="ASHIMA pavilion — architectural detail"', 'alt="ASHIMA 展亭——建筑细部"'),
 ("Digital <span>Assets</span>", "数字<span>资产</span>"),
 ('alt="XARU monogram"', 'alt="XARU 标识"'),
 ("Property, Settled with Precision", "房产交割，精准无误"),
 ("For qualifying clients, our specialized team facilitates property acquisition using digital assets (USDC, USDT, BTC) exclusively through regulated channels, with full KYC/AML verification and legal counsel in every jurisdiction.",
  "对于符合资格的客户，我们的专业团队协助以数字资产（USDC、USDT、BTC）完成房产收购，且仅通过受监管渠道进行，并在每一司法管辖区实施完整的 KYC/AML 核查并提供法律顾问。"),
 ("About — <span>The Company</span>", "关于——<span>本公司</span>"),
 ("One Structure, <br /> Built on Five Pillars", "单一架构， <br /> 立于五大支柱"),
 ("<span>Learn More</span>", "<span>了解更多</span>"),
 ('alt="About XARU HOME"', 'alt="关于 XARU HOME"'),
 ("For more than <strong>20 years</strong>, our team has guided private clients, families and institutions through significant real estate decisions. XARU HOME brings that experience into one structure — a NEXARU GLOBAL brand connecting acquisition, investment, development and relocation, worldwide.",
  "逾 <strong>20 年</strong>来，我们的团队指导私人客户、家族与机构做出重大的房产决策。XARU HOME 将这份经验汇聚于单一架构之中——作为 NEXARU GLOBAL 旗下品牌，连接收购、投资、开发与移居，遍及全球。"),
 ("Our network spans the United Arab Emirates and the Middle East, China, India, Pakistan, Europe, the United States and Latin America.",
  "我们的网络遍及阿拉伯联合酋长国与中东、中国、印度、巴基斯坦、欧洲、美国及拉丁美洲。"),
 (">UAE</span>", ">阿联酋</span>"), (">Middle East</span>", ">中东</span>"),
 (">China</span>", ">中国</span>"), (">India</span>", ">印度</span>"),
 (">Pakistan</span>", ">巴基斯坦</span>"), (">Europe</span>", ">欧洲</span>"),
 (">USA</span>", ">美国</span>"), (">LatAm</span>", ">拉美</span>"),
 (">Years of Experience</span>", ">从业年数</span>"),
 (">Continents Covered</span>", ">覆盖大洲</span>"),
 (">Land Under Structuring</span>", ">架构中的土地</span>"),
 (">Founding Pillars</span>", ">创立支柱</span>"),
 (">Health &amp; Wellness</h3>", ">健康与康养</h3>"),
 ("Spaces designed for wellbeing, from concept to daily life.", "为福祉而设计的空间，从概念到日常生活。"),
 (">Ancestral Local Culture</h3>", ">先祖本土文化</h3>"),
 ("Projects rooted in the heritage of the places they inhabit.", "植根于所在之地传承的项目。"),
 (">Eco-Friendly</h3>", ">生态友好</h3>"),
 ("Responsible materials, energy and construction practices.", "负责任的材料、能源与建造实践。"),
 (">Innovation</h3>", ">创新</h3>"),
 ("Technology and design at the service of timeless living.", "让科技与设计服务于历久弥新的生活。"),
 (">Sustainable Development</h3>", ">可持续发展</h3>"),
 ("Long-term value for owners, communities and the land.", "为业主、社群与土地创造长期价值。"),
 ("Begin with <span style=\"color:#C9A876\">XARU</span>", "与 <span style=\"color:#C9A876\">XARU</span> 一同启程"),
 ("Begin the Conversation, <br /> in Complete Confidence.", "开启对话， <br /> 尽享全然保密。"),
 ("<span>Contact Us</span>", "<span>联系我们</span>"),
 ("Global luxury real estate, one structure — from acquisition to relocation, worldwide.",
  "全球奢华房产，单一架构——从收购到移居，遍及全球。"),
 ("> Explore </h3>", ">探索</h3>"),
 (">Investment &amp; Funds</a>", ">投资与基金</a>"),
 ("> Company </h3>", ">公司</h3>"),
 (">Digital Assets</a>", ">数字资产</a>"),
 ("> Newsletter </h3>", ">订阅通讯</h3>"),
 ('placeholder="Enter Email Address"', 'placeholder="请输入电子邮箱"'),
 ("XARU HOME — a NEXARU GLOBAL brand. Licensed in the United Arab Emirates.",
  "XARU HOME — NEXARU GLOBAL 旗下品牌。持有阿拉伯联合酋长国牌照。"),
 ('aria-label="Nav link"', 'aria-label="导航链接"'),
 ('aria-label="Home page link"', 'aria-label="首页链接"'),
 ('aria-label="Contact page link"', 'aria-label="联系页面链接"'),
 ('aria-label="Contact link"', 'aria-label="联系链接"'),
 ('aria-label="Private enquiry link"', 'aria-label="私人咨询链接"'),
 ('aria-label="Explore opportunities link"', 'aria-label="探索机遇链接"'),
 ('aria-label="View land and developments link"', 'aria-label="查看土地与开发链接"'),
 ('aria-label="Enquire link"', 'aria-label="咨询链接"'),
 ('aria-label="View property details link"', 'aria-label="查看房产详情链接"'),
 ('aria-label="View all property link"', 'aria-label="查看全部房产链接"'),
 ('aria-label="View projects link"', 'aria-label="查看项目链接"'),
 ('aria-label="Gallery link"', 'aria-label="图库链接"'),
 ('aria-label="About page link"', 'aria-label="关于页面链接"'),
 ('aria-label="View contact page link"', 'aria-label="联系页面链接"'),
 ('aria-label="Footer menu link"', 'aria-label="页脚菜单链接"'),
]

# ---------------------------------------------------------------- shared chrome extras
# Chrome fragments that appear on inner pages but not on the index. Safe on every
# page (no-op where the fragment is absent). Merged into the master dict below.
SHARED_ES = [
 ('aria-label="Back to home button">Home</a>', 'aria-label="Volver al inicio">Inicio</a>'),
 ('aria-label="Back to home button"', 'aria-label="Volver al inicio"'),
 ('placeholder="Write your name"', 'placeholder="Escriba su nombre"'),
 ('placeholder="Enter email address"', 'placeholder="Introduzca su correo electrónico"'),
 ('placeholder="Phone number"', 'placeholder="Número de teléfono"'),
 ('placeholder="Write message"', 'placeholder="Escriba su mensaje"'),
 ('placeholder="Write Message"', 'placeholder="Escriba su mensaje"'),
 ('placeholder="Write your comment *"', 'placeholder="Escriba su comentario *"'),
 ('placeholder="Your name"', 'placeholder="Su nombre"'),
 ('placeholder="Your email"', 'placeholder="Su correo electrónico"'),
 ('placeholder="Search"', 'placeholder="Buscar"'),
 ('aria-label="Pagination arrow left"', 'aria-label="Flecha de paginación izquierda"'),
 ('aria-label="Pagination arrow right"', 'aria-label="Flecha de paginación derecha"'),
 ('aria-label="Search button"', 'aria-label="Botón de búsqueda"'),
 ('aria-label="Search"', 'aria-label="Buscar"'),
 ('aria-label="Category button"', 'aria-label="Botón de categoría"'),
 ('aria-label="Property list page link"', 'aria-label="Enlace a la página de propiedades"'),
 ('aria-label="About us page link"', 'aria-label="Enlace a la página Nosotros"'),
 ('aria-label="Submit Request"', 'aria-label="Enviar solicitud"'),
 # hero background slides (index) — descriptive keyword alt equivalents
 ('aria-label="Global luxury real estate — aerial coastline, XARU HOME"', 'aria-label="Inmobiliaria de lujo global — costa desde el aire, XARU HOME"'),
 ('aria-label="Isola del Faro, a private island held in a single title"', 'aria-label="Isola del Faro, isla privada reunida en un único título"'),
 ('aria-label="Master development land — ASHIMA, Oaxaca, Mexico"', 'aria-label="Suelo para desarrollo maestro — ASHIMA, Oaxaca, México"'),
]
SHARED_AR = [
 ('aria-label="Back to home button">Home</a>', 'aria-label="العودة إلى الرئيسية">الرئيسية</a>'),
 ('aria-label="Back to home button"', 'aria-label="العودة إلى الرئيسية"'),
 ('placeholder="Write your name"', 'placeholder="اكتب اسمك"'),
 ('placeholder="Enter email address"', 'placeholder="أدخل بريدك الإلكتروني"'),
 ('placeholder="Phone number"', 'placeholder="رقم الهاتف"'),
 ('placeholder="Write message"', 'placeholder="اكتب رسالتك"'),
 ('placeholder="Write Message"', 'placeholder="اكتب رسالتك"'),
 ('placeholder="Write your comment *"', 'placeholder="اكتب تعليقك *"'),
 ('placeholder="Your name"', 'placeholder="اسمك"'),
 ('placeholder="Your email"', 'placeholder="بريدك الإلكتروني"'),
 ('placeholder="Search"', 'placeholder="بحث"'),
 ('aria-label="Pagination arrow left"', 'aria-label="سهم ترقيم الصفحات لليسار"'),
 ('aria-label="Pagination arrow right"', 'aria-label="سهم ترقيم الصفحات لليمين"'),
 ('aria-label="Search button"', 'aria-label="زر البحث"'),
 ('aria-label="Search"', 'aria-label="بحث"'),
 ('aria-label="Category button"', 'aria-label="زر الفئة"'),
 ('aria-label="Property list page link"', 'aria-label="رابط صفحة العقارات"'),
 ('aria-label="About us page link"', 'aria-label="رابط صفحة من نحن"'),
 ('aria-label="Submit Request"', 'aria-label="إرسال الطلب"'),
 # hero background slides (index) — descriptive keyword alt equivalents
 ('aria-label="Global luxury real estate — aerial coastline, XARU HOME"', 'aria-label="عقارات فاخرة عالمية — ساحل من الأعلى، XARU HOME"'),
 ('aria-label="Isola del Faro, a private island held in a single title"', 'aria-label="Isola del Faro، جزيرة خاصة بسند ملكية واحد"'),
 ('aria-label="Master development land — ASHIMA, Oaxaca, Mexico"', 'aria-label="أرض لتطوير رئيسي — ASHIMA، واخاكا، المكسيك"'),
]

SHARED_ZH = [
 ('aria-label="Back to home button">Home</a>', 'aria-label="返回首页">首页</a>'),
 ('aria-label="Back to home button"', 'aria-label="返回首页"'),
 ('placeholder="Write your name"', 'placeholder="请填写您的姓名"'),
 ('placeholder="Enter email address"', 'placeholder="请输入电子邮箱"'),
 ('placeholder="Phone number"', 'placeholder="电话号码"'),
 ('placeholder="Write message"', 'placeholder="请填写留言"'),
 ('placeholder="Write Message"', 'placeholder="请填写留言"'),
 ('placeholder="Write your comment *"', 'placeholder="请填写您的评论 *"'),
 ('placeholder="Your name"', 'placeholder="您的姓名"'),
 ('placeholder="Your email"', 'placeholder="您的电子邮箱"'),
 ('placeholder="Search"', 'placeholder="搜索"'),
 ('aria-label="Pagination arrow left"', 'aria-label="分页左箭头"'),
 ('aria-label="Pagination arrow right"', 'aria-label="分页右箭头"'),
 ('aria-label="Search button"', 'aria-label="搜索按钮"'),
 ('aria-label="Search"', 'aria-label="搜索"'),
 ('aria-label="Category button"', 'aria-label="类别按钮"'),
 ('aria-label="Property list page link"', 'aria-label="房产列表页面链接"'),
 ('aria-label="About us page link"', 'aria-label="关于我们页面链接"'),
 ('aria-label="Submit Request"', 'aria-label="提交请求"'),
 # hero background slides (index) — descriptive keyword alt equivalents
 ('aria-label="Global luxury real estate — aerial coastline, XARU HOME"', 'aria-label="全球奢华房产——海岸鸟瞰，XARU HOME"'),
 ('aria-label="Isola del Faro, a private island held in a single title"', 'aria-label="Isola del Faro，单一产权私人岛屿"'),
 ('aria-label="Master development land — ASHIMA, Oaxaca, Mexico"', 'aria-label="大型开发用地——ASHIMA，墨西哥瓦哈卡"'),
]

DICT = {"es": ES + SHARED_ES, "ar": AR + SHARED_AR, "zh": ZH + SHARED_ZH}

# ---------------------------------------------------------------- per-page dictionaries
from page_dicts import PAGES  # noqa: E402  (page-specific strings & meta)
import seo_meta               # noqa: E402  (Phase 6 SEO/AEO meta + JSON-LD)
import arch_data as ARCH      # noqa: E402  (Phase 1 mega-menu + shell pages)

# non-index pages share these EN head strings
EN_GEN_TITLE   = "XARU HOME — Global Luxury Real Estate, One Structure"
EN_GEN_DESC    = "XARU HOME — Global Luxury Real Estate, One Structure"
EN_GEN_OGTITLE = "XARU HOME — Global Real Estate at Its Highest Scale"

TRANSLATED = {
 "index.html", "property-listing-buy.html", "property-listing-rent.html",
 "property-listing-search.html", "single-property-v1.html", "property-details.html",
 "agents-list.html", "about-us.html", "blog.html", "blog-details.html",
 "contact.html", "faq.html",
}

# Phase 6 — legacy template links that never had a page behind them.
_DEAD_LINKS = {
 "service-details.html": "property-details.html",   # property card CTA
 "gallery.html": "property-listing-buy.html",       # "explore the gallery" CTA
}

# ---------------------------------------------------------------- catalogo demostrativo
# Biblia Visual V3 §8/§17: las paginas de listado dejan de mostrar las 10 fichas
# fijas de la plantilla y pasan a renderizar el catalogo demostrativo completo
# (144 activos) desde data/properties/*.json, con <picture> AVIF/WebP/JPEG,
# srcset en 5 anchos, carga diferida y filtros por tipologia.
# Titulo de primer nivel para las paginas de listado. Auditoria 1-ago-2026:
# property-listing-rent.html usaba un <h2> como titulo de pagina y
# property-listing-search.html no tenia ningun encabezado de pagina. Ambas
# quedaban sin H1, que es un fallo de SEO real, no cosmetico.
CATALOG_H1 = {
 "property-listing-search.html": {
   "en": "Search the XARU HOME portfolio",
   "es": "Buscar en el portafolio de XARU HOME",
   "ar": "ابحث في محفظة XARU HOME",
   "zh": "检索 XARU HOME 资产组合"},
}


# ---------------------------------------------------------------- imagenes de seccion
# Las fotos de assets/img/xaru/gen2 hacen doble papel: fondo de cabecera a
# pantalla completa y foto de tarjeta a ~440 px. Servir el master de 1920 en los
# dos sitios era lo que ponia la portada en 11,7 MB. GEN2_BG devuelve las dos
# declaraciones CSS -- JPEG plano como suelo y luego image-set con WebP -- al
# ancho que de verdad ocupa la imagen. tools_derivatives_gen2.py genera las piezas.
def gen2_bg(name, w=1280):
    base = name[:-4] if name.endswith(".jpg") else name
    r = "/assets/img/xaru/gen2/r/%s-%d" % (base, w)
    return ("background-image:url('%s.jpg');"
            "background-image:image-set(url('%s.webp') type('image/webp'),"
            "url('%s.jpg') type('image/jpeg'))" % (r, r, r))

def gen2_src(name, w=1280, ext="jpg"):
    base = name[:-4] if name.endswith(".jpg") else name
    return "/assets/img/xaru/gen2/r/%s-%d.%s" % (base, w, ext)

# El listado ya no lee los tres paquetes estáticos: consume la API de la
# plataforma (data/api/v1/search-index.json), con 900+ activos en 130 países.
# El valor "api" activa ese camino en xaru-catalog.js.
CATALOG_PAGE = {
    "property-listing-buy.html":    "api",
    "property-listing-rent.html":   "api",
    "property-listing-search.html": "api",
}
CATALOG_SCOPE = {
    "property-listing-buy.html":  ' data-offering="sale"',
    "property-listing-rent.html": ' data-offering="rent"',
}

def _match_div(h, start):
    """Devuelve el indice final del <div> abierto en `start` (incluido su cierre)."""
    depth = 0
    for m in re.finditer(r'<div\b|</div>', h[start:]):
        if m.group(0) == '</div>':
            depth -= 1
            if depth == 0:
                return start + m.end()
        else:
            depth += 1
    return -1

# Paginas sin ningun H1. La plantilla usaba <h3> para el titulo del formulario
# (login, registro, recuperar clave) y en blog-details el unico titulo estaba en
# la barra lateral. Una pagina sin H1 no le dice a nadie —ni a un buscador ni a
# un lector de pantalla— de que trata. Se promociona el encabezado principal
# conservando sus clases: no cambia un pixel.
# La version arabe de property-listing-buy perdio su <h1> en la cadena de
# reemplazos de traduccion: quedaba con el subtitulo como unico encabezado.
# Se repone con el mismo texto que llevan las otras tres.
PLIST_H1 = {
    "property-listing-buy.html": {
        "en": "Private Islands &amp; Luxury Property for Sale",
        "es": "Islas privadas y propiedades de lujo en venta",
        "ar": "\u062c\u0632\u0631 \u062e\u0627\u0635\u0629 \u0648\u0639\u0642\u0627\u0631\u0627\u062a \u0641\u0627\u062e\u0631\u0629 \u0644\u0644\u0628\u064a\u0639",
        "zh": "\u79c1\u4eba\u5c9b\u5c7f\u4e0e\u5962\u534e\u623f\u4ea7\u5728\u552e",
    },
}

def restore_listing_h1(h, fname, lang):
    """Repone el H1 de una pagina de listado si la traduccion se lo comio."""
    if fname not in PLIST_H1 or re.search(r'<h1[\s>]', h):
        return h
    txt = PLIST_H1[fname].get(lang)
    if not txt:
        return h
    m = re.search(r'<h2 class="cs_section_subtitle', h)
    if not m:
        return h
    tag = ('<h1 class="cs_section_title cs_fs_49 cs_mb_10" data-aos="fade-up">%s</h1>\n          '
           % txt)
    return h[:m.start()] + tag + h[m.start():]

H1_PROMOTE = {
    "login.html":           r'<h3 class="cs_contact_form_heading[^"]*"[^>]*>',
    "register.html":        r'<h3 class="cs_contact_form_heading[^"]*"[^>]*>',
    "forgot-password.html": r'<h3 class="cs_contact_form_heading[^"]*"[^>]*>',
    # En blog-details el titulo del articulo es el unico <h2> SIN clase; los
    # demas son de barra lateral ("Categories", "Latest posts") o de seccion.
    "blog-details.html":    r'<h2>',
}

def ensure_h1(h, fname):
    """Si la pagina no tiene H1, promociona su encabezado principal."""
    if re.search(r'<h1[\s>]', h):
        return h
    pat = H1_PROMOTE.get(fname)
    if not pat:
        return h
    m = re.search(pat, h)
    if not m:
        return h
    tag = m.group(0)
    lvl = tag[2]                       # 2 o 3
    close = "</h%s>" % lvl
    j = h.find(close, m.end())
    if j < 0:
        return h
    nuevo = "<h1" + tag[3:]
    return h[:m.start()] + nuevo + h[m.end():j] + "</h1>" + h[j+len(close):]

def enforce_single_h1(h):
    """Deja un unico <h1> por pagina degradando los siguientes a <h2>.
    Conserva los atributos, de modo que el aspecto es identico; lo que cambia
    es la jerarquia que leen los buscadores y los lectores de pantalla."""
    out = []
    pos = 0
    n = 0
    for m in re.finditer(r'<h1([^>]*)>(.*?)</h1>', h, re.S):
        n += 1
        if n == 1:
            continue
        out.append((m.start(), m.end(), m.group(1), m.group(2)))
    for st, en, attrs, inner in reversed(out):
        h = h[:st] + '<h2%s>%s</h2>' % (attrs, inner) + h[en:]
    return h

LISTING_HEAD = {
 "property-listing-search.html": (
   ARCH.T("The portfolio", "El portafolio", "المحفظة", "作品集"),
   ARCH.T("Search the XARU HOME portfolio", "Busque en el portafolio de XARU HOME",
     "ابحث في محفظة XARU HOME", "检索 XARU HOME 资产组合"),
   "07_villa_dubai.jpg"),
 "property-listing-buy.html": (
   ARCH.T("Private real estate", "Inmobiliario privado", "العقارات الخاصة", "私人房产"),
   ARCH.T("Private Islands & Luxury Property for Sale", "Islas privadas y propiedad de lujo en venta",
     "جزر خاصة وعقارات فاخرة للبيع", "私人岛屿与豪华房产出售"),
   "09_villa_como.jpg"),
 "property-listing-rent.html": (
   ARCH.T("Commercial & hospitality", "Comercial y hosteleria", "التجاري والضيافة", "商业与酒店"),
   ARCH.T("Residences for Lease", "Residencias en alquiler", "مساكن للإيجار", "租赁住宅"),
   "05_hotel_project.jpg"),
}

LISTING_COUNT = ARCH.T("assets in the portfolio", "activos en el portafolio",
                  "أصل ضمن المحفظة", "项资产在册")

# ---------------------------------------------------------------- imagenes de plantilla
# La plantilla venia con su propio banco de fotos de relleno: casas de barrio
# residencial estadounidense, una cabana roja noruega, un plano de planta
# renderizado, un retrato de banco de imagenes. Nada de eso es XARU y estaba
# saliendo en contacto, faq, error y en la ficha estatica. Se sustituye por
# fotografia real de la casa, y los bloques que no tienen equivalente —
# planos de planta, galeria de ejemplo, retrato del autor — se retiran.
TEMPLATE_IMG = {
    "page-heading.jpg":    ("31_page_header.jpg",   1920),
    "contact-bg.jpg":      ("32_contact_panel.jpg", 1920),
    "city-dubai.jpg":      ("24_capital_district.jpg", 1280),
    "hero-bg-7.jpg":       ("07_villa_dubai.jpg",   1920),
    "property-banner.jpg": ("09_villa_como.jpg",    1280),
    "property-img-1.jpg":  ("10_casa_tulum.jpg",    1280),
    "property-img-2.jpg":  ("11_villa_marbella.jpg", 1280),
    "property-img-3.jpg":  ("05_hotel_project.jpg", 1280),
    "property-img-4.jpg":  ("02_island_rd.jpg",     1280),
    "property-img-5.jpg":  ("19_resort_complex.jpg", 1280),
    "property-img-6.jpg":  ("27_hotel_halted.jpg",  1280),
    "post-img-1.jpg":      ("03_land_mega.jpg",     1280),
    "post-img-2.jpg":      ("06_masterplan_ashima.jpg", 1280),
    "post-img-3.jpg":      ("25_trade_port.jpg",    1280),
    "post-img-4.jpg":      ("22_land_parcels.jpg",  1280),
    "post-img-5.jpg":      ("17_ocean_cliff.jpg",   1280),
    "post-img-6.jpg":      ("16_atlantic_aerial.jpg", 1280),
    "team-img-5.jpg":      ("26_corporate_services.jpg", 768),
}

# ---------------------------------------------------------------- enlaces muertos
# Biblia de Real Estate §0.5 y §1.1: ningun CTA visible puede estar fingido, y
# los iconos sociales con href="#" son exactamente eso — un objetivo de foco
# que no lleva a ninguna parte, repetido 519 veces en 169 paginas. Mientras no
# haya URLs reales se retiran de la interfaz publica, que es la salida que la
# propia Biblia autoriza. En cuanto existan, se rellenan aqui y vuelven solas.
SOCIAL_URLS = {
    # "linkedin":  "https://www.linkedin.com/company/...",
    # "instagram": "https://www.instagram.com/...",
    # "youtube":   "https://www.youtube.com/@...",
}
_SOCIAL_ICON = {"linkedin": "linkedin-in", "instagram": "instagram", "youtube": "youtube",
                "twitter": "twitter", "facebook": "facebook-f"}

def strip_index_html(h, lang="en"):
    """Biblia §20.2 y §26.3: ninguna URL publica lleva `index.html`.

    `_redirects` ya devuelve un 301 para quien llega con la extension, pero el
    propio sitio se enlazaba 278 veces a `index.html#ancla`. Cada uno de esos
    clics era un salto de mas y una URL duplicada para el rastreador.
    """
    h = re.sub(r'href="index\.html(#[^"]*)?"', lambda m: 'href="%s"' % (m.group(1) or "/"), h)
    h = re.sub(r'href="(\.\./)*index\.html(#[^"]*)?"',
               lambda m: 'href="%s"' % ((m.group(1) or "") + (m.group(2) or "")) if m.group(1)
               else 'href="%s"' % (m.group(2) or "/"), h)
    h = re.sub(r'href="([^"]*/)index\.html(#[^"]*)?"',
               lambda m: 'href="%s%s"' % (m.group(1), m.group(2) or ""), h)
    return h

def migrate_catalog_mount(h, fname):
    """El punto de montaje del catálogo quedó congelado por la guardia de
    idempotencia de inject_catalog. Aquí se reescribe al inventario de la
    plataforma sin volver a inyectar nada."""
    feed = CATALOG_PAGE.get(fname)
    if not feed:
        return h
    scope = CATALOG_SCOPE.get(fname, "")
    h = re.sub(r'<div class="row cs_gap_y_45" data-catalog="[^"]*"[^>]*>',
               '<div class="row cs_gap_y_45" data-catalog="%s"%s>' % (feed, scope), h)
    return h

def purge_dead_links(h):
    """Resuelve o retira todo href="#" del HTML publico."""
    def repl(m):
        tag = m.group(0)
        lbl = re.search(r'aria-label="([^"]*)"', tag)
        icon = re.search(r'fa-brands fa-([a-z-]+)', tag)
        key = (lbl.group(1).lower() if lbl else
               (icon.group(1) if icon else ""))
        for k, url in SOCIAL_URLS.items():
            if key.startswith(k) or _SOCIAL_ICON.get(k) == key:
                return tag.replace('href="#"', 'href="%s" target="_blank" rel="noopener"' % url)
        return ""          # sin URL real, fuera de la interfaz
    # <a href="#" …>…</a> completo, incluido su contenido
    h = re.sub(r'<a\b[^>]*href="#"[^>]*>.*?</a>', repl, h, flags=re.S)
    return h

def purge_template_images(h, lang="en"):
    pre = "" if lang == "en" else "../"
    for old, (new, w) in TEMPLATE_IMG.items():
        base = new[:-4]
        rep = "%sassets/img/xaru/gen2/r/%s-%d.jpg" % (pre, base, w)
        h = h.replace("%sassets/img/%s" % (pre, old), rep)
        if lang == "en":
            h = h.replace("/assets/img/%s" % old, "/assets/img/xaru/gen2/r/%s-%d.jpg" % (base, w))
    # Planos de planta y retrato de autor: no hay equivalente real, se van.
    for sel in ('<img[^>]*floor-plan[^>]*>', '<img[^>]*post-author[^>]*>',
                '<img[^>]*illustartion\.svg[^>]*>'):
        h = re.sub(sel, '', h)
    return h

def fix_listing_page(h, fname, lang="en"):
    """Repara las tres paginas de listado heredadas de la plantilla.

    Traian tres defectos visibles: (a) una cabecera falsa con un buscador de
    juguete -- Comprar/Alquilar, Apartamento, un desplegable de ciudades -- que
    ademas se solapaba sobre la foto a 1440 px; (b) el rotulo fijo "40 Real
    Estate Properties for Sell in London", que no era ni el numero ni la ciudad
    ni el idioma de esta casa; y (c) decenas de puntos de montaje del catalogo
    duplicados por regeneraciones antiguas, de los que el JS solo rellena el
    primero y el resto quedaban como un hueco en blanco.

    Es idempotente: cada arreglo comprueba antes si ya esta hecho.
    """
    if fname not in LISTING_HEAD:
        return h
    eyebrow, title, img = LISTING_HEAD[fname]

    # (c) un solo punto de montaje de filtros y de nota
    fmount = '<div class="xr_cat_filters" data-catalog-filters></div>'
    nmount = '<p class="xr_cat_note cs_secondary_color" data-catalog-note></p>'
    if h.count(fmount) > 1:
        first = h.find(fmount)
        head, tail = h[:first + len(fmount)], h[first + len(fmount):]
        tail = tail.replace(fmount, "")
        h = head + tail
    if h.count(nmount) > 1:
        first = h.find(nmount)
        head, tail = h[:first + len(nmount)], h[first + len(nmount):]
        tail = tail.replace(nmount, "")
        h = head + tail

    # (a) cabecera propia en lugar del buscador de juguete
    if 'xr_listing_header' not in h:
        m = re.search(r'<div class="cs_hero cs_style_7">', h)
        if m:
            end = _match_div(h, m.start())
            if end > 0:
                crumbs = ('<li class="breadcrumb-item"><a href="%s">%s</a></li>'
                          '<li class="breadcrumb-item active">%s</li>'
                          % (HOME[lang], _t(ARCH.CRUMB_HOME, lang), _t(title, lang)))
                band = (
                  '<section class="cs_page_header cs_style_1 cs_center cs_bg_filed xr_duotone_overlay '
                  'position-relative xr_listing_header" data-src="%s" style="%s">\n'
                  '      <div class="container">\n'
                  '        <div class="cs_page_header_content text-center">\n'
                  '          <span class="cs_page_header_subtitle cs_fs_14" style="letter-spacing:3px;'
                  'text-transform:uppercase;color:rgba(245,241,232,.9)">%s</span>\n'
                  '          <h1 class="cs_page_header_title cs_fs_49 mb-0" data-aos="fade-up">%s</h1>\n'
                  '          <ol class="breadcrumb cs_center mb-0">%s</ol>\n'
                  '        </div>\n'
                  '      </div>\n'
                  '    </section>'
                  % (gen2_src(img, 1920), gen2_bg(img, 1920),
                     _t(eyebrow, lang), _t(title, lang), crumbs))
                h = h[:m.start()] + band + h[end:]

    # (b) contador vivo en lugar del rotulo fijo de la plantilla
    m = re.search(r'<p class="cs_primary_color cs_primary_font mb-0">.*?</p>', h, re.S)
    if m and 'data-catalog-count' not in m.group(0):
        h = (h[:m.start()]
             + '<p class="cs_primary_color cs_primary_font mb-0">'
               '<span class="cs_fs_20 cs_semibold me-1" data-catalog-count>156</span>%s</p>'
               % _t(LISTING_COUNT, lang)
             + h[m.end():])

    # El titulo de la pagina vive ahora en la banda de cabecera. Los que
    # inject_catalog dejo sueltos dentro del cuerpo son repeticiones del mismo
    # texto, una debajo de otra: se retiran.
    # Se buscan en los cuatro idiomas: las paginas traducidas heredaron el
    # titulo en ingles de una generacion antigua y ahi se quedo congelado.
    for _L in ("en", "es", "ar", "zh"):
        h = re.sub(r'<h[12] class="cs_section_title cs_fs_49 cs_mb_10"[^>]*>%s</h[12]>\s*'
                   % re.escape(_t(title, _L)), '', h)

    # Los bloques "Property Type" y "Offer Type" de la plantilla ofrecian
    # Apartamento / Casa / Oficina / Comprar / Alquilar: ni una sola de esas
    # casillas tocaba el listado, y la tipologia ya se elige con las pastillas
    # de arriba. Un control que no hace nada es peor que no tenerlo.
    for _dead in ("Property Type", "Offer Type"):
        _m = re.search(r'<div class="cs_sidebar_widget">\s*<h3[^>]*>\s*<span>\s*%s\s*</span>'
                       % re.escape(_dead), h)
        if _m:
            _end = _match_div(h, _m.start())
            if _end > 0:
                h = h[:_m.start()] + h[_end:]

    # el desplegable "Sort by" de la plantilla no ordenaba nada
    h = re.sub(r'<div class="cs_property_sort_wrapper">.*?</div>\s*</div>\s*</div>',
               '</div>', h, count=1, flags=re.S)
    return h

def inject_catalog(h, fname, lang="en"):
    """Sustituye la rejilla estatica por el punto de montaje del catalogo."""
    feed = CATALOG_PAGE.get(fname)
    if not feed:
        return h
    # Idempotencia: build_en reescribe los ficheros en su sitio, asi que
    # regenerar dos veces volvia a inyectar el H1 y la pagina acababa con
    # dos. Si el montaje ya esta puesto, no se toca nada.
    if 'data-catalog=' in h:
        return h
    m = re.search(r'<div class="row cs_gap_y_45[^"]*"[^>]*>', h)
    if not m:
        return h
    b = m.start()
    end = _match_div(h, b)
    if end < 0:
        return h

    # H1 de pagina donde falta (search) y promocion de h2 a h1 (rent).
    h1 = ""
    t = CATALOG_H1.get(fname)
    if t:
        h1 = ('<h1 class="cs_section_title cs_fs_49 cs_mb_10" data-aos="fade-up">%s</h1>\n'
              '              ' % _t(t, lang))
    mount = (
        h1 +
        '<div class="xr_cat_filters" data-catalog-filters></div>\n'
        '              <p class="xr_cat_note cs_secondary_color" data-catalog-note></p>\n'
        '              <div class="row cs_gap_y_45" data-catalog="%s"%s></div>'
        % (feed, CATALOG_SCOPE.get(fname, ""))
    )
    h = h[:b] + mount + h[end:]

    # La paginacion de la plantilla ya no aplica: el filtrado es por tipologia.
    h = re.sub(r'<ul class="cs_pagination_box cs_mp_0">.*?</ul>', '', h, count=1, flags=re.S)

    # rent: el titulo de pagina venia como h2. Se promociona a h1 conservando
    # las clases, asi que el aspecto no cambia en absoluto.
    if fname == "property-listing-rent.html" and "<h1" not in h:
        h = h.replace('<h2 class="cs_section_title cs_fs_49 mb-0"',
                      '<h1 class="cs_section_title cs_fs_49 mb-0"', 1)
        i = h.find('<h1 class="cs_section_title cs_fs_49 mb-0"')
        if i >= 0:
            j = h.find('</h2>', i)
            if j >= 0:
                h = h[:j] + '</h1>' + h[j+5:]

    if 'xaru-catalog.js' not in h:
        h = h.replace('</body>',
            '  <script src="assets/js/xaru-catalog.js"></script>\n</body>', 1)
    return h

def fix_dead_links(h):
    """Repoint hrefs to template pages that do not exist in this build."""
    for dead, live in _DEAD_LINKS.items():
        h = re.sub(r'href="((?:\.\./)*)%s(["#?])' % re.escape(dead),
                   lambda m, l=live: 'href="%s%s%s' % (m.group(1), l, m.group(2)), h)
    return h

def fixlinks(h):
    def repl(m):
        href = m.group(1)
        if href.startswith(("http://", "https://", "#", "mailto:", "tel:", "/", "../")):
            return m.group(0)
        if ".html" not in href:
            return m.group(0)
        base = href.split("#")[0].split("?")[0]
        if base.startswith("./"):
            base = base[2:]
        if base in TRANSLATED:
            return m.group(0)          # same-language folder
        return 'href="../%s"' % href    # untranslated -> English root
    return re.sub(r'href="([^"]+)"', repl, h)

def loc(fname):
    """URL path for a page: home pages are CLEAN (''), inner pages keep .html."""
    return "" if fname == "index.html" else fname

def alternates(fname):
    p = loc(fname)
    return ("\n".join([
      '<link rel="alternate" type="text/llms.txt" href="/llms.txt" />',
      '    <link rel="canonical" href="https://xaruhome.com/%s/%s" />' % ("{L}", p),
      '    <link rel="alternate" hreflang="en" href="https://xaruhome.com/%s" />' % p,
      '    <link rel="alternate" hreflang="es" href="https://xaruhome.com/es/%s" />' % p,
      '    <link rel="alternate" hreflang="ar" href="https://xaruhome.com/ar/%s" />' % p,
      '    <link rel="alternate" hreflang="zh-CN" href="https://xaruhome.com/zh/%s" />' % p,
      '    <link rel="alternate" hreflang="x-default" href="https://xaruhome.com/%s" />' % p,
    ]))

def alternates_en(fname):
    """Canonical (self) + hreflang block for the English root pages."""
    p = loc(fname)
    return ("\n".join([
      '<link rel="alternate" type="text/llms.txt" href="/llms.txt" />',
      '    <link rel="canonical" href="https://xaruhome.com/%s" />' % p,
      '    <link rel="alternate" hreflang="en" href="https://xaruhome.com/%s" />' % p,
      '    <link rel="alternate" hreflang="es" href="https://xaruhome.com/es/%s" />' % p,
      '    <link rel="alternate" hreflang="ar" href="https://xaruhome.com/ar/%s" />' % p,
      '    <link rel="alternate" hreflang="zh-CN" href="https://xaruhome.com/zh/%s" />' % p,
      '    <link rel="alternate" hreflang="x-default" href="https://xaruhome.com/%s" />' % p,
    ]))

# ---------------------------------------------------------------- home links + active nav
def rewrite_home_links(h, lang):
    """Point every internal 'home' link (header logo, visible breadcrumb 'back to
    home') at the CLEAN, root-relative home of `lang` — '/', '/es/', '/ar/',
    '/zh/' — instead of an index.html filename. Section anchors and inner-page
    links are untouched."""
    home = HOME[lang]
    # Header logo <a ... class="cs_site_brand"> — href is on its own line.
    h = re.sub(r'href="index\.html"(\s+aria-label="[^"]*"\s+class="cs_site_brand")',
               lambda m: 'href="%s"%s' % (home, m.group(1)), h)
    # Visible breadcrumb "back to home" link on inner pages.
    h = re.sub(r'(<li class="breadcrumb-item"><a href=")index\.html(")',
               lambda m: m.group(1) + home + m.group(2), h)
    return h

def mark_active_nav(h, lang, fname):
    """Add aria-current="page" (accessible active state) to the menu item for the
    current page. On inner pages that item is the matching nav link; on the home
    page the active state rests on the logo/home brand. Additive only."""
    if fname == "index.html":
        return h.replace('class="cs_site_brand"',
                         'class="cs_site_brand" aria-current="page"', 1)
    def add_active(m):
        block = m.group(0)
        block = re.sub(r'(<li><a href="%s")' % re.escape(fname),
                       r'\1 aria-current="page" class="cs_current_page"', block, count=1)
        return block
    return re.sub(r'<ul class="cs_nav_list.*?</ul>', add_active, h, count=1, flags=re.S)

def strip_alts(h):
    """Remove any previously injected canonical/hreflang alternates (idempotency)."""
    h = re.sub(r'[ \t]*<link rel="canonical"[^>]*>\s*\n?', '', h)
    h = re.sub(r'[ \t]*<link rel="alternate" hreflang="[^"]*"[^>]*>\s*\n?', '', h)
    h = re.sub(r'[ \t]*<link rel="alternate" type="text/llms\.txt"[^>]*>\s*\n?', '', h)
    return h

# ---------------------------------------------------------------- JSON-LD (index only)
LD_URL      = {"en": "https://xaruhome.com/", "es": "https://xaruhome.com/es/",
               "ar": "https://xaruhome.com/ar/", "zh": "https://xaruhome.com/zh/"}
LD_INLANG   = {"en": "en", "es": "es", "ar": "ar", "zh": "zh-CN"}
LD_DESC = {
 "en": "XARU HOME — global luxury real estate at its highest scale. A NEXARU GLOBAL brand connecting acquisition, investment, development and relocation, worldwide.",
 "es": "XARU HOME — bienes raíces de lujo globales a la mayor escala. Una marca de NEXARU GLOBAL que conecta adquisición, inversión, desarrollo y relocalización, en todo el mundo.",
 "ar": "XARU HOME — عقارات فاخرة عالمية على أرفع مستوى. علامة من NEXARU GLOBAL تربط الاقتناء والاستثمار والتطوير والانتقال حول العالم.",
 "zh": "XARU HOME — 臻于至高格局的全球奢华房产。NEXARU GLOBAL 旗下品牌，连接收购、投资、开发与移居，遍及全球。",
}
LD_AREA = ["United Arab Emirates", "China", "India", "Pakistan", "Europe",
           "United States", "Mexico", "Colombia", "Ecuador", "Peru", "Panama",
           "Dominican Republic", "El Salvador", "Nicaragua"]

def jsonld_block(lang):
    """Organization/RealEstateAgent + WebSite JSON-LD for the index of `lang`."""
    org = {
        "@context": "https://schema.org",
        "@type": "RealEstateAgent",
        "name": "XARU HOME",
        "brand": {"@type": "Brand", "name": "XARU HOME"},
        "parentOrganization": {"@type": "Organization", "name": "NEXARU GLOBAL"},
        "description": LD_DESC[lang],
        "url": LD_URL[lang],
        "logo": "https://xaruhome.com/assets/img/xaru/monogram_gold_160.png",
        "image": "https://xaruhome.com/assets/img/xaru/og-cover.jpg",
        "areaServed": [{"@type": "Country", "name": c} for c in LD_AREA],
        "knowsLanguage": ["en", "es", "ar", "zh"],
    }
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "XARU HOME",
        "url": LD_URL[lang],
        "inLanguage": LD_INLANG[lang],
        "publisher": {"@type": "Organization", "name": "NEXARU GLOBAL"},
    }
    j = lambda d: json.dumps(d, ensure_ascii=False, indent=2)
    return ("    <!-- XARU JSON-LD -->\n"
            '    <script type="application/ld+json">\n' + j(org) + "\n    </script>\n"
            '    <script type="application/ld+json">\n' + j(website) + "\n    </script>\n"
            "    <!-- /XARU JSON-LD -->\n")

def strip_jsonld(h):
    return re.sub(r'[ \t]*<!-- XARU JSON-LD -->.*?<!-- /XARU JSON-LD -->\s*\n?', '', h, flags=re.S)

# ================================================================ Phase 1 architecture
# Mega-menu (4 doors + Company + Insights) + secondary CTA, injected into the
# shared chrome of EVERY generated page, per language. Links are root-absolute
# (/, /es/, /ar/, /zh/) so they survive asset-path rewrites and any folder depth.
def _t(d, lang):
    return d[lang]

def megamenu(lang):
    home = HOME[lang]
    lis = []
    for door in ARCH.NAV:
        cols_html = []
        for col in door["cols"]:
            wide = " xr_mega_col_wide" if col.get("wide") else ""
            hrefs = col.get("hrefs")  # Phase 5: per-item anchors (Company / Insights)
            subs = "\n                          ".join(
                '<a class="xr_mega_sub" href="%s%s">%s</a>' % (
                    home, (hrefs[i] if hrefs else col["slug"] + "/"), _t(it, lang))
                for i, it in enumerate(col["items"]))
            cols_html.append(
                '<div class="xr_mega_col%s">\n'
                '                        <a class="xr_mega_col_title" href="%s%s/">%s</a>\n'
                '                          %s\n'
                '                      </div>' % (wide, home, col["slug"], _t(col["title"], lang), subs))
        cols_joined = "\n                      ".join(cols_html)
        lis.append(
            '<li class="xr_mega_item">\n'
            '                    <a class="xr_mega_link" href="%s%s/" aria-label="%s">%s</a>\n'
            '                    <button type="button" class="xr_mega_toggle" aria-label="%s" aria-expanded="false"><span></span></button>\n'
            '                    <div class="xr_mega_panel">\n'
            '                      <div class="xr_mega_inner">\n'
            '                        <div class="xr_mega_intro">\n'
            '                          <p class="xr_mega_lead">%s</p>\n'
            '                          <p class="xr_mega_lead_sub">%s</p>\n'
            '                        </div>\n'
            '                        <div class="xr_mega_cols">\n'
            '                      %s\n'
            '                        </div>\n'
            '                      </div>\n'
            '                    </div>\n'
            '                  </li>' % (
                home, door["slug"], _t(door["label"], lang), _t(door["label"], lang),
                _t(ARCH.EXPAND, lang), _t(door["intro"], lang), _t(door["intro_sub"], lang),
                cols_joined))
    return '<ul class="cs_nav_list cs_mp_0">\n                    ' + \
           "\n                    ".join(lis) + '\n                  </ul>'

def right_buttons(lang):
    home = HOME[lang]
    return ('<!-- xr-cta -->\n'
            '                <li class="xr_header_cta">\n'
            '                  <a href="%sopportunities/submit/" aria-label="Submit an opportunity"\n'
            '                    class="cs_btn cs_style_1 cs_fs_16 cs_radius_20 text-capitalize xr_btn_ghost"\n'
            '                    ><span>%s</span></a>\n'
            '                </li>\n'
            '                <li>\n'
            '                  <a href="%sprivate-enquiry/" aria-label="Private enquiry"\n'
            '                    class="cs_btn cs_style_1 cs_primary_bg cs_fs_16 cs_white_color cs_radius_20 text-capitalize"\n'
            '                    ><span>%s</span></a>\n'
            '                </li>\n'
            '                <!-- /xr-cta -->' % (
                home, _t(ARCH.BTN_SUBMIT, lang), home, _t(ARCH.BTN_ENQUIRY, lang)))

_CTA_PAT = re.compile(
    r'<!-- xr-cta -->.*?<!-- /xr-cta -->'
    r'|<li>\s*<a[^>]*href="[^"]*contact\.html"[^>]*class="cs_btn[^"]*"[^>]*>.*?</a\s*>\s*</li>',
    re.S)

def inject_mega(h, lang):
    """Replace the legacy nav list with the mega-menu and the single Private
    Enquiry button with the two-button CTA. Idempotent (re-matches the injected
    markers on repeat runs)."""
    h = re.sub(r'<ul class="cs_nav_list cs_mp_0">.*?</ul>',
               lambda m: megamenu(lang), h, count=1, flags=re.S)
    h = _CTA_PAT.sub(lambda m: right_buttons(lang), h, count=1)
    return h

def inject_mega_js(h):
    if "xaru-mega.js" in h:
        return h
    return h.replace('<script src="assets/js/main.js"></script>',
                     '<script src="assets/js/main.js"></script>\n'
                     '    <script src="assets/js/xaru-mega.js"></script>', 1)

# ---------------------------------------------------------------- build (index — original path)
def build_index(lang):
    h = BASE
    # head meta (title/desc/og/twitter/og:url) via the Phase-6 SEO source of truth
    h = seo_meta.set_head(h, lang, "index.html")
    # rebuild canonical + hreflang (en/es/ar/zh + x-default) + JSON-LD freshly
    h = strip_alts(h)
    h = strip_jsonld(h)
    alt = alternates("index.html").replace("{L}", lang)
    h = h.replace("</head>", "    " + alt + "\n" + seo_meta.jsonld_for(lang, "index.html") + "  </head>", 1)
    h = inject_head_extras(h)
    h = apply(h, DICT[lang])
    h = apply(h, HERO_PAIRS.get(lang, []))
    return finish(h, lang, "index.html")

# ---------------------------------------------------------------- build (inner pages)
def build_page(lang, name):
    fname = name + ".html"
    src = "/home/claude/work/site/xaru/%s" % fname
    with open(src, encoding="utf-8") as f:
        h = f.read()
    page = PAGES[name]
    # head meta (title/desc/og/twitter/og:url) via the Phase-6 SEO source of truth
    h = seo_meta.set_head(h, lang, fname)
    # inject canonical + hreflang alternates + JSON-LD (strip any prior block first)
    h = strip_alts(h)
    h = strip_jsonld(h)
    alt = alternates(fname).replace("{L}", lang)
    h = h.replace("</head>", "    " + alt + "\n" + seo_meta.jsonld_for(lang, fname) + "  </head>", 1)
    h = inject_head_extras(h)
    # body: FAQ Q&A first (so full English strings match before chrome runs),
    # then master chrome + index reuse, then page-specific
    if name == "faq":
        h = apply(h, seo_meta.get_faq_pairs(lang))
    h = apply(h, DICT[lang])
    h = apply(h, page.get(lang + "_pairs", []))
    return finish(h, lang, fname)

def finish(h, lang, fname):
    # switcher (desktop header)
    sw = switcher(lang, fname).replace("{lbl}", SW_LABEL[lang])
    h = re.sub(r'<li class="cs_language_select">.*?</li>', lambda m: sw, h, flags=re.S)
    # language row inside the mobile hamburger menu
    h = inject_mobile_lang(h, lang, fname)
    # 4-door mega-menu + two-button CTA (root-absolute links, so pre asset rewrite)
    h = inject_mega(h, lang)
    h = inject_mega_js(h)
    # catalogo demostrativo (antes del reescrito de assets/)
    h = inject_catalog(h, fname, lang)
    # asset paths -> ../assets/
    h = re.sub(r'(["\'(])assets/', r'\1../assets/', h)
    # dead template links -> their live equivalent, then language-folder rewrite
    h = fix_dead_links(h)
    h = fixlinks(h)
    # clean root-relative home links (logo, breadcrumb) + accessible active nav
    h = rewrite_home_links(h, lang)
    h = mark_active_nav(h, lang, fname)
    # html tag / dir / rtl css
    if lang == "es":
        h = h.replace('<html lang="en">', '<html lang="es">')
    elif lang == "zh":
        h = h.replace('<html lang="en">', '<html lang="zh-CN">')  # Simplified Chinese, LTR (no RTL sheet)
    else:
        h = h.replace('<html lang="en">', '<html lang="ar" dir="rtl">')
        # inner pages use href="...xaru.css">, index uses "... />"; match both
        h = re.sub(r'(<link rel="stylesheet" href="\.\./assets/css/xaru\.css"\s*/?>)',
                   r'\1\n    <link rel="stylesheet" href="../assets/css/xaru-rtl.css" />',
                   h, count=1)
        h = h.replace('<div class="swiper xr_hero_slider">',
                      '<div class="swiper xr_hero_slider" dir="rtl">')
    h = ensure_h1(h, fname)
    h = enforce_single_h1(h)
    out = "/home/claude/work/site/xaru/%s/%s" % (lang, fname)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(h)
    print(lang, "->", out, len(h), "bytes")
    return h

# ---------------------------------------------------------------- English root (in place)
def build_en(name):
    """Rewrite the English root page's switcher (4 real links, ZH active) and
    hreflang block in place. Asset paths / body copy stay English & untouched.
    Runs AFTER the translated pages are built from the pristine source."""
    fname = name + ".html"
    p = "/home/claude/work/site/xaru/%s" % fname
    with open(p, encoding="utf-8") as f:
        h = f.read()
    # head meta (title/desc/og/twitter/og:url) via the Phase-6 SEO source of truth
    h = seo_meta.set_head(h, "en", fname)
    sw = switcher("en", fname).replace("{lbl}", SW_LABEL["en"])
    h = re.sub(r'<li class="cs_language_select">.*?</li>', lambda m: sw, h, flags=re.S)
    # mobile hamburger language row + head auto-detect script (root: no ../ rewrite)
    h = inject_mobile_lang(h, "en", fname)
    # 4-door mega-menu + two-button CTA (English root, no ../ rewrite)
    h = inject_mega(h, "en")
    h = inject_mega_js(h)
    h = inject_head_extras(h)
    h = inject_catalog(h, fname, "en")
    # clean root-relative home links (logo, breadcrumb) + accessible active nav
    h = fix_dead_links(h)
    h = rewrite_home_links(h, "en")
    h = mark_active_nav(h, "en", fname)
    # hreflang / canonical + JSON-LD: rebuild fresh for every page (idempotent)
    h = strip_alts(h)
    h = strip_jsonld(h)
    block = alternates_en(fname)
    ld = seo_meta.jsonld_for("en", fname)
    h = h.replace("</head>", "    " + block + "\n" + ld + "  </head>", 1)
    h = ensure_h1(h, fname)
    h = enforce_single_h1(h)
    with open(p, "w", encoding="utf-8") as f:
        f.write(h)
    print("en ->", p, len(h), "bytes")

# ================================================================ shell pages (Phase 1)
SHELL_DIR = {"en": "", "es": "es/", "ar": "ar/", "zh": "zh/"}
HTMLLANG  = {"en": "en", "es": "es", "ar": "ar", "zh": "zh-CN"}

def _shell_head(lang, slug, title, desc, css=()):
    # Phase 6: title/description come from the SEO source of truth when the slug
    # has a curated entry; the generator-supplied strings are the fallback.
    title, desc = seo_meta.shell_meta(lang, slug, title, desc)
    social = seo_meta.shell_social(lang, slug, title, desc)
    ld = seo_meta.shell_jsonld(lang, slug)
    title, desc = seo_meta.esc(title), seo_meta.esc(desc)
    pref = SHELL_DIR[lang]
    alts = "\n    ".join([
        '<link rel="alternate" type="text/llms.txt" href="/llms.txt" />',
        '<link rel="canonical" href="https://xaruhome.com/%s%s/" />' % (pref, slug),
        '<link rel="alternate" hreflang="en" href="https://xaruhome.com/%s/" />' % slug,
        '<link rel="alternate" hreflang="es" href="https://xaruhome.com/es/%s/" />' % slug,
        '<link rel="alternate" hreflang="ar" href="https://xaruhome.com/ar/%s/" />' % slug,
        '<link rel="alternate" hreflang="zh-CN" href="https://xaruhome.com/zh/%s/" />' % slug,
        '<link rel="alternate" hreflang="x-default" href="https://xaruhome.com/%s/" />' % slug,
    ])
    rtl = "".join('\n    <link rel="stylesheet" href="/assets/css/%s" />' % c for c in css)
    if lang == "ar":
        rtl += '\n    <link rel="stylesheet" href="/assets/css/xaru-rtl.css" />'
    return '''<!DOCTYPE html>
<html lang="%s"%s>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script src="/assets/js/xaru-lang-detect.js"></script>
    <meta name="description" content="%s" />
    <meta name="robots" content="index, follow" />
    %s
    <link rel="preconnect" href="https://xaruhome.com" />
    <link rel="icon" href="/assets/img/xaru/favicon.png" type="image/png" />
    <link rel="stylesheet" href="/assets/css/aos.min.css" />
    <link rel="stylesheet" href="/assets/css/bootstrap.min.css" />
    <link rel="stylesheet" href="/assets/css/tom-select.min.css" />
    <link rel="stylesheet" href="/assets/css/fontawesome.min.css" />
    <link rel="stylesheet" href="/assets/css/flag-icon.min.css" />
    <link rel="stylesheet" href="/assets/css/flatpickr.min.css" />
    <link rel="stylesheet" href="/assets/css/odometer.min.css" />
    <link rel="stylesheet" href="/assets/css/lightgallery.min.css" />
    <link rel="stylesheet" href="/assets/css/slick.min.css" />
    <link rel="stylesheet" href="/assets/css/data-tables.min.css" />
    <link rel="stylesheet" href="/assets/css/style.css" />
    <link rel="stylesheet" href="/assets/css/xaru.css" />%s
    <title>%s</title>
    %s
%s
  </head>''' % (HTMLLANG[lang], ' dir="rtl"' if lang == "ar" else "",
                desc, social, rtl, title, alts, ld)

def _shell_header(lang):
    home = HOME[lang]
    # mega-menu nav (root-absolute), switcher + mobile lang row, two-button CTA
    nav = megamenu(lang)
    sw = switcher(lang).replace("{lbl}", SW_LABEL[lang])
    mlang = mobile_switcher(lang).replace("{lbl}", SW_LABEL[lang])
    cta = right_buttons(lang)
    return '''    <div class="xr_transition_overlay"><span class="xr_layer"></span></div>
    <header class="cs_site_header cs_style_1 cs_sticky_header cs_primary_color cs_fs_14 cs_medium cs_primary_font text-uppercase">
      <div class="cs_header_main position-relative">
        <div class="container">
          <div class="cs_main_header_in">
            <div class="cs_main_header_left">
              <a href="%s" aria-label="Home page link" class="cs_site_brand">
                <img src="/assets/img/xaru/wordmark_gold_360.png" alt="XARU HOME" />
              </a>
            </div>
            <div class="cs_main_header_center">
              <div class="cs_nav">
                <div class="cs_nav_list_wrap">
                  %s
                  %s
                  <span class="cs_close_nav"></span>
                </div>
              </div>
            </div>
            <div class="cs_main_header_right">
              <ul class="cs_right_nav_list cs_mp_0">
                %s
                %s
              </ul>
            </div>
          </div>
        </div>
      </div>
    </header>''' % (home, nav, mlang, sw, cta)

def _shell_footer(lang):
    home = HOME[lang]
    explore = _t(ARCH.T("Explore", "Explorar", "استكشاف", "探索"), lang)
    company = _t(ARCH.T("Company", "Compañía", "الشركة", "公司"), lang)
    tagline = _t(ARCH.T("Global real estate, development and business solutions — one international structure.",
                        "Inmobiliario, desarrollo y soluciones empresariales globales — una sola estructura internacional.",
                        "عقارات وتطوير وحلول أعمال عالمية — بنية دولية واحدة.",
                        "全球房地产、开发与商业解决方案——单一国际架构。"), lang)
    legal = _t(ARCH.T("XARU HOME — a NEXARU GLOBAL brand. Licensed in the United Arab Emirates.",
                      "XARU HOME — una marca de NEXARU GLOBAL. Con licencia en los Emiratos Árabes Unidos.",
                      "XARU HOME — علامة من NEXARU GLOBAL. مرخّصة في الإمارات العربية المتحدة.",
                      "XARU HOME — NEXARU GLOBAL 旗下品牌。持有阿拉伯联合酋长国牌照。"), lang)
    doors = "\n                  ".join(
        '<li><a href="%s%s/" aria-label="Footer menu link">%s</a></li>' % (home, d["slug"], _t(d["label"], lang))
        for d in ARCH.NAV[:4])
    comp = "\n                  ".join(
        '<li><a href="%s%s/" aria-label="Footer menu link">%s</a></li>' % (home, d["slug"], _t(d["label"], lang))
        for d in ARCH.NAV[4:])
    comp += ('\n                  <li><a href="%sprivate-enquiry/" aria-label="Footer menu link">%s</a></li>'
             % (home, _t(ARCH.BTN_ENQUIRY, lang)))
    return '''    <footer class="cs_footer cs_style_1 cs_primary_bg cs_bg_filed" data-src="/assets/img/footer-bg-1.svg">
      <div class="container">
        <div class="cs_footer_main">
          <div class="row cs_gap_y_30">
            <div class="col-xl-5 col-lg-4">
              <div class="cs_footer_widget cs_text_widget">
                <div class="cs_logo"><img src="/assets/img/xaru/lockup_white_360.png" alt="XARU HOME" /></div>
                <p class="cs_gray_color cs_mb_23" style="max-width: 340px">%s</p>
              </div>
            </div>
            <div class="col-xl-3 col-lg-4">
              <div class="cs_footer_widget cs_menu_widget">
                <h3 class="cs_footer_widget_title cs_fs_20 cs_semibold cs_white_color cs_mb_17">%s</h3>
                <ul class="cs_footer_menu cs_gray_color cs_mp_0">
                  %s
                </ul>
              </div>
            </div>
            <div class="col-xl-3 col-lg-4">
              <div class="cs_footer_widget cs_menu_widget">
                <h3 class="cs_footer_widget_title cs_fs_20 cs_semibold cs_white_color cs_mb_17">%s</h3>
                <ul class="cs_footer_menu cs_gray_color cs_mp_0">
                  %s
                </ul>
              </div>
            </div>
          </div>
        </div>
        <div class="cs_footer_bottom cs_gray_color">
          <div class="cs_footer_text">%s</div>
          <div class="cs_footer_bottom_menu">
            <div class="cs_social_links xr_social_squares">
              <a href="#" aria-label="LinkedIn"><i class="fa-brands fa-linkedin-in"></i></a>
              <a href="#" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
              <a href="#" aria-label="YouTube"><i class="fa-brands fa-youtube"></i></a>
            </div>
          </div>
        </div>
      </div>
    </footer>
    <button type="button" name="ScrollToTopBtn" class="cs_scrollup_btn" id="scrollToTopBtn">
      <i class="fa-solid fa-arrow-up"></i>
    </button>
    <script src="/assets/js/jquery.min.js"></script>
    <script src="/assets/js/slick.min.js"></script>
    <script src="/assets/js/odometer.min.js"></script>
    <script src="/assets/js/tom-select.min.js"></script>
    <script src="/assets/js/flatpickr.min.js"></script>
    <script src="/assets/js/lenis.min.js"></script>
    <script src="/assets/js/light-gallery.min.js"></script>
    <script src="/assets/js/data-tables.min.js"></script>
    <script src="/assets/js/aos.min.js"></script>
    <script src="/assets/js/main.js"></script>
    <script src="/assets/js/xaru-mega.js"></script>
    <script src="/assets/js/xaru-effects.js"></script>
    <script src="/assets/js/xaru-transition.js"></script>
  </body>
</html>''' % (tagline, explore, doors, company, comp, legal)

def _shell_hero(lang, shell):
    slug = shell["slug"]
    img = ARCH.HERO_IMG.get(slug, "01_hero_v2.jpg")
    eyebrow = _t(ARCH.DOOR_EYEBROW.get(shell.get("door", slug), shell["label"]), lang)
    crumbs = ['<li class="breadcrumb-item"><a href="%s" aria-label="Back to home button">%s</a></li>'
              % (HOME[lang], _t(ARCH.CRUMB_HOME, lang))]
    for (plabel, pslug) in shell.get("parents", []):
        crumbs.append('<li class="breadcrumb-item"><a href="%s%s/">%s</a></li>'
                      % (HOME[lang], pslug, _t(plabel, lang)))
    crumbs.append('<li class="breadcrumb-item active">%s</li>' % _t(shell["label"], lang))
    return '''    <section class="cs_page_header cs_style_1 cs_center cs_bg_filed xr_duotone_overlay position-relative" data-src="%s">
      <div class="container">
        <div class="cs_page_header_content text-center">
          <span class="cs_page_header_subtitle cs_fs_14" style="letter-spacing:3px;text-transform:uppercase;color:rgba(245,241,232,.9)">%s</span>
          <h1 class="cs_page_header_title cs_fs_49 mb-0" data-aos="fade-up">%s</h1>
          <ol class="breadcrumb cs_center mb-0">
            %s
          </ol>
        </div>
      </div>
    </section>''' % (gen2_src(img, 1920), eyebrow, _t(shell["label"], lang), "\n            ".join(crumbs))

def _shell_intro(lang, shell):
    return '''    <section>
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container">
        <div class="row"><div class="col-lg-9">
          <p class="xr_pillar_intro" data-aos="fade-up">%s</p>
          <p class="xr_pillar_lead" style="max-width:720px">%s</p>
          <p class="xr_pillar_ph">%s</p>
        </div></div>
      </div>
    </section>''' % (_t(shell["intro"], lang), _t(shell["intro_sub"], lang), _t(ARCH.PH, lang))

def _shell_sections(lang, shell):
    home = HOME[lang]
    out = []
    for (num, heading) in ARCH.PILLAR_SECTIONS:
        if num == "12":
            out.append('''    <section class="xr_pillar_sec" id="s12">
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container">
        <div class="cs_cta cs_style_1 text-center" style="border:1px solid var(--border-color);border-radius:16px;padding:56px 24px;background:rgba(250,248,242,.6)">
          <b class="xr_sec_num">12</b>
          <h2 class="cs_section_title cs_fs_38" data-aos="fade-up">%s</h2>
          <p class="xr_pillar_lead" style="margin:0 auto 24px;max-width:560px">%s</p>
          <div class="d-flex gap-3 flex-wrap justify-content-center">
            <a href="%sprivate-enquiry/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a>
            <a href="%sopportunities/submit/" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>
          </div>
        </div>
      </div>
      <div class="cs_height_120 cs_height_lg_75"></div>
    </section>''' % (_t(heading, lang), _t(ARCH.SECTION_LEAD, lang), home,
                     _t(ARCH.BTN_ENQUIRY, lang), home, _t(ARCH.BTN_SUBMIT, lang)))
            continue
        extra = ""
        if num == "10":
            extra = '\n          <p class="xr_pillar_note">%s</p>' % _t(ARCH.CAPABILITY_NOTE, lang)
        out.append('''    <section class="xr_pillar_sec" id="s%s">
      <div class="cs_height_75 cs_height_lg_50"></div>
      <div class="container">
        <div class="cs_section_heading cs_style_1 cs_type_1">
          <div class="cs_section_heading_left">
            <b class="xr_sec_num">%s</b>
            <span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>
            <h2 class="cs_section_title cs_fs_38 mb-0" data-aos="fade-up">%s</h2>
          </div>
        </div>
        <div class="xr_pillar_body">
          <p class="xr_pillar_lead">%s</p>
          <p class="xr_pillar_ph">%s</p>%s
        </div>
      </div>
    </section>''' % (num, num, _t(shell["label"], lang), _t(heading, lang),
                     _t(ARCH.SECTION_LEAD, lang), _t(ARCH.PH, lang), extra))
    return "\n".join(out)

def _preloader():
    return '''    <div class="cs_preloader">
      <div class="xr_preloader_layer"></div>
      <div class="cs_preloader_in cs_center_column text-center">
        <img src="/assets/img/xaru/monogram_gold_160.png" alt="XARU HOME monogram" class="xr_preloader_logo cs_mb_24" />
        <p class="cs_fs_20 cs_primary_font mb-0 xr_text_rotater" data-text="XARU HOME | Global Luxury | Loading">XARU HOME</p>
      </div>
    </div>'''

# ---------------------------------------------------------------- video en paginas pilar
# Biblia V3 §5: minimo 1 video en cada pagina pilar, y prohibido repetir el mismo
# video en todas. Con seis clips disponibles se reparte asi; ninguna pagina
# comparte clip con su vecina inmediata.
PILLAR_VIDEO = {
    "real-estate":             "xaru-private-villa-cliffside",
    "developments":            "xaru-land-development-coastal",
    "capital":                 "xaru-capital-london-construction",
    "business-infrastructure": "xaru-hospitality-resort-beachfront",
    "company":                 "xaru-hero-coastal-territory",
}

def strip_video_bands(h):
    """Elimina bandas de video ya inyectadas para que reinyectar sea idempotente."""
    return re.sub(r'\s*<section class="xr_video_band_wrap">.*?</section>', "", h, flags=re.S)

def video_band(vid, caption=""):
    """Banda de video a todo ancho. Carga diferida: las fuentes van en data-src
    y las activa xaru-effects.js cuando la banda entra en pantalla."""
    if not vid:
        return ""
    cap = ('<p class="xr_video_band_cap">%s</p>' % caption) if caption else ""
    tpl = ('    <section class="xr_video_band_wrap">\n'
           '      <div class="container">\n'
           '        <div class="xr_video_band">\n'
           '          <video class="xr_video_band_el" muted loop playsinline preload="none"\n'
           '                 poster="/assets/img/xaru/video-posters/%s.jpg"\n'
           '                 aria-hidden="true" data-xr-lazyvideo="1">\n'
           '            <source data-src="/assets/video/%s.webm" type="video/webm" />\n'
           '            <source data-src="/assets/video/%s.mp4" type="video/mp4" />\n'
           '          </video>\n'
           '        </div>%s\n'
           '      </div>\n'
           '    </section>')
    return tpl % (vid, vid, vid, cap)

def _write_shell(lang, slug, title, desc, body, css=(), js=()):
    # §5: banda de video propia de cada pagina pilar de primer nivel.
    # Se inyecta aqui porque las puertas (developments, capital,
    # business-infrastructure, company) tienen constructores propios y no
    # pasan por build_pillar. El guard evita duplicarla si ya venia puesta.
    _v = None                               # banda retirada: rompia el diseno
    body = strip_video_bands(body)
    if _v:
        # Detras del hero, nunca delante: un video sin titulo encima de la
        # pagina no dice nada y parte la lectura.
        _j = body.find("</section>")
        if _j >= 0:
            _j += len("</section>")
            body = body[:_j] + "\n" + video_band(_v) + body[_j:]
        else:
            body = body + "\n" + video_band(_v)
    head = _shell_head(lang, slug, title, desc, css=css)
    foot = _shell_footer(lang)
    if js:
        foot = foot.replace("  </body>", "".join(
            '    <script src="/assets/js/%s"></script>\n' % f for f in js) + "  </body>", 1)
    html = head + "\n  <body>\n" + _preloader() + "\n" + _shell_header(lang) + "\n" + \
           body + "\n" + foot
    out = "/home/claude/work/site/xaru/%s%s/index.html" % (SHELL_DIR[lang], slug)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out

def build_shell(lang, shell):
    slug = shell["slug"]
    title = "%s — XARU HOME" % _t(shell["label"], lang)
    desc = "%s %s" % (_t(shell["intro"], lang), _t(shell["intro_sub"], lang))
    body = _shell_hero(lang, shell) + "\n" + _shell_intro(lang, shell) + "\n" + _shell_sections(lang, shell)
    return _write_shell(lang, slug, title, desc, body)

# ---------------------------------------------------------------- form shells
def _field(lang, f, kind="input", opts=None):
    lbl = _t(f, lang)
    if kind == "textarea":
        ctrl = '<textarea rows="4" placeholder="%s"></textarea>' % lbl
    elif kind == "select":
        o = "".join('<option>%s</option>' % _t(x, lang) for x in (opts or []))
        ctrl = '<select><option value="">—</option>%s</select>' % o
    else:
        ctrl = '<input type="text" placeholder="%s" />' % lbl
    return '<div class="xr_form_field"><label>%s</label>%s</div>' % (lbl, ctrl)

def _route_card(lang, anchor, head_t, sub_t, steps):
    ol = "".join('<li><span>%02d</span>%s</li>' % (i + 1, _t(s, lang))
                 for i, s in enumerate(steps))
    return ('<div class="col-lg-6" data-aos="fade-up"><div class="xr_cap_item" id="%s" '
            'style="display:flex;flex-direction:column">'
            '<h3 class="cs_fs_25" style="font-size:24px">%s</h3>'
            '<p style="color:var(--secondary-color)">%s</p>'
            '<ol class="xr_process" style="margin-top:6px">%s</ol>'
            '</div></div>' % (anchor, _t(head_t, lang), _t(sub_t, lang), ol))

def build_submit(lang):
    F = ARCH.FORM_SUBMIT
    S2 = F3.SUBMIT2
    home = HOME[lang]
    shell = {"slug": "opportunities/submit", "label": F["title"], "intro": F["lead"],
             "intro_sub": F["eyebrow"], "parents": [], "door": "capital"}
    common = (_field(lang, F["f_name"]) + _field(lang, F["f_email"]) + _field(lang, F["f_phone"]) +
              _field(lang, F["f_org"]) + _field(lang, F["f_country"]))
    sideA = ('<div class="xr_form_side"><h3>%s</h3>%s%s%s<div class="xr_form_field"><label><input type="checkbox" style="width:auto;margin-right:8px" /> %s</label></div></div>'
             % (_t(F["sideA"], lang),
                _field(lang, ARCH.T("Seeking", "Busco", "أبحث عن", "寻求"), "select", F["seekingA"]),
                _field(lang, F["f_ticket"]), _field(lang, F["f_detail"], "textarea"), _t(F["f_conf"], lang)))
    sideB = ('<div class="xr_form_side"><h3>%s</h3>%s%s%s<div class="xr_form_field"><label><input type="checkbox" style="width:auto;margin-right:8px" /> %s</label></div></div>'
             % (_t(F["sideB"], lang),
                _field(lang, ARCH.T("Seeking", "Busco", "أبحث عن", "寻求"), "select", F["seekingB"]),
                _field(lang, F["f_ticket"]), _field(lang, F["f_detail"], "textarea"), _t(F["f_conf"], lang)))
    routes = (_route_card(lang, "side-a", S2["routeA_h"], S2["routeA_sub"], S2["routeA_steps"]) +
              _route_card(lang, "side-b", S2["routeB_h"], S2["routeB_sub"], S2["routeB_steps"]))
    after = "".join('<li><span>%02d</span>%s</li>' % (i + 1, _t(s, lang))
                    for i, s in enumerate(S2["after_steps"]))
    body = _shell_hero(lang, shell) + '''
    <section>
      <div class="cs_height_100 cs_height_lg_60"></div>
      <div class="container">
        <p class="xr_pillar_intro" style="max-width:820px" data-aos="fade-up">%s</p>
        <div class="cs_height_40 cs_height_lg_30"></div>
        <div class="row cs_gap_y_30">%s</div>
      </div>
      <div class="cs_height_100 cs_height_lg_60"></div>
    </section>
    <section class="cs_gray2_bg">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        <span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>
        <h2 class="cs_section_title cs_fs_38 mb-0" data-aos="fade-up">%s</h2>
        <div class="cs_height_30"></div>
        <ol class="xr_process" style="max-width:820px">%s</ol>
      </div>
      <div class="cs_height_90 cs_height_lg_60"></div>
    </section>
    <section>
      <div class="cs_height_100 cs_height_lg_60"></div>
      <div class="container">
        <span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>
        <h2 class="cs_section_title cs_fs_38 mb-0" data-aos="fade-up">%s</h2>
        <form action="#" method="post" class="xr_form_shell" style="margin-top:28px">
          %s
          <div class="row"><div class="col-md-6">%s</div><div class="col-md-6">%s</div></div>
          <button type="submit" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></button>
          <p class="xr_form_note">%s</p>
        </form>
      </div>
      <div class="cs_height_120 cs_height_lg_75"></div>
    </section>''' % (_t(S2["lead"], lang), routes,
                     _t(S2["after_eyebrow"], lang), _t(S2["after_title"], lang), after,
                     _t(S2["form_eyebrow"], lang), _t(S2["form_title"], lang),
                     common, sideA, sideB, _t(F["submit"], lang), _t(F["note"], lang))
    title = "%s — XARU HOME" % _t(F["title"], lang)
    return _write_shell(lang, "opportunities/submit", title, _t(S2["lead"], lang), body)

# ---------------------------------------------------------------- Phase 3 — deal room + capital door
def build_dealroom(lang):
    D = F3.DEALROOM
    home = HOME[lang]
    shell = next(s for s in ARCH.SHELLS if s["slug"] == "capital/deal-room")
    steps = "".join(
        '<li><span>%02d</span><div><h4 class="cs_fs_20 mb-1">%s</h4>'
        '<p class="mb-0" style="color:var(--secondary-color)">%s</p></div></li>'
        % (i + 1, _t(t, lang), _t(d, lang)) for i, (t, d) in enumerate(D["steps"]))
    prot = D["protect_items"]
    prot_a = "".join('<li>%s</li>' % _t(x, lang) for x in prot[:4])
    prot_b = "".join('<li>%s</li>' % _t(x, lang) for x in prot[4:])
    teasers = [o for o in OPPS if o["model"] == "confidential-teaser"]
    tcards = "\n        ".join(opp_card(lang, o, home) for o in teasers)
    body = _shell_hero(lang, shell) + '''
    <section>
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container"><div class="row"><div class="col-lg-9">
        <p class="xr_pillar_intro" data-aos="fade-up">%s</p>
        <p class="xr_pillar_lead" style="max-width:720px">%s</p>
      </div></div></div>
    </section>
    <section id="route">
      <div class="cs_height_75 cs_height_lg_50"></div>
      <div class="container">
        <span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>
        <h2 class="cs_section_title cs_fs_38 mb-0" data-aos="fade-up">%s</h2>
        <div class="cs_height_30"></div>
        <ol class="xr_process" style="max-width:820px">%s</ol>
      </div>
    </section>
    <section class="cs_gray2_bg" id="protected">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        <span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>
        <h2 class="cs_section_title cs_fs_38 mb-0" data-aos="fade-up">%s</h2>
        <div class="cs_height_20"></div>
        <div class="row"><div class="col-md-6"><ul class="xr_pillar_list">%s</ul></div>
        <div class="col-md-6"><ul class="xr_pillar_list">%s</ul></div></div>
      </div>
      <div class="cs_height_90 cs_height_lg_60"></div>
    </section>
    <section id="teasers">
      <div class="cs_height_100 cs_height_lg_60"></div>
      <div class="container">
        <span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>
        <h2 class="cs_section_title cs_fs_38 mb-0" data-aos="fade-up">%s</h2>
        <p class="xr_pillar_lead" style="max-width:720px">%s</p>
        <div class="cs_height_30"></div>
        <div class="row cs_gap_y_30">
        %s
        </div>
      </div>
      <div class="cs_height_100 cs_height_lg_60"></div>
    </section>
    <section class="cs_gray2_bg" id="request-access">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        <span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>
        <h2 class="cs_section_title cs_fs_38 mb-0" data-aos="fade-up">%s</h2>
        <form action="#" method="post" class="xr_form_shell" style="margin-top:28px">
          <div class="row"><div class="col-md-6">%s</div><div class="col-md-6">%s</div></div>
          <div class="row"><div class="col-md-6">%s</div><div class="col-md-6">%s</div></div>
          <div class="row"><div class="col-md-6">%s</div><div class="col-md-6">%s</div></div>
          %s
          <button type="submit" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></button>
          <p class="xr_form_note">%s</p>
        </form>
      </div>
      <div class="cs_height_90 cs_height_lg_60"></div>
    </section>
    <section class="xr_dark_section text-center">
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container">
        <span class="xr_eyebrow_serif" style="color:#fff">%s</span>
        <h2 class="cs_section_title cs_fs_49" style="color:#fff;max-width:820px;margin:12px auto 28px" data-aos="fade-up">%s</h2>
        <a href="%sprivate-enquiry/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a>
      </div>
      <div class="cs_height_120 cs_height_lg_75"></div>
    </section>''' % (
        _t(D["lead"], lang), _t(D["sub"], lang),
        _t(D["route_eyebrow"], lang), _t(D["route_title"], lang), steps,
        _t(D["protect_eyebrow"], lang), _t(D["protect_title"], lang), prot_a, prot_b,
        _t(D["teaser_eyebrow"], lang), _t(D["teaser_title"], lang), _t(D["teaser_lead"], lang), tcards,
        _t(D["form_eyebrow"], lang), _t(D["form_title"], lang),
        # the seven form fields, laid out 2-2-2 + full-width message
        _field(lang, D["f_name"]), _field(lang, D["f_entity"]),
        _field(lang, D["f_role"]), _field(lang, D["f_jurisdiction"]),
        _field(lang, D["f_interest"]), _field(lang, D["f_ref"]),
        _field(lang, D["f_message"], "textarea"),
        _t(D["submit"], lang), _t(D["note"], lang),
        _t(D["desk_eyebrow"], lang), _t(D["desk_title"], lang), home, _t(D["desk_cta"], lang))
    title = "%s — XARU HOME" % _t(D["title"], lang)
    return _write_shell(lang, "capital/deal-room", title, _t(D["lead"], lang), body)

def build_capital_door(lang):
    C = F3.CAPITAL_DOOR
    home = HOME[lang]
    shell = next(s for s in ARCH.SHELLS if s["slug"] == "capital")
    dual = F3.PILLARS["capital/strategic-partnerships"]["03"]
    colhtml = []
    for c in dual["cols"]:
        items = "".join('<li>%s</li>' % _t(x, lang) for x in c["items"])
        cta = ('<div class="cs_height_25"></div>'
               '<a href="%s%s" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>'
               % (home, c["href"], _t(c["cta"], lang)))
        colhtml.append('<div class="col-md-6" data-aos="fade-up">'
                       '<div class="xr_cap_item" style="display:flex;flex-direction:column">'
                       '<h3 class="cs_fs_25" style="font-size:24px">%s</h3>'
                       '<ul class="xr_pillar_list" style="flex-grow:1">%s</ul>%s'
                       '</div></div>' % (_t(c["h"], lang), items, cta))
    cards = (
        '<div class="col-lg-6" data-aos="fade-up"><a class="xr_infra_card" href="%scapital/strategic-partnerships/">'
        '<h3>%s</h3><p>%s</p><span class="xr_link">%s<i class="fa-solid fa-angle-right"></i></span></a></div>'
        '<div class="col-lg-6" data-aos="fade-up"><a class="xr_infra_card" href="%scapital/deal-room/">'
        '<h3>%s</h3><p>%s</p><span class="xr_link">%s<i class="fa-solid fa-angle-right"></i></span></a></div>'
        % (home, _t(C["division_title"], lang), _t(C["division_lead"], lang), _t(C["division_cta"], lang),
           home, _t(C["dealroom_title"], lang), _t(C["dealroom_lead"], lang), _t(C["dealroom_cta"], lang)))
    body = _shell_hero(lang, shell) + '''
    <section>
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container"><div class="row"><div class="col-lg-9">
        <p class="xr_pillar_intro" data-aos="fade-up">%s</p>
        <p class="xr_pillar_lead" style="max-width:760px">%s</p>
      </div></div></div>
    </section>
    <section id="two-way">
      <div class="cs_height_75 cs_height_lg_50"></div>
      <div class="container">
        <div class="row cs_gap_y_30">%s</div>
      </div>
      <div class="cs_height_100 cs_height_lg_60"></div>
    </section>
    <section class="cs_gray2_bg">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        <div class="row cs_gap_y_30">%s</div>
      </div>
      <div class="cs_height_90 cs_height_lg_60"></div>
    </section>
    <section>
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container">
        <div class="cs_cta cs_style_1 text-center" style="border:1px solid var(--border-color);border-radius:16px;padding:56px 24px;background:rgba(250,248,242,.6)">
          <h2 class="cs_section_title cs_fs_38" data-aos="fade-up">%s</h2>
          <div class="d-flex gap-3 flex-wrap justify-content-center">
            <a href="%sprivate-enquiry/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a>
            <a href="%sopportunities/submit/" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>
          </div>
        </div>
      </div>
      <div class="cs_height_120 cs_height_lg_75"></div>
    </section>''' % (_t(C["lead"], lang), _t(C["not_matchmaker"], lang),
                     "".join(colhtml), cards,
                     _t(ARCH.PILLAR_SECTIONS[-1][1], lang),
                     home, _t(ARCH.BTN_ENQUIRY, lang), home, _t(ARCH.BTN_SUBMIT, lang))
    title = "%s — XARU HOME" % _t(shell["label"], lang)
    return _write_shell(lang, "capital", title, _t(C["lead"], lang), body)

def build_dev_door(lang):
    """Phase 6 — the Developments door, with real copy (replaces the generic shell)."""
    D = F3.DEV_DOOR
    home = HOME[lang]
    shell = next(s for s in ARCH.SHELLS if s["slug"] == "developments")
    card = ('<div class="col-lg-6" data-aos="fade-up"><a class="xr_infra_card" href="%s%s">'
            '<span class="xr_eyebrow_serif" style="display:block;margin-bottom:10px">%s</span>'
            '<h3>%s</h3><p>%s</p><span class="xr_link">%s<i class="fa-solid fa-angle-right"></i></span></a></div>')
    cards = (card % (home, "developments/land-master-developments/",
                     _t(D["land_eyebrow"], lang), _t(D["land_title"], lang),
                     _t(D["land_lead"], lang), _t(D["view_division"], lang)) +
             card % (home, "developments/project-structuring/",
                     _t(D["struct_eyebrow"], lang), _t(D["struct_title"], lang),
                     _t(D["struct_lead"], lang), _t(D["view_division"], lang)))
    chainlinks = ('<a href="%sopportunities/" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>'
                  '<a href="%scapital/" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>'
                  % (home, _t(D["chain_link1"], lang), home, _t(D["chain_link2"], lang)))
    body = _shell_hero(lang, shell) + '''
    <section>
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container"><div class="row"><div class="col-lg-9">
        <p class="xr_pillar_intro" data-aos="fade-up">%s</p>
        <p class="xr_pillar_lead" style="max-width:760px">%s</p>
      </div></div></div>
    </section>
    <section id="divisions">
      <div class="cs_height_75 cs_height_lg_50"></div>
      <div class="container">
        <div class="row cs_gap_y_30">%s</div>
      </div>
      <div class="cs_height_100 cs_height_lg_60"></div>
    </section>
    <section class="cs_gray2_bg" id="chain">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        <span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>
        <h2 class="cs_section_title cs_fs_38 mb-0" data-aos="fade-up">%s</h2>
        <div class="cs_height_20"></div>
        <p class="xr_pillar_lead" style="max-width:820px">%s</p>
        <div class="d-flex gap-3 flex-wrap" style="margin-top:8px">%s</div>
      </div>
      <div class="cs_height_90 cs_height_lg_60"></div>
    </section>
    <section>
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container">
        <div class="cs_cta cs_style_1 text-center" style="border:1px solid var(--border-color);border-radius:16px;padding:56px 24px;background:rgba(250,248,242,.6)">
          <h2 class="cs_section_title cs_fs_38" data-aos="fade-up">%s</h2>
          <div class="d-flex gap-3 flex-wrap justify-content-center">
            <a href="%sprivate-enquiry/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a>
            <a href="%sopportunities/submit/" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>
          </div>
        </div>
      </div>
      <div class="cs_height_120 cs_height_lg_75"></div>
    </section>''' % (_t(D["lead"], lang), _t(D["continuity"], lang), cards,
                     _t(D["chain_eyebrow"], lang), _t(D["chain_title"], lang),
                     _t(D["chain_lead"], lang), chainlinks,
                     _t(ARCH.PILLAR_SECTIONS[-1][1], lang),
                     home, _t(ARCH.BTN_ENQUIRY, lang), home, _t(ARCH.BTN_SUBMIT, lang))
    title = "%s — XARU HOME" % _t(shell["label"], lang)
    return _write_shell(lang, "developments", title, _t(D["lead"], lang), body)

def build_phase3():
    for L in ("en", "es", "ar", "zh"):
        build_pillar(L, "developments/project-structuring")
        build_dev_door(L)
        build_pillar(L, "capital/strategic-partnerships")
        build_capital_door(L)
        build_dealroom(L)
        build_submit(L)
    print("phase3 done")

# ---------------------------------------------------------------- Phase 4 — business infrastructure door
def build_bi_door(lang):
    B = F4.BI_DOOR
    home = HOME[lang]
    shell = next(s for s in ARCH.SHELLS if s["slug"] == "business-infrastructure")
    card = ('<div class="col-lg-6" data-aos="fade-up"><a class="xr_infra_card" href="%s%s">'
            '<span class="xr_eyebrow_serif" style="display:block;margin-bottom:10px">%s</span>'
            '<h3>%s</h3><p>%s</p><span class="xr_link">%s<i class="fa-solid fa-angle-right"></i></span></a></div>')
    cards = (card % (home, "business-infrastructure/trade-financial/",
                     _t(B["trade_eyebrow"], lang), _t(B["trade_title"], lang),
                     _t(B["trade_lead"], lang), _t(B["view_division"], lang)) +
             card % (home, "business-infrastructure/corporate-services/",
                     _t(B["corp_eyebrow"], lang), _t(B["corp_title"], lang),
                     _t(B["corp_lead"], lang), _t(B["view_division"], lang)))
    govlinks = ('<a href="%scompany/#governance" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>'
                '<a href="%scompany/#entities" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>'
                % (home, _t(B["gov_link1"], lang), home, _t(B["gov_link2"], lang)))
    body = _shell_hero(lang, shell) + '''
    <section>
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container"><div class="row"><div class="col-lg-9">
        <p class="xr_pillar_intro" data-aos="fade-up">%s</p>
        <p class="xr_pillar_lead" style="max-width:760px">%s</p>
      </div></div></div>
    </section>
    <section id="divisions">
      <div class="cs_height_75 cs_height_lg_50"></div>
      <div class="container">
        <div class="row cs_gap_y_30">%s</div>
      </div>
      <div class="cs_height_100 cs_height_lg_60"></div>
    </section>
    <section class="cs_gray2_bg" id="governance">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        <span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>
        <h2 class="cs_section_title cs_fs_38 mb-0" data-aos="fade-up">%s</h2>
        <div class="cs_height_20"></div>
        <p class="xr_pillar_lead" style="max-width:820px">%s</p>
        <div class="d-flex gap-3 flex-wrap" style="margin-top:8px">%s</div>
      </div>
      <div class="cs_height_90 cs_height_lg_60"></div>
    </section>
    <section>
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container">
        <div class="cs_cta cs_style_1 text-center" style="border:1px solid var(--border-color);border-radius:16px;padding:56px 24px;background:rgba(250,248,242,.6)">
          <h2 class="cs_section_title cs_fs_38" data-aos="fade-up">%s</h2>
          <div class="d-flex gap-3 flex-wrap justify-content-center">
            <a href="%sprivate-enquiry/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a>
            <a href="%sopportunities/submit/" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>
          </div>
        </div>
      </div>
      <div class="cs_height_120 cs_height_lg_75"></div>
    </section>''' % (_t(B["lead"], lang), _t(B["continuity"], lang), cards,
                     _t(B["gov_eyebrow"], lang), _t(B["gov_title"], lang),
                     _t(B["gov_lead"], lang), govlinks,
                     _t(ARCH.PILLAR_SECTIONS[-1][1], lang),
                     home, _t(ARCH.BTN_ENQUIRY, lang), home, _t(ARCH.BTN_SUBMIT, lang))
    title = "%s — XARU HOME" % _t(shell["label"], lang)
    return _write_shell(lang, "business-infrastructure", title, _t(B["lead"], lang), body)

def build_phase4():
    for L in ("en", "es", "ar", "zh"):
        build_pillar(L, "business-infrastructure/trade-financial")
        build_pillar(L, "business-infrastructure/corporate-services")
        build_bi_door(L)
    print("phase4 done")

def build_enquiry(lang):
    F = ARCH.FORM_ENQUIRY
    shell = {"slug": "private-enquiry", "label": F["title"], "intro": F["lead"],
             "intro_sub": F["eyebrow"], "parents": [], "door": "company"}
    body = _shell_hero(lang, shell) + '''
    <section>
      <div class="cs_height_100 cs_height_lg_60"></div>
      <div class="container">
        <p class="xr_pillar_intro" style="max-width:640px">%s</p>
        <form action="#" method="post" class="xr_form_shell" style="margin-top:28px">
          <div class="row"><div class="col-md-6">%s</div><div class="col-md-6">%s</div></div>
          <div class="row"><div class="col-md-6">%s</div><div class="col-md-6">%s</div></div>
          %s
          %s
          <button type="submit" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></button>
          <p class="xr_form_note">%s</p>
        </form>
      </div>
      <div class="cs_height_120 cs_height_lg_75"></div>
    </section>''' % (_t(F["lead"], lang),
                     _field(lang, F["f_name"]), _field(lang, F["f_email"]),
                     _field(lang, F["f_phone"]), _field(lang, F["f_country"]),
                     _field(lang, F["f_interest"]), _field(lang, F["f_message"], "textarea"),
                     _t(F["submit"], lang), _t(F["note"], lang))
    title = "%s — XARU HOME" % _t(F["title"], lang)
    return _write_shell(lang, "private-enquiry", title, _t(F["lead"], lang), body)

def build_all_shells():
    n = 0
    for L in ("en", "es", "ar", "zh"):
        for shell in ARCH.SHELLS:
            build_shell(L, shell); n += 1
        build_submit(L); build_enquiry(L); n += 2
    print("shells ->", n, "files")

# ================================================================ Phase 2 — property core
import f2_copy as F2  # noqa: E402
# Phase 3 — development & capital core (pillar copy merged into the same registry)
import f3_copy as F3  # noqa: E402
F2.PILLARS.update(F3.PILLARS)
# Phase 4 — business infrastructure (trade & financial · corporate services)
import f4_copy as F4  # noqa: E402
F2.PILLARS.update(F4.PILLARS)
# Phase 5 — institutional trust (Company + Insights hub + foundational articles)
import f5_copy as F5C      # noqa: E402
import f5_articles as F5A  # noqa: E402
with open("/home/claude/work/site/xaru/data/opportunities.json", encoding="utf-8") as _f:
    OPP = json.load(_f)
OPPS = OPP["opportunities"]
STATUSES = OPP["statuses"]

def _asset(p):
    return "/" + p.lstrip("/")

def _slug2(s):
    return re.sub(r'[^a-z0-9]+', '-', str(s).lower()).strip('-') or "x"

def _num(n):
    try:
        return "{:,}".format(int(n))
    except Exception:
        return str(n)

STATUS_MOD = {
 "available": "is-live", "operational": "is-live", "development-ready": "is-live",
 "exclusive-mandate": "is-gold", "open-mandate": "is-gold", "under-negotiation": "is-gold",
 "seeking-capital": "is-warn", "seeking-buyer": "is-warn", "seeking-developer": "is-warn",
 "seeking-operator": "is-warn", "halted-restructuring": "is-warn", "in-validation": "is-warn",
 "under-construction": "is-warn", "off-market": "is-off", "closed": "is-off",
 "sold": "is-sold",
}
OP_STATE = {
 "operational": F2.T("Operational", "Operativo", "تشغيلي", "运营中"),
 "halted": F2.T("Halted", "Detenido", "متوقف", "停滞"),
 "development": F2.T("Development", "Desarrollo", "تطوير", "开发"),
}

def status_badge(lang, key, extra=""):
    lbl = _t(STATUSES[key], lang)
    mod = STATUS_MOD.get(key, "is-gold")
    cls = "xr_status_badge %s%s" % (mod, (" " + extra) if extra else "")
    return '<span class="%s">%s</span>' % (cls, lbl)

def ficha_url(o):
    c = o["catalog"]
    if c == "private-properties":
        base = "real-estate/private-properties"
    elif c == "commercial-hospitality":
        base = "real-estate/commercial-hospitality"
    else:
        base = "opportunities"
    return "%s/%s" % (base, o["id"])

def _loc_str(o, lang):
    L = o["location"]
    if not L.get("country") or L["country"] == "Undisclosed":
        return _t(F2.T("Undisclosed", "Sin revelar", "غير مُفصَح عنه", "未披露"), lang)
    parts = [x for x in [L.get("city"), L.get("country")] if x]
    return " · ".join(parts)

SOLD_STATES = ("sold",)

def is_sold(o):
    return o.get("status") in SOLD_STATES

def _price_str(o, lang):
    # Biblia §1.2: en un activo vendido no se puede afirmar precio de cierre si
    # no hay dato verificable. El importe publicado era el de salida, no el de
    # cierre: mostrarlo bajo una insignia "Vendido" seria afirmar una cifra que
    # nadie ha confirmado. Se retira.
    if o.get("status") in SOLD_STATES and not o.get("closingPriceDisclosed"):
        return _t(F2.SOLD["price_withheld"], lang)
    d = o["price"].get("display", "")
    if d == "Undisclosed":
        return _t(F2.T("Undisclosed", "Sin revelar", "غير مُفصَح عنه", "未披露"), lang)
    if d == "Price upon application":
        return _t(F2.UI["poa"], lang)
    return d

def _tv(v, lang):
    """Translate a value that may be a 4-language dict (Phase 4 productive teasers)."""
    if isinstance(v, dict):
        return _t(v, lang)
    return v

def _desc(o, lang):
    m = o["model"]
    if m == "residential":
        s = o.get("specs", {})
        bits = []
        if s.get("bedrooms"):
            bits.append("%s %s" % (s["bedrooms"], _t(F2.FICHA["bedrooms"], lang).lower()))
        if s.get("style"):
            bits.append(s["style"])
        return " · ".join(bits) if bits else (s.get("style") or "")
    if m == "commercial-hospitality":
        op = o.get("operating", {})
        st = _t(OP_STATE.get(op.get("state"), F2.T(op.get("state", ""), "", "", "")), lang)
        return "%s %s · %s" % (op.get("keys", ""), _t(F2.FICHA["keys"], lang).lower(), st)
    if m == "land-development":
        ld = o.get("land", {})
        return "%s m² · %s" % (_num(ld.get("areaSqm")), ld.get("phase", ""))
    if m == "confidential-teaser":
        return _t(o["teaser"]["summary"], lang)
    if m == "productive-asset":
        pr = o.get("productive", {})
        bits = [_tv(pr.get("category"), lang), _tv(pr.get("scale"), lang)]
        return " · ".join(x for x in bits if x)
    return ""

def _facet_val(o, key):
    L = o["location"]
    if key == "location":
        return L.get("country") or "undisclosed"
    if key == "region":
        return L.get("region") or L.get("country") or "undisclosed"
    if key == "lifestyle":
        return o.get("specs", {}).get("style") or "-"
    if key == "bedrooms":
        b = o.get("specs", {}).get("bedrooms")
        return str(b) if b else "-"
    if key == "operating":
        return o.get("operating", {}).get("state") or "-"
    if key == "structure":
        return o.get("operating", {}).get("structure") or "-"
    if key == "phase":
        return o.get("land", {}).get("phase") or o.get("productive", {}).get("phase") or "-"
    if key == "opp_type":
        return o.get("status")
    return "-"

def _img_note(lang, kind="ref"):
    """Media-provenance caption (visual bible): stock may stand for a category, never a specific asset."""
    txt = ARCH.MEDIA_GEO_NOTE if kind == "geo" else ARCH.MEDIA_REF_NOTE
    return '<p class="xr_img_note">%s</p>' % _t(txt, lang)

def opp_card(lang, o, home, facets=(), sold=False):
    da = " ".join('data-f-%s="%s"' % (k, _slug2(_facet_val(o, k))) for k in facets)
    # El estado es una faceta mas, y la unica por la que se recuperan los vendidos.
    da += ' data-f-status="%s"' % ("sold" if sold else "active")
    if sold:
        da += ' data-sold="1" hidden'
    # La ficha muestra la foto a ~700 px de ancho: sirve la derivada de 1280,
    # no el master de 1920 (mismo encuadre, un tercio del peso).
    img = gen2_bg(o["images"][0].split("/")[-1], 1280)
    url = "%s%s/" % (home, ficha_url(o))
    badge = status_badge(lang, o["status"])
    sec = ""
    for s in o.get("secondaryStatus", [])[:1]:
        sec = status_badge(lang, s, "xr_badge_sm")
    return '''<div class="col-lg-4 col-md-6 xr_opp_col" %s data-aos="fade-up">
          <div class="xr_land_card xr_opp_card">
            <div class="xr_land_card_img">
              <div class="xr_px_img" style="%s"></div>
              <div class="xr_badge_stack">%s%s</div>
            </div>
            <div class="xr_land_card_body">
              <h3>%s</h3>
              <p class="xr_land_card_meta mb-2">%s</p>
              <p class="xr_opp_desc">%s</p>
              <div class="xr_land_price">
                <span>%s</span>
                <a href="%s" class="xr_link" aria-label="View details">%s<i class="fa-solid fa-angle-right"></i></a>
              </div>
            </div>
          </div>
        </div>''' % (da, img, badge, sec, _t(o["title"], lang), _loc_str(o, lang),
                     _desc(o, lang), _price_str(o, lang), url, _t(F2.UI["view_details"], lang))

def catalog_block(lang, catalog_key, home, items=None, block_id=None):
    meta = F2.CATALOG[catalog_key]
    facets = meta["facets"]
    if items is None:
        items = [o for o in OPPS if o["catalog"] == catalog_key]
    # Biblia §1.2: el inventario vendido sale de los resultados por defecto y del
    # contador. Sigue estando: se recupera con el filtro explicito de estado.
    sold = [o for o in items if is_sold(o)]
    items = [o for o in items if not is_sold(o)]
    bid = block_id or ("cat_" + _slug2(catalog_key))
    selects = []
    for k in facets:
        seen = {}
        for o in items:
            v = _facet_val(o, k)
            if v == "-":
                continue
            sl = _slug2(v)
            if k == "opp_type":
                disp = _t(STATUSES[o["status"]], lang)
            elif k == "operating":
                disp = _t(OP_STATE.get(v, F2.T(v, v, v, v)), lang)
            else:
                disp = str(v)
            seen[sl] = disp
        opts = "".join('<option value="%s">%s</option>' % (sl, dp) for sl, dp in seen.items())
        selects.append('<div class="xr_filter_field"><label>%s</label>'
                       '<select class="xr_filter_select" data-f="%s"><option value="">%s</option>%s</select></div>'
                       % (_t(F2.FACET_LABEL[k], lang), k, _t(F2.UI["all"], lang), opts))
    if sold:
        # Biblia §1.2: los vendidos deben poder encontrarse con un filtro
        # explicito. Por defecto se sirve el inventario activo.
        selects.append(
            '<div class="xr_filter_field"><label>%s</label>'
            '<select class="xr_filter_select" data-f="status">'
            '<option value="active">%s</option>'
            '<option value="sold">%s</option>'
            '<option value="">%s</option>'
            '</select></div>'
            % (_t(F2.SOLD["facet_label"], lang), _t(F2.SOLD["facet_active"], lang),
               _t(F2.SOLD["facet_sold"], lang), _t(F2.UI["all"], lang)))
    cards = "\n        ".join(opp_card(lang, o, home, facets) for o in items)
    if sold:
        cards += "\n        " + "\n        ".join(
            opp_card(lang, o, home, facets, sold=True) for o in sold)
    count = len(items)
    countline = '%s <b class="xr_count_now">%d</b> %s %d %s' % (
        _t(F2.UI["showing"], lang), count, _t(F2.UI["of"], lang), count, _t(F2.UI["results"], lang))
    js = ('''
    <script>
    (function(){
      var root=document.getElementById("%s");if(!root)return;''' % bid) + '''
      var sels=root.querySelectorAll(".xr_filter_select");
      var cols=root.querySelectorAll(".xr_opp_col");
      var now=root.querySelector(".xr_count_now");
      function apply(){var n=0;cols.forEach(function(c){var ok=true;
        sels.forEach(function(s){var k=s.getAttribute("data-f"),v=s.value;
          if(v&&c.getAttribute("data-f-"+k)!==v)ok=false;});
        /* Sin filtro de estado elegido, el vendido no entra: es inventario
           historico, no resultado por defecto. */
        var st=root.querySelector('.xr_filter_select[data-f="status"]');
        if(!st&&c.getAttribute("data-sold")==="1")ok=false;
        c.hidden=!ok;
        c.style.display=ok?"":"none";if(ok)n++;});
        if(now)now.textContent=n;
        var e=root.querySelector(".xr_no_results");if(e)e.style.display=n?"none":"block";}
      sels.forEach(function(s){s.addEventListener("change",apply);});
      var r=root.querySelector(".xr_filter_reset");
      if(r)r.addEventListener("click",function(){sels.forEach(function(s){s.value="";});apply();});
    })();
    </script>'''
    return '''    <div class="container xr_catalog" id="%s">
      <div class="xr_filter_bar" data-aos="fade-up">
        <span class="xr_filter_label">%s</span>
        %s
        <button type="button" class="xr_filter_reset">%s</button>
      </div>
      <p class="xr_catalog_count">%s</p>
      <div class="cs_height_40 cs_height_lg_30"></div>
      <div class="row cs_gap_y_30">
        %s
      </div>
      <p class="xr_no_results"%s>%s</p>
    </div>%s''' % (bid, _t(F2.UI["filters"], lang), "\n        ".join(selects),
                   _t(F2.UI["reset"], lang), countline, cards,
                   '' if not items else ' style="display:none"',
                   # Si no queda inventario activo el vacio es real, no un filtro
                   # mal puesto: se explica y se ofrece la salida (Biblia §36).
                   _t(F2.SOLD["empty_private"], lang) if not items else _t(F2.UI["no_results"], lang),
                   js)

CAT_IMG = {"private-properties": "09_villa_como.jpg",
           "commercial-hospitality": "05_hotel_project.jpg",
           "land-projects": "03_land_mega.jpg"}

def _page_header(lang, eyebrow, title, crumbs, img):
    cr = "\n            ".join(crumbs)
    return '''    <section class="cs_page_header cs_style_1 cs_center cs_bg_filed xr_duotone_overlay position-relative" data-src="%s" style="%s">
      <div class="container">
        <div class="cs_page_header_content text-center">
          <span class="cs_page_header_subtitle cs_fs_14" style="letter-spacing:3px;text-transform:uppercase;color:rgba(245,241,232,.9)">%s</span>
          <h1 class="cs_page_header_title cs_fs_49 mb-0" data-aos="fade-up">%s</h1>
          <ol class="breadcrumb cs_center mb-0">
            %s
          </ol>
        </div>
      </div>
    </section>''' % (gen2_src(img, 1920), gen2_bg(img, 1920), eyebrow, title, cr)

def _crumbs(lang, trail):
    home = HOME[lang]
    out = ['<li class="breadcrumb-item"><a href="%s" aria-label="Back to home button">%s</a></li>'
           % (home, _t(ARCH.CRUMB_HOME, lang))]
    for (lbl, slug) in trail[:-1]:
        out.append('<li class="breadcrumb-item"><a href="%s%s/">%s</a></li>' % (home, slug, _t(lbl, lang)))
    out.append('<li class="breadcrumb-item active">%s</li>' % _t(trail[-1][0], lang))
    return out

# ---------------------------------------------------------------- operaciones anteriores
def build_sold_page(lang):
    """Biblia §1.2 y §5.1: seccion editorial de operaciones anteriores.

    Los activos vendidos salen del inventario activo y de los resultados por
    defecto, pero no del sitio: aqui quedan reunidos, con su insignia, sin
    precio de cierre y sin canal de contacto comercial.
    """
    home = HOME[lang]
    RE = ARCH.T("Real Estate", "Inmobiliario", "العقارات", "房地产")
    slug = "real-estate/sold"
    title = "%s — XARU HOME" % _t(F2.SOLD["page_title"], lang)
    desc = _t(F2.SOLD["page_lead"], lang)
    trail = [(RE, "real-estate"), (F2.SOLD["page_title"], slug)]
    hero = _page_header(lang, _t(F2.SOLD["page_eyebrow"], lang),
                        _t(F2.SOLD["page_title"], lang),
                        _crumbs(lang, trail), CAT_IMG["private-properties"])
    sold = [o for o in OPPS if is_sold(o)]
    cards = "\n        ".join(
        opp_card(lang, o, home).replace(' data-f-status="active"', ' data-f-status="sold"')
        for o in sold)
    body = hero + '''
    <section>
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container"><div class="row"><div class="col-lg-9">
        <p class="xr_pillar_intro" data-aos="fade-up">%s</p>
      </div></div></div>
      <div class="cs_height_50 cs_height_lg_30"></div>
      <div class="container xr_catalog">
        <div class="row cs_gap_y_30">
        %s
        </div>
      </div>
      <div class="cs_height_150 cs_height_lg_80"></div>
    </section>''' % (_t(F2.SOLD["page_lead"], lang), cards)
    return _write_shell(lang, slug, title, desc, body)

# ================================================================ Marketplace (Biblia §5.1)
# Rutas de resultados con paridad de portal: comprar, alquilar, comercial,
# suelo, mapa y busqueda libre. Cada ruta es la misma aplicacion
# (assets/js/xaru-marketplace.js) con el filtro base fijado en el montaje, de
# modo que la URL es canonica y compartible, y el dia que exista el Search
# Service no cambia ni una sola de estas paginas.

MARKET_ROUTES = [
    # slug, offering, category, view, imagen de cabecera
    ("real-estate/search",         "",      "",            "list",  "31_page_header.jpg"),
    ("real-estate/buy",            "sale",  "residential", "list",  "09_villa_como.jpg"),
    ("real-estate/rent",           "rent",  "residential", "list",  "11_villa_marbella.jpg"),
    ("real-estate/commercial/buy", "sale",  "commercial",  "list",  "05_hotel_project.jpg"),
    ("real-estate/commercial/rent","rent",  "commercial",  "list",  "18_business_district.jpg"),
    ("real-estate/land",           "sale",  "land",        "list",  "22_land_parcels.jpg"),
    ("real-estate/map",            "",      "",            "split", "16_atlantic_aerial.jpg"),
]

MARKET_COPY = {
"real-estate/search": dict(
  eyebrow=ARCH.T("Inventory", "Inventario", "المعروض", "资产库"),
  title=ARCH.T("Search the inventory", "Buscar en el inventario", "ابحث في المعروض", "检索资产库"),
  lead=ARCH.T(
    "Every asset under mandate, in one place: residential, commercial, hospitality and land, across the markets where the firm operates. Filter by country, city, typology, price and surface; the address bar carries the search, so any result set can be sent to a client exactly as you see it.",
    "Todos los activos bajo mandato, en un solo lugar: residencial, comercial, hostelería y suelo, en los mercados donde opera la firma. Filtre por país, ciudad, tipología, precio y superficie; la barra de direcciones lleva la búsqueda, de modo que cualquier conjunto de resultados puede enviarse a un cliente tal como usted lo ve.",
    "جميع الأصول تحت التفويض في مكان واحد: سكني وتجاري وضيافة وأراضٍ، في الأسواق التي تعمل بها الشركة. رشّح حسب الدولة والمدينة والنوع والسعر والمساحة؛ ويحمل شريط العنوان البحث، فأي مجموعة نتائج يمكن إرسالها إلى العميل كما تراها تماماً.",
    "所有受托资产集中于此：住宅、商业、酒店与土地，覆盖本公司经营的各个市场。可按国家、城市、类型、价格与面积筛选；地址栏即承载搜索条件，任何结果集都可原样发送给客户。")),
"real-estate/buy": dict(
  eyebrow=ARCH.T("Residential — sale", "Residencial — venta", "سكني — للبيع", "住宅 — 出售"),
  title=ARCH.T("Residential for sale", "Residencial en venta", "سكني للبيع", "住宅出售"),
  lead=ARCH.T(
    "Private residences under sale mandate: villas, penthouses, estates, private islands and restored heritage houses. Each record carries its verification status, its typology and the office that holds the mandate.",
    "Residencias privadas bajo mandato de venta: villas, áticos, fincas, islas privadas y casas históricas rehabilitadas. Cada registro lleva su estado de verificación, su tipología y la oficina que tiene el mandato.",
    "مساكن خاصة تحت تفويض بيع: فلل وبنتهاوس وضياع وجزر خاصة وبيوت تراثية مُرمَّمة. يحمل كل سجل حالة التوثيق والنوع والمكتب صاحب التفويض.",
    "受托出售的私人住宅：别墅、顶层公寓、庄园、私人岛屿与修复的历史宅邸。每条记录均标注核验状态、物业类型及持有委托的分支机构。")),
"real-estate/rent": dict(
  eyebrow=ARCH.T("Residential — lease", "Residencial — alquiler", "سكني — للإيجار", "住宅 — 租赁"),
  title=ARCH.T("Residential to rent", "Residencial en alquiler", "سكني للإيجار", "住宅租赁"),
  lead=ARCH.T(
    "Long-let and seasonal residences, quoted per year. Relocation cases are handled by the same desk that manages the corporate structuring, so a lease and a residency file move together.",
    "Residencias de larga duración y de temporada, cotizadas por año. Los casos de relocalización los lleva la misma mesa que gestiona la estructuración corporativa, de modo que un arrendamiento y un expediente de residencia avanzan juntos.",
    "مساكن للإيجار الطويل والموسمي، مُسعَّرة سنوياً. تتولى حالات الانتقال المكتب نفسه الذي يدير الهيكلة المؤسسية، فيتقدم عقد الإيجار وملف الإقامة معاً.",
    "长租与季节性住宅，按年报价。搬迁安置由负责公司架构的同一团队处理，租约与居留申请同步推进。")),
"real-estate/commercial/buy": dict(
  eyebrow=ARCH.T("Commercial — sale", "Comercial — venta", "تجاري — للبيع", "商业 — 出售"),
  title=ARCH.T("Commercial and hospitality for sale", "Comercial y hostelería en venta", "تجاري وضيافة للبيع", "商业与酒店出售"),
  lead=ARCH.T(
    "Operating hotels, resorts, office and retail assets, logistics and industrial plant. Where the asset trades as a business rather than as bricks, the record states the keys, the operator and the completion status.",
    "Hoteles y resorts en explotación, activos de oficinas y retail, plataformas logísticas e instalaciones industriales. Cuando el activo se transmite como negocio y no como ladrillo, el registro indica las llaves, el operador y el estado de obra.",
    "فنادق ومنتجعات عاملة وأصول مكتبية وتجزئة ومنشآت لوجستية وصناعية. وحين يُتداول الأصل كنشاط تشغيلي لا كعقار، يوضّح السجل عدد المفاتيح والمشغّل وحالة الإنجاز.",
    "在营酒店与度假村、写字楼与零售资产、物流与工业设施。当资产以经营性业务而非单纯不动产交易时，记录会列明客房数、运营方与交付状态。")),
"real-estate/commercial/rent": dict(
  eyebrow=ARCH.T("Commercial — lease", "Comercial — alquiler", "تجاري — للإيجار", "商业 — 租赁"),
  title=ARCH.T("Commercial space to lease", "Espacio comercial en alquiler", "مساحات تجارية للإيجار", "商业空间租赁"),
  lead=ARCH.T(
    "Offices, retail units, warehouses and light industrial space, quoted per year. Fit-out, licensing and the corporate vehicle behind the tenancy are handled inside the same file.",
    "Oficinas, locales, naves y espacio industrial ligero, cotizados por año. La implantación, las licencias y el vehículo societario que firma el arrendamiento se llevan dentro del mismo expediente.",
    "مكاتب ومحال ومستودعات ومساحات صناعية خفيفة، مُسعَّرة سنوياً. ويُدار التجهيز والتراخيص والكيان المؤسسي المستأجر ضمن الملف نفسه.",
    "写字楼、商铺、仓库与轻工业空间，按年报价。装修、执照及承租主体的公司架构在同一档案内一并处理。")),
"real-estate/land": dict(
  eyebrow=ARCH.T("Land", "Suelo", "الأراضي", "土地"),
  title=ARCH.T("Land and large-scale sites", "Suelo y grandes superficies", "الأراضي والمواقع واسعة النطاق", "土地与大型地块"),
  lead=ARCH.T(
    "Development land, coastal and island holdings, agricultural and forestry estates, mining concessions and quarries, energy sites and parcels sized for entire new towns. Surface is stated in hectares where the parcel is measured that way.",
    "Suelo finalista, fincas costeras e insulares, explotaciones agrícolas y forestales, concesiones mineras y canteras, suelo energético y parcelas dimensionadas para ciudades enteras. La superficie se indica en hectáreas cuando la parcela se mide así.",
    "أراضٍ للتطوير، وممتلكات ساحلية وجزرية، وضياع زراعية وحرجية، وامتيازات تعدين ومحاجر، ومواقع طاقة، وقطع بحجم مدن كاملة. وتُذكر المساحة بالهكتار حيث تُقاس القطعة بهذه الوحدة.",
    "开发用地、海岸与岛屿地产、农林庄园、采矿权与采石场、能源用地，以及可容纳整座新城的地块。按公顷计量的地块以公顷标示面积。")),
"real-estate/map": dict(
  eyebrow=ARCH.T("Map", "Mapa", "الخريطة", "地图"),
  title=ARCH.T("The inventory on the map", "El inventario sobre el mapa", "المعروض على الخريطة", "地图上的资产库"),
  lead=ARCH.T(
    "The same inventory read geographically. Pan and zoom to work a market, and switch between map, split and list without losing the filters you already set.",
    "El mismo inventario leído geográficamente. Desplace y acerque para trabajar un mercado, y cambie entre mapa, vista dividida y lista sin perder los filtros que ya haya puesto.",
    "المعروض نفسه مقروءاً جغرافياً. حرّك الخريطة وقرّبها لتعمل على سوق بعينه، وبدّل بين الخريطة والعرض المقسّم والقائمة دون أن تفقد ما ضبطته من مرشحات.",
    "同一资产库的地理视图。平移与缩放以聚焦某一市场，并可在地图、分屏与列表之间切换而不丢失已设定的筛选条件。")),
}

MARKET_LINKS = ARCH.T("Other views", "Otras vistas", "عروض أخرى", "其他视图")

def _market_nav(lang, current):
    home = HOME[lang]
    out = []
    for (slug, _o, _c, _v, _i) in MARKET_ROUTES:
        lbl = _t(MARKET_COPY[slug]["eyebrow"], lang)
        if slug == current:
            out.append('<span class="xr_mp_navlink is-on">%s</span>' % lbl)
        else:
            out.append('<a class="xr_mp_navlink" href="%s%s/">%s</a>' % (home, slug, lbl))
    return ('<nav class="xr_mp_nav" aria-label="%s">%s</nav>'
            % (_t(MARKET_LINKS, lang), "".join(out)))

def build_marketplace(lang, route):
    """Una ruta de resultados. El montaje declara el filtro base; todo lo
    demas —orden, paginacion, mapa, facetas— lo resuelve el cliente contra
    /data/api/v1/search-index.json, que es la proyeccion de la base de datos."""
    slug, offering, category, view, img = route
    copy = MARKET_COPY[slug]
    RE = ARCH.T("Real Estate", "Inmobiliario", "العقارات", "房地产")
    title = "%s — XARU HOME" % _t(copy["title"], lang)
    desc = _t(copy["lead"], lang)
    trail = [(RE, "real-estate")]
    if slug.startswith("real-estate/commercial/"):
        trail.append((ARCH.T("Commercial", "Comercial", "تجاري", "商业"),
                      "real-estate/commercial-hospitality"))
    trail.append((copy["title"], slug))
    hero = _page_header(lang, _t(copy["eyebrow"], lang), _t(copy["title"], lang),
                        _crumbs(lang, trail), img)
    mount = ('<div class="xr_mp" data-marketplace data-offering="%s" data-category="%s" '
             'data-view="%s"></div>' % (offering, category, view))
    body = hero + '''
    <section>
      <div class="cs_height_70 cs_height_lg_45"></div>
      <div class="container"><div class="row"><div class="col-lg-9">
        <p class="xr_pillar_intro" data-aos="fade-up">%s</p>
      </div></div></div>
      <div class="cs_height_30"></div>
      <div class="container">%s</div>
      <div class="cs_height_40 cs_height_lg_25"></div>
      <div class="container">%s</div>
      <div class="cs_height_120 cs_height_lg_70"></div>
    </section>''' % (_t(copy["lead"], lang), _market_nav(lang, slug), mount)
    return _write_shell(lang, slug, title, desc, body,
                        css=("xaru-marketplace.css",), js=("xaru-marketplace.js",))

# ================================================================ Directorios (Biblia §5.6)
# Tres directorios y una ficha por entidad. Las fichas se generan como paginas
# reales —no como parametros de consulta— porque un perfil de asesor o de
# oficina es una URL que se comparte, se indexa y se traduce a los cuatro
# idiomas. Son 33 entidades: 132 paginas, y el buscador de cada directorio
# opera en cliente sobre el mismo JSON que alimenta al resto.

DIR_KINDS = {
 "agents": dict(
   slug="real-estate/agents", one="real-estate/agent",
   eyebrow=ARCH.T("The desk", "La mesa", "المكتب", "团队"),
   title=ARCH.T("Advisers", "Asesores", "المستشارون", "顾问团队"),
   lead=ARCH.T(
     "Every asset under mandate has a named adviser behind it, with the office that holds the mandate, the licence on file and the markets that adviser actually covers. Nothing is routed to an anonymous inbox.",
     "Cada activo bajo mandato tiene detrás un asesor con nombre, la oficina que lleva el mandato, la licencia registrada y las plazas que ese asesor cubre de verdad. Nada se dirige a un buzón anónimo.",
     "خلف كل أصل تحت التفويض مستشار باسمه، والمكتب صاحب التفويض، والترخيص المسجّل، والأسواق التي يغطيها فعلاً. ولا شيء يُوجَّه إلى بريد مجهول.",
     "每一项受托资产背后都有具名顾问、持有委托的分支机构、备案执照，以及该顾问真正覆盖的市场。任何咨询都不会流向匿名信箱。"),
   img="26_corporate_services.jpg"),
 "agencies": dict(
   slug="real-estate/agencies", one="real-estate/agency",
   eyebrow=ARCH.T("The structure", "La estructura", "البنية", "架构"),
   title=ARCH.T("Offices", "Oficinas", "المكاتب", "分支机构"),
   lead=ARCH.T(
     "The offices that hold the mandates, each with its legal entity, its licence and the inventory registered under it. Where an asset sits inside the structure is not a detail — it is what makes the mandate enforceable.",
     "Las oficinas que llevan los mandatos, cada una con su entidad legal, su licencia y el inventario registrado a su nombre. Dónde queda un activo dentro de la estructura no es un detalle: es lo que hace exigible el mandato.",
     "المكاتب التي تحمل التفويضات، لكلٍّ كيانه القانوني وترخيصه والمعروض المسجّل باسمه. وموقع الأصل داخل البنية ليس تفصيلاً: هو ما يجعل التفويض واجب النفاذ.",
     "持有委托的各分支机构，均附其法律主体、执照及名下登记的资产。资产在架构中的归属并非细节——它决定了委托是否具备可执行力。"),
   img="15_difc_gate.jpg"),
 "developers": dict(
   slug="real-estate/developers", one="real-estate/developer",
   eyebrow=ARCH.T("Who builds", "Quién construye", "من يبني", "开发方"),
   title=ARCH.T("Developers", "Promotoras", "المطوّرون", "开发商"),
   lead=ARCH.T(
     "The developers behind the off-plan projects on the platform, with the projects they have registered, the handover they have committed to and the payment plan on offer. Off-plan is a promise; the promiser has a name here.",
     "Las promotoras detrás de los proyectos off-plan de la plataforma, con los proyectos que tienen registrados, la entrega a la que se han comprometido y el plan de pago que ofrecen. El off-plan es una promesa; aquí quien promete tiene nombre.",
     "المطوّرون وراء مشاريع «على المخطط» في المنصة، مع مشاريعهم المسجّلة وموعد التسليم الذي التزموا به وخطة السداد المعروضة. البيع على المخطط وعد؛ وهنا لصاحب الوعد اسم.",
     "平台上期房项目背后的开发商，附其已登记的项目、承诺的交付时间与提供的付款计划。期房是一份承诺——在这里，承诺方有名有姓。"),
   img="24_capital_district.jpg"),
}

def build_directory(lang, kind):
    d = DIR_KINDS[kind]
    RE = ARCH.T("Real Estate", "Inmobiliario", "العقارات", "房地产")
    title = "%s — XARU HOME" % _t(d["title"], lang)
    desc = _t(d["lead"], lang)
    trail = [(RE, "real-estate"), (d["title"], d["slug"])]
    hero = _page_header(lang, _t(d["eyebrow"], lang), _t(d["title"], lang),
                        _crumbs(lang, trail), d["img"])
    body = hero + '''
    <section>
      <div class="cs_height_80 cs_height_lg_50"></div>
      <div class="container"><div class="row"><div class="col-lg-9">
        <p class="xr_pillar_intro" data-aos="fade-up">%s</p>
      </div></div></div>
      <div class="cs_height_45 cs_height_lg_30"></div>
      <div class="container"><div class="xr_dir" data-directory="%s"></div></div>
      <div class="cs_height_130 cs_height_lg_70"></div>
    </section>''' % (_t(d["lead"], lang), kind)
    return _write_shell(lang, d["slug"], title, desc, body,
                        css=("xaru-marketplace.css",), js=("xaru-directory.js",))

DIR_ROLE = {
 "agents":     ARCH.T("Adviser", "Asesor", "\u0645\u0633\u062a\u0634\u0627\u0631", "\u987e\u95ee"),
 "agencies":   ARCH.T("Office", "Oficina", "\u0645\u0643\u062a\u0628", "\u5206\u652f\u673a\u6784"),
 "developers": ARCH.T("Developer", "Promotora", "\u0645\u0637\u0648\u0651\u0631", "\u5f00\u53d1\u5546"),
}

def build_profile(lang, kind, slug, name):
    d = DIR_KINDS[kind]
    RE = ARCH.T("Real Estate", "Inmobiliario", "العقارات", "房地产")
    page_slug = d["one"] + "/" + slug
    role = _t(DIR_ROLE[kind], lang)
    title = "%s — %s | XARU HOME" % (name, role)
    desc = "%s — %s, XARU HOME." % (name, _t(d["title"], lang))
    trail = [(RE, "real-estate"), (d["title"], d["slug"]),
             (ARCH.T(name, name, name, name), page_slug)]
    hero = _page_header(lang, _t(d["eyebrow"], lang), name,
                        _crumbs(lang, trail), d["img"])
    body = hero + '''
    <section>
      <div class="cs_height_80 cs_height_lg_50"></div>
      <div class="container"><div class="xr_pf" data-profile="%s" data-slug="%s"></div></div>
      <div class="cs_height_130 cs_height_lg_70"></div>
    </section>''' % (kind, slug)
    return _write_shell(lang, page_slug, title, desc, body,
                        css=("xaru-marketplace.css",), js=("xaru-directory.js",))

def directory_entities():
    """Entidades publicadas, leidas de la propia API estatica."""
    base = "/home/claude/work/site/xaru/data/api/v1/"
    out = {"agents": [], "agencies": [], "developers": []}
    try:
        with open(base + "agents.json", encoding="utf-8") as f:
            for a in json.load(f)["items"]:
                out["agents"].append((a["slug"], a["name"]))
        with open(base + "agencies.json", encoding="utf-8") as f:
            for o in json.load(f)["items"]:
                k = "developers" if o["kind"] == "developer" else "agencies"
                out[k].append((o["slug"], o["name"]))
    except Exception as e:
        print("directorios: sin API estatica (%s)" % e)
    return out

def build_directories():
    ents = directory_entities()
    n = 0
    for L in ("en", "es", "ar", "zh"):
        for kind in ("agents", "agencies", "developers"):
            build_directory(L, kind)
            n += 1
            for (slug, name) in ents[kind]:
                build_profile(L, kind, slug, name)
                n += 1
    print("directorios y perfiles ->", n, "paginas")
    return ents

# ================================================================ Off-plan (Biblia §5.5)
PRJ_EYEBROW = ARCH.T("Under construction", "En construcción", "قيد الإنشاء", "在建")
PRJ_TITLE = ARCH.T("New projects", "Proyectos nuevos", "المشاريع الجديدة", "新项目")
PRJ_LEAD = ARCH.T(
  "Off-plan is a promise about a building that does not exist yet, so what matters is not the render: it is who has committed, to what date, at what stage the work actually stands, and how the money is staged against it. Every project here declares all four.",
  "El off-plan es una promesa sobre un edificio que aún no existe, así que lo que importa no es el render: es quién se ha comprometido, a qué fecha, en qué punto está la obra de verdad y cómo se escalona el dinero contra ella. Cada proyecto declara aquí las cuatro cosas.",
  "البيع على المخطط وعدٌ بشأن مبنى لم يقم بعد، فالمهم ليس الصورة التخيّلية: بل من التزم، ولأي تاريخ، وأين تقف الأشغال فعلاً، وكيف يُجدوَل المال في مقابلها. وكل مشروع هنا يعلن الأربعة.",
  "期房是关于一栋尚未建成的建筑的承诺，因此关键不在效果图，而在于：谁作出了承诺、承诺哪个日期、工程实际进展到哪一步，以及资金如何与之对应分期。此处每个项目都会申报这四项。")

def build_projects_index(lang):
    RE = ARCH.T("Real Estate", "Inmobiliario", "العقارات", "房地产")
    slug = "real-estate/new-projects"
    title = "%s — XARU HOME" % _t(PRJ_TITLE, lang)
    desc = _t(PRJ_LEAD, lang)
    trail = [(RE, "real-estate"), (PRJ_TITLE, slug)]
    hero = _page_header(lang, _t(PRJ_EYEBROW, lang), _t(PRJ_TITLE, lang),
                        _crumbs(lang, trail), "04_resort_dev.jpg")
    body = hero + '''
    <section>
      <div class="cs_height_80 cs_height_lg_50"></div>
      <div class="container"><div class="row"><div class="col-lg-9">
        <p class="xr_pillar_intro" data-aos="fade-up">%s</p>
      </div></div></div>
      <div class="cs_height_45 cs_height_lg_30"></div>
      <div class="container"><div class="xr_prj" data-projects></div></div>
      <div class="cs_height_130 cs_height_lg_70"></div>
    </section>''' % _t(PRJ_LEAD, lang)
    return _write_shell(lang, slug, title, desc, body,
                        css=("xaru-marketplace.css",), js=("xaru-projects.js",))

PRJ_ROLE = ARCH.T("Off-plan project", "Proyecto off-plan",
                  "\u0645\u0634\u0631\u0648\u0639 \u0639\u0644\u0649 \u0627\u0644\u0645\u062e\u0637\u0637", "\u671f\u623f\u9879\u76ee")

def build_project_page(lang, slug, name):
    RE = ARCH.T("Real Estate", "Inmobiliario", "العقارات", "房地产")
    page_slug = "real-estate/project/" + slug
    title = "%s — %s | XARU HOME" % (name, _t(PRJ_ROLE, lang))
    desc = "%s — %s. XARU HOME." % (name, _t(PRJ_TITLE, lang))
    trail = [(RE, "real-estate"), (PRJ_TITLE, "real-estate/new-projects"),
             (ARCH.T(name, name, name, name), page_slug)]
    hero = _page_header(lang, _t(PRJ_EYEBROW, lang), name,
                        _crumbs(lang, trail), "06_masterplan_ashima.jpg")
    body = hero + '''
    <section>
      <div class="cs_height_80 cs_height_lg_50"></div>
      <div class="container"><div class="xr_prj" data-project data-slug="%s"></div></div>
      <div class="cs_height_130 cs_height_lg_70"></div>
    </section>''' % slug
    return _write_shell(lang, page_slug, title, desc, body,
                        css=("xaru-marketplace.css",), js=("xaru-projects.js",))

def build_projects():
    base = "/home/claude/work/site/xaru/data/api/v1/projects.json"
    items = []
    try:
        with open(base, encoding="utf-8") as f:
            items = [(p["slug"], p["name"]) for p in json.load(f)["items"]]
    except Exception as e:
        print("proyectos: sin API estatica (%s)" % e)
    n = 0
    for L in ("en", "es", "ar", "zh"):
        build_projects_index(L)
        n += 1
        for (slug, name) in items:
            build_project_page(L, slug, name)
            n += 1
    print("proyectos off-plan ->", n, "paginas")

# ================================================================ Paneles (Biblia §5.7–§5.9)
PANELS = {
 "account": dict(
   slug="real-estate/account", mount='<div class="xr_ac" data-account></div>',
   js="xaru-account.js", img="29_private_market.jpg",
   eyebrow=ARCH.T("Your account", "Su cuenta", "حسابك", "您的账户"),
   title=ARCH.T("Saved assets and searches", "Activos y búsquedas guardadas",
                "الأصول وعمليات البحث المحفوظة", "收藏的资产与搜索"),
   lead=ARCH.T(
     "Everything you have kept in one place: saved assets sorted into folders, the searches you run again, the alerts on them, what you looked at recently, and up to four assets side by side. It lives on this device and is not sent anywhere.",
     "Todo lo que ha guardado en un solo lugar: activos ordenados en carpetas, las búsquedas que repite, las alertas sobre ellas, lo que ha mirado recientemente y hasta cuatro activos lado a lado. Vive en este dispositivo y no se envía a ningún sitio.",
     "كل ما احتفظت به في مكان واحد: أصول مرتّبة في مجلدات، وعمليات البحث التي تكرّرها، والتنبيهات عليها، وما شاهدته مؤخراً، وحتى أربعة أصول جنباً إلى جنب. يبقى على هذا الجهاز ولا يُرسل إلى أي جهة.",
     "您保留的一切集中于此：分文件夹整理的收藏资产、反复运行的搜索、其上的提醒、最近浏览的内容，以及最多四项资产的并排对比。全部存于本设备，不发送至任何地方。")),
 "b2b": dict(
   slug="real-estate/office", mount='<div class="xr_cs" data-console="b2b"></div>',
   js="xaru-console.js", img="18_business_district.jpg",
   eyebrow=ARCH.T("Partner console", "Consola del socio", "لوحة الشريك", "合作方控制台"),
   title=ARCH.T("Office operation", "Operación de la oficina",
                "تشغيل المكتب", "分支机构运营"),
   lead=ARCH.T(
     "What an office sees of its own operation: inventory by lifecycle state against the plan quota, the lead pipeline with its response deadlines, credit consumption, and the ten-step listing wizard that validates before anything reaches review.",
     "Lo que una oficina ve de su propia operación: inventario por estado del ciclo de vida contra la cuota del plan, el pipeline de leads con sus plazos de respuesta, el consumo de créditos y el asistente de alta en diez pasos que valida antes de que nada llegue a revisión.",
     "ما يراه المكتب من تشغيله: المعروض حسب حالة دورة الحياة في مقابل حصة الخطة، ومسار العملاء المحتملين بمواعيد الاستجابة، واستهلاك الأرصدة، ومعالج الإدراج بعشر خطوات الذي يتحقّق قبل أن يصل أي شيء إلى المراجعة.",
     "分支机构对自身运营的视图：按生命周期状态统计的资产及套餐配额、附响应时限的线索漏斗、额度消耗，以及在任何内容进入审核前完成校验的十步发布向导。")),
 "admin": dict(
   slug="real-estate/administration", mount='<div class="xr_cs" data-console="admin"></div>',
   js="xaru-console.js", img="21_concrete_lattice.jpg",
   eyebrow=ARCH.T("Platform control", "Control de plataforma",
                  "التحكم بالمنصة", "平台管控"),
   title=ARCH.T("Moderation and lifecycle", "Moderación y ciclo de vida",
                "المراجعة ودورة الحياة", "审核与生命周期"),
   lead=ARCH.T(
     "The moderation queue with the rule each record failed and the deadline it is running against, the distribution of the whole inventory across the seventeen lifecycle states, the transitions as they happen, and the taxonomies underneath. Read-only: deciding requires an authenticated identity and an audit trail.",
     "La cola de moderación con la regla que cada registro incumple y el plazo contra el que corre, la distribución de todo el inventario entre los diecisiete estados del ciclo de vida, las transiciones según ocurren y las taxonomías que hay debajo. Solo lectura: decidir exige identidad autenticada y traza de auditoría.",
     "قائمة المراجعة مع القاعدة التي خالفها كل سجل والمهلة التي يجري في مقابلها، وتوزيع المعروض كله على حالات دورة الحياة السبع عشرة، والانتقالات لحظة وقوعها، والتصنيفات في الأسفل. للقراءة فقط: فالقرار يتطلب هوية موثّقة وأثر تدقيق.",
     "审核队列附每条记录未通过的规则及其所对应的时限、全部资产在十七个生命周期状态间的分布、实时发生的状态迁移，以及底层分类体系。仅供查看：作出决定需经认证的身份与审计轨迹。")),
}

def build_panel(lang, key):
    d = PANELS[key]
    RE = ARCH.T("Real Estate", "Inmobiliario", "العقارات", "房地产")
    title = "%s — XARU HOME" % _t(d["title"], lang)
    desc = _t(d["lead"], lang)
    trail = [(RE, "real-estate"), (d["title"], d["slug"])]
    hero = _page_header(lang, _t(d["eyebrow"], lang), _t(d["title"], lang),
                        _crumbs(lang, trail), d["img"])
    body = hero + '''
    <section>
      <div class="cs_height_80 cs_height_lg_50"></div>
      <div class="container"><div class="row"><div class="col-lg-9">
        <p class="xr_pillar_intro" data-aos="fade-up">%s</p>
      </div></div></div>
      <div class="cs_height_45 cs_height_lg_30"></div>
      <div class="container">%s</div>
      <div class="cs_height_130 cs_height_lg_70"></div>
    </section>''' % (_t(d["lead"], lang), d["mount"])
    return _write_shell(lang, d["slug"], title, desc, body,
                        css=("xaru-marketplace.css",), js=(d["js"],))

def build_panels():
    n = 0
    for L in ("en", "es", "ar", "zh"):
        for key in PANELS:
            build_panel(L, key)
            n += 1
    print("paneles ->", n, "paginas")

def build_catalog_page(lang, catalog_key, slug, trail):
    home = HOME[lang]
    meta = F2.CATALOG[catalog_key]
    title = "%s — XARU HOME" % _t(meta["title"], lang)
    desc = _t(meta["lead"], lang)
    hero = _page_header(lang, _t(meta["eyebrow"], lang), _t(meta["title"], lang),
                        _crumbs(lang, trail), CAT_IMG[catalog_key])
    intro = '''    <section>
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container"><div class="row"><div class="col-lg-9">
        <p class="xr_pillar_intro" data-aos="fade-up">%s</p>
      </div></div></div>
      <div class="cs_height_50 cs_height_lg_30"></div>''' % _t(meta["lead"], lang)
    block = catalog_block(lang, catalog_key, home)
    tail = ""
    if any(is_sold(o) for o in OPPS if o["catalog"] == catalog_key):
        tail = ('\n      <div class="cs_height_40"></div>'
                '\n      <div class="container"><a href="%sreal-estate/sold/" class="xr_link">%s'
                '<i class="fa-solid fa-angle-right"></i></a></div>'
                % (home, _t(F2.SOLD["link_from_catalog"], lang)))
    body = hero + "\n" + intro + "\n" + block + tail + '\n      <div class="cs_height_150 cs_height_lg_80"></div>\n    </section>'
    return _write_shell(lang, slug, title, desc, body)

# ---------------------------------------------------------------- ficha (detail) pages
def _fact(label_t, value, lang):
    if value in (None, "", "None"):
        return ""
    return '<div class="xr_fact"><span class="xr_fact_l">%s</span><span class="xr_fact_v">%s</span></div>' % (
        _t(label_t, lang), value)

def _facts_for(o, lang):
    m = o["model"]
    F = F2.FICHA
    out = [_fact(F["status"] if False else F2.UI["status"], status_badge(lang, o["status"]), lang)]
    out.append(_fact(F["location"], _loc_str(o, lang), lang))
    out.append(_fact(F["price"], _price_str(o, lang), lang))
    if m == "residential":
        s = o.get("specs", {})
        out += [_fact(F["bedrooms"], s.get("bedrooms"), lang),
                _fact(F["bathrooms"], s.get("bathrooms"), lang),
                _fact(F["built"], (_num(s["builtAreaSqm"]) + " m²") if s.get("builtAreaSqm") else "", lang),
                _fact(F["plot"], (_num(s["plotAreaSqm"]) + " m²") if s.get("plotAreaSqm") else "", lang),
                _fact(F["style"], s.get("style"), lang)]
    elif m == "commercial-hospitality":
        op = o.get("operating", {})
        st = _t(OP_STATE.get(op.get("state"), F2.T(op.get("state", ""), "", "", "")), lang)
        out += [_fact(F["operating"], st, lang),
                _fact(F["keys"], op.get("keys"), lang),
                _fact(F["occupancy"], op.get("occupancyTeaser"), lang),
                _fact(F["noi"], op.get("noiTeaser"), lang),
                _fact(F["operator"], op.get("operator"), lang),
                _fact(F["structure"], op.get("structure"), lang),
                _fact(F["ticket"], o.get("ticket", {}).get("band"), lang)]
    elif m == "land-development":
        ld = o.get("land", {})
        cp = " · ".join(_t(F2.COUNTERPARTY.get(c, F2.T(c, c, c, c)), lang) for c in ld.get("counterpartySought", []))
        out += [_fact(F["area"], (_num(ld["areaSqm"]) + " m²") if ld.get("areaSqm") else "", lang),
                _fact(F["tenure"], ld.get("tenure"), lang),
                _fact(F["current_use"], ld.get("currentUse"), lang),
                _fact(F["projected_use"], ld.get("projectedUse"), lang),
                _fact(F["access"], ld.get("access"), lang),
                _fact(F["water"], ld.get("water"), lang),
                _fact(F["environmental"], ld.get("environmental"), lang),
                _fact(F["planning"], ld.get("planning"), lang),
                _fact(F["permits"], ld.get("permits"), lang),
                _fact(F["phase"], ld.get("phase"), lang),
                _fact(F["counterparty"], cp, lang),
                _fact(F["capital_req"], ld.get("capitalRequired"), lang)]
    elif m == "productive-asset":
        # Model 5 — commodities / productive asset. Teaser facts only: region,
        # category, scale, status, opportunity type. Detail lives under NDA.
        pr = o.get("productive", {})
        L = o["location"]
        region = L.get("region") or L.get("country") or ""
        cp = " · ".join(_t(F2.COUNTERPARTY.get(c, F2.T(c, c, c, c)), lang) for c in pr.get("counterpartySought", []))
        out += [_fact(F["region"], region, lang),
                _fact(F["category"], _tv(pr.get("category"), lang), lang),
                _fact(F["scale"], _tv(pr.get("scale"), lang), lang),
                _fact(F["permits"], _tv(pr.get("permitsTeaser"), lang), lang),
                _fact(F2.T("Production", "Producción", "الإنتاج", "产量"), _tv(pr.get("productionTeaser"), lang), lang),
                _fact(F2.T("Offtake / placement", "Offtake / colocación", "الشراء المسبق / التصريف", "承购 / 配售"),
                      _tv(pr.get("offtakeTeaser"), lang), lang),
                _fact(F["counterparty"], cp, lang),
                _fact(F["opp_type"], _tv(pr.get("oppType"), lang), lang)]
    return "\n          ".join(x for x in out if x)

def build_ficha(lang, o):
    home = HOME[lang]
    slug = ficha_url(o)
    m = o["model"]
    title = "%s — XARU HOME" % _t(o["title"], lang)
    cat = o["catalog"]
    cat_label = F2.CATALOG[cat]["title"]
    cat_slug = {"private-properties": "real-estate/private-properties",
                "commercial-hospitality": "real-estate/commercial-hospitality",
                "land-projects": "opportunities"}[cat]
    trail = [(cat_label, cat_slug), (o["title"], slug)]
    hero = _page_header(lang, _t(cat_label, lang), _t(o["title"], lang),
                        _crumbs(lang, trail), _asset(o["images"][0]).split("/")[-1])
    # La ficha muestra la foto a ~700 px: derivada de 1280, no el master de 1920.
    img = gen2_bg(o["images"][0].split("/")[-1], 1280)
    badges = status_badge(lang, o["status"]) + "".join(
        status_badge(lang, s, "xr_badge_sm") for s in o.get("secondaryStatus", []))

    if m == "confidential-teaser":
        te = o["teaser"]
        steps = "".join('<li>%s</li>' % s.replace("-", " ").title() for s in te["dealRoomProcess"])
        facts = "\n          ".join(x for x in [
            _fact(F2.FICHA["region"], _t(F2.T("Undisclosed", "Sin revelar", "غير مُفصَح عنه", "未披露"), lang), lang),
            _fact(F2.FICHA["category"], _t(F2.T("Portfolio", "Portafolio", "محفظة", "资产组合"), lang), lang),
            _fact(F2.FICHA["scale"], _t(F2.T("Significant", "De envergadura", "كبير", "大型"), lang), lang),
            _fact(F2.UI["status"], status_badge(lang, o["status"]), lang),
            _fact(F2.FICHA["opp_type"], _t(F2.T("Private market", "Mercado privado", "السوق الخاص", "私人市场"), lang), lang),
            _fact(F2.UI["verified_mandate"], _t(F2.T("Yes — internal", "Sí — interno", "نعم — داخلي", "是——内部"), lang), lang),
        ] if x)
        overview = '''    <section>
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container"><div class="row cs_gap_y_40">
        <div class="col-lg-7">
          <div class="xr_px_img xr_ficha_img" style="%s"></div>
          %s
        </div>
        <div class="col-lg-5">
          <div class="xr_badge_row mb-3">%s</div>
          <h2 class="cs_fs_38">%s</h2>
          <p class="xr_pillar_lead">%s</p>
          <p class="xr_nda_line"><i class="fa-solid fa-lock"></i> %s</p>
          <div class="xr_facts">
          %s
          </div>
          <div class="cs_height_25"></div>
          <a href="%scapital/deal-room/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a>
        </div>
      </div>
      <div class="cs_height_70 cs_height_lg_40"></div>
      <div class="container">
        <h3 class="cs_fs_25 mb-3">%s</h3>
        <ol class="xr_dealroom">%s</ol>
      </div>
      <div class="cs_height_150 cs_height_lg_80"></div>
    </section>''' % (img, _img_note(lang), badges, _t(o["title"], lang), _t(te["summary"], lang),
                     _t(F2.UI["nda_line"], lang), facts, home, _t(F2.UI["request_access"], lang),
                     _t(F2.UI["deal_room"], lang), steps)
        body = hero + "\n" + overview
    else:
        facts = _facts_for(o, lang)
        cta = '''<a href="%sprivate-enquiry/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a>''' % (home, _t(F2.UI["enquire_priv"], lang))
        # Model 5 (productive-asset) is teaser-only: NDA line + Deal Room CTA
        nda = ""
        if m == "productive-asset":
            nda = '<p class="xr_nda_line"><i class="fa-solid fa-lock"></i> %s</p>' % _t(F2.UI["nda_line"], lang)
            cta = '''<a href="%scapital/deal-room/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a>''' % (home, _t(F2.UI["request_access"], lang))
        # Un activo vendido no se contacta: se ofrece buscar similares y, si
        # procede, asesoria. El aviso deja claro que es una ficha historica y
        # que no se declara precio de cierre.
        if is_sold(o):
            nda = ('<p class="xr_sold_note"><i class="fa-solid fa-circle-info"></i> %s</p>'
                   % _t(F2.SOLD["historic_note"], lang)) + nda
            cta = ('''<a href="%s%s/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a>'''
                   % (home, cat_slug, _t(F2.SOLD["find_similar"], lang))
                   + ''' <a href="%sprivate-enquiry/" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>'''
                   % (home, _t(F2.SOLD["advisory"], lang)))
        body = hero + ('''
    <section>
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container"><div class="row cs_gap_y_40">
        <div class="col-lg-7">
          <div class="xr_px_img xr_ficha_img" style="%s"></div>
          %s
        </div>
        <div class="col-lg-5">
          <div class="xr_badge_row mb-3">%s</div>
          <p class="xr_land_card_meta">%s</p>
          <h2 class="cs_fs_38 mb-2">%s</h2>
          <p class="xr_ficha_price">%s</p>
          ''' + nda + '''
          <div class="cs_height_20"></div>
          <h3 class="cs_fs_20 mb-3">%s</h3>
          <div class="xr_facts">
          %s
          </div>
          <div class="cs_height_25"></div>
          %s
          <a href="%s%s/" class="xr_link" style="margin-left:18px">%s</a>
        </div>
      </div>
      <div class="cs_height_150 cs_height_lg_80"></div>
    </section>''') % (img, _img_note(lang), badges, _loc_str(o, lang), _t(o["title"], lang), _price_str(o, lang),
                      _t(F2.UI["key_facts"], lang), facts, cta, home, cat_slug,
                      _t(F2.UI["back_catalog"], lang))
    return _write_shell(lang, slug, title, _desc(o, lang), body)

# ---------------------------------------------------------------- pillar pages (real copy)
def _pillar_section(lang, slug, num, heading, copy):
    home = HOME[lang]
    body = []
    for p in copy.get("p", []):
        body.append('<p class="xr_pillar_lead">%s</p>' % _t(p, lang))
    if copy.get("list"):
        body.append('<ul class="xr_pillar_list">%s</ul>' %
                     "".join('<li>%s</li>' % _t(x, lang) for x in copy["list"]))
    if copy.get("cols"):
        # explicit two-way blocks (Phase 3 — Side A / Side B)
        colhtml = []
        for c in copy["cols"]:
            items = "".join('<li>%s</li>' % _t(x, lang) for x in c["items"])
            cta = ""
            if c.get("href"):
                cta = ('<div class="cs_height_25"></div>'
                       '<a href="%s%s" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>'
                       % (home, c["href"], _t(c["cta"], lang)))
            colhtml.append('<div class="col-md-6" data-aos="fade-up">'
                           '<div class="xr_cap_item" style="display:flex;flex-direction:column">'
                           '<h3 class="cs_fs_25" style="font-size:24px">%s</h3>'
                           '<ul class="xr_pillar_list" style="flex-grow:1">%s</ul>%s'
                           '</div></div>' % (_t(c["h"], lang), items, cta))
        body.append('<div class="row cs_gap_y_30" style="margin-top:8px">%s</div>' % "".join(colhtml))
    if copy.get("steps"):
        body.append('<ol class="xr_process">%s</ol>' %
                    "".join('<li><span>%02d</span>%s</li>' % (i + 1, _t(x, lang))
                            for i, x in enumerate(copy["steps"])))
    if copy.get("faq"):
        items = "".join('<div class="xr_faq_item"><h4>%s</h4><p>%s</p></div>' % (_t(q, lang), _t(a, lang))
                        for (q, a) in copy["faq"])
        body.append('<div class="xr_faq_block">%s</div>' % items)
    if num == "10":
        body.append('<p class="xr_pillar_note">%s</p>' % _t(ARCH.CAPABILITY_NOTE, lang))
    return '''    <section class="xr_pillar_sec" id="s%s">
      <div class="cs_height_75 cs_height_lg_50"></div>
      <div class="container">
        <div class="cs_section_heading cs_style_1 cs_type_1">
          <div class="cs_section_heading_left">
            <b class="xr_sec_num">%s</b>
            <span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>
            <h2 class="cs_section_title cs_fs_38 mb-0" data-aos="fade-up">%s</h2>
          </div>
        </div>
        <div class="xr_pillar_body">
          %s
        </div>
      </div>
    </section>''' % (num, num, _t(ARCH.DOOR_EYEBROW.get(slug.split("/")[0], heading), lang) if False else _label_for(slug, lang),
                     _t(heading, lang), "\n          ".join(body))

def _label_for(slug, lang):
    for sh in ARCH.SHELLS:
        if sh["slug"] == slug:
            return _t(sh["label"], lang)
    return ""

# ---------------------------------------------------------------- entrada al marketplace
MPH_EYEBROW = ARCH.T("The inventory", "El inventario", "المعروض", "资产库")
MPH_TITLE = ARCH.T("Open the inventory", "Abrir el inventario",
                   "افتح المعروض", "进入资产库")
MPH_LEAD = ARCH.T(
  "Choose the operation, name the market and the search opens with the filter already set. "
  "The address bar carries it, so the result set travels to a client exactly as you saw it.",
  "Elija la operación, nombre la plaza y la búsqueda se abre con el filtro ya puesto. "
  "La barra de direcciones lo lleva, de modo que el resultado viaja a un cliente tal como usted lo vio.",
  "اختر نوع العملية وسمِّ السوق، فتُفتح النتائج والمرشح مضبوط سلفاً. "
  "ويحمله شريط العنوان، فتصل النتيجة إلى العميل كما رأيتها تماماً.",
  "选择交易方式、指定市场，搜索即以设定好的筛选条件打开。条件由地址栏承载，"
  "结果可原样传递给客户。")

def marketplace_entry(lang):
    """Banda de entrada al inventario, encima de la seccion editorial.

    No sustituye nada: el pilar de Real Estate conserva sus once secciones y su
    catalogo. Esto se antepone porque es lo que viene a hacer quien llega
    buscando un activo, y porque sin ello el inventario quedaba a dos clics de
    profundidad dentro del menu.
    """
    return '''    <section class="xr_mph_band">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        <span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>
        <h2 class="cs_section_title cs_fs_38 mb-0" data-aos="fade-up">%s</h2>
        <div class="cs_height_20"></div>
        <div class="row"><div class="col-lg-8">
          <p class="xr_pillar_lead" style="max-width:760px">%s</p>
        </div></div>
        <div class="cs_height_35 cs_height_lg_25"></div>
        <div class="xr_mph" data-mp-home></div>
      </div>
      <div class="cs_height_110 cs_height_lg_70"></div>
    </section>''' % (_t(MPH_EYEBROW, lang), _t(MPH_TITLE, lang), _t(MPH_LEAD, lang))

def build_pillar(lang, slug, embed_catalog=None):
    home = HOME[lang]
    shell = next(s for s in ARCH.SHELLS if s["slug"] == slug)
    copy = F2.PILLARS[slug]
    title = "%s — XARU HOME" % _t(shell["label"], lang)
    intro_t = copy.get("intro", shell["intro"])
    intro_sub_t = copy.get("intro_sub", shell["intro_sub"])
    desc = "%s %s" % (_t(intro_t, lang), _t(intro_sub_t, lang))
    intro = '''    <section>
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container"><div class="row"><div class="col-lg-9">
        <p class="xr_pillar_intro" data-aos="fade-up">%s</p>
        <p class="xr_pillar_lead" style="max-width:760px">%s</p>
      </div></div></div>
    </section>''' % (_t(intro_t, lang), _t(intro_sub_t, lang))
    body = _shell_hero(lang, shell) + "\n" + intro
    if slug == "real-estate":
        body += "\n" + marketplace_entry(lang)
    # §5: banda de video propia de la pagina pilar, detras de la introduccion.
    # _write_shell la retirara y recolocara si hiciera falta (idempotente).
    # banda retirada de los pilares (rompia el diseno); ver docs
    # sections 01..11 with real copy; 12 = generic CTA
    for (num, heading) in ARCH.PILLAR_SECTIONS:
        if num == "12":
            body += "\n" + _pillar_cta(lang, heading)
            continue
        c = copy.get(num, {})
        body += "\n" + _pillar_section(lang, slug, num, heading, c)
        if embed_catalog and num == "03":
            body += '''
    <section class="cs_gray2_bg">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container"><span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>
      <h2 class="cs_section_title cs_fs_38 mb-0" data-aos="fade-up">%s</h2></div>
      <div class="cs_height_40 cs_height_lg_30"></div>
%s
      <div class="cs_height_120 cs_height_lg_75"></div>
    </section>''' % (_t(F2.CATALOG[embed_catalog]["eyebrow"], lang),
                     _t(F2.UI["explore_assets"], lang),
                     catalog_block(lang, embed_catalog, home, block_id="pcat_" + _slug2(embed_catalog)))
    css = ("xaru-marketplace.css",) if slug == "real-estate" else ()
    js = ("xaru-mp-home.js",) if slug == "real-estate" else ()
    return _write_shell(lang, slug, title, desc, body, css=css, js=js)

def _pillar_cta(lang, heading):
    home = HOME[lang]
    return '''    <section class="xr_pillar_sec" id="s12">
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container">
        <div class="cs_cta cs_style_1 text-center" style="border:1px solid var(--border-color);border-radius:16px;padding:56px 24px;background:rgba(250,248,242,.6)">
          <b class="xr_sec_num">12</b>
          <h2 class="cs_section_title cs_fs_38" data-aos="fade-up">%s</h2>
          <div class="d-flex gap-3 flex-wrap justify-content-center">
            <a href="%sprivate-enquiry/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a>
            <a href="%sopportunities/submit/" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>
          </div>
        </div>
      </div>
      <div class="cs_height_120 cs_height_lg_75"></div>
    </section>''' % (_t(heading, lang), home, _t(ARCH.BTN_ENQUIRY, lang), home, _t(ARCH.BTN_SUBMIT, lang))

# ---------------------------------------------------------------- homepage 12-block injector
HERO_PAIRS = {
 "es": [
   ("The operational home <br /> for assets, projects, capital <br /> and international expansion.",
    "El hogar operativo <br /> de activos, proyectos, capital <br /> y expansi\u00f3n internacional."),
   ("Real estate is the starting point. XARU HOME connects properties, developments, capital and international expansion under one structure.",
    "Real estate es el punto de partida. XARU HOME conecta propiedades, desarrollos, capital y expansi\u00f3n internacional bajo una sola estructura."),
   ("Land, Coastline <br />and Projects of Scale.",
    "Suelo, costa <br />y proyectos de escala."),
   ("Territory, developments, capital and international expansion &mdash; under one operational home.",
    "Territorio, desarrollos, capital y expansi\u00f3n internacional &mdash; bajo un solo hogar operativo."),
   ("REAL ESTATE | PROJECTS | CAPITAL | EXPANSION",
    "REAL ESTATE | PROYECTOS | CAPITAL | EXPANSI\u00d3N"),
   ("Explore Opportunities", "Explorar oportunidades"),
   ("Present an Asset or Project", "Presentar un activo o proyecto"),
   ("Explore Developments", "Explorar desarrollos"),
 ],
 "ar": [
   ("The operational home <br /> for assets, projects, capital <br /> and international expansion.",
    "\u0627\u0644\u0645\u0642\u0631\u0651 \u0627\u0644\u062a\u0634\u063a\u064a\u0644\u064a <br /> \u0644\u0644\u0623\u0635\u0648\u0644 \u0648\u0627\u0644\u0645\u0634\u0627\u0631\u064a\u0639 \u0648\u0631\u0623\u0633 \u0627\u0644\u0645\u0627\u0644 <br /> \u0648\u0627\u0644\u062a\u0648\u0633\u0651\u0639 \u0627\u0644\u062f\u0648\u0644\u064a."),
   ("Real estate is the starting point. XARU HOME connects properties, developments, capital and international expansion under one structure.",
    "\u0627\u0644\u0639\u0642\u0627\u0631\u0627\u062a \u0647\u064a \u0646\u0642\u0637\u0629 \u0627\u0644\u0627\u0646\u0637\u0644\u0627\u0642. \u062a\u0631\u0628\u0637 XARU HOME \u0627\u0644\u0639\u0642\u0627\u0631\u0627\u062a \u0648\u0627\u0644\u062a\u0637\u0648\u064a\u0631\u0627\u062a \u0648\u0631\u0623\u0633 \u0627\u0644\u0645\u0627\u0644 \u0648\u0627\u0644\u062a\u0648\u0633\u0651\u0639 \u0627\u0644\u062f\u0648\u0644\u064a \u0636\u0645\u0646 \u0628\u0646\u064a\u0629 \u0648\u0627\u062d\u062f\u0629."),
   ("Land, Coastline <br />and Projects of Scale.",
    "\u0623\u0631\u0627\u0636\u064d \u0648\u0633\u0648\u0627\u062d\u0644 <br />\u0648\u0645\u0634\u0627\u0631\u064a\u0639 \u0628\u062d\u062c\u0645\u064d \u0643\u0628\u064a\u0631."),
   ("Territory, developments, capital and international expansion &mdash; under one operational home.",
    "\u0623\u0631\u0627\u0636\u064d \u0648\u062a\u0637\u0648\u064a\u0631\u0627\u062a \u0648\u0631\u0623\u0633 \u0645\u0627\u0644 \u0648\u062a\u0648\u0633\u0651\u0639 \u062f\u0648\u0644\u064a &mdash; \u0636\u0645\u0646 \u0645\u0642\u0631\u0651 \u062a\u0634\u063a\u064a\u0644\u064a \u0648\u0627\u062d\u062f."),
   ("REAL ESTATE | PROJECTS | CAPITAL | EXPANSION",
    "\u0627\u0644\u0639\u0642\u0627\u0631\u0627\u062a | \u0627\u0644\u0645\u0634\u0627\u0631\u064a\u0639 | \u0631\u0623\u0633 \u0627\u0644\u0645\u0627\u0644 | \u0627\u0644\u062a\u0648\u0633\u0651\u0639"),
   ("Explore Opportunities", "\u0627\u0633\u062a\u0643\u0634\u0641 \u0627\u0644\u0641\u0631\u0635"),
   ("Present an Asset or Project", "\u0642\u062f\u0651\u0645 \u0623\u0635\u0644\u0627\u064b \u0623\u0648 \u0645\u0634\u0631\u0648\u0639\u0627\u064b"),
   ("Explore Developments", "\u0627\u0633\u062a\u0643\u0634\u0641 \u0627\u0644\u062a\u0637\u0648\u064a\u0631\u0627\u062a"),
 ],
 "zh": [
   ("The operational home <br /> for assets, projects, capital <br /> and international expansion.",
    "\u8d44\u4ea7\u3001\u9879\u76ee\u3001\u8d44\u672c <br /> \u4e0e\u56fd\u9645\u62d3\u5c55\u7684 <br /> \u8fd0\u8425\u4e2d\u67a2\u3002"),
   ("Real estate is the starting point. XARU HOME connects properties, developments, capital and international expansion under one structure.",
    "\u623f\u5730\u4ea7\u662f\u8d77\u70b9\u3002XARU HOME \u5c06\u7269\u4e1a\u3001\u5f00\u53d1\u9879\u76ee\u3001\u8d44\u672c\u4e0e\u56fd\u9645\u62d3\u5c55\u7eb3\u5165\u540c\u4e00\u67b6\u6784\u3002"),
   ("Land, Coastline <br />and Projects of Scale.",
    "\u571f\u5730\u3001\u6d77\u5cb8\u7ebf <br />\u4e0e\u5927\u89c4\u6a21\u9879\u76ee\u3002"),
   ("Territory, developments, capital and international expansion &mdash; under one operational home.",
    "\u571f\u5730\u3001\u5f00\u53d1\u3001\u8d44\u672c\u4e0e\u56fd\u9645\u62d3\u5c55 &mdash; \u5f52\u4e8e\u540c\u4e00\u4e2a\u8fd0\u8425\u4e2d\u67a2\u3002"),
   ("REAL ESTATE | PROJECTS | CAPITAL | EXPANSION",
    "\u623f\u5730\u4ea7 | \u9879\u76ee | \u8d44\u672c | \u62d3\u5c55"),
   ("Explore Opportunities", "\u63a2\u7d22\u673a\u4f1a"),
   ("Present an Asset or Project", "\u63d0\u4ea4\u8d44\u4ea7\u6216\u9879\u76ee"),
   ("Explore Developments", "\u63a2\u7d22\u5f00\u53d1\u9879\u76ee"),
 ],
}

def _home_head(num, eyebrow, title, fs="cs_fs_49"):
    return '''<div class="cs_section_heading cs_style_1 cs_type_1">
          <div class="cs_section_heading_left">
            <b class="xr_sec_num">%s</b>
            <span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>
            <h2 class="cs_section_title %s mb-0" data-aos="fade-up">%s</h2>
          </div>
        </div>''' % (num, eyebrow, fs, title)

def _tab_filter(name):
    if name == "private":
        return [o for o in OPPS if o["catalog"] == "private-properties"]
    if name == "commercial":
        return [o for o in OPPS if o["catalog"] == "commercial-hospitality"]
    if name == "land":
        return [o for o in OPPS if o["catalog"] == "land-projects" and o["model"] == "land-development"]
    if name == "projects":
        return [o for o in OPPS if ("ASHIMA" in o.get("tags", [])) or
                (o["catalog"] == "commercial-hospitality" and
                 o["status"] in ("halted-restructuring", "seeking-operator", "under-construction"))]
    if name == "private-market":
        return [o for o in OPPS if o["model"] == "confidential-teaser"]
    return []

def home_blocks(lang):
    home = HOME[lang]
    H = F2.HOME
    # Block 2 — journey selector
    jitems = "".join(
        '<a class="xr_journey_card" href="%s%s"><span class="xr_journey_i"><i class="fa-solid fa-angle-right"></i></span><span>%s</span></a>'
        % (home, route, _t(lbl, lang)) for (lbl, route) in H["journey"])
    b2 = '''    <!-- XR Block 02 Journey -->
    <section id="journey" class="xr_block">
      <div class="cs_height_150 cs_height_lg_80"></div>
      <div class="container">
        %s
        <div class="cs_height_50 cs_height_lg_30"></div>
        <div class="xr_journey_grid">%s</div>
      </div>
      <div class="cs_height_150 cs_height_lg_80"></div>
    </section>''' % (_home_head("02", _t(H["journey_eyebrow"], lang), _t(H["journey_title"], lang)), jitems)

    # Block 3 — three markets
    def _mcard(t, b, route, img, vid):
        vhtml = ""
        if vid:
            vhtml = ('''<video class="xr_card_video" muted loop playsinline preload="none"
                    poster="/assets/img/xaru/video-posters/%s.jpg" aria-hidden="true" data-xr-lazyvideo="1">
                    <source data-src="/assets/video/%s.webm" type="video/webm" />
                    <source data-src="/assets/video/%s.mp4" type="video/mp4" />
                  </video>''' % (vid, vid, vid))
        return ('''<div class="col-lg-4" data-aos="fade-up"><a class="xr_market_card" href="%s%s">
          <div class="xr_px_img" style="%s">%s</div>
          <div class="xr_market_body"><h3>%s</h3><p>%s</p>
          <span class="xr_link">%s<i class="fa-solid fa-angle-right"></i></span></div></a></div>'''
          % (home, route, gen2_bg(img, 1280), vhtml, _t(t, lang), _t(b, lang), _t(F2.UI["view_division"], lang)))
    MARKET_VIDEO = ["xaru-coastal-residence-aerial", "xaru-hospitality-resort-beachfront", "xaru-land-development-coastal"]
    mcards = "".join(_mcard(t, b, route, img, MARKET_VIDEO[i] if i < len(MARKET_VIDEO) else None)
                     for i, (t, b, route, img) in enumerate(H["markets"]))
    b3 = '''    <!-- XR Block 03 Markets -->
    <section id="markets" class="xr_block cs_gray2_bg">
      <div class="cs_height_150 cs_height_lg_80"></div>
      <div class="container">
        %s
        <div class="cs_height_60 cs_height_lg_40"></div>
        <div class="row cs_gap_y_30">%s</div>
      </div>
      <div class="cs_height_150 cs_height_lg_80"></div>
    </section>''' % (_home_head("03", _t(H["markets_eyebrow"], lang), _t(H["markets_title"], lang)), mcards)

    # Block 4 — featured opportunities tabs
    tabbtns, tabpanes = [], []
    for i, (key, lbl) in enumerate(H["tabs"]):
        act = " is-active" if i == 0 else ""
        tabbtns.append('<button type="button" class="xr_tab_btn%s" data-tab="%s">%s</button>' % (act, key, _t(lbl, lang)))
        # Biblia §1.2: los vendidos no son inventario destacado. Si al retirarlos
        # una pestana se queda sin nada, se dice, no se rellena.
        pool = [o for o in _tab_filter(key) if not is_sold(o)]
        if pool:
            cards = "\n        ".join(opp_card(lang, o, home) for o in pool)
        else:
            cards = ('<div class="col-12"><div class="xr_empty_state">'
                     '<p>%s</p>'
                     '<a href="%sproperty-listing-search.html" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a> '
                     '<a href="%sreal-estate/sold/" class="xr_link">%s<i class="fa-solid fa-angle-right"></i></a>'
                     '</div></div>'
                     % (_t(F2.SOLD["empty_private"], lang), home,
                        _t(F2.UI["view_all"], lang) if "view_all" in F2.UI else _t(F2.SOLD["find_similar"], lang),
                        home, _t(F2.SOLD["link_from_catalog"], lang)))
        tabpanes.append('<div class="xr_tab_pane%s" data-pane="%s"><div class="row cs_gap_y_30">%s</div></div>' % (act, key, cards))
    b4 = '''    <!-- XR Block 04 Featured -->
    <section id="featured" class="xr_block">
      <div class="cs_height_150 cs_height_lg_80"></div>
      <div class="container">
        %s
        <div class="cs_height_40 cs_height_lg_30"></div>
        <div class="xr_tabs">%s</div>
        <div class="cs_height_40 cs_height_lg_30"></div>
        %s
        <div class="cs_height_40"></div>
        <a href="%sopportunities/" class="xr_link">%s<i class="fa-solid fa-angle-right"></i></a>
      </div>
      <div class="cs_height_150 cs_height_lg_80"></div>
    </section>
    <script>
    (function(){var s=document.getElementById("featured");if(!s)return;
      var bs=s.querySelectorAll(".xr_tab_btn"),ps=s.querySelectorAll(".xr_tab_pane");
      bs.forEach(function(b){b.addEventListener("click",function(){
        var t=b.getAttribute("data-tab");
        bs.forEach(function(x){x.classList.remove("is-active");});b.classList.add("is-active");
        ps.forEach(function(p){p.classList.toggle("is-active",p.getAttribute("data-pane")===t);});});});
    })();
    </script>''' % (_home_head("04", _t(H["featured_eyebrow"], lang), _t(H["featured_title"], lang)),
                    "".join(tabbtns), "\n        ".join(tabpanes), home, _t(F2.UI["view_catalog"], lang))

    # Block 5 — capability strip
    caps = "".join('<div class="col-lg-4 col-md-6" data-aos="fade-up"><div class="xr_cap_item"><h3>%s</h3><p>%s</p></div></div>'
                   % (_t(t, lang), _t(d, lang)) for (t, d) in H["capability"])
    b5 = '''    <!-- XR Block 05 Capability -->
    <section id="capability" class="xr_block xr_dark_section">
      <div class="cs_height_150 cs_height_lg_80"></div>
      <div class="container">
        %s
        <div class="cs_height_60 cs_height_lg_40"></div>
        <div class="row cs_gap_y_30">%s</div>
      </div>
      <div class="cs_height_150 cs_height_lg_80"></div>
    </section>''' % (_home_head("05", _t(H["cap_eyebrow"], lang), _t(H["cap_title"], lang)), caps)

    # Block 6 — projects & capital dual
    b6 = '''    <!-- XR Block 06 Dual -->
    <section id="dual" class="xr_block">
      <div class="cs_height_150 cs_height_lg_80"></div>
      <div class="container">
        %s
        <div class="cs_height_40 cs_height_lg_30"></div>
        <p class="xr_pillar_intro" style="max-width:820px">%s</p>
        <div class="cs_height_30"></div>
        <div class="d-flex gap-3 flex-wrap">
          <a href="%s%s" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a>
          <a href="%s%s" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>
        </div>
      </div>
      <div class="cs_height_150 cs_height_lg_80"></div>
    </section>''' % (_home_head("06", _t(H["dual_eyebrow"], lang), _t(H["dual_title"], lang)),
                     _t(H["dual_lead"], lang), home, H["dual_a"][1], _t(H["dual_a"][0], lang),
                     home, H["dual_b"][1], _t(H["dual_b"][0], lang))

    # ASHIMA facets strip (block 7 support)
    afac = "".join('<div class="col-lg-3 col-md-6" data-aos="fade-up"><div class="xr_ashima_facet"><h4>%s</h4><p>%s</p></div></div>'
                   % (_t(t, lang), _t(d, lang)) for (t, d) in H["ashima_facets"])
    b7 = '''    <!-- XR Block 07 ASHIMA facets -->
    <section class="xr_block cs_gray2_bg">
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container">
        <span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>
        <h2 class="cs_section_title cs_fs_38 mb-0" data-aos="fade-up">%s</h2>
        <div class="cs_height_50 cs_height_lg_30"></div>
        <div class="row cs_gap_y_30">%s</div>
      </div>
      <div class="cs_height_120 cs_height_lg_75"></div>
    </section>''' % (_t(H["ashima_eyebrow"], lang), _t(H["ashima_title"], lang), afac)

    # Block 8 — infrastructure cards
    icards = "".join('<div class="col-lg-3 col-md-6" data-aos="fade-up"><a class="xr_infra_card" href="%s%s"><h3>%s</h3><p>%s</p><span class="xr_link">%s<i class="fa-solid fa-angle-right"></i></span></a></div>'
                     % (home, route, _t(t, lang), _t(d, lang), _t(F2.UI["view_division"], lang))
                     for (t, d, route) in H["infra"])
    b8 = '''    <!-- XR Block 08 Infra -->
    <section id="infra" class="xr_block">
      <div class="cs_height_150 cs_height_lg_80"></div>
      <div class="container">
        %s
        <div class="cs_height_60 cs_height_lg_40"></div>
        <div class="row cs_gap_y_30">%s</div>
      </div>
      <div class="cs_height_150 cs_height_lg_80"></div>
    </section>''' % (_home_head("08", _t(H["infra_eyebrow"], lang), _t(H["infra_title"], lang)), icards)

    # Block 9 — presence
    pitems = "".join('<div class="col-lg-3 col-md-6" data-aos="fade-up"><div class="xr_presence_item"><h4>%s</h4><p>%s</p></div></div>'
                     % (_t(t, lang), _t(d, lang)) for (t, d) in H["presence_items"])
    b9 = '''    <!-- XR Block 09 Presence -->
    <section id="presence" class="xr_block cs_gray2_bg">
      <div class="cs_height_150 cs_height_lg_80"></div>
      <div class="container">
        %s
        <div class="cs_height_30"></div>
        <p class="xr_pillar_intro" style="max-width:860px">%s</p>
        <p class="xr_phase0">%s %s</p>
        <div class="cs_height_40 cs_height_lg_30"></div>
        <div class="row cs_gap_y_30">%s</div>
        <div class="cs_height_40 cs_height_lg_30"></div>
        <a href="%scompany/" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>
      </div>
      <div class="cs_height_150 cs_height_lg_80"></div>
    </section>''' % (_home_head("09", _t(H["presence_eyebrow"], lang), _t(H["presence_title"], lang)),
                     _t(H["presence_lead"], lang), _t(F2.PHASE0, lang),
                     _t(F2.T("Office cities, entity details, team size and network figures are published once verified.",
                             "Ciudades de oficinas, detalles de entidades, tamaño del equipo y cifras de red se publican una vez verificados.",
                             "مدن المكاتب وتفاصيل الكيانات وحجم الفريق وأرقام الشبكة تُنشر بعد التحقق.",
                             "办公城市、实体细节、团队规模与网络数字经核实后公布。"), lang), pitems,
                     home,
                     _t(F2.T("The Company — offices, entities, team & network",
                             "La Compañía — oficinas, entidades, equipo y red",
                             "الشركة — المكاتب والكيانات والفريق والشبكة",
                             "公司——办公网络、实体、团队与网络"), lang))

    # Block 10 — governance
    gitems = "".join('<li>%s</li>' % _t(x, lang) for x in H["gov_items"])
    b10 = '''    <!-- XR Block 10 Governance -->
    <section id="governance" class="xr_block">
      <div class="cs_height_150 cs_height_lg_80"></div>
      <div class="container">
        %s
        <div class="cs_height_40 cs_height_lg_30"></div>
        <div class="row"><div class="col-lg-6"><ul class="xr_pillar_list">%s</ul></div>
        <div class="col-lg-6"><p class="xr_pillar_note">%s</p></div></div>
        <div class="cs_height_40 cs_height_lg_30"></div>
        <div class="d-flex gap-3 flex-wrap">
          <a href="%scompany/#governance" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>
          <a href="%scompany/#entities" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>
        </div>
      </div>
      <div class="cs_height_150 cs_height_lg_80"></div>
    </section>''' % (_home_head("10", _t(H["gov_eyebrow"], lang), _t(H["gov_title"], lang)),
                     gitems, _t(ARCH.CAPABILITY_NOTE, lang),
                     home, _t(F4.BI_DOOR["gov_link1"], lang),
                     home, _t(F4.BI_DOOR["gov_link2"], lang))

    # Block 11 — insights
    sectors = ARCH.NAV[5]["cols"][0]["items"]
    chips = "".join('<a class="xr_insight_chip" href="%sinsights/">%s</a>' % (home, _t(s, lang)) for s in sectors)
    b11 = '''    <!-- XR Block 11 Insights -->
    <section id="insights-home" class="xr_block cs_gray2_bg">
      <div class="cs_height_150 cs_height_lg_80"></div>
      <div class="container">
        %s
        <div class="cs_height_40 cs_height_lg_30"></div>
        <div class="xr_insight_chips">%s</div>
      </div>
      <div class="cs_height_150 cs_height_lg_80"></div>
    </section>''' % (_home_head("11", _t(H["ins_eyebrow"], lang), _t(H["ins_title"], lang)), chips)

    # Block 12 — private desk
    b12 = '''    <!-- XR Block 12 Private Desk -->
    <section id="private-desk" class="xr_block xr_dark_section text-center">
      <div class="cs_height_150 cs_height_lg_80"></div>
      <div class="container">
        <b class="xr_sec_num" style="color:var(--accent-color)">12</b>
        <span class="xr_eyebrow_serif" style="color:#fff">%s</span>
        <h2 class="cs_section_title cs_fs_49" style="color:#fff;max-width:820px;margin:12px auto 28px" data-aos="fade-up">%s</h2>
        <a href="%sprivate-enquiry/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a>
      </div>
      <div class="cs_height_150 cs_height_lg_80"></div>
    </section>''' % (_t(H["desk_eyebrow"], lang), _t(H["desk_title"], lang), home, _t(H["desk_cta"], lang))

    # §5: quinto video de portada — Projects, Capital & Expansion.
    # Va detras del bloque de mercados, como banda editorial a todo ancho.
    return {"after_hero": b2 + "\n" + b3 + "\n"
                          + video_band("xaru-capital-london-construction") + "\n"
                          + b4 + "\n" + b5 + "\n" + b6,
            "after_projects": b7 + "\n" + b8 + "\n" + b9 + "\n" + b10 + "\n" + b11,
            "before_about": b12}

def _rm_section(h, start, end):
    return re.sub(re.escape(start) + r".*?" + re.escape(end), "", h, flags=re.S)

def inject_home(lang):
    path = "/home/claude/work/site/xaru/index.html" if lang == "en" \
        else "/home/claude/work/site/xaru/%s/index.html" % lang
    with open(path, encoding="utf-8") as f:
        h = f.read()
    if "XR Block 02 Journey" in h:  # idempotent: strip prior injection
        h = re.sub(r'\s*<!-- XR Block \d+.*?</section>', '', h, flags=re.S)
    # remove superseded sections
    for (s, e) in [
        ("<!-- Start Land & Large-Scale Developments Section -->", "<!-- End Land & Large-Scale Developments Section -->"),
        ("<!-- Start Properties Section -->", "<!-- End Properties Section -->"),
        ("<!-- Start Investment & Funds Section -->", "<!-- End Investment & Funds Section -->"),
        ("<!-- Start Developers Section -->", "<!-- End Developers Section -->"),
        ("<!-- Start Relocation Section -->", "<!-- End Relocation Section -->"),
    ]:
        h = _rm_section(h, s, e)
    # strip section numbers from kept support sections
    h = h.replace('<b class="xr_sec_num">07</b>', '')       # digital-assets
    h = h.replace('<b class="xr_sec_num">08</b>', '')       # about
    h = h.replace('<b class="xr_sec_num" style="color:#fff">09</b>', '')  # contact
    h = h.replace('<b class="xr_sec_num">06</b>', '<b class="xr_sec_num">07</b>')  # projects -> 07
    blocks = home_blocks(lang)
    h = strip_video_bands(h)                # idempotencia en la portada
    h = h.replace("<!-- End Hero Section -->",
                  "<!-- End Hero Section -->\n" + blocks["after_hero"], 1)
    h = h.replace("<!-- End Projects Section -->",
                  "<!-- End Projects Section -->\n" + blocks["after_projects"], 1)
    h = h.replace("<!-- Start About Section -->",
                  blocks["before_about"] + "\n    <!-- Start About Section -->", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(h)
    print("home-inject", lang, "->", path, len(h))

def build_catalogs_fichas_pillars():
    RE = ARCH.T("Real Estate", "Inmobiliario", "العقارات", "房地产")
    OPPL = F2.CATALOG["land-projects"]["title"]
    for L in ("en", "es", "ar", "zh"):
        # catalogs (standalone)
        build_catalog_page(L, "private-properties", "real-estate/private-properties",
                           [(RE, "real-estate"), (F2.CATALOG["private-properties"]["title"], "real-estate/private-properties")])
        build_catalog_page(L, "land-projects", "opportunities",
                           [(OPPL, "opportunities")])
        build_sold_page(L)
        # marketplace routes (Biblia §5.1)
        for _r in MARKET_ROUTES:
            build_marketplace(L, _r)
        # pillars (override generic shells; commercial & land embed their catalog)
        build_pillar(L, "real-estate", embed_catalog="private-properties")
        build_pillar(L, "real-estate/commercial-hospitality", embed_catalog="commercial-hospitality")
        build_pillar(L, "developments/land-master-developments", embed_catalog="land-projects")
        # fichas (all opportunities)
        for o in OPPS:
            build_ficha(L, o)
    print("catalogs/fichas/pillars done")

# ================================================================ Phase 5 — Company + Insights
def _sec_head(lang, eyebrow_t, title_t, num=None):
    n = '<b class="xr_sec_num">%s</b>' % num if num else ""
    return ('<div class="cs_section_heading cs_style_1 cs_type_1">'
            '<div class="cs_section_heading_left">%s'
            '<span class="xr_eyebrow_serif" data-aos="fade-up">%s</span>'
            '<h2 class="cs_section_title cs_fs_38 mb-0" data-aos="fade-up">%s</h2>'
            '</div></div>' % (n, _t(eyebrow_t, lang), _t(title_t, lang)))

def build_company(lang):
    C = F5C.COMPANY
    home = HOME[lang]
    shell = next(s for s in ARCH.SHELLS if s["slug"] == "company")
    ph0 = _t(F2.PHASE0, lang)

    # -- who we are: three levels + guiding phrase
    lvl = "".join(
        '<div class="col-lg-4" data-aos="fade-up"><div class="xr_cap_item">'
        '<b class="xr_sec_num">0%d</b><h3 class="cs_fs_25" style="font-size:24px">%s</h3>'
        '<p style="color:var(--secondary-color);margin:0">%s</p></div></div>'
        % (i + 1, _t(h, lang), _t(p, lang)) for i, (h, p) in enumerate(C["who_levels"]))

    # -- corporate values (5)
    vals = "".join(
        '<div class="col-lg col-md-4 col-sm-6" data-aos="fade-up"><div class="xr_presence_item">'
        '<h4>%s</h4><p>%s</p></div></div>'
        % (_t(h, lang), _t(p, lang)) for (h, p) in C["values"])

    # -- operating model: 7 division links
    divs = "".join(
        '<a class="xr_journey_card" href="%s%s"><span class="xr_journey_i">'
        '<i class="fa-solid fa-angle-right"></i></span><span>%s</span></a>'
        % (home, route, _t(lbl, lang)) for (route, lbl) in C["divisions"])

    # -- team areas (7)
    team = "".join(
        '<div class="col-lg-3 col-md-6" data-aos="fade-up"><div class="xr_presence_item">'
        '<h4>%s</h4><p>%s</p></div></div>'
        % (_t(h, lang), _t(p, lang)) for (h, p) in C["team_areas"])

    # -- governance list, split 4/3
    gv = C["gov_items"]
    gov_a = "".join('<li>%s</li>' % _t(x, lang) for x in gv[:4])
    gov_b = "".join('<li>%s</li>' % _t(x, lang) for x in gv[4:])

    # -- network chips
    chips = "".join('<span class="xr_insight_chip">%s</span>' % _t(r, lang)
                    for r in C["net_regions"])

    body = _shell_hero(lang, shell) + '''
    <section>
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container"><div class="row"><div class="col-lg-9">
        <p class="xr_pillar_intro" data-aos="fade-up">%s</p>
        <p class="xr_pillar_lead" style="max-width:760px">%s</p>
      </div></div></div>
    </section>
    <section class="xr_pillar_sec" id="who-we-are">
      <div class="cs_height_75 cs_height_lg_50"></div>
      <div class="container">
        %s
        <div class="cs_height_20"></div>
        <p class="xr_pillar_lead" style="max-width:720px">%s</p>
        <div class="cs_height_30"></div>
        <div class="row cs_gap_y_30">%s</div>
        <div class="cs_height_40 cs_height_lg_30"></div>
        <p class="xr_pillar_intro" style="max-width:760px" data-aos="fade-up">%s</p>
      </div>
    </section>
    <section class="xr_pillar_sec cs_gray2_bg" id="values">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        %s
        <div class="cs_height_40 cs_height_lg_30"></div>
        <div class="row cs_gap_y_30">%s</div>
        <div class="cs_height_30"></div>
        <p class="xr_pillar_note" style="max-width:860px">%s</p>
      </div>
      <div class="cs_height_90 cs_height_lg_60"></div>
    </section>
    <section class="xr_pillar_sec" id="operating-model">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        %s
        <div class="cs_height_20"></div>
        <p class="xr_pillar_lead" style="max-width:820px">%s</p>
        <div class="cs_height_30"></div>
        <div class="xr_journey_grid">%s</div>
      </div>
      <div class="cs_height_90 cs_height_lg_60"></div>
    </section>
    <section class="xr_pillar_sec cs_gray2_bg" id="offices">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        %s
        <div class="cs_height_30"></div>
        <div class="row cs_gap_y_30">
          <div class="col-lg-6" data-aos="fade-up"><div class="xr_cap_item">
            <span class="xr_status_badge is-live">%s</span>
            <h3 class="cs_fs_25" style="font-size:24px;margin-top:14px">%s</h3>
            <p style="color:var(--secondary-color);margin:0">%s</p>
          </div></div>
          <div class="col-lg-6" data-aos="fade-up"><div class="xr_cap_item">
            <span class="xr_phase0">%s</span>
            <h3 class="cs_fs_25" style="font-size:24px;margin-top:14px">%s</h3>
            <p style="color:var(--secondary-color);margin:0">%s</p>
          </div></div>
        </div>
      </div>
      <div class="cs_height_90 cs_height_lg_60"></div>
    </section>
    <section class="xr_pillar_sec" id="team">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        %s
        <div class="cs_height_20"></div>
        <p class="xr_pillar_lead" style="max-width:760px">%s</p>
        <div class="cs_height_30"></div>
        <div class="row cs_gap_y_30">%s</div>
        <div class="cs_height_25"></div>
        <p class="xr_phase0">%s %s</p>
      </div>
      <div class="cs_height_90 cs_height_lg_60"></div>
    </section>
    <section class="xr_pillar_sec xr_dark_section" id="entities">
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container">
        <span class="xr_eyebrow_serif" style="color:#fff">%s</span>
        <h2 class="cs_section_title cs_fs_38" style="color:#fff" data-aos="fade-up">%s</h2>
        <div class="cs_height_20"></div>
        <p class="xr_pillar_intro" style="color:#F5F1E8;max-width:860px" data-aos="fade-up">%s</p>
        <p class="xr_pillar_lead" style="color:rgba(245,241,232,.75);max-width:760px">%s</p>
      </div>
      <div class="cs_height_120 cs_height_lg_75"></div>
    </section>
    <section class="xr_pillar_sec" id="governance">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        %s
        <div class="cs_height_20"></div>
        <p class="xr_pillar_lead" style="max-width:760px">%s</p>
        <div class="cs_height_20"></div>
        <div class="row"><div class="col-md-6"><ul class="xr_pillar_list">%s</ul></div>
        <div class="col-md-6"><ul class="xr_pillar_list">%s</ul></div></div>
        <div class="cs_height_25"></div>
        <p class="xr_pillar_note" style="max-width:860px">%s</p>
      </div>
      <div class="cs_height_90 cs_height_lg_60"></div>
    </section>
    <section class="xr_pillar_sec cs_gray2_bg" id="projects">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        %s
        <div class="cs_height_20"></div>
        <p class="xr_pillar_lead" style="max-width:820px">%s</p>
        <div class="cs_height_30"></div>
        <div class="row cs_gap_y_40 align-items-center">
          <div class="col-lg-7" data-aos="fade-up">
            <div class="xr_px_img xr_ficha_img" style="background-image:url('/assets/img/xaru/gen2/r/06_masterplan_ashima-1280.jpg');background-image:image-set(url('/assets/img/xaru/gen2/r/06_masterplan_ashima-1280.webp') type('image/webp'),url('/assets/img/xaru/gen2/r/06_masterplan_ashima-1280.jpg') type('image/jpeg'))"></div>
            %s
          </div>
          <div class="col-lg-5">
            <span class="xr_eyebrow_serif">%s</span>
            <h3 class="cs_fs_25" style="margin:10px 0 12px">%s</h3>
            <p class="xr_pillar_lead">%s</p>
            <a href="%sdevelopments/land-master-developments/" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>
          </div>
        </div>
        <div class="cs_height_40 cs_height_lg_30"></div>
        <div class="row"><div class="col-lg-8" data-aos="fade-up"><div class="xr_cap_item">
          <span class="xr_phase0">%s</span>
          <h3 class="cs_fs_25" style="font-size:22px;margin-top:12px">%s</h3>
          <p style="color:var(--secondary-color)">%s</p>
          <a href="%scapital/deal-room/" class="xr_link">%s<i class="fa-solid fa-angle-right"></i></a>
        </div></div></div>
      </div>
      <div class="cs_height_90 cs_height_lg_60"></div>
    </section>
    <section class="xr_pillar_sec" id="network">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        %s
        <div class="cs_height_20"></div>
        <p class="xr_pillar_lead" style="max-width:760px">%s</p>
        <div class="cs_height_25"></div>
        <div class="xr_insight_chips">%s</div>
        <div class="cs_height_25"></div>
        <p class="xr_pillar_note" style="max-width:760px">%s</p>
      </div>
      <div class="cs_height_90 cs_height_lg_60"></div>
    </section>
    <section class="xr_pillar_sec xr_dark_section text-center" id="contact">
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container">
        <span class="xr_eyebrow_serif" style="color:#fff">%s</span>
        <h2 class="cs_section_title cs_fs_49" style="color:#fff;max-width:820px;margin:12px auto 28px" data-aos="fade-up">%s</h2>
        <div class="d-flex gap-3 flex-wrap justify-content-center">
          <a href="%sprivate-enquiry/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a>
          <a href="%sopportunities/submit/" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>
        </div>
      </div>
      <div class="cs_height_120 cs_height_lg_75"></div>
    </section>''' % (
        _t(C["intro"], lang), _t(C["intro_sub"], lang),
        # who we are
        _sec_head(lang, C["who_eyebrow"], C["who_title"]),
        _t(C["who_lead"], lang), lvl, _t(C["who_phrase"], lang),
        # values
        _sec_head(lang, C["val_eyebrow"], C["val_title"]),
        vals, _t(C["val_note"], lang),
        # operating model
        _sec_head(lang, C["model_eyebrow"], C["model_title"]),
        _t(C["model_lead"], lang), divs,
        # offices
        _sec_head(lang, C["off_eyebrow"], C["off_title"]),
        _t(C["off_hq_tag"], lang), _t(C["off_hq_city"], lang), _t(C["off_hq_desc"], lang),
        ph0, _t(C["off_more_h"], lang), _t(C["off_more_p"], lang),
        # team
        _sec_head(lang, C["team_eyebrow"], C["team_title"]),
        _t(C["team_lead"], lang), team, ph0, _t(C["team_note"], lang),
        # entities
        _t(C["ent_eyebrow"], lang), _t(C["ent_title"], lang),
        _t(C["ent_main"], lang), _t(C["ent_sub"], lang),
        # governance
        _sec_head(lang, C["gov_eyebrow"], C["gov_title"]),
        _t(C["gov_lead"], lang), gov_a, gov_b, _t(ARCH.CAPABILITY_NOTE, lang),
        # projects
        _sec_head(lang, C["proj_eyebrow"], C["proj_title"]),
        _t(C["proj_lead"], lang), _img_note(lang, "geo"),
        _t(C["ashima_tag"], lang), _t(C["ashima_h"], lang), _t(C["ashima_p"], lang),
        home, _t(C["ashima_cta"], lang),
        ph0, _t(C["proj_more_h"], lang), _t(C["proj_more_p"], lang),
        home, _t(C["proj_more_cta"], lang),
        # network
        _sec_head(lang, C["net_eyebrow"], C["net_title"]),
        _t(C["net_lead"], lang), chips, _t(C["net_note"], lang),
        # cta
        _t(C["cta_eyebrow"], lang), _t(C["cta_title"], lang),
        home, _t(C["cta_btn"], lang), home, _t(C["cta_btn2"], lang))
    title = "%s — XARU HOME" % _t(shell["label"], lang)
    desc = "%s %s" % (_t(C["intro"], lang), _t(C["ent_main"], lang))
    return _write_shell(lang, "company", title, desc, body)

def _art_meta(lang, art):
    I = F5C.INSIGHTS
    cat_lbl = next(l for (s, l, b, k) in I["categories"] if s == art["cat"])
    return "%s · %s · %s" % (_t(cat_lbl, lang), art["date"], _t(I["byline"], lang))

def build_insights_hub(lang):
    I = F5C.INSIGHTS
    home = HOME[lang]
    shell = next(s for s in ARCH.SHELLS if s["slug"] == "insights")

    cats = []
    for (slug, lbl, blurb, artkey) in I["categories"]:
        if artkey:
            foot = ('<span class="xr_link">%s<i class="fa-solid fa-angle-right"></i></span>'
                    % _t(I["read"], lang))
            card = ('<a class="xr_infra_card" href="%sinsights/%s/"><h3>%s</h3><p>%s</p>%s</a>'
                    % (home, artkey, _t(lbl, lang), _t(blurb, lang), foot))
        else:
            card = ('<div class="xr_infra_card"><h3>%s</h3><p>%s</p>'
                    '<span class="xr_phase0">%s</span></div>'
                    % (_t(lbl, lang), _t(blurb, lang), _t(I["soon"], lang)))
        cats.append('<div class="col-lg-3 col-md-6" id="%s" data-aos="fade-up">%s</div>'
                    % (slug, card))

    arts = []
    for key in F5A.ORDER:
        a = F5A.ARTICLES[key]
        arts.append('''<div class="col-lg-6" data-aos="fade-up">
          <div class="xr_land_card xr_opp_card">
            <div class="xr_land_card_img"><div class="xr_px_img" style="%s"></div></div>
            <div class="xr_land_card_body">
              <p class="xr_land_card_meta mb-2">%s</p>
              <h3>%s</h3>
              <p class="xr_opp_desc">%s</p>
              <div class="xr_land_price"><span></span>
                <a href="%sinsights/%s/" class="xr_link">%s<i class="fa-solid fa-angle-right"></i></a>
              </div>
            </div>
          </div>
        </div>''' % (gen2_bg(a["img"], 1280), _art_meta(lang, a), _t(a["title"], lang),
                     _t(a["excerpt"], lang), home, key, _t(I["read"], lang)))

    body = _shell_hero(lang, shell) + '''
    <section>
      <div class="cs_height_120 cs_height_lg_75"></div>
      <div class="container"><div class="row"><div class="col-lg-9">
        <p class="xr_pillar_intro" data-aos="fade-up">%s</p>
        <p class="xr_pillar_lead" style="max-width:760px">%s</p>
      </div></div></div>
    </section>
    <section id="sectors">
      <div class="cs_height_75 cs_height_lg_50"></div>
      <div class="container">
        %s
        <div class="cs_height_40 cs_height_lg_30"></div>
        <div class="row cs_gap_y_30">%s</div>
      </div>
      <div class="cs_height_100 cs_height_lg_60"></div>
    </section>
    <section class="cs_gray2_bg" id="foundational">
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container">
        %s
        <div class="cs_height_40 cs_height_lg_30"></div>
        <div class="row cs_gap_y_30">%s</div>
      </div>
      <div class="cs_height_90 cs_height_lg_60"></div>
    </section>''' % (
        _t(I["intro"], lang), _t(I["intro_sub"], lang),
        _sec_head(lang, I["cats_eyebrow"], I["cats_title"]),
        "".join(cats),
        _sec_head(lang, I["found_eyebrow"], I["found_title"]),
        "\n        ".join(arts))
    title = "%s — XARU HOME" % _t(shell["label"], lang)
    desc = "%s %s" % (_t(I["intro"], lang), _t(I["intro_sub"], lang))
    return _write_shell(lang, "insights", title, desc, body)

def build_article(lang, key):
    I = F5C.INSIGHTS
    a = F5A.ARTICLES[key]
    home = HOME[lang]
    ins_lbl = ARCH.T("Insights", "Análisis", "رؤى", "洞察")
    trail = [(ins_lbl, "insights"), (a["title"], "insights/%s" % key)]
    hero = _page_header(lang, _t(ins_lbl, lang), _t(a["title"], lang),
                        _crumbs(lang, trail), a["img"])
    blocks = []
    for (kind, t) in a["body"]:
        if kind == "h":
            blocks.append('<h3 class="cs_fs_25" style="margin:34px 0 14px">%s</h3>' % _t(t, lang))
        else:
            blocks.append('<p class="xr_pillar_lead" style="margin-bottom:18px">%s</p>' % _t(t, lang))
    rel_href, rel_lbl = a["related"]
    body = hero + '''
    <section>
      <div class="cs_height_90 cs_height_lg_60"></div>
      <div class="container"><div class="row"><div class="col-lg-8">
        <p class="xr_land_card_meta" data-aos="fade-up">%s</p>
        <div class="cs_height_20"></div>
        %s
        <div class="cs_height_40 cs_height_lg_30"></div>
        <div class="d-flex gap-3 flex-wrap align-items-center">
          <a href="%s%s" class="cs_btn cs_style_1 xr_btn_ghost cs_radius_20"><span>%s</span></a>
          <a href="%sinsights/" class="xr_link">%s<i class="fa-solid fa-angle-right"></i></a>
        </div>
      </div></div></div>
    </section>
    <section class="xr_dark_section text-center">
      <div class="cs_height_100 cs_height_lg_60"></div>
      <div class="container">
        <span class="xr_eyebrow_serif" style="color:#fff">%s</span>
        <h2 class="cs_section_title cs_fs_38" style="color:#fff;max-width:760px;margin:12px auto 24px" data-aos="fade-up">%s</h2>
        <a href="%sprivate-enquiry/" class="cs_btn cs_style_1 cs_primary_bg cs_white_color cs_radius_20"><span>%s</span></a>
      </div>
      <div class="cs_height_100 cs_height_lg_60"></div>
    </section>''' % (
        _art_meta(lang, a), "\n        ".join(blocks),
        home, rel_href, _t(rel_lbl, lang),
        home, _t(I["back"], lang),
        _t(F2.HOME["desk_eyebrow"], lang), _t(F2.HOME["desk_title"], lang),
        home, _t(F2.HOME["desk_cta"], lang))
    title = "%s — XARU HOME" % _t(a["title"], lang)
    return _write_shell(lang, "insights/%s" % key, title, _t(a["excerpt"], lang), body)

# ---------------------------------------------------------------- blog -> insights redirect
_BLOG_RE = re.compile(r'[ \t]*<!-- xr-blog-redirect -->.*?<!-- /xr-blog-redirect -->\s*\n?', re.S)

def redirect_blogs():
    """Point the legacy blog pages at the new Insights hub: a same-language
    meta refresh + canonical to /insights/ in every blog.html / blog-details.html
    (EN root + es/ar/zh). Idempotent via marker comments. The _redirects file
    adds real 301s for hosts that support it."""
    for lang in ("en", "es", "ar", "zh"):
        pref = "" if lang == "en" else lang + "/"
        target = HOME[lang] + "insights/"
        for fname in ("blog.html", "blog-details.html"):
            p = "/home/claude/work/site/xaru/%s%s" % (pref, fname)
            if not os.path.exists(p):
                continue
            with open(p, encoding="utf-8") as f:
                h = f.read()
            h = _BLOG_RE.sub("", h)
            # canonical now points at the hub (strip the page's own canonical)
            h = re.sub(r'[ \t]*<link rel="canonical"[^>]*>\s*\n?', '', h)
            tag = ('    <!-- xr-blog-redirect -->\n'
                   '    <meta http-equiv="refresh" content="0; url=%s" />\n'
                   '    <link rel="canonical" href="https://xaruhome.com%s" />\n'
                   '    <!-- /xr-blog-redirect -->\n' % (target, target))
            h = h.replace("</head>", tag + "  </head>", 1)
            with open(p, "w", encoding="utf-8") as f:
                f.write(h)
            print("blog-redirect ->", p)

def build_phase5():
    for L in ("en", "es", "ar", "zh"):
        build_company(L)
        build_insights_hub(L)
        for key in F5A.ORDER:
            build_article(L, key)
    redirect_blogs()
    print("phase5 done")

# ================================================================ Phase 6 — sitemap + llms.txt
SITE_ROOT = "/home/claude/work/site/xaru"
LASTMOD = "2026-07-31"

# ---------------------------------------------------------------- portal heredado -> fuera
# La plantilla traia un area de cliente completa: "Property Agents" con seis
# personas inventadas, telefonos (555) y correos @xaruhome.com que no existen,
# mas el panel de "Amanda Jones" con Lorem ipsum. Estaba publicado y ademas en
# el sitemap en cuatro idiomas. XARU no opera como agencia con cartera de
# agentes, asi que no se maquilla: se saca de circulacion.
_PORTAL_RE = re.compile(r'[ \t]*<!-- xr-portal-redirect -->.*?<!-- /xr-portal-redirect -->\s*\n?', re.S)
PORTAL_PAGES = ("agents-list.html", "profile.html", "client-list.html",
                "add-property.html", "edit-property.html", "my-property.html",
                "favourite-property.html", "profile-settings.html")

def _strip_body(h, target, label):
    """Deja solo la cabecera y un enlace. Estas paginas ya no se sirven: dejar
    su cuerpo intacto significaba seguir publicando agentes inventados,
    testimonios repetidos y telefonos (555) que cualquier rastreador que
    ignore el meta refresh se lleva igual. El original queda en el historial."""
    m = re.search(r'<body[^>]*>', h)
    if not m:
        return h
    end = h.find("</body>")
    if end < 0:
        return h
    body = ('\n    <main style="font-family:system-ui,sans-serif;padding:80px 24px;text-align:center">\n'
            '      <p><a href="%s">%s</a></p>\n'
            '    </main>\n  ' % (target, label))
    return h[:m.end()] + body + h[end:]

LEGACY_REDIRECT = {
    # about-us.html es la pagina institucional de la plantilla: bajo la copia
    # buena de XARU traia tres testimonios inventados con la MISMA frase
    # repetida y cinco estrellas, y los cuatro agentes ficticios. La pagina
    # real de compania es /company/, escrita en la fase 5.
    "about-us.html": "company/",
    # single-property-v1.html es una landing oscura de plantilla: "$0B+ vendido",
    # "0K+ clientes satisfechos", planos de planta y folletos de un apartamento
    # de 980.000 dolares. Nada de eso es de esta casa.
    "single-property-v1.html": "property-listing-search.html",
}

def redirect_legacy():
    n = 0
    for lang in ("en", "es", "ar", "zh"):
        pref = "" if lang == "en" else lang + "/"
        for fname, dest in LEGACY_REDIRECT.items():
            p = "/home/claude/work/site/xaru/%s%s" % (pref, fname)
            if not os.path.exists(p):
                continue
            target = HOME[lang] + dest
            with open(p, encoding="utf-8") as f:
                h = f.read()
            h = _PORTAL_RE.sub("", h)
            h = re.sub(r'[ \t]*<link rel="canonical"[^>]*>\s*\n?', '', h)
            tag = ('    <!-- xr-portal-redirect -->\n'
                   '    <meta http-equiv="refresh" content="0; url=%s" />\n'
                   '    <link rel="canonical" href="https://xaruhome.com%s" />\n'
                   '    <!-- /xr-portal-redirect -->\n' % (target, target))
            h = h.replace("</head>", tag + "  </head>", 1)
            h = _strip_body(h, target, "XARU HOME")
            with open(p, "w", encoding="utf-8") as f:
                f.write(h)
            n += 1
    print("paginas heredadas redirigidas ->", n)


def redirect_portal():
    n = 0
    for lang in ("en", "es", "ar", "zh"):
        pref = "" if lang == "en" else lang + "/"
        target = HOME[lang]
        for fname in PORTAL_PAGES:
            p = "/home/claude/work/site/xaru/%s%s" % (pref, fname)
            if not os.path.exists(p):
                continue
            with open(p, encoding="utf-8") as f:
                h = f.read()
            h = _PORTAL_RE.sub("", h)
            h = re.sub(r'[ \t]*<link rel="canonical"[^>]*>\s*\n?', '', h)
            h = re.sub(r'[ \t]*<meta name="robots"[^>]*>\s*\n?', '', h)
            tag = ('    <!-- xr-portal-redirect -->\n'
                   '    <meta name="robots" content="noindex,nofollow" />\n'
                   '    <meta http-equiv="refresh" content="0; url=%s" />\n'
                   '    <link rel="canonical" href="https://xaruhome.com/" />\n'
                   '    <!-- /xr-portal-redirect -->\n' % target)
            h = h.replace("</head>", tag + "  </head>", 1)
            h = _strip_body(h, target, "XARU HOME")
            with open(p, "w", encoding="utf-8") as f:
                f.write(h)
            n += 1
    print("portal heredado retirado ->", n, "paginas")

def build_utility():
    """Legacy portal / auth / error templates: unique title + description +
    noindex, and dead template links repointed. English root only, never in the
    sitemap and never in the mega-menu."""
    n = 0
    for fname in seo_meta.UTILITY_META:
        p = SITE_ROOT + "/" + fname
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8") as f:
            h = f.read()
        h = seo_meta.set_utility_head(h, fname)
        h = fix_dead_links(h)
        with open(p, "w", encoding="utf-8") as f:
            f.write(h)
        n += 1
    print("utility pages ->", n)

def build_sitemap():
    """Full sitemap: every live URL in the four languages, clean folder URLs for
    the new architecture, .html for the legacy core. blog.html / blog-details.html
    are excluded (they 301/refresh to /insights/)."""
    langs = (("en", ""), ("es", "es/"), ("ar", "ar/"), ("zh", "zh/"))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    n = 0
    for path, pr in seo_meta.sitemap_entries():
        for lang, pref in langs:
            out.append("  <url>")
            out.append("    <loc>https://xaruhome.com/%s%s</loc>" % (pref, path))
            for hl, p2 in (("en", ""), ("es", "es/"), ("ar", "ar/"), ("zh-CN", "zh/")):
                out.append('    <xhtml:link rel="alternate" hreflang="%s" href="https://xaruhome.com/%s%s" />'
                           % (hl, p2, path))
            out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="https://xaruhome.com/%s" />' % path)
            out.append("    <lastmod>%s</lastmod>" % LASTMOD)
            out.append("    <priority>%s</priority>" % (pr if lang == "en" else
                                                        "%.1f" % max(0.1, float(pr) - 0.1)))
            out.append("  </url>")
            n += 1
    out.append("</urlset>")
    xml = "\n".join(out) + "\n"
    from xml.dom import minidom
    minidom.parseString(xml)          # fail loudly on malformed XML
    with open(SITE_ROOT + "/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml)
    print("sitemap ->", n, "urls")
    return n

LLMS = """# XARU HOME

> XARU HOME is the international real estate, development and business-infrastructure
> structure of NEXARU GLOBAL (UAE-licensed, based in Dubai). It reads on three levels:
> a clear real estate house at the surface; development, financing and execution beneath
> it; and a complete business platform underneath that. Four doors, seven autonomous
> divisions, three catalogues, a private deal room and a research desk — one structure,
> worldwide, in English, Spanish, Arabic and Chinese.

## The three levels

- Level 1 — Real estate, clearly: acquisition and sale of private islands, villas,
  castles, estates, branded residences, operating hotels, resorts and income assets.
- Level 2 — Development, financing and execution: territorial land, master plans,
  project structuring (feasibility, legal and fiduciary structuring, SPVs, licensing,
  operator selection, development management), capital and transactions.
- Level 3 — Business platform: corporate infrastructure, company formation, international
  relocation, commodities offtake and placement, and the governance behind all of it.

## The four doors

- [Real Estate](https://xaruhome.com/real-estate/): the property division — private
  islands, villas, estates and operating hospitality assets, curated worldwide.
- [Developments](https://xaruhome.com/developments/): land and master developments, from
  territory and feasibility to structuring, execution and delivery.
- [Capital & Transactions](https://xaruhome.com/capital/): a two-way structure — projects
  that seek capital, capital that seeks projects — under XARU's own diligence.
- [Business Infrastructure](https://xaruhome.com/business-infrastructure/): the corporate
  layer that continues after the transaction closes.

## The seven divisions

- [Private Properties](https://xaruhome.com/real-estate/private-properties/): villas,
  mansions, castles, estates, private islands, branded residences, private search by mandate.
- [Commercial & Hospitality](https://xaruhome.com/real-estate/commercial-hospitality/):
  operational hotels, repositioning, resorts, serviced residences, marinas, income
  commercial, halted or incomplete projects, confidential portfolio.
- [Land & Master Developments](https://xaruhome.com/developments/land-master-developments/):
  large, coastal, resort, permitted and regularizing land; master plans; planned
  communities; signature destinations including ASHIMA.
- [Project Structuring & Development](https://xaruhome.com/developments/project-structuring/):
  feasibility, legal and fiduciary structuring, SPVs, master plan and business model,
  licensing, operator selection, development management, commercialization.
- [Capital & Strategic Partnerships](https://xaruhome.com/capital/strategic-partnerships/):
  projects seeking capital, capital seeking projects, joint ventures, funds and family
  offices, due diligence, deal origination, transaction management.
- [Trade & Financial Infrastructure](https://xaruhome.com/business-infrastructure/trade-financial/):
  commodities offtake and placement, productive assets, and financial infrastructure
  designed, integrated and coordinated through authorised entities and partners.
- [Corporate Services & Relocation](https://xaruhome.com/business-infrastructure/corporate-services/):
  company formation in the UAE and elsewhere, entities, licensing, banking introductions,
  residency and international relocation for families and operations.

## The three catalogues

- [Private Properties catalogue](https://xaruhome.com/real-estate/private-properties/):
  private islands, villas, estates and branded residences for sale worldwide.
- [Commercial & Hospitality catalogue](https://xaruhome.com/real-estate/commercial-hospitality/):
  operational hotels for sale, resorts, halted projects and income assets, presented with
  their operating state — never as static listings.
- [Land, Projects & Opportunities](https://xaruhome.com/opportunities/): development land
  for sale, master plans, halted projects and capital opportunities under live mandate.

## Private Deal Room

- [Private Deal Room](https://xaruhome.com/capital/deal-room/): off-market real estate
  opportunities that are too large, too sensitive or too strategic for a public listing.
  Public teasers show region, category, scale and status only. Everything beyond the
  teaser travels a nine-step private route: access request, verification, NDA, approval,
  data room, adviser, transaction.
- [Submit an opportunity](https://xaruhome.com/opportunities/submit/): two-way intake for
  an asset, a project or capital.
- [Private Enquiry](https://xaruhome.com/private-enquiry/): one conversation, one
  structure, total confidentiality.

## Company & Insights

- [Company](https://xaruhome.com/company/): three levels, seven autonomous divisions, the
  entities XARU operates under, governance, offices, specialities and network.
- [Insights](https://xaruhome.com/insights/): research from XARU HOME Research across seven
  sectors. Foundational analyses (2026):
  [operational hospitality](https://xaruhome.com/insights/operational-hospitality/),
  [territorial land](https://xaruhome.com/insights/territorial-land/),
  [private capital and halted projects](https://xaruhome.com/insights/capital-halted-projects/),
  [establishing internationally](https://xaruhome.com/insights/international-establishment/).

## Legacy pages

- [About XARU HOME](https://xaruhome.com/about-us.html): the company, its NEXARU GLOBAL
  parent, the five pillars and the global network.
- [Contact](https://xaruhome.com/contact.html): private enquiries by appointment. Office in
  Dubai, United Arab Emirates. Email contact@xaruhome.com / support@xaruhome.com.
- [FAQ](https://xaruhome.com/faq.html): services, acquisition process, fees and
  digital-asset transactions.
- [Properties for sale](https://xaruhome.com/property-listing-buy.html) and
  [property search](https://xaruhome.com/property-listing-search.html).

## Languages

- English (root), Spanish (/es/), Arabic (/ar/, right-to-left), Chinese (/zh/).
  Every page declares reciprocal hreflang for en, es, ar, zh-CN plus x-default.

## Entity

- Brand: XARU HOME, a brand of NEXARU GLOBAL.
- Licensing: UAE-licensed; registered office in Dubai, United Arab Emirates.
- Experience: 20+ years advising private clients, families and institutions.
- Capacity: depending on the project, jurisdiction, feasibility and mandate, XARU may act
  as adviser, structurer, integrator, sponsor, manager or participant. XARU designs,
  integrates and coordinates financial and technological infrastructure through authorised
  entities and partners where the activity requires it.
- Reach: United Arab Emirates, Middle East, China, India, Pakistan, Europe, United States,
  Mexico, Colombia, Ecuador, Peru, Panama, Dominican Republic, El Salvador, Nicaragua.
- Languages: English, Spanish, Arabic, Chinese.

## Compliance

- Digital-asset transactions are conducted exclusively through regulated channels, with full
  KYC/AML verification and legal counsel in each jurisdiction. XARU HOME does not offer
  unregulated crypto services and does not provide financial or tax advice; all figures and
  availability are subject to due diligence.

## Contact

- Email: contact@xaruhome.com — support@xaruhome.com
- Office: Dubai, United Arab Emirates (private offices, by appointment).
"""

def build_llms():
    with open(SITE_ROOT + "/llms.txt", "w", encoding="utf-8") as f:
        f.write(LLMS)
    print("llms.txt ->", len(LLMS), "bytes")

if __name__ == "__main__":
    for L in ("es", "ar", "zh"):
        build_index(L)
    for name in PAGES:
        for L in ("es", "ar", "zh"):
            build_page(L, name)
    # refresh English root pages last (switcher + hreflang) from pristine source
    for name in ["index"] + list(PAGES.keys()):
        build_en(name)
    # Phase 1 shell pages (4 doors + 7 divisions + Company + Insights + 2 forms)
    build_all_shells()
    # Phase 2 property core: catalogs, fichas, pillars (override shells)
    build_catalogs_fichas_pillars()
    # Biblia §5.6: directorios y perfiles de asesores, oficinas y promotoras
    build_directories()
    # Biblia §5.5: proyectos off-plan con sus planes de pago
    build_projects()
    # Biblia §5.7-§5.9: paneles de comprador, oficina y administracion
    build_panels()
    # Phase 2 homepage: 12-block re-order (all four languages)
    for L in ("en", "es", "ar", "zh"):
        inject_home(L)
    # Phase 3 development & capital core (overrides the generic shells)
    build_phase3()
    # Phase 4 business infrastructure (overrides the generic shells)
    build_phase4()
    # Phase 5 institutional trust: Company + Insights hub + foundational articles
    build_phase5()
    # Phase 6 SEO close-out: utility pages, full sitemap + llms.txt
    build_utility()
    redirect_portal()
    redirect_legacy()
    build_sitemap()
    build_llms()
    # ---- pasada final de jerarquia de encabezados ----------------------
    # Algunas paginas de la plantilla (login, registro, recuperar clave,
    # detalle de blog) no pasan por los constructores anteriores, asi que la
    # correccion se aplica al final sobre TODO lo generado. Es idempotente.
    import glob as _glob
    _root = "/home/claude/work/site/xaru"
    # El glob por niveles dejaba fuera las fichas de real estate en es/ar/zh,
    # que estan a cinco niveles: 27 paginas nunca recibieron ninguna de las
    # correcciones de esta pasada. Se hace recursivo.
    _files = _glob.glob(_root + "/**/*.html", recursive=True)
    _n = 0
    for _f in _files:
        with open(_f, encoding="utf-8") as _fh:
            _h = _fh.read()
        _o = _h
        _base = os.path.basename(_f)
        _lang = "en"
        _rel = _f[len(_root) + 1:]
        for _L in ("es", "ar", "zh"):
            if _rel.startswith(_L + "/"):
                _lang = _L
        _h = migrate_catalog_mount(_h, _base)
        _h = purge_dead_links(_h)
        _h = strip_index_html(_h, _lang)
        _h = purge_template_images(_h, _lang)
        _h = fix_listing_page(_h, _base, _lang)
        # La ficha de activo se monta desde datos (?id=). El script debe estar
        # en las cuatro versiones de idioma, no solo en la inglesa.
        if _base == "property-details.html":
            # La copia de ejemplo de la plantilla — "Evergreen Estates",
            # 70.000 dolares, una casa alquilada en Filadelfia — se queda en el
            # HTML estatico y la ve cualquiera que llegue sin JavaScript, y
            # tambien los rastreadores. Se sustituye por el texto real que la
            # ficha usara al montarse.
            # El nombre de ejemplo aparece traducido en cada idioma
            # ("Fincas Evergreen", "إيفرغرين"…): se barren todas las variantes.
            for _dummy in ("Evergreen Estates", "Fincas Evergreen", "Evergreen"):
                _h = _h.replace(_dummy, "XARU HOME")
            _h = _h.replace("217 Horizon Heights Road, Silverstone Towers, NY 10022",
                            "Location shown on the asset record")
            _h = re.sub(r'\$(?:70|50),000', "Price upon application", _h)
            _h = re.sub(r'Est\. Payment \$[\d,]+/mo\*', "", _h)
            _h = _h.replace("Appartment", "Asset").replace("Built in 2010", "")
            _m = re.search(r'<p class="mb-0">Welcome home!.*?</p>', _h, re.S)
            if _m:
                _h = _h[:_m.start()] + '<p class="mb-0"></p>' + _h[_m.end():]
        if _base == "property-details.html":
            # La ficha usa los mismos bloques que el marketplace (distintivos,
            # panel de verificacion, mapa), asi que carga su hoja. Rutas
            # absolutas: la pagina existe en los cuatro arboles de idioma.
            if "xaru-marketplace.css" not in _h:
                _h = _h.replace('<link rel="stylesheet" href="/assets/css/xaru.css" />',
                                '<link rel="stylesheet" href="/assets/css/xaru.css" />\n'
                                '    <link rel="stylesheet" href="/assets/css/xaru-marketplace.css" />', 1)
                if "xaru-marketplace.css" not in _h:
                    _h = _h.replace("</head>",
                                    '    <link rel="stylesheet" href="/assets/css/xaru-marketplace.css" />\n  </head>', 1)
            if "xaru-property-detail.js" not in _h:
                _h = _h.replace("</body>",
                                '    <script src="/assets/js/xaru-property-detail.js"></script>\n  </body>', 1)
            else:
                _h = re.sub(r'<script src="(?:\.\./)*assets/js/xaru-property-detail\.js">',
                            '<script src="/assets/js/xaru-property-detail.js">', _h)
        _h = restore_listing_h1(_h, _base, _lang)
        _h = ensure_h1(_h, _base)
        _h = enforce_single_h1(_h)
        if _h != _o:
            with open(_f, "w", encoding="utf-8") as _fh:
                _fh.write(_h)
            _n += 1
    print("jerarquia de encabezados -> %d paginas corregidas" % _n)
    print("done")
