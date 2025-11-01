#!/usr/bin/env python3
"""
Script para migrar dados do localStorage para a database
Executa uma vez para sincronizar todos os dados
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = 'rental_prices.db'

def migrate_to_database():
    """
    Este script cria um endpoint que o frontend pode chamar
    para enviar todos os dados do localStorage para a database
    """
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("MIGRATION SCRIPT - LocalStorage → Database")
    print("=" * 60)
    
    # Verificar se as tabelas existem
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print("\n📋 Tables in database:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  ✅ {table}: {count} rows")
    
    print("\n" + "=" * 60)
    print("MIGRATION INSTRUCTIONS")
    print("=" * 60)
    print("""
1. Abra o website no browser
2. Abra o Console (F12 → Console)
3. Cole e execute o seguinte código:

// ============================================================
// MIGRATION SCRIPT - LocalStorage → Database
// ============================================================

async function migrateAllLocalStorageToDatabase() {
    console.log('🚀 Starting migration...');
    
    const results = {
        success: [],
        errors: []
    };
    
    // 1. Migrate Vans Pricing
    try {
        const vansPricing = JSON.parse(localStorage.getItem('vansPricing') || '{}');
        if (Object.keys(vansPricing).length > 0) {
            const response = await fetch('/api/vans-pricing', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(vansPricing)
            });
            const data = await response.json();
            if (data.ok) {
                results.success.push('✅ Vans Pricing migrated');
            } else {
                results.errors.push('❌ Vans Pricing: ' + data.error);
            }
        }
    } catch (e) {
        results.errors.push('❌ Vans Pricing: ' + e.message);
    }
    
    // 2. Migrate Automation Settings
    try {
        const settings = JSON.parse(localStorage.getItem('priceAutomationSettings') || '{}');
        if (Object.keys(settings).length > 0) {
            const response = await fetch('/api/automation-settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(settings)
            });
            const data = await response.json();
            if (data.ok) {
                results.success.push('✅ Automation Settings migrated');
            } else {
                results.errors.push('❌ Automation Settings: ' + data.error);
            }
        }
    } catch (e) {
        results.errors.push('❌ Automation Settings: ' + e.message);
    }
    
    // 3. Migrate Custom Days
    try {
        const customDias = JSON.parse(localStorage.getItem('customDias') || '[]');
        if (customDias.length > 0) {
            const response = await fetch('/api/custom-days', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ days: customDias })
            });
            const data = await response.json();
            if (data.ok) {
                results.success.push('✅ Custom Days migrated (' + customDias.length + ' days)');
            } else {
                results.errors.push('❌ Custom Days: ' + data.error);
            }
        }
    } catch (e) {
        results.errors.push('❌ Custom Days: ' + e.message);
    }
    
    // 4. Show Results
    console.log('\\n' + '='.repeat(60));
    console.log('MIGRATION RESULTS');
    console.log('='.repeat(60));
    
    if (results.success.length > 0) {
        console.log('\\n✅ SUCCESS:');
        results.success.forEach(msg => console.log('  ' + msg));
    }
    
    if (results.errors.length > 0) {
        console.log('\\n❌ ERRORS:');
        results.errors.forEach(msg => console.log('  ' + msg));
    }
    
    console.log('\\n' + '='.repeat(60));
    console.log('MIGRATION COMPLETE!');
    console.log('='.repeat(60));
    
    return results;
}

// Execute migration
migrateAllLocalStorageToDatabase();

// ============================================================

4. Aguarde a migração completar
5. Verifique os resultados no console

NOTA: Este script migra:
  - Vans Pricing (C3, C4, C5)
  - Automation Settings (excludeSuppliers, comissao)
  - Custom Days (dias personalizados)

Dados que NÃO precisam migração (já salvos automaticamente):
  - Export History (já na DB)
  - User Settings (já na DB)
  - AI Learning Data (será migrado quando implementado)
""")
    
    conn.close()

if __name__ == '__main__':
    migrate_to_database()
