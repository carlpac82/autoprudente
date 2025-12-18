#!/usr/bin/env python3
"""
Debug script para analisar estrutura HTML atual do CarJet
"""
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import sys
from datetime import datetime, timedelta

def analyze_carjet_html():
    """Captura e analisa HTML do CarJet"""
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        
        # iPhone 13 Pro user agent
        context = browser.new_context(
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            viewport={'width': 390, 'height': 844},
            locale='pt-PT',
            timezone_id='Europe/Lisbon'
        )
        
        page = context.new_page()
        
        # Acessa homepage
        print("📱 Acessando CarJet...", file=sys.stderr)
        page.goto('https://www.carjet.com/aluguel-carros/index.htm', wait_until='networkidle')
        
        # Rejeita cookies
        try:
            page.click('button:has-text("Rejeitar")', timeout=3000)
            print("✅ Cookies rejeitados", file=sys.stderr)
        except:
            print("⚠️  Sem popup de cookies", file=sys.stderr)
        
        # Preenche formulário
        page.fill('input[name="txt-rent-pickup"]', 'Albufeira')
        page.wait_for_timeout(500)
        
        # Clica no dropdown
        page.evaluate("""
            document.querySelector('.uiListTxt').click();
        """)
        page.wait_for_timeout(500)
        
        # Datas
        start_date = datetime.now() + timedelta(days=2)
        end_date = start_date + timedelta(days=2)
        
        page.fill('input[name="pickUpDate"]', start_date.strftime('%d/%m/%Y'))
        page.fill('input[name="dropOffDate"]', end_date.strftime('%d/%m/%Y'))
        page.select_option('select[name="pickUpTime"]', '15:00')
        page.select_option('select[name="dropOffTime"]', '15:00')
        
        print("📝 Formulário preenchido", file=sys.stderr)
        
        # Submete
        try:
            page.click('button[type="submit"]', timeout=5000)
            print("🔄 Formulário submetido", file=sys.stderr)
        except:
            print("⚠️  Submit via JS", file=sys.stderr)
            page.evaluate("document.querySelector('form').submit();")
        
        # Aguarda página carregar
        try:
            page.wait_for_url('**/do/list/**', timeout=10000)
            print("✅ Navegou para /do/list/", file=sys.stderr)
        except:
            print("⚠️  Não navegou para /do/list/", file=sys.stderr)
        
        # Aguarda JavaScript processar
        print("⏳ Aguardando JavaScript...", file=sys.stderr)
        page.wait_for_timeout(8000)
        
        # Captura HTML
        html = page.content()
        print(f"📄 HTML capturado: {len(html)} bytes", file=sys.stderr)
        
        # Salva HTML
        with open('carjet_debug_structure.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("💾 HTML salvo: carjet_debug_structure.html", file=sys.stderr)
        
        # Analisa estrutura
        soup = BeautifulSoup(html, 'html.parser')
        
        print("\n" + "="*80, file=sys.stderr)
        print("🔍 ANÁLISE DA ESTRUTURA", file=sys.stderr)
        print("="*80, file=sys.stderr)
        
        # Procura por diferentes seletores
        selectors = [
            "article",
            "article.car",
            "li.result",
            "li.car",
            ".car-item",
            ".result-row",
            "section.newcarlist article",
            ".newcarlist article",
            "[class*='car']",
            "[class*='result']",
            "[class*='vehicle']",
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                print(f"\n✅ {selector}: {len(elements)} elementos", file=sys.stderr)
                
                # Analisa primeiro elemento
                first = elements[0]
                print(f"   Classes: {first.get('class')}", file=sys.stderr)
                
                # Procura preços
                price_selectors = [
                    ".price.pr-euros",
                    ".pr-euros",
                    ".price",
                    "[class*='price']",
                    "[class*='Price']",
                    "span.price",
                ]
                
                for ps in price_selectors:
                    prices = first.select(ps)
                    if prices:
                        print(f"   💰 {ps}: {len(prices)} encontrados", file=sys.stderr)
                        for i, p in enumerate(prices[:3]):
                            print(f"      [{i}] {p.get('class')} = '{p.get_text(strip=True)[:50]}'", file=sys.stderr)
                
                # Procura spans
                spans = first.find_all('span')
                print(f"   📊 Spans: {len(spans)} encontrados", file=sys.stderr)
                if spans:
                    for i, sp in enumerate(spans[:5]):
                        print(f"      [{i}] {sp.get('class')} = '{sp.get_text(strip=True)[:50]}'", file=sys.stderr)
        
        browser.close()
        
        print("\n✅ Análise completa!", file=sys.stderr)

if __name__ == '__main__':
    analyze_carjet_html()
