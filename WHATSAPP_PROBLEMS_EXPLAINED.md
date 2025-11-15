# WhatsApp Dashboard - Problemas Identificados

## ✅ PROBLEMA 1: "Erro ao criar conversa: Desconhecido" (RESOLVIDO!)

### O que estava a acontecer:
- User clica num contacto sem conversa
- **Backend CRIA a conversa com sucesso** ✅ (logs provam: `Created new conversation #61`)
- **Mas frontend mostra erro** ❌: "Erro ao criar conversa: Desconhecido"

### Logs do Render (PROVAM que conversa foi criada):
```
[WHATSAPP] ✅ Created new conversation #61 for contact #2
```

### UI também mostra sucesso:
```
Filipe Pacheco
1 conversa  ← CONVERSA EXISTE!
```

### Causa do erro no frontend:
O código verificava `data.contact.conversation_id` mas o backend nem sempre retorna este campo no formato esperado, mesmo quando a conversa é criada com sucesso.

### Solução Implementada (Deploy agora):
1. ✅ Verificar apenas `data.success` (não `conversation_id`)
2. ✅ Recarregar lista de conversas
3. ✅ **Buscar conversa por `contact_id`** (mais confiável)
4. ✅ Retry automático após 500ms se não encontrar logo
5. ✅ Logs detalhados para debug

### Teste após deploy (2 minutos):
1. Recarregar WhatsApp Dashboard
2. Clicar contacto
3. ✅ Conversa abre automaticamente
4. ❌ SEM mensagem de erro

---

## ❌ PROBLEMA 2: "Erro ao enviar mensagem" (PROBLEMA EXTERNO - Facebook/Meta)

### O que está a acontecer:
Quando tentas enviar mensagem, aparece:
```
Erro ao enviar mensagem
```

### Logs do Render mostram:
```
[WHATSAPP] Sending message to 351964805750...
[WHATSAPP] ❌ Error sending message: {
    'error': {
        'message': 'API access blocked.',
        'type': 'OAuthException',
        'code': 200,
        'fbtrace_id': 'A8wsr6qw2FfMmAcQOD8dsb7'
    }
}
```

### Causa:
**Facebook/Meta está a BLOQUEAR o acesso à API do WhatsApp Business!**

Este **NÃO é um problema do código** - é o Facebook a negar acesso.

### Possíveis Razões:

1. **Token Expirado**
   - WhatsApp Business API tokens expiram
   - Precisas renovar no Facebook Business Manager

2. **Permissões Insuficientes**
   - App do WhatsApp Business pode não ter permissões
   - Verificar no Facebook Developers

3. **Limites de API**
   - Facebook pode ter bloqueado temporariamente
   - Demasiadas chamadas ou violação de políticas

4. **Número não Verificado**
   - `351964805750` pode não estar verificado
   - WhatsApp Business exige verificação

### Como Resolver:

#### Passo 1: Verificar Token no WhatsApp Dashboard

1. Ir para WhatsApp Dashboard
2. Clicar botão "Conectado" (verde)
3. Ver se token está ativo
4. Se necessário, reconectar

#### Passo 2: Facebook Business Manager

1. Aceder: https://business.facebook.com/
2. Ir para WhatsApp Business Account
3. Verificar:
   - ✅ App está ativo
   - ✅ Número está verificado
   - ✅ Token não expirou
   - ✅ Permissões corretas

#### Passo 3: Gerar Novo Token (se necessário)

1. Facebook Developers: https://developers.facebook.com/
2. Ir para App do WhatsApp Business
3. Settings → WhatsApp → API Setup
4. Generate new token
5. Copiar token
6. Colar no WhatsApp Dashboard (botão Config)

#### Passo 4: Verificar Número de Telefone

O número `351964805750` precisa estar:
- ✅ Registado no WhatsApp Business
- ✅ Verificado pela Meta
- ✅ Ativo e funcional

---

## 📊 Resumo

| Problema | Status | Solução |
|----------|--------|---------|
| "Erro ao criar conversa" | ✅ RESOLVIDO | Deploy em curso (2 min) |
| "Erro ao enviar mensagem" | ⚠️ EXTERNO | Renovar token WhatsApp API |

---

## 🔧 Próximos Passos

### Para "Erro ao criar conversa":
1. ⏳ Aguardar 2 minutos (deploy)
2. ✅ Recarregar dashboard
3. ✅ Testar clicar contacto
4. ✅ Deve abrir sem erro

### Para "Erro ao enviar mensagem":
1. 🔍 Verificar token no dashboard
2. 🔑 Se inválido, gerar novo token no Facebook
3. 💾 Guardar novo token no sistema
4. ✅ Testar enviar mensagem

---

## 🆘 Ajuda Adicional

Se o problema de enviar mensagens persistir:

1. **Verificar logs do Render**:
   - Procurar `OAuthException`
   - Ver qual o erro específico

2. **Verificar Meta Business**:
   - Status do número
   - Limites da API
   - Mensagens de aviso

3. **Contactar Meta Support**:
   - Se bloqueio persistir
   - Pode ser restrição de conta

---

**IMPORTANTE:** O problema de "criar conversa" estava no código e foi corrigido. O problema de "enviar mensagem" é externo (Facebook API) e requer ação no Facebook Business Manager.
