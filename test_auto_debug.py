#!/usr/bin/env python3
"""
Debug da detecção de automáticos
"""

car_name = "Fiat 500"
transmission = "Automatic"

car = car_name.lower().strip()
trans = transmission.lower()
auto = 'auto' in car or 'auto' in trans or 'automatic' in trans

print(f"car_name: '{car_name}'")
print(f"transmission: '{transmission}'")
print(f"car (lower): '{car}'")
print(f"trans (lower): '{trans}'")
print(f"'auto' in car: {'auto' in car}")
print(f"'auto' in trans: {'auto' in trans}")
print(f"'automatic' in trans: {'automatic' in trans}")
print(f"auto (resultado): {auto}")
