#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta

print("=" * 80)
print("TESTING MAIN.PY API")
print("=" * 80)

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

print(f"\nRequest: {payload}")
print(f"\nCalling API...")

try:
    # DEV_NO_AUTH=1 in .env, so no auth needed
    response = requests.post(
        'http://127.0.0.1:8000/api/track-by-params',
        json=payload,
        timeout=180
    )
    
    if response.status_code == 200:
        data = response.json()
        
        if data.get('ok'):
            items = data.get('items', [])
            method = data.get('method', 'unknown')
            
            print(f"\nSUCCESS!")
            print(f"Method: {method}")
            print(f"Cars found: {len(items)}")
            
            if items:
                print(f"\nTop 5 cheapest:")
                for i, car in enumerate(items[:5], 1):
                    print(f"  {i}. {car.get('name')} - {car.get('price')} ({car.get('supplier')})")
        else:
            print(f"\nError: {data.get('error')}")
    else:
        print(f"\nHTTP Error: {response.status_code}")
        
except Exception as e:
    print(f"\nError: {e}")

print("\n" + "=" * 80)
