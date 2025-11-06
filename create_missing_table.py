"""
Script para criar a tabela damage_report_mapping_history no PostgreSQL
Execute uma vez após o deploy
"""

import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL') or "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

try:
    print("🔗 Conectando ao PostgreSQL...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    print("📋 Criando tabela damage_report_mapping_history...")
    cursor.execute("""
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
            mapped_by TEXT,
            mapped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    
    # Verificar se foi criada
    cursor.execute("""
        SELECT COUNT(*) FROM information_schema.tables 
        WHERE table_name = 'damage_report_mapping_history'
    """)
    
    exists = cursor.fetchone()[0]
    
    if exists > 0:
        print("✅ Tabela damage_report_mapping_history criada com sucesso!")
        
        # Ver estrutura
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'damage_report_mapping_history'
            ORDER BY ordinal_position
        """)
        
        print("\n📊 Estrutura da tabela:")
        for col_name, data_type in cursor.fetchall():
            print(f"  - {col_name}: {data_type}")
    else:
        print("❌ Erro: Tabela não foi criada")
    
    cursor.close()
    conn.close()
    
    print("\n✅ Script concluído!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
