#!/usr/bin/env python3
"""
Teste unitário da função filter_automatic_only()
Valida se o filtro está corretamente identificando e removendo carros manuais
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from main import filter_automatic_only


def test_filter_function():
    print("=" * 80)
    print("TESTE: Função filter_automatic_only()")
    print("=" * 80)
    print()
    
    # Dataset de teste com carros automáticos e manuais
    test_data = [
        # Automáticos explícitos
        {
            "car": "VW Polo",
            "name": "VW Polo Auto",
            "transmission": "Automatic",
            "price": "€25/day"
        },
        {
            "car": "Nissan Qashqai",
            "name": "Nissan Qashqai Auto",
            "transmission": "Automático",
            "price": "€35/day"
        },
        {
            "car": "Ford Focus",
            "name": "Ford Focus",
            "transmission": "auto",
            "price": "€28/day"
        },
        # Manuais explícitos (devem ser filtrados)
        {
            "car": "Renault Clio",
            "name": "Renault Clio",
            "transmission": "Manual",
            "price": "€20/day"
        },
        {
            "car": "Peugeot 208",
            "name": "Peugeot 208",
            "transmission": "manual",
            "price": "€22/day"
        },
        # Automático por nome do carro (apesar de transmission vazio)
        {
            "car": "Toyota Corolla Auto",
            "name": "Toyota Corolla Auto",
            "transmission": "",
            "price": "€30/day"
        },
        # Edge cases
        {
            "car": "Hyundai i30",
            "name": "Hyundai i30",
            "transmission": "",  # Vazio - deve ser removido
            "price": "€26/day"
        },
        {
            "car": "Seat Leon",
            "name": "Seat Leon",
            "transmission": None,  # None - deve ser removido
            "price": "€27/day"
        },
    ]
    
    print(f"📊 Dataset de teste: {len(test_data)} carros")
    print()
    print("Carros antes do filtro:")
    for i, car in enumerate(test_data, 1):
        trans = car.get('transmission') or '(vazio)'
        print(f"  {i}. {car['name']:30s} | Trans: {trans:15s}")
    print()
    
    # Aplicar filtro
    print("🔧 Aplicando filter_automatic_only()...")
    filtered = filter_automatic_only(test_data)
    print()
    
    # Mostrar resultados
    print("=" * 80)
    print("RESULTADOS")
    print("=" * 80)
    print()
    print(f"Total antes do filtro:  {len(test_data)} carros")
    print(f"Total após filtro:      {len(filtered)} carros")
    print(f"Carros removidos:       {len(test_data) - len(filtered)} carros")
    print()
    
    if filtered:
        print("Carros mantidos (apenas automáticos):")
        for i, car in enumerate(filtered, 1):
            trans = car.get('transmission') or '(vazio)'
            print(f"  {i}. {car['name']:30s} | Trans: {trans:15s}")
        print()
    
    # Validações
    print("=" * 80)
    print("VALIDAÇÕES")
    print("=" * 80)
    print()
    
    success = True
    
    # 1. Verificar se manteve os automáticos corretos
    expected_automatic = [
        "VW Polo Auto",
        "Nissan Qashqai Auto",
        "Ford Focus",
        "Toyota Corolla Auto"
    ]
    
    filtered_names = [car['name'] for car in filtered]
    
    for expected in expected_automatic:
        if expected in filtered_names:
            print(f"✅ Manteve corretamente: {expected}")
        else:
            print(f"❌ ERRO: Deveria manter {expected}")
            success = False
    
    print()
    
    # 2. Verificar se removeu os manuais corretos
    expected_removed = [
        "Renault Clio",
        "Peugeot 208",
        "Hyundai i30",  # transmission vazio
        "Seat Leon"      # transmission None
    ]
    
    for expected in expected_removed:
        if expected not in filtered_names:
            print(f"✅ Removeu corretamente: {expected}")
        else:
            print(f"❌ ERRO: Deveria remover {expected}")
            success = False
    
    print()
    print("=" * 80)
    
    if success:
        print("✅ TESTE PASSOU: Filtro funcionando corretamente!")
    else:
        print("❌ TESTE FALHOU: Filtro não está funcionando como esperado")
    
    print("=" * 80)
    print()
    
    return success


if __name__ == "__main__":
    try:
        success = test_filter_function()
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
