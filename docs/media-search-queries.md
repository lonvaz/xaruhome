# CONSULTAS DE BÚSQUEDA DE MATERIAL — XARU HOME
**Fase 5 · Búsqueda de material** (incluye Fase 6 — criterios de rechazo y evaluación editorial)
Rama `agent/real-stock-media-audit` · 31-jul-2026
Insumos: [`visual-audit.md`](visual-audit.md) · [`visual-plan-home.md`](visual-plan-home.md) · [`visual-plan-inner-pages.md`](visual-plan-inner-pages.md)

> **Este documento no modifica ningún archivo del sitio. Es plan de búsqueda.**

---

## 0. CÓMO SE BUSCA

**Regla rectora.** Todo lo que se busque aquí sirve para representar **categorías y capacidades**. Ningún resultado de esta búsqueda puede acabar ilustrando un activo concreto de XARU (con nombre, precio, ubicación, superficie, nº de llaves, licencia, ASHIMA o isla identificable). Para eso sólo vale material auténtico del propietario o bloqueo/teaser.

**Cómo NO se busca.** Las consultas de una palabra son la causa directa del estado actual del sitio:

| Prohibido | Por qué |
|---|---|
| `luxury` | Devuelve mármol dorado, champán y catálogo. Es el término que produjo `13_investment_bg` y compañía. |
| `business` | Devuelve apretones de manos, gráficos y "hombre mirando la ciudad". |
| `real estate` | Devuelve fichas de agencia estadounidense y llaves sobre contrato. |
| `modern`, `elegant`, `exclusive`, `premium`, `dream` | Adjetivos: el banco los interpreta como "más brillante y más saturado". |
| `success`, `growth`, `future`, `innovation` | Metáforas: hologramas, redes de puntos y flechas. |

**Cómo SÍ se busca.** Sujeto + acción + condición de luz + punto de vista, en inglés (idioma de indexación de los bancos) y sin adjetivos de valor. Ejemplo: `hotel back of house corridor linen trolleys morning natural light` en vez de `luxury hotel`.

**Filtros que se aplican siempre**, además de los de cada ficha:

- Sin personas identificables en primer plano salvo que se indique, y en ese caso con **model release** verificado.
- Sin logotipos, marcas, matrículas, rótulos comerciales ni texto legible en ninguna lengua.
- Sin marcas de agua, sin bordes, sin firma del autor en el píxel.
- Excluir explícitamente categorías `AI generated` / `Generative AI` del proveedor. Si el proveedor no permite excluirlas, se aplica el criterio de rechazo §9 sobre cada candidata.
- Descargar **el original máximo**, nunca la vista previa.
- Registrar en la hoja de control: recurso · proveedor · nº de licencia · factura · fecha · alcance (web, 4 idiomas, redes, duración).

**Notación de resolución.** "Mín." es el lado largo del **original descargado**, no del recorte final. Los fondos a ancho completo necesitan 3000 px porque el sitio los sirve a 1920 px con `srcset` de 3 anchos y una variante vertical.

---

## 1. RESIDENCIAS

Destino: `H-03a` (portada, Private Real Estate), hero de `real-estate/`, `private-properties/`, fondos de sección residencial, Insights de residencial.
Prohibición transversal del grupo: **ninguna de estas imágenes puede aparecer en una tarjeta o ficha de activo nominado.**

