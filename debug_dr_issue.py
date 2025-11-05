"""
DEBUG: Investigar problema do DR39/2025
"""

import psycopg2
import urllib.parse

DATABASE_URL = "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

pg_conn = psycopg2.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

print("🔍 INVESTIGAÇÃO DO PROBLEMA")
print("=" * 80)

# 1. Ver exatamente como está o DR39 no banco
print("\n1️⃣ DR39/2025 no PostgreSQL:")
pg_cursor.execute("""
    SELECT 
        dr_number,
        LENGTH(dr_number) as len,
        ASCII(SUBSTRING(dr_number FROM 1 FOR 1)) as first_char,
        CASE WHEN pdf_data IS NULL THEN 'SEM PDF' ELSE 'COM PDF' END as has_pdf,
        LENGTH(pdf_data) as pdf_size
    FROM damage_reports
    WHERE dr_number LIKE '%39%2025'
""")

rows = pg_cursor.fetchall()
for row in rows:
    dr_num, length, first_char, has_pdf, pdf_size = row
    print(f"  dr_number: [{dr_num}]")
    print(f"  Comprimento: {length}")
    print(f"  Primeiro char ASCII: {first_char} (D=68)")
    print(f"  Bytes: {[ord(c) for c in dr_num[:5]]}")
    print(f"  Status: {has_pdf}")
    print(f"  PDF size: {pdf_size} bytes")

# 2. Ver TODOS os DRs que começam com DR
print("\n2️⃣ Todos os DRs no banco (primeiros 5):")
pg_cursor.execute("""
    SELECT dr_number
    FROM damage_reports
    ORDER BY dr_number
    LIMIT 5
""")

for row in pg_cursor.fetchall():
    print(f"  [{row[0]}]")

# 3. Testar diferentes variações do DR39
print("\n3️⃣ Testando variações do DR39:")
test_cases = [
    "DR39/2025",      # Sem espaço
    "DR 39/2025",     # Com espaço
    "DR  39/2025",    # Dois espaços
]

for test in test_cases:
    pg_cursor.execute("SELECT COUNT(*) FROM damage_reports WHERE dr_number = %s", (test,))
    count = pg_cursor.fetchone()[0]
    print(f"  '{test}': {'✅ EXISTE' if count > 0 else '❌ NÃO EXISTE'}")

# 4. URL encoding
print("\n4️⃣ URL Encoding:")
url_variants = [
    "DR39/2025",
    "DR%2039%2F2025",  # Com espaço encoded
    "DR39%2F2025",     # Sem espaço encoded
]

for url in url_variants:
    decoded = urllib.parse.unquote(url)
    print(f"  URL: {url}")
    print(f"  Decoded: [{decoded}]")
    pg_cursor.execute("SELECT COUNT(*) FROM damage_reports WHERE dr_number = %s", (decoded,))
    count = pg_cursor.fetchone()[0]
    print(f"  Match: {'✅ SIM' if count > 0 else '❌ NÃO'}")
    print()

pg_conn.close()

print("=" * 80)
print("✅ Investigação completa!")
