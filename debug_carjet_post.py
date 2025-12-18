"""
Script de debug para verificar o comportamento do CarJet POST
"""
import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Datas de teste
start_dt = datetime(2025, 12, 1, 15, 0)
end_dt = datetime(2025, 12, 15, 15, 0)

print("=" * 80)
print("🔍 DEBUG CARJET POST")
print("=" * 80)

# Criar sessão
session = requests.Session()

# Headers realistas
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-PT,pt;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
})

# PASSO 1: Visitar homepage
print("\n1️⃣ Visitando homepage...")
home_url = 'https://www.carjet.com/aluguel-carros/index.htm'
resp_home = session.get(home_url, timeout=15)
print(f"   Status: {resp_home.status_code}")
print(f"   Cookies: {len(session.cookies)}")
print(f"   URL final: {resp_home.url}")

# PASSO 2: Fazer POST
print("\n2️⃣ Submetendo formulário...")

pickup_date = start_dt.strftime('%d/%m/%Y %H:%M')
return_date = end_dt.strftime('%d/%m/%Y %H:%M')

form_data = {
    'frmDestino': 'ABF01',  # Albufeira
    'frmDestinoFinal': '',
    'frmFechaRecogida': pickup_date,
    'frmFechaDevolucion': return_date,
    'frmHasAge': 'False',
    'frmEdad': '35',
    'frmPrvNo': '',
    'frmMoneda': 'EUR',
    'frmMonedaForzada': 'EUR',
    'frmJsonFilterInfo': '',
    'frmTipoVeh': 'CAR',
    'idioma': 'PT',
    'frmSession': 'debug-test-123',
    'frmDetailCode': ''
}

post_headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.carjet.com',
    'Referer': home_url,
}

post_url = 'https://www.carjet.com/do/list/pt'
resp_post = session.post(post_url, data=form_data, headers=post_headers, timeout=15, allow_redirects=False)

print(f"   Status: {resp_post.status_code}")
print(f"   URL final: {resp_post.url}")
print(f"   Headers: {dict(resp_post.headers)}")
print(f"   HTML size: {len(resp_post.text)} bytes")

# PASSO 3: Verificar conteúdo
print("\n3️⃣ Analisando resposta...")

# Verificar se há redirect no Location header
if 'Location' in resp_post.headers:
    print(f"   ✅ HTTP Redirect para: {resp_post.headers['Location']}")

# Verificar se há redirect JavaScript
pattern = r"window\.location\.replace\('([^']+)'\)"
match = re.search(pattern, resp_post.text)
if match:
    print(f"   ✅ JavaScript redirect para: {match.group(1)}")
else:
    print("   ❌ NÃO encontrou JavaScript redirect")

# Verificar se é página de loading/espera
loading_indicators = [
    'A carregar',
    'Procurando',
    'Searching',
    'Waiting',
    'Please wait',
    'Aguarde',
]

is_loading = any(indicator in resp_post.text for indicator in loading_indicators)
print(f"   Página de loading: {'SIM' if is_loading else 'NÃO'}")

# Verificar se já tem resultados (divs de carros)
soup = BeautifulSoup(resp_post.text, 'html.parser')
car_cards = soup.select('.carCardWeb, .resultado-oferta, [class*="car-card"]')
print(f"   Divs de carros: {len(car_cards)}")

# Salvar HTML para análise
with open('debug_post_response.html', 'w', encoding='utf-8') as f:
    f.write(resp_post.text)
print(f"\n   💾 HTML salvo em: debug_post_response.html")

# Extrair primeiras linhas para análise
print("\n4️⃣ Primeiras 50 linhas do HTML:")
print("-" * 80)
lines = resp_post.text.split('\n')[:50]
for i, line in enumerate(lines, 1):
    print(f"{i:3d} | {line[:120]}")

print("\n" + "=" * 80)
print("✅ Debug completo")
