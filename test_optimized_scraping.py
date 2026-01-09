#!/usr/bin/env python3
"""
Teste de scraping otimizado - Medir tempo de resposta
"""
import time
import requests
from datetime import datetime, timedelta

# Configuração
API_URL = "http://localhost:8000/api/vehicles/search"
LOGIN_URL = "http://localhost:8000/login"

def test_scraping_performance():
    """Testar performance do scraping com otimizações"""
    
    # Calcular datas
    pickup_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    dropoff_date = (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d')
    
    print("=" * 70)
    print("🚀 TESTE DE PERFORMANCE - SCRAPING CARJET OTIMIZADO")
    print("=" * 70)
    print(f"📍 Local: Faro Airport")
    print(f"📅 Pickup: {pickup_date} 15:00")
    print(f"📅 Dropoff: {dropoff_date} 15:00")
    print(f"⏱️  Duração: 7 dias")
    print("=" * 70)
    print()
    
    # Criar sessão e fazer login
    session = requests.Session()
    
    print("🔐 Fazendo login...")
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    login_response = session.post(LOGIN_URL, data=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Erro no login: {login_response.status_code}")
        return
    
    print("✅ Login realizado")
    print()
    
    # Fazer pesquisa e medir tempo
    print("🔍 Iniciando scraping...")
    print("⏱️  Cronômetro iniciado...")
    print()
    
    start_time = time.time()
    
    try:
        # Fazer requisição
        params = {
            "q": "Aeroporto de Faro",
            "location": "Aeroporto de Faro",
            "start_date": pickup_date,
            "start_time": "15:00",
            "days": "7"
        }
        
        response = session.get(API_URL, params=params, timeout=300)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print()
        print("=" * 70)
        print("📊 RESULTADOS")
        print("=" * 70)
        print(f"⏱️  Tempo total: {elapsed_time:.2f} segundos ({elapsed_time/60:.2f} minutos)")
        print(f"📡 Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            # Tentar parsear resposta
            try:
                # Se for HTML, contar carros
                html = response.text
                if '<article' in html or 'car' in html.lower():
                    car_count = html.count('<article')
                    if car_count == 0:
                        car_count = html.count('class="car')
                    print(f"🚗 Carros encontrados: ~{car_count}")
                
                print()
                print("✅ Scraping concluído com sucesso!")
                
                # Análise de performance
                print()
                print("=" * 70)
                print("📈 ANÁLISE DE PERFORMANCE")
                print("=" * 70)
                
                if elapsed_time < 60:
                    print(f"🚀 EXCELENTE! Tempo abaixo de 1 minuto")
                    print(f"   Ganho: ~{((360 - elapsed_time) / 360 * 100):.0f}% mais rápido que antes")
                elif elapsed_time < 120:
                    print(f"✅ BOM! Tempo abaixo de 2 minutos")
                    print(f"   Ganho: ~{((360 - elapsed_time) / 360 * 100):.0f}% mais rápido que antes")
                elif elapsed_time < 300:
                    print(f"⚠️  ACEITÁVEL. Tempo abaixo de 5 minutos")
                    print(f"   Ganho: ~{((360 - elapsed_time) / 360 * 100):.0f}% mais rápido que antes")
                else:
                    print(f"❌ LENTO. Tempo acima de 5 minutos")
                    print(f"   Ainda precisa de otimização")
                
                print()
                print("Tempo antes das otimizações: ~6-10 minutos")
                print(f"Tempo atual: {elapsed_time:.2f} segundos")
                
            except Exception as e:
                print(f"⚠️  Erro ao analisar resposta: {e}")
                print(f"📄 Primeiros 500 chars: {response.text[:500]}")
        else:
            print(f"❌ Erro na requisição")
            print(f"📄 Resposta: {response.text[:500]}")
        
        print("=" * 70)
        
    except requests.Timeout:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print()
        print(f"⏱️  Timeout após {elapsed_time:.2f} segundos")
        print(f"❌ Scraping demorou mais de 5 minutos")
        
    except Exception as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print()
        print(f"❌ Erro após {elapsed_time:.2f} segundos: {e}")

if __name__ == "__main__":
    test_scraping_performance()
