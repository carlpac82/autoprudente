#!/usr/bin/env python3
"""
Script alternativo para converter Markdown para HTML profissional
Não requer WeasyPrint - pode abrir no browser e imprimir como PDF
"""

import markdown2
import base64
import os

# Template HTML profissional moderno
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @page {{
            size: A4;
            margin: 1.5cm;
        }}
        
        @media print {{
            .no-print {{ display: none; }}
            body {{ background: white; }}
            .page-break {{ page-break-before: always; }}
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #2d3748;
            background: #ffffff;
        }}
        
        /* Header compacto como website */
        .header {{
            background: #009cb6;
            padding: 15px 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 3px solid #00758a;
            margin-bottom: 30px;
        }}
        
        .header-left {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        
        .logo {{
            height: 40px;
            width: auto;
        }}
        
        .header-title {{
            color: white;
            font-size: 16pt;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        
        .header-right {{
            text-align: right;
            color: white;
            font-size: 10pt;
        }}
        
        .header-right .subtitle {{
            opacity: 0.9;
            font-weight: 300;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 40px 40px 40px;
        }}
        
        /* Títulos com ícones monocromáticos */
        h1 {{
            color: #1a202c;
            font-size: 24pt;
            font-weight: 700;
            margin: 40px 0 20px 0;
            padding-bottom: 15px;
            border-bottom: 3px solid #009cb6;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        h1::before {{
            content: '';
            display: inline-block;
            width: 6px;
            height: 40px;
            background: #009cb6;
            border-radius: 3px;
        }}
        
        h2 {{
            color: #2d3748;
            font-size: 18pt;
            font-weight: 600;
            margin: 35px 0 15px 0;
            padding: 12px 20px;
            background: #f7fafc;
            border-left: 4px solid #009cb6;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        h2 i {{
            color: #009cb6;
            font-size: 20pt;
            width: 30px;
            text-align: center;
        }}
        
        h3 {{
            color: #4a5568;
            font-size: 14pt;
            font-weight: 600;
            margin: 25px 0 12px 0;
            padding-left: 15px;
            border-left: 3px solid #cbd5e0;
        }}
        
        h4 {{
            color: #718096;
            font-size: 12pt;
            font-weight: 600;
            margin: 20px 0 10px 0;
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
            border: none;
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
        
        /* Footer compacto */
        .footer {{
            margin-top: 60px;
            padding: 20px 40px;
            background: #f7fafc;
            border-top: 3px solid #009cb6;
            text-align: center;
            font-size: 9pt;
            color: #718096;
        }}
        
        .footer strong {{
            color: #009cb6;
            font-weight: 600;
        }}
        
        /* Listas com ícones */
        ul {{
            list-style: none;
            padding-left: 0;
            margin: 15px 0;
        }}
        
        ul li {{
            padding: 8px 0 8px 35px;
            position: relative;
            line-height: 1.6;
        }}
        
        ul li::before {{
            content: '\\f00c';
            font-family: 'Font Awesome 6 Free';
            font-weight: 900;
            position: absolute;
            left: 0;
            color: #009cb6;
            font-size: 12pt;
        }}
        
        /* Boxes informativos modernos */
        .info-box {{
            background: #f0f9ff;
            border-left: 4px solid #009cb6;
            padding: 20px;
            margin: 25px 0;
            border-radius: 0 8px 8px 0;
        }}
        
        .info-box::before {{
            content: '\\f05a';
            font-family: 'Font Awesome 6 Free';
            font-weight: 900;
            color: #009cb6;
            font-size: 18pt;
            margin-right: 15px;
        }}
        
        .print-button {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #009cb6;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 0 4px 8px rgba(0, 156, 182, 0.3);
            z-index: 1000;
        }}
        
        .print-button:hover {{
            background: #00758a;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <button class="print-button no-print" onclick="window.print()">
        <i class="fas fa-print"></i> Imprimir / Guardar PDF
    </button>
    
    <!-- Header compacto como website -->
    <div class="header">
        <div class="header-left">
            <img src="{logo_data}" alt="AUTOPRUDENTE" class="logo">
            <div class="header-title">{title}</div>
        </div>
        <div class="header-right">
            <div class="subtitle">{subtitle}</div>
            <div>Versão 2.0 | Novembro 2025</div>
        </div>
    </div>
    
    <!-- Conteúdo -->
    <div class="container">
        {content}
    </div>
    
    <!-- Footer compacto -->
    <div class="footer">
        <p><strong>AUTOPRUDENTE</strong> - Sistema de Gestão de Preços de Aluguer de Viaturas | © 2025 Todos os direitos reservados</p>
    </div>
</body>
</html>
"""

def convert_markdown_to_html(md_file, title, subtitle):
    """Converter Markdown para HTML"""
    
    try:
        # Converter logo do header do website para base64
        logo_base64 = ""
        logo_path = "static/ap-heather.png"
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as img_file:
                logo_base64 = f"data:image/png;base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
        else:
            # Fallback para logo alternativo
            logo_path = "logo_autoprudente.png"
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as img_file:
                    logo_base64 = f"data:image/png;base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
        
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
        
        # Criar HTML completo
        full_html = HTML_TEMPLATE.format(
            title=title,
            subtitle=subtitle,
            content=html_content,
            logo_data=logo_base64
        )
        
        # Nome do ficheiro HTML
        html_file = md_file.replace('.md', '.html')
        
        # Salvar HTML
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"✅ HTML criado: {html_file}")
        print(f"   Abrir no browser e usar Ctrl+P (ou Cmd+P) para guardar como PDF")
        return html_file
        
    except Exception as e:
        print(f"❌ Erro ao converter: {e}")
        return None

def main():
    """Converter ambos os documentos"""
    
    print("=" * 80)
    print("🚗 AUTOPRUDENTE - Conversor de Documentação para HTML")
    print("=" * 80)
    print()
    
    # Documento 1: Funcionalidades
    print("1️⃣ FUNCIONALIDADES DO SISTEMA")
    html1 = convert_markdown_to_html(
        'FUNCIONALIDADES_SISTEMA.md',
        'RENTAL PRICE TRACKER',
        'Funcionalidades do Sistema'
    )
    print()
    
    # Documento 2: Manual do Utilizador
    print("2️⃣ MANUAL DO UTILIZADOR")
    html2 = convert_markdown_to_html(
        'MANUAL_UTILIZADOR.md',
        'RENTAL PRICE TRACKER',
        'Manual do Utilizador'
    )
    print()
    
    print("=" * 80)
    print("✅ CONVERSÃO COMPLETA!")
    print("=" * 80)
    print()
    print("📄 Ficheiros HTML criados:")
    if html1:
        print(f"   1. {html1}")
    if html2:
        print(f"   2. {html2}")
    print()
    print("📋 COMO GERAR PDF:")
    print("   1. Abrir ficheiro HTML no browser (Chrome, Safari, Firefox)")
    print("   2. Clicar no botão 'Imprimir / Guardar PDF' (canto superior direito)")
    print("   3. OU usar Cmd+P (Mac) / Ctrl+P (Windows)")
    print("   4. Selecionar 'Guardar como PDF'")
    print("   5. Guardar com nome desejado")
    print()
    print("🎨 Características:")
    print("   ✅ Header azul AUTOPRUDENTE")
    print("   ✅ Logo incluído")
    print("   ✅ Formatação profissional")
    print("   ✅ Cores do website")
    print("   ✅ Pronto para impressão")
    print()

if __name__ == "__main__":
    main()