| ID | Consulta | Orientación | Res. mín. | Debe aparecer en el encuadre | NO debe aparecer |
|---|---|---|---|---|---|
| RES-01 | `contemporary concrete house facade in side afternoon light, exterior, no people` | Horizontal 3:2 | 3000 px | Un volumen arquitectónico completo, sombra propia marcada, material visible (hormigón, piedra, madera) | Piscina, coche, mobiliario de jardín, personas, cielo reemplazado |
| RES-02 | `stone courtyard of a Mediterranean house with olive tree, morning shade` | Vertical 4:5 | 2400 px | Patio cerrado, pavimento de piedra, una sola sombra de vegetación | Mesa puesta, copas, cojines de revista, guirnaldas de luces |
| RES-03 | `detail of timber window frame and shutter on a rendered wall, natural light` | Cuadrado 1:1 | 2000 px | Carpintería real con marcas de uso, textura de revoco | Cristal reflejando un skyline, interiores visibles, precinto de obra |
| RES-04 | `hillside residential architecture seen from a distance among vegetation` | Horizontal 16:9 | 3600 px | Arquitectura integrada en el terreno, escala del paisaje | Un inmueble aislado y protagonista que pueda leerse como "en venta" |
| RES-05 | `empty room with bare walls and window light falling on the floor` | Horizontal 3:2 | 2400 px | Habitación vacía, luz de ventana dibujada en el suelo, superficie sin tratar | Muebles de catálogo, alfombras, arte enmarcado, staging |
| RES-06 | `long staircase and handrail in a residential interior, low contrast daylight` | Vertical 4:5 | 2400 px | Escalera como pieza arquitectónica, barandilla, luz cenital o lateral | Lámparas de araña, mármol pulido brillante, espejos |
| RES-07 | `roof tiles and chimneys of an old town seen from above at dawn` | Horizontal 21:9 | 3600 px | Tejido residencial denso, textura de cubierta, primera luz | Monumentos identificables, antenas modernas dominantes, turistas |
| RES-08 | `terrace floor and low wall facing an out of focus landscape` | Horizontal 3:2 | 2400 px | Umbral entre interior y paisaje, profundidad, materia del suelo | Tumbonas, sombrillas, piscina infinita, cóctel |
| RES-09 | `entrance door and threshold of a private house, side light, closed` | Vertical 4:5 | 2400 px | Puerta cerrada, umbral, materia; sensación de discreción | Números de portal legibles, buzón con nombre, cámaras, timbres con etiqueta |

---

## 2. HOSPITALITY

Destino: `H-03b`, hero de `real-estate/commercial-hospitality/`, artículo `insights/operational-hospitality` (I-11a).
Ángulo del grupo: **el activo que renta**, no el que se fotografía para un folleto. Operación, P&L, ocupación — se ve en el *back of house*, no en la suite.

| ID | Consulta | Orientación | Res. mín. | Debe aparecer en el encuadre | NO debe aparecer |
|---|---|---|---|---|---|
| HOS-01 | `hotel back of house corridor with linen trolleys, working hours, no guests` | Horizontal 3:2 | 2400 px | Pasillo de servicio, carros, señales de uso real | Huéspedes, alfombra de suite, dorados, iluminación de escenografía |
| HOS-02 | `hotel service kitchen during a shift, cooks working, seen from a distance` | Horizontal 3:2 | 2400 px | Actividad real, vapor, acero de cocina profesional, personas a media distancia | Rostros en primer plano, emplatado gourmet en primer término, chef posando |
| HOS-03 | `hotel reception desk at shift change, staff working, morning light` | Horizontal 16:9 | 3000 px | Mostrador en funcionamiento, dos personas, movimiento leve | Sonrisas a cámara, huésped entregando tarjeta con datos legibles, logotipo del hotel |
| HOS-04 | `housekeeping trolley in an empty hotel corridor, natural light from a window` | Vertical 4:5 | 2400 px | Carro de limpieza, pasillo largo, puertas numeradas sin marca | Nombre de cadena, números de habitación legibles y reconocibles, personal posando |
| HOS-05 | `hotel occupancy board or duty roster on a wall, back office` | Cuadrado 1:1 | 2000 px | Tablero de gestión, textura de oficina de operación | Datos legibles (nombres, cifras, fechas), pantallas con software identificable |
| HOS-06 | `hotel terrace before opening, chairs stacked, early morning, no people` | Horizontal 3:2 | 3000 px | Terraza fuera de servicio, sillas apiladas, luz temprana | Atardecer, cóctel, piscina iluminada, huéspedes en bata |
| HOS-07 | `loading bay and service entrance of a hotel building, daytime` | Horizontal 16:9 | 3000 px | Acceso logístico, muelle, contenedores de residuos, realidad operativa | Fachada principal glamurosa, portero de librea, alfombra roja |
| HOS-08 | `laundry room of a hotel with industrial machines in operation` | Horizontal 3:2 | 2400 px | Maquinaria industrial, cesta de lencería, calor | Marca del fabricante legible, operarios identificables |
| HOS-09 | `restaurant dining room being set before service, empty, daylight` | Horizontal 3:2 | 2400 px | Sala en preparación, sillas aún sin colocar, luz natural | Comensales, velas, montaje de boda, decoración temática |

