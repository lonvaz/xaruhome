# XARU HOME — Opportunities data model (`opportunities.json`)

Phase 1 deliverable. The opportunity data is **separated from the HTML**
(DERROTERO §10) so that Phase 2 templates can render the three catalogs and the
ficha (listing) models from a single source. Figures here are **illustrative
seeds**, never verified regulatory or financial data (see §7 capability matrix).

## Top-level shape

```
{
  version, phase, generatedNote,
  catalogs:      { <catalogKey>: { label{en,es,ar,zh}, search[] } },
  fichaModels:   [ "residential", "commercial-hospitality",
                   "land-development", "confidential-teaser", "productive-asset" ],
  statuses:      { <statusKey>: { en, es, ar, zh } },
  opportunities: [ <opportunity>, … ]
}
```

## The three catalogs (`catalog`, §5)

| key | contains | search facets |
|---|---|---|
| `private-properties` | villas, mansions, estates, castles, islands, residences | location, price, lifestyle, bedrooms, area |
| `commercial-hospitality` | hotels, resorts, income commercial, operating assets | assetType, operatingState, structure, region, ticket |
| `land-projects` | land, master plans, halted projects, JV, capital | area, phase, permits, use, capitalRequired, opportunity |

## Ficha (listing) models (`model`, §5 — 5 models)

1. **`residential`** — `location`, `price`, `specs{bedrooms,bathrooms,builtAreaSqm,plotAreaSqm,style}`.
2. **`commercial-hospitality`** — adds `operating{state,keys,occupancyTeaser,noiTeaser,operator,structure}` and `ticket{band}`. P&L / occupancy are **teasers only**.
3. **`land-development`** — `land{areaSqm,tenure,currentUse,projectedUse,access,water,environmental,planning,permits,phase,counterpartySought[],capitalRequired}`.
4. **`confidential-teaser`** — `teaser{teaserOnly,summary{4-lang},masked[],dealRoomProcess[]}`; owner / coordinates / financials / licenses / price are **masked**, released only through the Private Deal Room.
5. **`productive-asset`** *(Phase 4 — commodities / productive assets)* —
   `productive{category{4-lang},scale{4-lang},permitsTeaser{4-lang},productionTeaser{4-lang},offtakeTeaser{4-lang},oppType{4-lang},phase,counterpartySought[]}`.
   **Teaser format only**: region, category, scale, status, opportunity type.
   Owner, coordinates, licence numbers, volumes, contracts and price are **never
   published** — they are released only under NDA through the Private Deal Room
   route (`region`-level location, `price.display:"Undisclosed"`,
   `confidential:true`). Typical statuses: `in-validation`, `seeking-buyer`,
   `seeking-operator`, `operational`. Rendered fichas link from the
   Trade & Financial Infrastructure pillar (subdivision A).

## Every opportunity — required fields

| field | required | notes |
|---|---|---|
| `id` | yes | stable kebab-case slug |
| `catalog` | yes | one of the three catalog keys |
| `model` | yes | one of `fichaModels` |
| `status` | yes | one of the **mandatory statuses** below |
| `title` | yes | `{en,es,ar,zh}` — localised; brand/ASHIMA never translated |
| `location` | yes | `{country,region,city}`; `Undisclosed`/`null` for confidential |
| `price` | yes | `{display,currency,poa}`; `display:"Price upon application"` when `poa:true` |
| `images` | yes | asset-relative paths (reuse `assets/img/xaru/gen2/*`) |
| `mandate` | yes | `open` \| `exclusive` \| `confidential` |
| `confidential` | yes | boolean |
| `tags` | no | free-form facets |
| `secondaryStatus` | no | additional states an opportunity carries at once (e.g. a halted asset that is also `seeking-capital`) |
| model block | yes | `specs` / `operating`+`ticket` / `land` / `teaser` per `model` |

## Mandatory statuses (`status` / `secondaryStatus`, §5)

Never publish as "Available" what is still being validated. Canonical keys → labels in `statuses`:

`available` · `off-market` · `exclusive-mandate` · `open-mandate` ·
`in-validation` · `seeking-capital` · `seeking-buyer` · `seeking-developer` ·
`seeking-operator` · `development-ready` · `under-construction` ·
`halted-restructuring` · `operational` · `under-negotiation` · `closed`

## Private Market / Deal Room flow (`teaser.dealRoomProcess`)

`public-teaser → access-request → identity-verification → nda → kyc-aml →
internal-approval → data-room → adviser-assignment → transaction`

Lets XARU show that significant opportunities exist **without** revealing owners,
coordinates, financials, licenses, legal documents or sensitive price.

## Seed contents (Phase 1)

12 opportunities across all three catalogs and all four ficha models, with
varied statuses: `exclusive-mandate`, `available`, `off-market`,
`under-negotiation`, `operational`, `halted-restructuring`, `seeking-operator`,
`development-ready`, `in-validation` (+ `seeking-capital`, `seeking-developer`,
`seeking-buyer` as secondary). Images reuse the existing `gen2` set
(Samaná island, 11M m² land, resort, hotel, city villas, ASHIMA master plan).

## Phase 4 addition

`pa-quarry-license` — first `productive-asset` seed (quarry licence with permits,
`in-validation` + `seeking-buyer`, teaser only, detail under NDA), in the
`land-projects` catalog so it renders in Land, Projects & Opportunities and in
its own ficha at `/opportunities/pa-quarry-license/`.
