# 📖 MANUAL DO UTILIZADOR - RENTAL PRICE TRACKER

## AUTOPRUDENTE
**Guia Completo de Utilização do Sistema**

![Sistema AUTOPRUDENTE](screenshots/01_homepage.png)
*Interface principal do sistema*

---

## 📋 ÍNDICE

1. [Primeiros Passos](#primeiros-passos)
2. [Pesquisa de Preços](#pesquisa-de-preços)
3. [Automação de Preços](#automação-de-preços)
4. [Gestão de Grupos](#gestão-de-grupos)
5. [Histórico](#histórico)
6. [Exportação](#exportação)
7. [Configurações](#configurações)
8. [Dicas e Truques](#dicas-e-truques)

---

## 🚀 PRIMEIROS PASSOS

### **1. Aceder ao Sistema**

1. Abrir navegador (Chrome, Firefox, Safari, Edge)
2. Ir para: `https://seu-dominio.onrender.com`
3. Fazer login com credenciais fornecidas

**Credenciais padrão:**
- Utilizador: `admin`
- Password: (fornecida pelo administrador)

### **2. Interface Principal**

Após login, verás o **Dashboard** com:
- 🔍 **Barra de pesquisa** (topo)
- 📊 **Resultados** (centro)
- ⚙️ **Menu lateral** (esquerda)
- 📈 **Gráficos** (direita)

---

## 🔍 PESQUISA DE PREÇOS

![Formulário de Pesquisa](screenshots/02_search_form.png)
*Formulário de pesquisa - Passo a passo*

### **Pesquisa Rápida**

#### **Passo 1: Selecionar Localização**
1. Clicar no dropdown **"Localização"**
2. Escolher:
   - **Faro Aeroporto (FAO)**
   - **Albufeira Cidade**

#### **Passo 2: Definir Período**
1. Clicar em **"Data de Início"**
2. Selecionar data no calendário
3. Escolher **número de dias** (1-90)

**Exemplos:**
- 7 dias = 1 semana
- 14 dias = 2 semanas
- 31 dias = 1 mês
- 60 dias = 2 meses

#### **Passo 3: Pesquisar**
1. Clicar no botão **"Pesquisar"** (azul)
2. Aguardar 20-30 segundos
3. Resultados aparecem automaticamente

![Resultados](screenshots/03_price_results.png)
*Resultados de pesquisa com comparação de preços*

### **Interpretar Resultados**

#### **Tabela de Preços:**
```
Grupo | Veículo           | Fornecedor | Preço
------|-------------------|------------|-------
B     | VW Polo           | Goldcar    | 245€
C     | VW Golf           | Centauro   | 312€
D     | Audi A3           | Sixt       | 456€
```

#### **Gráfico Visual:**
- 📊 **Barras**: Comparação por grupo
- 🎨 **Cores**: Cada grupo tem cor única
- 💰 **Valores**: Preço em euros

#### **Estatísticas:**
- **Min**: Preço mais baixo
- **Max**: Preço mais alto
- **Média**: Preço médio
- **Resultados**: Número de carros encontrados

---

## 🤖 AUTOMAÇÃO DE PREÇOS

![Automação](screenshots/04_price_automation.png)
*Interface de automação de preços*

### **1. Aceder à Automação**

1. Menu lateral → **"Automação de Preços"**
2. Ou clicar no botão **"Automatizar"** após pesquisa

### **2. Configurar Estratégia**

#### **Escolher Estratégia:**

**A) Follow Lowest (Seguir Mais Baixo)**
- Segue o preço mais baixo do mercado
- **Quando usar**: Máxima competitividade

**Configuração:**
1. Selecionar **"Follow Lowest"**
2. Escolher tipo de ajuste:
   - **Percentagem** (-10% a +50%)
   - **Euros** (-50€ a +100€)
   - **Cêntimos** (-99¢ a +99¢)
3. Definir se é **adição (+)** ou **subtração (-)**
4. Definir **preço mínimo** (ex: 150€)

**Exemplo:**
```
Preço mais baixo: 200€
Ajuste: -5%
Resultado: 190€
```

**B) Follow Suppliers (Seguir Fornecedores)**
- Segue fornecedores específicos
- **Quando usar**: Confiança em fornecedores

**Configuração:**
1. Selecionar **"Follow Suppliers"**
2. Escolher fornecedores (múltipla seleção):
   - ✅ Goldcar
   - ✅ Centauro
   - ✅ Sixt
   - ✅ Hertz
3. Definir prioridade (1 = mais importante)
4. Definir ajuste (igual ao Follow Lowest)

**C) Fixed Margin (Margem Fixa)**
- Margem percentual fixa
- **Quando usar**: Grupos premium

**Configuração:**
1. Selecionar **"Fixed Margin"**
2. Definir margem (ex: 20%)
3. Preço base: Média do mercado

**D) Fixed Price (Preço Fixo)**
- Preço fixo por período
- **Quando usar**: Promoções

**Configuração:**
1. Selecionar **"Fixed Price"**
2. Inserir preço (ex: 299€)

### **3. Aplicar por Grupo**

#### **Configuração Individual:**
1. Selecionar **grupo** (A, B, C, etc.)
2. Configurar estratégia
3. Clicar **"Guardar"**

#### **Configuração em Massa:**
1. Clicar **"Aplicar a Todos"**
2. Confirmar
3. Todos os grupos usam mesma estratégia

![Tabela Automatizada](screenshots/05_automated_prices_table.png)
*Tabela de preços automatizados com cálculos*

### **4. Visualizar Preços Automatizados**

Após configurar:
1. Tabela mostra:
   - **Preço Real**: Da pesquisa
   - **Preço Auto**: Calculado
   - **Diferença**: % de variação
2. Cores:
   - 🟢 **Verde**: Preço competitivo
   - 🟡 **Amarelo**: Preço médio
   - 🔴 **Vermelho**: Preço alto

### **5. Guardar e Exportar**

1. Clicar **"Guardar Preços"**
2. Escolher formato:
   - Excel (.xlsx)
   - CSV
   - Way2Rentals
   - Abbycar
3. Download automático

---

## 📊 GESTÃO DE GRUPOS

### **1. Ver Grupos**

1. Menu lateral → **"Grupos de Veículos"**
2. Lista de todos os grupos

### **2. Editar Grupo**

1. Clicar no grupo (ex: **Grupo B**)
2. Ver veículos incluídos
3. Editar se necessário:
   - Adicionar veículos
   - Remover veículos
   - Alterar categoria

### **3. Mapeamento de Veículos**

#### **Adicionar Veículo Novo:**
1. Clicar **"Adicionar Veículo"**
2. Inserir nome (ex: "VW Polo")
3. Selecionar grupo (ex: B)
4. Upload de foto (opcional)
5. Guardar

#### **Editar Mapeamento:**
1. Procurar veículo
2. Clicar **"Editar"**
3. Alterar grupo ou nome
4. Guardar

### **4. Veículos Não Mapeados**

Se aparecerem veículos em **"Others - Not Parameterized"**:

1. Clicar no veículo
2. Selecionar grupo correto
3. Confirmar
4. Veículo é mapeado automaticamente

---

## 📈 HISTÓRICO

![Histórico](screenshots/06_history_tab.png)
*Tabs de histórico com múltiplas opções*

### **1. Histórico de Preços**

#### **Ver Histórico:**
1. Menu lateral → **"Histórico"**
2. Selecionar tipo:
   - **Preços Atuais**
   - **Preços Automatizados**

#### **Filtrar:**
1. Por **localização** (Faro, Albufeira)
2. Por **mês/ano**
3. Por **grupo**

#### **Comparar Versões:**
1. Selecionar 2 datas
2. Clicar **"Comparar"**
3. Ver diferenças

![Histórico de Pesquisas](screenshots/07_automated_search_history.png)
*Histórico de pesquisas automatizadas*

### **2. Histórico de Pesquisas**

#### **Ver Pesquisas:**
1. Menu lateral → **"Histórico de Pesquisas"**
2. Lista de todas as pesquisas

#### **Detalhes:**
- Data e hora
- Localização
- Período pesquisado
- Número de resultados
- Preços (min, max, média)

### **3. Editar Histórico**

1. Clicar em qualquer entrada
2. Tabela abre com preços
3. Editar valores se necessário
4. Guardar com data atual

---

## 📤 EXPORTAÇÃO

### **1. Exportar para Excel**

#### **Passo a Passo:**
1. Após pesquisa, clicar **"Exportar"**
2. Selecionar **"Excel (.xlsx)"**
3. Escolher opções:
   - ✅ Incluir gráficos
   - ✅ Formatação colorida
   - ✅ Múltiplas sheets
4. Clicar **"Download"**

#### **Conteúdo do Excel:**
- **Sheet 1**: Preços por grupo
- **Sheet 2**: Estatísticas
- **Sheet 3**: Gráficos
- **Sheet 4**: Detalhes completos

### **2. Exportar para Brokers**

#### **Way2Rentals:**
1. Clicar **"Exportar"**
2. Selecionar **"Way2Rentals"**
3. Escolher período
4. Download automático
5. Upload no portal Way2Rentals

#### **Abbycar:**
1. Clicar **"Exportar"**
2. Selecionar **"Abbycar"**
3. Escolher localização
4. Download automático
5. Upload no portal Abbycar

### **3. Histórico de Exports**

1. Menu lateral → **"Exports"**
2. Ver todos os exports realizados
3. Re-download disponível
4. Detalhes:
   - Data de export
   - Broker
   - Período
   - Utilizador

---

## ⚙️ CONFIGURAÇÕES

### **1. Configurações de Pesquisa**

#### **Dias Personalizados:**
1. Menu → **"Configurações"**
2. Secção **"Dias de Pesquisa"**
3. Adicionar/remover dias
4. Exemplo: `7, 14, 21, 31, 60, 90`

#### **Localizações:**
1. Ativar/desativar localizações
2. Adicionar novas (se necessário)

### **2. Configurações de Automação**

#### **Preços Mínimos:**
1. Menu → **"Configurações"** → **"Preços Mínimos"**
2. Definir por grupo:
   ```
   Grupo A: 100€
   Grupo B: 120€
   Grupo C: 150€
   Grupo D: 200€
   ```

#### **Margens Padrão:**
1. Definir margem padrão (ex: 15%)
2. Aplicável a todos os grupos

### **3. Notificações**

#### **Configurar Alertas:**
1. Menu → **"Notificações"**
2. Ativar tipos:
   - ✅ Preços fora de range
   - ✅ Novos veículos
   - ✅ Mudanças de mercado
3. Definir destinatários (emails)
4. Frequência (diário, semanal)

#### **Relatórios Automáticos:**
1. Ativar relatórios:
   - ✅ Relatório diário
   - ✅ Relatório semanal
   - ✅ Relatório mensal
2. Hora de envio (ex: 09:00)
3. Destinatários

### **4. Utilizadores**

#### **Adicionar Utilizador:**
1. Menu → **"Utilizadores"** (admin only)
2. Clicar **"Novo Utilizador"**
3. Inserir:
   - Nome
   - Email
   - Password
   - Role (admin, user, viewer)
4. Guardar

#### **Permissões:**
- **Admin**: Tudo
- **User**: Pesquisar, automatizar, exportar
- **Viewer**: Apenas visualizar

---

## 💡 DICAS E TRUQUES

### **1. Pesquisa Eficiente**

**Dica 1: Pesquisar Múltiplos Períodos**
- Usar "Pesquisa Rápida" para vários dias
- Exemplo: 7, 14, 31 dias de uma vez
- Comparar tendências

**Dica 2: Horário Ideal**
- Pesquisar de manhã (09:00-11:00)
- Preços mais estáveis
- Menos tráfego no site

**Dica 3: Guardar Pesquisas**
- Sempre guardar pesquisas importantes
- Usar histórico para comparar
- Análise de tendências

### **2. Automação Inteligente**

**Dica 1: Estratégias Mistas**
- Usar "Follow Lowest" para grupos económicos (A, B, C)
- Usar "Fixed Margin" para grupos premium (D, E, F)
- Usar "Fixed Price" para promoções

**Dica 2: Ajustes Sazonais**
- Alta temporada: Margens maiores (+20%)
- Baixa temporada: Preços competitivos (-5%)
- Eventos especiais: Preços fixos

**Dica 3: Preços Mínimos**
- Sempre definir preços mínimos
- Protege de preços muito baixos
- Garante rentabilidade

### **3. Análise de Mercado**

**Dica 1: Comparar Histórico**
- Ver evolução de preços
- Identificar padrões
- Antecipar mudanças

**Dica 2: Monitorizar Concorrência**
- Ver quais fornecedores são mais competitivos
- Ajustar estratégias
- Manter vantagem

**Dica 3: Usar AI Learning**
- Sistema aprende com ajustes manuais
- Sugestões melhoram com tempo
- Confiar nas recomendações

### **4. Exportação Profissional**

**Dica 1: Excel Completo**
- Sempre incluir gráficos
- Usar formatação colorida
- Facilita apresentações

**Dica 2: Nomear Ficheiros**
- Usar nomes descritivos
- Exemplo: `Precos_Faro_Jan2025.xlsx`
- Facilita organização

**Dica 3: Backup Regular**
- Exportar semanalmente
- Guardar em cloud (Google Drive, Dropbox)
- Segurança de dados

---

## 🆘 RESOLUÇÃO DE PROBLEMAS

### **Problema 1: Pesquisa Não Retorna Resultados**

**Soluções:**
1. Verificar ligação à internet
2. Tentar outra localização
3. Alterar período (ex: 7 dias em vez de 60)
4. Aguardar 5 minutos e tentar novamente
5. Contactar suporte se persistir

### **Problema 2: Preços Automatizados Estranhos**

**Soluções:**
1. Verificar estratégia configurada
2. Confirmar preços mínimos
3. Ver se ajuste está correto (+ ou -)
4. Recalcular preços
5. Ajustar configuração se necessário

### **Problema 3: Export Não Funciona**

**Soluções:**
1. Verificar se há dados para exportar
2. Tentar outro formato (CSV em vez de Excel)
3. Limpar cache do navegador
4. Tentar noutro navegador
5. Contactar suporte

### **Problema 4: Veículos Não Mapeados**

**Soluções:**
1. Ir para "Grupos de Veículos"
2. Procurar veículo em "Not Parameterized"
3. Mapear manualmente
4. Guardar
5. Pesquisar novamente

---

## 📞 SUPORTE

### **Contactos:**
- **Email**: suporte@autoprudente.pt
- **Telefone**: +351 XXX XXX XXX
- **Horário**: Segunda a Sexta, 09:00-18:00

### **Recursos Adicionais:**
- 📚 **Base de Conhecimento**: [link]
- 🎥 **Vídeos Tutorial**: [link]
- 💬 **Chat Online**: Disponível no sistema
- 📧 **Newsletter**: Atualizações mensais

---

## 📝 NOTAS IMPORTANTES

### **Boas Práticas:**
1. ✅ Fazer backup regular dos dados
2. ✅ Guardar pesquisas importantes
3. ✅ Verificar preços mínimos regularmente
4. ✅ Monitorizar concorrência semanalmente
5. ✅ Ajustar estratégias sazonalmente

### **Segurança:**
1. 🔒 Nunca partilhar password
2. 🔒 Fazer logout após usar
3. 🔒 Usar password forte
4. 🔒 Não aceder de computadores públicos
5. 🔒 Reportar atividade suspeita

### **Atualizações:**
- Sistema atualizado automaticamente
- Novas funcionalidades mensalmente
- Melhorias contínuas
- Feedback bem-vindo

---

## 🎓 GLOSSÁRIO

**Termos Importantes:**

- **Grupo**: Categoria de veículos (A, B, C, etc.)
- **Snapshot**: Registo de preços num momento
- **Estratégia**: Método de cálculo de preços
- **Broker**: Intermediário (Way2Rentals, Abbycar)
- **Margem**: Diferença entre custo e preço venda
- **AI Learning**: Aprendizagem automática
- **Export**: Exportação de dados
- **Scraping**: Recolha automática de dados
- **Follow Lowest**: Seguir preço mais baixo
- **Fixed Margin**: Margem fixa

---

## 📊 ATALHOS DE TECLADO

**Navegação Rápida:**
- `Ctrl + P`: Nova pesquisa
- `Ctrl + A`: Automação
- `Ctrl + E`: Exportar
- `Ctrl + H`: Histórico
- `Ctrl + S`: Guardar
- `Ctrl + Q`: Logout

**Edição:**
- `Ctrl + Z`: Desfazer
- `Ctrl + Y`: Refazer
- `Ctrl + C`: Copiar
- `Ctrl + V`: Colar

---

*Manual do Utilizador - Versão 2.0*  
*Última Atualização: Novembro 2025*  
*© 2025 AUTOPRUDENTE - Todos os direitos reservados*