---

## 3. SUELO Y DESARROLLOS

Destino: `H-03c`, hero de `developments/`, `land-master-developments/`, `project-structuring/`, artículo `insights/territorial-land` (I-11b), banda `H-05`.
Ángulo del grupo: **escala y tiempo**. El suelo territorial es una tesis, no una parcela.

| ID | Consulta | Orientación | Res. mín. | Debe aparecer en el encuadre | NO debe aparecer |
|---|---|---|---|---|---|
| SUE-01 | `high aerial view of extensive terrain showing a change of land use, dry season` | Horizontal 16:9 | 4000 px | Extensión sin límite visible, transición monte→cultivo→camino, referencia de escala mínima | Linderos, cifras, vallas de parcelación, urbanización, playa dorada |
| SUE-02 | `dirt track crossing open land towards a distant horizon` | Horizontal 21:9 | 3600 px | Camino como única obra humana, horizonte muy lejano | Señalización, coches, carteles de promotor |
| SUE-03 | `boundary between cultivated fields and uncleared scrubland from the air` | Horizontal 3:2 | 3600 px | Frontera de uso legible desde el aire, textura de dos vegetaciones | Marcadores catastrales, coordenadas GPS sobreimpresas |
| SUE-04 | `long coastline seen from high altitude, overcast, no buildings` | Horizontal 21:9 | 4000 px | Litoral largo, sin edificación, luz plana | Turquesa artificial, resort, embarcaciones, isla identificable |
| SUE-05 | `surveyor stakes and marking tape on open ground, low angle` | Cuadrado 1:1 | 2000 px | Estaca, cinta, tierra; el gesto del replanteo | Planos con datos legibles, personas identificables, logotipos en el equipo |
| SUE-06 | `topographic relief of dry hills at low sun, aerial` | Horizontal 16:9 | 4000 px | Relieve modelado por la luz rasante, escala geológica | Vegetación clonada (patrón repetido), cielo sustituido |
| SUE-07 | `quarry working face with excavator and aggregate stockpiles, daytime` | Horizontal 3:2 | 3600 px | Frente de explotación real, maquinaria, montones de árido | Marca de la maquinaria legible, operarios identificables. **Nunca se usará para la cantera concreta de XARU** |
| SUE-08 | `unfinished concrete frame of a building with vegetation growing, flat grey light` | Horizontal 3:2 | 3000 px | Estructura detenida, vegetación colonizando, óxido | Grúa en movimiento, obreros, cartel de obra con nombre |
| SUE-09 | `architectural site model on a table, raking light, no people` | Horizontal 3:2 | 2400 px | Maqueta física, topografía en capas, sombras marcadas | Render en pantalla al fondo, nombre de proyecto legible |
| SUE-10 | `construction site at intermediate stage seen frontally, scaffolding, dusk` | Panorámica 8:3 | 4000 px | Obra a media altura, andamio, cerramiento parcial | Marca de constructora, grúas con rótulo, cielo dramático |

---

## 4. CAPITAL Y ESTRUCTURACIÓN

Destino: hero de `capital/`, `strategic-partnerships/`, `deal-room/`, bloque `H-06` (mitad capital), `H-10` gobierno y confianza, artículo `insights/capital-halted-projects` (I-11c).
Ángulo del grupo: **la sala, el documento y el silencio.** Cero iconografía financiera.

