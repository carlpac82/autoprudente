#!/usr/bin/env python3
"""
Script para capturar screenshots profissionais do website AUTOPRUDENTE
Requer: pip install playwright
Depois: playwright install chromium
"""

import asyncio
from playwright.async_api import async_playwright
import os

# URL do website (ajustar se necessário)
WEBSITE_URL = "https://carrental-api-bf8g.onrender.com"

# Screenshots a capturar
SCREENSHOTS = [
    {
        "name": "01_homepage",
        "url": "/",
        "title": "Homepage - Dashboard Principal",
        "wait_for": "text=Pesquisar Preços",
        "viewport": {"width": 1920, "height": 1080}
    },
    {
        "name": "02_search_form",
        "url": "/",
        "title": "Formulário de Pesquisa",
        "wait_for": "select[name='location']",
        "viewport": {"width": 1920, "height": 1080},
        "scroll_to": "select[name='location']"
    },
    {
        "name": "03_price_results",
        "url": "/",
        "title": "Resultados de Preços",
        "wait_for": "text=Pesquisar Preços",
        "viewport": {"width": 1920, "height": 1080},
        "scroll_to": "#resultsContainer"
    },
    {
        "name": "04_price_automation",
        "url": "/price-automation",
        "title": "Automação de Preços",
        "wait_for": "text=Automação de Preços",
        "viewport": {"width": 1920, "height": 1080}
    },
    {
        "name": "05_automated_prices_table",
        "url": "/price-automation",
        "title": "Tabela de Preços Automatizados",
        "wait_for": "text=Preços Automatizados",
        "viewport": {"width": 1920, "height": 1080},
        "scroll_to": "#priceTableContainer"
    },
    {
        "name": "06_history_tab",
        "url": "/price-automation",
        "title": "Histórico de Preços",
        "wait_for": "text=Histórico",
        "viewport": {"width": 1920, "height": 1080},
        "click": "button:has-text('Histórico')"
    },
    {
        "name": "07_automated_search_history",
        "url": "/price-automation",
        "title": "Histórico de Pesquisas Automatizadas",
        "wait_for": "text=Histórico",
        "viewport": {"width": 1920, "height": 1080},
        "click": ["button:has-text('Histórico')", "button:has-text('Preços Automatizados')"]
    },
    {
        "name": "08_ai_insights",
        "url": "/price-automation",
        "title": "AI Insights",
        "wait_for": "text=AI Insights",
        "viewport": {"width": 1920, "height": 1080},
        "scroll_to": "#aiInsightsButton"
    },
    {
        "name": "09_groups_management",
        "url": "/admin",
        "title": "Gestão de Grupos",
        "wait_for": "text=Grupos de Veículos",
        "viewport": {"width": 1920, "height": 1080}
    },
    {
        "name": "10_mobile_view",
        "url": "/",
        "title": "Vista Mobile",
        "wait_for": "text=Pesquisar Preços",
        "viewport": {"width": 390, "height": 844}
    }
]

async def capture_screenshots():
    """Capturar screenshots do website"""
    
    # Criar pasta para screenshots
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    print("=" * 80)
    print("📸 CAPTURANDO SCREENSHOTS DO WEBSITE AUTOPRUDENTE")
    print("=" * 80)
    print()
    
    async with async_playwright() as p:
        # Lançar browser
        browser = await p.chromium.launch(headless=True)
        
        # Criar contexto com credenciais (se necessário)
        context = await browser.new_context(
            locale='pt-PT',
            timezone_id='Europe/Lisbon'
        )
        
        # Adicionar cookies de autenticação se necessário
        # await context.add_cookies([{
        #     'name': 'session',
        #     'value': 'your-session-token',
        #     'domain': 'carrental-api-bf8g.onrender.com',
        #     'path': '/'
        # }])
        
        page = await context.new_page()
        
        for i, screenshot in enumerate(SCREENSHOTS, 1):
            try:
                print(f"{i}/{len(SCREENSHOTS)} 📸 {screenshot['title']}...")
                
                # Configurar viewport
                await page.set_viewport_size(screenshot['viewport'])
                
                # Navegar para URL
                url = f"{WEBSITE_URL}{screenshot['url']}"
                await page.goto(url, wait_until='networkidle', timeout=30000)
                
                # Aguardar elemento específico
                if 'wait_for' in screenshot:
                    await page.wait_for_selector(screenshot['wait_for'], timeout=10000)
                
                # Clicar em elementos se necessário
                if 'click' in screenshot:
                    clicks = screenshot['click'] if isinstance(screenshot['click'], list) else [screenshot['click']]
                    for selector in clicks:
                        await page.click(selector)
                        await page.wait_for_timeout(1000)
                
                # Scroll para elemento se necessário
                if 'scroll_to' in screenshot:
                    try:
                        element = await page.query_selector(screenshot['scroll_to'])
                        if element:
                            await element.scroll_into_view_if_needed()
                            await page.wait_for_timeout(500)
                    except:
                        pass
                
                # Aguardar um pouco para garantir que tudo carregou
                await page.wait_for_timeout(2000)
                
                # Capturar screenshot
                filename = f"{screenshots_dir}/{screenshot['name']}.png"
                await page.screenshot(path=filename, full_page=False)
                
                print(f"   ✅ Salvo: {filename}")
                
            except Exception as e:
                print(f"   ❌ Erro: {e}")
        
        await browser.close()
    
    print()
    print("=" * 80)
    print("✅ SCREENSHOTS CAPTURADOS COM SUCESSO!")
    print("=" * 80)
    print()
    print(f"📁 Pasta: {screenshots_dir}/")
    print(f"📸 Total: {len(SCREENSHOTS)} screenshots")
    print()
    print("📋 PRÓXIMOS PASSOS:")
    print("   1. Verificar screenshots na pasta 'screenshots/'")
    print("   2. Screenshots serão incluídos automaticamente nos PDFs")
    print("   3. Executar: python convert_to_pdf.py")
    print()

def main():
    """Executar captura de screenshots"""
    try:
        asyncio.run(capture_screenshots())
    except KeyboardInterrupt:
        print("\n⚠️  Captura cancelada pelo utilizador")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("\n💡 Dica: Certifica-te que:")
        print("   1. Playwright está instalado: pip install playwright")
        print("   2. Chromium está instalado: playwright install chromium")
        print("   3. Website está acessível")

if __name__ == "__main__":
    main()
