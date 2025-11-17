#!/usr/bin/env python3
"""
Debug script para verificar parsing de preços do CarJet
"""
import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from carjet_direct import scrape_carjet_direct
from datetime import datetime, timedelta

# Data de teste (25/11/2025, 3 dias - igual ao screenshot)
start_dt = datetime(2025, 11, 25)
end_dt = start_dt + timedelta(days=3)

print(f"🔍 Testing CarJet scraping for Albufeira")
print(f"📅 Date: {start_dt.strftime('%d/%m/%Y')} - {end_dt.strftime('%d/%m/%Y')} (3 days)")
print("=" * 80)

# Scrape
items = scrape_carjet_direct('Albufeira', start_dt, end_dt)

print(f"\n📊 Total items found: {len(items)}")
print("=" * 80)

# Find Renault Clio from Flizzr
renault_clios = [item for item in items if 'clio' in item['car'].lower()]

print(f"\n🚗 Found {len(renault_clios)} Renault Clio(s):")
print("=" * 80)

for item in renault_clios:
    print(f"\n📋 Car: {item['car']}")
    print(f"🏢 Supplier: {item['supplier']}")
    print(f"💰 Price: {item['price']}")
    print(f"📦 Group: {item.get('group', 'N/A')}")
    print(f"⚙️ Transmission: {item.get('transmission', 'N/A')}")
    print(f"🏷️ Category: {item.get('category', 'N/A')}")

# Show all prices sorted (lowest first)
print(f"\n\n💵 ALL PRICES (sorted lowest → highest):")
print("=" * 80)

sorted_items = sorted(items, key=lambda x: float(x['price'].replace('€', '').replace(',', '.').strip()))

for i, item in enumerate(sorted_items[:10], 1):  # Top 10 cheapest
    price_val = float(item['price'].replace('€', '').replace(',', '.').strip())
    print(f"{i}. {price_val:7.2f}€ - {item['car']:<30} ({item['supplier']})")

print("\n" + "=" * 80)
print(f"✅ LOWEST: {sorted_items[0]['price']} - {sorted_items[0]['car']} ({sorted_items[0]['supplier']})")
