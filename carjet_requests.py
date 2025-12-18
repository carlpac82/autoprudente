"""
CarJet scraping usando requests com sessão persistente
Importa funções de parse do carjet_direct.py para manter compatibilidade
"""
import requests
import re
import time
from datetime import datetime
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import uuid

# Importar funções de parse completas do carjet_direct.py
try:
    from carjet_direct import (
        parse_carjet_html_complete,
        SUPPLIER_MAP,
        normalize_supplier,
        detect_category_from_car,
        map_category_to_group_code,
        VEHICLES
    )
    HAS_CARJET_PARSE = True
except ImportError:
    HAS_CARJET_PARSE = False
    print("[REQUESTS] ⚠️ Não foi possível importar funções do carjet_direct.py")


def extract_redirect_url(html: str) -> str:
    """Extrai URL de redirect do JavaScript com múltiplos métodos"""
    import sys
    
    # Método 1: window.location.replace com aspas simples
    pattern1 = r"window\.location\.replace\('([^']+)'\)"
    match = re.search(pattern1, html)
    if match:
        print(f"[REQUESTS] ✅ URL extraída (método 1): {match.group(1)}", file=sys.stderr, flush=True)
        return match.group(1)
    
    # Método 2: window.location.replace com aspas duplas
    pattern2 = r'window\.location\.replace\("([^"]+)"\)'
    match = re.search(pattern2, html)
    if match:
        print(f"[REQUESTS] ✅ URL extraída (método 2): {match.group(1)}", file=sys.stderr, flush=True)
        return match.group(1)
    
    # Método 3: window.location.href
    pattern3 = r"window\.location\.href\s*=\s*['\"]([^'\"]+)['\"]"
    match = re.search(pattern3, html)
    if match:
        print(f"[REQUESTS] ✅ URL extraída (método 3): {match.group(1)}", file=sys.stderr, flush=True)
        return match.group(1)
    
    # Método 4: Procurar por /do/list/ na URL (fallback - mais permissivo)
    pattern4 = r'["\']?(/do/list/[^\s"\'<>]+)["\']?'
    match = re.search(pattern4, html)
    if match:
        url = match.group(1)
        # Validar se a URL parece completa (deve ter mais de 20 caracteres)
        if len(url) > 20 and ('s=' in url or 'b=' in url or len(url) > 30):
            print(f"[REQUESTS] ✅ URL extraída (método 4 fallback): {url}", file=sys.stderr, flush=True)
            return url
        else:
            print(f"[REQUESTS] ⚠️ URL método 4 parece incompleta (ignorando): {url}", file=sys.stderr, flush=True)
    
    # Método 5: Procurar especificamente por padrão com s= e b=
    pattern5 = r'/do/list/\w+\?[^"\'<>\s]*[sb]=[^"\'<>\s]+'
    match = re.search(pattern5, html)
    if match:
        url = match.group(0)
        print(f"[REQUESTS] ✅ URL extraída (método 5 - com parâmetros): {url}", file=sys.stderr, flush=True)
        return url
    
    print(f"[REQUESTS] ❌ Nenhum redirect encontrado no HTML", file=sys.stderr, flush=True)
    return None


