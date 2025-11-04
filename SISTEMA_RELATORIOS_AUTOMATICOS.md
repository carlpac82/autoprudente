# 📊 SISTEMA DE RELATÓRIOS AUTOMÁTICOS - Especificação Completa

**Data:** 4 de Novembro de 2025, 22:35  
**Status:** Especificação para implementação

---

## 🎯 REQUISITOS

### Relatório Diário:

**Horário:** 09h00 (configurável)

**Processo:**
1. **07h00** - Scraping automático (2h antes)
   - Data aleatória no mês corrente
   - Faro + Albufeira
   - Todos os grupos de carros
   - Salva em `price_snapshots`

2. **09h00** - Geração e envio
   - Busca última pesquisa do histórico
   - Compara com scraping de 07h00
   - Gera relatório HTML
   - Envia para destinatários

**Dados incluídos:**
- ✅ Preços atuais (scraping 07h00)
- ✅ Preços anteriores (última pesquisa histórico)
- ✅ Comparação (diferença %)
- ✅ Alertas (mudanças >10%)
- ✅ Carros mais baratos/caros
- ✅ Disponibilidade por grupo

---

### Relatório Semanal:

**Horário:** Segundas-feiras 09h00 (configurável)

**Processo:**
1. **07h00** - Scraping automático (2h antes)
   - Datas aleatórias nos próximos 3 meses (ou configurável)
   - Faro + Albufeira
   - Todos os grupos
   - Salva em `price_snapshots`

2. **09h00** - Geração e envio
   - Busca pesquisas da última semana
   - Compara tendências
   - Gera relatório HTML
   - Envia para destinatários

**Dados incluídos:**
- ✅ Resumo de 7 dias
- ✅ Tendências de preços (↑↓)
- ✅ Análise de competitividade
- ✅ Recomendações de ajuste
- ✅ Performance por grupo
- ✅ Projeções para próximos 3 meses

---

## 🔧 IMPLEMENTAÇÃO

### 1. Tabela de Configuração:

```sql
CREATE TABLE IF NOT EXISTS automated_reports_config (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  report_type TEXT NOT NULL, -- 'daily' ou 'weekly'
  enabled INTEGER DEFAULT 0,
  send_time TEXT DEFAULT '09:00', -- HH:MM
  scraping_advance_hours INTEGER DEFAULT 2,
  daily_month_range TEXT DEFAULT 'current', -- 'current' ou 'next'
  weekly_months_ahead INTEGER DEFAULT 3,
  last_run TEXT,
  next_run TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

---

### 2. Scheduler (APScheduler):

```python
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

scheduler = BackgroundScheduler(timezone=pytz.timezone('Europe/Lisbon'))

def schedule_reports():
    """Agendar relatórios automáticos"""
    
    # Buscar configurações
    config_daily = get_report_config('daily')
    config_weekly = get_report_config('weekly')
    
    if config_daily and config_daily['enabled']:
        # Agendar scraping diário (2h antes)
        scraping_time = subtract_hours(config_daily['send_time'], 2)
        scheduler.add_job(
            run_daily_scraping,
            CronTrigger(hour=scraping_time.hour, minute=scraping_time.minute),
            id='daily_scraping'
        )
        
        # Agendar envio diário
        send_time = parse_time(config_daily['send_time'])
        scheduler.add_job(
            send_daily_report,
            CronTrigger(hour=send_time.hour, minute=send_time.minute),
            id='daily_report'
        )
    
    if config_weekly and config_weekly['enabled']:
        # Agendar scraping semanal (2h antes, segundas)
        scraping_time = subtract_hours(config_weekly['send_time'], 2)
        scheduler.add_job(
            run_weekly_scraping,
            CronTrigger(day_of_week='mon', hour=scraping_time.hour, minute=scraping_time.minute),
            id='weekly_scraping'
        )
        
        # Agendar envio semanal (segundas)
        send_time = parse_time(config_weekly['send_time'])
        scheduler.add_job(
            send_weekly_report,
            CronTrigger(day_of_week='mon', hour=send_time.hour, minute=send_time.minute),
            id='weekly_report'
        )
    
    scheduler.start()
