"""
Restaurar Damage Reports do backup SQLite local para PostgreSQL no Render
"""

import sqlite3
import psycopg2

# Conectar ao SQLite local (backup)
sqlite_conn = sqlite3.connect('data.db')
sqlite_conn.row_factory = sqlite3.Row
sqlite_cursor = sqlite_conn.cursor()

# Conectar ao PostgreSQL do Render (URL direta)
DATABASE_URL = "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

pg_conn = psycopg2.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

print("📋 Restaurando Damage Reports...")
print("=" * 60)

# Buscar todos os DRs do SQLite (exceto os inválidos 1:2025, 2:2025, 3:2025)
sqlite_cursor.execute("""
    SELECT * FROM damage_reports 
    WHERE dr_number NOT IN ('1:2025', '2:2025', '3:2025')
    ORDER BY dr_number
""")

rows = sqlite_cursor.fetchall()
print(f"📊 Encontrados {len(rows)} DRs no backup local")
print()

restored = 0
skipped = 0
errors = []

for row in rows:
    dr_number = row['dr_number']
    
    try:
        # Verificar se já existe no PostgreSQL
        pg_cursor.execute("SELECT COUNT(*) FROM damage_reports WHERE dr_number = %s", (dr_number,))
        exists = pg_cursor.fetchone()[0] > 0
        
        if exists:
            print(f"⏭️  {dr_number} - Já existe, pulando...")
            skipped += 1
            continue
        
        # Inserir no PostgreSQL (usando apenas campos que existem no backup)
        pg_cursor.execute("""
            INSERT INTO damage_reports (
                dr_number, ra_number, contract_number, date,
                client_name, client_email, client_phone,
                client_address, client_city, client_postal_code,
                vehicle_plate, vehicle_model, vehicle_brand,
                pickup_date, pickup_location,
                return_date, return_location,
                inspection_type, inspector_name,
                mileage, fuel_level, damage_description, observations,
                damage_diagram_data, repair_items,
                total_amount, status, pdf_data, pdf_filename,
                is_protected, created_at, created_by, updated_at
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s,
                %s, %s,
                %s, %s,
                %s, %s, %s, %s,
                %s, %s,
                %s, %s, %s, %s,
                1, %s, %s, %s
            )
        """, (
            row['dr_number'], row['ra_number'], row['contract_number'], row['date'],
            row['client_name'], row['client_email'], row['client_phone'],
            row['client_address'], row['client_city'], row['client_postal_code'],
            row['vehicle_plate'], row['vehicle_model'], row['vehicle_brand'],
            row['pickup_date'], row['pickup_location'],
            row['return_date'], row['return_location'],
            row['inspection_type'], row['inspector_name'],
            row['mileage'], row['fuel_level'], row['damage_description'], row['observations'],
            row['damage_diagram_data'], row['repair_items'],
            row['total_amount'], row['status'], row['pdf_data'], row['pdf_filename'],
            row['created_at'], row['created_by'], row['updated_at']
        ))
        
        pg_conn.commit()
        print(f"✅ {dr_number} - Restaurado com sucesso!")
        restored += 1
        
    except Exception as e:
        error_msg = f"{dr_number}: {str(e)}"
        errors.append(error_msg)
        print(f"❌ {dr_number} - ERRO: {e}")
        pg_conn.rollback()

print()
print("=" * 60)
print("📊 RESUMO:")
print(f"✅ Restaurados: {restored}")
print(f"⏭️  Já existiam: {skipped}")
print(f"❌ Erros: {len(errors)}")

if errors:
    print()
    print("ERROS:")
    for error in errors:
        print(f"  - {error}")

# Fechar conexões
sqlite_conn.close()
pg_conn.close()

print()
print("✅ Restauração concluída!")
