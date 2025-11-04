# 📧 CONFIGURAÇÃO DE EMAIL - Guia Completo

**Data:** 4 de Novembro de 2025, 22:26  
**Status:** Sistema configurado com Gmail OAuth

---

## 🔍 PROBLEMA IDENTIFICADO

### Email de Teste:
- ✅ Diz "enviado com sucesso"
- ❌ Não recebe email
- ❌ Erro não é mostrado ao utilizador

### Causa:
1. **SMTP não configurado:** Configurações SMTP vazias na BD
2. **Erro silencioso:** Função retornava sem lançar exceção
3. **Gmail OAuth:** Sistema usa Gmail API, não SMTP tradicional

---

## 📊 DOIS SISTEMAS DE EMAIL

### 1. SMTP Tradicional (Para emails de credenciais)

**Usado em:**
- Envio de credenciais para novos utilizadores
- Emails administrativos simples

**Configuração necessária:**
```
Settings → Admin Settings:
- SMTP Host: smtp.gmail.com
- SMTP Port: 587
- SMTP Username: seu-email@gmail.com
- SMTP Password: senha-de-app-gmail
- SMTP From: seu-email@gmail.com
- SMTP TLS: ✅ Ativado
```

**Como obter senha de app Gmail:**
1. Vai a https://myaccount.google.com/security
2. Ativa verificação em 2 passos
3. Vai a "Senhas de app"
4. Gera senha para "Mail"
5. Usa essa senha no SMTP Password

---

### 2. Gmail OAuth (Para relatórios automáticos)

**Usado em:**
- Relatórios diários
- Relatórios semanais
- Alertas de preços

**Configuração:**
1. Vai a Settings → Email Configuration
2. Clica "Connect Gmail Account"
3. Autoriza acesso
4. ✅ Token guardado automaticamente

**Email hardcoded:**
```python
test_email = "carlpac82@hotmail.com"  # Linha 13633
```

**Para mudar:**
- Editar `main.py` linha 13633
- Ou adicionar campo no frontend

---

## ✅ CORREÇÕES IMPLEMENTADAS

### 1. Melhor Tratamento de Erros:

**Antes:**
```python
if not host or not to_email:
    return  # Silencioso!
```

**Depois:**
```python
if not host or not to_email:
    error_msg = f"Missing SMTP configuration: host={bool(host)}, to_email={bool(to_email)}"
    raise Exception(error_msg)  # Mostra erro!
```

### 2. Detalhes do Erro:

**Antes:**
```python
except Exception as e:
    # Escreve ficheiro mas não mostra
    pass
```

**Depois:**
```python
except Exception as e:
    error_details = f"{type(e).__name__}: {e}\nHost: {host}\nPort: {port}..."
    raise  # Re-lança para mostrar ao utilizador
```

---

## 🎯 COMO CONFIGURAR

### Passo 1: Configurar SMTP (Render)

1. **Acede ao Render:**
   - https://carrental-api-5f8q.onrender.com/

2. **Vai a Settings → Admin Settings**

3. **Preenche configurações SMTP:**
   ```
   SMTP Host: smtp.gmail.com
   SMTP Port: 587
   SMTP Username: comercial.autoprudente@gmail.com
   SMTP Password: [senha de app - ver abaixo]
   SMTP From: comercial.autoprudente@gmail.com
   SMTP TLS: ✅
   ```

4. **Guarda**

---

### Passo 2: Obter Senha de App Gmail

1. **Vai a Google Account:**
   - https://myaccount.google.com/security

2. **Ativa verificação em 2 passos:**
   - Se ainda não estiver ativa

3. **Vai a "Senhas de app":**
   - Procura "App passwords" ou "Senhas de app"

4. **Gera nova senha:**
   - App: Mail
   - Device: Render
   - Copia a senha gerada (16 caracteres)

5. **Cola no SMTP Password**

---

### Passo 3: Conectar Gmail OAuth (Render)

1. **Vai a Settings → Email Configuration**

2. **Clica "Connect Gmail Account"**

3. **Autoriza acesso:**
   - Seleciona conta Gmail
   - Permite envio de emails

4. **✅ Token guardado automaticamente**

---

### Passo 4: Testar

#### Teste SMTP:
1. Vai a Admin → Test Email
2. Insere teu email
3. Envia
4. ✅ Deve receber email de teste

#### Teste Relatórios:
1. Vai a Settings → Automated Reports
2. Clica "Send Test Daily Report"
3. ✅ Deve receber em carlpac82@hotmail.com

---

## 📊 RELATÓRIOS AUTOMÁTICOS

### Como Funcionam:

**Relatórios Diários:**
- Enviados às 09h00 (configurável)
- Inclui comparação de preços
- Alertas de mudanças significativas
- Gráficos e estatísticas

**Relatórios Semanais:**
- Enviados às segundas-feiras
- Resumo da semana
- Tendências de preços
- Análise de competitividade

---

### Dados Incluídos:

