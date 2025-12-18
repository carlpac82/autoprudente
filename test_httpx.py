#!/usr/bin/env python3
"""
Teste com httpx - suporte HTTP/2 e melhor compatibilidade
"""

import httpx
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup

def test_httpx():
    print("=" * 60)
    print("TESTE HTTPX - CarJet")
    print("=" * 60)
    
    base_url = "https://www.carjet.com"
    
    # Headers completos como browser real
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'pt-PT,pt;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
    }
    
    with httpx.Client(headers=headers, follow_redirects=True, timeout=30.0) as client:
        # 1. Homepage
        print("\n[1] Visitando homepage...")
        resp = client.get(f"{base_url}/aluguel-carros/index.htm")
        print(f"    Status: {resp.status_code}, Cookies: {len(client.cookies)}")
        
        # Extrair TODOS os campos do formulário
        soup = BeautifulSoup(resp.text, 'html.parser')
        form = soup.find('form', {'name': 'frm_search_cars'})
        
        form_fields = {}
        if form:
            for inp in form.find_all(['input', 'select']):
                name = inp.get('name', '')
                value = inp.get('value', '')
                if name and name not in ['btnBuscar']:
                    form_fields[name] = value
            print(f"    Campos extraídos: {len(form_fields)}")
            print(f"    dtprc: {form_fields.get('dtprc', 'N/A')}")
        
        time.sleep(1)
        
        # 2. Preencher campos de pesquisa
        start_dt = datetime(2025, 4, 15, 15, 0)
        end_dt = datetime(2025, 4, 22, 15, 0)
        
        form_fields.update({
            'pais': 'PT',
            'destino': 'FAO02',
            'recogida': 'FAO02',
            'devolucion': 'FAO02',
            'destino_recogida_description': 'Faro Aeroporto (FAO)',
            'destino_devolucion_description': 'Faro Aeroporto (FAO)',
            'pickup': 'Faro Aeroporto (FAO)',
            'dropoff': '',
            'fechaRecogida': start_dt.strftime('%d/%m/%Y'),
            'horaRecogida': start_dt.strftime('%H:%M'),
            'fechaDevolucion': end_dt.strftime('%d/%m/%Y'),
            'horaDevolucion': end_dt.strftime('%H:%M'),
            'edadConductor': '35',
            'check_one_way': 'yes',
            'check_edad_conductor': 'yes',
            'pixelRatio': '3',
        })
        
        # 3. POST
        print("\n[2] Submetendo formulário...")
        timestamp = int(time.time() * 1000)
        post_url = f"{base_url}/do/list/pt?f=Do&dt1={timestamp}"
        
        post_headers = headers.copy()
        post_headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': base_url,
            'Referer': f'{base_url}/aluguel-carros/index.htm',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
        })
        
        resp_post = client.post(post_url, data=form_fields, headers=post_headers)
        
        print(f"    Status: {resp_post.status_code}")
        print(f"    URL final: {resp_post.url}")
        
        if 'war=' in str(resp_post.url):
            print(f"\n❌ ERRO: {resp_post.url}")
            
            # Tentar extrair mensagem de erro
            if resp_post.text:
                soup_err = BeautifulSoup(resp_post.text, 'html.parser')
                error_div = soup_err.find(class_='error') or soup_err.find(id='error')
                if error_div:
                    print(f"    Mensagem: {error_div.get_text(strip=True)[:100]}")
            
            with open('/tmp/httpx_error.html', 'w') as f:
                f.write(resp_post.text)
            return
        
        # 4. Verificar redirect
        print("\n[3] Verificando resultado...")
        
        redirect_url = None
        patterns = [
            r"window\.location\.replace\(['\"]([^'\"]+)['\"]\)",
            r"(/do/list/[^\s'\"<>]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, resp_post.text)
            if match:
                url = match.group(1)
                if '/do/list/' in url:
                    redirect_url = url if url.startswith('http') else f"{base_url}{url}"
                    break
        
        if '/do/list/' in str(resp_post.url):
            redirect_url = str(resp_post.url)
        
        if redirect_url:
            print(f"    Redirect: {redirect_url[:60]}...")
            
            # Polling
            for i in range(5):
                print(f"\n[4] Polling {i+1}/5...")
                time.sleep(5)
                
                resp_results = client.get(redirect_url)
                html = resp_results.text
                
                has_cars = 'carCardWeb' in html or 'car-card' in html
                is_loading = 'A carregar' in html
                
                print(f"    HTML: {len(html)} bytes, cars={has_cars}, loading={is_loading}")
                
                if has_cars and not is_loading:
                    print("\n✅ SUCESSO!")
                    soup = BeautifulSoup(html, 'html.parser')
                    cards = soup.select('.carCardWeb, [class*="carCard"]')
                    print(f"    Carros: {len(cards)}")
                    return
        else:
            print("    Sem redirect encontrado")
            with open('/tmp/httpx_no_redirect.html', 'w') as f:
                f.write(resp_post.text)

if __name__ == "__main__":
    test_httpx()
