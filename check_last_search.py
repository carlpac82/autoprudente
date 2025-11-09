#!/usr/bin/env python3
"""
Ver última pesquisa para extrair formato das imagens
"""

import os
import json
import psycopg2
from pathlib import Path
from datetime import datetime

def load_env():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env()

database_url = os.environ.get('DATABASE_URL')
conn = psycopg2.connect(database_url)
cursor = conn.cursor()

# Buscar última pesquisa
cursor.execute("""
    SELECT location, start_date, days, results_data, timestamp
    FROM recent_searches
    ORDER BY timestamp DESC
    LIMIT 1
""")

row = cursor.fetchone()

if row:
    location, start_date, days, results_data, timestamp = row
    results = json.loads(results_data) if results_data else []
    
    print("=" * 80)
    print(f"ÚLTIMA PESQUISA: {timestamp}")
    print(f"Local: {location}")
    print(f"Data: {start_date}, Dias: {days}")
    print(f"Total carros: {len(results)}")
    print("=" * 80)
    
    if results:
        print("\nPRIMEIRO CARRO (exemplo):")
        print("-" * 80)
        first_car = results[0]
        
        for key, value in first_car.items():
            if isinstance(value, str) and len(value) > 100:
                print(f"{key}: {value[:100]}...")
            else:
                print(f"{key}: {value}")
        
        print("\n" + "=" * 80)
        print("CAMPOS DISPONÍVEIS:")
        print(", ".join(first_car.keys()))
        print("=" * 80)
        
        # Ver se tem campo de imagem
        image_fields = [k for k in first_car.keys() if 'image' in k.lower() or 'img' in k.lower() or 'photo' in k.lower() or 'pic' in k.lower()]
        if image_fields:
            print(f"\n✅ CAMPOS DE IMAGEM ENCONTRADOS: {image_fields}")
            for field in image_fields:
                print(f"\n{field}: {first_car.get(field)}")
        else:
            print("\n❌ Nenhum campo de imagem encontrado")
            print("\nTodos os campos:")
            for k in sorted(first_car.keys()):
                print(f"  - {k}")

cursor.close()
conn.close()
