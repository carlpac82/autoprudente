"""
Script de teste para verificar estrutura HTML atual do CarJet
"""
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
import uuid
from bs4 import BeautifulSoup

def test_carjet_structure():
    """Testa a estrutura HTML atual do CarJet"""
    
    # Datas de teste
    start_dt = datetime.now() + timedelta(days=7)
    end_dt = start_dt + timedelta(days=1)
    
    pickup_date = start_dt.strftime('%d/%m/%Y %H:%M')
    return_date = end_dt.strftime('%d/%m/%Y %H:%M')
    session_id = str(uuid.uuid4())
    
    form_data = {
        'frmDestino': 'ABF01',  # Albufeira
        'frmDestinoFinal': '',
        'frmFechaRecogida': pickup_date,
        'frmFechaDevolucion': return_date,
        'frmHasAge': 'False',
        'frmEdad': '35',
        'frmPrvNo': '',
        'frmMoneda': 'EUR',
        'frmMonedaForzada': '',
        'frmJsonFilterInfo': '',
        'frmTipoVeh': 'CAR',
        'idioma': 'PT',
        'frmSession': session_id,
        'frmDetailCode': ''
    }
    
    encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')
    url = 'https://www.carjet.com/do/list/pt'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'pt-PT,pt;q=0.9',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Referer': 'https://www.carjet.com/aluguel-carros/index.htm',
        'Origin': 'https://www.carjet.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    print("=" * 80)
    print("🔍 TESTE DE ESTRUTURA HTML DO CARJET")
    print("=" * 80)
    print(f"📅 Datas: {pickup_date} → {return_date}")
    print(f"📍 Local: Albufeira (ABF01)")
    print()
    
    try:
        # POST inicial
        print("📤 Fazendo POST para CarJet...")
        req = urllib.request.Request(url, data=encoded_data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
        
        print(f"✅ HTML recebido: {len(html)} bytes")
        
        # Verificar se tem redirect
        if 'window.location.replace' in html:
            import re
            import time
            
            pattern = r"window\.location\.replace\('([^']+)'\)"
            match = re.search(pattern, html)
            
            if match:
                redirect_url = match.group(1)
                print(f"🔄 Redirect detectado: {redirect_url[:80]}...")
                print("⏳ Aguardando 4 segundos...")
                time.sleep(4)
                
                full_url = f'https://www.carjet.com{redirect_url}'
                
                # Headers com cookies para forçar EUR
                headers_with_cookies = dict(headers)
                headers_with_cookies['Cookie'] = 'monedaForzada=EUR; moneda=EUR; currency=EUR; country=PT; idioma=PT; lang=pt'
                
                req2 = urllib.request.Request(full_url, headers=headers_with_cookies, method='GET')
                
                with urllib.request.urlopen(req2, timeout=30) as response2:
                    html = response2.read().decode('utf-8')
                
                print(f"✅ HTML final: {len(html)} bytes")
        
        # Parse com BeautifulSoup
        print("\n" + "=" * 80)
        print("📊 ANÁLISE DA ESTRUTURA HTML")
        print("=" * 80)
        
        soup = BeautifulSoup(html, 'lxml')
        
        # 1. Verificar <article> tags
        articles = soup.find_all('article')
        print(f"\n1️⃣  <article> tags encontrados: {len(articles)}")
        if articles:
            print(f"   Exemplo de classes: {articles[0].get('class')}")
            print(f"   Exemplo de atributos: {articles[0].attrs}")
        
        # 2. Verificar divs com classes de carro
        car_divs = soup.find_all('div', class_=lambda x: x and ('car' in str(x).lower() or 'auto' in str(x).lower() or 'result' in str(x).lower()) if x else False)
        print(f"\n2️⃣  <div> com classes 'car/auto/result': {len(car_divs)}")
        if car_divs:
            print(f"   Exemplo de classes: {car_divs[0].get('class')}")
        
        # 3. Verificar spans com preços
        price_spans = soup.find_all('span', class_=lambda x: x and 'price' in str(x).lower() if x else False)
        print(f"\n3️⃣  <span> com classe 'price': {len(price_spans)}")
        if price_spans:
            for i, span in enumerate(price_spans[:5]):
                print(f"   [{i}] Classes: {span.get('class')} | Texto: {span.get_text(strip=True)[:50]}")
        
        # 4. Verificar h3/h4 com nomes de carros
        car_names = []
        for tag in soup.find_all(['h3', 'h4', 'span', 'div']):
            text = tag.get_text(strip=True)
            if any(brand in text.lower() for brand in ['fiat', 'renault', 'peugeot', 'ford', 'vw', 'volkswagen', 'opel']):
                car_names.append(text[:80])
                if len(car_names) >= 5:
                    break
        
        print(f"\n4️⃣  Nomes de carros encontrados: {len(car_names)}")
        for i, name in enumerate(car_names[:5]):
            print(f"   [{i}] {name}")
        
        # 5. Verificar imagens
        car_images = []
        for img in soup.find_all('img'):
            src = img.get('src', '') or img.get('data-src', '')
            alt = img.get('alt', '')
            if '/car' in src.lower() or '/vehicle' in src.lower() or any(brand in alt.lower() for brand in ['fiat', 'renault', 'peugeot']):
                car_images.append({'src': src[:80], 'alt': alt[:50]})
                if len(car_images) >= 3:
                    break
        
        print(f"\n5️⃣  Imagens de carros encontradas: {len(car_images)}")
        for i, img in enumerate(car_images[:3]):
            print(f"   [{i}] src: {img['src']}")
            print(f"       alt: {img['alt']}")
        
        # 6. Salvar HTML para análise manual
        output_file = '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay/carjet_html_debug.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"\n💾 HTML completo salvo em: {output_file}")
        print("   Abre este ficheiro no browser para ver a estrutura completa")
        
        # 7. Verificar se há mensagens de erro/bloqueio
        print("\n" + "=" * 80)
        print("🔒 VERIFICAÇÃO DE BLOQUEIO")
        print("=" * 80)
        
        error_indicators = [
            ('captcha', 'CAPTCHA detectado'),
            ('blocked', 'Acesso bloqueado'),
            ('access denied', 'Acesso negado'),
            ('too many requests', 'Rate limit'),
            ('503', 'Serviço indisponível'),
            ('cloudflare', 'Proteção Cloudflare'),
        ]
        
        html_lower = html.lower()
        blocked = False
        for indicator, message in error_indicators:
            if indicator in html_lower:
                print(f"⚠️  {message} - '{indicator}' encontrado no HTML")
                blocked = True
        
        if not blocked:
            print("✅ Nenhum indicador de bloqueio encontrado")
        
        print("\n" + "=" * 80)
        print("✅ TESTE COMPLETO!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_carjet_structure()
