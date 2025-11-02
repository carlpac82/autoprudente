#!/usr/bin/env python3
"""
Teste simples para verificar se as URLs de Albufeira estão válidas
"""
import os
import sys
from dotenv import load_dotenv
import requests

# Carregar .env
load_dotenv()

# Testar URLs de Albufeira
test_cases = [
    ("ALBUFEIRA_1D", 1),
    ("ALBUFEIRA_2D", 2),
    ("ALBUFEIRA_7D", 7),
]

print("=" * 70)
print("TESTE DE URLS DE ALBUFEIRA")
print("=" * 70)

for env_key, days in test_cases:
    url = os.getenv(env_key, "")
    print(f"\n{env_key} ({days} dias):")
    
    if not url:
        print(f"  ❌ Variável {env_key} não encontrada no .env")
        continue
    
    if not url.startswith('http'):
        print(f"  ❌ URL inválida: {url[:100]}...")
        continue
    
    print(f"  URL: {url[:80]}...")
    
    try:
        # Tentar fazer request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Cookie': 'monedaForzada=EUR; moneda=EUR; currency=EUR'
        }
        r = requests.get(url, headers=headers, timeout=10)
        
        print(f"  Status: {r.status_code}")
        print(f"  Tamanho: {len(r.text)} bytes")
        
        # Verificar se tem carros
        if 'data-nombre-coche' in r.text or 'class="price"' in r.text:
            print(f"  ✅ Parece conter dados de carros!")
        else:
            print(f"  ⚠️  Não encontrei dados de carros na resposta")
            
    except Exception as e:
        print(f"  ❌ ERRO: {e}")

print("\n" + "=" * 70)
print("\nRECOMENDAÇÃO:")
print("Se as URLs estão válidas, reinicia o servidor para aplicar as mudanças:")
print("  1. Parar servidor (Ctrl+C se estiver rodando)")
print("  2. python3 main.py")
print("=" * 70)
