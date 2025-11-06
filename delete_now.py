import sqlite3

conn = sqlite3.connect('rental_tracker.db')
cursor = conn.cursor()

invalid_drs = ["1:2025", "2:2025", "3:2025"]

for dr in invalid_drs:
    cursor.execute("DELETE FROM damage_reports WHERE dr_number = ?", (dr,))
    print(f"✅ {dr} eliminado")

conn.commit()
conn.close()
print("\n✅ CONCLUÍDO!")
