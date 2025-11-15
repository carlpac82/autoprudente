# ⏰ WhatsApp: Janela de 24 Horas

## 🚨 Erro Detectado

Você recebeu este erro:

```
Error 131047: Re-engagement message
"Message failed to send because more than 24 hours have passed 
since the customer last replied to this number."
```

---

## 📋 O Que É a Janela de 24 Horas?

### Regra do WhatsApp Business API

O WhatsApp Business API tem uma **limitação importante**:

> **Você só pode enviar mensagens NORMAIS (texto livre) dentro de 24 horas após a última resposta do cliente.**

### Timeline Exemplo

```
Dia 1 - 10:00 → Cliente envia mensagem
Dia 1 - 10:05 → ✅ Você pode responder (dentro de 24h)
Dia 1 - 14:30 → ✅ Você pode responder (dentro de 24h)
Dia 2 - 09:00 → ✅ Você pode responder (dentro de 24h)
Dia 2 - 10:01 → ❌ JANELA FECHOU! (passou 24h01min)
```

### O Que Acontece Após 24h?

| Ação | Resultado |
|------|-----------|
| Enviar mensagem normal | ❌ **FALHA** com erro 131047 |
| Enviar template aprovado | ✅ **FUNCIONA** |
| Cliente responde | ✅ **Reabre janela** por mais 24h |

---

## ✅ Como Resolver

### Solução 1: Aguardar Cliente Responder

**Mais simples:**
- Aguarde o cliente enviar uma mensagem
- Quando ele responder → janela reabre por 24h
- Você pode enviar mensagens normais novamente

### Solução 2: Usar Template Aprovado (Recomendado)

**Para re-engajar cliente:**

#### Passo 1: Criar Template
```
Admin → WhatsApp Settings → Templates → + Criar Template

Nome: boas_vindas_retorno
Categoria: UTILITY
Conteúdo: Olá! Tem alguma dúvida sobre sua reserva?
```

#### Passo 2: Aguardar Aprovação
- WhatsApp revisa template
- Aprovação em até 24 horas
- Receberá notificação

#### Passo 3: Usar Template
```
WhatsApp Dashboard → Conversa → Botão "Templates" → Selecionar template aprovado
```

---

## 🔍 Como Detectar Janela Expirada

### No Sistema (Agora Implementado)

**1. Na Lista de Conversas:**
```
Filipe Pacheco
⚠️ Janela de 24h expirou. Use template aprovado.
```

**2. Ao Tentar Enviar Mensagem:**
```
⚠️ ATENÇÃO: Já passaram mais de 24 horas desde a última resposta do cliente.

Mensagens normais NÃO serão entregues!

Use um TEMPLATE APROVADO para re-engajar o cliente.

Deseja continuar mesmo assim?
[Cancelar] [Continuar]
```

**3. Nos Logs do Servidor:**
```
[WHATSAPP-WEBHOOK] ❌ Message FAILED to 351925720390
[WHATSAPP-WEBHOOK] Error 131047: Re-engagement message
[WHATSAPP-WEBHOOK] 🕐 24-hour window expired for 351925720390
[WHATSAPP-WEBHOOK] 💡 User must use approved template to re-engage
```

---

## 📊 Tipos de Mensagens WhatsApp

| Tipo | Quando Usar | Requer Aprovação | Funciona Após 24h |
|------|-------------|------------------|-------------------|
| **Mensagem Normal** | Responder dentro de 24h | ❌ Não | ❌ NÃO |
| **Template** | Re-engajar após 24h | ✅ Sim | ✅ SIM |
| **Mídia (imagem/doc)** | Responder dentro de 24h | ❌ Não | ❌ NÃO |

---

## 🛠️ Criar Templates Eficazes

### Template Bom ✅

```
Nome: confirmacao_reserva
Categoria: UTILITY
Conteúdo: Olá! Sua reserva está confirmada para {{1}}. 
          Precisa de algo mais?
```

**Por quê funciona:**
- ✅ Clara e objetiva
- ✅ Relacionada ao negócio
- ✅ Variável {{1}} para personalizar
- ✅ Categoria correta (UTILITY)

