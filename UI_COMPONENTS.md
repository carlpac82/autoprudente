# 🎨 Componentes de UI - Guia de Estilo

## 🎯 Cores do Website

### Cores Principais
```css
--brand-teal: #009cb6      /* Azul principal (botões, links) */
--brand-yellow: #f4ad0f    /* Amarelo (destaques, hover) */
--brand-header: #7ec6e0    /* Azul claro (header) */
```

### Cores de Estado
```css
--success: #009cb6         /* Sucesso (azul do site) */
--error: #ef4444           /* Erro (vermelho) */
--warning: #f4ad0f         /* Aviso (amarelo do site) */
```

## 📦 Componentes Implementados

### 1. **Alertas / Avisos**

#### Sucesso (Success)
```html
<div class="mb-4 p-4 rounded-lg border-l-4 border-[#009cb6] bg-blue-50 flex items-start gap-3">
  <svg class="w-5 h-5 text-[#009cb6] flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
  </svg>
  <div>
    <p class="font-semibold text-[#009cb6]">Título do Sucesso</p>
    <p class="text-sm text-gray-600 mt-1">Mensagem detalhada.</p>
  </div>
</div>
```

**Visual:**
```
┌─────────────────────────────────────────┐
│ ✓ Configurações guardadas com sucesso!  │
│   As alterações foram aplicadas.        │
└─────────────────────────────────────────┘
```

#### Erro (Error)
```html
<div class="mb-4 p-4 rounded-lg border-l-4 border-red-500 bg-red-50 flex items-start gap-3">
  <svg class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
  </svg>
  <div>
    <p class="font-semibold text-red-800">Erro ao guardar</p>
    <p class="text-sm text-red-700 mt-1">Mensagem de erro detalhada.</p>
  </div>
</div>
```

#### Aviso (Warning)
```html
<div class="mb-4 p-4 rounded-lg border-l-4 border-[#f4ad0f] bg-yellow-50 flex items-start gap-3">
  <svg class="w-5 h-5 text-[#f4ad0f] flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
  </svg>
  <div>
    <p class="font-semibold text-[#f4ad0f]">Atenção</p>
    <p class="text-sm text-gray-700 mt-1">⚠️ Dados de cache (3.2h atrás)</p>
  </div>
</div>
```

### 2. **Ícones de Secção**

Todos os ícones usam a cor do website (`#009cb6`) e são monocromáticos:

#### Ícone de Documento/Export
```html
<svg class="w-5 h-5 text-[#009cb6]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
</svg>
```

#### Ícone de Dinheiro/Preço
```html
<svg class="w-4 h-4 text-[#f4ad0f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
</svg>
```

#### Ícone de Pintura/Design
```html
<svg class="w-5 h-5 text-[#009cb6]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"/>
</svg>
```

### 3. **Botões**

#### Botão Principal
```html
<button class="px-4 py-2 rounded bg-[#009cb6] text-white hover:bg-[#f4ad0f] transition-colors">
  Save
</button>
```

#### Botão Secundário
```html
<button class="px-4 py-2 rounded border border-[#009cb6] text-[#009cb6] bg-white hover:bg-[#f6b511] hover:border-[#f6b511] hover:text-white transition-colors">
  Cancel
</button>
```

### 4. **Inputs**

#### Input de Texto
```html
<input type="text" 
  class="mt-1 w-full rounded-md border-gray-300 shadow-sm focus:border-[#009cb6] focus:ring-2 focus:ring-[#009cb6]" 
  placeholder="0.00" />
```

#### Input de Cor
```html
<input type="color" 
  class="h-10 w-20 rounded border border-gray-300 cursor-pointer" 
  value="#009cb6" />
```

#### Checkbox
```html
<input type="checkbox" 
  class="w-4 h-4 text-[#009cb6] border-gray-300 rounded focus:ring-[#009cb6]" />
```

### 5. **Títulos de Secção**

```html
<h3 class="text-md font-semibold text-gray-800 mb-3 flex items-center gap-2">
  <svg class="w-5 h-5 text-[#009cb6]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <!-- ícone aqui -->
  </svg>
  Título da Secção
</h3>
```

## 🎨 Classes CSS Reutilizáveis

### Alertas
```css
.alert-success {
  padding: 1rem;
  border-radius: 0.5rem;
  border-left: 4px solid #009cb6;
  background-color: #eff6ff;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.alert-error {
  padding: 1rem;
  border-radius: 0.5rem;
  border-left: 4px solid #ef4444;
  background-color: #fef2f2;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.alert-warning {
  padding: 1rem;
  border-radius: 0.5rem;
  border-left: 4px solid #f4ad0f;
  background-color: #fffbeb;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}
```

## 📋 Checklist de Implementação

Ao criar novos componentes, garantir:

- ✅ Ícones monocromáticos com cor `#009cb6` ou `#f4ad0f`
- ✅ Alertas com borda esquerda de 4px
- ✅ Hover states com transição suave
- ✅ Focus states visíveis (ring)
- ✅ Espaçamento consistente (gap-2, gap-3, p-4)
- ✅ Bordas arredondadas (rounded, rounded-lg)
- ✅ Texto legível (text-gray-700, text-gray-800)
- ✅ Sem emojis (exceto em mensagens de cache/warning)

## 🚀 Exemplos de Uso

### Aviso de Cache
```html
<div class="mb-4 p-4 rounded-lg border-l-4 border-[#f4ad0f] bg-yellow-50 flex items-start gap-3">
  <svg class="w-5 h-5 text-[#f4ad0f] flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
  </svg>
  <div>
    <p class="font-semibold text-[#f4ad0f]">Dados de Cache</p>
    <p class="text-sm text-gray-700 mt-1">⚠️ Usando dados guardados (3.2h atrás). Scraping temporariamente indisponível.</p>
  </div>
</div>
```

### Sucesso ao Guardar
```html
<div class="mb-4 p-4 rounded-lg border-l-4 border-[#009cb6] bg-blue-50 flex items-start gap-3">
  <svg class="w-5 h-5 text-[#009cb6] flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
  </svg>
  <div>
    <p class="font-semibold text-[#009cb6]">Configurações guardadas!</p>
    <p class="text-sm text-gray-600 mt-1">As alterações foram aplicadas com sucesso.</p>
  </div>
</div>
```

## 🎯 Regras de Design

1. **Consistência:** Todos os alertas seguem o mesmo padrão
2. **Cores:** Usar apenas as cores do website (#009cb6, #f4ad0f)
3. **Ícones:** Sempre monocromáticos, nunca coloridos
4. **Espaçamento:** Consistente (p-4, gap-3, mb-4)
5. **Tipografia:** Títulos em semibold, texto em regular
6. **Acessibilidade:** Contraste adequado, focus states visíveis
7. **Responsividade:** Funciona em mobile e desktop

---

**Todos os componentes seguem este guia de estilo para manter consistência visual!** 🎨
