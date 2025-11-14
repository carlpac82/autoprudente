# 🚀 WhatsApp - Próximos Passos

## ✅ TUDO PRONTO! Agora é só configurar:

---

## 📋 Passo 1: Configurar no Admin Panel

1. **Vai a:** https://carrental-api-5f8q.onrender.com/admin/whatsapp
2. **Tab:** "Conexão Facebook"
3. **Preenche:**
   ```
   Access Token: EAAMQ6ZCiEI6oBP5sEnShZC340UpLPLZCksvZAxVpGRopNB3VRoqV3DR3S25PJlhnEZCSpsMcpZBmW4v9RzZANGWbSzHUnfAzm24z252MZBbbPMZApbmQtT7AyqLP9YPqt9sZAcGZCgPMo7mfvtCpGB2FSBPDZB0Tjnn5qtkDvPOFdhAWIJL3cGE7ZBwxRpPG5cVualEFY5NwMqyu1gzl3bdXTRNQdqHZCLrQ3TOEKnQDtomLRKF4vBTQZDZD
   
   Phone Number ID: 929618760228345
   
   Business Account ID: 187665584329030
   
   Webhook Verify Token: Prudente.2025
   ```
4. **Clica:** "Guardar Configurações" (botão azul)
5. **Testa:** Clica "Testar Conexão" (botão verde)

---

## 🔗 Passo 2: Registar Webhook no Meta

1. **Volta ao Meta for Developers:** https://developers.facebook.com/apps
2. **Seleciona tua app:** "AutoPrudente WhatsApp"
3. **WhatsApp → Configuration → Webhook**
4. **Clica:** "Edit" ou "Configure Webhook"
5. **Preenche:**
   ```
   Callback URL: https://carrental-api-5f8q.onrender.com/api/whatsapp/webhook
   
   Verify Token: Prudente.2025
   ```
6. **Clica:** "Verify and Save"
7. **Subscribe to:** 
   - ✅ messages
   - ✅ messaging_postbacks (opcional)
8. **Save**

---

## 🧪 Passo 3: Testar o Sistema

### Teste com Número de Teste:

1. **Adiciona teu número** aos números de teste no Meta:
   - WhatsApp → API Setup → "To"
   - Add recipient phone number
   - Insere teu número (+351...)
   
2. **Envia mensagem** do teu WhatsApp para: **+1 555 176 6396**

3. **Verifica logs** do Render:
   - https://dashboard.render.com/web/carrental-api-5f8q/logs
   - Procura por: `[WHATSAPP]` ou `webhook received`

4. **Sistema deve:**
   - ✅ Receber a mensagem
   - ✅ Processar e guardar
   - ✅ (Opcional) Responder automaticamente

---

## 📊 Passo 4: Monitorizar

**Render Logs:**
https://dashboard.render.com/web/carrental-api-5f8q/logs

**Meta Dashboard:**
https://developers.facebook.com/apps → Tua App → WhatsApp → Insights

**Admin Panel:**
https://carrental-api-5f8q.onrender.com/admin/whatsapp

---

## 🎯 Funcionalidades Disponíveis (após configurar):

### ✅ JÁ IMPLEMENTADO:
- Receber mensagens via webhook
- Guardar configurações no PostgreSQL
- Admin panel para gestão
- Quick Replies (respostas rápidas)
- Templates management
- Automações

### 🔄 A DESENVOLVER (se quiseres):
- Enviar mensagens automáticas
- Chatbot com respostas inteligentes
- Integração com sistema de reservas
- Notificações de novos carros
- Follow-up de clientes

---

## ⚠️ NOTAS IMPORTANTES

### Limitações do Número de Teste:
- ✅ Funciona para testar (90 dias grátis)
- ✅ Até 5 números de destinatários
- ❌ Clientes reais NÃO podem enviar mensagens

### Quando Migrar para Número Real:
- Segue instruções do `WHATSAPP_SETUP_GUIDE.md`
- Faz backup do WhatsApp Business App
- Desinstala app ANTES de verificar na API

---

## 🔐 Segurança

**NUNCA:**
- Partilhar Access Token publicamente
- Fazer commit das credenciais no Git
- Dar acesso ao Admin Panel a utilizadores não confiáveis

**SEMPRE:**
- Usar HTTPS (já configurado)
- Verificar Webhook Verify Token
- Monitorizar logs de acesso

---

## 📞 Suporte

Se tiveres problemas:
1. Verifica logs do Render
2. Testa conexão no Admin Panel
3. Verifica webhook no Meta está "Connected"
4. Consulta docs oficiais: https://developers.facebook.com/docs/whatsapp

---

**✅ TUDO CONFIGURADO! Bom trabalho! 🎉**
