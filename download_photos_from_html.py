#!/usr/bin/env python3
"""
Download de fotos do CarJet extraindo URLs do HTML
Sem scraping - apenas parse do HTML
"""

import re
import sqlite3
import httpx
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from bs4 import BeautifulSoup

def clean_car_name(name):
    """Limpa nome do carro"""
    name = name.lower().strip()
    # Remover "ou similar"
    name = re.sub(r'\s+(ou\s*similar|or\s*similar).*$', '', name, flags=re.IGNORECASE)
    # Remover categorias
    name = re.sub(r'\s*\|\s*.*$', '', name)
    # Normalizar espaços
    name = re.sub(r'\s+', ' ', name).strip()
    return name

async def get_carjet_html():
    """Obtém HTML do CarJet via POST"""
    
    # Datas
    start_date = datetime.now() + timedelta(days=3)
    end_date = start_date + timedelta(days=7)
    
    # Formato CarJet: dd/mm/yyyy
    pickup_date = start_date.strftime('%d/%m/%Y')
    return_date = end_date.strftime('%d/%m/%Y')
    
    form_data = {
        'frmDestino': 'FAO02',  # Faro
        'frmDestinoFinal': '',
        'frmFechaRecogida': pickup_date,
        'frmFechaDevolucion': return_date,
        'frmHasAge': 'False',
        'frmEdad': '35',
        'frmPrvNo': '',
        'frmMoneda': 'EUR',
        'frmMonedaForzada': '',
        'frmJsonFilterInfo': '',
        'frmTipoVeh': 'CAR',
        'idioma': 'PT',
        'frmSession': '',
        'frmDetailCode': ''
    }
    
    url = 'https://www.carjet.com/do/list/pt'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html',
        'Accept-Language': 'pt-PT,pt;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://www.carjet.com/',
        'Origin': 'https://www.carjet.com'
    }
    
    print(f"📅 Datas: {pickup_date} → {return_date}")
    print(f"🌐 POST → {url}")
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        # POST inicial
        response = await client.post(url, data=form_data, headers=headers)
        
        print(f"📄 HTML recebido: {len(response.text)} bytes")
        print(f"🔗 URL final: {response.url}")
        
        # Se houver redirect, aguardar e fazer GET
        if 'Waiting' in response.text or 'window.location' in response.text:
            print("⏳ Aguardando 3s para resultados...")
            await asyncio.sleep(3)
            
            # Fazer GET na URL final
            response = await client.get(str(response.url), headers=headers)
            print(f"📄 HTML final: {len(response.text)} bytes")
        
        return response.text

def extract_photos_from_html(html):
    """Extrai fotos do HTML"""
    
    soup = BeautifulSoup(html, 'html.parser')
    
    photos = {}
    
    # Procurar por articles (carros)
    articles = soup.find_all('article')
    
    print(f"\n📊 {len(articles)} artigos encontrados")
    
    for article in articles:
        try:
            # Nome do carro - procurar em h3, h4, etc
            car_name = None
            for tag in article.find_all(['h3', 'h4', 'span', 'div']):
                text = tag.get_text(strip=True)
                # Verificar se tem marca de carro
                if any(brand in text.lower() for brand in ['fiat', 'renault', 'peugeot', 'citroen', 'toyota', 'ford', 'vw', 'volkswagen', 'opel', 'seat', 'hyundai', 'kia', 'nissan', 'mercedes', 'bmw', 'audi', 'mini', 'jeep', 'dacia', 'skoda', 'mazda']):
                    car_name = text
                    break
            
            if not car_name:
                continue
            
            # Limpar nome
            car_clean = clean_car_name(car_name)
            
            # Procurar foto
            img_tags = article.find_all('img')
            
            for img in img_tags:
                src = img.get('src', '') or img.get('data-src', '')
                alt = img.get('alt', '').lower()
                
                # Ignorar logos
                if '/logo' in src.lower() or 'logo_' in src.lower():
                    continue
                
                # Ignorar placeholders
                if 'loading-car.png' in src:
                    continue
                
                # Verificar se é foto de carro
                if '/car' in src.lower() or '/img' in src.lower() or any(brand in alt for brand in ['fiat', 'renault', 'peugeot', 'citroen', 'toyota', 'ford', 'vw', 'volkswagen', 'opel', 'seat', 'hyundai', 'kia', 'nissan', 'mercedes', 'bmw', 'audi', 'mini', 'jeep', 'dacia', 'skoda', 'mazda']):
                    
                    # Completar URL se necessário
                    if src and not src.startswith('http'):
                        src = f'https://www.carjet.com{src}'
                    
                    if src:
                        photos[car_clean] = src
                        print(f"✅ {car_clean}: {src[:80]}...")
                        break
        
        except Exception as e:
            print(f"❌ Erro ao processar artigo: {e}")
            continue
    
    return photos

async def download_and_save_photos(photos):
    """Baixa e salva fotos na base de dados"""
    
    db_path = Path(__file__).parent / "data.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    downloaded = 0
    skipped = 0
    failed = 0
    
    print(f"\n📥 Iniciando download de {len(photos)} fotos...")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for idx, (car_name, photo_url) in enumerate(photos.items(), 1):
            
            # Verificar se já tem foto
            cursor.execute("""
                SELECT COUNT(*) FROM vehicle_photos 
                WHERE vehicle_name = ?
            """, (car_name,))
            
            has_photo = cursor.fetchone()[0] > 0
            
            if has_photo:
                print(f"[{idx}/{len(photos)}] ⏭️  {car_name} - Já tem foto")
                skipped += 1
                continue
            
            try:
                print(f"[{idx}/{len(photos)}] 📥 {car_name}")
                print(f"                    {photo_url}")
                
                response = await client.get(photo_url)
                
                if response.status_code == 200:
                    photo_data = response.content
                    
                    # Salvar na base de dados
                    cursor.execute("""
                        INSERT OR REPLACE INTO vehicle_photos 
                        (vehicle_name, photo_data, photo_url, updated_at)
                        VALUES (?, ?, ?, ?)
                    """, (car_name, photo_data, photo_url, datetime.now().isoformat()))
                    
                    cursor.execute("""
                        INSERT OR REPLACE INTO vehicle_images 
                        (vehicle_name, image_data, image_url, updated_at)
                        VALUES (?, ?, ?, ?)
                    """, (car_name, photo_data, photo_url, datetime.now().isoformat()))
                    
                    conn.commit()
                    downloaded += 1
                    print(f"                    ✅ {len(photo_data)} bytes")
                else:
                    print(f"                    ❌ HTTP {response.status_code}")
                    failed += 1
                    
            except Exception as e:
                print(f"                    ❌ Erro: {e}")
                failed += 1
    
    conn.close()
    
    print("="*60)
    print(f"✅ Baixadas: {downloaded}")
    print(f"⏭️  Ignoradas: {skipped}")
    print(f"❌ Falharam: {failed}")
    print(f"📊 Total: {downloaded + skipped}/{len(photos)}")

async def main():
    """Função principal"""
    
    print("="*60)
    print("DOWNLOAD DE FOTOS DO CARJET")
    print("="*60)
    
    # 1. Obter HTML
    html = await get_carjet_html()
    
    # 2. Extrair fotos
    photos = extract_photos_from_html(html)
    
    # 3. Baixar e salvar
    if photos:
        await download_and_save_photos(photos)
    else:
        print("\n❌ Nenhuma foto encontrada no HTML")

if __name__ == "__main__":
    asyncio.run(main())
