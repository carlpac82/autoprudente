#!/usr/bin/env python3
"""
Teste do método direct com Albufeira após adicionar cookies
"""
from datetime import datetime, timedelta
from carjet_direct import scrape_carjet_direct

print("=" * 70)
print("TESTE MÉTODO DIRECT - ALBUFEIRA")
print("=" * 70)

# Datas de teste (14 dias no futuro, 2 dias de aluguer)
start_dt = datetime.now() + timedelta(days=14)
end_dt = start_dt + timedelta(days=2)

print(f"\nLocal: Albufeira")
print(f"Pickup: {start_dt.strftime('%d/%m/%Y %H:%M')}")
print(f"Return: {end_dt.strftime('%d/%m/%Y %H:%M')}")
print()

items = scrape_carjet_direct("Albufeira", start_dt, end_dt, quick=0)

print(f"\n{'='*70}")
print(f"RESULTADO: {len(items)} carros encontrados")
print(f"{'='*70}")

if items:
    print("\nPrimeiros 5 carros:")
    for i, item in enumerate(items[:5], 1):
        print(f"\n{i}. {item['car']}")
        print(f"   Supplier: {item['supplier']}")
        print(f"   Preço: {item['price']}")
        print(f"   Categoria: {item['category']}")
else:
    print("\n⚠️ NENHUM CARRO ENCONTRADO!")
    print("Verifica os logs acima para detalhes do erro.")
