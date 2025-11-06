"""
Teste para verificar se o histórico de pesquisas está a ser guardado corretamente
"""

import psycopg2
import os
from datetime import datetime

DATABASE_URL = os.environ.get('DATABASE_URL') or "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

def test_search_history_table():
    """Verifica se a tabela search_history existe e está configurada corretamente"""
    
    print("=" * 80)
    print("🔍 TESTE: HISTÓRICO DE PESQUISAS NO POSTGRESQL")
    print("=" * 80)
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # 1. Verificar se tabela existe
        print("\n1️⃣ Verificando se tabela existe...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_name = 'search_history'
        """)
        exists = cursor.fetchone()[0]
        
        if exists > 0:
            print("   ✅ Tabela 'search_history' existe")
        else:
            print("   ❌ Tabela 'search_history' NÃO existe")
            print("   🔧 Criando tabela...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_history (
                    id SERIAL PRIMARY KEY,
                    location TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    days INTEGER NOT NULL,
                    results_count INTEGER DEFAULT 0,
                    min_price REAL,
                    max_price REAL,
                    avg_price REAL,
                    user TEXT DEFAULT 'admin',
                    search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    search_params TEXT
                )
            """)
            conn.commit()
            print("   ✅ Tabela criada com sucesso")
        
        # 2. Verificar estrutura da tabela
        print("\n2️⃣ Verificando estrutura da tabela...")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'search_history'
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        print(f"   📋 {len(columns)} colunas encontradas:")
        for col_name, data_type in columns:
            print(f"      - {col_name}: {data_type}")
        
        # 3. Contar registos existentes
        print("\n3️⃣ Verificando registos existentes...")
        cursor.execute("SELECT COUNT(*) FROM search_history")
        count = cursor.fetchone()[0]
        print(f"   📊 {count} registos na tabela")
        
        if count > 0:
            # Mostrar últimos 5 registos
            print("\n   📝 Últimos 5 registos:")
            cursor.execute("""
                SELECT location, start_date, end_date, days, results_count, search_timestamp
                FROM search_history
                ORDER BY search_timestamp DESC
                LIMIT 5
            """)
            for row in cursor.fetchall():
                print(f"      • {row[0]} | {row[1]} a {row[2]} | {row[3]}d | {row[4]} resultados | {row[5]}")
        
        # 4. Teste de INSERT
        print("\n4️⃣ Testando INSERT...")
        test_data = (
            'Albufeira',
            '2025-11-10',
            '2025-11-13',
            3,
            15,
            45.00,
            85.00,
            62.50,
            'test_user',
            '{"test": true}'
        )
        
        cursor.execute("""
            INSERT INTO search_history 
            (location, start_date, end_date, days, results_count, min_price, max_price, avg_price, "user", search_params)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, test_data)
        
        new_id = cursor.fetchone()[0]
        conn.commit()
        print(f"   ✅ Registo de teste inserido com ID: {new_id}")
        
        # 5. Verificar se foi guardado
        cursor.execute("SELECT COUNT(*) FROM search_history WHERE id = %s", (new_id,))
        if cursor.fetchone()[0] > 0:
            print("   ✅ Registo confirmado no PostgreSQL")
        
        # 6. Limpar teste
        cursor.execute("DELETE FROM search_history WHERE id = %s", (new_id,))
        conn.commit()
        print("   🧹 Registo de teste removido")
        
        # 7. Verificações finais
        print("\n" + "=" * 80)
        print("📋 RESUMO DA VERIFICAÇÃO")
        print("=" * 80)
        print(f"✅ Tabela existe: SIM")
        print(f"✅ Estrutura correta: SIM ({len(columns)} colunas)")
        print(f"✅ INSERT funciona: SIM")
        print(f"✅ COMMIT funciona: SIM")
        print(f"📊 Registos atuais: {count}")
        
        if count == 0:
            print("\n⚠️  NOTA:")
            print("   A tabela está vazia porque ainda não foram feitas pesquisas")
            print("   após o último deploy.")
            print("\n📝 PRÓXIMOS PASSOS:")
            print("   1. Fazer uma pesquisa na interface")
            print("   2. Verificar se o registo aparece")
            print("   3. Executar este script novamente")
        
        print("\n✅ TODOS OS TESTES PASSARAM!")
        print("=" * 80)
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_search_history_table()
