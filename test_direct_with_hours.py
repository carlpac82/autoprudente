#!/usr/bin/env python3
"""
Testar método DIRECT com horas entre 14:30-17:00
"""
from datetime import datetime, timedelta
import random

# Importar função do carjet_direct
from carjet_direct import scrape_carjet_direct

print("=" * 70)
print("TESTE MÉTODO DIRECT COM HORAS 14:30-17:00")
print("=" * 70)

# Datas de teste
start_dt = datetime.now() + timedelta(days=14)
end_dt = start_dt + timedelta(days=2)

# Hora aleatória entre 14:30 e 17:00
possible_times = ["14:30", "15:00", "15:30", "16:00", "16:30", "17:00"]
pickup_time = random.choice(possible_times)

# Ajustar datetime para usar a hora escolhida
hour, minute = pickup_time.split(":")
start_dt = start_dt.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
end_dt = end_dt.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)

print(f"\nLocal: Albufeira")
print(f"Pickup: {start_dt.strftime('%d/%m/%Y %H:%M')}")
print(f"Return: {end_dt.strftime('%d/%m/%Y %H:%M')}")
print(f"Hora escolhida: {pickup_time}")
print()

# Testar método DIRECT
items = scrape_carjet_direct("Albufeira", start_dt, end_dt, quick=0)

print(f"\n{'='*70}")
print(f"RESULTADO: {len(items)} carros encontrados")
print(f"{'='*70}")

if items:
    print("\n✅ SUCESSO! Primeiros 5 carros:")
    for i, item in enumerate(items[:5], 1):
        print(f"\n{i}. {item['car']}")
        print(f"   Supplier: {item['supplier']}")
        print(f"   Preço: {item['price']}")
        print(f"   Categoria: {item['category']}")
else:
    print("\n⚠️ NENHUM CARRO ENCONTRADO!")
    print("O método DIRECT ainda não funciona.")
