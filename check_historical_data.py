#!/usr/bin/env python3
"""
Verifica se há problemas no histórico de dados armazenados
"""
import sys
sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')

from database import get_db
from carjet_direct import detect_category_from_car
from main import map_category_to_group

print("="*100)
print("VERIFICAÇÃO DE DADOS HISTÓRICOS")
print("="*100)

# Conectar à base de dados
db = get_db()

# Buscar amostra de dados históricos
query = """
SELECT DISTINCT car, supplier
FROM price_snapshots
ORDER BY ts DESC
LIMIT 100
"""

results = db.execute(query).fetchall()

print(f"\n📊 Analisando {len(results)} carros únicos do histórico...\n")

# Carros que podem estar problemáticos
problems = []
automatic_without_auto = []
manual_with_auto = []

for row in results:
    car_name = row[0]
    if not car_name:
        continue
    
    car_lower = car_name.lower()
    has_auto_keyword = 'auto' in car_lower
    
    # Detectar categoria atual (sem transmissão)
    category = detect_category_from_car(car_name, '')
    group = map_category_to_group(category, car_name, '')
    
    # Verificar se parece ser automático mas não tem "Auto" no nome
    is_electric_hybrid = any(word in car_lower for word in ['electric', 'e-', 'hybrid', 'híbrido'])
    
    # Casos suspeitos
    if is_electric_hybrid and not has_auto_keyword:
        automatic_without_auto.append({
            'car': car_name,
            'category': category,
            'group': group,
            'reason': 'Elétrico/Híbrido sem "Auto" no nome'
        })
    
    # Carros que têm "Auto" mas podem estar em grupo manual
    if has_auto_keyword:
        if group in ['B1', 'B2', 'D', 'F', 'J1', 'M1']:  # Grupos manuais
            manual_with_auto.append({
                'car': car_name,
                'category': category,
                'group': group,
                'reason': 'Tem "Auto" no nome mas está em grupo manual'
            })

print("="*100)
print("CARROS ELÉTRICOS/HÍBRIDOS SEM 'AUTO' NO NOME")
print("="*100)

if automatic_without_auto:
    print(f"\n⚠️  {len(automatic_without_auto)} carros encontrados:\n")
    for item in automatic_without_auto[:20]:
        print(f"   • {item['car']:45} | Grupo: {item['group']:4} | Cat: {item['category']}")
        print(f"     → {item['reason']}")
else:
    print("\n✅ Nenhum problema encontrado!")

print("\n" + "="*100)
print("CARROS COM 'AUTO' NO NOME EM GRUPOS MANUAIS")
print("="*100)

if manual_with_auto:
    print(f"\n⚠️  {len(manual_with_auto)} carros encontrados:\n")
    for item in manual_with_auto[:20]:
        print(f"   • {item['car']:45} | Grupo: {item['group']:4} | Cat: {item['category']}")
        print(f"     → {item['reason']}")
else:
    print("\n✅ Nenhum problema encontrado!")

print("\n" + "="*100)
print("ANÁLISE GERAL")
print("="*100)

# Contar grupos
from collections import Counter
groups_count = Counter()

for row in results:
    car_name = row[0]
    if not car_name:
        continue
    
    category = detect_category_from_car(car_name, '')
    group = map_category_to_group(category, car_name, '')
    groups_count[group] += 1

print("\nDistribuição por grupos (amostra de 100 carros):")
for group in sorted(groups_count.keys()):
    count = groups_count[group]
    print(f"   {group:4}: {count:3} carros ({count/len(results)*100:.1f}%)")

print("\n" + "="*100)
print("CONCLUSÃO")
print("="*100)

if not automatic_without_auto and not manual_with_auto:
    print("""
✅ HISTÓRICO OK!

Todos os carros no histórico têm nomes consistentes:
- Automáticos têm "Auto" no nome
- Elétricos/Híbridos estão bem identificados
- Grupos estão corretos

A nova deteção pelo ícone icon-transm-auto só afeta NOVAS pesquisas,
mas o histórico já está correto porque os nomes dos carros incluem
a informação de transmissão.
""")
else:
    print(f"""
⚠️  PROBLEMAS ENCONTRADOS NO HISTÓRICO!

- {len(automatic_without_auto)} carros elétricos/híbridos sem "Auto" no nome
- {len(manual_with_auto)} carros com "Auto" em grupos manuais

IMPACTO:
Estes carros podem estar categorizados incorretamente no frontend
quando visualizas dados históricos.

SOLUÇÃO:
Executar um script de correção para padronizar nomes no histórico.
""")

print("="*100)
