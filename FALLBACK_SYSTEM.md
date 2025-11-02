# 🛡️ Sistema de Fallback e Recuperação Automática

## 🎯 O que acontece quando o scraping falha?

### Sistema de Fallback em Cascata

```
1. DIRECT POST (rápido, 90% sucesso)
   ↓ FALHA
2. SELENIUM (robusto, lida com JavaScript)
   ↓ FALHA
3. PLAYWRIGHT (alternativa ao Selenium)
   ↓ FALHA
4. CACHE (últimos preços válidos, até 48h)
   ↓ FALHA
5. ALERTA (notificação ao admin)
```

## ✅ Implementado

### 1. **Cache de Preços** ✅
- **Quando guarda:** Sempre que scraping tem sucesso
- **Validade:** 48 horas
- **Localização:** SQLite database (`price_cache` table)
- **Chave:** `{location}_{start_date}_{days}`

#### Estrutura do Cache:
```sql
CREATE TABLE price_cache (
    cache_key TEXT PRIMARY KEY,
    location TEXT,
    start_date TEXT,
    days INTEGER,
    items_json TEXT,
    cached_at TEXT,
    method TEXT
)
```

### 2. **Monitorização Automática** ✅
- Rastreia sucessos/falhas por localização
- Alerta após 3 falhas consecutivas
- Dashboard de saúde: `/api/monitor/health`

### 3. **Logs Estruturados** ✅
```
[CACHE] ✅ Saved 82 items for Albufeira
[CACHE] ✅ Found 82 items (2.5h old)
[CACHE] ⚠️  Cache expirado (49.2h > 48h)
[MONITOR] ✅ Albufeira | Método: DIRECT_POST | Items: 82
[MONITOR] ❌ Faro | Método: SELENIUM | Falhas consecutivas: 2
```

## 🔄 Fluxo Completo

### Cenário 1: Sucesso Normal
```
1. User faz pedido → /api/prices?location=Albufeira&days=7
2. DIRECT POST → ✅ 82 carros
3. Guardar em cache
4. Log sucesso no monitor
5. Retornar resultados
```

### Cenário 2: Falha com Cache Disponível
```
1. User faz pedido → /api/prices?location=Faro&days=7
2. DIRECT POST → ❌ Timeout
3. SELENIUM → ❌ Cookie bloqueou
4. PLAYWRIGHT → ❌ Não disponível
5. Verificar cache → ✅ Encontrado (3h atrás)
6. Log falha no monitor
7. Retornar cache com aviso
```

**Response JSON:**
```json
{
  "ok": true,
  "items": [...],
  "from_cache": true,
  "cache_age_hours": 3.2,
  "cache_warning": "⚠️ Dados de cache (3.2h atrás)"
}
```

### Cenário 3: Falha Total (Sem Cache)
```
1. User faz pedido → /api/prices?location=Lisboa&days=7
2. DIRECT POST → ❌ Falhou
3. SELENIUM → ❌ Falhou
4. PLAYWRIGHT → ❌ Falhou
5. Verificar cache → ❌ Não existe ou expirado
6. Log falha no monitor (3ª falha → ALERTA!)
7. Retornar erro 502
```

**Response JSON:**
```json
{
  "ok": false,
  "error": "Upstream fetch failed"
}
```

**Alerta no Terminal:**
```
╔═══════════════════════════════════════════════════════════════╗
║                    🚨 ALERTA DE SCRAPING 🚨                   ║
╠═══════════════════════════════════════════════════════════════╣
║ Location: Lisboa                                              ║
║ Falhas consecutivas: 3                                        ║
║ Último erro: Upstream fetch failed                            ║
║ Última vez que funcionou: 2025-11-02 15:30:00                ║
╚═══════════════════════════════════════════════════════════════╝
```

## 📊 Configurações

### Cache Max Age
```python
# Default: 48 horas
cache_result = _get_price_cache(location, start_date, days, max_age_hours=48)

# Personalizar:
cache_result = _get_price_cache(location, start_date, days, max_age_hours=72)  # 3 dias
```

