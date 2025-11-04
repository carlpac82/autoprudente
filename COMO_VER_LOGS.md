# 📊 Como Ver os Logs do Scraping

## 🎯 Problema Resolvido

Agora todos os passos do scraping aparecem nos logs do servidor!

## 🚀 Como Ver os Logs

### Opção 1: Terminal do Servidor

Quando inicias o servidor, vês os logs diretamente:

```bash
python3 main.py
```

Vais ver:
```
[SELENIUM_SIMPLE] Iniciando scraping...
[SELENIUM_SIMPLE] Local: Faro Aeroporto (FAO)
[SELENIUM_SIMPLE] Datas: 11/11/2025 - 19/11/2025
[SELENIUM_SIMPLE] Navegando para https://www.carjet.com/aluguel-carros/index.htm
[SELENIUM_SIMPLE] ✅ Cookies rejeitados
[SELENIUM_SIMPLE] PASSO 1: Escrevendo local...
[SELENIUM_SIMPLE] ✓ Local digitado
[SELENIUM_SIMPLE] PASSO 2: Aguardando dropdown...
[SELENIUM_SIMPLE] ✅ Dropdown clicado
[SELENIUM_SIMPLE] PASSO 3: Preenchendo datas e horas...
[SELENIUM_SIMPLE] ✓ Datas preenchidas
[SELENIUM_SIMPLE] PASSO 4: Submetendo...
[SELENIUM_SIMPLE] Aguardando navegação...
[SELENIUM_SIMPLE] Aguardando página de resultados...
[SELENIUM_SIMPLE] ✅ Página carregada após 0s
[SELENIUM_SIMPLE] URL final: https://www.carjet.com/do/list/pt?s=...
[SELENIUM_SIMPLE] ✅ Sucesso! HTML: 1127947 bytes
[SELENIUM] ✅ 281 carros encontrados!
```

### Opção 2: Salvar Logs em Ficheiro

```bash
# Iniciar servidor e salvar logs
python3 main.py 2>&1 | tee server.log
```

Depois, noutro terminal:
```bash
# Ver logs em tempo real
./view_logs.sh
```

### Opção 3: Ver Logs Filtrados

```bash
# Ver apenas logs do Selenium
tail -f server.log | grep SELENIUM_SIMPLE

# Ver apenas erros
tail -f server.log | grep "❌\|⚠️"

# Ver apenas sucessos
tail -f server.log | grep "✅"
```

## 📋 O Que Cada Log Significa

### ✅ Logs de Sucesso

- `[SELENIUM_SIMPLE] ✅ Cookies rejeitados` - Cookies aceites/rejeitados
- `[SELENIUM_SIMPLE] ✓ Local digitado` - Local escrito no campo
- `[SELENIUM_SIMPLE] ✅ Dropdown clicado` - Dropdown do local clicado
- `[SELENIUM_SIMPLE] ✓ Datas preenchidas` - Datas e horas preenchidas
- `[SELENIUM_SIMPLE] ✅ Página carregada` - Página de resultados carregada
- `[SELENIUM_SIMPLE] ✅ Sucesso!` - HTML capturado com sucesso
- `[SELENIUM] ✅ X carros encontrados!` - Carros parseados

### ⚠️ Logs de Aviso

- `[SELENIUM_SIMPLE] ⚠️ URL com war=` - Sem disponibilidade para essas datas
- `[POST_DIRETO] ⚠️ Retornou 0 items` - POST direto falhou

### ❌ Logs de Erro

- `[SELENIUM_SIMPLE] ❌ Erro:` - Erro durante scraping
- `[SELENIUM_SIMPLE] ❌ URL inesperada` - URL não esperada

## 🔍 Debugging

Se o scraping falhar, procura por:

1. **Dropdown não clicou?**
   ```
   [SELENIUM_SIMPLE] PASSO 2: Aguardando dropdown...
   [SELENIUM_SIMPLE] ❌ Erro: ...
   ```

2. **Datas não preenchidas?**
   ```
   [SELENIUM_SIMPLE] PASSO 3: Preenchendo datas...
   [SELENIUM_SIMPLE] ✓ Datas preenchidas: {'allFilled': False, ...}
   ```

3. **Página não carregou?**
   ```
   [SELENIUM_SIMPLE] Aguardando página de resultados...
   [SELENIUM_SIMPLE] ❌ URL inesperada: ...
   ```

## 🎯 Logs na Interface Web

Os logs aparecem automaticamente no terminal onde o servidor está a correr.

**Não precisas fazer nada extra!** Basta olhar para o terminal. 👀

## 📝 Exemplo Completo de Sucesso

```
[API] REQUEST: location=Faro, start_date=2025-11-11, days=8
[POST_DIRETO] Tentando POST direto ao Carjet...
[POST_DIRETO] ⚠️ Retornou 0 items, continuando para SELENIUM...
[SELENIUM] Iniciando scraping SIMPLES (igual ao teste) para Faro
[SELENIUM_SIMPLE] Iniciando scraping...
[SELENIUM_SIMPLE] Local: Faro Aeroporto (FAO)
[SELENIUM_SIMPLE] Datas: 11/11/2025 - 19/11/2025
[SELENIUM_SIMPLE] Navegando para https://www.carjet.com/aluguel-carros/index.htm
[SELENIUM_SIMPLE] ✅ Cookies rejeitados
[SELENIUM_SIMPLE] PASSO 1: Escrevendo local...
[SELENIUM_SIMPLE] ✓ Local digitado
[SELENIUM_SIMPLE] PASSO 2: Aguardando dropdown...
[SELENIUM_SIMPLE] ✅ Dropdown clicado
[SELENIUM_SIMPLE] PASSO 3: Preenchendo datas e horas...
[SELENIUM_SIMPLE] ✓ Datas preenchidas: {'allFilled': True, ...}
[SELENIUM_SIMPLE] PASSO 4: Submetendo...
[SELENIUM_SIMPLE] Aguardando navegação...
[SELENIUM_SIMPLE] Aguardando página de resultados...
[SELENIUM_SIMPLE] ✅ Página carregada após 0s
[SELENIUM_SIMPLE] URL final: https://www.carjet.com/do/list/pt?s=...&b=...
[SELENIUM_SIMPLE] ✅ Sucesso! HTML: 1127947 bytes
[SELENIUM] ✅ Scraping simples bem-sucedido!
[SELENIUM] Fazendo parse de 1127947 bytes...
[SELENIUM] Parsed 281 items
[SELENIUM] ✅ 281 carros encontrados!
```

## ✅ Tudo Pronto!

Agora podes ver **TODOS** os passos do scraping em tempo real! 🎉
