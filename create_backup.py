import os
import zipfile
import shutil
from datetime import datetime

def create_backup():
    # Nome do arquivo de backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = 'backups'
    backup_file = os.path.join(backup_dir, f'backup_full_{timestamp}.zip')
    
    # Lista de diretórios e arquivos para backup
    backup_paths = [
        'templates/',
        'static/',
        'data/',
        'uploads/',
        'main.py',
        'requirements.txt',
        'config.py',
        '.env',
        '*.db',
        '*.sqlite'
    ]
    
    # Criar diretório de backups se não existir
    os.makedirs(backup_dir, exist_ok=True)
    
    # Criar arquivo ZIP
    with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for path in backup_paths:
            if os.path.isfile(path):
                zipf.write(path)
            elif os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            zipf.write(file_path)
                        except Exception as e:
                            print(f"Aviso: Não foi possível adicionar {file_path}: {e}")
    
    print(f"Backup criado com sucesso: {backup_file}")
    print(f"Tamanho: {os.path.getsize(backup_file) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    print("Iniciando backup completo do sistema...")
    create_backup()
