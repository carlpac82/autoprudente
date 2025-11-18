#!/usr/bin/env python3
"""
Teste completo de todos os grupos automáticos - Pesquisa 7 dias Faro
"""

import sys
import json
from datetime import datetime, timedelta
from carjet_requests import scrape_carjet_requests

# Pesquisa 7 dias no Aeroporto de Faro
location = "Faro"
start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=7)

print("=" * 80)
print(f"TESTE: Pesquisa 7 dias - Aeroporto de Faro")
print(f"Datas: {start_dt.strftime('%d/%m/%Y')} - {end_dt.strftime('%d/%m/%Y')}")
print("=" * 80)

try:
    results = scrape_carjet_requests(location, start_dt, end_dt)
    
    if not results:
        print("❌ Nenhum resultado retornado!")
        sys.exit(1)
    
    print(f"\n✅ Total de carros encontrados: {len(results)}")
    
    # Agrupar por grupo e filtrar automáticos
    grupos = {}
    automaticos = []
    manuais = []
    
    for car in results:
        trans = car.get('transmission', '')
        group = car.get('group', '')
        category = car.get('category', '')
        
        if 'auto' in trans.lower() or 'automatic' in trans.lower():
            automaticos.append(car)
            if group not in grupos:
                grupos[group] = []
            grupos[group].append(car)
        else:
            manuais.append(car)
    
    print(f"\n📊 RESUMO:")
    print(f"  Automáticos: {len(automaticos)}")
    print(f"  Manuais: {len(manuais)}")
    print(f"  Grupos automáticos encontrados: {len(grupos)}")
    
    # Verificar grupos esperados de automáticos
    grupos_esperados = {
        'E1': 'MINI Auto',
        'E2': 'ECONOMY Auto',
        'K1': 'Crossover Auto',
        'L1': 'SUV Auto',
        'L2': 'Station Wagon Auto',
        'M2': '7 Lugares Auto'
    }
    
    print("\n" + "=" * 80)
    print("VERIFICAÇÃO DE GRUPOS AUTOMÁTICOS")
    print("=" * 80)
    
    for group_code, group_name in sorted(grupos_esperados.items()):
        if group_code in grupos:
            count = len(grupos[group_code])
            status = "✅"
            print(f"\n{status} {group_code} - {group_name}: {count} carros")
            
            # Mostrar primeiros 3 exemplos
            for i, car in enumerate(grupos[group_code][:3]):
                price = car.get('price', 'N/A')
                supplier = car.get('supplier', 'N/A')
                print(f"    {i+1}. {car.get('car', 'N/A'):30} | €{price:>8} | {supplier}")
        else:
            print(f"\n⚠️  {group_code} - {group_name}: NÃO ENCONTRADO")
    
    # Verificar se há automáticos em grupos errados (B1, B2, D, F, J1, J2, M1)
    grupos_manuais = ['B1', 'B2', 'D', 'F', 'J1', 'J2', 'M1']
    automaticos_errados = []
    
    print("\n" + "=" * 80)
    print("VERIFICAÇÃO DE ERROS (Automáticos em grupos de manuais)")
    print("=" * 80)
    
    for car in automaticos:
        group = car.get('group', '')
        if group in grupos_manuais:
            automaticos_errados.append(car)
    
    if automaticos_errados:
        print(f"\n❌ {len(automaticos_errados)} AUTOMÁTICOS EM GRUPOS ERRADOS:")
        for car in automaticos_errados[:10]:  # Mostrar primeiros 10
            print(f"  {car.get('car', 'N/A'):30} | Grupo: {car.get('group', 'N/A')} | Cat: {car.get('category', 'N/A')}")
    else:
        print("\n✅ Nenhum automático em grupo errado!")
    
    # Estatísticas detalhadas por grupo
    print("\n" + "=" * 80)
    print("ESTATÍSTICAS DETALHADAS")
    print("=" * 80)
    
    for group_code in sorted(grupos.keys()):
        carros = grupos[group_code]
        # Limpar preços (remover €, espaços, etc)
        precos = []
        for c in carros:
            price_str = str(c.get('price', '0'))
            price_clean = price_str.replace('€', '').replace(' ', '').replace(',', '.').strip()
            try:
                precos.append(float(price_clean))
            except:
                pass
        
        if precos:
            print(f"\n{group_code}:")
            print(f"  Carros: {len(carros)}")
            print(f"  Preço min: €{min(precos):.2f}")
            print(f"  Preço max: €{max(precos):.2f}")
            print(f"  Preço médio: €{sum(precos)/len(precos):.2f}")
    
    # Salvar resultados completos em JSON
    output_file = "test_faro_7days_auto_groups.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'location': location,
            'start': start_dt.isoformat(),
            'end': end_dt.isoformat(),
            'days': 7,
            'total_cars': len(results),
            'automaticos': len(automaticos),
            'manuais': len(manuais),
            'grupos': {k: len(v) for k, v in grupos.items()},
            'automaticos_errados': len(automaticos_errados),
            'results': results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n\n💾 Resultados salvos em: {output_file}")
    
    print("\n" + "=" * 80)
    if not automaticos_errados and len(grupos) >= 4:
        print("✅ TODOS OS TESTES PASSARAM!")
    else:
        print("⚠️  ALGUNS PROBLEMAS ENCONTRADOS")
    print("=" * 80)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
