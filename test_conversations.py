#!/usr/bin/env python3
"""
Testar endpoint de conversas
"""

import requests

# Criar sessão
session = requests.Session()

# Login como admin
print("🔐 Fazendo login...")
login_response = session.post(
    'http://localhost:8000/login',
    data={'username': 'admin', 'password': 'admin'},
    timeout=10
)

if login_response.status_code != 200:
    print(f"❌ Erro ao fazer login: {login_response.status_code}")
    exit(1)

print("✅ Login bem-sucedido!")

# Testar endpoint de conversas
print("\n📞 Testando endpoint de conversas...")
response = session.get(
    'http://localhost:8000/api/whatsapp/conversations',
    timeout=10
)

print(f"\n📊 Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"✅ SUCESSO!")
    print(f"📄 Conversas encontradas: {len(data.get('conversations', []))}")
    print(f"📄 Response keys: {list(data.keys())}")
else:
    print(f"❌ ERRO! Status {response.status_code}")
    print(f"Response: {response.text[:500]}")