**Relatório Diário:**
```
✅ Preços atualizados (Faro, Albufeira)
✅ Comparação com dia anterior
✅ Alertas de mudanças >10%
✅ Carros mais baratos/caros
✅ Disponibilidade por grupo
```

**Relatório Semanal:**
```
✅ Resumo de 7 dias
✅ Tendências de preços
✅ Análise de competitividade
✅ Recomendações de ajuste
✅ Performance por grupo
```

---

### Verificar se Geram Dados:

**Endpoint de teste:**
```bash
POST /api/reports/test-daily
{
  "accessToken": "..."
}
```

**Resposta esperada:**
```json
{
  "ok": true,
  "message": "Email enviado com sucesso!",
  "messageId": "..."
}
```

**Email recebido deve conter:**
- ✅ Header com logo
- ✅ Data atual
- ✅ Mensagem de teste
- ✅ Próximos passos
- ✅ Footer com copyright

---

## 🔧 TROUBLESHOOTING

### Problema: "Email enviado" mas não recebe

**Causa 1: SMTP não configurado**
- Verifica Settings → Admin Settings
- Preenche todas as configurações SMTP
- Testa novamente

**Causa 2: Senha de app incorreta**
- Gera nova senha de app no Gmail
- Atualiza SMTP Password
- Testa novamente

**Causa 3: Gmail OAuth não conectado**
- Vai a Settings → Email Configuration
- Conecta conta Gmail
- Autoriza acesso
- Testa relatórios

**Causa 4: Email na spam**
- Verifica pasta spam/lixo
- Adiciona remetente aos contactos
- Marca como "não é spam"

---

### Problema: Erro ao enviar

**Erro: "Missing SMTP configuration"**
- ✅ Configurações SMTP vazias
- ✅ Preenche em Settings → Admin Settings

**Erro: "Authentication failed"**
- ✅ Senha de app incorreta
- ✅ Gera nova senha de app
- ✅ Verifica username correto

**Erro: "Connection refused"**
- ✅ Porta incorreta (deve ser 587)
- ✅ TLS deve estar ativado
- ✅ Firewall pode estar a bloquear

**Erro: "Token OAuth não encontrado"**
- ✅ Gmail OAuth não conectado
- ✅ Conecta em Settings → Email Configuration

---

## 📝 CHECKLIST

### Configuração SMTP:
- [ ] SMTP Host configurado
- [ ] SMTP Port = 587
- [ ] SMTP Username = email Gmail
- [ ] SMTP Password = senha de app (16 chars)
- [ ] SMTP From = email Gmail
- [ ] SMTP TLS = ✅ Ativado
- [ ] Teste enviado com sucesso
- [ ] Email recebido

### Configuração Gmail OAuth:
- [ ] Conta Gmail conectada
- [ ] Token OAuth guardado
- [ ] Teste de relatório enviado
- [ ] Email recebido em carlpac82@hotmail.com

### Relatórios Automáticos:
- [ ] Horário configurado (09h00)
- [ ] Email de destino correto
- [ ] Relatórios diários ativados
- [ ] Relatórios semanais ativados
- [ ] Testes funcionando

---

## 🎯 PRÓXIMOS PASSOS

1. **Configurar SMTP no Render:**
   - Preencher todas as configurações
   - Obter senha de app Gmail
   - Testar envio

2. **Conectar Gmail OAuth:**
   - Autorizar acesso
   - Testar relatórios

3. **Ativar relatórios automáticos:**
   - Configurar horários
   - Verificar emails recebidos

4. **Monitorizar:**
   - Verificar logs
   - Confirmar recepção
   - Ajustar se necessário

---

## 📧 EMAILS DE DESTINO

### ✅ Sistema Automático (Implementado):

**Relatórios usam destinatários das Notification Rules!**

```python
# Busca destinatários ativos
SELECT DISTINCT recipient FROM notification_rules 
WHERE enabled = 1 AND notification_type = 'email'
```

**Prioridade:**
1. 🥇 Destinatários das Notification Rules (ativas)
2. 🥈 Configuração `report_email` na BD
3. 🥉 Email padrão: carlpac82@hotmail.com

### Como Configurar:

**Opção 1: Via Notification Rules (Recomendado)**
```
1. Settings → Notifications
2. Adiciona nova regra
3. Tipo: Email
4. Destinatário: teu-email@example.com
5. Ativa regra
6. ✅ Relatórios vão para esse email!
```

**Opção 2: Via Configuração**
```
1. Settings → Admin Settings
2. Adiciona: report_email = teu-email@example.com
3. Guarda
4. ✅ Usado se não houver notification rules
```

**Múltiplos Destinatários:**
- Cria múltiplas notification rules
- Cada uma com email diferente
- Todas ativas
- ✅ Relatórios enviados para todos!

---

**IMPORTANTE:** Todas as configurações devem ser feitas no **RENDER**, não no local!

**Lembra-te:** Workflow correto = Código no Windsurf, Configurações no Render! ✅