| ID | Consulta | Orientación | Res. mín. | Debe aparecer en el encuadre | NO debe aparecer |
|---|---|---|---|---|---|
| CAP-01 | `empty boardroom with a long table lit by window light, no people` | Horizontal 16:9 | 3000 px | Mesa larga, sillas alineadas, luz natural lateral | Pantallas encendidas, gráficos, jarra de agua de catálogo, vistas de skyline dominantes |
| CAP-02 | `closed paper file on a dark table, side light, macro` | Cuadrado 1:1 | 2400 px | Canto del expediente, textura del papel, sombra | Texto legible, nombres, cifras, sellos identificables |
| CAP-03 | `hand signing a document, cropped, no face, natural light` | Horizontal 3:2 | 2400 px | Gesto de firma, pluma, papel; manos anatómicamente correctas | Rostro, contenido legible del documento, anillos o relojes de marca |
| CAP-04 | `archive shelves with numbered document boxes, corridor perspective` | Vertical 4:5 | 3000 px | Archivo físico, cajas, perspectiva de fuga | Etiquetas legibles, nombres de empresa, personas |
| CAP-05 | `blinds casting light stripes on an office desk, no people` | Horizontal 3:2 | 2400 px | Luz de persiana, superficie de mesa, geometría de sombras | Ordenador con pantalla visible, tazas de café, plantas decorativas |
| CAP-06 | `two chairs facing each other in an empty room, low light` | Horizontal 3:2 | 2400 px | Dos sillas, distancia, penumbra; la conversación que aún no ocurre | Personas, mesa de negociación, cámaras |
| CAP-07 | `stack of technical reports and bound documents on a desk` | Cuadrado 1:1 | 2000 px | Volumen físico de documentación, encuadernación | Títulos legibles, logotipos, gráficos visibles |
| CAP-08 | `corridor leading to a closed door, dim interior lighting` | Vertical 4:5 | 2400 px | Pasillo, puerta cerrada al fondo, una sola fuente de luz | Rótulos, números de sala, señalética de empresa |
| CAP-09 | `stationary crane over an unfinished building, flat grey sky` | Horizontal 3:2 | 3000 px | Grúa inmóvil, estructura parada, cielo neutro | Actividad, operarios, atardecer dramático, marca de la grúa |

---

## 5. RELOCALIZACIÓN

Destino: hero de `business-infrastructure/corporate-services/`, artículo `insights/international-establishment` (I-11d), bloques de migración y establecimiento.
Ángulo del grupo: **el trámite, no el destino.** Administrativo, sobrio, sin promesa de estilo de vida.

| ID | Consulta | Orientación | Res. mín. | Debe aparecer en el encuadre | NO debe aparecer |
|---|---|---|---|---|---|
| REL-01 | `waiting area of an administrative office with a service counter, daylight` | Horizontal 3:2 | 2400 px | Mostrador, sillas de espera, luz institucional | Banderas, escudos nacionales, personas identificables, colas |
| REL-02 | `rubber stamp pressed on a paper form, close up, no readable text` | Cuadrado 1:1 | 2000 px | Sello, tinta, papel de formulario | Texto legible, nombres, número de expediente, escudo de un país |
| REL-03 | `airport transit corridor at dawn, few people, motion blur` | Horizontal 16:9 | 3000 px | Tránsito, hora temprana, arquitectura de terminal | Logotipos de aerolínea, rótulos de destino legibles, rostros |
| REL-04 | `numbered queue ticket dispenser in a public office` | Vertical 4:5 | 2000 px | Máquina de turno, número, pared neutra | Nombre del organismo, idioma que fije una jurisdicción no declarada |
| REL-05 | `moving boxes stacked in an empty apartment with window light` | Horizontal 3:2 | 2400 px | Cajas, piso vacío, luz de ventana | Familia sonriente, mascotas, cinta de mudanza con marca |
| REL-06 | `office nameplate slot empty on a wall directory` | Cuadrado 1:1 | 2000 px | Directorio de empresas con hueco vacío; la instalación aún por hacer | Nombres de empresas reales legibles |
| REL-07 | `desk with a folder, a pen and an empty chair, administrative interior` | Horizontal 3:2 | 2400 px | Escritorio de trámite, expediente cerrado | Ordenador con software identificable, tazas, decoración personal |
| REL-08 | `city street of a business district early morning, few people, flat light` | Horizontal 16:9 | 3600 px | Calle real de distrito de negocios, luz plana | Skyline icónico usado como promesa, rótulos de banco, turistas |

---

## 6. INFRAESTRUCTURA FINANCIERA

Destino: hero de `business-infrastructure/trade-financial/`, bloque `H-08`, secciones de pagos, orquestación, conciliación e integraciones.
Ángulo del grupo: **infraestructura física real.** Cero metáforas digitales.