```

---

### 3. Scraping Automático Diário:

```python
async def run_daily_scraping():
    """Scraping automático para relatório diário"""
    try:
        logging.info("🔄 Starting daily automated scraping...")
        
        # Data aleatória no mês corrente
        today = datetime.now()
        random_day = random.randint(1, 28)  # Seguro para todos os meses
        random_date = today.replace(day=random_day)
        
        # Se a data for no passado, usar próximo mês
        if random_date < today:
            random_date = random_date.replace(month=today.month + 1)
        
        start_date = random_date
        end_date = start_date + timedelta(days=7)  # 7 dias de aluguer
        
        # Scraping Faro
        logging.info(f"📍 Scraping Faro: {start_date.strftime('%d/%m/%Y')}")
        results_faro = await scrape_carjet_direct("Faro", start_date, end_date)
        
        # Scraping Albufeira
        logging.info(f"📍 Scraping Albufeira: {start_date.strftime('%d/%m/%Y')}")
        results_albufeira = await scrape_carjet_direct("Albufeira", start_date, end_date)
        
        # Salvar em price_snapshots
        save_to_snapshots(results_faro, "Faro", start_date, end_date)
        save_to_snapshots(results_albufeira, "Albufeira", start_date, end_date)
        
        # Marcar como concluído
        mark_scraping_completed('daily', datetime.now())
        
        logging.info(f"✅ Daily scraping completed: {len(results_faro) + len(results_albufeira)} results")
        
    except Exception as e:
        logging.error(f"❌ Daily scraping error: {str(e)}")
        raise
```

---

### 4. Scraping Automático Semanal:

```python
async def run_weekly_scraping():
    """Scraping automático para relatório semanal"""
    try:
        logging.info("🔄 Starting weekly automated scraping...")
        
        # Buscar configuração de meses
        config = get_report_config('weekly')
        months_ahead = config.get('weekly_months_ahead', 3)
        
        today = datetime.now()
        all_results = []
        
        # Scraping para próximos N meses
        for month_offset in range(months_ahead):
            # Data aleatória em cada mês
            target_month = today.month + month_offset
            target_year = today.year
            
            if target_month > 12:
                target_month -= 12
                target_year += 1
            
            random_day = random.randint(1, 28)
            random_date = datetime(target_year, target_month, random_day)
            
            start_date = random_date
            end_date = start_date + timedelta(days=7)
            
            logging.info(f"📅 Month {month_offset + 1}: {start_date.strftime('%d/%m/%Y')}")
            
            # Scraping Faro
            results_faro = await scrape_carjet_direct("Faro", start_date, end_date)
            save_to_snapshots(results_faro, "Faro", start_date, end_date)
            
            # Scraping Albufeira
            results_albufeira = await scrape_carjet_direct("Albufeira", start_date, end_date)
            save_to_snapshots(results_albufeira, "Albufeira", start_date, end_date)
            
            all_results.extend(results_faro + results_albufeira)
        
        # Marcar como concluído
        mark_scraping_completed('weekly', datetime.now())
        
        logging.info(f"✅ Weekly scraping completed: {len(all_results)} results across {months_ahead} months")
        
    except Exception as e:
        logging.error(f"❌ Weekly scraping error: {str(e)}")
        raise
