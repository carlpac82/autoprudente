#!/usr/bin/env python3
"""
Teste do download de fotos do CarJet
"""

import sys
from datetime import datetime, timedelta
from carjet_direct import scrape_carjet_direct

def test_download():
    print("="*60)
    print("TESTE DE DOWNLOAD DE FOTOS")
    print("="*60)
    
    # Datas de teste
    start_date = datetime.now() + timedelta(days=3)
    end_date = start_date + timedelta(days=7)
    
    print(f"\n📅 Datas:")
    print(f"   Início: {start_date.strftime('%Y-%m-%d')}")
    print(f"   Fim: {end_date.strftime('%Y-%m-%d')}")
    
    # Testar Faro
    print(f"\n🔍 Fazendo scraping em FARO...")
    faro_results = scrape_carjet_direct("Faro", start_date, end_date, quick=0)
    
    print(f"\n📊 RESULTADOS FARO:")
    print(f"   Total de carros: {len(faro_results)}")
    
    # Analisar fotos
    with_photos = 0
    without_photos = 0
    
    print(f"\n📸 ANÁLISE DE FOTOS:")
    for idx, item in enumerate(faro_results[:10], 1):  # Mostrar apenas os primeiros 10
        car = item.get('car', 'N/A')
        photo = item.get('photo', '')
        
        if photo:
            with_photos += 1
            print(f"   ✅ [{idx}] {car}")
            print(f"      URL: {photo[:80]}...")
        else:
            without_photos += 1
            print(f"   ❌ [{idx}] {car} - SEM FOTO")
    
    # Contar total
    for item in faro_results[10:]:
        if item.get('photo'):
            with_photos += 1
        else:
            without_photos += 1
    
    print(f"\n📈 RESUMO:")
    print(f"   Com fotos: {with_photos}/{len(faro_results)}")
    print(f"   Sem fotos: {without_photos}/{len(faro_results)}")
    print(f"   Percentual: {(with_photos/len(faro_results)*100):.1f}%")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    test_download()
