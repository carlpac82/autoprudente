# 🚀 Modo Headless (Chrome Invisível)

## ✅ IMPLEMENTADO

O Chrome agora roda em **modo headless (invisível)** por padrão!

---

## 🎯 Como Funciona

### Modo Padrão (Headless - Invisível)

```bash
# Iniciar servidor normalmente
python3 main.py
```

**Comportamento:**
- ✅ Chrome **NÃO abre** janela visível
- ✅ Scraping funciona em background
- ✅ Mais rápido
- ✅ Não interrompe trabalho

**Logs:**
```
[SELENIUM_SIMPLE] Modo headless (invisível)
[SELENIUM_SIMPLE] Iniciando scraping...
[SELENIUM_SIMPLE] ✅ Sucesso!
```

---

## 🔍 Modo Debug (Visível)

Para **ver o Chrome** durante scraping (útil para debug):

### Opção 1: Via .env

```bash
# Editar .env
SHOW_BROWSER=1
```

Depois reiniciar servidor:
```bash
python3 main.py
```

### Opção 2: Via Terminal (Temporário)

```bash
# Definir variável e iniciar
SHOW_BROWSER=1 python3 main.py
```

**Comportamento:**
- 👁️ Chrome **abre** janela visível
- 👁️ Podes ver cada passo
- 👁️ Útil para debug
- ⚠️ Mais lento

**Logs:**
```
[SELENIUM_SIMPLE] Modo visível (debug)
[SELENIUM_SIMPLE] Iniciando scraping...
```

---

## 📋 Comparação

| Característica | Headless (Padrão) | Visível (Debug) |
|----------------|-------------------|-----------------|
| Chrome abre? | ❌ Não | ✅ Sim |
| Velocidade | ⚡ Rápido | 🐢 Mais lento |
| Uso de memória | 💚 Baixo | 🟡 Médio |
| Debug | ⚠️ Logs apenas | ✅ Visual |
| Produção | ✅ Recomendado | ❌ Não usar |

---

## 🎯 Quando Usar Cada Modo

### Headless (Padrão) - Usar Sempre

**Situações:**
- ✅ Uso normal do sistema
- ✅ Produção (Render)
- ✅ Automated prices
- ✅ Pesquisas regulares

**Vantagens:**
- Não interrompe trabalho
- Mais rápido
- Menos recursos

### Visível (Debug) - Apenas para Debug

**Situações:**
- 🔍 Investigar problema
- 🔍 Ver o que está a acontecer
- 🔍 Testar novo código
- 🔍 Verificar dropdown

**Vantagens:**
- Vês cada passo
- Fácil identificar problemas
- Confirmar comportamento

---

## 🚀 Render (Produção)

No Render, **SEMPRE usa headless** automaticamente:

```
Render Environment:
SHOW_BROWSER não definido → Headless ✅
```

**Por quê?**
- Render não tem interface gráfica
- Headless é obrigatório
- Mais eficiente

---

## 🧪 Testar

### Teste 1: Headless (Padrão)

```bash
# Iniciar servidor
python3 main.py

# Fazer pesquisa
python3 test_main_api.py
```

**Resultado esperado:**
- ❌ Chrome NÃO abre
- ✅ Scraping funciona
- ✅ 281 carros encontrados

### Teste 2: Visível (Debug)

```bash
# Iniciar com SHOW_BROWSER
SHOW_BROWSER=1 python3 main.py

# Fazer pesquisa
python3 test_main_api.py
```

**Resultado esperado:**
- ✅ Chrome abre
- 👁️ Vês o scraping acontecer
- ✅ 281 carros encontrados

---

## ⚙️ Configuração

### .env (Permanente)

```bash
# .env
SHOW_BROWSER=1  # Descomentar para ativar
```

### Terminal (Temporário)

```bash
# Mac/Linux
export SHOW_BROWSER=1
python3 main.py

# Ou numa linha:
SHOW_BROWSER=1 python3 main.py
```

### Desativar

```bash
# .env
# SHOW_BROWSER=1  # Comentar ou remover

# Ou terminal:
unset SHOW_BROWSER
```

---

## 🐛 Troubleshooting

### Chrome não fecha?

**Problema:** Chrome fica aberto após scraping

**Solução:**
```bash
# Matar todos os Chrome:
pkill -f chrome
```

### Headless não funciona?

**Problema:** Erro ao usar headless

**Solução:**
```bash
# Usar modo visível temporariamente:
SHOW_BROWSER=1 python3 main.py
```

### Quer sempre visível?

**Solução:**
```bash
# Adicionar ao .env:
SHOW_BROWSER=1
```

---

## ✅ Resumo

**Padrão (Recomendado):**
```bash
python3 main.py
# Chrome invisível ✅
```

**Debug (Quando Necessário):**
```bash
SHOW_BROWSER=1 python3 main.py
# Chrome visível 👁️
```

**Produção (Render):**
```
Sempre headless ✅
Automático
```

---

**🎉 Chrome agora é invisível por padrão!**
