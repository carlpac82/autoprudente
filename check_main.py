#!/usr/bin/env python3
"""
Script para verificar e diagnosticar problemas com o main.py
"""

import os
import sys

def check_main_file():
    main_path = "main.py"
    
    print("🔍 DIAGNÓSTICO DO ARQUIVO MAIN.PY")
    print("=" * 50)
    
    # 1. Verificar se arquivo existe
    if not os.path.exists(main_path):
        print("❌ Arquivo main.py não encontrado!")
        return False
    
    # 2. Verificar tamanho do arquivo
    size = os.path.getsize(main_path)
    print(f"📁 Tamanho do arquivo: {size:,} bytes")
    
    # 3. Ler primeiras linhas
    try:
        with open(main_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"📄 Total de linhas: {len(lines)}")
        
        # 4. Verificar imports essenciais
        content = ''.join(lines)
        
        checks = [
            ("FastAPI import", "from fastapi import" in content or "import fastapi" in content),
            ("FastAPI app", "app = FastAPI" in content),
            ("Uvicorn", "uvicorn" in content),
            ("Routes (@app.)", "@app." in content),
            ("Main block", "if __name__" in content),
        ]
        
        print("\n🔍 VERIFICAÇÕES:")
        for name, check in checks:
            status = "✅" if check else "❌"
            print(f"{status} {name}")
        
        # 5. Contar rotas
        route_count = content.count("@app.")
        print(f"\n🛣️  Total de rotas encontradas: {route_count}")
        
        # 6. Verificar se há problemas de encoding
        try:
            content.encode('utf-8')
            print("✅ Encoding UTF-8 OK")
        except:
            print("❌ Problema de encoding")
        
        # 7. Verificar estrutura básica
        if "from fastapi import" not in content:
            print("\n🚨 PROBLEMA CRÍTICO: FastAPI não importado!")
            print("   O arquivo parece estar corrompido ou incompleto.")
            
            # Sugerir restauração do backup
            backup_path = "backups/full_backup_10_20251106_010005/code/main.py"
            if os.path.exists(backup_path):
                print(f"💡 SOLUÇÃO: Restaurar do backup em {backup_path}")
                return "restore_backup"
            else:
                print("💡 SOLUÇÃO: Recriar arquivo main.py do zero")
                return "recreate"
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return False

def main():
    result = check_main_file()
    
    if result == "restore_backup":
        print("\n" + "="*50)
        print("🔧 AÇÃO RECOMENDADA:")
        print("1. Fazer backup do main.py atual:")
        print("   cp main.py main.py.broken")
        print("2. Restaurar do backup:")
        print("   cp backups/full_backup_10_20251106_010005/code/main.py .")
        print("3. Reiniciar o servidor:")
        print("   python main.py")
        
    elif result == "recreate":
        print("\n" + "="*50)
        print("🔧 AÇÃO RECOMENDADA:")
        print("O arquivo main.py precisa ser recriado do zero.")
        
    elif result:
        print("\n✅ Arquivo main.py parece estar OK")
        print("🔧 Verificar se o servidor está rodando:")
        print("   python main.py")
        print("   Ou: uvicorn main:app --host 0.0.0.0 --port 8000")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    main()
