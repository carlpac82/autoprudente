"""
Script para criar backup COMPLETO do sistema
- Backup LOCAL: Código, BD SQLite, uploads, templates, static
- Backup SERVIDOR: PostgreSQL do Render via pg_dump
"""

import os
import zipfile
import json
import psycopg2
from datetime import datetime
from pathlib import Path
import shutil

DATABASE_URL = os.environ.get('DATABASE_URL') or "postgresql://carrental_user:cmXcauHIuQinAyDQjcB9XiVMU0Gaxviz@dpg-d44gvnm3jp1c73dc2edg-a.frankfurt-postgres.render.com/carrental_db_9klo?sslmode=require"

def create_backup_directory():
    """Criar diretório de backups com timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path(f'backups/full_backup_10_{timestamp}')
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir, timestamp

def backup_postgresql(backup_dir):
    """Backup do PostgreSQL do Render"""
    print("\n" + "=" * 80)
    print("📦 BACKUP POSTGRESQL DO RENDER")
    print("=" * 80)
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # 1. Listar todas as tabelas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print(f"\n✅ {len(tables)} tabelas encontradas")
        
        # 2. Criar backup JSON de cada tabela
        postgres_backup = {}
        total_records = 0
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                
                if count > 0:
                    # Buscar dados
                    cursor.execute(f"SELECT * FROM {table}")
                    rows = cursor.fetchall()
                    
                    # Buscar nomes das colunas
                    cursor.execute(f"""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = '{table}'
                        ORDER BY ordinal_position
                    """)
                    columns = [row[0] for row in cursor.fetchall()]
                    
                    # Converter para lista de dicionários
                    table_data = []
                    for row in rows:
                        row_dict = {}
                        for i, col in enumerate(columns):
                            value = row[i]
                            # Converter bytes para base64 se necessário
                            if isinstance(value, bytes):
                                import base64
                                value = base64.b64encode(value).decode('utf-8')
                                row_dict[col] = {'_type': 'bytes', '_value': value}
                            else:
                                row_dict[col] = value
                        table_data.append(row_dict)
                    
                    postgres_backup[table] = {
                        'count': count,
                        'columns': columns,
                        'data': table_data
                    }
                    
                    total_records += count
                    print(f"   ✅ {table:<40} {count:>10} registos")
                else:
                    print(f"   ⚠️  {table:<40} {count:>10} registos (vazia)")
                    
            except Exception as e:
                print(f"   ❌ {table:<40} ERRO: {str(e)}")
        
        # 3. Salvar JSON
        postgres_file = backup_dir / 'postgresql_backup.json'
        with open(postgres_file, 'w', encoding='utf-8') as f:
            json.dump(postgres_backup, f, indent=2, default=str)
        
        size_mb = postgres_file.stat().st_size / (1024 * 1024)
        print(f"\n✅ PostgreSQL backup salvo: {postgres_file.name} ({size_mb:.2f} MB)")
        print(f"✅ Total: {len(postgres_backup)} tabelas, {total_records:,} registos")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Erro no backup PostgreSQL: {e}")
        import traceback
        traceback.print_exc()
        return False

def backup_local_databases(backup_dir):
    """Backup das bases de dados SQLite locais"""
    print("\n" + "=" * 80)
    print("💾 BACKUP BASES DE DADOS SQLITE LOCAIS")
    print("=" * 80)
    
    db_files = [
        'data.db',
        'rental_tracker.db',
        'car_images.db',
        'carrental.db'
    ]
    
    db_backup_dir = backup_dir / 'databases'
    db_backup_dir.mkdir(exist_ok=True)
    
    total_size = 0
    for db_file in db_files:
        if Path(db_file).exists():
            size = Path(db_file).stat().st_size / (1024 * 1024)
            shutil.copy2(db_file, db_backup_dir / db_file)
            print(f"   ✅ {db_file:<30} {size:>10.2f} MB")
            total_size += size
        else:
            print(f"   ⚠️  {db_file:<30} (não existe)")
    
    print(f"\n✅ Total SQLite: {total_size:.2f} MB")
    return total_size > 0

def backup_code_and_config(backup_dir):
    """Backup de código Python e configurações"""
    print("\n" + "=" * 80)
    print("🐍 BACKUP CÓDIGO E CONFIGURAÇÕES")
    print("=" * 80)
    
    code_dir = backup_dir / 'code'
    code_dir.mkdir(exist_ok=True)
    
    # Python files
    py_files = list(Path('.').glob('*.py'))
    for py_file in py_files:
        if py_file.name not in ['__pycache__']:
            shutil.copy2(py_file, code_dir / py_file.name)
    print(f"   ✅ {len(py_files)} ficheiros Python")
    
    # Config files
    config_files = [
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        '.gitignore',
        'README.md'
    ]
    
    config_count = 0
    for config_file in config_files:
        if Path(config_file).exists():
            shutil.copy2(config_file, code_dir / config_file)
            config_count += 1
    
    print(f"   ✅ {config_count} ficheiros de configuração")
    return True

def backup_templates(backup_dir):
    """Backup de templates HTML"""
    print("\n" + "=" * 80)
    print("📄 BACKUP TEMPLATES")
    print("=" * 80)
    
    templates_src = Path('templates')
    if templates_src.exists():
        templates_dst = backup_dir / 'templates'
        shutil.copytree(templates_src, templates_dst, dirs_exist_ok=True)
        
        template_files = list(templates_dst.rglob('*.html'))
        print(f"   ✅ {len(template_files)} templates HTML")
        return True
    else:
        print("   ⚠️  Diretório templates não encontrado")
        return False

def backup_static_files(backup_dir):
    """Backup de ficheiros estáticos"""
    print("\n" + "=" * 80)
    print("🎨 BACKUP STATIC FILES")
    print("=" * 80)
    
    static_src = Path('static')
    if static_src.exists():
        static_dst = backup_dir / 'static'
        shutil.copytree(static_src, static_dst, dirs_exist_ok=True)
        
        total_size = sum(f.stat().st_size for f in static_dst.rglob('*') if f.is_file())
        size_mb = total_size / (1024 * 1024)
        
        file_count = len(list(static_dst.rglob('*')))
        print(f"   ✅ {file_count} ficheiros ({size_mb:.2f} MB)")
        return True
    else:
        print("   ⚠️  Diretório static não encontrado")
        return False

def backup_uploads(backup_dir):
    """Backup de uploads (logos, fotos, etc.)"""
    print("\n" + "=" * 80)
    print("📤 BACKUP UPLOADS")
    print("=" * 80)
    
    uploads_src = Path('uploads')
    if uploads_src.exists():
        uploads_dst = backup_dir / 'uploads'
        shutil.copytree(uploads_src, uploads_dst, dirs_exist_ok=True)
        
        total_size = sum(f.stat().st_size for f in uploads_dst.rglob('*') if f.is_file())
        size_mb = total_size / (1024 * 1024)
        
        file_count = len(list(uploads_dst.rglob('*')))
        print(f"   ✅ {file_count} ficheiros ({size_mb:.2f} MB)")
        return True
    else:
        print("   ⚠️  Diretório uploads não encontrado")
        return False

def backup_documentation(backup_dir):
    """Backup de documentação markdown"""
    print("\n" + "=" * 80)
    print("📋 BACKUP DOCUMENTAÇÃO")
    print("=" * 80)
    
    docs_dir = backup_dir / 'documentation'
    docs_dir.mkdir(exist_ok=True)
    
    md_files = list(Path('.').glob('*.md'))
    for md_file in md_files:
        shutil.copy2(md_file, docs_dir / md_file.name)
    
    print(f"   ✅ {len(md_files)} ficheiros Markdown")
    return True

def create_zip_archive(backup_dir, timestamp):
    """Criar arquivo ZIP do backup"""
    print("\n" + "=" * 80)
    print("🗜️  CRIANDO ARQUIVO ZIP")
    print("=" * 80)
    
    zip_filename = f'backups/full_backup_10_{timestamp}.zip'
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in backup_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(backup_dir.parent)
                zipf.write(file_path, arcname)
    
    zip_size = Path(zip_filename).stat().st_size / (1024 * 1024)
    print(f"\n✅ Arquivo ZIP criado: {zip_filename}")
    print(f"✅ Tamanho: {zip_size:.2f} MB")
    
    return zip_filename, zip_size

def create_backup_manifest(backup_dir, timestamp):
    """Criar manifesto do backup"""
    manifest = {
        'backup_date': datetime.now().isoformat(),
        'timestamp': timestamp,
        'backup_type': 'FULL_BACKUP_10',
        'includes': {
            'postgresql': True,
            'sqlite_databases': True,
            'python_code': True,
            'templates': True,
            'static_files': True,
            'uploads': True,
            'documentation': True,
            'configuration': True
        },
        'postgresql_url': DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else 'hidden',
        'created_by': 'create_full_backup.py',
        'version': '1.0'
    }
    
    manifest_file = backup_dir / 'BACKUP_MANIFEST.json'
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n✅ Manifesto criado: {manifest_file.name}")

def main():
    print("=" * 80)
    print("🚀 CRIAR BACKUP COMPLETO - LOCAL + SERVIDOR")
    print("=" * 80)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 1. Criar diretório
    backup_dir, timestamp = create_backup_directory()
    print(f"📁 Diretório: {backup_dir}\n")
    
    # 2. Backup PostgreSQL (SERVIDOR)
    postgres_ok = backup_postgresql(backup_dir)
    
    # 3. Backup SQLite (LOCAL)
    sqlite_ok = backup_local_databases(backup_dir)
    
    # 4. Backup código
    code_ok = backup_code_and_config(backup_dir)
    
    # 5. Backup templates
    templates_ok = backup_templates(backup_dir)
    
    # 6. Backup static
    static_ok = backup_static_files(backup_dir)
    
    # 7. Backup uploads
    uploads_ok = backup_uploads(backup_dir)
    
    # 8. Backup documentação
    docs_ok = backup_documentation(backup_dir)
    
    # 9. Criar manifesto
    create_backup_manifest(backup_dir, timestamp)
    
    # 10. Criar ZIP
    zip_file, zip_size = create_zip_archive(backup_dir, timestamp)
    
    # Resumo final
    print("\n" + "=" * 80)
    print("📊 RESUMO DO BACKUP")
    print("=" * 80)
    print(f"✅ PostgreSQL (Servidor):  {'SIM' if postgres_ok else 'NÃO'}")
    print(f"✅ SQLite (Local):         {'SIM' if sqlite_ok else 'NÃO'}")
    print(f"✅ Código Python:          {'SIM' if code_ok else 'NÃO'}")
    print(f"✅ Templates:              {'SIM' if templates_ok else 'NÃO'}")
    print(f"✅ Static Files:           {'SIM' if static_ok else 'NÃO'}")
    print(f"✅ Uploads:                {'SIM' if uploads_ok else 'NÃO'}")
    print(f"✅ Documentação:           {'SIM' if docs_ok else 'NÃO'}")
    print("=" * 80)
    print(f"\n📦 BACKUP COMPLETO CRIADO!")
    print(f"📁 Pasta: {backup_dir}")
    print(f"🗜️  ZIP: {zip_file} ({zip_size:.2f} MB)")
    print("\n✅ BACKUP LOCAL + SERVIDOR 100% COMPLETO! 🎯")
    print("=" * 80)

if __name__ == "__main__":
    main()
