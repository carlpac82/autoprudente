#!/usr/bin/env python3
"""
Ver detalhes dos carros por grupo
"""
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, timedelta
from carjet_direct import parse_carjet_html_complete
from collections import defaultdict

async def main():
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
        """, {'pickup': pickup_date_str, 'return': return_date_str})
        
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
        
        # Agrupar por grupo
        by_group = defaultdict(list)
        for item in items:
            group = item.get('group', 'N/A')
            by_group[group].append(item)
        
        print('📊 CARROS POR GRUPO (ANTES DO FILTRO):')
        print('=' * 80)
        
        for group in sorted(by_group.keys()):
            cars = by_group[group]
            print(f'\n🏷️  GRUPO {group}: {len(cars)} carros')
            
            # Contar automáticos vs manuais
            auto_count = 0
            manual_count = 0
            
            for car in cars[:5]:  # Mostrar só 5 exemplos
                trans = car.get('transmission', 'N/A')
                name = car.get('car_name', 'N/A')
                
                if 'auto' in trans.lower():
                    auto_count += 1
                    trans_symbol = '🔵 AUTO'
                else:
                    manual_count += 1
                    trans_symbol = '⚪ MANUAL'
                
                print(f'   {trans_symbol} - {name[:50]}')
            
            if len(cars) > 5:
                print(f'   ... +{len(cars) - 5} carros')
            
            # Totais
            for car in cars[5:]:
                trans = car.get('transmission', 'N/A')
                if 'auto' in trans.lower():
                    auto_count += 1
                else:
                    manual_count += 1
            
            print(f'   📊 Total: {auto_count} automáticos, {manual_count} manuais')
        
        print(f'\n✅ Total geral: {len(items)} carros')

asyncio.run(main())
