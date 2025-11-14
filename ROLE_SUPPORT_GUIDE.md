# 👥 Role "Support" (Atendimento) - Guia Completo

Sistema de utilizadores com acesso restrito para equipa de atendimento.

---

## ✨ Funcionalidades do Role "Support"

### Acessos Permitidos
- ✅ **WhatsApp Dashboard** (`/whatsapp`)
  - Ver conversas
  - Responder clientes
  - Enviar mensagens
  - Gestão de contactos
  
- ✅ **Inspeção de Veículos** (`/vehicle-inspection`)
  - Registar inspeções
  - Ver histórico
  - Tirar fotos de danos
  
- ✅ **API Endpoints Relacionados**
  - `/api/whatsapp/*` - Todas as APIs do WhatsApp
  - `/api/inspections/*` - APIs de inspeção
  - `/api/vehicles/*` - Dados de veículos

### Acessos Bloqueados
- ❌ Homepage (pesquisa de preços)
- ❌ Histórico de Preços
- ❌ Automação de Preços
- ❌ Damage Reports
- ❌ Painel Admin
- ❌ Todas as outras páginas

### Características Especiais
- 🔓 **Sessão Permanente** - Não expira automaticamente
- 🚫 **Sem Timeout** - Podem ficar logados indefinidamente
- 🔒 **Acesso Restrito** - Só conseguem aceder às 2 páginas permitidas

---

## 🚀 Como Criar Utilizador "Support"

### Via Admin Panel

1. **Login como Admin**
   - Acede: https://carrental-api-5f8q.onrender.com/login
   - Faz login com conta admin

2. **Ir para Users**
   - Clica no ícone de Settings no header
   - Vai a "Users"

3. **Criar/Editar Utilizador**
   - Clica em "Add User" para criar novo
   - Ou clica em "Edit" num utilizador existente

4. **Configurar Role**
   - **Username**: nome do utilizador (ex: `atendimento1`)
   - **Password**: password segura
   - **Role**: Seleciona `support`
   - **Can Access Inspection**: Deixa marcado (já tem por defeito)

5. **Salvar**
   - Clica "Create User" ou "Update"

---

## 📝 Exemplo de Utilizadores

### Equipa de Atendimento Típica

```
Utilizador 1:
- Username: atendimento.ana
- Role: support
- Acesso: WhatsApp + Inspeções

Utilizador 2:
- Username: atendimento.joao
- Role: support
- Acesso: WhatsApp + Inspeções

Utilizador 3:
- Username: recepcao.lisboa
- Role: support
- Acesso: WhatsApp + Inspeções
```

---

## 🔐 Comparação de Roles

| Funcionalidade | Admin | User | Receptionist | **Support** |
|----------------|-------|------|--------------|-------------|
| **Pesquisa Preços** | ✅ | ✅ | ❌ | ❌ |
| **Histórico Preços** | ✅ | ✅ | ❌ | ❌ |
| **Automação Preços** | ✅ | ✅ | ❌ | ❌ |
| **Damage Reports** | ✅ | ✅ | ❌ | ❌ |
| **Inspeção Veículos** | ✅ | ✅* | ✅ | ✅ |
| **WhatsApp** | ✅ | ✅ | ❌ | ✅ |
| **Admin Panel** | ✅ | ❌ | ❌ | ❌ |
| **Sessão Expira?** | Sim (30min) | Sim (30min) | Sim (30min) | **Não** |

*User normal precisa de permissão explícita para inspeções

---

## 💡 Quando Usar Role "Support"

### ✅ Ideal Para:
- **Equipa de Atendimento** ao cliente via WhatsApp
- **Recepcionistas** que fazem inspeções de veículos
- **Assistentes** que não precisam de acesso a preços
- **Turnos longos** (não precisam fazer re-login)

### ❌ Não Usar Para:
- Utilizadores que precisam de pesquisar preços
- Managers que precisam de ver histórico de preços
- Qualquer pessoa que precise de acesso ao sistema completo

