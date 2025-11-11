#!/usr/bin/env python3
"""
Script para adicionar as rotas de vehicle inspection ao main.py
"""

import os
import shutil
from datetime import datetime

def add_routes_to_main():
    """Adiciona as rotas de vehicle inspection ao main.py"""
    
    print("🔧 ADICIONANDO ROTAS DE VEHICLE INSPECTION")
    print("=" * 50)
    
    # 1. Fazer backup do main.py atual
    backup_name = f"main.py.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy("main.py", backup_name)
    print(f"✅ Backup criado: {backup_name}")
    
    # 2. Ler o arquivo main.py
    with open("main.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 3. Ler as rotas do arquivo separado
    with open("vehicle_inspection_routes.py", "r", encoding="utf-8") as f:
        routes_content = f.read()
    
    # 4. Extrair apenas as funções das rotas (sem imports)
    routes_lines = routes_content.split('\n')
    route_functions = []
    in_function = False
    current_function = []
    
    for line in routes_lines:
        if line.strip().startswith('@app.'):
            in_function = True
            current_function = [line]
        elif in_function:
            current_function.append(line)
            # Se chegou ao final da função (linha vazia ou nova função)
            if (line.strip() == "" and len(current_function) > 10) or line.strip().startswith('@app.'):
                if line.strip().startswith('@app.'):
                    # Nova função começando, salvar a anterior
                    route_functions.append('\n'.join(current_function[:-1]))
                    current_function = [line]
                else:
                    # Função terminou
                    route_functions.append('\n'.join(current_function))
                    in_function = False
                    current_function = []
    
    # Adicionar última função se existir
    if current_function:
        route_functions.append('\n'.join(current_function))
    
    # 5. Encontrar onde inserir as rotas (antes do if __name__)
    lines = content.split('\n')
    insert_index = -1
    
    for i, line in enumerate(lines):
        if line.strip().startswith('if __name__ == "__main__":'):
            insert_index = i
            break
    
    if insert_index == -1:
        print("❌ Não foi possível encontrar 'if __name__ == \"__main__\"' no main.py")
        return False
    
    # 6. Inserir as rotas
    new_lines = lines[:insert_index]
    
    # Adicionar comentário
    new_lines.append("")
    new_lines.append("# =" * 80)
    new_lines.append("# VEHICLE INSPECTION ROUTES")
    new_lines.append("# =" * 80)
    new_lines.append("")
    
    # Adicionar cada rota
    for route_func in route_functions:
        if route_func.strip():
            new_lines.extend(route_func.split('\n'))
            new_lines.append("")
    
    # Adicionar o resto do arquivo
    new_lines.extend(lines[insert_index:])
    
    # 7. Escrever o novo arquivo
    new_content = '\n'.join(new_lines)
    
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"✅ Adicionadas {len(route_functions)} rotas ao main.py")
    print("✅ Arquivo main.py atualizado com sucesso!")
    
    return True

def main():
    if not os.path.exists("main.py"):
        print("❌ Arquivo main.py não encontrado!")
        return
    
    if not os.path.exists("vehicle_inspection_routes.py"):
        print("❌ Arquivo vehicle_inspection_routes.py não encontrado!")
        return
    
    success = add_routes_to_main()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 ROTAS ADICIONADAS COM SUCESSO!")
        print("🔧 Próximos passos:")
        print("1. Reiniciar o servidor:")
        print("   python3 main.py")
        print("2. Testar as rotas:")
        print("   http://localhost:8000/check-in")
        print("   http://localhost:8000/check-out")
        print("   http://localhost:8000/vehicle-inspections")
        print("\n📝 NOTA: As rotas são mock implementations")
        print("   Para funcionalidade completa, implemente:")
        print("   - Database schema para inspections")
        print("   - Email sending")
        print("   - PDF generation")
    else:
        print("\n❌ Falha ao adicionar rotas!")

if __name__ == "__main__":
    main()
