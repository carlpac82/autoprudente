#!/usr/bin/env python3
"""
Script para detectar campos de formulário em PDF
"""

from PyPDF2 import PdfReader
import sys

def detect_pdf_fields(pdf_path):
    """Detecta todos os campos de formulário no PDF"""
    try:
        reader = PdfReader(pdf_path)
        
        print(f"\n{'='*60}")
        print(f"📄 Analisando PDF: {pdf_path}")
        print(f"{'='*60}\n")
        
        # Verificar se tem campos de formulário
        if "/AcroForm" in reader.trailer["/Root"]:
            print("✅ PDF TEM CAMPOS DE FORMULÁRIO (AcroForm)!\n")
            
            fields = reader.get_fields()
            
            if fields:
                print(f"📋 Total de campos encontrados: {len(fields)}\n")
                print(f"{'Nome do Campo':<40} {'Tipo':<15} {'Valor Atual'}")
                print("-" * 80)
                
                for field_name, field_data in fields.items():
                    field_type = field_data.get('/FT', 'Unknown')
                    field_value = field_data.get('/V', '')
                    
                    # Converter tipo para legível
                    type_map = {
                        '/Tx': 'Text',
                        '/Btn': 'Button',
                        '/Ch': 'Choice',
                        '/Sig': 'Signature'
                    }
                    field_type_str = type_map.get(field_type, str(field_type))
                    
                    print(f"{field_name:<40} {field_type_str:<15} {field_value}")
                
                print("\n" + "="*60)
                print("✅ Use estes nomes de campos para preencher o PDF!")
                print("="*60 + "\n")
                
                # Gerar código exemplo
                print("📝 CÓDIGO EXEMPLO PARA PREENCHER:")
                print("-" * 60)
                print("from PyPDF2 import PdfReader, PdfWriter\n")
                print("reader = PdfReader('template.pdf')")
                print("writer = PdfWriter()\n")
                print("# Preencher campos:")
                for field_name in list(fields.keys())[:5]:  # Mostrar só 5 exemplos
                    print(f"writer.update_page_form_field_values(")
                    print(f"    writer.pages[0], {{'{field_name}': 'VALOR'}})")
                print("\nwith open('output.pdf', 'wb') as f:")
                print("    writer.write(f)")
                print("-" * 60 + "\n")
                
            else:
                print("⚠️ PDF tem AcroForm mas sem campos detectados\n")
        else:
            print("❌ PDF NÃO TEM CAMPOS DE FORMULÁRIO\n")
            print("💡 SOLUÇÕES:\n")
            print("1. Usar Adobe Acrobat para adicionar campos de formulário")
            print("2. Usar coordenadas (x, y) para posicionar texto")
            print("3. Enviar PDF com campos já criados\n")
            
            # Tentar extrair texto para ver estrutura
            print("📄 ESTRUTURA DO PDF:")
            print("-" * 60)
            for i, page in enumerate(reader.pages):
                print(f"\nPágina {i+1}:")
                print(f"  Tamanho: {page.mediabox.width} x {page.mediabox.height} pontos")
                text = page.extract_text()
                if text:
                    lines = text.split('\n')[:10]  # Primeiras 10 linhas
                    for line in lines:
                        if line.strip():
                            print(f"  {line[:80]}")
            print("-" * 60 + "\n")
            
    except Exception as e:
        print(f"❌ Erro ao analisar PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 detect_pdf_fields.py <caminho_do_pdf>")
        print("\nExemplo:")
        print("  python3 detect_pdf_fields.py 'DR 39:2025.pdf'")
        print("  python3 detect_pdf_fields.py damage_report_template.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    detect_pdf_fields(pdf_path)
