#!/usr/bin/env python3
"""Valida transmissões dos carros vs parametrização"""

import asyncio
import httpx
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from carjet_direct import VEHICLES

def normalize_name(name: str) -> str:
    """Normaliza nome do carro"""
    name = name.lower().strip()
    name = re.sub(r'\s+(ou\s*similar|or\s*similar).*$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s*\|\s*.*$', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

async def get_transmission(url: str) -> str:
    """Busca transmissão da página de detalhes"""
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            r = await client.get(url)
            if r.status_code != 200:
                return ""
            soup = BeautifulSoup(r.text, "lxml")
            li = soup.find("li", {"value": ["A", "M"]})
            if li:
                return "auto" if li.get("value") == "A" else "manual"
            text = soup.get_text(" ", strip=True).lower()
            if "automático" in text or "automatic" in text:
                return "auto"
            elif "manual" in text:
                return "manual"
            return ""
    except:
        return ""

def is_auto_name(name: str) -> bool:
    """Detecta auto pelo nome"""
    patterns = [r'\bauto\b', r'\bautomatic\b', r'\belectric\b', r'\be-\d+']
    return any(re.search(p, name.lower()) for p in patterns)

def find_in_dict(name: str):
    """Procura no VEHICLES"""
    norm = normalize_name(name)
    if norm in VEHICLES:
        cat = VEHICLES[norm]
        return cat, ('Auto' in cat)
    # Busca parcial
    for k in sorted(VEHICLES.keys(), key=len, reverse=True):
        if k in norm:
            cat = VEHICLES[k]
            return cat, ('Auto' in cat)
    return None, None

async def main():
    print("\n🚗 VALIDAÇÃO DE TRANSMISSÕES - CarJet Real vs VEHICLES\n")
    
    # POST CarJet
    url = "https://www.carjet.com/do/list/pt"
    start = datetime.now() + timedelta(days=7)
    end = start + timedelta(days=7)
    
    data = {
        'frmDestino': 'FAO02',
        'frmFechaRecogida': start.strftime('%d/%m/%Y 15:00'),
        'frmFechaDevolucion': end.strftime('%d/%m/%Y 15:00'),
        'frmMoneda': 'EUR',
        'frmTipoVeh': 'CAR',
        'idioma': 'PT',
    }
    
    print("⏳ Fazendo scraping...")
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        r = await client.post(url, data=data)
        html = r.text
        
        if 'window.location.replace' in html:
            m = re.search(r"window\.location\.replace\('([^']+)'\)", html)
            if m:
                await asyncio.sleep(3)
                r = await client.get(f"https://www.carjet.com{m.group(1)}")
                html = r.text
    
    soup = BeautifulSoup(html, 'lxml')
    blocks = soup.find_all('article') or soup.find_all('div', class_=lambda x: x and ('car' in x or 'result' in x) if x else False)
    blocks = blocks[:50]  # Limitar a 50
    
    print(f"✅ {len(blocks)} carros encontrados\n")
    
    issues = []
    brands = ['fiat', 'renault', 'peugeot', 'citroen', 'toyota', 'ford', 'volkswagen', 
              'vw', 'opel', 'seat', 'hyundai', 'kia', 'nissan', 'mercedes', 'bmw', 
              'audi', 'mini', 'jeep', 'dacia', 'skoda', 'mazda', 'mg', 'volvo']
    
    checked = 0
    for block in blocks:
        # Nome
        name = ''
        for tag in block.find_all(['h3', 'h4', 'span', 'div']):
            txt = tag.get_text(strip=True)
            if any(b in txt.lower() for b in brands):
                name = txt
                break
        if not name:
            continue
        
        name = re.sub(r'\s+(ou\s*similar).*$', '', name, flags=re.I)
        name = re.sub(r'\s+', ' ', name).strip()
        
        # Link
        link = ''
        a = block.find('a', href=True)
        if a:
            link = f"https://www.carjet.com{a['href']}" if a['href'].startswith('/') else a['href']
        
        # Verificar
        auto_name = is_auto_name(name)
        cat, auto_dict = find_in_dict(name)
        
        trans_real = None
        if not auto_name and link:
            checked += 1
            print(f"🔍 [{checked}] {name[:50]:<50} ... ", end='', flush=True)
            trans_real = await get_transmission(link)
            print(f"{'✅ ' + trans_real if trans_real else '❓ desconhecido'}")
            await asyncio.sleep(0.4)
        elif auto_name:
            trans_real = "auto"
        
        # Comparar
        if cat and trans_real and auto_dict is not None:
            real_is_auto = (trans_real == "auto")
            if real_is_auto != auto_dict:
                issues.append({
                    'name': name,
                    'cat': cat,
                    'expected': 'AUTO' if auto_dict else 'MANUAL',
                    'real': 'AUTO' if real_is_auto else 'MANUAL'
                })
                print(f"❌ {name}")
                print(f"   Dict: {cat} → {issues[-1]['expected']}")
                print(f"   Real: {issues[-1]['real']}\n")
    
    print(f"\n{'='*60}")
    print(f"📊 ESTATÍSTICAS:")
    print(f"   - Carros encontrados: {len(blocks)}")
    print(f"   - Páginas consultadas: {checked}")
    print(f"   - Inconsistências: {len(issues)}")
    print(f"{'='*60}")
    
    if len(issues) == 0:
        print(f"\n✅ TODAS AS PARAMETRIZAÇÕES ESTÃO CORRETAS!\n")
    else:
        print(f"\n❌ CORREÇÕES NECESSÁRIAS:\n")
        for issue in issues:
            print(f"   {issue['name']}")
            print(f"   → Mudar de {issue['expected']} para {issue['real']}")
            print()

if __name__ == "__main__":
    asyncio.run(main())
