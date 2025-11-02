#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import requests

load_dotenv()

url = os.getenv("ALBUFEIRA_1D", "")
print(f"Testando URL: {url}\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Cookie': 'monedaForzada=EUR; moneda=EUR; currency=EUR'
}

r = requests.get(url, headers=headers, timeout=10)
print(f"Status: {r.status_code}")
print(f"Tamanho: {len(r.text)} bytes\n")
print("Primeiros 1000 caracteres:")
print("=" * 70)
print(r.text[:1000])
print("=" * 70)
