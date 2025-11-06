"""
Verificar e corrigir numeração DR no PostgreSQL
"""

import psycopg2

DATABASE_URL = "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

pg_conn = psycopg2.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

print("=" * 80)
print("🔍 VERIFICAR NUMERAÇÃO DR NO POSTGRESQL")
print("=" * 80)

# 1. Ver estado atual
pg_cursor.execute("""
    SELECT id, current_year, current_number, prefix, updated_at
    FROM damage_report_numbering
    WHERE id = 1
""")

row = pg_cursor.fetchone()

if row:
    id, current_year, current_number, prefix, updated_at = row
    print(f"\n📊 ESTADO ATUAL:")
    print(f"  ID: {id}")
    print(f"  Ano: {current_year}")
    print(f"  Número Atual: {current_number}")
    print(f"  Prefixo: {prefix}")
    print(f"  Próximo DR: {prefix}{current_number + 1:02d}/{current_year}")
    print(f"  Atualizado: {updated_at}")
    
    # 2. Verificar último DR criado
    pg_cursor.execute("""
        SELECT dr_number, created_at
        FROM damage_reports
        ORDER BY created_at DESC
        LIMIT 1
    """)
    
    last_dr = pg_cursor.fetchone()
    if last_dr:
        dr_number, created_at = last_dr
        print(f"\n📄 ÚLTIMO DR CRIADO:")
        print(f"  DR: {dr_number}")
        print(f"  Data: {created_at}")
        
        # Extrair número do último DR
        import re
        match = re.search(r'(\d+)/(\d+)', dr_number)
        if match:
            last_num = int(match.group(1))
            last_year = int(match.group(2))
            print(f"  Número extraído: {last_num}")
            
            if last_num != current_number:
                print(f"\n⚠️  INCONSISTÊNCIA DETECTADA!")
                print(f"     Último DR criado: {last_num}")
                print(f"     Número na config: {current_number}")
                print(f"     Diferença: {current_number - last_num}")
                
                # Oferecer correção
                print(f"\n💡 QUER CORRIGIR?")
                print(f"   Para sincronizar, o current_number deveria ser: {last_num}")
                
                response = input("\n   Atualizar para o último DR criado? (s/n): ")
                
                if response.lower() == 's':
                    pg_cursor.execute("""
                        UPDATE damage_report_numbering
                        SET current_number = %s
                        WHERE id = 1
                    """, (last_num,))
                    pg_conn.commit()
                    print(f"   ✅ Atualizado! Próximo DR será: {prefix}{last_num + 1:02d}/{current_year}")
            else:
                print(f"\n✅ NUMERAÇÃO CONSISTENTE!")
                print(f"   Último DR: {last_num}")
                print(f"   Config: {current_number}")
                print(f"   Próximo será: {prefix}{current_number + 1:02d}/{current_year}")
else:
    print("\n❌ Configuração não encontrada!")

pg_conn.close()

print("\n" + "=" * 80)
print("✅ Verificação completa!")
