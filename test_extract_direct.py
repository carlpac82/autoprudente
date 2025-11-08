#!/usr/bin/env python3
"""
Testar extração diretamente (sem HTTP, sem auth)
"""
import sys
import sqlite3
from io import BytesIO

# Criar PDF de teste
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

print("\n" + "="*80)
print("🧪 TESTE DIRETO DE EXTRAÇÃO (SEM HTTP)")
print("="*80)

# Verificar coordenadas na BD
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM rental_agreement_coordinates")
count = cursor.fetchone()[0]
print(f"\n📊 Coordenadas na BD: {count}")
conn.close()

if count == 0:
    print("❌ Nenhuma coordenada encontrada!")
    sys.exit(1)

# Criar PDF
pdf_buffer = BytesIO()
c = canvas.Canvas(pdf_buffer, pagesize=A4)
width, height = A4

# Escrever dados
c.drawString(14, height - 97, "06424-09")
c.drawString(12, height - 130, "EIKE BERENS")  
c.drawString(293, height - 96.5, "RUA EXEMPLO 123")
c.drawString(442, height - 96.5, "FIAT / 500")
c.drawString(292, height - 182.5, "AB-12-CD")
c.drawString(442.5, height - 182.5, "10:30")
c.drawString(442.5, height - 210, "AUTO PRUDENTE")
c.drawString(292.6569, height - 237, "06-11-2025")
c.drawString(442, height - 237, "3/4")
c.drawString(13.5, height - 271, "DE")
c.drawString(13.5, height - 351.5, "8000-000")
c.drawString(110, height - 351.5, "+351 912345678")

c.save()
pdf_buffer.seek(0)
pdf_contents = pdf_buffer.read()

print(f"✅ PDF criado ({len(pdf_contents)} bytes)")

# Importar função de extração
print("\n🔍 Importando função de extração...")

# Simular extração básica com PyMuPDF
try:
    import fitz
    import sqlite3
    
    print("\n" + "="*80)
    print("🚨 EXTRAÇÃO POR COORDENADAS - INÍCIO")
    print("="*80)
    
    # Abrir PDF
    pdf_doc = fitz.open(stream=pdf_contents, filetype="pdf")
    print(f"📄 PDF: {len(pdf_doc)} página(s)")
    
    # Carregar coordenadas
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT field_id, x, y, width, height, page FROM rental_agreement_coordinates")
    coords_rows = cursor.fetchall()
    conn.close()
    
    print(f"🔍 Coordenadas encontradas: {len(coords_rows)}")
    print(f"✅ USANDO {len(coords_rows)} COORDENADAS MAPEADAS!")
    
    fields_extracted = {}
    
    for row in coords_rows:
        field_id, x, y, width, height, page = row
        
        print(f"\n{'='*60}")
        print(f"📍 TESTANDO CAMPO: {field_id}")
        print(f"{'='*60}")
        
        page_num = int(page) - 1 if page else 0
        
        if page_num < len(pdf_doc):
            pdf_page = pdf_doc[page_num]
            page_height = pdf_page.rect.height
            page_width = pdf_page.rect.width
            
            print(f"   📄 PDF: {page_width:.1f}x{page_height:.1f}")
            print(f"   📐 Coords DB: x={x:.1f}, y={y:.1f}, w={width:.1f}, h={height:.1f}")
            
            # Testar múltiplos métodos
            scale_factor = 2.0
            
            methods = {
                "DIRETO": (x, y, width, height),
                "INVERTIDO": (x, page_height - y, width, height),
                "INV+HEIGHT": (x, page_height - y - height, width, height),
                "ESCALA_DIRETO": (x/scale_factor, y/scale_factor, width/scale_factor, height/scale_factor),
                "ESCALA_INV": (x/scale_factor, page_height - y/scale_factor, width/scale_factor, height/scale_factor),
                "ESCALA_INV+H": (x/scale_factor, page_height - y/scale_factor - height/scale_factor, width/scale_factor, height/scale_factor),
            }
            
            best_text = ""
            best_method = "DIRETO"
            
            for method_name, (test_x, test_y, test_w, test_h) in methods.items():
                rect_test = fitz.Rect(test_x, test_y, test_x + test_w, test_y + test_h)
                text_test = pdf_page.get_text("text", clip=rect_test).strip()
                text_clean = ' '.join(text_test.split()) if text_test else ""
                
                print(f"   🧪 {method_name}: ({test_x:.1f},{test_y:.1f}) → '{text_clean[:40]}'")
                
                if len(text_clean) > len(best_text) and any(c.isalpha() or c.isdigit() for c in text_clean):
                    best_text = text_clean
                    best_method = method_name
            
            print(f"   ✅ MELHOR: {best_method} → '{best_text[:60]}'")
            
            if best_text:
                fields_extracted[field_id] = best_text
    
    pdf_doc.close()
    
    print(f"\n{'='*80}")
    print(f"📊 RESULTADO FINAL")
    print(f"{'='*80}")
    print(f"✅ Extraídos {len(fields_extracted)} campos:")
    for field, value in fields_extracted.items():
        print(f"   • {field}: {value}")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
