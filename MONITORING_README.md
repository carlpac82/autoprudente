# 🔍 Sistema de Monitorização Automática

## ✅ O que foi implementado

### 1. **Classe ScrapingMonitor**
- Rastreia sucessos e falhas por localização
- Conta falhas consecutivas
- Regista timestamp da última vez que funcionou
- Envia alertas após 3 falhas consecutivas

### 2. **Logs Estruturados**
Agora vais ver logs como:
```
[MONITOR] ✅ Albufeira | Método: DIRECT_POST | Items: 82 | Sucessos: 5
[MONITOR] ❌ Albufeira | Método: SELENIUM | Falhas consecutivas: 1 | Erro: Timeout
```

### 3. **Alertas Automáticos**
Após 3 falhas consecutivas, aparece um alerta visual:
```
╔═══════════════════════════════════════════════════════════════╗
║                    🚨 ALERTA DE SCRAPING 🚨                   ║
╠═══════════════════════════════════════════════════════════════╣
║ Location: Albufeira                                           ║
║ Falhas consecutivas: 3                                        ║
║ Último erro: Timeout waiting for element                      ║
║ Última vez que funcionou: 2025-11-02 18:00:00                ║
╚═══════════════════════════════════════════════════════════════╝
```

### 4. **Endpoint de Health Check**
```bash
curl http://localhost:8080/api/monitor/health
```

Resposta:
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

## 🔧 Como usar

### Ver status em tempo real:
```bash
# Ver logs do monitor
tail -f server.log | grep MONITOR

# Ver health check
curl http://localhost:8080/api/monitor/health | jq
```

### Integração futura (TODO):

#### 1. **Email Alerts**
Descomentar em `_send_alert()`:
```python
def _send_email_alert(self, location, failure_count, error):
    msg = EmailMessage()
    msg['Subject'] = f'🚨 Scraping Alert: {location}'
    msg['From'] = 'alerts@yourapp.com'
    msg['To'] = 'your@email.com'
    msg.set_content(f'Falhas: {failure_count}\nErro: {error}')
    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('your@email.com', 'password')
        smtp.send_message(msg)
```

#### 2. **Telegram Alerts**
```python
def _send_telegram_alert(self, location, failure_count, error):
    import requests
    bot_token = 'YOUR_BOT_TOKEN'
    chat_id = 'YOUR_CHAT_ID'
    message = f'🚨 *Scraping Alert*\n\nLocation: {location}\nFalhas: {failure_count}\nErro: {error}'
    
    requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendMessage',
        json={'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}
    )
```

#### 3. **Dashboard Web**
Criar página em `/monitor` para visualizar:
- Gráfico de sucessos/falhas por dia
- Status atual de cada localização
- Histórico de erros
- Tempo médio de resposta

## 📊 Métricas Rastreadas

- **success_count**: Total de sucessos por localização
- **last_success**: Timestamp do último sucesso
- **failures**: Lista de falhas com timestamp, método e erro
- **alert_threshold**: Número de falhas antes de alertar (padrão: 3)

## 🎯 Próximos Passos

1. ✅ **Implementado**: Sistema básico de monitorização
2. ⏳ **TODO**: Adicionar email/Telegram alerts
3. ⏳ **TODO**: Dashboard web visual
4. ⏳ **TODO**: Métricas de performance (tempo de resposta)
5. ⏳ **TODO**: Cache de preços para fallback
6. ⏳ **TODO**: Testes automáticos diários

## 🚀 Benefícios

- ✅ Detecta problemas automaticamente
- ✅ Logs estruturados para debug rápido
- ✅ Histórico de falhas por localização
- ✅ Alertas visuais no terminal
- ✅ API para integração com ferramentas externas
- ✅ Pronto para adicionar notificações (email/Telegram)
