#!/usr/bin/env python3
"""
Teste simples para verificar se os logs aparecem
"""
import sqlite3

print("\n" + "="*80)
print("🔍 VERIFICANDO SISTEMA DE EXTRAÇÃO")
print("="*80)

# 1. Verificar se tabelas existem
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM rental_agreement_coordinates")
coords_count = cursor.fetchone()[0]
print(f"\n📊 Coordenadas na BD: {coords_count}")

if coords_count == 0:
    print("\n⚠️  NENHUMA COORDENADA MAPEADA!")
    print("   Isso explica porque a extração usa fallback de padrões")
    print("   Os logs de 'TESTANDO CAMPO' SÓ aparecem se houver coordenadas!")
    print("\n💡 SOLUÇÃO:")
    print("   1. Abrir o mapeador RA: http://localhost:8000/admin/damage-report/ra-mapper")
    print("   2. Mapear pelo menos 1 campo (ex: contractNumber)")
    print("   3. Salvar coordenadas")
    print("   4. Executar teste de extração novamente")
else:
    print(f"\n✅ Encontradas {coords_count} coordenadas!")
    
    cursor.execute("SELECT field_id, x, y, width, height FROM rental_agreement_coordinates LIMIT 5")
    coords = cursor.fetchall()
    print("\n📋 Primeiras coordenadas:")
    for row in coords:
        print(f"   • {row[0]}: ({row[1]:.1f}, {row[2]:.1f}) - {row[3]:.1f}x{row[4]:.1f}")

conn.close()

print("\n" + "="*80)
print("📝 PRÓXIMO PASSO:")
print("   Se coords_count == 0 → Mapear campos primeiro")
print("   Se coords_count > 0 → Testar extração para ver logs")
print("="*80)
