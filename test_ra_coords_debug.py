#!/usr/bin/env python3
"""
Script para diagnosticar as coordenadas mapeadas do Rental Agreement
e ver exatamente o que cada uma está a extrair do PDF.
"""

import sqlite3
import fitz  # PyMuPDF
import sys

# Caminho para o PDF de teste (ajustar se necessário)
PDF_PATH = "06424-09.pdf"  # Ajustar para o caminho correto do seu PDF

def main():
    # Conectar à BD
    conn = sqlite3.connect('data.db')
    cursor = conn.execute("""
        SELECT field_id, x, y, width, height, page 
        FROM rental_agreement_coordinates 
        ORDER BY field_id
    """)
    coords_rows = cursor.fetchall()
    conn.close()
    
    print(f"\n{'='*80}")
    print(f"🔍 DIAGNÓSTICO DE COORDENADAS DO RENTAL AGREEMENT")
    print(f"{'='*80}\n")
    print(f"📊 Total de campos mapeados: {len(coords_rows)}")
    
    if not coords_rows:
        print("❌ Nenhuma coordenada encontrada na base de dados!")
        return
    
    # Verificar se PDF existe
    try:
        pdf_doc = fitz.open(PDF_PATH)
    except Exception as e:
        print(f"\n❌ ERRO ao abrir PDF '{PDF_PATH}': {e}")
        print("\n💡 Coloque o PDF na mesma pasta que este script ou ajuste PDF_PATH")
        return
    
    print(f"✅ PDF aberto: {PDF_PATH} ({len(pdf_doc)} páginas)\n")
    
    # Testar cada coordenada
    for row in coords_rows:
        field_id, x, y, width, height, page = row
        
        print(f"\n{'─'*80}")
        print(f"📍 Campo: {field_id}")
        print(f"   Coordenadas: x={x:.1f}, y={y:.1f}, width={width:.1f}, height={height:.1f}, page={page}")
        
        try:
            page_num = int(page) - 1 if page else 0
            
            if page_num >= len(pdf_doc):
                print(f"   ⚠️  Página {page} não existe no PDF!")
                continue
            
            pdf_page = pdf_doc[page_num]
            page_height = pdf_page.rect.height
            
            # Testar 4 métodos de coordenadas
            methods = {
                "DIRETO": (x, y, x + width, y + height),
                "INVERTIDO_Y": (x, page_height - y - height, x + width, page_height - y),
                "ESCALA_2": (x/2, y/2, (x + width)/2, (y + height)/2),
                "ESCALA_INV": (x/2, page_height - y/2 - height/2, (x + width)/2, page_height - y/2),
            }
            
            for method_name, coords in methods.items():
                rect = fitz.Rect(*coords)
                text = pdf_page.get_text("text", clip=rect).strip()
                text_clean = ' '.join(text.split()) if text else ""
                
                if text_clean:
                    print(f"   {method_name:15} → '{text_clean[:60]}'")
                else:
                    print(f"   {method_name:15} → (vazio)")
        
        except Exception as e:
            print(f"   ❌ ERRO: {e}")
    
    pdf_doc.close()
    
    print(f"\n{'='*80}")
    print("✅ Diagnóstico concluído!")
    print(f"{'='*80}\n")
    
    print("💡 INTERPRETAÇÃO:")
    print("   • Se DIRETO mostra o texto correto → coordenadas OK")
    print("   • Se INVERTIDO_Y mostra o correto → PDF usa coordenadas invertidas")
    print("   • Se todos vazios → coordenadas estão fora do conteúdo")
    print("   • Se texto errado em todos → caixa desenhada no lugar errado!\n")

if __name__ == "__main__":
    main()
