#!/usr/bin/env python3
"""
Teste Playwright - anti-detecção de bot
"""

import asyncio
from playwright.async_api import async_playwright

async def test_carjet():
    print("=" * 60)
    print("TESTE PLAYWRIGHT - CarJet")
    print("Datas: 15/04/2025 - 22/04/2025")
    print("=" * 60)
    
    async with async_playwright() as p:
        # Lançar browser
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        # Emulação iPhone
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            viewport={'width': 390, 'height': 844},
            device_scale_factor=3.0,
            is_mobile=True,
            has_touch=True,
        )
        
        page = await context.new_page()
        
        # Remover webdriver flag
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("\n[1] Abrindo CarJet...")
        await page.goto('https://www.carjet.com/aluguel-carros/index.htm', timeout=60000)
        await page.wait_for_timeout(3000)
        
        # Remover cookies popup
        print("[2] Removendo cookies popup...")
        await page.evaluate("""
            document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=consent], [id*=didomi]').forEach(el => el.remove());
            document.body.style.overflow = 'auto';
        """)
        
        # Preencher local
        print("[3] Preenchendo local: Faro...")
        await page.fill('#pickup', 'Faro')
        await page.wait_for_timeout(2000)
        
        # Clicar no dropdown
        print("[4] Clicando no dropdown...")
        try:
            await page.click('#recogida_lista li:first-child a', timeout=5000)
            print("    ✅ Dropdown clicado!")
        except:
            print("    ⚠️ Tentando via JS...")
            await page.evaluate("""
                const items = document.querySelectorAll('#recogida_lista li');
                for (let item of items) {
                    if (item.offsetParent !== null) {
                        item.click();
                        break;
                    }
                }
            """)
        
        await page.wait_for_timeout(1000)
        
        # Preencher datas
        print("[5] Preenchendo datas...")
        await page.evaluate("""
            const pickup = document.querySelector('#fechaRecogida');
            const dropoff = document.querySelector('#fechaDevolucion') || document.querySelector('#fechaEntrega');
            if (pickup) { pickup.value = '15/04/2025'; pickup.dispatchEvent(new Event('change')); }
            if (dropoff) { dropoff.value = '22/04/2025'; dropoff.dispatchEvent(new Event('change')); }
            
            const h1 = document.querySelector('#fechaRecogidaSelHour');
            const h2 = document.querySelector('#fechaDevolucionSelHour') || document.querySelector('#fechaEntregaSelHour');
            if (h1) { h1.value = '15:00'; h1.dispatchEvent(new Event('change')); }
            if (h2) { h2.value = '15:00'; h2.dispatchEvent(new Event('change')); }
        """)
        
        # Verificar valores
        values = await page.evaluate("""
            () => ({
                pickup: document.querySelector('#pickup')?.value,
                recogida: document.querySelector('#recogida')?.value,
                fechaRecogida: document.querySelector('#fechaRecogida')?.value,
                fechaDevolucion: (document.querySelector('#fechaDevolucion') || document.querySelector('#fechaEntrega'))?.value,
            })
        """)
        print(f"    Valores: {values}")
        
        await page.wait_for_timeout(1000)
        
        # Submeter
        print("[6] Submetendo formulário...")
        await page.evaluate("document.querySelector('form').submit()")
        
        # Aguardar navegação
        print("[7] Aguardando resultado...")
        await page.wait_for_timeout(5000)
        
        url = page.url
        print(f"\n{'=' * 60}")
        print(f"URL FINAL: {url}")
        print(f"{'=' * 60}")
        
        if 'war=' in url:
            print(f"\n❌ Erro detectado (war=)")
        elif '/do/list/' in url:
            print(f"\n✅ Página de resultados!")
        
        print("\nPrima ENTER para fechar...")
        input()
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_carjet())
