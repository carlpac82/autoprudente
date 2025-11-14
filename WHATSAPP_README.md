# 📱 WhatsApp Integration - Auto Prudente

Sistema completo de integração WhatsApp Business API para atendimento via website.

## ✅ O Que Foi Implementado

### Backend
- ✅ **WhatsApp Client** (`whatsapp_client.py`)
  - Enviar mensagens de texto
  - Enviar imagens e documentos
  - Enviar templates aprovados
  - Enviar localização
  - Marcar mensagens como lidas
  
- ✅ **API Endpoints** (`whatsapp_api.py`)
  - Webhook para receber mensagens
  - Endpoints para enviar mensagens
  - Gestão de conversas
  - Quick replies (respostas rápidas)
  - Logs de eventos

- ✅ **Database Schema** (`database_whatsapp.sql`)
  - Tabela de contactos
  - Tabela de conversas
  - Tabela de mensagens
  - Tabela de templates
  - Tabela de quick replies
  - Tabela de configurações
  - Tabela de logs

### Frontend
- ✅ **Dashboard WhatsApp** (`templates/whatsapp_dashboard.html`)
  - Lista de conversas em tempo real
  - Chat interface
  - Envio de mensagens
  - Filtros de status
  - Respostas rápidas
  - Templates

## 🚀 Setup - Passos para Configurar

### 1. Database Setup

Execute o script SQL para criar as tabelas:

```bash
psql -U your_username -d your_database -f database_whatsapp.sql
```

Ou via Python no servidor Render:
```python
import asyncpg
async def setup_db():
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    with open('database_whatsapp.sql', 'r') as f:
        await conn.execute(f.read())
    await conn.close()
```

### 2. WhatsApp Cloud API Setup

Segue o guia em `WHATSAPP_SETUP_GUIDE.md` para:
1. Criar Meta Business Account
2. Criar App no Meta for Developers
3. Adicionar WhatsApp Product
4. Configurar número de telefone
5. Obter credenciais

### 3. Configurar Variáveis de Ambiente

Adiciona ao teu `.env` ou Render environment variables:

```bash
WHATSAPP_ACCESS_TOKEN=your_permanent_access_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id_here
WHATSAPP_VERIFY_TOKEN=meu_token_secreto_123  # Qualquer senha segura
```

### 4. Configurar Webhook no Meta

Depois do deploy no Render:

1. Vai a: https://developers.facebook.com/apps
2. Seleciona a tua app
3. WhatsApp → Configuration
4. Webhook:
   - **Callback URL**: `https://carrental-api-5f8q.onrender.com/api/whatsapp/webhook`
   - **Verify Token**: `meu_token_secreto_123` (o mesmo do .env)
5. Subscribe to: `messages`, `message_status`

### 5. Deploy

```bash
git add .
git commit -m "WhatsApp integration complete"
git push origin main
```

O Render fará deploy automático.

## 📖 Como Usar

### Acessar Dashboard

1. Login no sistema: https://carrental-api-5f8q.onrender.com/login
2. Ir para: https://carrental-api-5f8q.onrender.com/whatsapp

### Enviar Mensagem

**Via Dashboard:**
1. Seleciona conversa
2. Escreve mensagem
3. Clica em enviar

**Via API:**
```bash
curl -X POST https://carrental-api-5f8q.onrender.com/api/whatsapp/send-message \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "351912345678",
    "message": "Olá! Como posso ajudar?"
  }'
```

### Criar Quick Reply

```bash
curl -X POST https://carrental-api-5f8q.onrender.com/api/whatsapp/quick-replies \
  -H "Content-Type: application/json" \
  -d '{
    "shortcut": "/preco",
    "title": "Consultar Preços",
    "message_text": "Para consultar preços, indique as datas e tipo de veículo",
    "category": "pricing"
  }'
```

## 🔧 Próximos Passos (Tu Decides)

### Automações de Reserva
- [ ] Template de confirmação de reserva
- [ ] Notificação automática de pickup
- [ ] Lembrete de devolução
- [ ] Envio de contrato via WhatsApp

### Funcionalidades Avançadas
- [ ] Chatbot com respostas automáticas
- [ ] Integração com sistema de reservas
- [ ] Analytics de atendimento
- [ ] Multi-agente (atribuir conversas a colaboradores)

### Templates a Criar no WhatsApp

Tens de criar e aprovar templates no Meta Business Manager:

**Template de Confirmação:**
```
Olá {{1}}! 
Sua reserva foi confirmada:
📅 Pickup: {{2}}
🚗 Veículo: {{3}}
📍 Local: {{4}}

Obrigado pela preferência!
Auto Prudente
```

**Template de Lembrete:**
```
Olá {{1}}!
Lembrete: Seu pickup é amanhã às {{2}}.
Local: {{3}}

Estamos à disposição!
Auto Prudente
```

## 🆘 Troubleshooting

### Webhook não recebe mensagens
1. Verifica se o webhook está configurado corretamente no Meta
2. Testa o endpoint: `GET https://carrental-api-5f8q.onrender.com/api/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=meu_token_secreto_123&hub.challenge=test`
3. Deve retornar "test"

### Mensagens não são enviadas
1. Verifica se `WHATSAPP_ACCESS_TOKEN` e `WHATSAPP_PHONE_NUMBER_ID` estão corretos
2. Testa diretamente via API:
   ```bash
   curl -X POST https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages \
     -H "Authorization: Bearer {ACCESS_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{"messaging_product":"whatsapp","to":"351912345678","type":"text","text":{"body":"Test"}}'
   ```

### Database errors
1. Verifica se o schema foi executado: `SELECT * FROM whatsapp_contacts LIMIT 1;`
2. Se não existir, executa `database_whatsapp.sql` novamente

## 📊 Estrutura de Dados

### Fluxo de Mensagem Recebida
```
WhatsApp → Webhook → whatsapp_api.py → Database
                                      → Marca como lida
                                      → Update conversa
```

### Fluxo de Mensagem Enviada
```
Dashboard → API → whatsapp_client.py → WhatsApp Cloud API
                → Database (save outbound message)
```

## 🔐 Segurança

- ✅ Webhook verifica token antes de processar
- ✅ Todas as credenciais em variáveis de ambiente
- ✅ Autenticação obrigatória para aceder ao dashboard
- ✅ HTTPS em todas as comunicações

## 📝 Notas

- **Templates**: Só podes enviar mensagens iniciadas pelo negócio (após 24h) usando templates aprovados
- **Custos**: 1.000 conversas/mês GRÁTIS, depois ~€0.01-0.05 por conversa
- **Limite**: 250 mensagens/segundo (mais que suficiente para Auto Prudente)
- **Número**: Tens de usar número dedicado (não pode estar no WhatsApp App)

## ✅ Checklist Final

- [ ] Database schema executado
- [ ] Variáveis de ambiente configuradas no Render
- [ ] Meta Business Account criada
- [ ] App criada no Meta for Developers
- [ ] WhatsApp Product adicionado
- [ ] Número de telefone configurado
- [ ] Webhook configurado e verificado
- [ ] Templates criados e aprovados (opcional no início)
- [ ] Testado envio/recepção de mensagens
- [ ] Dashboard acessível em /whatsapp

---

**Desenvolvido para Auto Prudente • 2024**
