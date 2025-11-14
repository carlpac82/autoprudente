#!/usr/bin/env python3
"""
Teste do Filtro de Transmissão Automática no CarJet
Verifica se todas as pesquisas retornam apenas carros automáticos
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import from main.py
from main import try_direct_carjet, parse_prices

def test_automatic_filter():
    print("=" * 80)
    print("TESTE: Filtro de Transmissão Automática - CarJet")
    print("=" * 80)
    print()
    
    # Configurar pesquisa
    location = "Faro Aeroporto (FAO)"
    start_dt = datetime.now() + timedelta(days=7)
    end_dt = start_dt + timedelta(days=5)
    
    print(f"📍 Local: {location}")
    print(f"📅 Data Pickup: {start_dt.strftime('%d/%m/%Y %H:%M')}")
    print(f"📅 Data Dropoff: {end_dt.strftime('%d/%m/%Y %H:%M')}")
    print(f"🕐 Dias: 5")
    print()
    
    # Fazer request ao CarJet
    print("🔄 Fazendo request ao CarJet com filtro automático...")
    html = try_direct_carjet(location, start_dt, end_dt, lang="pt", currency="EUR")
    
    if not html:
        print("❌ ERRO: Não recebeu HTML do CarJet")
        return False
    
    print(f"✅ HTML recebido: {len(html)} caracteres")
    print()
    
    # Parse dos resultados
    print("🔍 Parsing dos resultados...")
    results = parse_prices(html, "https://www.carjet.com/do/list/pt")
    
    if not results:
        print("❌ ERRO: Nenhum carro encontrado")
        print()
        print("💡 Possíveis causas:")
        print("   - Filtro muito restritivo (poucos automáticos disponíveis)")
        print("   - Problema no parsing do HTML")
        print("   - CarJet não retornou resultados")
        return False
    
    print(f"✅ Encontrados {len(results)} carros")
    print()
    
    # Verificar transmissão de cada carro
    print("=" * 80)
    print("VERIFICAÇÃO DE TRANSMISSÃO")
    print("=" * 80)
    print()
    
    automatic_count = 0
    manual_count = 0
    unknown_count = 0
    
    for i, car in enumerate(results, 1):
        name = car.get('name', 'Unknown')
        transmission = car.get('transmission', '').lower()
        
        # Determinar tipo de transmissão
        if 'automatic' in transmission or 'automático' in transmission or 'auto' in transmission:
            status = "✅ AUTOMÁTICO"
            automatic_count += 1
        elif 'manual' in transmission:
            status = "❌ MANUAL"
            manual_count += 1
        else:
            status = "⚠️  DESCONHECIDO"
            unknown_count += 1
        
        print(f"{i:2d}. {name:40s} | {transmission:15s} | {status}")
    
    print()
    print("=" * 80)
    print("RESUMO DOS RESULTADOS")
    print("=" * 80)
    print()
    print(f"Total de carros:     {len(results)}")
    print(f"Automáticos:         {automatic_count} ({automatic_count/len(results)*100:.1f}%)")
    print(f"Manuais:             {manual_count} ({manual_count/len(results)*100:.1f}%)")
    print(f"Desconhecidos:       {unknown_count} ({unknown_count/len(results)*100:.1f}%)")
    print()
    
    # Verificar se filtro funcionou
    if manual_count > 0:
        print("❌ TESTE FALHOU: Foram encontrados carros manuais!")
        print(f"   O filtro deveria retornar apenas automáticos, mas {manual_count} manuais foram encontrados.")
        return False
    
    if automatic_count == 0:
        print("⚠️  ATENÇÃO: Nenhum carro marcado explicitamente como automático")
        print("   Pode ser que o campo 'transmission' não esteja sendo parseado corretamente")
        print()
        print("📝 Exemplo do primeiro carro:")
        if results:
            import json
            print(json.dumps(results[0], indent=2, ensure_ascii=False))
        return False
    
    print("✅ TESTE PASSOU: Todos os carros são automáticos!")
    print()
    
    # Mostrar exemplo de um carro
    print("=" * 80)
    print("EXEMPLO DE CARRO AUTOMÁTICO")
    print("=" * 80)
    print()
    if results:
        import json
        print(json.dumps(results[0], indent=2, ensure_ascii=False))
    
    return True


if __name__ == "__main__":
    try:
        success = test_automatic_filter()
        sys.exit(0 if success else 1)
    except Exception as e:
        print()
        print("=" * 80)
        print("❌ ERRO DURANTE O TESTE")
        print("=" * 80)
        print()
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
