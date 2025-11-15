# 📞 WhatsApp: Contactos vs Conversas

## 🔍 DIFERENÇA IMPORTANTE

### 👤 CONTACTO
- **Permanente** - não é apagado
- Armazenado na tabela `whatsapp_contacts`
- Contém: nome, telefone, foto perfil
- Pode ter MÚLTIPLAS conversas ao longo do tempo

### 💬 CONVERSA  
- **Temporária** - pode ser apagada
- Armazenada na tabela `whatsapp_conversations`
- Contém: mensagens, histórico, status
- Está LIGADA a um contacto

---

## ✅ COMPORTAMENTO CORRETO

### Apagar CONVERSA:
```
✅ Apaga mensagens
✅ Apaga histórico da conversa
✅ MANTÉM o contacto
```

Depois de apagar conversa:
- Contacto permanece na lista
- Pode iniciar NOVA conversa com o mesmo contacto
- Histórico anterior desaparece

### Apagar CONTACTO:
```
❌ Apaga contacto
❌ Apaga TODAS as conversas deste contacto
❌ Apaga todas as mensagens
```

Depois de apagar contacto:
- Contacto desaparece completamente
- Todas as conversas são apagadas
- Para falar novamente = criar novo contacto

---

## 🐛 PROBLEMA ATUAL

O sistema está **CONFUNDINDO** contactos com conversas!

**O que acontece agora (ERRADO):**
1. Apaga conversa
2. Contacto também desaparece ❌

**O que deveria acontecer (CORRETO):**
1. Apaga conversa
2. Contacto permanece ✅
3. Pode criar nova conversa com o mesmo contacto

---

## 🔧 CORREÇÃO IMPLEMENTADA

### Backend (`main.py`):
✅ Endpoint `/api/whatsapp/conversations/{id}` - apaga APENAS conversa
✅ Contacto permanece intacto
✅ Mensagem de confirmação clara

### Próximo Passo:
⏳ Garantir que sistema usa corretamente a tabela `whatsapp_contacts`
⏳ Separar lógica de contactos e conversas no frontend

---

## 📊 ESTRUTURA DE DADOS

```
whatsapp_contacts (PERMANENTE)
├── id
├── name
├── phone_number
├── has_whatsapp
└── profile_picture_url

whatsapp_conversations (TEMPORÁRIA)
├── id
├── contact_id  →  whatsapp_contacts.id
├── phone_number
├── last_message_at
└── status

whatsapp_messages (TEMPORÁRIA)
├── id
├── conversation_id  →  whatsapp_conversations.id
├── message_text
└── timestamp
```

---

## 💡 CASOS DE USO

### Caso 1: Cliente irritado - quero apagar conversa
```
Ação: Apagar conversa
Resultado: ✅ Histórico limpo, contacto mantido
Benefício: Pode recomeçar com historial limpo
```

### Caso 2: Número errado - não quero mais contato
```
Ação: Apagar contacto
Resultado: ✅ Tudo apagado (contacto + conversas)
Benefício: Cleanup completo
```

### Caso 3: Reserva concluída - limpar chat
```
Ação: Apagar conversa (não contacto!)
Resultado: ✅ Cliente permanece para futuras reservas
Benefício: Histórico limpo, cliente pode voltar
```

---

## ⚠️ ATENÇÃO

**ANTES desta correção:**
- Apagar conversa = apaga contacto (ERRADO)

**DEPOIS desta correção:**
- Apagar conversa = mantém contacto (CORRETO)

**Deploy necessário para aplicar correção!**
