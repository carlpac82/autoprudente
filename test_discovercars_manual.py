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
        # Add flags to prevent detection and resizing
        browser = await p.chromium.launch(
            headless=False,  # VISIBLE BROWSER
            devtools=False,  # NO DEVTOOLS (prevents resizing)
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--start-maximized',  # Start maximized
            ]
        )
        
        # Create context with DESKTOP viewport (more stable)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},  # Desktop Full HD
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
        print("1. ❌ ACEITAR/REJEITAR cookies")
        print("2. 📍 Clicar na caixa 'Local de levantamento'")
        print("3. ⌨️  Digitar: Aeroporto de Faro (FAO)")
        print("4. 🖱️  Escolher do dropdown menu")
        print("5. 📅 Inserir datas e hora")
        print("6. 🔍 Clicar em 'Pesquisar agora'")
        print("\n🎥 VOU GRAVAR SCREENSHOTS A CADA 3 SEGUNDOS!")
        print("\n" + "="*60)
        print("💡 Quando terminares, fecha o browser ou pressiona Ctrl+C aqui")
        print("="*60 + "\n")
        
        # Keep browser open until user closes it or presses Ctrl+C
        # Take screenshots every 3 seconds to record the process
        screenshot_counter = 0
        try:
            while True:
                await asyncio.sleep(3)
                
                # Take screenshot
                try:
                    screenshot_path = f'/tmp/manual_demo_{screenshot_counter:03d}.png'
                    await page.screenshot(path=screenshot_path, full_page=True)
                    print(f"📸 Screenshot {screenshot_counter} salvo: {screenshot_path}")
                    screenshot_counter += 1
                except:
                    pass
                
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
