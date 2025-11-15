# 📋 Como Usar Templates WhatsApp e Quick Replies

## 🎯 Diferença Entre Templates e Quick Replies

### **Templates WhatsApp** 📤
- **O que são:** Mensagens pré-aprovadas pelo WhatsApp
- **Quando usar:** Para INICIAR conversas ou contactar clientes FORA da janela de 24 horas
- **Aprovação:** ⚠️ PRECISAM ser aprovados pelo WhatsApp (demora até 24h)
- **Exemplos:**
  - Confirmação de reserva
  - Lembrete de recolha
  - Seguimento de orçamento
  - Instruções de check-in

### **Quick Replies** 💬
- **O que são:** Respostas rápidas prontas a usar
- **Quando usar:** DENTRO de conversas ativas (janela de 24 horas)
- **Aprovação:** ✅ NÃO precisam aprovação - funcionam imediatamente
- **Exemplos:**
  - Bom dia / Boa tarde
  - Obrigado / De nada
  - Um momento, por favor
  - Entendido

---

## 🚀 PASSO 1: Criar Templates WhatsApp (40 templates)

### 1.1 Abrir Console
1. Ir para: **https://carrental-api-5f8q.onrender.com/admin/whatsapp**
2. Fazer login como admin
3. Pressionar **F12** → aba **Console**

### 1.2 Carregar Script
1. Abrir arquivo: `TEMPLATES_WHATSAPP.js`
2. Selecionar TUDO (**Cmd+A**)
3. Copiar (**Cmd+C**)
4. Colar no Console (**Cmd+V**)
5. Pressionar **ENTER**

Vai aparecer:
```
╔════════════════════════════════════════════════════════════╗
║      TEMPLATES WHATSAPP - MENSAGENS DE NEGÓCIO            ║
║      Precisam aprovação do WhatsApp (24h)                 ║
╚════════════════════════════════════════════════════════════╝

📋 10 Templates × 4 idiomas = 40 templates total:

🚗 TEMPLATES DE NEGÓCIO:
   1. confirmacao_interesse
   2. confirmacao_reserva
   ...
```

### 1.3 Criar Templates
No console, executar:
```javascript
criarTemplatesWhatsApp()
```

**Aguardar ~40 segundos** (1 segundo por template)

Resultado esperado:
```
✅ confirmacao_interesse (pt_PT) - CRIADO E ENVIADO
✅ confirmacao_interesse (en) - CRIADO E ENVIADO
✅ confirmacao_interesse (fr) - CRIADO E ENVIADO
✅ confirmacao_interesse (de) - CRIADO E ENVIADO
...

╔════════════════════════════════════╗
║   RESUMO - TEMPLATES WHATSAPP      ║
╠════════════════════════════════════╣
║ ✅ Criados: 40                     ║
║ ❌ Erros:    0                     ║
║ 📊 Total:   40                     ║
╚════════════════════════════════════╝

⏰ Aguarde até 24 horas para aprovação do WhatsApp.
```

### 1.4 Verificar Status (depois de algumas horas)
```javascript
verificarStatusTemplates()
```

---

## 💬 PASSO 2: Criar Quick Replies (60 respostas)

### 2.1 Carregar Script
1. No mesmo console (ou abrir novamente)
2. Abrir arquivo: `QUICK_REPLIES_WHATSAPP.js`
3. Selecionar TUDO (**Cmd+A**)
4. Copiar (**Cmd+C**)
5. Colar no Console (**Cmd+V**)
6. Pressionar **ENTER**

Vai aparecer:
```
╔════════════════════════════════════════════════════════════╗
║           QUICK REPLIES - RESPOSTAS RÁPIDAS               ║
║           NÃO precisam aprovação do WhatsApp              ║
╚════════════════════════════════════════════════════════════╝

📋 15 Respostas × 4 idiomas = 60 quick replies total:
```

### 2.2 Criar Quick Replies
No console, executar:
```javascript
criarQuickReplies()
```

**Aguardar ~12 segundos** (200ms por reply)

Resultado esperado:
```
✅ bom_dia_pt - CRIADO
✅ bom_dia_en - CRIADO
✅ bom_dia_fr - CRIADO
✅ bom_dia_de - CRIADO
...

╔════════════════════════════════════╗
║     RESUMO - QUICK REPLIES         ║
╠════════════════════════════════════╣
║ ✅ Criados: 60                     ║
║ ❌ Erros:    0                     ║
║ 📊 Total:   60                     ║
╚════════════════════════════════════╝

✅ Quick Replies NÃO precisam aprovação!
💡 Já estão prontas para usar no chat!
```

### 2.3 Listar Quick Replies
```javascript
listarQuickReplies()
```

---

## 🧹 Funções Úteis

### Deletar Todos os Templates
⚠️ **CUIDADO:** Isto deleta TUDO!
```javascript
deletarTodosTemplates()
```

### Deletar Todas as Quick Replies
```javascript
deletarTodasQuickReplies()
```

---

## 📊 Resumo Final

Depois de executar ambos os scripts, terá:

| Tipo | Quantidade | Aprovação | Uso |
|------|------------|-----------|-----|
| **Templates WhatsApp** | 40 (10×4) | ⚠️ Sim (24h) | Iniciar conversas |
| **Quick Replies** | 60 (15×4) | ✅ Não | Dentro de conversas |
| **TOTAL** | 100 | - | - |

---

## ✅ Como Usar Depois de Criados

### Templates WhatsApp (depois de aprovados)
1. Ir para **WhatsApp Dashboard**
2. Selecionar contacto
3. Clicar **"Usar Template"**
4. Escolher template aprovado
5. Enviar

### Quick Replies
1. Ir para **WhatsApp Dashboard**
2. Selecionar conversa ativa
3. Na caixa de mensagem, digitar **/** (barra)
4. Escolher quick reply da lista
5. Enviar

---

## 🌍 Idiomas Disponíveis

Todos os templates e quick replies estão disponíveis em:

- 🇵🇹 **Português** (pt_PT)
- 🇬🇧 **Inglês** (en)
- 🇫🇷 **Francês** (fr)
- 🇩🇪 **Alemão** (de)

---

## ❓ Troubleshooting

### Erro: "current transaction is aborted"
- ✅ **JÁ CORRIGIDO** no commit mais recente
- Aguarde deploy completar (~2 min)
- Tente novamente

### Templates não aparecem
- Verificar se foram enviados: `verificarStatusTemplates()`
- Aguardar aprovação do WhatsApp (até 24h)

### Quick Replies não aparecem
- Verificar se foram criadas: `listarQuickReplies()`
- Recarregar página do WhatsApp Dashboard

---

## 📝 Arquivos

- ✅ `TEMPLATES_WHATSAPP.js` - Templates de negócio (USE ESTE)
- ✅ `QUICK_REPLIES_WHATSAPP.js` - Respostas rápidas (USE ESTE)
- ❌ `TEMPLATES_AUTOMOVEIS.js` - DESATUALIZADO (NÃO USAR)

---

**Pronto! Sistema completo de mensagens WhatsApp configurado! 🎉**
