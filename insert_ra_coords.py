#!/usr/bin/env python3
"""
Inserir coordenadas de teste na BD
"""
import sqlite3
import json

# Coordenadas recebidas
coords_data = {
    "ok": True,
    "total": 12,
    "coordinates": [
        {"field_id": "address", "x": 293.0, "y": 96.5, "width": 138.0, "height": 10.5, "page": 1},
        {"field_id": "clientName", "x": 12.0, "y": 130.0, "width": 92.5, "height": 10.5, "page": 1},
        {"field_id": "clientPhone", "x": 110.0, "y": 351.5, "width": 164.5, "height": 11.0, "page": 1},
        {"field_id": "contractNumber", "x": 14.0, "y": 97.0, "width": 261.5, "height": 10.0, "page": 1},
        {"field_id": "country", "x": 13.5, "y": 271.0, "width": 262.0, "height": 12.344014, "page": 1},
        {"field_id": "pickupDate", "x": 292.6569, "y": 237.0, "width": 67.84312, "height": 13.688028, "page": 1},
        {"field_id": "pickupFuel", "x": 442.0, "y": 237.0, "width": 68.5, "height": 15.0, "page": 1},
        {"field_id": "pickupLocation", "x": 442.5, "y": 210.0, "width": 68.5, "height": 13.688028, "page": 1},
        {"field_id": "pickupTime", "x": 442.5, "y": 182.5, "width": 140.0, "height": 11.0, "page": 1},
        {"field_id": "postalCodeCity", "x": 13.5, "y": 351.5, "width": 85.5, "height": 11.0, "page": 1},
        {"field_id": "vehicleBrandModel", "x": 442.0, "y": 96.5, "width": 139.0, "height": 10.5, "page": 1},
        {"field_id": "vehiclePlate", "x": 292.0, "y": 182.5, "width": 140.5, "height": 11.5, "page": 1}
    ]
}

print("\n" + "="*80)
print("💾 INSERINDO COORDENADAS NA BASE DE DADOS")
print("="*80)

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Limpar coordenadas antigas (se existirem)
cursor.execute("DELETE FROM rental_agreement_coordinates")
print(f"\n🗑️  Limpadas coordenadas antigas")

# Inserir novas coordenadas
inserted = 0
for coord in coords_data["coordinates"]:
    cursor.execute("""
        INSERT INTO rental_agreement_coordinates 
        (field_id, x, y, width, height, page, template_version)
        VALUES (?, ?, ?, ?, ?, ?, 1)
    """, (
        coord["field_id"],
        coord["x"],
        coord["y"],
        coord["width"],
        coord["height"],
        coord["page"]
    ))
    inserted += 1
    print(f"   ✅ {coord['field_id']}: ({coord['x']:.1f}, {coord['y']:.1f}) - {coord['width']:.1f}x{coord['height']:.1f}")

conn.commit()
conn.close()

print(f"\n✅ {inserted} coordenadas inseridas com sucesso!")
print("\n" + "="*80)
print("🧪 PRÓXIMO PASSO: Testar extração para ver os logs")
print("="*80)
