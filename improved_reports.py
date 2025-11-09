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
                font-family: Arial, sans-serif;
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
    """Footer padrão para todos os relatórios"""
    return f"""
            </div>
            <div class="footer">
                <p style="margin: 0;">Auto Prudente © {datetime.now().year} • Sistema de Monitorização de Preços</p>
                <p style="margin: 8px 0 0 0; font-size: 11px; color: #cbd5e1;">
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
    """
    if not search_data or not search_data.get('results'):
        html = generate_report_header(
            f"Relatório Diário - {location}",
            datetime.now().strftime('%d de %B de %Y')
        )
        html += """
        <div style="text-align: center; padding: 40px;">
            <p style="color: #ef4444; font-size: 16px;">⚠️ Sem dados de pesquisa disponíveis</p>
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
    
    # Group by car group AND days
    groups_by_days = {}
    for car in results:
        group = car.get('group', 'Unknown')
        days = car.get('days', 1)
        key = f"{group}_{days}"
        
        if key not in groups_by_days:
            groups_by_days[key] = {
                'group': group,
                'days': days,
                'cars': []
            }
        groups_by_days[key]['cars'].append(car)
    
    # Stats
    total_groups = len(set(g['group'] for g in groups_by_days.values()))
    ap_best_price = 0
    ap_competitive = 0
    
    # Generate HTML
    html = generate_report_header(
        f"Relatório Diário - {location}",
        datetime.now().strftime('%d de %B de %Y')
    )
    
    # Car cards by group and days
    car_cards_html = ""
    
    # Sort by group name and then by days
    sorted_keys = sorted(groups_by_days.keys(), key=lambda k: (groups_by_days[k]['group'], groups_by_days[k]['days']))
    
    for key in sorted_keys:
        data = groups_by_days[key]
        group = data['group']
        days = data['days']
        cars = data['cars']
        
        # Sort cars by price
        sorted_cars = sorted(cars, key=lambda x: float(x.get('price_num', 999999)))
        
        # Find Auto Prudente position
        ap_position = None
        ap_car = None
        for idx, car in enumerate(sorted_cars, 1):
            supplier = (car.get('supplier', '') or '').lower()
            if 'autoprudente' in supplier or 'auto prudente' in supplier:
                ap_car = car
                ap_position = idx
                break
        
        if ap_position == 1:
            ap_best_price += 1
            position_class = "position-1"
            position_text = "🏆 1º Lugar"
        elif ap_position and ap_position <= 3:
            ap_competitive += 1
            position_class = "position-2" if ap_position == 2 else "position-3"
            position_text = f"#{ap_position} Posição"
        elif ap_position:
            position_class = "position-bad"
            position_text = f"⚠️ #{ap_position} Posição"
        else:
            position_class = "position-bad"
            position_text = "Indisponível"
        
        # Generate card
        car_cards_html += f"""
        <div class="group-card">
            <div class="group-header">
                <div>
                    <div class="group-name">🚗 {group}</div>
                    <div style="font-size: 14px; color: #64748b; margin-top: 5px;">
                        📅 {days} dia{'s' if days > 1 else ''} • 📍 {location}
                    </div>
                </div>
                <span class="position-badge {position_class}">{position_text}</span>
            </div>
            <div class="price-comparison">
        """
        
        # Top 5 competitors
        for idx, car in enumerate(sorted_cars[:5], 1):
            supplier = car.get('supplier', 'Unknown')
            price = float(car.get('price_num', 0))
            is_ap = 'autoprudente' in supplier.lower()
            
            car_cards_html += f"""
            <div class="competitor {'autoprudente' if is_ap else ''}">
                <div>
                    <div style="font-weight: {'bold' if is_ap else '500'}; color: {'#009cb6' if is_ap else '#1e293b'};">
                        {idx}. {supplier}
                    </div>
                </div>
                <div style="font-size: 18px; font-weight: bold; color: {'#009cb6' if is_ap else '#1e293b'};">
                    {price:.2f}€
                </div>
            </div>
            """
        
        car_cards_html += """
            </div>
        </div>
        """
    
    # Calculate percentage
    total_searches = len(groups_by_days)
    ap_percentage = (ap_best_price / total_searches * 100) if total_searches > 0 else 0
    
    # Add stats
    stats_html = f"""
    <div class="stats-box">
        <div class="stat">
            <div class="stat-value" style="color: {COLOR_GREEN};">{ap_best_price}</div>
            <div class="stat-label">Melhores Preços</div>
        </div>
        <div class="stat">
            <div class="stat-value" style="color: {COLOR_YELLOW};">{ap_competitive}</div>
            <div class="stat-label">Competitivos</div>
        </div>
        <div class="stat">
            <div class="stat-value">{ap_percentage:.0f}%</div>
            <div class="stat-label">Taxa de Liderança</div>
        </div>
    </div>
    """
    
    html += stats_html + car_cards_html + generate_report_footer()
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
