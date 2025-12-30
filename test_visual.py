#!/usr/bin/env python3
"""Teste HTTP direto - sem Selenium"""

import sys
import time
import requests
from datetime import datetime, timedelta

def test_carjet():
    print("🚀 Teste via HTTP direto (sem Selenium)...")
    
    # Datas de teste
    start_dt = datetime.now() + timedelta(days=7)
    end_dt = start_dt + timedelta(days=3)
    
    # Headers de browser real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'pt-PT,pt;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }
    
    session = requests.Session()
    
    # Tentar URL de resultados direto
    # Formato: /pt/do/list/pt?s=YYYYMMDD&e=YYYYMMDD&st=HH:MM&et=HH:MM&b=faro&...
    pickup_date = start_dt.strftime("%Y%m%d")
    dropoff_date = end_dt.strftime("%Y%m%d")
    
    url = f"https://www.carjet.com/pt/do/list/pt?s={pickup_date}&e={dropoff_date}&st=10:00&et=10:00&b=faro&age=30"
    
    print(f"📍 Tentando URL direta: {url}")
    
    try:
        response = session.get(url, headers=headers, timeout=30)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Tamanho: {len(response.text)} bytes")
        
        # Verificar se tem carros ou bloqueio
        if 'war=' in response.url or 'captcha' in response.text.lower():
            print("❌ Bloqueado (WAR/Captcha)")
        elif 'car' in response.text.lower() and 'price' in response.text.lower():
            print("✅ Parece ter resultados!")
            # Guardar para análise
            with open('/tmp/carjet_response.html', 'w') as f:
                f.write(response.text)
            print("📁 Guardado em /tmp/carjet_response.html")
        else:
            print("⚠️ Resposta inesperada")
            with open('/tmp/carjet_response.html', 'w') as f:
                f.write(response.text)
                
    except Exception as e:
        print(f"❌ Erro: {e}")
        
        # Preencher datas diretamente via JavaScript (funciona mesmo com banner)
        print(f"📅 Preenchendo datas: {start_dt.strftime('%d/%m/%Y')} - {end_dt.strftime('%d/%m/%Y')}")
        month_year_pickup = start_dt.strftime("%Y%m")
        month_year_dropoff = end_dt.strftime("%Y%m")
        day_pickup = start_dt.strftime("%d")
        day_dropoff = end_dt.strftime("%d")
        
        result = driver.execute_script("""
            const monthYearPickup = arguments[0];
            const monthYearDropoff = arguments[1];
            const dayPickup = arguments[2];
            const dayDropoff = arguments[3];
            
            let filled = {};
            
            // DESKTOP: Preencher campos de data diretamente
            // Formato dd/mm/yyyy para campos de texto
            const pickupDate = dayPickup + '/' + monthYearPickup.substring(4,6) + '/' + monthYearPickup.substring(0,4);
            const dropoffDate = dayDropoff + '/' + monthYearDropoff.substring(4,6) + '/' + monthYearDropoff.substring(0,4);
            
            // Campo de recolha (vários possíveis IDs)
            const pickupFields = ['#fechaRecogida', '#pickup_date', 'input[name="fechaRecogida"]', 'input[name="pickup_date"]'];
            for (const sel of pickupFields) {
                const el = document.querySelector(sel);
                if (el) {
                    el.value = pickupDate;
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                    filled.pickup = sel + '=' + pickupDate;
                    break;
                }
            }
            
            // Campo de devolução
            const dropoffFields = ['#fechaDevolucion', '#dropoff_date', 'input[name="fechaDevolucion"]', 'input[name="dropoff_date"]'];
            for (const sel of dropoffFields) {
                const el = document.querySelector(sel);
                if (el) {
                    el.value = dropoffDate;
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                    filled.dropoff = sel + '=' + dropoffDate;
                    break;
                }
            }
            
            // Dropdowns MyBooking (se existirem)
            const monthSelect1 = document.querySelector('#fechaRecogidaMyBookingMonthYear');
            if (monthSelect1) { monthSelect1.value = monthYearPickup; monthSelect1.dispatchEvent(new Event('change', {bubbles: true})); filled.m1 = monthYearPickup; }
            
            const daySelect1 = document.querySelector('#fechaRecogidaMyBookingDay');
            if (daySelect1) { daySelect1.value = dayPickup; daySelect1.dispatchEvent(new Event('change', {bubbles: true})); filled.d1 = dayPickup; }
            
            const monthSelect2 = document.querySelector('#fechaDevolucionMyBookingMonthYear');
            if (monthSelect2) { monthSelect2.value = monthYearDropoff; monthSelect2.dispatchEvent(new Event('change', {bubbles: true})); filled.m2 = monthYearDropoff; }
            
            const daySelect2 = document.querySelector('#fechaDevolucionMyBookingDay');
            if (daySelect2) { daySelect2.value = dayDropoff; daySelect2.dispatchEvent(new Event('change', {bubbles: true})); filled.d2 = dayDropoff; }
            
            // Horas
            const hourFields = ['#fechaRecogidaSelHour', 'select[name="horaRecogida"]', '#pickup_time'];
            for (const sel of hourFields) {
                const el = document.querySelector(sel);
                if (el) { el.value = '10:00'; el.dispatchEvent(new Event('change', {bubbles: true})); filled.h1 = '10:00'; break; }
            }
            
            const hourFields2 = ['#fechaDevolucionSelHour', 'select[name="horaDevolucion"]', '#dropoff_time'];
            for (const sel of hourFields2) {
                const el = document.querySelector(sel);
                if (el) { el.value = '10:00'; el.dispatchEvent(new Event('change', {bubbles: true})); filled.h2 = '10:00'; break; }
            }
            
            return filled;
        """, month_year_pickup, month_year_dropoff, day_pickup, day_dropoff)
        print(f"   Campos preenchidos: {result}")
        
        time.sleep(1)
        
        # Submit
        print("🔍 Submetendo formulário...")
        submit_result = driver.execute_script("""
            let form = document.querySelector('form[name="menu_tarifas"]') || 
                       document.querySelector('form#booking_form') ||
                       document.querySelector('form');
            if (form) { form.submit(); return 'OK'; }
            return 'NO_FORM';
        """)
        print(f"   Submit: {submit_result}")
        
        # Aguardar resultados
        print("⏳ Aguardando página de resultados...")
        max_wait = 30
        waited = 0
        while waited < max_wait:
            current_url = driver.current_url
            if '/do/list/' in current_url:
                print(f"✅ Página de resultados carregada após {waited}s")
                break
            time.sleep(2)
            waited += 2
            print(f"   Aguardando... ({waited}s) URL: {current_url[:60]}...")
        
        time.sleep(3)
        final_url = driver.current_url
        print(f"\n📍 URL final: {final_url}")
        
        # Verificar se tem carros
        if '/do/list/' in final_url:
            cars = driver.execute_script("""
                const items = document.querySelectorAll('.car-item, .vehicle-card, [class*="car"], [class*="vehicle"]');
                return items.length;
            """)
            print(f"🚗 Carros encontrados: {cars}")
        
        print("\n✅ Teste concluído! Pressione Enter para fechar...")
        input()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione Enter para fechar...")
    finally:
        if driver:
            driver.quit()
            print("🧹 Driver fechado")

if __name__ == "__main__":
    test_carjet()
