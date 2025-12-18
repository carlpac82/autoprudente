#!/usr/bin/env python3
"""
Teste API direta CarJet - SEM BROWSER
"""

from datetime import datetime, timedelta
from carjet_requests import scrape_carjet_requests

def test_api():
    print("=" * 60)
    print("TESTE API DIRETA CARJET (SEM BROWSER)")
    print("=" * 60)
    
    # Datas: 15-22 abril 2025
    start_dt = datetime(2025, 4, 15, 15, 0)
    end_dt = datetime(2025, 4, 22, 15, 0)
    
    print(f"\nLocal: Faro Aeroporto")
    print(f"Datas: {start_dt.strftime('%d/%m/%Y %H:%M')} → {end_dt.strftime('%d/%m/%Y %H:%M')}")
    print("-" * 60)
    
    results = scrape_carjet_requests("Faro Aeroporto", start_dt, end_dt)
    
    print("\n" + "=" * 60)
    if results:
        print(f"✅ SUCESSO! {len(results)} carros encontrados:")
        print("-" * 60)
        for i, car in enumerate(results[:10]):  # Mostrar só os primeiros 10
            print(f"{i+1}. {car.get('vehicle', 'N/A')} - €{car.get('price', 'N/A')}/dia - {car.get('supplier', 'N/A')}")
        if len(results) > 10:
            print(f"   ... e mais {len(results) - 10} carros")
    else:
        print("❌ FALHOU - Nenhum resultado")
    print("=" * 60)

if __name__ == "__main__":
    test_api()
