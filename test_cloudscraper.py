#!/usr/bin/env python3
"""
Teste com cloudscraper - especializado em anti-bot
"""

import cloudscraper
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup

def test_cloudscraper():
    print("=" * 60)
    print("TESTE CLOUDSCRAPER - CarJet")
    print("=" * 60)
    
    # Criar scraper com browser simulation
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'ios',
            'mobile': True
        }
    )
    
    base_url = "https://www.carjet.com"
    
    # 1. Homepage
    print("\n[1] Visitando homepage...")
    resp = scraper.get(f"{base_url}/aluguel-carros/index.htm", timeout=30)
    print(f"    Status: {resp.status_code}, Cookies: {len(scraper.cookies)}")
    
    # Extrair campos hidden
    soup = BeautifulSoup(resp.text, 'html.parser')
    form = soup.find('form', {'name': 'frm_search_cars'})
    
    form_fields = {}
    if form:
        for inp in form.find_all('input', {'type': 'hidden'}):
            name = inp.get('name', '')
            value = inp.get('value', '')
            if name:
                form_fields[name] = value
        print(f"    Campos: {len(form_fields)}")
    
    time.sleep(1)
    
    # 2. Autocomplete
    print("\n[2] Obtendo código destino...")
    resp_auto = scraper.post(
        f"{base_url}/do2/ajax/autocomplete",
        data={'idioma': 'PT', 'destino': 'Faro', 'origen': 'normal', 'experimento': '[M]'},
        headers={'X-Requested-With': 'XMLHttpRequest'}
    )
    
    dest_code = 'FAO02'
    dest_desc = 'Faro Aeroporto (FAO)'
    
    if resp_auto.status_code == 200:
        soup_auto = BeautifulSoup(resp_auto.text, 'html.parser')
        first = soup_auto.find('li')
        if first:
            dest_code = first.get('data-destino', 'FAO02')
            dest_desc = first.get('data-destino-description', 'Faro Aeroporto (FAO)')
    
    print(f"    Destino: {dest_code} - {dest_desc}")
    
    time.sleep(0.5)
    
    # 3. Preparar formulário
    print("\n[3] Preparando formulário...")
    
    start_dt = datetime(2025, 4, 15, 15, 0)
    end_dt = datetime(2025, 4, 22, 15, 0)
    timestamp = int(time.time() * 1000)
    
    form_data = form_fields.copy()
    form_data.update({
        'pais': 'PT',
        'destino': dest_code,
        'recogida': dest_code,
        'devolucion': dest_code,
        'destino_recogida_description': dest_desc,
        'destino_devolucion_description': dest_desc,
        'pickup': 'Faro',
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
    
    # 4. POST
    print("\n[4] Submetendo formulário...")
    post_url = f"{base_url}/do/list/pt?f=Do&dt1={timestamp}"
    
    resp_post = scraper.post(
        post_url,
        data=form_data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': base_url,
            'Referer': f'{base_url}/aluguel-carros/index.htm',
        },
        timeout=30,
        allow_redirects=True
    )
    
    print(f"    Status: {resp_post.status_code}")
    print(f"    URL: {resp_post.url}")
    
    if 'war=' in resp_post.url:
        print(f"\n❌ ERRO: {resp_post.url}")
        with open('/tmp/cloudscraper_error.html', 'w') as f:
            f.write(resp_post.text)
        return
    
    # 5. Extrair redirect
    print("\n[5] Procurando redirect...")
    
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
    
    if '/do/list/' in resp_post.url:
        redirect_url = resp_post.url
    
    if not redirect_url:
        print("    ❌ Redirect não encontrado")
        with open('/tmp/cloudscraper_no_redirect.html', 'w') as f:
            f.write(resp_post.text)
        return
    
    print(f"    Redirect: {redirect_url[:70]}...")
    
    # 6. Polling
    print("\n[6] Polling resultados...")
    
    for i in range(6):
        delay = [3, 4, 5, 6, 8, 10][i]
        print(f"    Tentativa {i+1}/6 (aguardando {delay}s)...")
        time.sleep(delay)
        
        resp_results = scraper.get(redirect_url, timeout=30)
        html = resp_results.text
        
        has_cars = 'carCardWeb' in html or 'resultado-oferta' in html
        is_loading = 'A carregar' in html or 'Procurando' in html
        
        if has_cars and not is_loading:
            print(f"\n✅ SUCESSO! Resultados prontos!")
            
            # Parse simples
            soup = BeautifulSoup(html, 'html.parser')
            cards = soup.select('.carCardWeb, .resultado-oferta, [class*="carCard"]')
            print(f"    Carros encontrados: {len(cards)}")
            
            for card in cards[:5]:
                title = card.select_one('.carCardWeb__title, h3, h4')
                if title:
                    print(f"    - {title.get_text(strip=True)[:50]}")
            
            return
        
        print(f"    HTML: {len(html)} bytes, loading={is_loading}")
    
    print("\n⏰ Timeout")

if __name__ == "__main__":
    test_cloudscraper()
