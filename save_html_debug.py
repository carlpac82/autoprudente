#!/usr/bin/env python3
"""
Salva o HTML real para debug
"""
import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from selenium_simple import scrape_carjet_simple
from datetime import datetime, timedelta

start_dt = datetime.now() + timedelta(days=60)  # 60 dias no futuro
end_dt = start_dt + timedelta(days=7)

print("Fazendo scraping...")
result = scrape_carjet_simple('albufeira', start_dt, end_dt)

if result['ok']:
    html = result['html']
    
    # Salvar HTML
    with open('/tmp/carjet_debug.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML salvo: /tmp/carjet_debug.html ({len(html)} bytes)")
    
    # Procurar por ícones de transmissão
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')
    
    # Procurar todos os ícones
    all_icons = soup.find_all('i', class_=lambda x: x and 'icon' in x)
    print(f"\n📊 Total de ícones <i> encontrados: {len(all_icons)}")
    
    # Procurar especificamente transmissão
    trans_icons = soup.find_all('i', class_=lambda x: x and 'transm' in x)
    print(f"🔧 Ícones de transmissão: {len(trans_icons)}")
    
    if trans_icons:
        print("\n🔍 Exemplos de ícones de transmissão encontrados:")
        for icon in trans_icons[:5]:
            classes = ' '.join(icon.get('class', []))
            print(f"   - <i class=\"{classes}\">")
    else:
        print("\n⚠️  NENHUM ícone de transmissão encontrado!")
        print("\nVou procurar por 'manual' ou 'automatic' no HTML...")
        
        # Procurar texto
        if 'manual' in html.lower():
            print("✅ Palavra 'manual' encontrada no HTML")
        if 'automatic' in html.lower() or 'automático' in html.lower():
            print("✅ Palavra 'automatic' encontrada no HTML")
    
    # Procurar cards de carros
    cards = soup.find_all('article', class_=lambda x: x and 'card' in x)
    if not cards:
        cards = soup.find_all('div', class_=lambda x: x and 'card' in x)
    
    print(f"\n🚗 Cards de carros encontrados: {len(cards)}")
    
    if cards:
        print("\n🔍 Analisando primeiro card:")
        first_card = cards[0]
        print(f"Classes do card: {first_card.get('class', [])}")
        print(f"HTML do card (primeiros 500 chars):")
        print(str(first_card)[:500])
        
else:
    print(f"❌ Erro: {result.get('error')}")
