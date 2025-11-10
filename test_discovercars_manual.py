#!/usr/bin/env python3
"""
Manual test - Open DiscoverCars in Chromium for manual demonstration
"""

import asyncio
from playwright.async_api import async_playwright

async def open_browser_for_manual_test():
    """Open browser and wait for manual interaction"""
    async with async_playwright() as p:
        # Launch browser in NON-headless mode (visible)
        browser = await p.chromium.launch(
            headless=False,  # VISIBLE BROWSER
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
            ]
        )
        
        # Create context with iPhone mobile
        context = await browser.new_context(
            viewport={'width': 390, 'height': 844},  # iPhone
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True
        )
        
        # Create page
        page = await context.new_page()
        
        # Navigate to DiscoverCars
        print("🌐 Navigating to DiscoverCars...")
        await page.goto('https://www.discovercars.com/pt', wait_until='domcontentloaded')
        await asyncio.sleep(2)
        
        print("\n" + "="*60)
        print("✅ Browser aberto!")
        print("="*60)
        print("\n📋 INSTRUÇÕES:")
        print("1. ❌ REJEITAR cookies")
        print("2. 📍 Clicar na caixa 'Local de levantamento'")
        print("3. ⌨️  Digitar: Aeroporto de Faro (FAO)")
        print("4. 🖱️  Escolher do dropdown menu")
        print("5. 📅 Inserir datas e hora")
        print("6. 🔍 Clicar em 'Pesquisar agora'")
        print("\n" + "="*60)
        print("💡 Quando terminares, fecha o browser ou pressiona Ctrl+C aqui")
        print("="*60 + "\n")
        
        # Keep browser open until user closes it or presses Ctrl+C
        try:
            # Wait indefinitely (until browser closed or Ctrl+C)
            while True:
                await asyncio.sleep(1)
                # Check if page is still alive
                try:
                    await page.evaluate('() => true')
                except:
                    print("\n🔴 Browser fechado!")
                    break
        except KeyboardInterrupt:
            print("\n\n🛑 Interrompido pelo utilizador")
        finally:
            await browser.close()
            print("✅ Browser fechado")

if __name__ == "__main__":
    print("\n🚀 A abrir Chromium em modo iPhone mobile...\n")
    asyncio.run(open_browser_for_manual_test())
