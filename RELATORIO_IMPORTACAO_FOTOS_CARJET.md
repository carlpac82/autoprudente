# 📸 RELATÓRIO DE IMPORTAÇÃO DE FOTOS DA CARJET

**Data:** 4 de Novembro de 2025  
**Objetivo:** Download e importação de fotos de viaturas da Carjet para o sistema de pricing

---

## ✅ RESUMO EXECUTIVO

### Resultados Globais
- **164 fotos descarregadas** da página da Carjet
- **74 carros mapeados** com sucesso na base de dados
- **90 carros não mapeados** (não existem na tabela `vehicle_name_overrides`)
- **74 registos atualizados** na tabela `vehicle_photos`

---

## 🔧 PROCESSO IMPLEMENTADO

### 1. Download das Fotos (Script: `download_carjet_photos_selenium.py`)

**Método:**
- ✅ Selenium com Chrome em modo visível
- ✅ Mobile emulation (iPhone 13 Pro)
- ✅ Extração direta do HTML da página de resultados
- ✅ Parsing com BeautifulSoup

**Estrutura HTML Identificada:**
```html
<article data-tab="car">
  <div class="cl--name">
    <h2>Nome do Carro <small>ou similar</small></h2>
    <span class="cl--name-type">Categoria</span>
  </div>
  <img class="cl--car-img" src="/cdn/img/cars/L/car_XXX.jpg">
</article>
```

**Dados Extraídos:**
- Nome da viatura (sem sufixo "ou similar")
- URL da foto (convertida para URL absoluta)
- Categoria (Pequeno, Médio, Grande, Automático, etc.)

**Ficheiros Criados:**
- `carjet_photos/` - 164 imagens (JPG, PNG, GIF)
- `carjet_cars_data.json` - Dados estruturados em JSON
- `carjet_cars_list.txt` - Lista legível
- `carjet_page_debug.html` - HTML da página para debug

---

### 2. Importação para Base de Dados (Script: `import_carjet_photos_to_db.py`)

**Processo:**
1. Leitura dos dados do ficheiro JSON
2. Normalização dos nomes (remoção de sufixos, lowercase)
3. Mapeamento manual para nomes conhecidos (VW → Volkswagen, etc.)
4. Pesquisa na tabela `vehicle_name_overrides`
5. Cópia da foto para diretório `uploaded/`
6. Inserção do BLOB na tabela `vehicle_photos`

**Tabela Atualizada:**
```sql
vehicle_photos (
  vehicle_name TEXT PRIMARY KEY,
  photo_data BLOB,
  photo_url TEXT,
  content_type TEXT,
  uploaded_at TEXT
)
```

---

## 📊 ESTATÍSTICAS DETALHADAS

### Carros Mapeados com Sucesso (74)

**Exemplos:**
- ✅ Fiat 500 → `fiat 500`
- ✅ Hyundai i10 → `hyundai i10`
- ✅ Toyota Aygo → `toyota aygo x`
- ✅ Mazda 2 → `mazda 2 auto`
- ✅ Citroen C4 → `citroen c4`
- ✅ Nissan Juke → `nissan juke auto`
- ✅ Toyota Yaris → `toyota yaris`
- ✅ Kia Sportage → `kia sportage`
- ✅ BMW X5 → `bmw x5 auto`
- ✅ Mercedes E Class → (várias variantes)

### Carros Não Mapeados (90)

**Principais Razões:**
1. **Não existem na tabela `vehicle_name_overrides`** (não foram parametrizados)
2. **Nomes diferentes** entre Carjet e sistema interno
3. **Variantes específicas** (SW, Hybrid, Electric) não mapeadas

**Exemplos de Não Mapeados:**
- ❌ Fiat Panda (não parametrizado)
- ❌ Renault Clio (não parametrizado)
- ❌ VW Polo (existe como "VW Polo" mas pesquisa por "volkswagen polo")
- ❌ Opel Corsa (não parametrizado)
- ❌ Peugeot 208 (não parametrizado)
- ❌ Seat Ibiza (não parametrizado)

---

## 📁 ESTRUTURA DE FICHEIROS

```
RentalPriceTrackerPerDay/
├── carjet_photos/                    # 164 fotos descarregadas
│   ├── Fiat_500.jpg
│   ├── VW_Golf.jpg
│   ├── Toyota_Yaris.png
│   └── ...
│
├── uploaded/                         # 74 fotos importadas
│   ├── carjet_fiat_500.png
│   ├── carjet_hyundai_i10.png
│   └── ...
│
├── carjet_cars_data.json            # Dados estruturados (164 carros)
├── carjet_cars_list.txt             # Lista legível
├── carjet_page_debug.html           # HTML da página
│
├── download_carjet_photos_selenium.py    # Script de download
└── import_carjet_photos_to_db.py         # Script de importação
```

