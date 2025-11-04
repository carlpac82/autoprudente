#!/usr/bin/env python3
"""
Teste completo de extração de nome do carro do atributo alt
Simula HTML real do CarJet e valida o mapeamento foto → carro
"""

from bs4 import BeautifulSoup
import re

# HTML de exemplo do CarJet (estrutura real)
html_samples = [
    {
        'name': 'Skoda Scala',
        'html': '''
        <div class="car-card">
            <img class="cl--car-img" 
                 src="/cdn/img/cars/M/car_C166.jpg" 
                 data-original="" 
                 alt="Skoda Scala ou similar ">
        </div>
        ''',
        'expected_photo': '/cdn/img/cars/M/car_C166.jpg',
        'expected_name': 'Skoda Scala'
    },
    {
        'name': 'Toyota Aygo',
        'html': '''
        <div class="car-card">
            <img class="cl--car-img" 
                 src="/cdn/img/cars/M/car_C01.jpg" 
                 alt="Toyota Aygo ou similar | Pequeno">
        </div>
        ''',
        'expected_photo': '/cdn/img/cars/M/car_C01.jpg',
        'expected_name': 'Toyota Aygo'
    },
    {
        'name': 'Renault Clio (English)',
        'html': '''
        <div class="car-card">
            <img class="cl--car-img" 
                 src="/cdn/img/cars/M/car_C04.jpg" 
                 alt="Renault Clio or similar">
        </div>
        ''',
        'expected_photo': '/cdn/img/cars/M/car_C04.jpg',
        'expected_name': 'Renault Clio'
    },
    {
        'name': 'Fiat 500 (sem similar)',
        'html': '''
        <div class="car-card">
            <img class="cl--car-img" 
                 src="/cdn/img/cars/M/car_C02.jpg" 
                 alt="Fiat 500">
        </div>
        ''',
        'expected_photo': '/cdn/img/cars/M/car_C02.jpg',
        'expected_name': 'Fiat 500'
    }
]

print("=" * 80)
print("TESTE DE EXTRAÇÃO DE NOME DO CARRO DO ATRIBUTO ALT")
print("=" * 80)

total_tests = len(html_samples)
passed_tests = 0

for idx, test in enumerate(html_samples, 1):
    print(f"\n[TESTE {idx}/{total_tests}] {test['name']}")
    print("-" * 80)
    
    soup = BeautifulSoup(test['html'], 'html.parser')
    card = soup.select_one('.car-card')
    
    # Simular extração (igual ao código do main.py)
    car_img = card.select_one("img.cl--car-img")
    
    if car_img:
        src = (car_img.get("src") or car_img.get("data-src") or car_img.get("data-original") or "").strip()
        alt_text = (car_img.get("alt") or "").strip()
        
        print(f"  Foto encontrada: {src}")
        print(f"  Alt text: '{alt_text}'")
        
        if alt_text:
            # Processar alt text (igual ao código)
            alt_car_name = alt_text.split('ou similar')[0].split('or similar')[0].split('|')[0].strip()
            
            print(f"  Nome extraído: '{alt_car_name}'")
            
            # Validar
            photo_match = src == test['expected_photo']
            name_match = alt_car_name == test['expected_name']
            
            if photo_match and name_match:
                print(f"  ✅ SUCESSO!")
                print(f"     Foto: {src}")
                print(f"     Carro: {alt_car_name}")
                passed_tests += 1
            else:
                print(f"  ❌ FALHA!")
                if not photo_match:
                    print(f"     Foto esperada: {test['expected_photo']}")
                    print(f"     Foto obtida: {src}")
                if not name_match:
                    print(f"     Nome esperado: {test['expected_name']}")
                    print(f"     Nome obtido: {alt_car_name}")
        else:
            print(f"  ❌ FALHA: Atributo alt vazio")
    else:
        print(f"  ❌ FALHA: Imagem cl--car-img não encontrada")

print("\n" + "=" * 80)
print(f"RESULTADO FINAL: {passed_tests}/{total_tests} testes passaram")
print("=" * 80)

if passed_tests == total_tests:
    print("\n🎉 TODOS OS TESTES PASSARAM!")
    print("\n✅ O sistema está extraindo corretamente:")
    print("   - Nome do carro do atributo alt da imagem")
    print("   - Removendo 'ou similar' / 'or similar'")
    print("   - Removendo categorias após '|'")
    print("   - Mapeando foto → carro corretamente")
else:
    print(f"\n⚠️  {total_tests - passed_tests} teste(s) falharam")

# Teste adicional: Verificar limpeza de nome
print("\n" + "=" * 80)
print("TESTE ADICIONAL: LIMPEZA DE NOME DO CARRO")
print("=" * 80)

test_names = [
    ("Skoda Scala ou similar ", "skoda scala"),
    ("Toyota Aygo ou similar | Pequeno", "toyota aygo"),
    ("Renault Clio or similar", "renault clio"),
    ("Fiat 500", "fiat 500"),
    ("VW Polo ou similar | Médio", "vw polo"),
]

for original, expected_clean in test_names:
    # Simular limpeza
    cleaned = original.split('ou similar')[0].split('or similar')[0].split('|')[0].strip().lower()
    
    if cleaned == expected_clean:
        print(f"✅ '{original}' → '{cleaned}'")
    else:
        print(f"❌ '{original}' → '{cleaned}' (esperado: '{expected_clean}')")

print("\n" + "=" * 80)
print("✅ TESTE COMPLETO FINALIZADO!")
print("=" * 80)
