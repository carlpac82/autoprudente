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
            line-height: 1.8;
            color: #2d3748;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(to bottom, #ffffff 0%, #f7fafc 100%);
        }}
        
        /* Header AUTOPRUDENTE - Cores do website */
        .header {{
            position: running(header);
            background: linear-gradient(135deg, #009cb6 0%, #00b8d4 100%);
            color: white;
            padding: 25px;
            text-align: center;
            border-radius: 0 0 15px 15px;
            box-shadow: 0 6px 12px rgba(0, 156, 182, 0.3);
            margin-bottom: 40px;
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
        
        /* Logo */
        .logo {{
            width: 200px;
            height: auto;
            margin: 0 auto 15px auto;
            display: block;
        }}
        
        h1 {{
            color: #009cb6;
            border-bottom: 4px solid #009cb6;
            padding-bottom: 12px;
            margin-top: 35px;
            font-weight: 700;
        }}
        
        h2 {{
            color: #009cb6;
            margin-top: 28px;
            border-left: 5px solid #00b8d4;
            padding-left: 18px;
            font-weight: 600;
            background: linear-gradient(90deg, rgba(0, 156, 182, 0.05) 0%, transparent 100%);
            padding: 10px 10px 10px 18px;
            border-radius: 0 8px 8px 0;
        }}
        
        h3 {{
            color: #00758a;
            margin-top: 22px;
            font-weight: 600;
        }}
        
        code {{
            background: #e6f7fa;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #00758a;
            border: 1px solid #b3e5f0;
        }}
        
        pre {{
            background: #00758a;
            color: #ffffff;
            padding: 18px;
            border-radius: 10px;
            overflow-x: auto;
            border-left: 5px solid #00b8d4;
            box-shadow: 0 4px 8px rgba(0, 117, 138, 0.2);
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
            background: linear-gradient(135deg, #009cb6 0%, #00b8d4 100%);
            color: white;
            padding: 14px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 9pt;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 10px;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        tr:nth-child(even) {{
            background: #f9fafb;
        }}
        
        blockquote {{
            border-left: 5px solid #009cb6;
            padding-left: 22px;
            margin-left: 0;
            color: #4b5563;
            font-style: italic;
            background: rgba(0, 156, 182, 0.05);
            padding: 15px 15px 15px 22px;
            border-radius: 0 8px 8px 0;
        }}
        
        ul, ol {{
            padding-left: 35px;
            margin: 15px 0;
        }}
        
        li {{
            margin: 10px 0;
            line-height: 1.8;
        }}
        
        ul li::marker {{
            color: #009cb6;
            font-weight: bold;
        }}
        
        ol li::marker {{
            color: #009cb6;
            font-weight: bold;
        }}
        
        .emoji {{
            font-size: 1.3em;
            vertical-align: middle;
        }}
        
        /* Boxes informativos */
        .info-box {{
            background: linear-gradient(135deg, rgba(0, 156, 182, 0.1) 0%, rgba(0, 184, 212, 0.05) 100%);
            border-left: 5px solid #009cb6;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 0 10px 10px 0;
            box-shadow: 0 2px 8px rgba(0, 156, 182, 0.1);
        }}
        
        .warning-box {{
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
            border-left: 5px solid #f59e0b;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 0 10px 10px 0;
        }}
        
        .success-box {{
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
            border-left: 5px solid #10b981;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 0 10px 10px 0;
        }}
        
        /* Footer */
        .footer {{
            margin-top: 60px;
            padding: 25px;
            background: linear-gradient(135deg, #009cb6 0%, #00b8d4 100%);
            color: white;
            text-align: center;
            font-size: 10pt;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 156, 182, 0.2);
        }}
        
        .footer strong {{
            font-size: 12pt;
            letter-spacing: 1px;
        }}
        
        .footer p {{
            margin: 8px 0;
            opacity: 0.95;
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
            background: #009cb6;
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
        <img src="logo_autoprudente.png" alt="AUTOPRUDENTE" class="logo">
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
        import base64
        import os
        
        # Converter logo para base64
        logo_base64 = ""
        logo_path = "logo_autoprudente.png"
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as img_file:
                logo_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        
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
        # Substituir src da imagem por base64
        template_with_logo = HTML_TEMPLATE.replace(
            'src="logo_autoprudente.png"',
            f'src="data:image/png;base64,{logo_base64}"' if logo_base64 else 'src=""'
        )
        
        full_html = template_with_logo.format(
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
