#!/usr/bin/env python3
"""
Script MELHORADO para importar fotos da Carjet com garantia de mapeamento correto.
Usa os códigos dos carros (C45, C25, etc.) para identificação única.
"""

import sqlite3
import json
import os
import shutil
from pathlib import Path

# Diretórios
CARJET_PHOTOS_DIR = 'carjet_photos_v2'
UPLOADED_PHOTOS_DIR = 'uploaded'
CARJET_DATA_FILE = 'carjet_cars_data_v2.json'
DATABASE_FILE = 'data.db'

def normalize_car_name(name):
    """
    Normaliza o nome do carro para facilitar matching
    """
    # Remover espaços extras, converter para minúsculas
    name = name.strip().lower()
    
    # Remover sufixos comuns
    suffixes_to_remove = [
        ', hybrid', ', electric', 
        ' auto', ' hybrid', ' electric',
        ' sw', ' cabrio', ' 4x4'
    ]
    
    for suffix in suffixes_to_remove:
        if name.endswith(suffix):
            name = name[:-len(suffix)].strip()
    
    return name


def get_vehicle_mapping():
    """
    Retorna mapeamento de nomes de carros da Carjet para nomes parametrizados
    """
    # Mapeamento manual de nomes diferentes
    manual_mapping = {
        'vw polo': 'volkswagen polo',
        'vw golf': 'volkswagen golf',
        'vw taigo': 'volkswagen taigo',
        'vw tiguan': 'volkswagen tiguan',
        'vw passat': 'volkswagen passat',
        'vw caddy': 'volkswagen caddy',
        'vw caravelle': 'volkswagen caravelle',
        'vw multivan': 'volkswagen multivan',
        'vw sharan': 'volkswagen sharan',
        'vw transporter': 'volkswagen transporter',
        'volkswagen up': 'volkswagen up!',
        'volkswagen t-cross': 'volkswagen t-cross',
        'volkswagen t-roc': 'volkswagen t-roc',
        'volkswagen id.5 5 door': 'volkswagen id.5',
        'toyota chr': 'toyota c-hr',
        'mercedes a class': 'mercedes-benz a-class',
        'mercedes c class': 'mercedes-benz c-class',
        'mercedes e class': 'mercedes-benz e-class',
        'mercedes s class': 'mercedes-benz s-class',
        'mercedes v class': 'mercedes-benz v-class',
        'mercedes gla': 'mercedes-benz gla',
        'mercedes glb 7 seater': 'mercedes-benz glb',
        'mercedes cla': 'mercedes-benz cla',
        'mercedes cle coupe': 'mercedes-benz cle',
        'mercedes vito': 'mercedes-benz vito',
        'mercedes benz vito': 'mercedes-benz vito',
        'bmw 1 series': 'bmw 1 series',
        'bmw 2 series gran coupe': 'bmw 2 series',
        'bmw 3 series': 'bmw 3 series',
        'bmw 4 series gran coupe': 'bmw 4 series',
        'bmw 5 series': 'bmw 5 series',
        'mini countryman': 'mini countryman',
        'mini one cabrio': 'mini one',
        'range rover evoque': 'range rover evoque',
        'byd seal u': 'byd seal u',
        'mg zs': 'mg zs',
        'mazda mx5 cabrio': 'mazda mx-5',
        'mazda 2': 'mazda 2',
        'volvo ex30': 'volvo ex30',
        'volvo xc40': 'volvo xc40',
        'volvo xc60': 'volvo xc60',
        'volvo v60': 'volvo v60',
        'volvo v60 4x4': 'volvo v60',
    }
    
    return manual_mapping


