# 📱 Guia de Setup - WhatsApp Business API

## ⚠️ IMPORTANTE: Passos QUE TU PRECISAS DE FAZER

### Passo 1: Criar Meta Business Account (5-10 min)

1. **Vai a:** https://business.facebook.com/
2. **Clica em:** "Criar Conta"
3. **Preenche:**
   - Nome do negócio: "Auto Prudente"
   - Teu nome
   - Email comercial
4. **Confirma** o email

---

### Passo 2: Criar App no Meta for Developers (10 min)

1. **Vai a:** https://developers.facebook.com/
2. **Clica:** "My Apps" → "Create App"
3. **Seleciona:** "Business" como tipo de app
4. **Preenche:**
   - App Name: "AutoPrudente WhatsApp"
   - Contact Email: teu email
   - Business Account: seleciona "Auto Prudente" (criado no Passo 1)
5. **Clica:** "Create App"

---

### Passo 3: Adicionar WhatsApp Product

1. **No dashboard da app**, procura "WhatsApp" nos produtos
2. **Clica:** "Set Up" no WhatsApp
3. **Seleciona** ou cria um Meta Business Account
4. **Clica:** "Continue"

---

### Passo 4: Configurar Número de Telefone

#### Opção A: Usar Número de Teste (para desenvolvimento)
1. Meta fornece um número de teste automaticamente
2. Podes testar com até 5 números que registares
3. **USE ISTO PRIMEIRO PARA TESTAR**

#### Opção B: Adicionar Teu Número Real (produção)
1. **Clica:** "Add Phone Number"
2. **Seleciona:** País (Portugal +351)
3. **Insere:** O número que está no WhatsApp Business App
4. **⚠️ IMPORTANTE:** Vais receber um código por SMS
5. **ANTES de inserir o código:** 
   - Faz backup das conversas do WhatsApp Business App
   - Desinstala WhatsApp Business App do telemóvel
   - **Só depois insere o código de verificação**
6. O número fica associado à API

---

### Passo 5: Obter Credenciais (GUARDAR BEM!)

Depois de configurar, precisas de copiar:

1. **Access Token** (temporário, para testes)
   - No dashboard do WhatsApp Product
   - Copia e guarda num ficheiro seguro
   
2. **Phone Number ID**
   - Aparece ao lado do número configurado
   - Copia e guarda
   
3. **WhatsApp Business Account ID**
   - No topo da página do WhatsApp Product
   - Copia e guarda

4. **App ID** e **App Secret**
   - Settings → Basic
   - Copia ambos e guarda

---

### Passo 6: Gerar Permanent Access Token (OBRIGATÓRIO)

O token temporário expira em 24h. Precisas de um permanente:

1. **Vai a:** Settings → Basic (da tua app)
2. **Copia:** App ID e App Secret
3. **Vai a:** https://developers.facebook.com/tools/explorer/
4. **Seleciona:** A tua app
5. **User Token:** Clica "Generate Access Token"
6. **Permissões necessárias:**
   - `whatsapp_business_messaging`
   - `whatsapp_business_management`
7. **Gera** o token e guarda num local SEGURO

---

### Passo 7: Configurar Webhook (EU FAÇO DEPOIS)

Isto vai permitir receber mensagens dos clientes em tempo real.
Precisas de me dar:
- Access Token permanente
- Phone Number ID
- WhatsApp Business Account ID

**Eu vou configurar o webhook no servidor.**

---

## 📋 Checklist Final

Depois de fazeres tudo, deves ter:

- [ ] Meta Business Account criada
- [ ] App criada no Meta for Developers
- [ ] WhatsApp Product adicionado à app
- [ ] Número de telefone configurado (teste OU real)
- [ ] **Access Token Permanente** (guardado)
- [ ] **Phone Number ID** (guardado)
- [ ] **WhatsApp Business Account ID** (guardado)
- [ ] **App ID** (guardado)
- [ ] **App Secret** (guardado)

---

## ⚠️ NOTAS IMPORTANTES

### Quando Migrar o Número Real:

1. **Faz backup** de todas as conversas importantes do WhatsApp Business App
2. **Avisa os clientes** que o atendimento vai melhorar (agora com sistema web)
3. **Desinstala** WhatsApp Business App ANTES de verificar o número na API
4. **Nunca mais** poderás usar esse número no WhatsApp Business App
5. Todo o atendimento passa para o **dashboard web** que vou criar

### Período de Teste:

- **USA O NÚMERO DE TESTE PRIMEIRO** durante alguns dias
- Testa o sistema completo antes de migrar o número real
- Assim não corres riscos

---

## 🆘 Precisa de Ajuda?

Se tiveres dificuldades em algum passo, avisa que eu ajudo!

---

## 🚀 Próximo Passo

**Depois de teres as credenciais**, cria um ficheiro `.env` na pasta do projeto:

```bash
WHATSAPP_ACCESS_TOKEN=your_permanent_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_id_here
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id_here
WHATSAPP_APP_ID=your_app_id_here
WHATSAPP_APP_SECRET=your_app_secret_here
WHATSAPP_VERIFY_TOKEN=meu_token_secreto_123  # Cria uma password qualquer
```

**NUNCA partilhes estas credenciais publicamente!**
