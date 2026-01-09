# Otimizações de Performance - Scraping Carjet

## 🐌 Problemas Identificados (Análise dos Logs)

### 1. **Timeout no Dropdown (120s)**
```
[SELENIUM] ⚠️ Dropdown falhou: HTTPConnectionPool(host='localhost', port=57377): Read timed out. (read timeout=120)
```
- **Causa:** Timeout HTTP do Selenium muito alto
- **Impacto:** 2 minutos de espera desnecessária
- **Solução:** Reduzir para 10-15s

### 2. **Processamento Sequencial de Cards (269 cards)**
```
🔍 [CARD-START] Processando card 1/269...
🔍 [CARD-START] Processando card 2/269...
...
🔍 [CARD-START] Processando card 269/269...
```
- **Causa:** Loop sequencial card por card
- **Impacto:** ~1-2s por card = 4-8 minutos total
- **Solução:** Processar todos os cards de uma vez com JavaScript

### 3. **Polling Constante do WhatsApp**
```
[WHATSAPP] ❌ Error getting unread count: no such table: whatsapp_conversations
INFO: None:0 - "GET /api/whatsapp/unread-count HTTP/1.1" 500 Internal Server Error
```
- **Causa:** Frontend faz polling a cada 2-3 segundos
- **Impacto:** Logs poluídos, overhead desnecessário
- **Solução:** Desativar polling ou criar tabela

### 4. **Verificações de Conflito Repetidas**
```
WARNING:root:⚠️ [VEHICLES-CONFLICT] Mercedes GLB 7 seater:
WARNING:root:     VEHICLES diz: Manual (grupo M1)
WARNING:root:     DETECTADO: Automatic
WARNING:root:     → USANDO DETECTADO (li value é mais confiável)
```
- **Causa:** Verificação para cada carro individualmente
- **Impacto:** Logs verbosos, processamento extra
- **Solução:** Cache de verificações ou reduzir logging

### 5. **Limpeza do Driver com Retries**
```
WARNING:urllib3.connectionpool:Retrying (Retry(total=2, connect=None, read=None...
WARNING:urllib3.connectionpool:Retrying (Retry(total=1, connect=None, read=None...
WARNING:urllib3.connectionpool:Retrying (Retry(total=0, connect=None, read=None...
```
- **Causa:** Driver já fechado mas tenta fechar novamente
- **Impacto:** 3 tentativas falhadas = ~10s perdidos
- **Solução:** Try/except silencioso ou flag de estado

---

## ✅ Soluções Implementadas

### Otimização 1: Reduzir Timeout do Selenium
**Localização:** `main.py` linha ~11730

**Antes:**
```python
driver.set_script_timeout(5)  # 5s
# Mas o HTTP timeout é 120s por padrão
```

**Depois:**
```python
driver.set_page_load_timeout(15)  # Máximo 15s para carregar página
driver.set_script_timeout(10)     # Máximo 10s para scripts
# Configurar timeout HTTP do Selenium para 15s
```

### Otimização 2: Parsing de Cards em Batch
**Localização:** `main.py` função de parsing

**Antes:**
```python
for card in cards:
    price = extract_price(card)
    name = extract_name(card)
    # ... processar 1 por 1
```

**Depois:**
```python
# Extrair TODOS os dados de uma vez via JavaScript
all_data = driver.execute_script("""
    return Array.from(document.querySelectorAll('article')).map(card => ({
        price: card.querySelector('.price')?.textContent,
        name: card.querySelector('.name')?.textContent,
        // ... todos os campos
    }));
""")
# Processar array Python (muito mais rápido)
```

### Otimização 3: Desativar Polling WhatsApp
**Localização:** Frontend JavaScript

**Solução:**
```javascript
// Comentar ou remover:
// setInterval(() => fetch('/api/whatsapp/unread-count'), 3000);

// Ou criar tabela vazia:
CREATE TABLE IF NOT EXISTS whatsapp_conversations (id INTEGER PRIMARY KEY);
```

### Otimização 4: Reduzir Logging Verboso
**Localização:** `main.py` warnings

**Antes:**
```python
logger.warning(f"⚠️ [VEHICLES-CONFLICT] {car_name}:")
logger.warning(f"     VEHICLES diz: {db_trans}")
logger.warning(f"     DETECTADO: {detected_trans}")
logger.warning(f"     → USANDO DETECTADO")
```

**Depois:**
```python
# Apenas em modo DEBUG
if DEBUG_MODE:
    logger.debug(f"Conflict: {car_name} - using detected: {detected_trans}")
```

### Otimização 5: Limpeza Silenciosa do Driver
**Localização:** `main.py` cleanup

**Antes:**
```python
driver.quit()  # Pode falhar com retries
```

**Depois:**
```python
try:
    driver.quit()
except:
    pass  # Ignorar erros de cleanup
```

---

## 📊 Impacto Esperado

| Otimização | Tempo Antes | Tempo Depois | Ganho |
|------------|-------------|--------------|-------|
| Timeout dropdown | 120s | 15s | -105s |
| Parsing cards | 4-8min | 5-10s | -4min |
| WhatsApp polling | Constante | 0 | Logs limpos |
| Logging verboso | N/A | N/A | Logs 50% menores |
| Driver cleanup | 10s | 0.5s | -9.5s |
| **TOTAL** | **~6-10min** | **~30-60s** | **~85% mais rápido** |

---

## 🚀 Como Aplicar

1. Fazer backup do `main.py`
2. Aplicar otimizações uma por uma
3. Testar após cada otimização
4. Medir tempo de resposta
5. Ajustar conforme necessário

---

## 📝 Notas

- Prioridade: **Otimização 2 (Parsing em Batch)** - maior impacto
- Teste: Fazer pesquisa Faro 7 dias e medir tempo
- Monitorar: Logs do Selenium para novos erros
- Rollback: Manter backup do código original
