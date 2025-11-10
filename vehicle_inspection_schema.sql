-- ============================================================
-- VEHICLE INSPECTION SYSTEM - COMPLETE SCHEMA
-- Check-in/Check-out with AI Damage Detection
-- ============================================================

-- Main inspections table
CREATE TABLE IF NOT EXISTS vehicle_inspections (
    id SERIAL PRIMARY KEY,
    
    -- Inspection basics
    inspection_number VARCHAR(50) UNIQUE NOT NULL,  -- VI-2025-001
    inspection_type VARCHAR(20) NOT NULL,           -- 'check_in' or 'check_out'
    inspection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Vehicle & Contract info
    vehicle_plate VARCHAR(20) NOT NULL,
    vehicle_brand VARCHAR(50),
    vehicle_model VARCHAR(50),
    contract_number VARCHAR(50),
    
    -- Customer info
    customer_name VARCHAR(200),
    customer_email VARCHAR(200),
    customer_phone VARCHAR(50),
    
    -- Inspector
    inspector_name VARCHAR(100) NOT NULL,
    inspector_email VARCHAR(200),
    
    -- Damage assessment
    has_damage BOOLEAN DEFAULT FALSE,
    damage_count INTEGER DEFAULT 0,
    damage_severity VARCHAR(20),  -- 'none', 'minor', 'moderate', 'severe'
    
    -- AI Results Summary
    ai_analysis_complete BOOLEAN DEFAULT FALSE,
    ai_confidence_avg DECIMAL(5,2),
    ai_damages_detected TEXT,  -- JSON array of damage types
    
    -- Notes
    inspector_notes TEXT,
    damage_description TEXT,
    
    -- Photos (we'll store photo IDs in separate table)
    photo_count INTEGER DEFAULT 0,
    
    -- Odometer
    odometer_reading INTEGER,
    fuel_level VARCHAR(20),  -- 'empty', '1/4', '1/2', '3/4', 'full'
    
    -- Status
    status VARCHAR(20) DEFAULT 'draft',  -- 'draft', 'completed', 'reviewed'
    
    -- Linked inspection (for check-out to reference check-in)
    linked_inspection_id INTEGER REFERENCES vehicle_inspections(id),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_plate (vehicle_plate),
    INDEX idx_contract (contract_number),
    INDEX idx_type (inspection_type),
    INDEX idx_date (inspection_date)
);

-- Photos table (stores actual photos)
CREATE TABLE IF NOT EXISTS inspection_photos (
    id SERIAL PRIMARY KEY,
    
    inspection_id INTEGER NOT NULL REFERENCES vehicle_inspections(id) ON DELETE CASCADE,
    
    -- Photo info
    photo_type VARCHAR(50) NOT NULL,  -- 'front', 'back', 'left', 'right', 'interior', 'odometer', 'damage_detail'
    photo_order INTEGER DEFAULT 0,
    
    -- Image data
    image_data BYTEA NOT NULL,
    image_filename VARCHAR(200),
    image_size INTEGER,
    image_format VARCHAR(10),  -- 'jpg', 'png', 'webp'
    
    -- AI Analysis for this photo
    ai_analyzed BOOLEAN DEFAULT FALSE,
    ai_has_damage BOOLEAN DEFAULT FALSE,
    ai_damage_type VARCHAR(50),
    ai_confidence DECIMAL(5,2),
    ai_result JSON,  -- Full AI result
    
    -- Location on vehicle (optional - for damage mapping)
    damage_location VARCHAR(100),  -- 'front_bumper', 'door_left', etc.
    damage_coordinates JSON,  -- {x, y, width, height} for marking on photo
    
    -- Notes
    photo_notes TEXT,
    
    -- Metadata
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_inspection (inspection_id),
    INDEX idx_type (photo_type)
);

-- Damage items table (detailed damage list)
CREATE TABLE IF NOT EXISTS inspection_damages (
    id SERIAL PRIMARY KEY,
    
    inspection_id INTEGER NOT NULL REFERENCES vehicle_inspections(id) ON DELETE CASCADE,
    photo_id INTEGER REFERENCES inspection_photos(id),
    
    -- Damage details
    damage_type VARCHAR(50) NOT NULL,  -- 'DENT', 'SCRATCH', 'CRACK', etc.
    damage_severity VARCHAR(20),  -- 'minor', 'moderate', 'severe'
    damage_location VARCHAR(100),
    damage_size VARCHAR(50),  -- 'small', 'medium', 'large'
    
    -- Detection
    detected_by VARCHAR(20),  -- 'ai', 'manual', 'both'
    ai_confidence DECIMAL(5,2),
    
    -- Cost estimation (optional)
    estimated_cost DECIMAL(10,2),
    
    -- Description
    description TEXT,
    
    -- New damage? (only on check-out)
    is_new_damage BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_inspection (inspection_id)
);

-- Inspection comparisons (check-in vs check-out)
CREATE TABLE IF NOT EXISTS inspection_comparisons (
    id SERIAL PRIMARY KEY,
    
    checkin_inspection_id INTEGER NOT NULL REFERENCES vehicle_inspections(id),
    checkout_inspection_id INTEGER NOT NULL REFERENCES vehicle_inspections(id),
    
    -- Comparison results
    new_damages_count INTEGER DEFAULT 0,
    new_damages_list TEXT,  -- JSON array
    total_damage_cost DECIMAL(10,2),
    
    -- Responsibility
    customer_responsible BOOLEAN DEFAULT FALSE,
    insurance_claim BOOLEAN DEFAULT FALSE,
    
    -- Notes
    comparison_notes TEXT,
    
    -- PDF Report
    report_pdf BYTEA,
    report_filename VARCHAR(200),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_checkin (checkin_inspection_id),
    INDEX idx_checkout (checkout_inspection_id)
);

-- Inspection templates (standard photo angles)
CREATE TABLE IF NOT EXISTS inspection_templates (
    id SERIAL PRIMARY KEY,
    
    template_name VARCHAR(100) NOT NULL,
    template_description TEXT,
    
    -- Required photos
    required_photos JSON,  -- ['front', 'back', 'left', 'right', 'interior', 'odometer']
    
    -- Instructions for each photo
    photo_instructions JSON,
    
    is_default BOOLEAN DEFAULT FALSE,
    active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default template
INSERT INTO inspection_templates (template_name, template_description, required_photos, photo_instructions, is_default, active)
VALUES (
    'Standard 6-Point Inspection',
    'Standard vehicle inspection with 6 required photos',
    '["front", "back", "left", "right", "interior", "odometer"]'::JSON,
    '{
        "front": "Take photo from front center, include license plate and entire front",
        "back": "Take photo from rear center, include license plate and entire back", 
        "left": "Take photo from left side, include all doors and wheels",
        "right": "Take photo from right side, include all doors and wheels",
        "interior": "Take photo of interior, focus on seats and dashboard condition",
        "odometer": "Clear photo of odometer showing mileage"
    }'::JSON,
    true,
    true
)
ON CONFLICT DO NOTHING;
