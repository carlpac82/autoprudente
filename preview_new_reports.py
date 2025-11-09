#!/usr/bin/env python3
"""
🎨 PREVIEW dos Novos Relatórios
Cria um HTML local para visualizar antes de aplicar
"""

from improved_reports import (
    generate_daily_report_html_by_location,
    COLOR_PRIMARY,
    COLOR_YELLOW
)
from datetime import datetime

# Dados de TESTE (simular pesquisa com IMAGENS)
mock_search_data = {
    'location': 'Albufeira',
    'date': datetime.now().strftime('%Y-%m-%d'),
    'results': [
        # Grupo A - 3 dias - Albufeira (IMAGENS REAIS do CarJet)
        {'group': 'Grupo A', 'days': 3, 'location': 'Albufeira', 'supplier': 'Auto Prudente', 'price_num': 45.00, 'price': '45.00€', 'car': 'Renault Clio', 'photo': 'https://www.carjet.com/cdn/img/cars/L/car_A01.jpg'},
        {'group': 'Grupo A', 'days': 3, 'location': 'Albufeira', 'supplier': 'Guerin', 'price_num': 50.00, 'price': '50.00€', 'car': 'Peugeot 208', 'photo': 'https://www.carjet.com/cdn/img/cars/L/car_B04.jpg'},
        {'group': 'Grupo A', 'days': 3, 'location': 'Albufeira', 'supplier': 'Europcar', 'price_num': 52.00, 'price': '52.00€', 'car': 'Opel Corsa', 'photo': 'https://www.carjet.com/cdn/img/cars/L/car_B01.jpg'},
        
        # Grupo A - 7 dias - Albufeira
        {'group': 'Grupo A', 'days': 7, 'location': 'Albufeira', 'supplier': 'Guerin', 'price_num': 90.00, 'price': '90.00€', 'car': 'Peugeot 208', 'photo': 'https://www.carjet.com/cdn/img/cars/L/car_B04.jpg'},
        {'group': 'Grupo A', 'days': 7, 'location': 'Albufeira', 'supplier': 'Auto Prudente', 'price_num': 92.00, 'price': '92.00€', 'car': 'Renault Clio', 'photo': 'https://www.carjet.com/cdn/img/cars/L/car_A01.jpg'},
        {'group': 'Grupo A', 'days': 7, 'location': 'Albufeira', 'supplier': 'Hertz', 'price_num': 95.00, 'price': '95.00€', 'car': 'Ford Fiesta', 'photo': 'https://www.carjet.com/cdn/img/cars/L/car_B05.jpg'},
        
        # Grupo B - 3 dias - Albufeira  
        {'group': 'Grupo B', 'days': 3, 'location': 'Albufeira', 'supplier': 'Budget', 'price_num': 60.00, 'price': '60.00€', 'car': 'Volkswagen Polo', 'photo': 'https://www.carjet.com/cdn/img/cars/L/car_C01.jpg'},
        {'group': 'Grupo B', 'days': 3, 'location': 'Albufeira', 'supplier': 'Auto Prudente', 'price_num': 62.00, 'price': '62.00€', 'car': 'Seat Ibiza', 'photo': 'https://www.carjet.com/cdn/img/cars/L/car_B02.jpg'},
        {'group': 'Grupo B', 'days': 3, 'location': 'Albufeira', 'supplier': 'Sixt', 'price_num': 65.00, 'price': '65.00€', 'car': 'Fiat 500', 'photo': 'https://www.carjet.com/cdn/img/cars/L/car_A03.jpg'},
        
        # Aeroporto (não deve aparecer no relatório de Albufeira)
        {'group': 'Grupo A', 'days': 3, 'location': 'Aeroporto de Faro', 'supplier': 'Auto Prudente', 'price_num': 48.00, 'price': '48.00€', 'car': 'Renault Clio', 'photo': 'https://www.carjet.com/cdn/img/cars/L/car_A01.jpg'},
    ]
}

def main():
    print("🎨 Gerando preview dos relatórios...")
    print("=" * 60)
    
    # Generate Albufeira report
    print("\n📍 Relatório para ALBUFEIRA:")
    html_albufeira = generate_daily_report_html_by_location(mock_search_data, "Albufeira")
    
    with open('preview_albufeira.html', 'w', encoding='utf-8') as f:
        f.write(html_albufeira)
    
    print("   ✅ preview_albufeira.html criado")
    
    # Generate Aeroporto report
    print("\n✈️  Relatório para AEROPORTO:")
    html_aeroporto = generate_daily_report_html_by_location(mock_search_data, "Aeroporto de Faro")
    
    with open('preview_aeroporto.html', 'w', encoding='utf-8') as f:
        f.write(html_aeroporto)
    
    print("   ✅ preview_aeroporto.html criado")
    
    print("\n" + "=" * 60)
    print("✅ PREVIEWS CRIADOS!")
    print("=" * 60)
    print("\n📂 Ficheiros criados:")
    print("   • preview_albufeira.html")
    print("   • preview_aeroporto.html")
    print("\n🌐 ABRIR NO BROWSER:")
    print(f"   open preview_albufeira.html")
    print(f"   open preview_aeroporto.html")
    print("\n🎨 CORES USADAS:")
    print(f"   • Azul Auto Prudente: {COLOR_PRIMARY}")
    print(f"   • Amarelo: {COLOR_YELLOW}")
    print("\n✅ FUNCIONALIDADES:")
    print("   • Header igual ao DR (barra turquesa + logo)")
    print("   • Grupos organizados por dias")
    print("   • Mostra TODOS os dias pesquisados")
    print("   • Filtrado por localização (1 email por local)")
    print("   • Estatísticas de desempenho")
    print("   • Top 5 competidores por grupo/dias")
    print("\n💡 Se aprovares o layout, aplico no main.py!")
    print("=" * 60)

if __name__ == "__main__":
    main()
