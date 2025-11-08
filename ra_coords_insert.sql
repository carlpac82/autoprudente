-- Comandos SQL para inserir coordenadas do RA no PostgreSQL do Render
-- Copie e cole estes comandos no Render Shell ou em um cliente PostgreSQL

-- Limpar coordenadas antigas
DELETE FROM rental_agreement_coordinates;

-- Inserir coordenadas do mapeamento local
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('address', 13.0, 271.0, 261.5, 12.34, 1, 'text', 1, CURRENT_TIMESTAMP);
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('clientEmail', 109.0, 351.5, 165.0, 12.69, 1, 'text', 1, CURRENT_TIMESTAMP);
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('clientName', 14.0, 96.5, 261.0, 10.0, 1, 'text', 1, CURRENT_TIMESTAMP);
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('clientPhone', 13.0, 351.5, 86.0, 10.5, 1, 'text', 1, CURRENT_TIMESTAMP);
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('contractNumber', 483.5, 56.0, 83.5, 12.0, 1, 'text', 1, CURRENT_TIMESTAMP);
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('country', 12.0, 128.5, 92.5, 12.5, 1, 'text', 1, CURRENT_TIMESTAMP);
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('pickupDate', 292.5, 210.5, 66.5, 12.52, 1, 'date', 1, CURRENT_TIMESTAMP);
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('pickupLocation', 292.0, 182.5, 139.5, 12.19, 1, 'text', 1, CURRENT_TIMESTAMP);
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('pickupTime', 293.0, 237.5, 67.5, 13.86, 1, 'text', 1, CURRENT_TIMESTAMP);
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('postalCodeCity', 13.0, 284.5, 261.5, 12.34, 1, 'text', 1, CURRENT_TIMESTAMP);
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('returnDate', 442.5, 210.0, 68.5, 13.69, 1, 'date', 1, CURRENT_TIMESTAMP);
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('returnLocation', 442.5, 182.5, 137.5, 11.5, 1, 'text', 1, CURRENT_TIMESTAMP);
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('returnTime', 442.5, 237.5, 65.5, 13.86, 1, 'text', 1, CURRENT_TIMESTAMP);
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('vehicleBrandModel', 292.0, 96.0, 139.0, 12.02, 1, 'text', 1, CURRENT_TIMESTAMP);
INSERT INTO rental_agreement_coordinates (field_id, x, y, width, height, page, field_type, template_version, created_at) VALUES ('vehiclePlate', 442.0, 96.5, 139.5, 10.5, 1, 'text', 1, CURRENT_TIMESTAMP);

-- Verificar inserção
SELECT field_id, x, y FROM rental_agreement_coordinates ORDER BY field_id;
