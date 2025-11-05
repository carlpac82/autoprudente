#!/usr/bin/env python3
"""
Script para verificar e corrigir estrutura da tabela price_snapshots
"""

import os
import psycopg2

def fix_price_snapshots():
    """Verificar e corrigir estrutura da tabela price_snapshots"""
    
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL não encontrado!")
        return False
    
    try:
        print("=" * 80)
        print("🔧 VERIFICANDO TABELA price_snapshots")
        print("=" * 80)
        print()
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'price_snapshots'
            )
        """)
        exists = cursor.fetchone()[0]
        
        if not exists:
            print("❌ Tabela price_snapshots não existe!")
            print("   Criando tabela...")
            cursor.execute("""
                CREATE TABLE price_snapshots (
                    id SERIAL PRIMARY KEY,
                    location TEXT NOT NULL,
                    pickup_date TEXT NOT NULL,
                    days INTEGER NOT NULL,
                    car TEXT NOT NULL,
                    "group" TEXT,
                    supplier TEXT,
                    price REAL,
                    snapshot_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    search_id TEXT
                )
            """)
            conn.commit()
            print("✅ Tabela criada!")
            return True
        
        # Get current columns
        print("📋 Verificando estrutura atual...")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'price_snapshots'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        
        print("\n📊 Colunas atuais:")
        for col_name, col_type in columns:
            print(f"   - {col_name} ({col_type})")
        
        # Check for missing columns
        required_columns = {
            'location': 'TEXT',
            'pickup_date': 'TEXT',
            'days': 'INTEGER',
            'car': 'TEXT',
            'group': 'TEXT',
            'supplier': 'TEXT',
            'price': 'REAL',
            'snapshot_time': 'TIMESTAMP',
            'search_id': 'TEXT'
        }
        
        existing_cols = {col[0] for col in columns}
        missing_cols = set(required_columns.keys()) - existing_cols
        
        if missing_cols:
            print(f"\n⚠️  Colunas em falta: {missing_cols}")
            print("\n🔧 Adicionando colunas...")
            
            for col_name in missing_cols:
                col_type = required_columns[col_name]
                try:
                    if col_name == 'group':
                        # Group is a reserved keyword, needs quotes
                        cursor.execute(f'ALTER TABLE price_snapshots ADD COLUMN "group" {col_type}')
                    else:
                        cursor.execute(f'ALTER TABLE price_snapshots ADD COLUMN {col_name} {col_type}')
                    print(f"   ✅ Coluna {col_name} adicionada")
                except Exception as e:
                    print(f"   ⚠️  Erro ao adicionar {col_name}: {e}")
                    conn.rollback()
            
            conn.commit()
        else:
            print("\n✅ Todas as colunas necessárias existem!")
        
        # Create indexes if they don't exist
        print("\n📊 Criando índices...")
        indexes = [
            ("idx_snapshots_location", "location"),
            ("idx_snapshots_date", "pickup_date"),
            ("idx_snapshots_group", '"group"')
        ]
        
        for idx_name, col_name in indexes:
            try:
                cursor.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON price_snapshots({col_name})")
                print(f"   ✅ Índice {idx_name} criado")
            except Exception as e:
                print(f"   ⚠️  Erro ao criar índice {idx_name}: {e}")
                conn.rollback()
        
        conn.commit()
        
        # Count rows
        cursor.execute("SELECT COUNT(*) FROM price_snapshots")
        count = cursor.fetchone()[0]
        
        print()
        print("=" * 80)
        print("✅ TABELA price_snapshots PRONTA!")
        print("=" * 80)
        print(f"\n📊 Registos existentes: {count:,}")
        print()
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print()
    print("🔧 FIX: Estrutura da tabela price_snapshots")
    print()
    
    success = fix_price_snapshots()
    
    if success:
        print("✅ Estrutura corrigida!")
        print()
        print("📋 Próximos passos:")
        print("   1. Reiniciar o serviço no Render")
        print("   2. Testar funcionalidade de veículos")
        print()
    else:
        print("❌ Erro ao corrigir estrutura!")

if __name__ == "__main__":
    main()
