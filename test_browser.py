#!/usr/bin/env python3
"""
Test browser - Opens Chromium to see what's happening
"""

from playwright.sync_api import sync_playwright
import time

print("=" * 60)
print("🚀 OPENING CHROMIUM")
print("=" * 60)

p = sync_playwright().start()

print("Launching browser...")
browser = p.chromium.launch(headless=False, slow_mo=1000)

print("Creating page...")
page = browser.new_page(viewport={"width": 1920, "height": 1080})

print("Going to CarJet...")
page.goto("https://www.carjet.com/aluguel-carros/")

print("\n" + "=" * 60)
print("✅ CHROMIUM IS OPEN!")
print("=" * 60)
print("You should see the Chromium window now!")
print("Keeping it open for 2 minutes...")
print("Press Ctrl+C to close earlier")
print("=" * 60)

try:
    time.sleep(120)
except KeyboardInterrupt:
    print("\n👋 Closing early...")

print("\nClosing browser...")
browser.close()
p.stop()

print("✅ Done!")
