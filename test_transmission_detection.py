#!/usr/bin/env python3
"""
Teste de detecção de transmissão por ícone
"""
import requests
import json
from datetime import datetime, timedelta

def test_transmission_detection():
    """Testa se a detecção de transmissão está funcionando"""
    
    # Configurar datas (7 dias a partir de amanhã)
    start_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    print("=" * 80)
    print("🔧 TESTE DE DETECÇÃO DE TRANSMISSÃO")
    print("=" * 80)
    print(f"📅 Data: {start_date} (7 dias)")
    print(f"📍 Local: Aeroporto de Faro")
    print()
    
    # Fazer requisição
    url = "http://localhost:8000/api/track-by-params"
    params = {
        "location": "Aeroporto de Faro",
        "start_date": start_date,
        "start_time": "15:00",
        "days": 7
    }
    
    print(f"🌐 Fazendo requisição: {url}")
    print(f"   Params: {params}")
    print()
    print("⏳ Aguardando scraping... (pode demorar 30-60s)")
    print()
    
    try:
        response = requests.post(url, json=params, timeout=120)
        
        if response.status_code != 200:
            print(f"❌ Erro HTTP {response.status_code}")
            print(response.text)
            return
        
        data = response.json()
        items = data.get('items', [])
        
        print("=" * 80)
        print(f"✅ SCRAPING CONCLUÍDO - {len(items)} carros encontrados")
        print("=" * 80)
        print()
        
        # Agrupar por transmissão
        automatic = []
        manual = []
        unknown = []
        
        for item in items:
            car_name = item.get('car', 'N/A')
            transmission = item.get('transmission', '')
            supplier = item.get('supplier', 'N/A')
            group = item.get('group', 'N/A')
            
            if transmission == 'Automatic':
                automatic.append((car_name, supplier, group))
            elif transmission == 'Manual':
                manual.append((car_name, supplier, group))
            else:
                unknown.append((car_name, supplier, group, transmission))
        
        # Mostrar resultados
        print(f"🔵 AUTOMÁTICOS: {len(automatic)} carros")
        print("-" * 80)
        for car, supplier, group in sorted(automatic):
            print(f"  ✓ {car:40} | {supplier:20} | Grupo {group}")
        print()
        
        print(f"🔴 MANUAIS: {len(manual)} carros")
        print("-" * 80)
        for car, supplier, group in sorted(manual):
            print(f"  ✗ {car:40} | {supplier:20} | Grupo {group}")
        print()
        
        if unknown:
            print(f"⚪ DESCONHECIDOS: {len(unknown)} carros")
            print("-" * 80)
            for car, supplier, group, trans in sorted(unknown):
                print(f"  ? {car:40} | {supplier:20} | Grupo {group} | Trans: '{trans}'")
            print()
        
        # Resumo
        print("=" * 80)
        print("📊 RESUMO:")
        print(f"   Total: {len(items)}")
        print(f"   Automáticos: {len(automatic)} ({len(automatic)*100//len(items) if items else 0}%)")
        print(f"   Manuais: {len(manual)} ({len(manual)*100//len(items) if items else 0}%)")
        print(f"   Desconhecidos: {len(unknown)} ({len(unknown)*100//len(items) if items else 0}%)")
        print("=" * 80)
        
        # Verificar casos específicos
        print()
        print("🔍 VERIFICANDO CASOS ESPECÍFICOS:")
        print("-" * 80)
        
        # VW Sharan (deve ser MANUAL)
        sharan = [item for item in items if 'sharan' in item.get('car', '').lower()]
        if sharan:
            for s in sharan:
                trans = s.get('transmission', 'N/A')
                supplier = s.get('supplier', 'N/A')
                expected = "Manual" if supplier == "Autorent" else "?"
                status = "✅" if trans == expected else "❌"
                print(f"{status} VW Sharan ({supplier}): {trans} (esperado: {expected})")
        else:
            print("  ℹ️  VW Sharan não encontrado")
        
        # VW Up (pode aparecer manual E automático de fornecedores diferentes)
        vw_up = [item for item in items if 'volkswagen up' in item.get('car', '').lower() or 'vw up' in item.get('car', '').lower()]
        if vw_up:
            print()
            print(f"  VW Up encontrado {len(vw_up)} vez(es):")
            for up in vw_up:
                trans = up.get('transmission', 'N/A')
                supplier = up.get('supplier', 'N/A')
                group = up.get('group', 'N/A')
                print(f"    - {supplier:20} | {trans:10} | Grupo {group}")
        else:
            print("  ℹ️  VW Up não encontrado")
        
        print("=" * 80)
        
    except requests.exceptions.Timeout:
        print("❌ Timeout - Servidor demorou muito tempo")
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - Servidor não está rodando?")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_transmission_detection()
