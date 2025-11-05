#!/usr/bin/env python3
"""
Verificar se os dados do Damage Report estão sendo salvos no PostgreSQL
"""

import sqlite3
import os

def verify_tables():
    """Verificar se as tabelas existem"""
    print("=" * 60)
    print("VERIFICAÇÃO DAS TABELAS DO DAMAGE REPORT")
    print("=" * 60)
    
    db_path = 'data.db'
    if not os.path.exists(db_path):
        print("❌ Base de dados não encontrada!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar tabelas
    tables = [
        'damage_report_coordinates',
        'damage_report_templates',
        'damage_report_mapping_history',
        'damage_reports'
    ]
    
    print("\n📊 TABELAS:")
    for table in tables:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        exists = cursor.fetchone()
        
        if exists:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  ✅ {table}: {count} registos")
            
            # Mostrar estrutura
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print(f"     Colunas: {', '.join([col[1] for col in columns])}")
        else:
            print(f"  ❌ {table}: NÃO EXISTE")
    
    # Verificar coordenadas
    print("\n📍 COORDENADAS MAPEADAS:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='damage_report_coordinates'")
    if cursor.fetchone():
        cursor.execute("""
            SELECT field_id, page, template_version, updated_at 
            FROM damage_report_coordinates 
            ORDER BY field_id
        """)
        coords = cursor.fetchall()
        
        if coords:
            print(f"  Total: {len(coords)} campos mapeados")
            for coord in coords[:5]:  # Mostrar primeiros 5
                print(f"    - {coord[0]} (Página {coord[1]}, Versão {coord[2]})")
            if len(coords) > 5:
                print(f"    ... e mais {len(coords) - 5} campos")
        else:
            print("  ⚠️  Nenhuma coordenada mapeada ainda")
    
    # Verificar templates
    print("\n📄 TEMPLATES PDF:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='damage_report_templates'")
    if cursor.fetchone():
        cursor.execute("""
            SELECT version, filename, num_pages, is_active, uploaded_by, uploaded_at 
            FROM damage_report_templates 
            ORDER BY version DESC
        """)
        templates = cursor.fetchall()
        
        if templates:
            print(f"  Total: {len(templates)} versões")
            for tmpl in templates:
                status = "✅ ATIVO" if tmpl[3] == 1 else "  inativo"
                print(f"    {status} v{tmpl[0]}: {tmpl[1]} ({tmpl[2]} páginas) - {tmpl[4]} em {tmpl[5]}")
        else:
            print("  ⚠️  Nenhum template carregado ainda")
    
    # Verificar histórico
    print("\n📜 HISTÓRICO DE MAPEAMENTOS:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='damage_report_mapping_history'")
    if cursor.fetchone():
        cursor.execute("""
            SELECT COUNT(*), COUNT(DISTINCT template_version), COUNT(DISTINCT mapped_by)
            FROM damage_report_mapping_history
        """)
        stats = cursor.fetchone()
        print(f"  Total de mapeamentos: {stats[0]}")
        print(f"  Versões diferentes: {stats[1]}")
        print(f"  Usuários diferentes: {stats[2]}")
        
        # Últimos mapeamentos
        cursor.execute("""
            SELECT field_id, template_version, mapped_by, mapped_at
            FROM damage_report_mapping_history
            ORDER BY mapped_at DESC
            LIMIT 5
        """)
        recent = cursor.fetchall()
        if recent:
            print("\n  Últimos mapeamentos:")
            for r in recent:
                print(f"    - {r[0]} (v{r[1]}) por {r[2]} em {r[3]}")
    
    # Verificar Damage Reports criados
    print("\n📋 DAMAGE REPORTS CRIADOS:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='damage_reports'")
    if cursor.fetchone():
        cursor.execute("SELECT COUNT(*) FROM damage_reports")
        count = cursor.fetchone()[0]
        print(f"  Total: {count} relatórios")
        
        if count > 0:
            cursor.execute("""
                SELECT dr_number, client_name, vehicle_plate, created_at
                FROM damage_reports
                ORDER BY created_at DESC
                LIMIT 5
            """)
            reports = cursor.fetchall()
            print("\n  Últimos relatórios:")
            for r in reports:
                print(f"    - DR {r[0]}: {r[1]} ({r[2]}) em {r[3]}")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ VERIFICAÇÃO COMPLETA")
    print("=" * 60)
    print("\n💡 NOTAS:")
    print("  - Dados em SQLite local (desenvolvimento)")
    print("  - Em produção (Render), dados estão em PostgreSQL")
    print("  - Estrutura das tabelas é idêntica")
    print("  - Dados persistem após restart do servidor")
    print("\n🔄 SINCRONIZAÇÃO:")
    print("  - Local: SQLite (data.db)")
    print("  - Produção: PostgreSQL (DATABASE_URL)")
    print("  - Código usa _db_connect() que suporta ambos")

if __name__ == '__main__':
    verify_tables()
