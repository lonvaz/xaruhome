-- =====================================================================
-- XARU HOME — esquema canónico de la plataforma inmobiliaria
-- =====================================================================
-- Escrito en SQL portable: se ejecuta hoy sobre SQLite (modo simulación,
-- sin servidor) y migra a PostgreSQL cambiando únicamente los tipos
-- marcados con -- PG:. Ninguna tabla es de mentira: es el modelo real que
-- la plataforma usará cuando se contraten los servicios.
--
-- Convenciones
--   · identificadores internos: TEXT con ULID/UUIDv7 ordenable  -- PG: uuid
--   · public_id no secuencial para URLs
--   · dinero: enteros en la unidad mínima (céntimos) + moneda ISO-4217.
--     Nunca float. -- PG: numeric(19,4) si se prefiere decimal
--   · fechas: ISO-8601 UTC en TEXT           -- PG: timestamptz
--   · toda tabla de negocio lleva tenant_id: el aislamiento es del modelo,
--     no de la interfaz
--   · is_demo marca el inventario de prueba de la plataforma. No se borra
--     nunca: se filtra. Permite convivir inventario real y de muestra.
-- =====================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------- tenancy
CREATE TABLE IF NOT EXISTS tenants (
  id            TEXT PRIMARY KEY,
  name          TEXT NOT NULL,
  country_code  TEXT NOT NULL,
  data_region   TEXT NOT NULL DEFAULT 'eu',
  created_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS organizations (
  id             TEXT PRIMARY KEY,
  tenant_id      TEXT NOT NULL REFERENCES tenants(id),
  public_id      TEXT NOT NULL UNIQUE,
  kind           TEXT NOT NULL CHECK (kind IN ('agency','developer','owner_professional','platform')),
  legal_name     TEXT NOT NULL,
  trade_name     TEXT NOT NULL,
  slug           TEXT NOT NULL UNIQUE,
  logo_media_id  TEXT,
  description    TEXT,
  country_code   TEXT NOT NULL,
  city           TEXT,
  website        TEXT,
  phone          TEXT,
  email          TEXT,
  licence_number TEXT,
  licence_expires_at TEXT,
  verification_status TEXT NOT NULL DEFAULT 'unverified'
                 CHECK (verification_status IN ('unverified','pending','verified','rejected','expired')),
  plan_code      TEXT,
  listing_quota  INTEGER NOT NULL DEFAULT 0,
  is_demo        INTEGER NOT NULL DEFAULT 0,
  created_at     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS branches (
  id          TEXT PRIMARY KEY,
  tenant_id   TEXT NOT NULL REFERENCES tenants(id),
  org_id      TEXT NOT NULL REFERENCES organizations(id),
  name        TEXT NOT NULL,
  city        TEXT,
  country_code TEXT,
  is_demo     INTEGER NOT NULL DEFAULT 0
);

-- ---------------------------------------------------------------- identidad
CREATE TABLE IF NOT EXISTS users (
  id            TEXT PRIMARY KEY,
  public_id     TEXT NOT NULL UNIQUE,
  email         TEXT NOT NULL UNIQUE,
  display_name  TEXT NOT NULL,
  locale        TEXT NOT NULL DEFAULT 'en',
  phone         TEXT,
  role          TEXT NOT NULL CHECK (role IN
                ('buyer','tenant_user','owner','agent','team_lead','agency_admin',
                 'finance','moderator','compliance','support','platform_admin')),
  tenant_id     TEXT REFERENCES tenants(id),
  org_id        TEXT REFERENCES organizations(id),
  mfa_enabled   INTEGER NOT NULL DEFAULT 0,
  is_demo       INTEGER NOT NULL DEFAULT 0,
  created_at    TEXT NOT NULL,
  last_seen_at  TEXT
);

CREATE TABLE IF NOT EXISTS agents (
  id             TEXT PRIMARY KEY,
  tenant_id      TEXT NOT NULL REFERENCES tenants(id),
  user_id        TEXT NOT NULL REFERENCES users(id),
  org_id         TEXT NOT NULL REFERENCES organizations(id),
  branch_id      TEXT REFERENCES branches(id),
  public_id      TEXT NOT NULL UNIQUE,
  slug           TEXT NOT NULL UNIQUE,
  display_name   TEXT NOT NULL,
  job_title      TEXT,
  bio            TEXT,
  photo_media_id TEXT,
  languages      TEXT,                 -- CSV ISO-639-1
  specialities   TEXT,                 -- CSV de subcategorías
  service_areas  TEXT,                 -- CSV de location_id
  licence_number TEXT,
  licence_expires_at TEXT,
  verification_status TEXT NOT NULL DEFAULT 'unverified',
  phone          TEXT,
  whatsapp       TEXT,
  email          TEXT,
  response_minutes_p50 INTEGER,        -- calculado, nunca inventado
  rating_avg     REAL,
  rating_count   INTEGER NOT NULL DEFAULT 0,
  status         TEXT NOT NULL DEFAULT 'active'
                 CHECK (status IN ('active','suspended','detached')),
  is_demo        INTEGER NOT NULL DEFAULT 0,
  created_at     TEXT NOT NULL
);

-- ---------------------------------------------------------------- geografía
CREATE TABLE IF NOT EXISTS locations (
  id            TEXT PRIMARY KEY,
  parent_id     TEXT REFERENCES locations(id),
  level         TEXT NOT NULL CHECK (level IN
                ('country','admin1','city','district','community','subcommunity','building','project')),
  slug          TEXT NOT NULL,
  name_en       TEXT NOT NULL,
  name_es       TEXT,
  name_ar       TEXT,
  name_zh       TEXT,
  country_code  TEXT NOT NULL,
  latitude      REAL,
  longitude     REAL,
  path          TEXT NOT NULL,         -- p. ej. es/catalonia/barcelona
  listing_count INTEGER NOT NULL DEFAULT 0,
  UNIQUE (path)
);
CREATE INDEX IF NOT EXISTS ix_locations_country ON locations(country_code);
CREATE INDEX IF NOT EXISTS ix_locations_parent  ON locations(parent_id);

-- ---------------------------------------------------------------- taxonomías
CREATE TABLE IF NOT EXISTS property_types (
  id            TEXT PRIMARY KEY,
  business_category TEXT NOT NULL CHECK (business_category IN ('residential','commercial','land')),
  slug          TEXT NOT NULL UNIQUE,
  name_en       TEXT NOT NULL, name_es TEXT, name_ar TEXT, name_zh TEXT,
  sort_order    INTEGER NOT NULL DEFAULT 0,
  is_active     INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS amenities (
  id          TEXT PRIMARY KEY,
  slug        TEXT NOT NULL UNIQUE,
  category    TEXT NOT NULL,
  name_en     TEXT NOT NULL, name_es TEXT, name_ar TEXT, name_zh TEXT,
  icon        TEXT,
  applies_to  TEXT NOT NULL DEFAULT 'residential',   -- CSV
  sort_order  INTEGER NOT NULL DEFAULT 0,
  is_active   INTEGER NOT NULL DEFAULT 1
);

-- ---------------------------------------------------------------- proyectos
CREATE TABLE IF NOT EXISTS developers (
  id          TEXT PRIMARY KEY,
  org_id      TEXT NOT NULL REFERENCES organizations(id),
  public_id   TEXT NOT NULL UNIQUE,
  slug        TEXT NOT NULL UNIQUE,
  name        TEXT NOT NULL,
  country_code TEXT NOT NULL,
  founded_year INTEGER,
  description TEXT,
  logo_media_id TEXT,
  verification_status TEXT NOT NULL DEFAULT 'unverified',
  is_demo     INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS projects (
  id             TEXT PRIMARY KEY,
  tenant_id      TEXT NOT NULL REFERENCES tenants(id),
  developer_id   TEXT NOT NULL REFERENCES developers(id),
  public_id      TEXT NOT NULL UNIQUE,
  slug           TEXT NOT NULL UNIQUE,
  name           TEXT NOT NULL,
  location_id    TEXT NOT NULL REFERENCES locations(id),
  status         TEXT NOT NULL CHECK (status IN
                 ('upcoming','launched','off_plan','under_construction','ready','sold_out')),
  launch_date    TEXT,
  handover_quarter INTEGER,
  handover_year  INTEGER,
  construction_progress_percent INTEGER,
  progress_source TEXT,
  progress_updated_at TEXT,
  price_min_minor INTEGER,
  price_max_minor INTEGER,
  currency       TEXT,
  units_total    INTEGER,
  units_available INTEGER,
  description    TEXT,
  hero_media_id  TEXT,
  is_demo        INTEGER NOT NULL DEFAULT 0,
  created_at     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS unit_types (
  id          TEXT PRIMARY KEY,
  project_id  TEXT NOT NULL REFERENCES projects(id),
  name        TEXT NOT NULL,
  bedrooms    REAL,
  bathrooms   REAL,
  area_min_sqm REAL,
  area_max_sqm REAL,
  price_min_minor INTEGER,
  price_max_minor INTEGER,
  currency    TEXT,
  units_available INTEGER
);

CREATE TABLE IF NOT EXISTS payment_plans (
  id          TEXT PRIMARY KEY,
  project_id  TEXT NOT NULL REFERENCES projects(id),
  name        TEXT NOT NULL,
  version     INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS payment_plan_milestones (
  id            TEXT PRIMARY KEY,
  plan_id       TEXT NOT NULL REFERENCES payment_plans(id),
  label         TEXT NOT NULL,
  percent       REAL NOT NULL,
  trigger_event TEXT,
  sort_order    INTEGER NOT NULL DEFAULT 0
);

-- ---------------------------------------------------------------- inventario
CREATE TABLE IF NOT EXISTS listings (
  id                TEXT PRIMARY KEY,
  public_id         TEXT NOT NULL UNIQUE,
  tenant_id         TEXT NOT NULL REFERENCES tenants(id),
  org_id            TEXT REFERENCES organizations(id),
  branch_id         TEXT REFERENCES branches(id),
  agent_id          TEXT REFERENCES agents(id),
  project_id        TEXT REFERENCES projects(id),
  unit_type_id      TEXT REFERENCES unit_types(id),
  external_reference TEXT,
  source_system     TEXT NOT NULL DEFAULT 'migration'
                    CHECK (source_system IN ('manual','api','csv','xml','migration','partner_feed')),
  version           INTEGER NOT NULL DEFAULT 1,

  -- clasificación
  business_category TEXT NOT NULL CHECK (business_category IN ('residential','commercial','land')),
  offering_type     TEXT NOT NULL CHECK (offering_type IN ('sale','rent','short_term_rent')),
  inventory_type    TEXT NOT NULL DEFAULT 'ready'
                    CHECK (inventory_type IN ('ready','off_plan_first_sale','off_plan_resale')),
  property_type_id  TEXT NOT NULL REFERENCES property_types(id),
  subtype           TEXT,

  -- localización
  location_id       TEXT NOT NULL REFERENCES locations(id),
  country_code      TEXT NOT NULL,
  admin_area_1      TEXT,
  city              TEXT,
  district          TEXT,
  community         TEXT,
  building_name     TEXT,
  unit_number_private TEXT,            -- nunca sale en el DTO público
  street_address_private TEXT,         -- nunca sale en el DTO público
  latitude          REAL,
  longitude         REAL,
  location_precision TEXT NOT NULL DEFAULT 'community'
                    CHECK (location_precision IN ('exact','building','community','approximate','confidential')),
  public_display_address TEXT,

  -- espacios
  bedrooms          REAL,
  bedroom_label     TEXT,
  bathrooms         REAL,
  maid_rooms        INTEGER,
  study_rooms       INTEGER,
  parking_spaces    INTEGER,
  floor_number      INTEGER,
  total_building_floors INTEGER,
  built_area_sqm    REAL,
  plot_area_sqm     REAL,
  hectares          REAL,
  hotel_keys        INTEGER,
  berths            INTEGER,

  -- precio
  currency          TEXT NOT NULL DEFAULT 'USD',
  price_minor       INTEGER,           -- unidad mínima; NULL si price_on_application
  price_on_application INTEGER NOT NULL DEFAULT 0,
  rent_frequency    TEXT CHECK (rent_frequency IN ('daily','weekly','monthly','yearly')),
  service_charge_minor INTEGER,
  price_per_sqm_minor  INTEGER,        -- derivado, para ordenar
  negotiable        INTEGER NOT NULL DEFAULT 0,
  financing_available INTEGER NOT NULL DEFAULT 0,

  -- disponibilidad
  available_from    TEXT,
  occupancy_status  TEXT DEFAULT 'unknown'
                    CHECK (occupancy_status IN ('vacant','owner_occupied','tenanted','unknown')),
  furnishing        TEXT DEFAULT 'unknown'
                    CHECK (furnishing IN ('furnished','unfurnished','partly_furnished','unknown')),
  condition         TEXT DEFAULT 'unknown',
  completion_status TEXT DEFAULT 'ready'
                    CHECK (completion_status IN ('ready','off_plan','under_construction')),
  handover_quarter  INTEGER,
  handover_year     INTEGER,
  ownership_type    TEXT DEFAULT 'unknown'
                    CHECK (ownership_type IN ('freehold','leasehold','usufruct','unknown')),

  -- regulación
  regulatory_jurisdiction TEXT,
  permit_number     TEXT,
  verification_status TEXT NOT NULL DEFAULT 'unverified',
  verification_expires_at TEXT,

  -- publicación y confianza
  lifecycle_status  TEXT NOT NULL DEFAULT 'DRAFT' CHECK (lifecycle_status IN
                    ('DRAFT','INCOMPLETE','SUBMITTED','AUTOMATED_REVIEW','HUMAN_REVIEW',
                     'CHANGES_REQUESTED','APPROVED','SCHEDULED','PUBLISHED','PAUSED',
                     'UNDER_OFFER','REJECTED','SUSPENDED','EXPIRED','SOLD','RENTED','ARCHIVED')),
  moderation_status TEXT NOT NULL DEFAULT 'pending',
  quality_score     INTEGER,
  promotion_tier    TEXT CHECK (promotion_tier IN ('none','featured','premium','spotlight')),
  hero_media_id     TEXT,
  published_at      TEXT,
  updated_at        TEXT,
  expires_at        TEXT,
  sold_at           TEXT,
  rented_at         TEXT,
  archived_at       TEXT,
  created_by        TEXT,
  updated_by        TEXT,
  suspension_reason_code TEXT,

  -- inventario de muestra de la plataforma
  is_demo           INTEGER NOT NULL DEFAULT 0,
  demo_label        TEXT,

  created_at        TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_listings_status   ON listings(lifecycle_status);
CREATE INDEX IF NOT EXISTS ix_listings_country  ON listings(country_code);
CREATE INDEX IF NOT EXISTS ix_listings_location ON listings(location_id);
CREATE INDEX IF NOT EXISTS ix_listings_offer    ON listings(offering_type, business_category);
CREATE INDEX IF NOT EXISTS ix_listings_price    ON listings(currency, price_minor);
CREATE INDEX IF NOT EXISTS ix_listings_agent    ON listings(agent_id);
CREATE INDEX IF NOT EXISTS ix_listings_org      ON listings(org_id);

CREATE TABLE IF NOT EXISTS listing_translations (
  listing_id  TEXT NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  locale      TEXT NOT NULL,
  title       TEXT NOT NULL,
  description TEXT,
  highlights  TEXT,
  slug        TEXT NOT NULL,
  translation_status TEXT NOT NULL DEFAULT 'human'
              CHECK (translation_status IN ('human','machine','machine_reviewed')),
  PRIMARY KEY (listing_id, locale)
);

CREATE TABLE IF NOT EXISTS media (
  id            TEXT PRIMARY KEY,
  tenant_id     TEXT,
  kind          TEXT NOT NULL CHECK (kind IN ('photo','floorplan','video','tour360','brochure','logo','avatar')),
  storage_key   TEXT NOT NULL,
  width         INTEGER,
  height        INTEGER,
  checksum      TEXT,
  perceptual_hash TEXT,
  rights        TEXT NOT NULL DEFAULT 'licensed_stock',
  moderation_status TEXT NOT NULL DEFAULT 'approved',
  created_at    TEXT
);

CREATE TABLE IF NOT EXISTS listing_media (
  listing_id  TEXT NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  media_id    TEXT NOT NULL REFERENCES media(id),
  sort_order  INTEGER NOT NULL DEFAULT 0,
  is_cover    INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (listing_id, media_id)
);

CREATE TABLE IF NOT EXISTS listing_amenities (
  listing_id  TEXT NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  amenity_id  TEXT NOT NULL REFERENCES amenities(id),
  PRIMARY KEY (listing_id, amenity_id)
);

-- historial de precio: dominio, no un JSON mutable
CREATE TABLE IF NOT EXISTS listing_price_history (
  id          TEXT PRIMARY KEY,
  listing_id  TEXT NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  currency    TEXT NOT NULL,
  price_minor INTEGER,
  changed_at  TEXT NOT NULL,
  actor       TEXT
);

-- máquina de estados: toda transición queda, con actor y motivo
CREATE TABLE IF NOT EXISTS listing_transitions (
  id            TEXT PRIMARY KEY,
  listing_id    TEXT NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  from_status   TEXT,
  to_status     TEXT NOT NULL,
  actor         TEXT NOT NULL,
  reason_code   TEXT,
  note          TEXT,
  occurred_at   TEXT NOT NULL,
  correlation_id TEXT
);

-- outbox transaccional: el evento se escribe con el agregado
CREATE TABLE IF NOT EXISTS outbox_events (
  id             TEXT PRIMARY KEY,
  event_type     TEXT NOT NULL,
  aggregate_id   TEXT NOT NULL,
  aggregate_type TEXT NOT NULL,
  aggregate_version INTEGER NOT NULL DEFAULT 1,
  tenant_id      TEXT,
  occurred_at    TEXT NOT NULL,
  producer       TEXT NOT NULL,
  correlation_id TEXT,
  causation_id   TEXT,
  schema_version INTEGER NOT NULL DEFAULT 1,
  payload        TEXT NOT NULL,
  published_at   TEXT
);
CREATE INDEX IF NOT EXISTS ix_outbox_unpublished ON outbox_events(published_at);

-- ---------------------------------------------------------------- demanda
CREATE TABLE IF NOT EXISTS leads (
  id            TEXT PRIMARY KEY,
  public_id     TEXT NOT NULL UNIQUE,
  tenant_id     TEXT NOT NULL REFERENCES tenants(id),
  listing_id    TEXT REFERENCES listings(id),
  project_id    TEXT REFERENCES projects(id),
  agent_id      TEXT REFERENCES agents(id),
  org_id        TEXT REFERENCES organizations(id),
  user_id       TEXT REFERENCES users(id),
  channel       TEXT NOT NULL CHECK (channel IN ('form','email','call','whatsapp','chat','api')),
  contact_name  TEXT,
  contact_email TEXT,                  -- cifrado en producción
  contact_phone TEXT,                  -- cifrado en producción
  message       TEXT,
  consent_given INTEGER NOT NULL DEFAULT 0,
  consent_basis TEXT,
  utm_source    TEXT, utm_medium TEXT, utm_campaign TEXT, referer TEXT,
  stage         TEXT NOT NULL DEFAULT 'new' CHECK (stage IN
                ('new','contacted','qualified','viewing','negotiation','won','lost','spam')),
  priority      TEXT NOT NULL DEFAULT 'normal',
  spam_score    REAL NOT NULL DEFAULT 0,
  budget_min_minor INTEGER, budget_max_minor INTEGER, budget_currency TEXT,
  dedupe_key    TEXT,
  sla_due_at    TEXT,
  first_response_at TEXT,
  lost_reason   TEXT,
  is_demo       INTEGER NOT NULL DEFAULT 0,
  created_at    TEXT NOT NULL,
  updated_at    TEXT
);
CREATE INDEX IF NOT EXISTS ix_leads_stage ON leads(stage);
CREATE INDEX IF NOT EXISTS ix_leads_agent ON leads(agent_id);

CREATE TABLE IF NOT EXISTS lead_activities (
  id          TEXT PRIMARY KEY,
  lead_id     TEXT NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  kind        TEXT NOT NULL,
  body        TEXT,
  actor       TEXT,
  occurred_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS favorites (
  user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  listing_id  TEXT NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  collection  TEXT NOT NULL DEFAULT 'default',
  note        TEXT,
  created_at  TEXT NOT NULL,
  PRIMARY KEY (user_id, listing_id)
);

CREATE TABLE IF NOT EXISTS saved_searches (
  id          TEXT PRIMARY KEY,
  user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name        TEXT NOT NULL,
  query_json  TEXT NOT NULL,
  canonical_url TEXT,
  created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS alert_subscriptions (
  id              TEXT PRIMARY KEY,
  saved_search_id TEXT NOT NULL REFERENCES saved_searches(id) ON DELETE CASCADE,
  user_id         TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  frequency       TEXT NOT NULL CHECK (frequency IN ('instant','daily','weekly')),
  channels        TEXT NOT NULL DEFAULT 'email',
  last_cursor     TEXT,
  active          INTEGER NOT NULL DEFAULT 1,
  created_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS viewed_listings (
  user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  listing_id  TEXT NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  viewed_at   TEXT NOT NULL,
  PRIMARY KEY (user_id, listing_id)
);

-- ---------------------------------------------------------------- moderación
CREATE TABLE IF NOT EXISTS moderation_cases (
  id          TEXT PRIMARY KEY,
  listing_id  TEXT NOT NULL REFERENCES listings(id),
  opened_at   TEXT NOT NULL,
  priority    TEXT NOT NULL DEFAULT 'normal',
  sla_due_at  TEXT,
  status      TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','in_review','decided','escalated')),
  risk_score  REAL,
  failed_rules TEXT,
  assignee    TEXT
);

CREATE TABLE IF NOT EXISTS moderation_decisions (
  id          TEXT PRIMARY KEY,
  case_id     TEXT NOT NULL REFERENCES moderation_cases(id),
  decision    TEXT NOT NULL CHECK (decision IN ('approve','reject','request_changes','suspend','escalate')),
  reason_code TEXT NOT NULL,
  note        TEXT,
  actor       TEXT NOT NULL,
  decided_at  TEXT NOT NULL
);

-- ---------------------------------------------------------------- monetización
CREATE TABLE IF NOT EXISTS plans (
  code        TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  currency    TEXT NOT NULL,
  price_minor INTEGER NOT NULL,
  period      TEXT NOT NULL DEFAULT 'month',
  listing_quota INTEGER NOT NULL,
  seat_quota  INTEGER NOT NULL,
  features    TEXT
);

CREATE TABLE IF NOT EXISTS subscriptions (
  id          TEXT PRIMARY KEY,
  org_id      TEXT NOT NULL REFERENCES organizations(id),
  plan_code   TEXT NOT NULL REFERENCES plans(code),
  status      TEXT NOT NULL DEFAULT 'active',
  started_at  TEXT NOT NULL,
  renews_at   TEXT,
  seats       INTEGER NOT NULL DEFAULT 1
);

-- ledger de doble entrada: el saldo es la suma, nunca un campo mutable
CREATE TABLE IF NOT EXISTS credit_ledger (
  id          TEXT PRIMARY KEY,
  org_id      TEXT NOT NULL REFERENCES organizations(id),
  entry_type  TEXT NOT NULL CHECK (entry_type IN
              ('purchase','allocation','reservation','consumption','release','adjustment','expiry','refund')),
  credits     INTEGER NOT NULL,        -- positivo o negativo
  reference   TEXT,
  idempotency_key TEXT UNIQUE,
  occurred_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS promotions (
  id          TEXT PRIMARY KEY,
  org_id      TEXT NOT NULL REFERENCES organizations(id),
  listing_id  TEXT NOT NULL REFERENCES listings(id),
  tier        TEXT NOT NULL CHECK (tier IN ('featured','premium','spotlight')),
  starts_at   TEXT NOT NULL,
  ends_at     TEXT NOT NULL,
  credits_spent INTEGER NOT NULL,
  status      TEXT NOT NULL DEFAULT 'active'
);

-- ---------------------------------------------------------------- auditoría
CREATE TABLE IF NOT EXISTS audit_log (
  id          TEXT PRIMARY KEY,
  actor       TEXT NOT NULL,
  action      TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id   TEXT NOT NULL,
  tenant_id   TEXT,
  context     TEXT,
  occurred_at TEXT NOT NULL
);

-- ---------------------------------------------------------------- vistas de lectura
-- Proyección pública: lo que puede salir por la API sin filtrar a mano.
-- La dirección exacta, el número de unidad y el propietario NO están aquí.
CREATE VIEW IF NOT EXISTS v_public_listings AS
SELECT
  l.id, l.public_id, l.business_category, l.offering_type, l.inventory_type,
  l.property_type_id, l.subtype, l.location_id, l.country_code, l.admin_area_1,
  l.city, l.district, l.community, l.building_name, l.latitude, l.longitude,
  l.location_precision, l.public_display_address,
  l.bedrooms, l.bedroom_label, l.bathrooms, l.parking_spaces,
  l.built_area_sqm, l.plot_area_sqm, l.hectares, l.hotel_keys, l.berths,
  l.currency, l.price_minor, l.price_on_application, l.rent_frequency,
  l.price_per_sqm_minor, l.furnishing, l.completion_status, l.ownership_type,
  l.handover_quarter, l.handover_year,
  l.verification_status, l.lifecycle_status, l.quality_score, l.promotion_tier,
  l.hero_media_id, l.published_at, l.updated_at, l.sold_at,
  l.agent_id, l.org_id, l.project_id, l.is_demo, l.demo_label
FROM listings l
WHERE l.lifecycle_status IN ('PUBLISHED','UNDER_OFFER','SOLD','RENTED');
