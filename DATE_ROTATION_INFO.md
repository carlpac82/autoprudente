# 🔄 Date Rotation - Anti-Detecção

## ✅ FUNCIONALIDADE ATIVADA!

A rotação de datas agora está implementada no endpoint `/api/track-by-params` que é usado pelo **Automated Prices**.

## 🎯 Como Funciona

### Exemplo Prático:

Se procuras preços para **4 de Novembro** com `maxDaysAhead = 4`:

```
Pesquisa 1: 4 Nov → Sistema escolhe aleatoriamente: 6 Nov (+2 dias)
Pesquisa 2: 4 Nov → Sistema escolhe aleatoriamente: 4 Nov (+0 dias)
Pesquisa 3: 4 Nov → Sistema escolhe aleatoriamente: 7 Nov (+3 dias)
Pesquisa 4: 4 Nov → Sistema escolhe aleatoriamente: 5 Nov (+1 dia)
```

### 📊 Resultado:

Cada pesquisa usa uma data diferente (dentro do intervalo 0-4 dias), tornando cada request único para o WAF (Web Application Firewall).

## ⚙️ Configuração

### Onde Configurar:

**Price Automation → Settings → Anti-WAF Protection**

1. **Enable Date Rotation** ✅ (checkbox)
   - Ativa/desativa a rotação de datas
   - Padrão: Ativado

2. **Max Days Ahead** (0-7)
   - Quantos dias à frente pode variar
   - Padrão: 4 dias
   - Exemplo: Se escolheres 3, varia entre 0 e 3 dias

### 💾 Onde é Guardado:

- Base de dados: `price_automation_settings`
- Keys: `date_rotation_enabled` e `date_rotation_max_days`

## 📋 Logs

Quando faz uma pesquisa, vês nos logs:

```
[DATE_ROTATION] Original: 2025-11-04, Rotated: 2025-11-06 (+2 days)
```

Ou se estiver desativado:

```
[DATE_ROTATION] Desativado, usando data original: 2025-11-04
```

## 🔍 Diferença com Alternative Search

### Date Rotation (Este):
- **Objetivo:** Evitar detecção pelo WAF
- **Quando:** SEMPRE que faz uma pesquisa
- **Como:** Escolhe aleatoriamente uma data entre 0 e N dias
- **Exemplo:** Procuras 4 Nov → Sistema usa 6 Nov

### Alternative Search (Outro):
- **Objetivo:** Encontrar preços quando não há disponibilidade
- **Quando:** APENAS quando não encontra preços
- **Como:** Tenta sequencialmente +1, +2, +3 dias até encontrar
- **Exemplo:** Procuras 4 Nov → Sem preços → Tenta 5 Nov → Tenta 6 Nov → Encontrou!

## ⚠️ Importante

### O Que Faz:
✅ Varia a data de pesquisa aleatoriamente
✅ Torna cada request único
✅ Evita padrões de detecção
✅ Configurável nas settings

### O Que NÃO Faz:
❌ Não garante que encontra preços
❌ Não tenta múltiplas datas se falhar
❌ Não muda o número de dias de aluguer

## 🎲 Combinações Anti-Detecção

Com todas as rotações ativas:

```
Date Rotation:     0-4 dias (5 opções)
Time Rotation:     14:30-17:00 (múltiplas opções)
Device Rotation:   4 devices
Timezone Rotation: 4 timezones
Referrer Rotation: 5 referrers

Total: Milhares de combinações únicas!
```

## 🧪 Testar

1. Ativa Date Rotation nas settings
2. Define Max Days Ahead (ex: 4)
3. Faz uma pesquisa no Automated Prices
4. Olha para os logs do servidor:
   ```bash
   tail -f server.log | grep DATE_ROTATION
   ```

Vais ver:
```
[DATE_ROTATION] Original: 2025-11-04, Rotated: 2025-11-07 (+3 days)
[DATE_ROTATION] Original: 2025-11-05, Rotated: 2025-11-05 (+0 days)
[DATE_ROTATION] Original: 2025-11-06, Rotated: 2025-11-08 (+2 days)
```

## ✅ Status

- ✅ Implementado no `/api/track-by-params`
- ✅ Configurável nas settings
- ✅ Logs visíveis no terminal
- ✅ Funciona com `selenium_simple.py`
- ✅ Compatível com Alternative Search

**Tudo pronto e funcionando!** 🚀