| ID | Consulta | Orientación | Res. mín. | Debe aparecer en el encuadre | NO debe aparecer |
|---|---|---|---|---|---|
| FIN-01 | `data center cold aisle corridor, server racks, no people` | Horizontal 2:1 | 3600 px | Pasillo de racks, cableado ordenado, iluminación técnica | Luces azules de cine, humo, hologramas, marcas de fabricante |
| FIN-02 | `structured network cabling patch panel, close up` | Cuadrado 1:1 | 2400 px | Panel de parcheo, cables etiquetados sin texto legible | Etiquetas legibles, logotipos, cables desordenados de decorado |
| FIN-03 | `operations room with switched off screens, low light` | Horizontal 16:9 | 3000 px | Sala de operación real, monitores apagados, mobiliario técnico | Gráficos bursátiles en pantalla, velas japonesas, mapas del mundo con líneas |
| FIN-04 | `printed ledger or reconciliation sheet on a desk, side light` | Horizontal 3:2 | 2400 px | Papel de conciliación, columnas, textura de impresión matricial | Cifras legibles, nombres de entidad, membretes |
| FIN-05 | `technician working on server hardware, hands only, no face` | Horizontal 3:2 | 2400 px | Manos correctas, herramienta, hardware abierto | Rostro, marca del equipo, guantes de laboratorio de stock |
| FIN-06 | `underground utility conduits and cable trays in a technical corridor` | Vertical 4:5 | 2400 px | Canalización, bandeja de cables, hormigón visto | Señalética con texto, tuberías con marca, iluminación de color |
| FIN-07 | `fibre optic termination box mounted on a wall, neutral light` | Cuadrado 1:1 | 2000 px | Caja de terminación, orden, materia técnica | Fibras brillando de forma imposible, azul saturado, fondo negro de render |
| FIN-08 | `air handling and cooling units on the roof of a technical building` | Horizontal 16:9 | 3000 px | Climatización industrial, cubierta técnica, cielo real | Cielo reemplazado, HDR, marcas de fabricante |

---

## 7. OPERACIONES Y COMERCIO

Destino: hero de `business-infrastructure/`, `trade-financial/` (rama commodities), bloques de comercialización, offtake, distribución internacional y activos productivos.
Ángulo del grupo: **la mercancía se mueve.** Logística real, no ilustración de comercio global.

| ID | Consulta | Orientación | Res. mín. | Debe aparecer en el encuadre | NO debe aparecer |
|---|---|---|---|---|---|
| OPE-01 | `container terminal at dawn, stacked containers, gantry cranes, wide` | Horizontal 21:9 | 4000 px | Terminal real, apilamiento, grúas pórtico, primera luz | Logotipos de naviera legibles, cielo sustituido, saturación de postal |
| OPE-02 | `bulk cargo conveyor loading aggregates into a hold` | Horizontal 3:2 | 3000 px | Cinta transportadora, material a granel, polvo | Marca del operador, personas identificables |
| OPE-03 | `warehouse aisle with palletised goods and a forklift, industrial lighting` | Horizontal 16:9 | 3000 px | Pasillo de almacén, palés, carretilla en uso | Etiquetas legibles, marcas de producto, cajas de consumo reconocibles |
| OPE-04 | `truck loading dock in operation, daytime, wide shot` | Horizontal 3:2 | 3000 px | Muelle de carga, camión atracado, actividad | Matrículas legibles, rotulación de flota, conductor identificable |
| OPE-05 | `agricultural harvest being loaded onto a trailer in a field` | Horizontal 3:2 | 3000 px | Cosecha real, remolque, trabajo agrícola a media distancia | Rostros en primer plano, marca de maquinaria, cielo HDR |
| OPE-06 | `mineral stockpile with a wheel loader, industrial site, overcast` | Horizontal 16:9 | 3600 px | Acopio de mineral, pala cargadora, luz plana | Marca de la maquinaria, cartel de la explotación, personas identificables |
| OPE-07 | `sacks of commodity goods stacked in a storage building` | Cuadrado 1:1 | 2400 px | Sacos apilados, textura de arpillera, almacén | Texto impreso legible, nombre de país u origen, banderas |
| OPE-08 | `port crane and ship hull from below, industrial detail, grey sky` | Vertical 4:5 | 3000 px | Escala industrial, casco, grúa, cielo neutro | Nombre del buque, bandera, logotipo, atardecer coloreado |
| OPE-09 | `weighbridge and control cabin at an industrial site entrance` | Horizontal 3:2 | 2400 px | Báscula, caseta de control, acceso industrial | Rótulos legibles, cámaras identificables, personal |

