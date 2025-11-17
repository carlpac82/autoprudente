#!/usr/bin/env python3
"""
Testar o filtro filter_automatic_only
"""
import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from main import filter_automatic_only
from carjet_direct import parse_carjet_html_complete
from collections import Counter
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, timedelta

async def test():
    location = "Albufeira"
    start_dt = datetime.now() + timedelta(days=2)
    end_dt = start_dt + timedelta(days=7)
    
    pickup_date_str = start_dt.strftime('%d/%m/%Y')
    return_date_str = end_dt.strftime('%d/%m/%Y')
    
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
        await page.goto(form_url, wait_until='networkidle', timeout=30000)
        
        # Rejeitar cookies
        try:
            await page.evaluate("""
                const btns = [...document.querySelectorAll('button, a')];
                for (let btn of btns) {
                    if (btn.textContent.toLowerCase().includes('rejeitar')) {
                        btn.click();
                        break;
                    }
                }
            """)
            await page.wait_for_timeout(500)
        except:
            pass
        
        await page.fill('#pickup', 'Albufeira')
        await page.wait_for_timeout(2000)
        
        try:
            await page.click('#recogida_lista li:first-child a', timeout=3000)
        except:
            pass
        
        await page.evaluate("""
            (dates) => {
                function fill(sel, val) {
                    const el = document.querySelector(sel);
                    if (el) { 
                        el.value = val; 
                        el.dispatchEvent(new Event('input', {bubbles: true}));
                        el.dispatchEvent(new Event('change', {bubbles: true}));
                        return true;
                    }
                    return false;
                }
                fill('input[id="fechaRecogida"]', dates.pickup);
                fill('input[id="fechaDevolucion"]', dates.return);
                fill('select[id="fechaRecogidaSelHour"]', '15:00');
                fill('select[id="fechaDevolucionSelHour"]', '15:00');
            }
        """, {'pickup': pickup_date_str, 'return': return_date_str})
        
        await page.wait_for_timeout(1000)
        
        await page.evaluate("""
            const btn = document.querySelector('button[type="submit"]');
            if (btn) btn.click();
        """)
        
        await page.wait_for_load_state('networkidle', timeout=60000)
        await page.wait_for_timeout(3000)
        
        html = await page.content()
        await browser.close()
        
        # Parse
        items_before = parse_carjet_html_complete(html)
        
        print(f'📊 ANTES DO FILTRO: {len(items_before)} carros')
        groups_before = Counter([item.get('group', 'N/A') for item in items_before])
        for group, count in sorted(groups_before.items()):
            print(f'  {group}: {count}')
        
        # Aplicar filtro
        items_after = filter_automatic_only(items_before)
        
        print(f'\n📊 DEPOIS DO FILTRO: {len(items_after)} carros')
        groups_after = Counter([item.get('group', 'N/A') for item in items_after])
        for group, count in sorted(groups_after.items()):
            print(f'  {group}: {count}')
        
        print(f'\n🔧 REMOVIDOS: {len(items_before) - len(items_after)} carros')
        
        # Mostrar exemplos do que foi removido
        removed = [item for item in items_before if item not in items_after]
        if removed:
            print(f'\n❌ EXEMPLOS DE CARROS REMOVIDOS (primeiros 5):')
            for item in removed[:5]:
                print(f'  - {item.get("car_name")} ({item.get("group")}) - Trans: {item.get("transmission")}')

asyncio.run(test())
