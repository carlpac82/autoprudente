# 🚀 IMPLEMENTAÇÃO DE RELATÓRIOS AUTOMÁTICOS

**Data:** 4 de Novembro de 2025, 22:38  
**Status:** EM IMPLEMENTAÇÃO

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1: Dependências ✅
- [x] Adicionar APScheduler ao requirements.txt
- [x] Instalar pytz para timezone

### Fase 2: Base de Dados ⏳
- [ ] Criar tabela `automated_reports_config`
- [ ] Criar tabela `automated_reports_log`
- [ ] Seed configuração padrão

### Fase 3: Scheduler ⏳
- [ ] Configurar APScheduler no main.py
- [ ] Criar funções de agendamento
- [ ] Iniciar scheduler no startup

### Fase 4: Scraping Automático ⏳
- [ ] Implementar `run_daily_scraping()`
- [ ] Implementar `run_weekly_scraping()`
- [ ] Integrar com carjet_direct

### Fase 5: Geração de Relatórios ⏳
- [ ] Implementar `generate_daily_report()`
- [ ] Implementar `generate_weekly_report()`
- [ ] Templates HTML completos

### Fase 6: Endpoints API ⏳
- [ ] `/api/reports/config/save`
- [ ] `/api/reports/config/load`
- [ ] `/api/reports/manual-trigger`
- [ ] Atualizar endpoints de teste

### Fase 7: Interface ⏳
- [ ] Atualizar customization_automated_reports.html
- [ ] Mostrar destinatários (notification_rules)
- [ ] Adicionar opções de scraping
- [ ] Logs de execução

### Fase 8: Testes ⏳
- [ ] Testar scraping manual
- [ ] Testar geração de relatórios
- [ ] Testar agendamento
- [ ] Testar envio de emails

---

## 🔧 IMPLEMENTAÇÃO

### 1. Requirements.txt

```txt
APScheduler==3.10.4
pytz==2023.3
```

### 2. Tabelas BD

```sql
-- Configuração de relatórios
CREATE TABLE IF NOT EXISTS automated_reports_config (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  report_type TEXT NOT NULL,
  enabled INTEGER DEFAULT 0,
  send_time TEXT DEFAULT '09:00',
  scraping_advance_hours INTEGER DEFAULT 2,
  locations TEXT DEFAULT 'Faro,Albufeira',
  compare_with TEXT DEFAULT 'last_search',
  organization TEXT DEFAULT 'by_day',
  include_logo INTEGER DEFAULT 1,
  weekly_day TEXT DEFAULT 'monday',
  weekly_months INTEGER DEFAULT 3,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Log de execuções
CREATE TABLE IF NOT EXISTS automated_reports_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  report_type TEXT NOT NULL,
  action TEXT NOT NULL,
  status TEXT NOT NULL,
  message TEXT,
  recipients_count INTEGER DEFAULT 0,
  execution_time REAL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

---

## ✅ PRÓXIMOS PASSOS

1. Adicionar APScheduler
2. Criar tabelas
3. Implementar funções
4. Testar sistema
5. Deploy

**Vamos começar!** 🚀