---

## 🎯 Fluxo de Trabalho Típico

### Utilizador "Support" no Dia-a-Dia

1. **Manhã (08:00)**
   - Login em https://carrental-api-5f8q.onrender.com
   - Redirecionado automaticamente para `/whatsapp`
   
2. **Durante o Dia**
   - Responder mensagens WhatsApp
   - Quando cliente chega: ir para `/vehicle-inspection`
   - Fazer inspeção do veículo
   - Voltar para `/whatsapp` para continuar atendimento
   
3. **Fim do Dia**
   - Não precisa fazer logout (sessão não expira)
   - Pode fechar browser e fica logado

---

## 🔧 Configuração Técnica

### Como Funciona Internamente

```python
# Sessão não expira para role "support"
if user_role != "support":
    # Verifica timeout de 30 minutos
    if now - last_active > 1800:  # 30min
        session.clear()  # Logout automático

# Support: esta verificação é saltada!
```

### Páginas Permitidas para Support

```python
support_allowed_pages = [
    "/whatsapp",              # Dashboard WhatsApp
    "/api/whatsapp",          # APIs WhatsApp
    "/vehicle-inspection",    # Inspeção Veículos
    "/inspection-history",    # Histórico Inspeções
    "/api/inspections",       # APIs Inspeção
    "/api/inspection",        # API Inspeção (singular)
    "/api/vehicles",          # Dados Veículos
    "/logout",                # Logout
    "/static/",               # Ficheiros estáticos
    "/api/profile-picture",   # Foto perfil
    "/api/current-user",      # Dados utilizador
    "/api/user-settings"      # Definições
]
```

---

## 🆘 Troubleshooting

### Problema: Utilizador Support não consegue aceder WhatsApp

**Solução:**
1. Verifica se o role está correto: Admin → Users → Editar utilizador
2. Confirma que o role é exatamente `support` (lowercase)
3. Tenta fazer logout e login novamente

### Problema: Sessão continua a expirar

**Solução:**
1. Verifica o role na database:
   ```sql
   SELECT username, role FROM users WHERE username='nome_utilizador';
   ```
2. Deve retornar `support` exatamente
3. Se estiver diferente, atualiza:
   ```sql
   UPDATE users SET role='support' WHERE username='nome_utilizador';
   ```

### Problema: Redirecionado para página errada após login

**Comportamento Esperado:**
- **Admin**: Vai para `/` (homepage)
- **Support**: Se tentar ir para `/`, é bloqueado (403) e redirecionado para `/whatsapp`
- **Receptionist**: Se tentar ir para `/`, é bloqueado (403) e redirecionado para `/vehicle-inspection`

---

## 📊 Estatísticas e Monitorização

### Ver Utilizadores Support Ativos

No Admin Panel → Users, filtra por Role = "support"

### Logs de Atividade

Os utilizadores Support aparecem nos logs normais:
- Login/Logout
- Mensagens WhatsApp enviadas
- Inspeções criadas

---

## ✅ Checklist de Setup

Quando criares um novo utilizador Support:

- [ ] Username criado
- [ ] Password definida (partilhar com utilizador)
- [ ] Role = `support` (exatamente, lowercase)
- [ ] Can Access Inspection = ✅ (marcado)
- [ ] Testado login
- [ ] Testado acesso a `/whatsapp`
- [ ] Testado acesso a `/vehicle-inspection`
- [ ] Confirmado que não consegue aceder a outras páginas
- [ ] Confirmado que sessão não expira

---

## 🔮 Futuras Melhorias (Opcional)

Funcionalidades que podem ser adicionadas no futuro:

- [ ] Dashboard específico para role Support
- [ ] Analytics de atendimento (tempo médio resposta, etc)
- [ ] Sistema de turnos (atribuir conversas automaticamente)
- [ ] Notificações push para novas mensagens
- [ ] Chat interno entre utilizadores Support

---

**Desenvolvido para Auto Prudente • 2024**
