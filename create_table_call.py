#!/usr/bin/env python3
"""
Chamar endpoint para criar tabela whatsapp_contacts
"""

import requests
import time

# Aguardar servidor estar pronto
print("⏳ Aguardando servidor estar pronto...")
time.sleep(2)

# Criar sessão
session = requests.Session()

# Login como admin
print("🔐 Fazendo login como admin...")
login_response = session.post(
    'http://localhost:8000/login',
    data={'username': 'admin', 'password': 'admin'},
    timeout=10
)

if login_response.status_code != 200:
    print(f"❌ Erro ao fazer login: {login_response.status_code}")
    print(login_response.text)
    exit(1)

print("✅ Login bem-sucedido!")

# Chamar endpoint para criar tabela
print("\n🔨 Criando tabela whatsapp_contacts...")
response = session.post(
    'http://localhost:8000/api/admin/whatsapp/create-contacts-table',
    timeout=30
)

print(f"\n📊 Status: {response.status_code}")
print(f"📄 Response:")
print(response.json())

if response.status_code == 200:
    print("\n🎉 SUCESSO! Tabela criada.")
else:
    print(f"\n❌ ERRO! Status {response.status_code}")
