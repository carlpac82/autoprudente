-- Script para criar tabelas de Damage Reports no PostgreSQL
-- Executar no Render Shell: psql $DATABASE_URL < create_damage_reports_tables.sql

-- Tabela principal de Damage Reports
CREATE TABLE IF NOT EXISTS damage_reports (
    id SERIAL PRIMARY KEY,
    dr_number TEXT UNIQUE,
    ra_number TEXT,
    contract_number TEXT,
    date DATE,
    client_name TEXT,
    client_email TEXT,
    client_phone TEXT,
    client_address TEXT,
    client_city TEXT,
    client_postal_code TEXT,
    client_country TEXT,
    vehicle_plate TEXT,
    vehicle_model TEXT,
    vehicle_brand TEXT,
    pickup_date TIMESTAMP,
    pickup_time TEXT,
    pickup_location TEXT,
    return_date TIMESTAMP,
    return_time TEXT,
    return_location TEXT,
    issued_by TEXT,
    inspection_type TEXT,
    inspector_name TEXT,
    mileage INTEGER,
    fuel_level TEXT,
    damage_description TEXT,
    observations TEXT,
    damage_diagram_data TEXT,
    repair_items TEXT,
    damage_images TEXT,
    total_amount REAL,
    status TEXT DEFAULT 'draft',
    pdf_data BYTEA,
    pdf_filename TEXT,
    is_protected INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de coordenadas de campos do PDF
CREATE TABLE IF NOT EXISTS damage_report_coordinates (
    id SERIAL PRIMARY KEY,
    field_id TEXT NOT NULL,
    x REAL NOT NULL,
    y REAL NOT NULL,
    width REAL NOT NULL,
    height REAL NOT NULL,
    page INTEGER DEFAULT 1,
    field_type TEXT,
    template_version INTEGER DEFAULT 1,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de templates PDF
CREATE TABLE IF NOT EXISTS damage_report_templates (
    id SERIAL PRIMARY KEY,
    version INTEGER NOT NULL,
    filename TEXT NOT NULL,
    file_data BYTEA NOT NULL,
    num_pages INTEGER,
    uploaded_by TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER DEFAULT 0,
    notes TEXT
);

-- Tabela de histórico de mapeamentos
CREATE TABLE IF NOT EXISTS damage_report_mapping_history (
    id SERIAL PRIMARY KEY,
    template_version INTEGER NOT NULL,
    field_id TEXT NOT NULL,
    x REAL NOT NULL,
    y REAL NOT NULL,
    width REAL NOT NULL,
    height REAL NOT NULL,
    page INTEGER DEFAULT 1,
    field_type TEXT,
    mapped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mapped_by TEXT
);

-- Tabela de numeração automática
CREATE TABLE IF NOT EXISTS damage_report_numbering (
    id SERIAL PRIMARY KEY,
    current_year INTEGER NOT NULL,
    current_number INTEGER NOT NULL,
    prefix TEXT DEFAULT 'DR',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir configuração inicial de numeração (se não existir)
INSERT INTO damage_report_numbering (id, current_year, current_number, prefix)
VALUES (1, 2025, 40, 'DR')
ON CONFLICT (id) DO NOTHING;

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_dr_number ON damage_reports(dr_number);
CREATE INDEX IF NOT EXISTS idx_dr_created_at ON damage_reports(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_dr_is_protected ON damage_reports(is_protected);

\echo '✅ Tabelas de Damage Reports criadas com sucesso!'
