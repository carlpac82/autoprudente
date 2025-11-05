#!/usr/bin/env python3
"""
Sistema simples para mapear coordenadas do PDF
Mostra o PDF e tu dizes as coordenadas manualmente
"""

from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
import json

def create_test_pdf_with_grid():
    """Criar PDF de teste com grid de coordenadas"""
    print("\n" + "="*70)
    print("📐 CRIANDO PDF COM GRID DE COORDENADAS")
    print("="*70 + "\n")
    
    # Ler PDF original
    reader = PdfReader("Damage Report.pdf")
    page = reader.pages[0]
    
    # Criar novo PDF com grid
    c = canvas.Canvas("damage_report_with_grid.pdf", pagesize=A4)
    width, height = A4
    
    print(f"📄 Tamanho do PDF: {width:.1f} x {height:.1f} pontos")
    print(f"📄 Em cm: {width/cm:.1f} x {height/cm:.1f} cm\n")
    
    # Desenhar grid
    c.setStrokeColor(colors.lightgrey)
    c.setLineWidth(0.5)
    
    # Linhas verticais a cada 1cm
    for x in range(0, int(width/cm) + 1):
        x_pos = x * cm
        c.line(x_pos, 0, x_pos, height)
        if x % 2 == 0:  # Números a cada 2cm
            c.setFont("Helvetica", 6)
            c.setFillColor(colors.grey)
            c.drawString(x_pos + 2, height - 10, f"{x}")
            c.drawString(x_pos + 2, 5, f"{x}")
    
    # Linhas horizontais a cada 1cm
    for y in range(0, int(height/cm) + 1):
        y_pos = y * cm
        c.line(0, y_pos, width, y_pos)
        if y % 2 == 0:  # Números a cada 2cm
            c.setFont("Helvetica", 6)
            c.setFillColor(colors.grey)
            c.drawString(5, y_pos + 2, f"{y}")
            c.drawString(width - 15, y_pos + 2, f"{y}")
    
    # Adicionar legenda
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.red)
    c.drawString(2*cm, height - 1*cm, "GRID DE COORDENADAS (em cm)")
    c.setFont("Helvetica", 8)
    c.drawString(2*cm, height - 1.5*cm, "Use este PDF para identificar as posições dos campos")
    
    c.save()
    
    print("✅ PDF com grid criado: damage_report_with_grid.pdf")
    print("\n📋 INSTRUÇÕES:")
    print("1. Abre o ficheiro 'damage_report_with_grid.pdf'")
    print("2. Abre também o 'Damage Report.pdf' original")
    print("3. Compara os dois e anota as coordenadas de cada campo")
    print("4. Volta aqui e insere as coordenadas\n")
    print("="*70 + "\n")

def manual_mapping():
    """Mapear campos manualmente"""
    print("\n" + "="*70)
    print("📝 MAPEAMENTO MANUAL DE CAMPOS")
    print("="*70 + "\n")
    
    fields = [
        ('dr_number', 'DR Nº (topo direita)'),
        ('date', 'Data (topo direita)'),
        ('client_name', 'Nome Completo do Cliente'),
        ('client_email', 'Email do Cliente'),
        ('client_phone', 'Telefone do Cliente'),
        ('client_address', 'Morada do Cliente'),
        ('client_postal_code', 'Código Postal'),
        ('client_city', 'Cidade'),
        ('client_country', 'País'),
        ('vehicle_plate', 'Matrícula'),
        ('vehicle_brand', 'Marca'),
        ('vehicle_model', 'Modelo'),
        ('pickup_date', 'Data de Levantamento'),
        ('pickup_time', 'Hora de Levantamento'),
        ('pickup_location', 'Local de Levantamento'),
        ('return_date', 'Data de Devolução'),
        ('return_time', 'Hora de Devolução'),
        ('return_location', 'Local de Devolução'),
        ('issued_by', 'Feito por / Issued by'),
    ]
    
    coordinates = {}
    
    print("Para cada campo, insere as coordenadas em cm (X Y)")
    print("Exemplo: 15.5 25.0")
    print("Ou deixa vazio para pular\n")
    
    for field_id, field_name in fields:
        while True:
            response = input(f"\n📍 {field_name}\n   Coordenadas (X Y em cm) ou Enter para pular: ").strip()
            
            if not response:
                print("   ⏭️ Campo pulado")
                break
            
            try:
                parts = response.split()
                if len(parts) != 2:
                    print("   ❌ Formato inválido! Use: X Y (exemplo: 15.5 25.0)")
                    continue
                
                x_cm = float(parts[0])
                y_cm = float(parts[1])
                
                # Converter cm para pontos
                x_pt = x_cm * cm
                y_pt = y_cm * cm
                
                coordinates[field_id] = (x_pt, y_pt)
                print(f"   ✅ Guardado: ({x_cm} cm, {y_cm} cm) = ({x_pt:.1f} pt, {y_pt:.1f} pt)")
                break
            except ValueError:
                print("   ❌ Valores inválidos! Use números (exemplo: 15.5 25.0)")
    
    if coordinates:
        # Guardar em JSON
        with open('damage_report_coordinates.json', 'w') as f:
            json.dump(coordinates, f, indent=2)
        
        # Guardar código Python
        with open('damage_report_coordinates.py', 'w') as f:
            f.write("# Coordenadas dos campos do Damage Report PDF\n")
            f.write("# Formato: (X em pontos, Y em pontos)\n")
            f.write("# 1 cm = 28.35 pontos\n\n")
            f.write("DAMAGE_REPORT_FIELDS = {\n")
            for field_id, (x, y) in coordinates.items():
                f.write(f"    '{field_id}': ({x:.1f}, {y:.1f}),  # {x/cm:.1f} cm, {y/cm:.1f} cm\n")
            f.write("}\n")
        
        print("\n" + "="*70)
        print(f"✅ {len(coordinates)} CAMPOS GUARDADOS!")
        print("="*70)
        print("\nFicheiros criados:")
        print("• damage_report_coordinates.json")
        print("• damage_report_coordinates.py")
        print("\n" + "="*70 + "\n")
    else:
        print("\n⚠️ Nenhum campo foi mapeado!")

if __name__ == "__main__":
    print("\n🎯 SISTEMA DE MAPEAMENTO DE CAMPOS DO DAMAGE REPORT\n")
    
    # Criar PDF com grid
    create_test_pdf_with_grid()
    
    # Perguntar se quer continuar
    response = input("Queres mapear os campos agora? (s/n): ").strip().lower()
    
    if response == 's':
        manual_mapping()
    else:
        print("\n📋 Quando estiveres pronto:")
        print("   python3 map_fields_simple.py")
        print("\nE escolhe 's' para começar o mapeamento!\n")