```

---

### 5. Geração Relatório Diário:

```python
async def send_daily_report():
    """Gerar e enviar relatório diário"""
    try:
        logging.info("📊 Generating daily report...")
        
        # 1. Buscar última pesquisa do histórico
        last_search = get_last_search_from_history()
        
        # 2. Buscar scraping de hoje (07h00)
        today_scraping = get_today_scraping()
        
        # 3. Comparar dados
        comparison = compare_prices(last_search, today_scraping)
        
        # 4. Identificar alertas (mudanças >10%)
        alerts = identify_price_alerts(comparison, threshold=10)
        
        # 5. Gerar HTML
        html_content = generate_daily_report_html(
            current_data=today_scraping,
            previous_data=last_search,
            comparison=comparison,
            alerts=alerts
        )
        
        # 6. Buscar destinatários
        recipients = get_report_recipients()
        
        # 7. Enviar emails
        sent_count = 0
        for recipient in recipients:
            try:
                send_report_email(
                    to=recipient,
                    subject=f"📊 Relatório Diário de Preços - {datetime.now().strftime('%d/%m/%Y')}",
                    html=html_content
                )
                sent_count += 1
            except Exception as e:
                logging.error(f"Failed to send to {recipient}: {str(e)}")
        
        # 8. Marcar como enviado
        mark_report_sent('daily', datetime.now(), sent_count)
        
        logging.info(f"✅ Daily report sent to {sent_count} recipient(s)")
        
    except Exception as e:
        logging.error(f"❌ Daily report error: {str(e)}")
        raise
```

---

### 6. Geração Relatório Semanal:

```python
async def send_weekly_report():
    """Gerar e enviar relatório semanal"""
    try:
        logging.info("📊 Generating weekly report...")
        
        # 1. Buscar pesquisas dos últimos 7 dias
        week_searches = get_searches_last_7_days()
        
        # 2. Buscar scraping de hoje (07h00)
        today_scraping = get_today_scraping()
        
        # 3. Calcular tendências
        trends = calculate_price_trends(week_searches)
        
        # 4. Análise de competitividade
        competitiveness = analyze_competitiveness(today_scraping)
        
        # 5. Recomendações
        recommendations = generate_recommendations(trends, competitiveness)
        
        # 6. Projeções
        projections = calculate_projections(trends, months=3)
        
        # 7. Gerar HTML
        html_content = generate_weekly_report_html(
            week_data=week_searches,
            current_data=today_scraping,
            trends=trends,
            competitiveness=competitiveness,
            recommendations=recommendations,
            projections=projections
        )
        
        # 8. Buscar destinatários
        recipients = get_report_recipients()
        
        # 9. Enviar emails
        sent_count = 0
        for recipient in recipients:
            try:
                send_report_email(
                    to=recipient,
                    subject=f"📊 Relatório Semanal de Preços - Semana {datetime.now().strftime('%W/%Y')}",
                    html=html_content
                )
                sent_count += 1
            except Exception as e:
                logging.error(f"Failed to send to {recipient}: {str(e)}")
        
        # 10. Marcar como enviado
        mark_report_sent('weekly', datetime.now(), sent_count)
        
        logging.info(f"✅ Weekly report sent to {sent_count} recipient(s)")
        
    except Exception as e:
        logging.error(f"❌ Weekly report error: {str(e)}")
        raise
