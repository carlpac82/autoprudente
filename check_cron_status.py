#!/usr/bin/env python3
"""
Verificar status dos cron jobs e emails diários no Render
"""
import requests
import json
from datetime import datetime

RENDER_URL = "https://carrental-api-5f8q.onrender.com"
USERNAME = "admin"
PASSWORD = "admin"

print("=" * 80)
print("🔍 VERIFICAR STATUS DE PESQUISAS E EMAILS DIÁRIOS")
print("=" * 80)
print()

# Login
print("🔐 Login...")
session = requests.Session()
session.post(f"{RENDER_URL}/login", 
             data={'username': USERNAME, 'password': PASSWORD},
             timeout=60)
print("✅ Login OK")
print()

# 1. Verificar histórico de pesquisas recentes
print("📊 HISTÓRICO DE PESQUISAS RECENTES:")
print("-" * 80)
try:
    response = session.get(f"{RENDER_URL}/api/recent-searches", timeout=60)
    
    if response.status_code == 200:
        searches = response.json()
        print(f"✅ Total: {len(searches)} pesquisas")
        
        # Filtrar pesquisas automatizadas (source='automated')
        automated = [s for s in searches if s.get('source') == 'automated']
        manual = [s for s in searches if s.get('source') != 'automated']
        
        print(f"🤖 Automatizadas: {len(automated)}")
        print(f"👤 Manuais: {len(manual)}")
        print()
        
        if automated:
            print("📅 ÚLTIMAS 5 PESQUISAS AUTOMATIZADAS:")
            for search in automated[:5]:
                timestamp = search.get('timestamp', 'N/A')
                location = search.get('location', 'N/A')
                days = search.get('days', 'N/A')
                results = search.get('results_data', [])
                print(f"  • {timestamp} | {location} | {days} dias | {len(results)} resultados")
            print()
        else:
            print("⚠️  Nenhuma pesquisa automatizada encontrada!")
            print()
    else:
        print(f"❌ Erro: HTTP {response.status_code}")
        print()
except Exception as e:
    print(f"❌ Erro ao buscar pesquisas: {e}")
    print()

# 2. Verificar configuração de emails automatizados
print("📧 CONFIGURAÇÃO DE EMAILS AUTOMATIZADOS:")
print("-" * 80)
try:
    response = session.get(f"{RENDER_URL}/api/email/settings/load", timeout=60)
    
    if response.status_code == 200:
        settings = response.json()
        
        if settings.get('ok'):
            config = settings.get('settings', {})
            
            print(f"✅ Relatório Diário: {'ATIVO' if config.get('daily_report_enabled') else 'INATIVO'}")
            print(f"   Hora: {config.get('daily_report_time', 'N/A')}")
            print(f"   Destinatários: {len(config.get('daily_report_recipients', []))}")
            
            print(f"✅ Relatório Semanal: {'ATIVO' if config.get('weekly_report_enabled') else 'INATIVO'}")
            print(f"   Dia: {config.get('weekly_report_day', 'N/A')}")
            print(f"   Hora: {config.get('weekly_report_time', 'N/A')}")
            print(f"   Destinatários: {len(config.get('weekly_report_recipients', []))}")
            print()
        else:
            print("⚠️  Nenhuma configuração encontrada")
            print()
    else:
        print(f"❌ Erro: HTTP {response.status_code}")
        print()
except Exception as e:
    print(f"❌ Erro ao buscar configuração: {e}")
    print()

# 3. Verificar OAuth do Gmail
print("🔐 OAUTH GMAIL:")
print("-" * 80)
try:
    response = session.get(f"{RENDER_URL}/api/oauth/load-token", timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        
        if data.get('ok'):
            token_data = data.get('token', {})
            print(f"✅ Gmail conectado: {token_data.get('user_email', 'N/A')}")
            print(f"   Expira em: {token_data.get('expires_at', 'N/A')}")
            print()
        else:
            print("⚠️  Gmail não conectado!")
            print()
    else:
        print(f"❌ Erro: HTTP {response.status_code}")
        print()
except Exception as e:
    print(f"❌ Erro ao verificar OAuth: {e}")
    print()

# 4. Informação sobre cron jobs
print("⏰ CRON JOBS (Horários de Lisboa):")
print("-" * 80)
print("📅 DIÁRIO: 7h00 (UTC 07:00) - Pesquisas + Email")
print("📅 SEMANAL: Segunda-feira 9h00 (UTC 09:00) - Email")
print()
print("Nota: Cron jobs são executados pelo Render Cron Jobs")
print("      Para ver execuções, verifica 'Cron Jobs' no dashboard do Render")
print()

# 5. Hora atual
print("🕐 HORA ATUAL:")
print("-" * 80)
now = datetime.now()
print(f"Local: {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"UTC: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
print()

print("=" * 80)
print("🎯 DIAGNÓSTICO:")
print("=" * 80)
print()
print("✅ Se pesquisas automatizadas aparecem: Cron job funciona")
print("⚠️  Se não há pesquisas automatizadas: Cron job não executou ainda")
print()
print("✅ Se Gmail está conectado: Emails podem ser enviados")
print("⚠️  Se Gmail não está conectado: Emails não serão enviados")
print()
print("✅ Se relatório diário está ATIVO: Email será enviado às 7h")
print("⚠️  Se relatório diário está INATIVO: Email não será enviado")
print()
print("📋 PRÓXIMOS PASSOS:")
print("1. Verificar dashboard do Render → Cron Jobs")
print("2. Ver logs de execução dos cron jobs")
print("3. Confirmar se pesquisas estão a ser salvas")
print("4. Confirmar se emails estão a ser enviados")
print()
