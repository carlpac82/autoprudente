#!/usr/bin/env python3
"""
Teste do Playwright - Verificar se consegue fazer scraping do CarJet
"""
import asyncio
from datetime import datetime, timedelta
from playwright.async_api import async_playwright

async def test_playwright_carjet():
    location = "Albufeira"
    start_dt = datetime.now() + timedelta(days=2)
    end_dt = start_dt + timedelta(days=7)
    
    pickup_code = 'ABF01'  # Albufeira
    
    print(f"🎭 TESTE PLAYWRIGHT CARJET")
    print(f"Location: {location}")
    print(f"Dates: {start_dt.strftime('%d/%m/%Y')} - {end_dt.strftime('%d/%m/%Y')}")
    print("=" * 80)
    
    try:
        async with async_playwright() as p:
            print("🚀 Iniciando Chromium...")
            browser = await p.chromium.launch(headless=False)  # headless=False para ver o que acontece
            
            # EMULAR iPhone 13 Pro (IGUAL AO SELENIUM!)
            print("📱 Emulando iPhone 13 Pro...")
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
            
            # Ir para a página do form
            form_url = 'https://www.carjet.com/aluguel-carros/index.htm'
            print(f"🌐 Navegando para {form_url}")
            await page.goto(form_url, wait_until='domcontentloaded', timeout=30000)
            print("✅ Página carregada")
            
            await page.wait_for_timeout(2000)
            
            # Rejeitar cookies
            print("🍪 Rejeitando cookies...")
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
            
            # PASSO 1: Escrever local e aguardar dropdown
            print(f"📝 PASSO 1: Escrevendo local '{pickup_code}'...")
            await page.fill('#pickup', 'Albufeira')
            print("✅ Local digitado")
            
            # PASSO 2: Aguardar e clicar no dropdown
            print(f"⏳ PASSO 2: Aguardando dropdown...")
            await page.wait_for_timeout(2000)
            
            try:
                print("🔍 Procurando dropdown...")
                await page.click('#recogida_lista li:first-child a', timeout=3000)
                print("✅ Dropdown clicado")
            except:
                print("⚠️ Dropdown não apareceu via selector, tentando JS...")
                await page.evaluate("""
                    const items = document.querySelectorAll('#recogida_lista li');
                    for (let item of items) {
                        if (item.offsetParent !== null) {
                            item.click();
                            break;
                        }
                    }
                """)
                print("✅ Dropdown clicado (JS)")
            
            await page.wait_for_timeout(1000)
            
            # PASSO 3: Preencher datas e horas (DEPOIS do dropdown!)
            print(f"📅 PASSO 3: Preenchendo datas e horas...")
            pickup_date_str = start_dt.strftime('%d/%m/%Y')
            return_date_str = end_dt.strftime('%d/%m/%Y')
            
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
            print("✅ Datas e horas preenchidas")
            
            await page.wait_for_timeout(500)
            
            # PASSO 4: Submeter form
            print(f"📤 PASSO 4: Submetendo formulário...")
            await page.evaluate("document.querySelector('form').submit()")
            
            # Aguardar navegação
            print(f"⏳ Aguardando navegação para /do/list/...")
            await page.wait_for_url('**/do/list/**', timeout=15000)
            print("✅ Navegação completa")
            
            await page.wait_for_timeout(3000)
            
            # Pegar URL final
            final_url = page.url
            print(f"🔗 URL final: {final_url}")
            
            # Pegar HTML final
            html = await page.content()
            print(f"📄 HTML recebido: {len(html)} bytes")
            
            # Verificar se tem redirect
            if 'window.location.replace' in html:
                print("⚠️ HTML ainda tem redirect - não esperou o suficiente")
            elif len(html) > 200000:
                print("⚠️ HTML muito grande - pode ser página de bloqueio")
                print(f"Primeiros 500 chars:\n{html[:500]}")
            else:
                print("✅ HTML parece correto (tamanho normal)")
            
            # Procurar por artigos de carros
            articles = await page.query_selector_all('article')
            print(f"🚗 Artigos encontrados: {len(articles)}")
            
            if len(articles) > 0:
                # Ver primeiro artigo
                first_article = await articles[0].inner_html()
                print(f"\n📦 Primeiro artigo (primeiros 500 chars):")
                print(first_article[:500])
            
            # Tentar parsear com função existente
            print("\n" + "=" * 80)
            print("🔍 TENTANDO PARSEAR COM parse_carjet_html_complete:")
            
            from carjet_direct import parse_carjet_html_complete
            items = parse_carjet_html_complete(html)
            
            print(f"✅ Carros parseados: {len(items)}")
            
            if len(items) > 0:
                print("\n📋 Primeiros 3 carros:")
                for i, item in enumerate(items[:3], 1):
                    print(f"\n{i}. {item.get('car_name', 'N/A')}")
                    print(f"   Preço: {item.get('price', 'N/A')} {item.get('currency', 'EUR')}")
                    print(f"   Supplier: {item.get('supplier', 'N/A')}")
                    print(f"   Categoria: {item.get('category', 'N/A')}")
                    print(f"   Grupo: {item.get('group', 'N/A')}")
                    print(f"   Transmissão: {item.get('transmission', 'N/A')}")
            
            # Manter browser aberto por 5 segundos para ver
            print("\n⏸️ Mantendo browser aberto por 5 segundos...")
            await page.wait_for_timeout(5000)
            
            await browser.close()
            print("\n✅ TESTE COMPLETO!")
            
            return len(items)
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return 0

if __name__ == "__main__":
    result = asyncio.run(test_playwright_carjet())
    print(f"\n{'='*80}")
    print(f"🎯 RESULTADO FINAL: {result} carros encontrados")
    print(f"{'='*80}")
