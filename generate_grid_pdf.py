#!/usr/bin/env python3
"""
Gerar PDF com grid sobreposto ao Damage Report original (2 páginas)
"""

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from io import BytesIO

def create_grid_overlay():
    """Criar overlay com grid"""
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)
    width, height = A4
    
    # Grid semi-transparente
    c.setStrokeColor(colors.Color(0, 0, 1, alpha=0.3))  # Azul transparente
    c.setLineWidth(0.5)
    
    # Linhas verticais a cada 1cm
    for x in range(0, int(width/cm) + 1):
        x_pos = x * cm
        c.line(x_pos, 0, x_pos, height)
        if x % 2 == 0:
            c.setFont('Helvetica', 7)
            c.setFillColor(colors.Color(0, 0, 1, alpha=0.7))
            c.drawString(x_pos + 2, height - 12, str(x))
            c.drawString(x_pos + 2, 8, str(x))
    
    # Linhas horizontais a cada 1cm
    for y in range(0, int(height/cm) + 1):
        y_pos = y * cm
        c.line(0, y_pos, width, y_pos)
        if y % 2 == 0:
            c.setFont('Helvetica', 7)
            c.setFillColor(colors.Color(0, 0, 1, alpha=0.7))
            c.drawString(8, y_pos + 2, str(y))
            c.drawString(width - 18, y_pos + 2, str(y))
    
    # Legenda
    c.setFont('Helvetica-Bold', 11)
    c.setFillColor(colors.Color(1, 0, 0, alpha=0.9))
    c.drawString(2*cm, height - 0.8*cm, 'GRID DE COORDENADAS (em cm)')
    c.setFont('Helvetica', 9)
    c.drawString(2*cm, height - 1.3*cm, 'Clica nas posições dos campos')
    
    c.save()
    packet.seek(0)
    return packet

# Ler PDF original
print("📄 Lendo Damage Report.pdf...")
reader = PdfReader('Damage Report.pdf')
num_pages = len(reader.pages)
print(f"   Páginas encontradas: {num_pages}")

# Criar PDF de saída
writer = PdfWriter()

# Processar cada página
for page_num in range(num_pages):
    print(f"\n📐 Processando página {page_num + 1}...")
    
    # Obter página original
    original_page = reader.pages[page_num]
    
    # Criar overlay com grid
    grid_overlay = create_grid_overlay()
    overlay_pdf = PdfReader(grid_overlay)
    overlay_page = overlay_pdf.pages[0]
    
    # Merge
    original_page.merge_page(overlay_page)
    
    # Adicionar ao writer
    writer.add_page(original_page)
    print(f"   ✅ Página {page_num + 1} processada")

# Salvar
output_path = 'static/damage_report_with_grid.pdf'
with open(output_path, 'wb') as f:
    writer.write(f)

print(f"\n✅ PDF com grid criado: {output_path}")
print(f"📄 Total de páginas: {num_pages}")
