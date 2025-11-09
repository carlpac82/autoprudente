"""
🎨 RELATÓRIOS MELHORADOS - Diários e Semanais
✅ Header igual ao DR (barra turquesa + logo)
✅ Cores: Azul #009cb6 e Amarelo #fbbf24
✅ TODOS os dias selecionados nas definições
✅ 2 emails separados (Albufeira e Aeroporto)
"""

from datetime import datetime

# Cores oficiais
COLOR_PRIMARY = "#009cb6"      # Turquesa (Auto Prudente)
COLOR_YELLOW = "#fbbf24"       # Amarelo
COLOR_GREEN = "#10b981"        # Verde (melhor preço)
COLOR_ORANGE = "#f59e0b"       # Laranja (competitivo)
COLOR_RED = "#ef4444"          # Vermelho (alerta)
COLOR_GRAY = "#94a3b8"         # Cinza

def generate_report_header(title, subtitle=""):
    """Header padrão para todos os relatórios (igual ao DR)"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }}
            .email-container {{
                max-width: 800px;
                margin: 0 auto;
                background-color: #fff;
            }}
            .header {{
                background-color: {COLOR_PRIMARY};
                padding: 20px;
            }}
            .header-content {{
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .logo img {{
                height: 50px;
            }}
            .header-info {{
                text-align: right;
                color: #fff;
            }}
            .header-title {{
                font-size: 20px;
                font-weight: bold;
                margin: 0;
            }}
            .header-subtitle {{
                font-size: 14px;
                margin: 5px 0 0 0;
                opacity: 0.9;
            }}
            .content {{
                padding: 30px 20px;
            }}
            .group-card {{
                background: #fff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
            }}
            .group-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                padding-bottom: 15px;
                border-bottom: 2px solid {COLOR_PRIMARY};
            }}
            .group-name {{
                font-size: 18px;
                font-weight: bold;
                color: #1e293b;
            }}
            .location-badge {{
                background: {COLOR_YELLOW};
                color: #92400e;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
            }}
            .price-comparison {{
                background: #f8fafc;
                border-radius: 6px;
                padding: 15px;
                margin-bottom: 10px;
            }}
            .competitor {{
                display: flex;
                justify-content: space-between;
                padding: 10px;
                margin: 5px 0;
                background: #fff;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
            }}
            .competitor.autoprudente {{
                background: #e0f7fa;
                border: 2px solid {COLOR_PRIMARY};
            }}
            .position-badge {{
                display: inline-flex;
                align-items: center;
                gap: 5px;
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 13px;
                font-weight: 600;
            }}
            .position-1 {{ background: {COLOR_GREEN}; color: #fff; }}
            .position-2 {{ background: {COLOR_YELLOW}; color: #92400e; }}
            .position-3 {{ background: {COLOR_ORANGE}; color: #fff; }}
            .position-bad {{ background: {COLOR_RED}; color: #fff; }}
            .stats-box {{
                display: flex;
                justify-content: space-around;
                background: #f8fafc;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 25px;
            }}
            .stat {{
                text-align: center;
            }}
            .stat-value {{
                font-size: 32px;
                font-weight: bold;
                color: {COLOR_PRIMARY};
            }}
            .stat-label {{
                font-size: 13px;
                color: #64748b;
                margin-top: 5px;
            }}
            .footer {{
                background: #f8fafc;
                padding: 20px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
                font-size: 12px;
                color: #94a3b8;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="header-content">
                    <div class="logo">
                        <img src="https://carrental-api-5f8q.onrender.com/static/ap-heather.png" alt="Auto Prudente" style="height:50px"/>
                    </div>
                    <div class="header-info">
                        <div class="header-title">{title}</div>
                        {f'<div class="header-subtitle">{subtitle}</div>' if subtitle else ''}
                    </div>
                </div>
            </div>
            <div class="content">
    """

def generate_report_footer():
    """Footer padrão - BARRA AZUL + texto ABAIXO (fora da barra)"""
    return f"""
            </div>
            <!-- Footer: Barra azul -->
            <div style="background: {COLOR_PRIMARY}; padding: 20px; text-align: center;">
                <p style="margin: 0; font-size: 14px; color: #fff; font-weight: 500;">
                    Auto Prudente © {datetime.now().year}
                </p>
            </div>
            <!-- Texto ABAIXO da barra azul (fora) -->
            <div style="background: #f8fafc; padding: 20px; text-align: center;">
                <p style="margin: 0; font-size: 12px; color: #64748b; font-weight: 500;">
                    Sistema de Monitorização de Preços
                </p>
                <p style="margin: 10px 0 0 0; font-size: 11px; color: #94a3b8;">
                    Dados baseados na última pesquisa • Atualizado automaticamente
                </p>
            </div>
        </div>
    </body>
    </html>
    """

