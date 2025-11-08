#!/usr/bin/env python3
"""
Adicionar coordenadas que faltam no damage_report_coordinates.json
"""

import json

# Ler coordenadas existentes
with open('damage_report_coordinates.json', 'r') as f:
    coords = json.load(f)

print("="*60)
print("📍 COORDENADAS ATUAIS:")
print("="*60)
for field in sorted(coords.keys()):
    print(f"  ✅ {field}")

print("\n" + "="*60)
print("❌ CAMPOS QUE FALTAM:")
print("="*60)

missing_fields = {
    'date': {
        'description': 'Data do relatório (campo principal)',
        'page': 1,
        'x': 400,  # Posição estimada - PRECISA AJUSTAR
        'y': 100,
        'width': 100,
        'height': 15
    },
    'inspection_date': {
        'description': 'Data de inspeção (alias)',
        'page': 1,
        'x': 400,  # Posição estimada - PRECISA AJUSTAR
        'y': 100,
        'width': 100,
        'height': 15
    },
    'vehicle_diagram': {
        'description': 'Croqui do veículo (imagem base)',
        'page': 1,
        'x': 50,   # Posição estimada - PRECISA AJUSTAR
        'y': 350,
        'width': 500,
        'height': 350
    }
}

for field, info in missing_fields.items():
    print(f"\n❌ {field}")
    print(f"   Descrição: {info['description']}")
    print(f"   Coordenadas estimadas: x={info['x']}, y={info['y']}, w={info['width']}, h={info['height']}")

print("\n" + "="*60)
print("⚠️  SOLUÇÃO:")
print("="*60)
print("""
1. OPÇÃO MANUAL (Recomendado):
   - Abrir 'Damage Report.pdf' no Adobe Acrobat
   - Medir coordenadas exatas dos campos que faltam
   - Adicionar manualmente ao damage_report_coordinates.json

2. OPÇÃO AUTOMÁTICA (Aproximado):
   - Executar: python3 fix_missing_coordinates.py --add
   - Usa coordenadas estimadas (pode não ficar perfeito)
   - Precisa ajustar manualmente depois

3. OPÇÃO VISUAL (Mais fácil):
   - Usar map_pdf_coordinates.py para mapear visualmente
   - python3 map_pdf_coordinates.py
   - Clique nos locais corretos do PDF
""")

print("\n📄 COORDENADAS PRECISAS:")
print("="*60)
print("""
Para cada campo, preciso saber:
- x: Distância da esquerda (em pontos)
- y: Distância de BAIXO (não do topo!)
- width: Largura da caixa
- height: Altura da caixa

NOTA: PDFs usam coordenadas com origem no canto INFERIOR ESQUERDO!
      (0,0) = canto inferior esquerdo
      (595,842) = canto superior direito (A4)
""")

print("\n🔧 PRÓXIMO PASSO:")
print("="*60)
print("""
Opções:
A) Tens o PDF original em formato editável?
   -> Posso extrair as coordenadas automaticamente

B) Queres usar coordenadas aproximadas primeiro?
   -> Adiciono agora com estimativa

C) Queres mapear visualmente?
   -> Usa o script map_pdf_coordinates.py
""")
