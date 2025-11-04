#!/usr/bin/env python3
"""
Test ScraperAPI integration
"""
import os
import requests
from datetime import datetime, timedelta

# Load API key
SCRAPERAPI_KEY = "9de9d0c9014128cc2d5ad947dbeb56f4"

print("=" * 80)
print("🌐 TESTING SCRAPERAPI INTEGRATION")
print("=" * 80)

# Test 1: Simple GET request
print("\n📋 Test 1: Simple GET to CarJet homepage")
try:
    response = requests.get(
        'https://api.scraperapi.com/',
        params={
            'api_key': SCRAPERAPI_KEY,
            'url': 'https://www.carjet.com/aluguel-carros/index.htm',
        },
        timeout=30
    )
    
    if response.status_code == 200:
        print(f"✅ Success! Status: {response.status_code}")
        print(f"📄 HTML length: {len(response.text)} bytes")
        
        # Check if important elements are present
        if 'pickup' in response.text:
            print("✅ Found 'pickup' field")
        if 'fechaRecogida' in response.text:
            print("✅ Found 'fechaRecogida' field")
        if 'recogida_lista' in response.text:
            print("✅ Found 'recogida_lista' dropdown")
    else:
        print(f"❌ Failed! Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: GET with JavaScript rendering
print("\n📋 Test 2: GET with JavaScript rendering")
try:
    response = requests.get(
        'https://api.scraperapi.com/',
        params={
            'api_key': SCRAPERAPI_KEY,
            'url': 'https://www.carjet.com/aluguel-carros/index.htm',
            'render': 'true',  # Enable JavaScript rendering
            'country_code': 'pt',
        },
        timeout=60
    )
    
    if response.status_code == 200:
        print(f"✅ Success! Status: {response.status_code}")
        print(f"📄 HTML length: {len(response.text)} bytes")
    else:
        print(f"❌ Failed! Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: POST request with form data
print("\n📋 Test 3: POST with form data")
try:
    # Build form payload
    start_date = datetime.now() + timedelta(days=7)
    end_date = start_date + timedelta(days=8)
    
    payload = {
        'pickup': 'Faro Aeroporto (FAO)',
        'fechaRecogida': start_date.strftime('%d/%m/%Y'),
        'fechaDevolucion': end_date.strftime('%d/%m/%Y'),
        'fechaRecogidaSelHour': '15:00',
        'fechaDevolucionSelHour': '15:00',
        'moneda': 'EUR',
        'idioma': 'PT',
        'country': 'PT',
    }
    
    print(f"📅 Dates: {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}")
    
    response = requests.post(
        'https://api.scraperapi.com/',
        params={
            'api_key': SCRAPERAPI_KEY,
            'url': 'https://www.carjet.com/do/list/pt',
            'country_code': 'pt',
        },
        data=payload,
        timeout=60
    )
    
    if response.status_code == 200:
        print(f"✅ Success! Status: {response.status_code}")
        print(f"📄 HTML length: {len(response.text)} bytes")
        
        # Check for car results
        if 'Group' in response.text or 'grupo' in response.text.lower():
            print("✅ Found car groups in results!")
        if 'EUR' in response.text or '€' in response.text:
            print("✅ Found prices in results!")
            
        # Check for errors
        if 'war=' in response.text:
            print("⚠️  Warning: 'war=' parameter found (might indicate error)")
        if 's=' in response.text and 'b=' in response.text:
            print("✅ Found 's=' and 'b=' parameters (success indicators)")
    else:
        print(f"❌ Failed! Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("🏁 TEST COMPLETE")
print("=" * 80)
