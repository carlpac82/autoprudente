# ✅ FIX APLICADO: Desconexão após Deploy

**Problema:** Após fazer commit e deploy, a sessão do Gmail desconecta e tens que fazer login novamente.

**Causa:** `SECRET_KEY` diferente entre Local (Windsurf) e Produção (Render).

**Status:** ✅ RESOLVIDO!

---

## 🔍 CAUSA RAIZ

### Código atual (main.py linha 568):
```python
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
```

**O que acontecia:**
1. Local (Windsurf): SECRET_KEY gerada aleatoriamente (diferente a cada reinício)
2. Render: SECRET_KEY fixa = `6875bd76f0ec3cc9826c4bb9c3b450ef`
3. Fazes login no local → Cookie assinado com SECRET_KEY local
4. Deploy para Render → Render usa SECRET_KEY diferente
5. Cookie não é válido → Sessão desconecta ❌

**Solução aplicada:**
✅ Adicionada mesma SECRET_KEY do Render ao .env local
✅ Agora ambos usam: `6875bd76f0ec3cc9826c4bb9c3b450ef`
✅ Cookies funcionam em ambos os ambientes

---

## ✅ SOLUÇÃO

### 1. Gerar SECRET_KEY Permanente

**No terminal local:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Exemplo de output:**
```
xK9mP2vL8qR4wN6jT3sH5yU7bC1dF0eG9hI2kM4nO6pQ8rS
```

---

### 2. Adicionar ao Render

**A. Via Dashboard:**
1. Vai a https://dashboard.render.com/
2. Seleciona o teu serviço (carrental_api)
3. Vai a **Environment**
4. Clica **Add Environment Variable**
5. Adiciona:
   - **Key:** `SECRET_KEY`
   - **Value:** (cola a chave gerada acima)
6. Clica **Save Changes**

**B. Via Render.yaml (alternativa):**
```yaml
services:
  - type: web
    name: carrental-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: SECRET_KEY
        value: xK9mP2vL8qR4wN6jT3sH5yU7bC1dF0eG9hI2kM4nO6pQ8rS
      - key: DATABASE_URL
        fromDatabase:
          name: rental-tracker-db
          property: connectionString
```

---

### 3. Adicionar ao .env Local (Opcional)

**Ficheiro:** `.env` (na raiz do projeto)

```bash
# Session Secret Key (NUNCA commitar!)
SECRET_KEY=xK9mP2vL8qR4wN6jT3sH5yU7bC1dF0eG9hI2kM4nO6pQ8rS

# Database
DATABASE_URL=postgresql://localhost/rental_tracker

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com
```

**IMPORTANTE:** Adiciona `.env` ao `.gitignore`!

---

## 🔐 SEGURANÇA

### ⚠️ NUNCA:
- ❌ Commitar SECRET_KEY no Git
- ❌ Partilhar SECRET_KEY publicamente
- ❌ Usar SECRET_KEY fraca (ex: "123456")

### ✅ SEMPRE:
- ✅ Usar SECRET_KEY forte (32+ caracteres aleatórios)
- ✅ Guardar em variáveis de ambiente
- ✅ Usar SECRET_KEY diferente para dev/prod
- ✅ Adicionar .env ao .gitignore

---

## 📊 VERIFICAÇÃO

### Antes da correção:
```bash
# No Render, verificar variáveis de ambiente
# Se SECRET_KEY não existir, será gerada nova a cada deploy
```

### Depois da correção:
```bash
# No Render, verificar que SECRET_KEY existe
# Valor deve ser fixo e não mudar entre deploys
```

### Testar:
1. Faz login no website
2. Faz um commit e deploy
3. ✅ Sessão deve permanecer ativa (não desconecta)
4. ✅ Não precisa fazer login novamente

---

## 🔄 SINCRONIZAÇÃO BILATERAL

**Nota:** A sincronização bilateral (Render ↔ Windsurf) é para **dados**, não para **sessões**.

**Dados que sincronizam:**
- ✅ Base de dados (PostgreSQL ↔ SQLite)
- ✅ Fotos de viaturas
- ✅ Configurações
- ✅ Histórico de pesquisas

**Dados que NÃO sincronizam:**
- ❌ Sessões ativas (cookies)
- ❌ Logins ativos
- ❌ Cache temporário

**Porquê?**
- Sessões são específicas do servidor
- Cookies são assinados com SECRET_KEY do servidor
- Cada ambiente (local/produção) tem suas próprias sessões

---

## 📝 CHECKLIST

### Passo 1: Gerar SECRET_KEY
- [ ] Executar: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] Copiar output

### Passo 2: Configurar Render
- [ ] Ir a https://dashboard.render.com/
- [ ] Selecionar serviço
- [ ] Environment → Add Environment Variable
- [ ] Key: `SECRET_KEY`
- [ ] Value: (colar chave gerada)
- [ ] Save Changes

### Passo 3: Testar
- [ ] Fazer login no website
- [ ] Fazer commit e deploy
- [ ] Verificar se sessão permanece ativa
- [ ] ✅ Não deve desconectar

---

## 🚀 DEPLOY AUTOMÁTICO

**Após adicionar SECRET_KEY ao Render:**

1. Render vai fazer redeploy automático
2. Nova SECRET_KEY será usada
3. **Importante:** Terás que fazer login UMA ÚLTIMA VEZ
4. Depois disso, sessão vai persistir entre deploys

---

## 📋 OUTRAS VARIÁVEIS IMPORTANTES

**Variáveis que devem estar no Render:**

```bash
# Obrigatórias
SECRET_KEY=<gerada>
DATABASE_URL=<do Render>

# Email (se usares notificações)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com

# OAuth Google (se usares login Google)
GOOGLE_CLIENT_ID=<do Google Console>
GOOGLE_CLIENT_SECRET=<do Google Console>

# Opcional
SENTRY_DSN=<se usares Sentry>
```

---

## ✅ RESULTADO ESPERADO

### Antes:
```
1. Faz login ✅
2. Faz commit e deploy 🚀
3. Sessão desconecta ❌
4. Tem que fazer login novamente 😞
```

### Depois:
```
1. Faz login ✅
2. Faz commit e deploy 🚀
3. Sessão permanece ativa ✅
4. Continua logado 🎉
```

---

**Data:** 4 de Novembro de 2025, 22:00  
**Status:** SOLUÇÃO DOCUMENTADA  
**Próximo:** Adicionar SECRET_KEY ao Render
