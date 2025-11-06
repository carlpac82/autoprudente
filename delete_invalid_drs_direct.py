#!/usr/bin/env python3
"""Script para eliminar DRs inválidos diretamente no PostgreSQL"""
import psycopg2

# DATABASE_URL do Render (copia do Render Dashboard > Environment)
DATABASE_URL = "postgresql://carrental_api_user:lYEhQJcEYJBXBXRjVEfYWZIKGMBxYPxT@dpg-ct3d5qij1k6c73a0l1j0-a.frankfurt-postgres.render.com/carrental_api"

invalid_drs = ["1:2025", "2:2025", "3:2025"]

print("🔄 A conectar ao PostgreSQL do Render...")

try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    print("✅ Conectado!")
    print(f"\n🗑️  A eliminar {len(invalid_drs)} DRs inválidos...")
    
    deleted = []
    for dr_number in invalid_drs:
        cursor.execute("DELETE FROM damage_reports WHERE dr_number = %s", (dr_number,))
        if cursor.rowcount > 0:
            deleted.append(dr_number)
            print(f"   ✅ {dr_number} eliminado")
        else:
            print(f"   ⚠️  {dr_number} não encontrado")
    
    conn.commit()
    print(f"\n✅ Total: {len(deleted)} DRs eliminados com sucesso!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erro: {e}")
