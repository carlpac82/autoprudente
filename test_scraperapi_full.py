#!/usr/bin/env python3
"""
Test full ScraperAPI integration with main.py
"""
import requests
from datetime import datetime, timedelta

print("=" * 80)
print("🚗 TESTING FULL SCRAPERAPI INTEGRATION")
print("=" * 80)

# Test parameters
start_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
end_date = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')

payload = {
    "location": "Faro",
    "start_date": start_date,
    "end_date": end_date,
    "start_time": "15:00",
    "end_time": "15:00",
    "currency": "EUR"
}

print(f"\n📋 Request:")
print(f"  Location: {payload['location']}")
print(f"  Dates: {payload['start_date']} to {payload['end_date']}")
print(f"  Time: {payload['start_time']}")

print(f"\n🌐 Calling API...")

try:
    response = requests.post(
        'http://127.0.0.1:8000/api/track',
        json=payload,
        timeout=120  # 2 minutes timeout
    )
    
    if response.status_code == 200:
        data = response.json()
        
        if data.get('ok'):
            items = data.get('items', [])
            method = data.get('method', 'unknown')
            
            print(f"\n✅ SUCCESS!")
            print(f"  Method: {method}")
            print(f"  Cars found: {len(items)}")
            
            if items:
                print(f"\n🚗 Top 5 cheapest cars:")
                for i, car in enumerate(items[:5], 1):
                    print(f"  {i}. {car.get('name', 'N/A')} - {car.get('price', 'N/A')} ({car.get('supplier', 'N/A')})")
                    
                # Check if ScraperAPI was used
                if method == 'scraperapi':
                    print(f"\n🎉 ScraperAPI was used successfully!")
                else:
                    print(f"\n⚠️  ScraperAPI was NOT used. Method: {method}")
            else:
                print(f"\n⚠️  No cars found")
        else:
            print(f"\n❌ API returned error:")
            print(f"  {data.get('error', 'Unknown error')}")
    else:
        print(f"\n❌ HTTP Error: {response.status_code}")
        print(f"  Response: {response.text[:500]}")
        
except requests.exceptions.Timeout:
    print(f"\n⏱️  Request timed out (>2 minutes)")
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 80)
print("🏁 TEST COMPLETE")
print("=" * 80)
