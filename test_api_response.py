#!/usr/bin/env python3
"""
Testar resposta da API para ver campo 'group'
"""

import requests
import json
from datetime import datetime, timedelta

# URL da API local
url = "http://localhost:8000/api/track-by-params"

# Preparar dados de teste
today = datetime.now()
pickup_date = (today + timedelta(days=7)).strftime("%Y-%m-%d")

payload = {
    "location": "Aeroporto de Faro",
    "start_date": pickup_date,
    "start_time": "15:00",
    "days": 7,
    "lang": "pt",
    "currency": "EUR"
}

print("=" * 80)
print("TESTE DE RESPOSTA DA API")
print("=" * 80)
print()
print(f"📍 Local: {payload['location']}")
print(f"📅 Data: {payload['start_date']}")
print(f"⏱️  Dias: {payload['days']}")
print()
print("Enviando request...")
print()

try:
    response = requests.post(url, json=payload, timeout=120)
    
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        
        print(f"✅ Sucesso! {len(items)} carros encontrados")
        print()
        print("=" * 80)
        print("ANÁLISE DE CAMPOS 'group':")
        print("=" * 80)
        print()
        
        # Contar por grupo
        group_counts = {}
        cars_without_group = []
        cars_with_others = []
        
        for item in items:
            car = item.get("car", "")
            group = item.get("group", "")
            category = item.get("category", "")
            
            if not group:
                cars_without_group.append((car, category))
                group = "(vazio)"
            elif group == "Others":
                cars_with_others.append((car, category))
            
            if group not in group_counts:
                group_counts[group] = []
            group_counts[group].append(car)
        
        # Mostrar estatísticas
        print("📊 DISTRIBUIÇÃO POR GRUPO:")
        print("-" * 80)
        for group_code in sorted(group_counts.keys()):
            count = len(group_counts[group_code])
            percentage = (count / len(items)) * 100
            print(f"{group_code:15s}: {count:4d} carros ({percentage:5.1f}%)")
        
        print()
        print("=" * 80)
        
        # Carros sem grupo
        if cars_without_group:
            print(f"⚠️  CARROS SEM CAMPO 'group': {len(cars_without_group)}")
            print("-" * 80)
            for i, (car, cat) in enumerate(cars_without_group[:20], 1):
                print(f"{i:3d}. {car:50s} | Cat: {cat or '(sem)'}")
            if len(cars_without_group) > 20:
                print(f"... e mais {len(cars_without_group) - 20}")
            print()
        
        # Carros com grupo "Others"
        if cars_with_others:
            print(f"⚠️  CARROS COM GRUPO 'Others': {len(cars_with_others)}")
            print("-" * 80)
            for i, (car, cat) in enumerate(cars_with_others[:30], 1):
                print(f"{i:3d}. {car:50s} | Cat: {cat or '(sem)'}")
            if len(cars_with_others) > 30:
                print(f"... e mais {len(cars_with_others) - 30}")
            print()
        
        # Mostrar exemplo de item completo
        if items:
            print("=" * 80)
            print("EXEMPLO DE ITEM (primeiro resultado):")
            print("-" * 80)
            print(json.dumps(items[0], indent=2, ensure_ascii=False))
        
    else:
        print(f"❌ Erro: Status {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Erro: {e}")

print()
print("=" * 80)
