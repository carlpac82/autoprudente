# 📋 PLANO DE TESTES - SEPARAÇÃO CONTACTOS/CONVERSAS

## ✅ IMPLEMENTAÇÃO COMPLETADA

### Backend - Endpoints Atualizados

1. **POST /api/admin/whatsapp/migrate-contacts** ✓
   - Migra conversas existentes para tabela whatsapp_contacts
   - Cria contactos se não existirem
   - Liga conversas aos contactos via contact_id

2. **POST /api/whatsapp/webhook** ✓
   - SEMPRE cria/atualiza contacto antes de criar conversa
   - Garante contact_id em todas as novas conversas

3. **POST /api/whatsapp/contacts/add** ✓
   - Cria contacto PRIMEIRO em whatsapp_contacts
   - Depois cria conversa ligada ao contacto

4. **GET /api/whatsapp/conversations** ✓
   - JOIN com whatsapp_contacts
   - Retorna dados do contacto (nome, foto, etc.)
   - Usa nome do contacto como display_name

5. **GET /api/whatsapp/contacts** ✓
   - Novo endpoint para listar contactos
   - Inclui conversation_count para cada contacto
   - Ordenado por created_at DESC

6. **POST /api/whatsapp/send-message** ✓
   - Cria contacto se não existir antes de enviar
   - Atualiza contact_id na conversa

7. **POST /api/whatsapp/send-template** ✓
   - Cria contacto se não existir antes de enviar
   - Atualiza contact_id na conversa

8. **POST /api/whatsapp/send-media** ✓
   - Já estava correto, valida phone_number do form-data

9. **DELETE /api/whatsapp/conversations/{id}** ✓
   - Apaga APENAS conversa + mensagens
   - MANTÉM contacto intacto

10. **DELETE /api/whatsapp/contacts/{id}** ✓
    - Apaga contacto + TODAS conversas + mensagens
    - Usa contact_id para encontrar conversas associadas

### Frontend - Funções Atualizadas

1. **loadContacts()** ✓
   - Chama GET /api/whatsapp/contacts
   - Mostra lista separada de contactos

2. **renderContacts()** ✓
   - Mostra conversation_count em vez de unread_count
   - Remove onclick para abrir conversa (contactos ≠ conversas)
   - Tooltip correto no botão delete

3. **deleteContact()** ✓
   - Confirmação clara: apaga contacto + TODAS conversas
   - Recarrega ambas as listas após delete

4. **deleteConversation()** ✓
   - Confirmação clara: apaga conversa, MANTÉM contacto
   - Recarrega lista de conversas

5. **submitAddContact()** ✓
   - Recarrega AMBAS listas (contacts + conversations)
   - Aguarda commit da BD

---

## 🧪 TESTES A EXECUTAR

### Teste 1: Migração de Dados
```bash
# Executar migração
curl -X POST http://localhost:8000/api/admin/whatsapp/migrate-contacts \
  -H "Cookie: session_token=SEU_TOKEN"
```

**Validar:**
- ✅ Todos os números em whatsapp_conversations foram migrados para whatsapp_contacts
- ✅ Campo contact_id foi preenchido em todas as conversas
- ✅ Logs mostram contactos criados

---

### Teste 2: Receber Mensagem (Webhook)
**Simular:** Cliente envia mensagem via WhatsApp

**Validar:**
- ✅ Contacto criado/atualizado em whatsapp_contacts
- ✅ Conversa criada com contact_id correto
- ✅ Mensagem registrada

---

### Teste 3: Adicionar Contacto Novo
**Ação:** Usar interface "Adicionar Contacto"

**Validar:**
- ✅ Contacto criado em whatsapp_contacts
- ✅ Conversa criada ligada ao contacto
- ✅ Ambos os tabs (Conversas + Contactos) atualizam

---

### Teste 4: Apagar Conversa (Manter Contacto)
**Ação:** Clicar lixo no chat de uma conversa

**Validar:**
- ✅ Conversa e mensagens apagadas
- ✅ Contacto MANTIDO em whatsapp_contacts
- ✅ Contacto continua visível no tab Contactos
- ✅ Mensagem de confirmação correta

---

### Teste 5: Apagar Contacto (Apagar Todas Conversas)
**Ação:** Clicar lixo no tab Contactos

**Validar:**
- ✅ Contacto apagado
- ✅ TODAS conversas do contacto apagadas
- ✅ TODAS mensagens apagadas
- ✅ Mensagem de confirmação correta mostrando número de conversas apagadas

---

### Teste 6: Enviar Template
**Ação:** Enviar template check-in para cliente

**Validar:**
- ✅ Se contacto não existir, é criado
- ✅ Template enviado com sucesso
- ✅ Mensagem registrada na conversa

---

### Teste 7: Enviar Media
**Ação:** Enviar imagem/documento via WhatsApp

**Validar:**
- ✅ Media enviado sem erro "parameter to is required"
- ✅ phone_number corretamente extraído da conversa

---

### Teste 8: Listar Contactos
**Ação:** Abrir tab "Contactos"

**Validar:**
- ✅ Lista carrega de GET /api/whatsapp/contacts
- ✅ Mostra conversation_count correto
- ✅ Mostra nome, telefone, foto de perfil
- ✅ Aviso ⚠️ se has_whatsapp = false

---

### Teste 9: Listar Conversas
**Ação:** Abrir tab "Conversas"

**Validar:**
- ✅ Lista carrega de GET /api/whatsapp/conversations
- ✅ Mostra nome do contacto (via JOIN)
- ✅ Mostra foto do contacto
- ✅ Mostra preview última mensagem
- ✅ Mostra unread_count

---

## 📊 ESTRUTURA FINAL

### Tabela: whatsapp_contacts
```
id | name | phone_number | has_whatsapp | profile_picture_url | created_at
```

### Tabela: whatsapp_conversations
```
id | contact_id (FK) | phone_number | last_message_at | last_message_preview | 
unread_count | status | assigned_to | created_at
```

### Tabela: whatsapp_messages
```
id | conversation_id (FK) | message_text | direction | timestamp | 
status | sender_name | media_url
```

---

## 🎯 REGRAS DE NEGÓCIO

1. **Contacto ≠ Conversa**
   - Um contacto pode ter VÁRIAS conversas
   - Uma conversa pertence a UM contacto

2. **Delete Conversa**
   - Apaga: conversa + mensagens
   - Mantém: contacto

3. **Delete Contacto**
   - Apaga: contacto + TODAS conversas + mensagens

4. **Webhook**
   - SEMPRE cria/atualiza contacto primeiro
   - Depois cria/atualiza conversa

5. **Enviar Mensagem**
   - Se contacto não existe, cria
   - Se conversa não existe, cria
   - Liga conversa ao contacto

---

## ⏱️ TEMPO ESTIMADO DE TESTES: 20 minutos

## 🚀 PRÓXIMOS PASSOS

1. ✅ Executar migração
2. ✅ Reiniciar servidor
3. ✅ Executar testes 1-9
4. ✅ Validar logs
5. ✅ Confirmar correção dos bugs originais