def generate_daily_report_html_by_location(search_data, location):
    """
    Generate visual HTML report for ONE location only
    Shows ALL selected days from settings
    ORGANIZED BY DAYS FIRST (1 day → all groups, 2 days → all groups, etc)
    """
    # SVG Icons (monocromáticos)
    icon_car = '<svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/></svg>'
    icon_trophy = '<svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M20 7h-2V5c0-1.1-.9-2-2-2H8c-1.1 0-2 .9-2 2v2H4c-1.1 0-2 .9-2 2v3c0 2.5 1.5 4.7 3.8 5.7.5 1.7 1.8 3 3.5 3.7V23h5v-1.6c1.7-.7 3-2 3.5-3.7 2.3-1 3.8-3.2 3.8-5.7V9c0-1.1-.9-2-2-2zm0 5c0 1.9-1.2 3.5-2.9 4.1-.2-1.3-.8-2.4-1.7-3.3l-1.4 1.4c.6.6 1 1.5 1 2.4 0 1.9-1.6 3.5-3.5 3.5S8 18.5 8 16.6c0-.9.4-1.8 1-2.4L7.6 12.8c-.9.9-1.5 2-1.7 3.3C4.2 15.5 3 13.9 3 12V9h3V5h12v4h3v3z"/></svg>'
    icon_calendar = '<svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V10h14v10zM5 8V6h14v2H5z"/></svg>'
    icon_location = '<svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>'
    
    if not search_data or not search_data.get('results'):
        html = generate_report_header(
            f"Relatório Diário - {location}",
            datetime.now().strftime('%d de %B de %Y')
        )
        html += """
        <div style="text-align: center; padding: 40px;">
            <p style="color: #ef4444; font-size: 16px;">Sem dados de pesquisa disponíveis</p>
            <p style="color: #94a3b8; font-size: 14px;">Execute uma pesquisa para gerar relatórios</p>
        </div>
        """
        html += generate_report_footer()
        return html
    
    # Filter results by location
    results = [r for r in search_data['results'] if r.get('location', '').lower() == location.lower()]
    
    if not results:
        html = generate_report_header(
            f"Relatório Diário - {location}",
            datetime.now().strftime('%d de %B de %Y')
        )
        html += f"""
        <div style="text-align: center; padding: 40px;">
            <p style="color: #94a3b8; font-size: 16px;">Sem dados para {location}</p>
        </div>
        """
        html += generate_report_footer()
        return html
    
    # Group by DAYS first, then by GROUP
    data_by_days = {}
    for car in results:
        days = car.get('days', 1)
        group = car.get('group', 'Unknown')
        
        if days not in data_by_days:
            data_by_days[days] = {}
        
        if group not in data_by_days[days]:
            data_by_days[days][group] = []
        
        data_by_days[days][group].append(car)
    
    # Stats
    ap_best_price = 0
    ap_competitive = 0
    total_searches = 0
    
    # Generate HTML
    html = generate_report_header(
        f"Relatório Diário - {location}",
        datetime.now().strftime('%d de %B de %Y')
    )
    
    # Sort days
    sorted_days = sorted(data_by_days.keys())
    
    content_html = ""
    
    for days in sorted_days:
        groups = data_by_days[days]
        
        # BARRA AZUL - Separador de dias
        content_html += f"""
        <div style="background: {COLOR_PRIMARY}; padding: 15px 20px; margin: 30px 0 20px 0; border-radius: 6px;">
            <div style="color: #fff; font-size: 18px; font-weight: bold; display: flex; align-items: center; gap: 8px;">
                {icon_calendar} {days} dia{'s' if days > 1 else ''}
            </div>
        </div>
        """
        
        # Sort groups
        for group in sorted(groups.keys()):
            cars = groups[group]
            total_searches += 1
            
            # Sort cars by price
            sorted_cars = sorted(cars, key=lambda x: float(x.get('price_num', 999999)))
            
            # Find Auto Prudente position
            ap_position = None
            for idx, car in enumerate(sorted_cars, 1):
                supplier = (car.get('supplier', '') or '').lower()
                if 'autoprudente' in supplier or 'auto prudente' in supplier:
                    ap_position = idx
                    break
            
            if ap_position == 1:
                ap_best_price += 1
                position_bg = COLOR_PRIMARY  # AZUL do website em vez de verde
                position_text = "1º"
                position_icon = icon_trophy
            elif ap_position == 2:
                ap_competitive += 1
                position_bg = COLOR_ORANGE
                position_text = "2º"
                position_icon = icon_trophy
            elif ap_position == 3:
                ap_competitive += 1
                position_bg = COLOR_YELLOW
                position_text = "3º"
                position_icon = icon_trophy
            elif ap_position and ap_position <= 5:
                position_bg = COLOR_GRAY
                position_text = f"{ap_position}º"
                position_icon = ""
            elif ap_position:
                position_bg = COLOR_RED
                position_text = f"{ap_position}º"
                position_icon = ""
            else:
                position_bg = COLOR_GRAY
                position_text = "N/A"
                position_icon = ""
            
            # Cor do texto (branco ou escuro)
            text_color = "#fff" if position_bg not in [COLOR_YELLOW] else "#92400e"
            
            # BARRA AMARELA pequena - Separador de grupos
            content_html += f"""
            <div style="background: {COLOR_YELLOW}; height: 3px; margin: 15px 0 15px 0;"></div>
            """
            
            # Group card
            content_html += f"""
            <div class="group-card">
                <div class="group-header">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        {icon_car}
                        <span class="group-name">{group}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; background: {position_bg}; color: {text_color}; padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: 600; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        {position_icon}
                        <span>{position_text}</span>
                    </div>
                </div>
                <div class="price-comparison">
            """
            
            # Top 5 competitors
            for idx, car in enumerate(sorted_cars[:5], 1):
                supplier = car.get('supplier', 'Unknown')
                price = float(car.get('price_num', 0))
                is_ap = 'autoprudente' in supplier.lower()
                
                # Imagem real do carro (extraída do CarJet)
                car_image = car.get('car_image', '')
                car_name = car.get('car', 'Unknown')
                
                # Se não tiver imagem, usa ícone SVG
                if car_image and car_image.startswith('http'):
                    car_visual = f'<img src="{car_image}" alt="{car_name}" style="width: 60px; height: auto; border-radius: 4px; border: 1px solid #e2e8f0;" onerror="this.style.display=\'none\'">'
                else:
                    car_visual = icon_car
                
                content_html += f"""
                <div class="competitor {'autoprudente' if is_ap else ''}">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        {car_visual}
                        <div>
                            <div style="font-weight: {'bold' if is_ap else '500'}; color: {'#009cb6' if is_ap else '#1e293b'}; font-size: 15px;">
                                {idx}. {supplier}
                            </div>
                            <div style="font-size: 12px; color: #64748b; margin-top: 2px;">
                                {car_name}
                            </div>
                        </div>
                    </div>
                    <div style="font-size: 18px; font-weight: bold; color: {'#009cb6' if is_ap else '#1e293b'};">
                        {price:.2f}€
                    </div>
                </div>
                """
            
            content_html += """
                </div>
            </div>
            """
    
    # Calculate percentage
    ap_percentage = (ap_best_price / total_searches * 100) if total_searches > 0 else 0
    
    # Add stats
    stats_html = f"""
    <div class="stats-box">
        <div class="stat">
            <div class="stat-value" style="color: {COLOR_PRIMARY};">{ap_best_price}</div>
            <div class="stat-label">Melhores Preços</div>
        </div>
        <div class="stat">
            <div class="stat-value" style="color: #92400e;">{ap_competitive}</div>
            <div class="stat-label">Competitivos</div>
        </div>
        <div class="stat">
            <div class="stat-value">{ap_percentage:.0f}%</div>
            <div class="stat-label">Taxa de Liderança</div>
        </div>
    </div>
    """
    
    html += stats_html + content_html + generate_report_footer()
    return html

def generate_weekly_report_html_by_location(months_data, location):
    """
    Generate weekly report for ONE location
    Similar structure to daily but with weekly data
    """
    # Similar logic to daily but adapted for weekly data
    # (código similar ao generate_daily_report_html_by_location mas para dados semanais)
    
    html = generate_report_header(
        f"Relatório Semanal - {location}",
        f"Semana {datetime.now().strftime('%W/%Y')}"
    )
    
    html += """
    <div style="text-align: center; padding: 40px;">
        <p style="color: #94a3b8;">Relatório semanal em desenvolvimento...</p>
    </div>
    """
    
    html += generate_report_footer()
    return html