def import_photos_to_database():
    """
    Importa fotos da Carjet para a base de dados com mapeamento preciso
    """
    print("=" * 80)
    print("📸 IMPORTAÇÃO DE FOTOS DA CARJET V2 (Mapeamento Preciso)")
    print("=" * 80)
    print()
    
    # Verificar se os ficheiros existem
    if not os.path.exists(CARJET_DATA_FILE):
        print(f"❌ Ficheiro {CARJET_DATA_FILE} não encontrado!")
        return
    
    if not os.path.exists(CARJET_PHOTOS_DIR):
        print(f"❌ Diretório {CARJET_PHOTOS_DIR} não encontrado!")
        return
    
    if not os.path.exists(DATABASE_FILE):
        print(f"❌ Base de dados {DATABASE_FILE} não encontrada!")
        return
    
    # Criar diretório uploaded se não existir
    os.makedirs(UPLOADED_PHOTOS_DIR, exist_ok=True)
    
    # Carregar dados dos carros
    with open(CARJET_DATA_FILE, 'r', encoding='utf-8') as f:
        carjet_cars = json.load(f)
    
    # Filtrar apenas fotos reais (não placeholders)
    real_cars = [c for c in carjet_cars if not c['is_placeholder']]
    
    print(f"📦 Carregados {len(carjet_cars)} carros do ficheiro JSON")
    print(f"📸 Fotos reais (não placeholders): {len(real_cars)}")
    print()
    
    # Conectar à base de dados
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Obter mapeamento de nomes
    manual_mapping = get_vehicle_mapping()
    
    # Estatísticas
    matched = 0
    not_matched = 0
    photos_copied = 0
    photos_updated = 0
    
    print("🔍 A processar carros COM FOTOS REAIS...")
    print()
    
    # Processar apenas carros com fotos reais
    for car in real_cars:
        carjet_name = car['name']
        photo_url = car['photo_url']
        category = car['category']
        car_code = car['car_code']
        
        # Normalizar nome
        normalized_name = normalize_car_name(carjet_name)
        
        # Aplicar mapeamento manual se existir
        if normalized_name in manual_mapping:
            search_name = manual_mapping[normalized_name]
        else:
            search_name = normalized_name
        
        # Procurar na tabela vehicle_name_overrides
        # Tentar várias variações do nome
        search_variations = [
            search_name,
            normalized_name,
            carjet_name.lower(),
        ]
        
        result = None
        for search_var in search_variations:
            cursor.execute("""
                SELECT original_name, edited_name 
                FROM vehicle_name_overrides 
                WHERE LOWER(original_name) LIKE ? OR LOWER(edited_name) LIKE ?
            """, (f'%{search_var}%', f'%{search_var}%'))
            
            result = cursor.fetchone()
            if result:
                break
        
        if result:
            original_name, edited_name = result
            matched += 1
            
            # Determinar nome do ficheiro da foto
            # USAR O CÓDIGO DO CARRO para garantir identificação única
            if car_code:
                # Nome com código: C45_Fiat_Panda.jpg
                safe_name = f"{car_code}_{carjet_name.replace(' ', '_').replace(',', '').replace('/', '_')}"
            else:
                # Fallback sem código
                safe_name = carjet_name.replace(' ', '_').replace(',', '').replace('/', '_')
            
            # Procurar ficheiro no diretório
            photo_files = [
                f for f in os.listdir(CARJET_PHOTOS_DIR)
                if f.startswith(safe_name) or (car_code and f.startswith(car_code))
            ]
            
            if photo_files:
                source_file = os.path.join(CARJET_PHOTOS_DIR, photo_files[0])
                
                # Verificar tamanho (só copiar se > 1KB = foto real)
                file_size = os.path.getsize(source_file)
                
                if file_size > 1024:  # Maior que 1KB
                    # Copiar para uploaded com nome padronizado
                    ext = os.path.splitext(photo_files[0])[1]
                    vehicle_name_safe = (edited_name or original_name).replace(' ', '_').replace('/', '_')
                    
                    # Incluir código do carro no nome do ficheiro
                    if car_code:
                        dest_filename = f"carjet_{car_code}_{vehicle_name_safe}{ext}"
                    else:
                        dest_filename = f"carjet_{vehicle_name_safe}{ext}"
                    
                    dest_file = os.path.join(UPLOADED_PHOTOS_DIR, dest_filename)
                    
                    # Copiar ficheiro
                    shutil.copy2(source_file, dest_file)
                    photos_copied += 1
                    
                    # Ler ficheiro como BLOB
                    with open(dest_file, 'rb') as f:
                        photo_blob = f.read()
                    
                    # Determinar content_type
                    content_type = 'image/jpeg'
                    if ext.lower() == '.png':
                        content_type = 'image/png'
                    elif ext.lower() == '.gif':
                        content_type = 'image/gif'
                    elif ext.lower() == '.webp':
                        content_type = 'image/webp'
                    
                    # Atualizar base de dados - tabela vehicle_photos
                    cursor.execute("""
                        INSERT OR REPLACE INTO vehicle_photos (vehicle_name, photo_data, photo_url, content_type)
                        VALUES (?, ?, ?, ?)
                    """, (edited_name or original_name, photo_blob, photo_url, content_type))
                    
                    photos_updated += 1
                    
                    print(f"✅ {carjet_name}")
                    print(f"   → Código: {car_code}")
                    print(f"   → Mapeado para: {edited_name or original_name}")
                    print(f"   → Foto: {dest_filename} ({file_size:,} bytes)")
                    print(f"   → URL: {photo_url}")
                    print()
                else:
                    print(f"⚠️  {carjet_name}")
                    print(f"   → Código: {car_code}")
                    print(f"   → Mapeado para: {edited_name or original_name}")
                    print(f"   → Foto muito pequena (placeholder): {file_size} bytes")
                    print()
            else:
                print(f"⚠️  {carjet_name}")
                print(f"   → Código: {car_code}")
                print(f"   → Mapeado para: {edited_name or original_name}")
                print(f"   → Foto não encontrada!")
                print()
        else:
            not_matched += 1
            print(f"❌ {carjet_name}")
            print(f"   → Código: {car_code}")
            print(f"   → Não encontrado na base de dados")
            print(f"   → URL: {photo_url}")
            print()
    
    # Commit das alterações
    conn.commit()
    conn.close()
    
    print()
    print("=" * 80)
    print("📊 RESUMO DA IMPORTAÇÃO")
    print("=" * 80)
    print(f"📸 Fotos reais disponíveis: {len(real_cars)}")
    print(f"✅ Carros mapeados: {matched}")
    print(f"❌ Carros não mapeados: {not_matched}")
    print(f"📸 Fotos copiadas: {photos_copied}")
    print(f"💾 Registos atualizados na BD: {photos_updated}")
    print(f"📁 Fotos guardadas em: {UPLOADED_PHOTOS_DIR}/")
    print("=" * 80)


def list_real_photos():
    """
    Lista apenas as fotos reais (não placeholders)
    """
    print("\n" + "=" * 80)
    print("📸 FOTOS REAIS IMPORTADAS")
    print("=" * 80)
    print()
    
    # Carregar dados dos carros
    with open(CARJET_DATA_FILE, 'r', encoding='utf-8') as f:
        carjet_cars = json.load(f)
    
    # Filtrar fotos reais
    real_cars = [c for c in carjet_cars if not c['is_placeholder']]
    
    if real_cars:
        print(f"Encontradas {len(real_cars)} fotos reais:\n")
        for idx, car in enumerate(real_cars, 1):
            print(f"{idx}. {car['name']}")
            print(f"   Código: {car['car_code']}")
            print(f"   Categoria: {car['category']}")
            print(f"   URL: {car['photo_url']}")
            print()
    else:
        print("⚠️ Nenhuma foto real encontrada!")
    
    print("=" * 80)


if __name__ == '__main__':
    import_photos_to_database()
    list_real_photos()
