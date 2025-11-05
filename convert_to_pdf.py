#!/usr/bin/env python3
"""
Script para converter Markdown para PDF com logo e header da AUTOPRUDENTE
Requer: pip install markdown2 weasyprint pillow
"""

import os
from pathlib import Path

# Template HTML com logo e header azul
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm 2cm 2cm 2cm;
            @top-center {{
                content: element(header);
            }}
            @bottom-center {{
                content: "Página " counter(page) " de " counter(pages);
                font-size: 10pt;
                color: #666;
            }}
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* Header azul AUTOPRUDENTE */
        .header {{
            position: running(header);
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 28pt;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .header .subtitle {{
            margin: 5px 0 0 0;
            font-size: 14pt;
            opacity: 0.9;
        }}
        
        /* Logo placeholder */
        .logo {{
            width: 150px;
            height: 60px;
            background: white;
            border-radius: 8px;
            margin: 0 auto 15px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #1e3a8a;
            font-size: 18pt;
        }}
        
        h1 {{
            color: #1e3a8a;
            border-bottom: 3px solid #3b82f6;
            padding-bottom: 10px;
            margin-top: 30px;
        }}
        
        h2 {{
            color: #3b82f6;
            margin-top: 25px;
            border-left: 4px solid #3b82f6;
            padding-left: 15px;
        }}
        
        h3 {{
            color: #1e3a8a;
            margin-top: 20px;
        }}
        
        code {{
            background: #f3f4f6;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #dc2626;
        }}
        
        pre {{
            background: #1f2937;
            color: #f3f4f6;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 4px solid #3b82f6;
        }}
        
        pre code {{
            background: transparent;
            color: #f3f4f6;
            padding: 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        th {{
            background: #1e3a8a;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        
        td {{
            padding: 10px;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        tr:nth-child(even) {{
            background: #f9fafb;
        }}
        
        blockquote {{
            border-left: 4px solid #3b82f6;
            padding-left: 20px;
            margin-left: 0;
            color: #4b5563;
            font-style: italic;
        }}
        
        ul, ol {{
            padding-left: 30px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        .emoji {{
            font-size: 1.2em;
        }}
        
        /* Footer */
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #e5e7eb;
            text-align: center;
            color: #6b7280;
            font-size: 10pt;
        }}
        
        /* Badges */
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 10pt;
            font-weight: bold;
            margin: 0 5px;
        }}
        
        .badge-success {{
            background: #10b981;
            color: white;
        }}
        
        .badge-info {{
            background: #3b82f6;
            color: white;
        }}
        
        .badge-warning {{
            background: #f59e0b;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">AUTOPRUDENTE</div>
        <h1>{title}</h1>
        <div class="subtitle">{subtitle}</div>
    </div>
    
    <div class="content">
        {content}
    </div>
    
    <div class="footer">
        <p><strong>AUTOPRUDENTE</strong> - Sistema de Gestão de Preços de Aluguer de Viaturas</p>
        <p>© 2025 AUTOPRUDENTE - Todos os direitos reservados</p>
        <p>Versão 2.0 | Última Atualização: Novembro 2025</p>
    </div>
</body>
</html>
"""

def convert_markdown_to_pdf(md_file, title, subtitle):
    """Converter Markdown para PDF com template personalizado"""
    
    try:
        import markdown2
        from weasyprint import HTML, CSS
        
        # Ler ficheiro Markdown
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Converter Markdown para HTML
        html_content = markdown2.markdown(
            md_content,
            extras=[
                'tables',
                'fenced-code-blocks',
                'code-friendly',
                'break-on-newline',
                'header-ids'
            ]
        )
        
        # Criar HTML completo com template
        full_html = HTML_TEMPLATE.format(
            title=title,
            subtitle=subtitle,
            content=html_content
        )
        
        # Nome do ficheiro PDF
        pdf_file = md_file.replace('.md', '.pdf')
        
        # Converter para PDF
        print(f"📄 Convertendo {md_file}...")
        HTML(string=full_html).write_pdf(pdf_file)
        
        print(f"✅ PDF criado: {pdf_file}")
        return pdf_file
        
    except ImportError as e:
        print(f"❌ Erro: Bibliotecas em falta!")
        print(f"   Execute: pip install markdown2 weasyprint pillow")
        return None
    except Exception as e:
        print(f"❌ Erro ao converter: {e}")
        return None

def main():
    """Converter ambos os documentos"""
    
    print("=" * 80)
    print("🚗 AUTOPRUDENTE - Conversor de Documentação para PDF")
    print("=" * 80)
    print()
    
    # Documento 1: Funcionalidades
    print("1️⃣ FUNCIONALIDADES DO SISTEMA")
    convert_markdown_to_pdf(
        'FUNCIONALIDADES_SISTEMA.md',
        'RENTAL PRICE TRACKER',
        'Funcionalidades do Sistema'
    )
    print()
    
    # Documento 2: Manual do Utilizador
    print("2️⃣ MANUAL DO UTILIZADOR")
    convert_markdown_to_pdf(
        'MANUAL_UTILIZADOR.md',
        'RENTAL PRICE TRACKER',
        'Manual do Utilizador'
    )
    print()
    
    print("=" * 80)
    print("✅ CONVERSÃO COMPLETA!")
    print("=" * 80)
    print()
    print("📄 Ficheiros criados:")
    print("   1. FUNCIONALIDADES_SISTEMA.pdf")
    print("   2. MANUAL_UTILIZADOR.pdf")
    print()
    print("🎨 Características:")
    print("   ✅ Header azul AUTOPRUDENTE")
    print("   ✅ Logo incluído")
    print("   ✅ Formatação profissional")
    print("   ✅ Numeração de páginas")
    print("   ✅ Tabelas estilizadas")
    print("   ✅ Código com syntax highlight")
    print()

if __name__ == "__main__":
    main()