---

## 🔍 ANÁLISE DE QUALIDADE DAS FOTOS

### Tipos de Imagens
- **JPG:** 10 imagens (~8-11 KB) - Fotos reais de alta qualidade
- **PNG:** 154 imagens (680 bytes) - Placeholders/ícones genéricos
- **GIF:** 1 imagem (11 KB) - Animação de loading

### Observações
⚠️ **Problema Identificado:** A maioria das imagens (154/164) são placeholders de 680 bytes (`loading-car@2x.png`), não fotos reais dos carros.

**Fotos Reais Encontradas (10):**
1. Fiat Panda - 11,478 bytes
2. Fiat 500 - 7,610 bytes
3. Renault Clio - 8,517 bytes
4. VW Polo - 8,083 bytes
5. Opel Corsa - 7,700 bytes
6. VW Golf - 11,251 bytes
7. Opel Mokka Electric - 10,519 bytes
8. Peugeot 2008 - 8,411 bytes
9. Renault Megane - 11,240 bytes
10. Peugeot 308 - 11,380 bytes

---

## 💡 RECOMENDAÇÕES

### Prioridade ALTA

1. **Parametrizar Carros em Falta**
   - Adicionar os 90 carros não mapeados à tabela `vehicle_name_overrides`
   - Focar nos mais comuns: Fiat Panda, Renault Clio, VW Polo, Opel Corsa

2. **Melhorar Download de Fotos**
   - As fotos estão em lazy-loading
   - Implementar scroll mais lento para carregar todas as imagens
   - Aguardar mais tempo após scroll
   - Verificar se imagem mudou de placeholder para foto real

3. **Normalização de Nomes**
   - Criar mapeamento mais robusto VW ↔ Volkswagen
   - Tratar variantes (SW, Auto, Hybrid, Electric) de forma consistente

### Prioridade MÉDIA

4. **Download de Fotos Alternativo**
   - Tentar extrair URLs das fotos do código JavaScript da página
   - Fazer download direto das URLs sem depender do lazy-loading

5. **Validação de Qualidade**
   - Verificar tamanho do ficheiro (> 1KB = foto real)
   - Rejeitar placeholders automaticamente
   - Retry para fotos que não carregaram

### Prioridade BAIXA

6. **Otimização**
   - Comprimir imagens para reduzir tamanho da base de dados
   - Converter todas para formato WebP (melhor compressão)
   - Criar thumbnails para listagens

---

## 🎯 PRÓXIMOS PASSOS

### Imediato
1. ✅ Executar script de download - **CONCLUÍDO**
2. ✅ Executar script de importação - **CONCLUÍDO**
3. ⏳ Parametrizar carros em falta
4. ⏳ Re-executar importação após parametrização

### Curto Prazo
5. ⏳ Melhorar download para obter fotos reais (não placeholders)
6. ⏳ Adicionar validação de qualidade de imagem
7. ⏳ Criar endpoint para visualizar fotos no frontend

### Médio Prazo
8. ⏳ Automatizar download periódico (cron job)
9. ⏳ Implementar cache de fotos
10. ⏳ Adicionar fotos de outras fontes (Booking, Rentalcars, etc.)

---

## 📝 NOTAS TÉCNICAS

### URLs das Fotos da Carjet
- **Padrão:** `https://www.carjet.com/cdn/img/cars/L/car_XXX.jpg`
- **Placeholder:** `https://www.carjet.com/cdn/img/cars/loading-car@2x.png`
- **Tamanho:** L = Large (existem também M e S)

### Códigos de Carros
- Cada carro tem um código único (ex: C45, C25, F12)
- Código está no nome do ficheiro da foto
- Pode ser usado para identificação única

### Lazy Loading
- Fotos carregam apenas quando visíveis no viewport
- Atributo `data-srcset` pode conter URL real
- Necessário scroll + wait para carregar todas

---

## ✅ CONCLUSÃO

**Sucesso Parcial:**
- ✅ Sistema de download implementado e funcional
- ✅ 74 carros mapeados com sucesso
- ✅ Fotos armazenadas na base de dados
- ⚠️ Maioria das fotos são placeholders (lazy-loading)
- ⚠️ 90 carros não parametrizados

**Próximo Objetivo:**
Parametrizar os 90 carros em falta e melhorar o download para obter fotos reais em vez de placeholders.

---

**Ficheiros de Referência:**
- `download_carjet_photos_selenium.py` - Script de download
- `import_carjet_photos_to_db.py` - Script de importação
- `carjet_cars_data.json` - Dados extraídos
- `carjet_cars_list.txt` - Lista de carros
