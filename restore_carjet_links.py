"""
Restaurar links das fotos da Carjet para vehicle_photos
Baseado no ficheiro carjet_cars_data_v3.json com 170 carros
"""

import psycopg2
import json
import re
from difflib import SequenceMatcher

DATABASE_URL = "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

# Load Carjet data from JSON
print("📂 Carregando dados da Carjet...")
with open('carjet_cars_data_v3.json', 'r', encoding='utf-8') as f:
    carjet_data = json.load(f)

print(f"✅ {len(carjet_data)} carros carregados da Carjet")

def normalize_name(name):
    """Normalizar nome do veículo"""
    name = name.lower().strip()
    # Replace common variations
    name = name.replace('volkswagen', 'vw')
    name = name.replace('mercedes benz', 'mercedes')
    name = name.replace('mercedes-benz', 'mercedes')
    # Remove extra spaces
    name = ' '.join(name.split())
    return name

def similarity(a, b):
    """Calcular similaridade entre dois nomes"""
    return SequenceMatcher(None, a, b).ratio()

def get_carjet_url(vehicle_name):
    """Obter URL da Carjet para um veículo usando matching inteligente"""
    normalized = normalize_name(vehicle_name)
    
    best_match = None
    best_score = 0
    
    for car in carjet_data:
        car_name = normalize_name(car['full_name'])
        
        # Exact match
        if car_name == normalized:
            return car['photo_url']
        
        # Check if vehicle_name is in car_name or vice versa
        if car_name in normalized or normalized in car_name:
            score = similarity(car_name, normalized)
            if score > best_score:
                best_score = score
                best_match = car
        
        # Check base name match (without variant)
        if 'base_name' in car:
            base_name = normalize_name(car['base_name'])
            if base_name == normalized or base_name in normalized:
                score = similarity(base_name, normalized)
                if score > best_score:
                    best_score = score
                    best_match = car
        
        # Check brand + model match
        brand = normalize_name(car['brand'])
        model = normalize_name(car['model'])
        brand_model = f"{brand} {model}"
        
        if brand_model in normalized or normalized.startswith(brand_model):
            score = similarity(brand_model, normalized)
            if score > best_score:
                best_score = score
                best_match = car
    
    # Return if similarity is good enough (>0.7)
    if best_match and best_score > 0.7:
        return best_match['photo_url']
    
    return None

# Connect to PostgreSQL
pg_conn = psycopg2.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

print("=" * 80)
print("🔗 RESTAURAR LINKS DAS FOTOS DA CARJET")
print("=" * 80)

# Get all vehicles without photo_url
pg_cursor.execute("""
    SELECT vehicle_name
    FROM vehicle_photos
    WHERE photo_url IS NULL OR photo_url = ''
    ORDER BY vehicle_name
""")

vehicles = pg_cursor.fetchall()
total = len(vehicles)

print(f"\n📊 {total} veículos sem photo_url")
print("\n🔄 Processando...\n")

updated = 0
not_found = 0
not_found_list = []

for (vehicle_name,) in vehicles:
    url = get_carjet_url(vehicle_name)
    
    if url:
        try:
            pg_cursor.execute("""
                UPDATE vehicle_photos
                SET photo_url = %s
                WHERE vehicle_name = %s
            """, (url, vehicle_name))
            pg_conn.commit()
            print(f"✅ {vehicle_name}: {url}")
            updated += 1
        except Exception as e:
            print(f"❌ {vehicle_name}: ERRO - {e}")
    else:
        print(f"⚠️  {vehicle_name}: Código não encontrado")
        not_found += 1
        not_found_list.append(vehicle_name)

print("\n" + "=" * 80)
print("📊 RESUMO")
print("=" * 80)
print(f"✅ Atualizados: {updated}/{total} ({updated/total*100:.1f}%)")
print(f"⚠️  Não encontrados: {not_found}/{total} ({not_found/total*100:.1f}%)")

if not_found_list:
    print(f"\n📋 VEÍCULOS SEM CÓDIGO ({len(not_found_list)}):")
    for v in not_found_list[:20]:  # Show first 20
        print(f"  - {v}")
    if len(not_found_list) > 20:
        print(f"  ... e mais {len(not_found_list) - 20}")

pg_conn.close()

print("\n✅ Script concluído!")
print("\n💡 PRÓXIMO PASSO:")
print("   Para os veículos não encontrados, podes:")
print("   1. Adicionar códigos manualmente ao dicionário CARJET_CODES")
print("   2. Re-executar este script")
