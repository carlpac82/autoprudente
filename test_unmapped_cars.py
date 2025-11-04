#!/usr/bin/env python3
"""
Testar quais carros não estão a ser mapeados corretamente
"""

import sys
import sqlite3
from pathlib import Path

# Import da função do main.py
sys.path.insert(0, '.')
from main import map_category_to_group, clean_car_name

# Conectar à base de dados
db_path = Path(__file__).parent / "data.db"
conn = sqlite3.connect(db_path)

# Buscar todos os carros únicos dos snapshots recentes
query = """
SELECT DISTINCT car, category 
FROM price_snapshots 
WHERE timestamp > datetime('now', '-7 days')
ORDER BY car
"""

cursor = conn.execute(query)
rows = cursor.fetchall()

print("=" * 80)
print(f"ANÁLISE DE MAPEAMENTO DE GRUPOS - {len(rows)} carros únicos")
print("=" * 80)
print()

# Contar por grupo
group_counts = {}
unmapped_cars = []

for car_name, category in rows:
    if not car_name:
        continue
    
    car_clean = clean_car_name(car_name)
    group_code = map_category_to_group(category or "", car_clean)
    
    if group_code not in group_counts:
        group_counts[group_code] = []
    
    group_counts[group_code].append((car_clean, category))
    
    if group_code == "Others":
        unmapped_cars.append((car_clean, category))

# Mostrar estatísticas
print("📊 ESTATÍSTICAS POR GRUPO:")
print("-" * 80)
for group_code in sorted(group_counts.keys()):
    count = len(group_counts[group_code])
    print(f"{group_code:10s}: {count:4d} carros")

print()
print("=" * 80)
print(f"⚠️  CARROS NÃO MAPEADOS (Others): {len(unmapped_cars)}")
print("=" * 80)
print()

if unmapped_cars:
    print("Lista de carros em 'Others':")
    print("-" * 80)
    for i, (car, cat) in enumerate(unmapped_cars[:50], 1):  # Mostrar primeiros 50
        print(f"{i:3d}. {car:50s} | Cat: {cat or '(sem categoria)'}")
    
    if len(unmapped_cars) > 50:
        print(f"\n... e mais {len(unmapped_cars) - 50} carros")

conn.close()

print()
print("=" * 80)
print("✅ Análise completa!")
print("=" * 80)
