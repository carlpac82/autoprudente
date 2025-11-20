#!/usr/bin/env python3
"""
Script para investigar e corrigir search_type de Novembro 2025

Este script:
1. Lista todas as 27 entradas de Novembro
2. Identifica quais deveriam ser 'current' mas estão como 'automated'
3. Oferece opção de corrigir automaticamente
"""

import os
import psycopg2
from datetime import datetime
import json

def connect_db():
    """Connect to PostgreSQL database"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise Exception("DATABASE_URL environment variable not set")
    
    # Handle Render.com postgres:// -> postgresql:// conversion
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return psycopg2.connect(database_url)

def analyze_november():
    """Analyze November 2025 entries"""
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            # Get all November entries
            cur.execute("""
                SELECT 
                    id,
                    location,
                    search_type,
                    search_date,
                    pickup_date,
                    price_count,
                    user_email,
                    CAST(search_date AS DATE) as search_day,
                    CAST(search_date AS TIME) as search_time
                FROM automated_search_history
                WHERE month_key = '2025-11'
                ORDER BY search_date DESC
            """)
            
            rows = cur.fetchall()
            
            print(f"\n{'='*80}")
            print(f"ANÁLISE DE NOVEMBRO 2025 - {len(rows)} ENTRADAS")
            print(f"{'='*80}\n")
            
            # Group by day
            by_day = {}
            for row in rows:
                search_id, location, search_type, search_date, pickup_date, price_count, user_email, search_day, search_time = row
                
                day_key = str(search_day)
                if day_key not in by_day:
                    by_day[day_key] = []
                
                by_day[day_key].append({
                    'id': search_id,
                    'location': location,
                    'search_type': search_type,
                    'search_date': search_date,
                    'pickup_date': pickup_date,
                    'price_count': price_count,
                    'user_email': user_email,
                    'search_time': str(search_time)
                })
            
            # Analyze patterns
            print(f"📅 Entradas por dia:\n")
            
            potential_issues = []
            
            for day in sorted(by_day.keys(), reverse=True):
                entries = by_day[day]
                auto_count = sum(1 for e in entries if e['search_type'] == 'automated')
                curr_count = sum(1 for e in entries if e['search_type'] == 'current')
                
                print(f"  {day}: {len(entries)} total ({auto_count} auto, {curr_count} current)")
                
                # Check for multiple entries on same day - might indicate manual searches marked as auto
                if len(entries) > 1 and curr_count == 0:
                    print(f"    ⚠️  SUSPEITO: {len(entries)} entradas mas nenhuma 'current'!")
                    for entry in entries:
                        print(f"       - ID {entry['id']}: {entry['search_time']} - {entry['search_type']} - {entry['price_count']} preços")
                        # If multiple searches on same day with different times, probably manual
                        if len(entries) > 1:
                            potential_issues.append(entry)
            
            print(f"\n{'='*80}")
            print(f"RESUMO:")
            print(f"{'='*80}")
            print(f"Total de entradas: {len(rows)}")
            print(f"Entradas 'automated': {sum(1 for r in rows if r[2] == 'automated')}")
            print(f"Entradas 'current': {sum(1 for r in rows if r[2] == 'current')}")
            print(f"Dias com múltiplas entradas: {sum(1 for entries in by_day.values() if len(entries) > 1)}")
            print(f"Potenciais problemas identificados: {len(potential_issues)}")
            
            # Detailed analysis of suspicious entries
            if potential_issues:
                print(f"\n{'='*80}")
                print(f"ENTRADAS SUSPEITAS (podem estar incorretas):")
                print(f"{'='*80}\n")
                
                for entry in potential_issues:
                    print(f"ID {entry['id']}:")
                    print(f"  Data: {entry['search_date']}")
                    print(f"  Hora: {entry['search_time']}")
                    print(f"  Tipo: {entry['search_type']} (deveria ser 'current'?)")
                    print(f"  Location: {entry['location']}")
                    print(f"  Pickup Date: {entry['pickup_date']}")
                    print(f"  Preços: {entry['price_count']}")
                    print(f"  User: {entry['user_email']}")
                    print()
            
            return potential_issues
            
    finally:
        conn.close()

def fix_search_types(entry_ids):
    """Fix search_type from 'automated' to 'current' for given IDs"""
    if not entry_ids:
        print("Nenhuma entrada para corrigir.")
        return
    
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            # Update search_type
            cur.execute("""
                UPDATE automated_search_history
                SET search_type = 'current'
                WHERE id = ANY(%s)
                  AND search_type = 'automated'
            """, (entry_ids,))
            
            updated_count = cur.rowcount
            conn.commit()
            
            print(f"\n✅ Corrigidas {updated_count} entradas de 'automated' para 'current'")
            
    finally:
        conn.close()

if __name__ == '__main__':
    print("\n🔍 A analisar entradas de Novembro 2025...\n")
    
    try:
        potential_issues = analyze_november()
        
        # Ask user if they want to fix
        if potential_issues:
            print(f"\n{'='*80}")
            print("OPÇÕES:")
            print(f"{'='*80}")
            print("1. Não fazer nada (apenas análise)")
            print("2. Corrigir TODAS as entradas suspeitas para 'current'")
            print("3. Deixar-me escolher manualmente")
            
            choice = input("\nEscolha uma opção (1/2/3): ").strip()
            
            if choice == '2':
                entry_ids = [e['id'] for e in potential_issues]
                fix_search_types(entry_ids)
                print("\n✅ Correção completa! Execute novamente para verificar.")
            elif choice == '3':
                print("\nPor favor lista os IDs que quer corrigir, separados por vírgula:")
                ids_input = input("IDs: ").strip()
                entry_ids = [int(id.strip()) for id in ids_input.split(',') if id.strip().isdigit()]
                if entry_ids:
                    fix_search_types(entry_ids)
                    print("\n✅ Correção completa! Execute novamente para verificar.")
                else:
                    print("❌ Nenhum ID válido fornecido.")
            else:
                print("\n✅ Análise completa. Nenhuma alteração feita.")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
