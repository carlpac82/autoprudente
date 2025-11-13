#!/usr/bin/env python3
"""
Simular a lógica de detecção de transmissão do scraping
"""
import re

def detect_transmission_from_name(car_name):
    """
    Simula a lógica de inferência de transmissão a partir do nome do carro
    (mesma lógica que está no carjet_direct.py)
    """
    transmission = ''
    car_lower = car_name.lower()
    
    # Elétricos e híbridos são sempre automáticos
    if any(word in car_lower for word in ['electric', 'e-', 'hybrid', 'híbrido']):
        transmission = 'Automatic'
    # Se tem "auto" ou "automatic" explícito no nome
    elif re.search(r'\b(auto|automatic|automático|automatico)\b', car_lower):
        transmission = 'Automatic'
    
    return transmission

# Testes
test_cases = [
    ('Fiat 500', ''),
    ('Fiat 500 Auto', 'Automatic'),
    ('Fiat 500 Electric', 'Automatic'),
    ('Fiat 500e', ''),  # ⚠️ "e" sozinho não detecta
    ('Fiat 500 e', ''),  # ⚠️ "e" sozinho não detecta
    ('Fiat 500 Hybrid', 'Automatic'),
    ('Toyota Aygo', ''),
    ('Toyota Aygo Auto', 'Automatic'),
    ('Toyota Aygo X', ''),
    ('Toyota Aygo X Auto', 'Automatic'),
    ('Toyota Aygo E-', 'Automatic'),
    ('Peugeot 208 Electric', 'Automatic'),
    ('Renault Zoe e-Tech', 'Automatic'),
]

print("\n" + "="*100)
print("TESTE DE DETECÇÃO DE TRANSMISSÃO A PARTIR DO NOME DO CARRO")
print("="*100)

for car_name, expected_transmission in test_cases:
    detected = detect_transmission_from_name(car_name)
    
    if expected_transmission:
        status = "✅" if detected == expected_transmission else f"❌ Got: '{detected}'"
    else:
        status = "📋" if not detected else f"⚠️  Unexpected: '{detected}'"
    
    expected_str = expected_transmission or 'N/A'
    detected_str = detected or 'N/A'
    print(f"{status:20} | {car_name:30} | Expected: {expected_str:10} | Detected: {detected_str:10}")

print("\n" + "="*100)
print("NOTAS:")
print("  • 'Fiat 500e' e 'Fiat 500 e' não são detectados como elétricos")
print("  • Solução: Adicionar estas variações ao VEHICLES explicitamente")
print("  • OU melhorar regex: r'\\b(e-|electric|elétrico|e\\b)' (mas pode capturar falsos positivos)")
print("="*100)