```

---

## 📊 ESTRUTURA DOS DADOS

### Relatório Diário:

```json
{
  "report_type": "daily",
  "date": "2025-11-04",
  "scraping_date": "2025-11-15",
  "locations": ["Faro", "Albufeira"],
  "summary": {
    "total_cars": 150,
    "price_changes": 23,
    "alerts": 5
  },
  "comparison": [
    {
      "car": "VW Golf",
      "group": "D",
      "location": "Faro",
      "current_price": 45.50,
      "previous_price": 42.00,
      "change_pct": 8.3,
      "alert": false
    }
  ],
  "alerts": [
    {
      "car": "BMW 3 Series",
      "group": "J2",
      "location": "Albufeira",
      "current_price": 95.00,
      "previous_price": 78.00,
      "change_pct": 21.8,
      "alert": true
    }
  ],
  "cheapest": [...],
  "most_expensive": [...],
  "availability": {...}
}
```

---

### Relatório Semanal:

```json
{
  "report_type": "weekly",
  "week": "45/2025",
  "date_range": ["2025-11-04", "2025-11-10"],
  "scraping_dates": ["2025-11-15", "2025-12-10", "2026-01-08"],
  "summary": {
    "total_searches": 7,
    "avg_price_change": 3.2,
    "trending_up": 45,
    "trending_down": 32
  },
  "trends": [
    {
      "car": "VW Golf",
      "group": "D",
      "trend": "up",
      "avg_change": 5.2,
      "volatility": "low"
    }
  ],
  "competitiveness": {
    "very_competitive": 45,
    "competitive": 67,
    "expensive": 23
  },
  "recommendations": [
    {
      "action": "reduce_price",
      "car": "BMW 3 Series",
      "current": 95.00,
      "suggested": 85.00,
      "reason": "20% above market average"
    }
  ],
  "projections": {
    "next_month": {...},
    "2_months": {...},
    "3_months": {...}
  }
}
```

---

## 🎨 TEMPLATE HTML

### Relatório Diário:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Relatório Diário de Preços</title>
</head>
<body style="font-family: 'Segoe UI', sans-serif; background: #f8fafc;">
    <!-- Header -->
    <div style="background: linear-gradient(135deg, #009cb6 0%, #007a91 100%); padding: 30px; text-align: center;">
        <h1 style="color: white; margin: 0;">📊 Relatório Diário de Preços</h1>
        <p style="color: #e0f2f7; margin: 10px 0 0 0;">{{date}} - Data de Pesquisa: {{scraping_date}}</p>
    </div>
    
    <!-- Summary -->
    <div style="padding: 20px;">
        <h2>📈 Resumo</h2>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
            <div style="background: white; padding: 20px; border-radius: 8px; text-align: center;">
                <div style="font-size: 32px; color: #009cb6; font-weight: bold;">{{total_cars}}</div>
                <div style="color: #64748b; font-size: 14px;">Carros Analisados</div>
            </div>
            <div style="background: white; padding: 20px; border-radius: 8px; text-align: center;">
                <div style="font-size: 32px; color: #f59e0b; font-weight: bold;">{{price_changes}}</div>
                <div style="color: #64748b; font-size: 14px;">Mudanças de Preço</div>
            </div>
            <div style="background: white; padding: 20px; border-radius: 8px; text-align: center;">
                <div style="font-size: 32px; color: #ef4444; font-weight: bold;">{{alerts}}</div>
                <div style="color: #64748b; font-size: 14px;">Alertas (>10%)</div>
            </div>
        </div>
    </div>
    
    <!-- Alerts -->
    {{#if alerts}}
    <div style="padding: 20px;">
        <h2>🚨 Alertas de Preço</h2>
        {{#each alerts}}
        <div style="background: #fef2f2; border-left: 4px solid #ef4444; padding: 15px; margin-bottom: 10px; border-radius: 4px;">
            <div style="font-weight: bold; color: #991b1b;">{{car}} ({{group}}) - {{location}}</div>
            <div style="color: #7f1d1d; font-size: 14px; margin-top: 5px;">
                €{{previous_price}} → €{{current_price}} 
                <span style="color: #ef4444; font-weight: bold;">(+{{change_pct}}%)</span>
            </div>
        </div>
        {{/each}}
    </div>
    {{/if}}
    
    <!-- Comparison Table -->
    <div style="padding: 20px;">
        <h2>📊 Comparação de Preços</h2>
        <table style="width: 100%; background: white; border-radius: 8px; overflow: hidden;">
            <thead>
                <tr style="background: #f1f5f9;">
                    <th style="padding: 12px; text-align: left;">Carro</th>
                    <th style="padding: 12px; text-align: left;">Grupo</th>
                    <th style="padding: 12px; text-align: left;">Local</th>
                    <th style="padding: 12px; text-align: right;">Anterior</th>
                    <th style="padding: 12px; text-align: right;">Atual</th>
                    <th style="padding: 12px; text-align: right;">Mudança</th>
                </tr>
            </thead>
            <tbody>
                {{#each comparison}}
                <tr style="border-bottom: 1px solid #e2e8f0;">
                    <td style="padding: 12px;">{{car}}</td>
                    <td style="padding: 12px;">{{group}}</td>
                    <td style="padding: 12px;">{{location}}</td>
                    <td style="padding: 12px; text-align: right;">€{{previous_price}}</td>
                    <td style="padding: 12px; text-align: right;">€{{current_price}}</td>
                    <td style="padding: 12px; text-align: right; color: {{#if (gt change_pct 0)}}#ef4444{{else}}#10b981{{/if}};">
                        {{#if (gt change_pct 0)}}+{{/if}}{{change_pct}}%
                    </td>
                </tr>
                {{/each}}
            </tbody>
        </table>
    </div>
    
    <!-- Footer -->
    <div style="padding: 20px; text-align: center; color: #94a3b8; font-size: 12px;">
        Auto Prudente © 2025 - Sistema de Monitorização de Preços
    </div>
</body>
</html>
```