### Alert Threshold
```python
# Default: 3 falhas consecutivas
class ScrapingMonitor:
    def __init__(self):
        self.alert_threshold = 3  # Mudar aqui
```

## 🎛️ Endpoints

### Ver Status do Sistema
```bash
curl http://localhost:8080/api/monitor/health | jq
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-02T18:00:00",
  "success_count": {
    "Albufeira": 10,
    "Faro": 8
  },
  "last_success": {
    "Albufeira": "2025-11-02T17:55:00",
    "Faro": "2025-11-02T17:50:00"
  },
  "active_failures": {},
  "total_locations_monitored": 2
}
```

### Limpar Cache (Manual)
```sql
-- Limpar cache expirado
DELETE FROM price_cache 
WHERE datetime(cached_at) < datetime('now', '-48 hours');

-- Limpar todo o cache
DELETE FROM price_cache;
```

## 🚨 Quando Receberes Alertas

### Alerta: 3 Falhas Consecutivas

#### 1. **Verificar Logs**
```bash
tail -f server.log | grep -E "MONITOR|CACHE|ERROR"
```

#### 2. **Verificar Site CarJet**
- Abrir manualmente: https://www.carjet.com
- Verificar se está online
- Verificar se mudaram o layout

#### 3. **Testar API Manualmente**
```bash
curl "http://localhost:8080/api/prices?location=Albufeira&days=7" | jq
```

#### 4. **Ver Health Status**
```bash
curl http://localhost:8080/api/monitor/health | jq
```

#### 5. **Ações Possíveis:**
- ✅ Esperar (pode ser temporário)
- ✅ Usar cache (dados antigos mas válidos)
- ✅ Verificar se CarJet mudou HTML
- ✅ Atualizar seletores CSS
- ✅ Contactar suporte CarJet

## 📈 Melhorias Futuras (TODO)

### 1. **Retry Automático com Backoff**
```python
for attempt in range(3):
    result = try_scrape()
    if result:
        break
    time.sleep(5 * (attempt + 1))  # 5s, 10s, 15s
```

### 2. **Email/Telegram Alerts**
```python
def _send_alert(self, location, failure_count, error):
    # Email
    send_email(
        to="admin@example.com",
        subject=f"🚨 Scraping Alert: {location}",
        body=f"Falhas: {failure_count}\nErro: {error}"
    )
    
    # Telegram
    send_telegram(
        chat_id="123456",
        text=f"🚨 {location}: {failure_count} falhas"
    )
```

### 3. **Cache Inteligente**
- Priorizar cache mais recente
- Combinar múltiplos caches
- Previsão de preços baseada em histórico

### 4. **Rotação de Proxies**
```python
proxies = ["proxy1.com", "proxy2.com", "proxy3.com"]
for proxy in proxies:
    result = try_scrape(proxy=proxy)
    if result:
        break
```

### 5. **Dashboard Web**
- Gráfico de uptime
- Histórico de falhas
- Botão "Force Refresh"
- Status em tempo real

## 🎯 Resumo: O que fazer quando falha?

### ✅ Sistema Automático (Já Implementado)
1. Tenta DIRECT POST
2. Tenta SELENIUM
3. Tenta PLAYWRIGHT
4. Usa CACHE (até 48h)
5. Envia ALERTA (após 3 falhas)

### 🔧 Ação Manual (Se Necessário)
1. Ver logs: `tail -f server.log | grep MONITOR`
2. Ver health: `curl /api/monitor/health`
3. Testar manualmente: Abrir CarJet no browser
4. Aguardar (pode ser temporário)
5. Atualizar código (se CarJet mudou)

### 📞 Quando Contactar Suporte
- ❌ Falhas > 24 horas
- ❌ Cache expirado
- ❌ CarJet mudou completamente
- ❌ Erro 403/429 (bloqueado)

---

**Sistema robusto implementado! Agora tens:**
- ✅ Cache automático
- ✅ Fallback em cascata
- ✅ Monitorização
- ✅ Alertas visuais
- ✅ Logs estruturados