def scrape_carjet_requests(location: str, start_dt: datetime, end_dt: datetime) -> List[Dict[str, Any]]:
    """
    Scraping do CarJet usando requests com sessão persistente
    """
    import sys
    try:
        # Mapeamento de localizações
        location_codes = {
            'faro': 'FAO02',
            'aeroporto de faro': 'FAO02',
            'albufeira': 'ABF01',
        }
        
        loc_lower = location.lower()
        pickup_code = 'FAO02'
        for key, code in location_codes.items():
            if key in loc_lower:
                pickup_code = code
                break
        
        print(f"[REQUESTS] Location: {location} ({pickup_code})")
        print(f"[REQUESTS] Datas: {start_dt.strftime('%d/%m/%Y')} → {end_dt.strftime('%d/%m/%Y')}")
        
        # Criar sessão persistente (mantém cookies automaticamente)
        session = requests.Session()
        
        # Headers realistas simulando iPhone Safari
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-PT,pt;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # PASSO 1: Visitar homepage para obter cookies iniciais
        print("[REQUESTS] Passo 1: Visitando homepage...")
        home_url = 'https://www.carjet.com/aluguel-carros/index.htm'
        resp_home = session.get(home_url, timeout=15)
        print(f"[REQUESTS] Homepage: {resp_home.status_code} - Cookies: {len(session.cookies)}")
        
        # Aguardar um pouco (simular comportamento humano)
        time.sleep(2)
        
        # PASSO 2: Fazer POST do formulário
        print("[REQUESTS] Passo 2: Submetendo formulário...", file=sys.stderr, flush=True)
        
        pickup_date = start_dt.strftime('%d/%m/%Y %H:%M')
        return_date = end_dt.strftime('%d/%m/%Y %H:%M')
        session_id = str(uuid.uuid4())
        
        form_data = {
            'frmDestino': pickup_code,
            'frmDestinoFinal': '',
            'frmFechaRecogida': pickup_date,
            'frmFechaDevolucion': return_date,
            'frmHasAge': 'False',
            'frmEdad': '35',
            'frmPrvNo': '',
            'frmMoneda': 'EUR',
            'frmMonedaForzada': 'EUR',  # Forçar EUR
            'frmJsonFilterInfo': '',
            'frmTipoVeh': 'CAR',
            'idioma': 'PT',
            'frmSession': session_id,
            'frmDetailCode': ''
        }
        
        # Adicionar headers específicos para POST
        post_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.carjet.com',
            'Referer': home_url,
        }
        
        post_url = 'https://www.carjet.com/do/list/pt'
        print(f"[REQUESTS] POST URL: {post_url}", file=sys.stderr, flush=True)
        print(f"[REQUESTS] POST Data: {pickup_code}, {pickup_date} -> {return_date}", file=sys.stderr, flush=True)
        
        try:
            resp_post = session.post(post_url, data=form_data, headers=post_headers, timeout=10, allow_redirects=True)
            print(f"[REQUESTS] ✅ POST completado em <10s", file=sys.stderr, flush=True)
        except requests.exceptions.Timeout:
            print(f"[REQUESTS] ⏰ POST timeout após 10s - abortando", file=sys.stderr, flush=True)
            return []
        except Exception as post_err:
            print(f"[REQUESTS] ❌ POST erro: {post_err}", file=sys.stderr, flush=True)
            return []
        
        print(f"[REQUESTS] POST: {resp_post.status_code} - URL: {resp_post.url}", file=sys.stderr, flush=True)
        print(f"[REQUESTS] HTML: {len(resp_post.text)} bytes", file=sys.stderr, flush=True)
        
        # Verificar se CarJet retornou erro (war= parameter)
        if 'war=' in resp_post.url or 'error' in resp_post.url.lower():
            print(f"[REQUESTS] ❌ CarJet retornou erro na URL: {resp_post.url}", file=sys.stderr, flush=True)
            print(f"[REQUESTS] Possíveis causas: datas inválidas, localização incorreta, ou bloqueio", file=sys.stderr, flush=True)
            return []
        
        # Verificar se ficou na homepage (não navegou)
        if '/index.htm' in resp_post.url and '/do/list/' not in resp_post.url:
            print(f"[REQUESTS] ❌ Não navegou para página de resultados", file=sys.stderr, flush=True)
            return []
        
        # PASSO 3: Extrair URL de redirect do HTML (se ainda não estiver em /do/list/)
        if '/do/list/' not in resp_post.url:
            redirect_url = extract_redirect_url(resp_post.text)
        else:
            # Já está na página de resultados!
            redirect_url = resp_post.url.replace('https://www.carjet.com', '')
        
        if not redirect_url:
            print("[REQUESTS] ⚠️ Não encontrou URL de redirect")
            # Salvar HTML para debug
            try:
                with open('carjet_no_redirect_debug.html', 'w', encoding='utf-8') as f:
                    f.write(resp_post.text)
                print("[REQUESTS] 💾 HTML salvo em: carjet_no_redirect_debug.html", file=sys.stderr, flush=True)
            except:
                pass
            return []
        
        full_redirect_url = f'https://www.carjet.com{redirect_url}'
        print(f"[REQUESTS] Redirect URL: {redirect_url[:100]}...")
        
        # PASSO 4: POLLING - Fazer GET múltiplas vezes até resultados aparecerem
        max_attempts = 8
        delays = [4, 5, 6, 7, 8, 9, 10, 12]  # Total: ~61s
        
        html_results = None
        
        for attempt in range(max_attempts):
            delay = delays[attempt] if attempt < len(delays) else 10
            print(f"[REQUESTS] Tentativa {attempt + 1}/{max_attempts} - aguardando {delay}s...")
            time.sleep(delay)
            
            # GET com cookies da sessão (automático)
            resp_results = session.get(full_redirect_url, timeout=15)
            html = resp_results.text
            
            print(f"[REQUESTS] HTML recebido: {len(html)} bytes", file=sys.stderr, flush=True)
            
            # Verificar se ainda é página de loading
            # IMPORTANTE: Não usar len(html) porque a página de loading pode ser grande (200KB+)
            # Em vez disso, verificar se há CARROS no HTML
            loading_indicators = [
                'A carregar...',
                'Procurando',
                'Searching',
                'Waiting',
                'Please wait',
                'Aguarde',
                'Cargando',
            ]
            
            has_loading_text = any(indicator in html for indicator in loading_indicators)
            
            # Verificar se há elementos de carros no HTML (melhor indicador)
            has_car_cards = (
                'class="carCardWeb"' in html or
                'class="resultado-oferta"' in html or
                'class="price pr-euros"' in html or
                '<div class="car-card' in html
            )
            
            is_loading = has_loading_text or not has_car_cards
            
            if is_loading:
                print(f"[REQUESTS] ⏳ Ainda a processar... (loading={has_loading_text}, cards={has_car_cards})", file=sys.stderr, flush=True)
                if attempt < max_attempts - 1:
                    continue
                else:
                    print(f"[REQUESTS] ⚠️ Timeout após {max_attempts} tentativas", file=sys.stderr, flush=True)
                    # Salvar HTML para debug
                    with open('carjet_timeout_debug.html', 'w', encoding='utf-8') as f:
                        f.write(html)
                    print("[REQUESTS] HTML salvo em: carjet_timeout_debug.html", file=sys.stderr, flush=True)
                    return []
            else:
                # HTML com carros = resultados prontos!
                print(f"[REQUESTS] ✅ Resultados prontos! (tentativa {attempt + 1}, cards encontrados)", file=sys.stderr, flush=True)
                html_results = html
                break
        
        if not html_results:
            return []
        
        # PASSO 5: Parse do HTML
        print("[REQUESTS] Fazendo parse do HTML...")
        
        # Usar parse completo do carjet_direct.py se disponível
        if HAS_CARJET_PARSE:
            cars = parse_carjet_html_complete(html_results)
            print(f"[REQUESTS] ✅ {len(cars)} carros encontrados (parse completo)")
        else:
            # Fallback para parse simples
            cars = parse_cars_simple(html_results)
            print(f"[REQUESTS] ✅ {len(cars)} carros encontrados (parse simples)")
        
        return cars
        
    except Exception as e:
        print(f"[REQUESTS] ❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return []


def parse_cars_simple(html: str) -> List[Dict[str, Any]]:
    """
    Parse COMPLETO do HTML do CarJet
    Copiado de carjet_direct.py parse_carjet_html_complete()
    """
    items = []
    
    try:
        soup = BeautifulSoup(html, 'lxml')
        
        # Procurar blocos de carros
        car_blocks = (
            soup.find_all('article') or
            soup.find_all('div', class_=lambda x: x and ('car' in str(x).lower() or 'auto' in str(x).lower() or 'result' in str(x).lower()) if x else False)
        )
        
        print(f"[PARSE] {len(car_blocks)} blocos encontrados")
        
        for idx, block in enumerate(car_blocks):
            try:
                # Nome do carro
                car_name = ''
                for tag in block.find_all(['h3', 'h4', 'span', 'div']):
                    text = tag.get_text(strip=True)
                    # Verificar se parece nome de carro (tem marca conhecida)
                    if any(brand in text.lower() for brand in ['fiat', 'renault', 'peugeot', 'citroen', 'toyota', 'ford', 'vw', 'volkswagen', 'opel', 'seat', 'hyundai', 'kia', 'nissan', 'mercedes', 'bmw', 'audi', 'mini', 'jeep', 'dacia', 'skoda', 'mazda', 'mitsubishi', 'honda', 'suzuki']):
                        car_name = text
                        
                        # LIMPEZA COMPLETA do nome do carro
                        # 1. Remover "ou similar" / "or similar" e tudo depois (pode estar grudado sem espaço)
                        car_name = re.sub(r'(ou\s*similar|or\s*similar).*$', '', car_name, flags=re.IGNORECASE)
                        
                        # 2. Remover categorias após pipe |
                        car_name = re.sub(r'\s*\|\s*.*$', '', car_name)
                        
                        # 3. Remover categorias de tamanho (Pequeno, Médio, Grande, etc)
                        car_name = re.sub(r'(pequeno|médio|medio|grande|compacto|economico|econômico|familiar|luxo|premium|standard|suvs|mini|comp)', '', car_name, flags=re.IGNORECASE)
                        
                        # 4. Remover palavras em inglês (Small, Medium, Large, etc)
                        car_name = re.sub(r'(small|medium|large|compact|economy|luxury|premium|suv|mini)', '', car_name, flags=re.IGNORECASE)
                        
                        # 5. Normalizar espaços múltiplos
                        car_name = re.sub(r'\s+', ' ', car_name).strip()
                        break
                
                if not car_name:
                    continue
                
                # Supplier - PRIORIDADE 1: atributo data-prv
                supplier = 'CarJet'
                data_prv = block.get('data-prv', '').strip()
                if data_prv:
                    # Normalizar supplier se função disponível
                    if HAS_CARJET_PARSE:
                        supplier = normalize_supplier(data_prv)
                    else:
                        supplier = data_prv
                
                # PRIORIDADE 2: procurar por logo de supplier (fallback)
                if supplier == 'CarJet':
                    img_tags_supplier = block.find_all('img')
                    for img in img_tags_supplier:
                        src = img.get('src', '')
                        if '/logo' in src.lower() or 'logo_' in src.lower():
                            # Extrair código do supplier do nome do logo (ex: logo_GMO1.png → GMO1)
                            logo_match = re.search(r'logo[_-]([A-Z0-9]+)', src, re.IGNORECASE)
                            if logo_match:
                                supplier_code = logo_match.group(1)
                                if HAS_CARJET_PARSE:
                                    supplier = normalize_supplier(supplier_code)
                                else:
                                    # Fallback sem normalize_supplier
                                    supplier = supplier_code
                            break
                
                # Preço - procurar .price.pr-euros
                price = '€0.00'
                
                for span_tag in block.find_all('span'):
                    classes = span_tag.get('class', [])
                    if not classes:
                        continue
                    
                    # Verificar se tem 'price' E 'pr-euros' MAS NÃO tem 'day' nem 'old-price'
                    has_price = 'price' in classes
                    has_pr_euros = 'pr-euros' in classes
                    has_day = any('day' in c for c in classes)
                    has_old = any('old' in c for c in classes)
                    
                    if has_price and has_pr_euros and not has_day and not has_old:
                        text = span_tag.get_text(strip=True)
                        all_matches = re.findall(r'([\d.,]+)\s*€', text)
                        if all_matches:
                            try:
                                price_str = all_matches[-1]  # Último preço (com desconto)
                                # Normalizar formato europeu
                                if ',' in price_str and '.' in price_str:
                                    price_str = price_str.replace('.', '').replace(',', '.')
                                elif ',' in price_str:
                                    price_str = price_str.replace(',', '.')
                                
                                price_val = float(price_str)
                                if 10 < price_val < 10000:
                                    price = f'{price_val:.2f} €'
                                    break
                            except:
                                pass
                
                if price == '€0.00':
                    continue  # Skip carros sem preço
                
                # Foto
                photo = ''
                img_tags = block.find_all('img')
                for img in img_tags:
                    src = img.get('src', '') or img.get('data-src', '')
                    if '/logo' not in src.lower() and 'logo_' not in src.lower():
                        if '/car' in src.lower() or '/vehicle' in src.lower() or src:
                            photo = src if src.startswith('http') else f'https://www.carjet.com{src}'
                            break
                
                # Transmissão
                transmission = 'Manual'
                car_lower = car_name.lower()
                auto_patterns = [r'\bauto\b', r'\baut\.\b', r'automatic', r'automático', r'automatico']
                if any(re.search(pattern, car_lower) for pattern in auto_patterns):
                    transmission = 'Automatic'
                elif any(word in car_lower for word in ['electric', 'e-', 'hybrid', 'híbrido']):
                    transmission = 'Automatic'
                
                # Categoria (simplificada)
                category = 'ECONOMY'
                if 'mini' in car_lower or '500' in car_lower or 'aygo' in car_lower:
                    category = 'MINI Auto' if transmission == 'Automatic' else 'MINI 4 Lugares'
                elif 'suv' in car_lower or 'qashqai' in car_lower or '3008' in car_lower:
                    category = 'SUV Auto' if transmission == 'Automatic' else 'SUV'
                elif '7' in car_lower or 'sharan' in car_lower or 'galaxy' in car_lower:
                    category = '7 Lugares Auto' if transmission == 'Automatic' else '7 Lugares'
                elif transmission == 'Automatic':
                    category = 'ECONOMY Auto'
                
                items.append({
                    'id': idx,
                    'car': car_name,
                    'car_name': car_name,
                    'supplier': supplier,
                    'price': price,
                    'category': category,
                    'transmission': transmission,
                    'photo': photo,
                    'currency': 'EUR',
                    'link': '',
                })
                
            except Exception as e:
                continue
        
        print(f"[PARSE] {len(items)} items válidos")
        
    except Exception as e:
        print(f"[PARSE ERROR] {e}")
        import traceback
        traceback.print_exc()
    
    return items


if __name__ == '__main__':
    from datetime import timedelta
    
    start_dt = datetime.now() + timedelta(days=7)
    end_dt = start_dt + timedelta(days=1)
    
    print("=" * 80)
    print("🧪 TESTE COM REQUESTS + SESSÃO")
    print("=" * 80)
    
    results = scrape_carjet_requests('Albufeira', start_dt, end_dt)
    
    print("\n" + "=" * 80)
    print(f"RESULTADO: {len(results)} carros")
    print("=" * 80)
    
    for car in results[:5]:
        print(f"- {car['car']}: {car['price']}")