---

## ⚙️ CONFIGURAÇÃO

### Settings → Automated Reports:

```
┌─────────────────────────────────────────┐
│ Relatórios Automáticos                  │
├─────────────────────────────────────────┤
│                                          │
│ Relatório Diário:                        │
│ ☑ Ativado                                │
│ Horário de Envio: [09:00] ▼             │
│ Scraping: 2 horas antes                  │
│ Mês: ⦿ Corrente  ○ Próximo              │
│                                          │
│ Relatório Semanal:                       │
│ ☑ Ativado                                │
│ Horário de Envio: [09:00] ▼             │
│ Dia: ⦿ Segunda  ○ Sexta                 │
│ Scraping: 2 horas antes                  │
│ Meses à frente: [3] ▼                    │
│                                          │
│ Destinatários:                           │
│ (Usa Notification Rules ativas)         │
│                                          │
│ [Guardar Configuração]  [Testar Agora]  │
└─────────────────────────────────────────┘
```

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1: Base de Dados
- [ ] Criar tabela `automated_reports_config`
- [ ] Criar índices necessários
- [ ] Seed configuração padrão

### Fase 2: Scheduler
- [ ] Instalar APScheduler
- [ ] Configurar timezone (Europe/Lisbon)
- [ ] Criar funções de agendamento
- [ ] Testar agendamento

### Fase 3: Scraping Automático
- [ ] Implementar `run_daily_scraping()`
- [ ] Implementar `run_weekly_scraping()`
- [ ] Testar scraping
- [ ] Validar salvamento em BD

### Fase 4: Geração de Relatórios
- [ ] Implementar `send_daily_report()`
- [ ] Implementar `send_weekly_report()`
- [ ] Criar templates HTML
- [ ] Testar geração

### Fase 5: Comparação e Análise
- [ ] Implementar `compare_prices()`
- [ ] Implementar `identify_price_alerts()`
- [ ] Implementar `calculate_price_trends()`
- [ ] Implementar `analyze_competitiveness()`
- [ ] Implementar `generate_recommendations()`

### Fase 6: Interface
- [ ] Criar página de configuração
- [ ] Adicionar botões de teste
- [ ] Mostrar histórico de envios
- [ ] Logs de execução

### Fase 7: Testes
- [ ] Testar scraping manual
- [ ] Testar geração de relatórios
- [ ] Testar envio de emails
- [ ] Testar agendamento

### Fase 8: Deploy
- [ ] Commit e push
- [ ] Deploy no Render
- [ ] Configurar no Render
- [ ] Monitorizar primeiros envios

---

## 🎯 PRÓXIMOS PASSOS

1. **Criar tabelas na BD**
2. **Instalar APScheduler**
3. **Implementar funções de scraping**
4. **Implementar geração de relatórios**
5. **Criar interface de configuração**
6. **Testar sistema completo**
7. **Deploy e ativação**

---

**SISTEMA COMPLETO ESPECIFICADO!** ✅  
**Pronto para implementação!** 🚀
