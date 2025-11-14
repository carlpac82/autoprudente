#!/usr/bin/env python3
"""
Debug do Filtro de Transmissão Automática
Examina o HTML retornado pelo CarJet
"""

import sys
import os
import re
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))

from main import try_direct_carjet

def test_automatic_filter_debug():
    print("=" * 80)
    print("DEBUG: Filtro de Transmissão Automática - CarJet")
    print("=" * 80)
    print()
    
    # Configurar pesquisa
    location = "Faro Aeroporto (FAO)"
    start_dt = datetime.now() + timedelta(days=7)
    end_dt = start_dt + timedelta(days=5)
    
    print(f"📍 Local: {location}")
    print(f"📅 Data Pickup: {start_dt.strftime('%d/%m/%Y %H:%M')}")
    print(f"📅 Data Dropoff: {end_dt.strftime('%d/%m/%Y %H:%M')}")
    print()
    
    # Fazer request ao CarJet
    print("🔄 Fazendo request ao CarJet com filtro automático...")
    html = try_direct_carjet(location, start_dt, end_dt, lang="pt", currency="EUR")
    
    if not html:
        print("❌ ERRO: Não recebeu HTML do CarJet")
        return
    
    print(f"✅ HTML recebido: {len(html)} caracteres")
    print()
    
    # Salvar HTML para análise
    filename = "carjet_automatic_filter_response.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"💾 HTML salvo em: {filename}")
    print()
    
    # Analisar conteúdo do HTML
    print("=" * 80)
    print("ANÁLISE DO HTML")
    print("=" * 80)
    print()
    
    # Verificar tipo de página
    if 'hrental_pagetype' in html:
        match = re.search(r'hrental_pagetype["\s:]+([^"]+)', html)
        if match:
            pagetype = match.group(1)
            print(f"📄 Tipo de página: {pagetype}")
    
    # Verificar se tem filtro aplicado
    if 'frmTrans' in html:
        print("✅ Campo frmTrans encontrado no HTML")
        # Procurar valor do filtro
        matches = re.findall(r'frmTrans["\s:=]+["\']?(\w+)', html)
        if matches:
            print(f"   Valores encontrados: {matches}")
    else:
        print("⚠️  Campo frmTrans NÃO encontrado no HTML")
    
    # Verificar se tem checkbox de transmissão automática
    if 'chkTransAu' in html or 'Automatic' in html or 'Automático' in html:
        print("✅ Referências a transmissão automática encontradas")
    
    # Contar artigos/cards de carros
    article_count = html.count('<article')
    print(f"\n📊 Artigos/cards encontrados: {article_count}")
    
    # Procurar mensagens de erro ou "sem resultados"
    error_patterns = [
        r'No\s+results',
        r'Sem\s+resultados',
        r'Nenhum\s+carro',
        r'war=',
        r'error',
    ]
    
    print("\n🔍 Verificando mensagens de erro:")
    for pattern in error_patterns:
        if re.search(pattern, html, re.IGNORECASE):
            print(f"   ⚠️  Encontrado padrão: {pattern}")
    
    # Procurar por "list" ou "carList"
    if '/do/list/' in html:
        print("\n✅ URL de lista encontrada no HTML")
    
    # Verificar se tem dados de carros
    car_indicators = [
        'data-price',
        'data-grupo',
        'data-prv',
        'car_code',
        'vehicle',
    ]
    
    print("\n🚗 Indicadores de carros no HTML:")
    for indicator in car_indicators:
        count = html.count(indicator)
        if count > 0:
            print(f"   ✅ {indicator}: {count} ocorrências")
    
    # Extrair snippet do HTML (primeiros e últimos caracteres)
    print("\n" + "=" * 80)
    print("SNIPPET DO HTML")
    print("=" * 80)
    print("\n📝 Primeiros 500 caracteres:")
    print("-" * 80)
    print(html[:500])
    print("-" * 80)
    
    print("\n📝 Últimos 500 caracteres:")
    print("-" * 80)
    print(html[-500:])
    print("-" * 80)
    
    # Procurar tags específicas de filtro no HTML
    print("\n" + "=" * 80)
    print("VERIFICAÇÃO DE FILTROS NO HTML")
    print("=" * 80)
    
    # Procurar inputs de filtro
    filter_inputs = re.findall(r'<input[^>]*name=["\']frm\w+["\'][^>]*>', html)
    if filter_inputs:
        print(f"\n✅ Encontrados {len(filter_inputs)} inputs de filtro:")
        for inp in filter_inputs[:5]:  # Mostrar apenas os primeiros 5
            print(f"   {inp[:100]}...")
    
    # Verificar se o filtro está checked
    if re.search(r'chkTransAu[^>]*checked', html):
        print("\n✅ Checkbox de transmissão automática está CHECKED")
    elif 'chkTransAu' in html:
        print("\n⚠️  Checkbox de transmissão automática existe mas NÃO está checked")
    else:
        print("\n❌ Checkbox de transmissão automática NÃO encontrado")


if __name__ == "__main__":
    try:
        test_automatic_filter_debug()
    except Exception as e:
        print()
        print("=" * 80)
        print("❌ ERRO DURANTE O DEBUG")
        print("=" * 80)
        print()
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
