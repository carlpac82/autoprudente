#!/usr/bin/env python3
"""Verificar campos mapeados no Damage Report"""

import sqlite3

# Connect to database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Get all mapped fields
cursor.execute("SELECT field_id, page FROM damage_report_coordinates ORDER BY field_id")
rows = cursor.fetchall()

print(f"\n📊 Total de campos mapeados: {len(rows)}\n")
print("=" * 60)

# Group by category
categories = {
    'Básicos': [],
    'Diagrama': [],
    'Fotos': [],
    'Descrições': [],
    'Reparações': [],
    'Assinaturas': [],
    'Outros': []
}

for field_id, page in rows:
    if 'diagram' in field_id:
        categories['Diagrama'].append(f"  ✓ {field_id} (página {page})")
    elif 'photo' in field_id:
        categories['Fotos'].append(f"  ✓ {field_id} (página {page})")
    elif 'description' in field_id:
        categories['Descrições'].append(f"  ✓ {field_id} (página {page})")
    elif 'repair' in field_id:
        categories['Reparações'].append(f"  ✓ {field_id} (página {page})")
    elif 'signature' in field_id:
        categories['Assinaturas'].append(f"  ✓ {field_id} (página {page})")
    elif any(x in field_id for x in ['dr_', 'contract', 'customer', 'vehicle', 'pickup', 'return']):
        categories['Básicos'].append(f"  ✓ {field_id} (página {page})")
    else:
        categories['Outros'].append(f"  ✓ {field_id} (página {page})")

# Print by category
for category, fields in categories.items():
    if fields:
        print(f"\n{category}: {len(fields)}")
        for field in fields:
            print(field)

# Check missing critical fields
print("\n" + "=" * 60)
print("\n❌ Campos CRÍTICOS em falta:\n")

critical = {
    'vehicle_diagram': 'Diagrama do Veículo',
    'damage_photo_1': 'Foto 1',
    'damage_photo_2': 'Foto 2',
    'damage_photo_3': 'Foto 3',
    'signature_inspector': 'Assinatura Inspetor',
    'signature_client': 'Assinatura Cliente',
}

existing = [row[0] for row in rows]
missing = []

for field_id, name in critical.items():
    if field_id not in existing:
        missing.append(f"  ⚠️  {name} ({field_id})")

if missing:
    for m in missing:
        print(m)
else:
    print("  ✅ Todos os campos críticos estão mapeados!")

print("\n" + "=" * 60)
conn.close()
