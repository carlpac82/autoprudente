#!/usr/bin/env python3
"""
Testar distribuição de grupos do Playwright
"""
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, timedelta
from carjet_direct import parse_carjet_html_complete
from collections import Counter

async def main():
    location = "Albufeira"
    start_dt = datetime.now() + timedelta(days=2)
    end_dt = start_dt + timedelta(days=7)
    
    pickup_date = start_dt.strftime('%d/%m/%Y %H:%M')
    return_date = end_dt.strftime('%d/%m/%Y %H:%M')
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            viewport={'width': 390, 'height': 844},
            device_scale_factor=3.0,
            is_mobile=True,
            has_touch=True,
            locale='pt-PT',
            timezone_id='Europe/Lisbon'
        )
        page = await context.new_page()
        
        form_url = 'https://www.carjet.com/aluguel-carros/index.htm'
        await page.goto(form_url, wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(2000)
        
        # Rejeitar cookies
        try:
            await page.evaluate("""
                const btns = [...document.querySelectorAll('button, a')];
                for (let btn of btns) {
                    const text = btn.textContent.toLowerCase();
                    if (text.includes('rejeitar') || text.includes('recusar') || text.includes('reject')) {
                        btn.click();
                        break;
                    }
                }
            """)
            await page.wait_for_timeout(500)
        except:
            pass
        
        # Escrever local
        await page.fill('#pickup', 'Albufeira')
        await page.wait_for_timeout(2000)
        
        # Clicar dropdown
        try:
            await page.click('#recogida_lista li:first-child a', timeout=3000)
        except:
            pass
        
        # Preencher datas
        await page.evaluate("""
            (dates) => {
                function fill(sel, val) {
                    const el = document.querySelector(sel);
                    if (el) { 
                        el.value = val; 
                        el.dispatchEvent(new Event('input', {bubbles: true}));
                        el.dispatchEvent(new Event('change', {bubbles: true}));
                        el.dispatchEvent(new Event('blur', {bubbles: true}));
                        return true;
                    }
                    return false;
                }
                
                fill('input[id="fechaRecogida"]', dates.pickup);
                fill('input[id="fechaDevolucion"]', dates.return);
                fill('select[id="fechaRecogidaSelHour"]', '15:00');
                fill('select[id="fechaDevolucionSelHour"]', '15:00');
            }
        """, {'pickup': pickup_date, 'return': return_date})
        
        await page.wait_for_timeout(1000)
        
        # Submit usando JavaScript
        await page.evaluate("""
            const btn = document.querySelector('button[type="submit"]') || 
                        document.querySelector('input[type="submit"]') ||
                        document.querySelector('.btn-search');
            if (btn) btn.click();
        """)
        
        await page.wait_for_url('**/do/list/**', timeout=45000)
        await page.wait_for_timeout(5000)
        
        html = await page.content()
        await browser.close()
        
        # Parse
        items = parse_carjet_html_complete(html)
        
        # Analisar grupos
        groups = [item.get('group', 'N/A') for item in items]
        counter = Counter(groups)
        
        print('📊 DISTRIBUIÇÃO POR GRUPOS:')
        for group, count in sorted(counter.items()):
            print(f'  {group}: {count} carros')
        
        print(f'\n✅ Total: {len(items)} carros')
        print(f'📋 HTML size: {len(html)} bytes')
        
        # Mostrar exemplos por grupo
        print('\n📋 EXEMPLOS POR GRUPO:')
        for group in sorted(set(groups)):
            group_cars = [item for item in items if item.get('group') == group]
            if group_cars:
                car = group_cars[0]
                print(f"\n{group}:")
                print(f"  Nome: {car.get('car_name')}")
                print(f"  Preço: {car.get('price')} {car.get('currency')}")
                print(f"  Supplier: {car.get('supplier')}")

asyncio.run(main())