---

## 8. RESUMEN DE LA BÚSQUEDA

| Grupo | Consultas | Destino principal | Selección objetivo |
|---|---:|---|---:|
| Residencias | 9 | `H-03a`, catálogo residencial | 3 |
| Hospitality | 9 | `H-03b`, catálogo hospitality, I-11a | 3 |
| Suelo y desarrollos | 10 | `H-03c`, `H-05`, catálogo suelo/proyectos, I-11b | 4 |
| Capital y estructuración | 9 | `H-06`, `H-10`, `H-12`, deal room, I-11c | 4 |
| Relocalización | 8 | `corporate-services/`, I-11d | 2 |
| Infraestructura financiera | 8 | `H-08`, `trade-financial/` | 2 |
| Operaciones y comercio | 9 | `business-infrastructure/`, commodities | 2 |
| **Total** | **62** | | **20** |

Ratio de trabajo esperado: **≈ 25 candidatas descargadas por cada 1 seleccionada.** Con 62 consultas se revisan ~500 imágenes para quedarse con ~20. Ese ratio no es exceso de celo: es lo que separa este material del que hay hoy en el sitio.

---

## 9. CRITERIOS DE RECHAZO (FASE 6)

**Descarte inmediato, sin apelación.** Una sola marca de esta lista invalida la candidata. Se inspecciona **al 100 % y al 400 %**, no en la miniatura.

| # | Criterio | Cómo se detecta |
|---|---|---|
| 1 | **Piel artificial** | Textura plástica, poro ausente, transiciones sin vello, brillo uniforme, orejas y dientes fundidos. Firma de IA y de retoque excesivo. |
| 2 | **Arquitectura deformada** | Líneas que no cierran, forjados que cambian de grosor, escaleras que no llegan, barandillas que se fusionan con el muro, columnas de sección variable. |
| 3 | **Ventanas inconsistentes** | Retícula de huecos que no repite, marcos de anchos distintos en la misma fachada, un piso con más ventanas que el de al lado sin razón, cristales con reflejos de escenas distintas. |
| 4 | **Reflejos imposibles** | Agua que refleja algo que no está en el encuadre, cristal que refleja una fuente de luz inexistente, sombras en dos direcciones. |
| 5 | **Vegetación repetida** | El mismo árbol o arbusto clonado en el mismo plano, patrón de copas que se repite a intervalos regulares, textura de hoja idéntica en toda la superficie. |
| 6 | **Manos incorrectas** | Nº de dedos, longitud, articulaciones, agarre imposible, dos manos con anatomía distinta. Motivo principal de rechazo en cualquier plano con gesto. |
| 7 | **Cielos artificiales** | Cielo pegado con recorte visible en el contorno, banda de halo alrededor de edificios, iluminación del cielo incoherente con la del sujeto, nubes de biblioteca reconocibles. |
| 8 | **HDR exagerado** | Halos claros en los contornos oscuros, texturas de piedra "de cómic", cielos morados, sombras sin negro, micro-contraste hipertrofiado. |
| 9 | **Saturación extrema** | Turquesas y verdes fuera de gama, pieles anaranjadas, cielos cian; cualquier canal recortado en el histograma. |
| 10 | **Lujo vulgar** | Oro, mármol brillante, champán, yates, coches deportivos, joyería, modelos posando. Contradice frontalmente la línea editorial de XARU. |
| 11 | **Composición de catálogo barato** | Sujeto centrado con espacio muerto simétrico, gran vacío a un lado "para poner el texto", encuadre de folleto inmobiliario estadounidense, gran angular deformando el salón. |
| 12 | **Logos** | Cualquier marca de tercero reconocible: hotel, promotor, aerolínea, coche, maquinaria, software, naviera. Incluye logotipos de plantilla como `text-logo.svg`. |
| 13 | **Texto incrustado** | Rótulos, cifras, direcciones, señalética legible, precios, "Price upon application" quemado. Todo texto es HTML por i18n y accesibilidad. |
| 14 | **Marcas de agua** | Cualquier watermark, incluida la del propio proveedor: significa que se descargó la vista previa, no el original licenciado. |

