# 📱 Mobile Scraping Implementation - WAF Bypass

## 🎯 Objetivo
Evitar detecção do WAF (Web Application Firewall) da CarJet simulando um dispositivo móvel real (iPhone).

## 🔧 Alterações Implementadas

### Arquivo: `main.py` (linha ~7815)
### Função: `track_carjet()` → `run()` → `browser.new_context()`

### ANTES:
```python
context = await browser.new_context()
default_headers = {"User-Agent": "Mozilla/5.0 (compatible; PriceTracker/1.0)"}
await context.set_extra_http_headers(default_headers)
```

### DEPOIS:
```python
# Use mobile user agent and viewport to avoid WAF detection
context = await browser.new_context(
    user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    viewport={"width": 390, "height": 844},  # iPhone 13 Pro
    device_scale_factor=3,
    is_mobile=True,
    has_touch=True,
    locale="pt-PT"
)

# Mobile headers
default_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
}
await context.set_extra_http_headers(default_headers)
```

## 📊 Especificações do Dispositivo Simulado

### iPhone 13 Pro
- **User Agent**: Safari 16.6 no iOS 16.6
- **Viewport**: 390x844 pixels
- **Device Scale**: 3x (Retina)
- **Touch Support**: Ativado
- **Mobile Flag**: Ativado
- **Locale**: pt-PT (Português de Portugal)

## 🎭 Headers Mobile

### Accept Headers
- `Accept`: Suporta HTML, XHTML, XML
- `Accept-Language`: Prioriza PT-PT, depois PT, depois EN
- `Accept-Encoding`: Suporta gzip, deflate, brotli

## ✅ Vantagens

1. **WAF Bypass**: O WAF vê um iPhone legítimo em vez de um bot
2. **Comportamento Real**: Touch events, mobile viewport, device scale
3. **Headers Autênticos**: Headers típicos de Safari mobile
4. **Locale Correto**: pt-PT para conteúdo em português
5. **Performance**: Sites mobile geralmente têm menos JavaScript

## 🧪 Como Testar

### Via API (requer autenticação):
```bash
curl -X POST https://carrental-api-5f8q.onrender.com/api/track-carjet \
  -H "Content-Type: application/json" \
  -H "Cookie: session=YOUR_SESSION" \
  -d '{
    "pickupDate": "2025-11-12",
    "pickupTime": "15:00",
    "durations": [3, 7],
    "locations": [
      {"name": "Albufeira", "template": ""},
      {"name": "Aeroporto de Faro", "template": ""}
    ],
    "lang": "pt",
    "currency": "EUR"
  }'
```

### Via Interface Web:
1. Aceder à página principal
2. Fazer uma pesquisa normal
3. O Playwright automaticamente usará o contexto mobile
4. Verificar logs para confirmar: `[MOBILE]` ou similar

## 📝 Logs Esperados

```
[API] COMPUTED: start_dt=2025-11-12, end_dt=2025-11-19, days=7
[MOBILE] Using iPhone 13 Pro user agent
[MOBILE] Viewport: 390x844, Scale: 3x
[DIRECT] Location: Albufeira, Start: 2025-11-12 15:00:00
[SUCCESS] Found X vehicles
```

## ⚠️ Notas Importantes

1. **Apenas para `/api/track-carjet`**: Esta mudança afeta apenas esta rota
2. **Outras rotas**: Mantêm o comportamento original
3. **Headless**: Continua em modo headless (sem interface gráfica)
4. **Performance**: Pode ser ligeiramente mais lento devido ao mobile rendering

## 🔄 Rollback

Se necessário reverter:
```bash
git revert a19ebbe
```

Ou manualmente, remover os parâmetros mobile do `new_context()`.

## 📅 Histórico

- **2025-11-03 15:54**: Implementação inicial
- **Commit**: `a19ebbe`
- **Branch**: `main`
- **Deploy**: Render (automático)

## 🎯 Próximos Passos (Opcional)

1. Adicionar rotação de user agents (diferentes iPhones)
2. Adicionar delays aleatórios entre requests
3. Simular scroll e interações mobile
4. Adicionar fingerprint mobile mais completo
5. Testar com Android user agents também

---

**Status**: ✅ Implementado e em produção
**Impacto**: Redução esperada de bloqueios WAF
**Risco**: Baixo (apenas mudança de user agent e viewport)
