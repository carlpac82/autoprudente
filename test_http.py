#!/usr/bin/env python3
"""Teste HTTP direto - sem Selenium"""

import requests
from datetime import datetime, timedelta

def test_carjet():
    print("🚀 Teste via HTTP direto (sem Selenium)...")
    
    # Datas de teste - Janeiro 2025
    start_dt = datetime(2025, 1, 6, 10, 0)
    end_dt = datetime(2025, 1, 9, 10, 0)
    print(f"📅 Datas: {start_dt.strftime('%Y-%m-%d')} a {end_dt.strftime('%Y-%m-%d')}")
    
    # Headers de browser real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'pt-PT,pt;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
    }
    
    session = requests.Session()
    
    # Tentar URL de resultados direto
    pickup_date = start_dt.strftime("%Y%m%d")
    dropoff_date = end_dt.strftime("%Y%m%d")
    
    # Formato correto da URL CarJet
    url = f"https://www.carjet.com/pt/do/list/pt?b=faro&s={pickup_date}&st=10:00&e={dropoff_date}&et=10:00&age=30&cur=EUR"
    
    print(f"📍 Tentando URL direta: {url}")
    
    try:
        response = session.get(url, headers=headers, timeout=30)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Tamanho: {len(response.text)} bytes")
        print(f"🔗 URL final: {response.url}")
        
        # Verificar se tem carros ou bloqueio
        if 'war=' in response.url:
            print("❌ Bloqueado (WAR)")
        elif 'captcha' in response.text.lower() or 'datadome' in response.text.lower():
            print("❌ Bloqueado (Captcha/DataDome)")
        else:
            print("📄 Primeiros 500 chars:")
            print(response.text[:500])
            
        # Guardar para análise
        with open('/tmp/carjet_response.html', 'w') as f:
            f.write(response.text)
        print("📁 Guardado em /tmp/carjet_response.html")
                
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_carjet()