**Nota operativa.** Los criterios 1-7 son los que hoy delatan los 15 archivos de `assets/img/xaru/gen2/`. Aplicar esta lista al material existente produce el mismo veredicto que la Fase 1: retirada total.

---

## 10. LOS 15 CRITERIOS DE EVALUACIÓN EDITORIAL

Se aplican **después** del filtro de rechazo, a las candidatas que hayan sobrevivido. Puntuación **0-5** por criterio. **Umbral de selección: ≥ 55/75 y ningún criterio por debajo de 3.** Los criterios 1, 2 y 15 son eliminatorios: un 0 en cualquiera de ellos descarta la imagen sea cual sea el total.

| # | Criterio | Qué se juzga | 0 | 5 |
|---:|---|---|---|---|
| 1 | **Veracidad documental** *(eliminatorio)* | ¿Es una fotografía de algo que existió delante de una cámara? | Sintética o dudosa | Documental verificable, con autor y fecha |
| 2 | **Correspondencia con el texto** *(eliminatorio)* | ¿Muestra lo que el bloque afirma? | Contradice el texto | Documenta el texto |
| 3 | **Nivel de concreción** | ¿Representa una categoría o insinúa un activo concreto? | Se lee como una oferta | Inequívocamente categoría |
| 4 | **Silencio** | ¿Aporta calma o grita? | Efectista, saturada, dramática | Sobria, contenida, editorial |
| 5 | **Verdad de la luz** | ¿La luz es coherente y creíble? | Múltiples fuentes imposibles, HDR | Una lógica de luz, hora identificable |
| 6 | **Composición** | ¿La estructura del encuadre sostiene el mensaje? | Sujeto centrado sin razón, vacío muerto | Jerarquía clara, tensión en el tercio correcto |
| 7 | **Escala legible** | ¿Se entiende el tamaño de lo que se ve? | Sin referencia, imposible dimensionar | Referencia de escala natural e integrada |
| 8 | **Materia** | ¿Se lee la textura (piedra, madera, hormigón, papel, metal)? | Superficies planas y limpias de render | Materia con historia y grano |
| 9 | **Ausencia de cliché** | ¿Evita la imagen que ya está en todas partes? | Apretón de manos, llave, atardecer | Punto de vista propio |
| 10 | **Calidad técnica** | Nitidez en el plano correcto, ruido controlado, sin aberración ni moiré | Blanda, con artefactos de compresión | Limpia a 100 %, nítida donde importa |
| 11 | **Resolución y encuadre útil** | ¿Aguanta el ancho completo y admite recorte 4:5 sin perder el sujeto? | Se queda corta o pierde el sujeto al recortar | Original amplio, recorte vertical viable |
| 12 | **Consistencia con la paleta** | ¿Convive en la tira de contacto con las demás seleccionadas? | Salta del conjunto | Pertenece al mismo mundo |
| 13 | **Limpieza de derechos** | Licencia comercial verificable, model/property release cuando aplique, sin logos ni personas identificables sin cesión | Origen o derechos dudosos | Licencia y releases registrados |
| 14 | **Neutralidad geográfica y cultural** | ¿Evita fijar una jurisdicción o cultura que XARU no ha declarado? | Sitúa el negocio donde no está | Legible en EN/ES/AR/ZH sin fricción |
| 15 | **Alt escribible sin mentir** *(eliminatorio)* | ¿Se puede describir la imagen con honestidad y que siga sirviendo al bloque? | El alt honesto revela que la imagen no encaja | El alt honesto refuerza el bloque |

**Prueba final del criterio 15** — la más rápida y la más severa: escribe el `alt` en una sola frase, sin adjetivos, describiendo sólo lo que se ve. Si esa frase deja el bloque en evidencia, **la imagen es el problema, no el alt**.