### Template Ruim ❌

```
Nome: spam
Categoria: MARKETING
Conteúdo: PROMOÇÃO!!! CLIQUE AQUI!!! 🎉🎉🎉
```

**Por quê NÃO funciona:**
- ❌ Spam/marketing agressivo
- ❌ Muitos emojis/caps
- ❌ Sem valor para cliente
- ❌ WhatsApp rejeita

---

## 💡 Boas Práticas

### ✅ Fazer

1. **Responder Rápido**
   - Cliente respondeu? Responda dentro de 24h
   - Mantenha janela aberta

2. **Criar Templates Úteis**
   - Confirmação de reserva
   - Lembrete de check-in
   - Atualização de status

3. **Monitorar Tempo**
   - Ver última mensagem do cliente
   - Planejar resposta dentro de 24h

4. **Usar Sistema de Avisos**
   - Sistema mostra "⚠️ Janela de 24h expirou"
   - Não tente enviar mensagem normal

### ❌ Evitar

1. **Ignorar Avisos**
   - Sistema avisa → não ignore
   - Mensagem VAI FALHAR

2. **Spam com Templates**
   - Templates são para re-engajar
   - Não enviar templates repetidos

3. **Templates Genéricos**
   - "Olá, tudo bem?" → Rejeitado
   - Ser específico e útil

---

## 🔄 Fluxo de Re-engagement

### Cenário: Cliente Não Responde Há 3 Dias

```
Dia 1 - 10:00
├─ Cliente: "Gostaria de reservar um carro"
└─ Você: "Ótimo! Qual modelo?" ✅

Dia 1 - 14:00
├─ Cliente: [sem resposta]
└─ Janela ainda aberta (10h restantes)

Dia 2 - 10:00
├─ Cliente: [sem resposta]
└─ Janela ainda aberta (30min restantes)

Dia 2 - 10:30
├─ ⚠️ JANELA FECHOU
└─ Mensagens normais falham ❌

Dia 4 - 09:00
├─ Você quer follow-up
├─ ✅ SOLUÇÃO: Enviar template "lembrete_reserva"
└─ Template: "Olá! Ainda tem interesse na reserva?"

Dia 4 - 09:15
├─ Cliente: "Sim, quero reservar!"
├─ ✅ JANELA REABRE
└─ Você pode enviar mensagens normais por 24h
```

---

## 📞 Suporte WhatsApp API

### Documentação Oficial

- **Error Codes:** https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes/
- **Templates:** https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates/
- **Message Template Guidelines:** https://developers.facebook.com/docs/whatsapp/message-templates/guidelines

### Erro 131047 Específico

```json
{
  "code": 131047,
  "title": "Re-engagement message",
  "message": "Re-engagement message",
  "error_data": {
    "details": "Message failed to send because more than 24 hours 
                have passed since the customer last replied to this number."
  }
}
```

---

## ✅ Checklist de Resolução

Quando ver erro 131047:

- [ ] Verificar tempo desde última resposta do cliente
- [ ] Confirmar que passou >24 horas
- [ ] Decidir: aguardar resposta OU usar template
- [ ] Se usar template:
  - [ ] Verificar templates aprovados
  - [ ] Se não tem → criar e aguardar aprovação
  - [ ] Enviar template apropriado
- [ ] Cliente respondeu?
  - [ ] ✅ Janela reabre → pode usar mensagens normais
  - [ ] ❌ Ainda não → aguardar ou enviar outro template

---

## 🎯 Resumo Rápido

**A Regra de Ouro:**
> Mensagens normais = Só dentro de 24h após última resposta do cliente
> 
> Templates aprovados = Funcionam sempre

**Como Sistema Ajuda:**
- ⚠️ Mostra aviso na conversa
- 🔔 Alerta antes de enviar
- 📊 Logs detalhados

**O Que Fazer:**
1. Ver aviso "⚠️ Janela de 24h expirou"
2. Usar template aprovado
3. OU aguardar cliente responder

---

**Criado:** 2025-11-15  
**Última Atualização:** 2025-11-15  
**Versão:** 1.0
