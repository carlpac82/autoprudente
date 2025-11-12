#!/usr/bin/env python3
"""
Testar manualmente a pesquisa e envio de email diário
NOTA: Precisa do CRON_SECRET do Render
"""
import requests
import json

RENDER_URL = "https://carrental-api-5f8q.onrender.com"

# IMPORTANTE: Substituir pelo CRON_SECRET real do Render
# Encontra em: Render Dashboard → Environment → CRON_SECRET
CRON_SECRET = "PRECISA_SUBSTITUIR"

print("=" * 80)
print("🧪 TESTE MANUAL - PESQUISA E EMAIL DIÁRIO")
print("=" * 80)
print()

if CRON_SECRET == "PRECISA_SUBSTITUIR":
    print("❌ ERRO: Precisa definir CRON_SECRET!")
    print()
    print("📋 COMO OBTER:")
    print("1. Vai a: https://dashboard.render.com")
    print("2. Abre: carrental-api-5f8q")
    print("3. Environment → CRON_SECRET")
    print("4. Copia o valor")
    print("5. Cola neste script na variável CRON_SECRET")
    print()
    exit(1)

print("🔍 Testando endpoint de pesquisa diária...")
print()

# Testar endpoint do cron job
try:
    response = requests.post(
        f"{RENDER_URL}/api/cron/daily-search",
        headers={"X-Cron-Secret": CRON_SECRET},
        timeout=300  # 5 minutos (pesquisa pode demorar)
    )
    
    print(f"Status: {response.status_code}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        print("✅ SUCESSO!")
        print()
        print(json.dumps(data, indent=2))
        print()
        print("📊 VERIFICAÇÕES:")
        print("1. Pesquisas foram feitas?")
        print("2. Dados foram salvos na BD?")
        print("3. Email foi enviado?")
        print()
    elif response.status_code == 401:
        print("❌ ERRO: CRON_SECRET inválido!")
        print("   Verifica o secret no Render Dashboard")
        print()
    elif response.status_code == 500:
        print("❌ ERRO: Servidor falhou ao executar")
        print()
        print("Response:")
        print(response.text)
        print()
    else:
        print(f"⚠️  Status inesperado: {response.status_code}")
        print()
        print("Response:")
        print(response.text)
        print()
        
except requests.exceptions.Timeout:
    print("⏱️  TIMEOUT: Pesquisa demorou mais de 5 minutos")
    print("   Isto é normal se o Render estava dormindo")
    print("   Verifica os logs do Render para ver se completou")
    print()
except Exception as e:
    print(f"❌ ERRO: {e}")
    print()

print("=" * 80)
print("📋 ALTERNATIVA - TRIGGER VIA RENDER DASHBOARD:")
print("=" * 80)
print()
print("Se não tens o CRON_SECRET:")
print("1. Vai ao Render Dashboard")
print("2. Cron Jobs → daily-search-and-report")
print("3. Clica em 'Trigger Job Now'")
print("4. Espera 2-5 minutos")
print("5. Verifica os logs")
print()
