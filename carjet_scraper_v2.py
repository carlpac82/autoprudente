#!/usr/bin/env python3
"""
CarJet Scraper V2 - Baseado na análise do JavaScript do site
"""

import requests
import re
import time
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup

class CarJetScraper:
    """Scraper para CarJet usando a mesma lógica do site"""
    
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.carjet.com"
        
        # Headers que imitam iPhone Safari
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-PT,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_destination_code(self, location: str) -> Optional[Dict]:
        """Obtém código do destino via API de autocomplete"""
        url = f"{self.base_url}/do2/ajax/autocomplete"
        
        data = {
            'idioma': 'PT',
            'destino': location,
            'origen': 'normal',
            'experimento': '[M]'
        }
        
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': f'{self.base_url}/aluguel-carros/index.htm'
        }
        
        try:
            resp = self.session.post(url, data=data, headers=headers, timeout=10)
            if resp.status_code == 200 and resp.text:
                soup = BeautifulSoup(resp.text, 'html.parser')
                first_item = soup.find('li')
                if first_item:
                    return {
                        'code': first_item.get('data-destino'),
                        'pais': first_item.get('data-pais'),
                        'description': first_item.get('data-destino-description'),
                        'iata': first_item.get('data-iata', '')
                    }
        except Exception as e:
            print(f"[SCRAPER] Erro autocomplete: {e}")
        
        return None
    
    def init_session(self) -> bool:
        """Inicializa sessão visitando homepage"""
        print("[SCRAPER] Inicializando sessão...")
        
        try:
            # Visitar homepage
            resp = self.session.get(f"{self.base_url}/aluguel-carros/index.htm", timeout=15)
            print(f"[SCRAPER] Homepage: {resp.status_code}, Cookies: {len(self.session.cookies)}")
            
            # Extrair campos hidden do formulário
            soup = BeautifulSoup(resp.text, 'html.parser')
            form = soup.find('form', {'name': 'frm_search_cars'})
            
            self.form_fields = {}
            if form:
                for inp in form.find_all('input', {'type': 'hidden'}):
                    name = inp.get('name', '')
                    value = inp.get('value', '')
                    if name:
                        self.form_fields[name] = value
                print(f"[SCRAPER] Campos extraídos: {len(self.form_fields)}")
            
            return True
        except Exception as e:
            print(f"[SCRAPER] Erro init: {e}")
            return False
    
    def search(self, location: str, start_dt: datetime, end_dt: datetime) -> List[Dict]:
        """Executa pesquisa de carros"""
        print(f"[SCRAPER] Pesquisa: {location}")
        print(f"[SCRAPER] Datas: {start_dt.strftime('%d/%m/%Y %H:%M')} → {end_dt.strftime('%d/%m/%Y %H:%M')}")
        
        # 1. Inicializar sessão
        if not self.init_session():
            return []
        
        time.sleep(random.uniform(0.5, 1.5))
        
        # 2. Obter código do destino
        dest_info = self.get_destination_code(location)
        if not dest_info:
            print("[SCRAPER] ❌ Destino não encontrado")
            return []
        
        print(f"[SCRAPER] Destino: {dest_info}")
        
        time.sleep(random.uniform(0.3, 0.8))
        
        # 3. Preparar dados do formulário
        timestamp = int(time.time() * 1000)
        
        form_data = self.form_fields.copy()
        form_data.update({
            'pais': dest_info['pais'],
            'destino': dest_info['code'],
            'recogida': dest_info['code'],
            'devolucion': dest_info['code'],
            'destino_recogida_description': dest_info['description'],
            'destino_devolucion_description': dest_info['description'],
            'pickup': location,
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
        
        # 4. Submeter formulário
        post_url = f"{self.base_url}/do/list/pt?f=Do&dt1={timestamp}"
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/aluguel-carros/index.htm',
        }
        
        print(f"[SCRAPER] POST: {post_url}")
        
        try:
            resp = self.session.post(post_url, data=form_data, headers=headers, timeout=15, allow_redirects=True)
            print(f"[SCRAPER] Resposta: {resp.status_code}, URL: {resp.url[:80]}...")
            
            # Verificar erro
            if 'war=' in resp.url:
                print(f"[SCRAPER] ❌ Erro CarJet: {resp.url}")
                # Salvar para debug
                with open('/tmp/carjet_error.html', 'w') as f:
                    f.write(resp.text)
                return []
            
            # 5. Extrair URL de redirect
            redirect_url = self._extract_redirect(resp.text)
            
            if not redirect_url:
                # Verificar se já está na página de resultados
                if '/do/list/' in resp.url:
                    redirect_url = resp.url
                else:
                    print("[SCRAPER] ❌ Redirect não encontrado")
                    with open('/tmp/carjet_no_redirect.html', 'w') as f:
                        f.write(resp.text)
                    return []
            
            if not redirect_url.startswith('http'):
                redirect_url = f"{self.base_url}{redirect_url}"
            
            print(f"[SCRAPER] Redirect: {redirect_url[:80]}...")
            
            # 6. Polling para resultados
            return self._poll_results(redirect_url)
            
        except Exception as e:
            print(f"[SCRAPER] ❌ Erro POST: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _extract_redirect(self, html: str) -> Optional[str]:
        """Extrai URL de redirect do JavaScript"""
        patterns = [
            r"window\.location\.replace\(['\"]([^'\"]+)['\"]\)",
            r"window\.location\.href\s*=\s*['\"]([^'\"]+)['\"]",
            r"location\.href\s*=\s*['\"]([^'\"]+)['\"]",
            r"(/do/list/[^\s'\"<>]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                url = match.group(1)
                if '/do/list/' in url and len(url) > 20:
                    return url
        
        return None
    
    def _poll_results(self, url: str, max_attempts: int = 8) -> List[Dict]:
        """Faz polling até resultados estarem prontos"""
        delays = [3, 4, 5, 6, 7, 8, 10, 12]
        
        for attempt in range(max_attempts):
            delay = delays[attempt] if attempt < len(delays) else 10
            print(f"[SCRAPER] Polling {attempt+1}/{max_attempts} (aguardando {delay}s)...")
            time.sleep(delay)
            
            try:
                resp = self.session.get(url, timeout=15)
                html = resp.text
                
                # Verificar se ainda está a carregar
                loading_indicators = ['A carregar', 'Procurando', 'Searching', 'Please wait', 'Aguarde']
                is_loading = any(ind in html for ind in loading_indicators)
                
                # Verificar se tem carros
                has_cars = 'carCardWeb' in html or 'resultado-oferta' in html or 'price pr-euros' in html
                
                if has_cars and not is_loading:
                    print(f"[SCRAPER] ✅ Resultados prontos!")
                    return self._parse_results(html)
                
                if is_loading:
                    print(f"[SCRAPER] ⏳ Ainda a carregar...")
                else:
                    print(f"[SCRAPER] HTML: {len(html)} bytes")
                    
            except Exception as e:
                print(f"[SCRAPER] Erro polling: {e}")
        
        print("[SCRAPER] ⏰ Timeout - sem resultados")
        return []
    
    def _parse_results(self, html: str) -> List[Dict]:
        """Parse dos resultados"""
        cars = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Tentar vários seletores
        cards = soup.select('.carCardWeb, .resultado-oferta, .car-card, [class*="carCard"]')
        
        print(f"[SCRAPER] Cards encontrados: {len(cards)}")
        
        for card in cards:
            try:
                car = {}
                
                # Nome do veículo
                name_el = card.select_one('.carCardWeb__title, .car-name, h3, h4')
                car['vehicle'] = name_el.get_text(strip=True) if name_el else 'N/A'
                
                # Preço
                price_el = card.select_one('.price, .precio, [class*="price"]')
                if price_el:
                    price_text = price_el.get_text(strip=True)
                    # Extrair número
                    price_match = re.search(r'[\d,\.]+', price_text.replace(',', '.'))
                    car['price'] = float(price_match.group()) if price_match else 0
                else:
                    car['price'] = 0
                
                # Fornecedor
                supplier_el = card.select_one('.supplier, .proveedor, img[alt*="logo"]')
                if supplier_el:
                    car['supplier'] = supplier_el.get('alt', '') or supplier_el.get_text(strip=True)
                else:
                    car['supplier'] = 'N/A'
                
                if car['vehicle'] != 'N/A':
                    cars.append(car)
                    
            except Exception as e:
                continue
        
        return cars


def test_scraper():
    """Teste do scraper"""
    print("=" * 60)
    print("TESTE CARJET SCRAPER V2")
    print("=" * 60)
    
    scraper = CarJetScraper()
    
    start_dt = datetime(2025, 4, 15, 15, 0)
    end_dt = datetime(2025, 4, 22, 15, 0)
    
    results = scraper.search("Faro", start_dt, end_dt)
    
    print("\n" + "=" * 60)
    if results:
        print(f"✅ {len(results)} carros encontrados:")
        for i, car in enumerate(results[:10]):
            print(f"  {i+1}. {car['vehicle']} - €{car['price']} - {car['supplier']}")
    else:
        print("❌ Nenhum resultado")
    print("=" * 60)


if __name__ == "__main__":
    test_scraper()
