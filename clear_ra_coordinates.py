#!/usr/bin/env python3
"""
Limpar TODAS as coordenadas do Rental Agreement para começar de novo
"""
import sqlite3

print("\n" + "="*80)
print("🗑️  LIMPAR COORDENADAS DO RENTAL AGREEMENT")
print("="*80)

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Ver quantas coordenadas existem
cursor.execute("SELECT COUNT(*) FROM rental_agreement_coordinates")
count_before = cursor.fetchone()[0]
print(f"\n📊 Coordenadas ANTES: {count_before}")

# Limpar TODAS as coordenadas
cursor.execute("DELETE FROM rental_agreement_coordinates")
conn.commit()

# Verificar
cursor.execute("SELECT COUNT(*) FROM rental_agreement_coordinates")
count_after = cursor.fetchone()[0]
print(f"📊 Coordenadas DEPOIS: {count_after}")

conn.close()

print(f"\n✅ {count_before} coordenadas removidas!")
print("\n💡 PRÓXIMO PASSO:")
print("   1. Abrir: http://localhost:8000/rental-agreement-mapper")
print("   2. Fazer upload do PDF do Rental Agreement")
print("   3. Mapear CUIDADOSAMENTE cada campo:")
print("      - Número Contrato → Caixa no número do contrato")
print("      - Nome Cliente → Caixa no NOME (ex: EIKE BERENS)")
print("      - Matrícula → Caixa na matrícula")
print("      - etc.")
print("   4. Salvar coordenadas")
print("   5. Testar extração novamente")
print("\n" + "="*80)
