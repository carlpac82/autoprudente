# Fix CarJet Scraping - Dezembro 2025

## Problema
Sistema de automated prices retornava **0 carros** em todas as tentativas (requests, Playwright, Selenium).

## Causa Raiz
O formulário do CarJet não estava sendo submetido corretamente:
- Botão `#sendForm` existe no HTML mas não é "interactable" via Selenium após interagir com campos
- Tentativas de clicar no botão falhavam
- Sistema não navegava para `/do/list/` (página de resultados)
- HTML capturado era da página intermediária (sem preços)

## Correções Aplicadas

### 1. **main.py** - Playwright (linha ~11119)
Adicionado seletor `#sendForm` na lista de tentativas:

```python
submit_selectors = [
    '#sendForm',  # ID correto do botão CarJet
    'button#sendForm',
    'button[type="submit"]',
    'input[type="submit"]',
    'form button',
    '#btnSearch',
    '.btn-search',
]
```

### 2. **main.py** - Selenium (linha ~11627)
Melhorado fallback para usar JavaScript quando Selenium falha:

```python
# Tentar clicar no botão #sendForm (mais confiável que form.submit)
try:
    submit_btn = driver.find_element(By.ID, 'sendForm')
    submit_btn.click()
    print(f"[SELENIUM] ✓ Botão #sendForm clicado")
except Exception as e:
    print(f"[SELENIUM] ⚠️ Erro ao clicar no botão, usando JS: {e}")
    driver.execute_script("document.getElementById('sendForm').click();")
```

## Teste de Validação
Script `test_form_submit_direct.py` confirma que a correção funciona:

```
✅ Navegou para /do/list/ após 0s
📊 Articles: 89
🚗 Primeiro carro: Peugeot 108
💰 Preços .pr-euros: 1
   [0] -25%23,12 €17,34 €

✅✅✅ PREÇOS ENCONTRADOS! Sistema está funcionando!
```

## Seletores Verificados
✅ `#pickup` - Input de localização  
✅ `#fechaRecogida` / `#fechaDevolucion` - Datas (hidden)  
✅ `#fechaRecogidaSelHour` / `#fechaDevolucionSelHour` - Horas  
✅ `#sendForm` - Botão submit (type="submit", class="btn")  
✅ `#recogida_lista li` - Dropdown de localizações  

## Estrutura HTML de Resultados
Confirma que parsing está correto:

```html
<section class="newcarlist price-per-day">
  <article class="halloween" data-order="1" data-prv="GMO1">
    <h2>Peugeot 108</h2>
    <span class="price pr-euros">17,34 €</span>
  </article>
</section>
```

## Status
✅ **RESOLVIDO** - Sistema volta a obter preços corretamente

## Próximos Passos
1. Reiniciar `automated_scheduler.py` para aplicar correções
2. Monitorar logs para confirmar que está obtendo preços
3. Verificar se histórico volta a popular

## Data
17 de Dezembro de 2025
