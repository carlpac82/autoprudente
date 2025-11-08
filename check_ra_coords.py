#!/usr/bin/env python3
"""
Verificar coordenadas de Rental Agreement na base de dados
"""
import sqlite3
import os

def check_coords():
    print("\n" + "="*80)
    print("🔍 VERIFICANDO COORDENADAS DO RENTAL AGREEMENT")
    print("="*80)
    
    db_path = "data.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de dados não encontrada: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\n📊 Tabelas na BD: {len(tables)}")
    
    ra_tables = [t for t in tables if 'rental' in t.lower() or 'agreement' in t.lower()]
    print(f"\n🔍 Tabelas relacionadas com Rental Agreement:")
    for table in ra_tables:
        print(f"   • {table}")
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"     └─ {count} registos")
        
        if count > 0:
            # Mostrar estrutura
            cursor.execute(f"PRAGMA table_info({table})")
            cols = cursor.fetchall()
            print(f"     └─ Colunas: {', '.join([c[1] for c in cols])}")
            
            # Mostrar amostra
            cursor.execute(f"SELECT * FROM {table} LIMIT 3")
            rows = cursor.fetchall()
            print(f"     └─ Primeiros registos:")
            for row in rows:
                print(f"        {row}")
    
    conn.close()
    
    print("\n" + "="*80)

if __name__ == "__main__":
    check_coords()
