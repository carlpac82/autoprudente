"""
Verificar DRs no PostgreSQL do Render
"""

import psycopg2

DATABASE_URL = "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

pg_conn = psycopg2.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

print("📋 DRs no PostgreSQL do Render:")
print("=" * 80)

pg_cursor.execute("""
    SELECT 
        dr_number, 
        pdf_filename,
        CASE WHEN pdf_data IS NULL THEN 'SEM PDF' ELSE 'COM PDF' END as status,
        LENGTH(pdf_data) as pdf_size
    FROM damage_reports
    ORDER BY dr_number
    LIMIT 50
""")

rows = pg_cursor.fetchall()

for row in rows:
    dr_number, pdf_filename, status, pdf_size = row
    size_kb = f"{pdf_size / 1024:.1f} KB" if pdf_size else "0 KB"
    print(f"{dr_number:<15} | {pdf_filename:<25} | {status:<10} | {size_kb}")

print("=" * 80)
print(f"Total: {len(rows)} DRs")

pg_conn.close()
