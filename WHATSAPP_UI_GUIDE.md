# 📱 WhatsApp Dashboard - Guia de Utilização

## ✅ O Que Foi Corrigido

### 1. **Scroll nas Mensagens**
- ✅ Área de mensagens agora tem **altura fixa** com scroll automático
- ✅ Mensagens não ultrapassam mais a página
- ✅ Layout: `height: calc(100vh - 280px)` - adapta-se à altura da janela

### 2. **Botão Eliminar Mensagens**
- ✅ Aparece ao **passar o mouse** sobre qualquer mensagem
- ✅ Posição: **canto superior direito** da bolha da mensagem
- ✅ Ícone: **❌ vermelho circular**
- ✅ Efeito visual: mensagem ganha sombra quando hover

### 3. **Menu Arquivar/Eliminar Conversa**
- ✅ Botão **⋮** (três pontos) no header da conversa
- ✅ Ao lado dos botões "Resolver" e "Atribuir a Mim"
- ✅ Menu dropdown com 3 opções:
  - 📥 Exportar Conversa
  - 📦 Arquivar
  - 🗑️ Eliminar

---

## 🎯 Como Usar

### **Eliminar Mensagem Individual**

1. **Abra uma conversa** no WhatsApp Dashboard
2. **Passe o mouse** sobre a mensagem que quer eliminar
3. Aparece botão **❌ vermelho** no canto superior direito da mensagem
4. **Clique no botão**
5. Confirme a eliminação
6. Mensagem é removida imediatamente

**Dica:** A mensagem ganha uma **sombra** quando passa o mouse para mostrar que está ativa.

---

### **Arquivar Conversa**

1. **Abra a conversa** que quer arquivar
2. No **header da conversa**, clique no botão **⋮** (três pontos verticais)
3. Aparece menu dropdown
4. Clique em **"📦 Arquivar"**
5. Confirme
6. Conversa é ocultada da lista principal

**Para ver conversas arquivadas:** Use o filtro na lista de conversas.

---

### **Eliminar Conversa Permanentemente**

⚠️ **ATENÇÃO:** Esta ação é **irreversível**!

1. **Abra a conversa** que quer eliminar
2. No **header da conversa**, clique no botão **⋮** (três pontos verticais)
3. Aparece menu dropdown
4. Clique em **"🗑️ Eliminar"** (texto em vermelho)
5. **Confirme duas vezes**:
   - Primeira confirmação: "Tem a certeza?"
   - Segunda confirmação automática
6. Conversa e **todas as mensagens** são apagadas da base de dados

**O que é eliminado:**
- ✅ Todas as mensagens da conversa
- ✅ Histórico completo
- ✅ Metadados (última mensagem, contador não lidos, etc.)

---

## 📐 Layout Visual

```
┌─────────────────────────────────────────────────────────┐
│  WhatsApp Dashboard                    [Conectado] [⚙️]  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌───────────┐  ┌──────────────────────────────────┐   │
│  │           │  │ 👤 Filipe Pacheco    +351912...  │   │
│  │ Conversas │  │ [Resolver] [Atribuir] [⋮ Menu]   │   │
│  │           │  ├──────────────────────────────────┤   │
│  │ - João    │  │ ┌───────────────────────────┐ ❌ │   │
│  │ - Maria   │  │ │ Olá! Bom dia             │    │ <- Hover mostra ❌
│  │ - Pedro   │  │ └───────────────────────────┘    │   │
│  │           │  │          ┌──────────────────┐    │   │
│  │           │  │          │ Bom dia! Como    │    │   │
│  │           │  │          │ posso ajudar?    │    │   │
│  │           │  │          └──────────────────┘    │   │
│  │           │  │                                   │   │
│  │           │  │ SCROLL ↕️ (altura fixa)          │   │
│  │           │  │                                   │   │
│  └───────────┘  └──────────────────────────────────┘   │
│                  [😀] [📷] [📎] [Digite mensagem...] [➤]│
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Cores e Estilos

### **Mensagens Recebidas (Inbound)**
- **Posição:** Lado ESQUERDO
- **Cor de fundo:** Amarelo claro `rgba(245, 158, 11, 0.2)`
- **Borda:** Arredondada (exceto canto superior esquerdo)
- **Exemplo:** Mensagens de clientes

### **Mensagens Enviadas (Outbound)**
- **Posição:** Lado DIREITO
- **Cor de fundo:** Azul claro `rgba(0, 156, 182, 0.2)`
- **Borda:** Arredondada (exceto canto superior direito)
- **Exemplo:** Mensagens que você enviou

### **Botão Eliminar Mensagem**
- **Cor:** Vermelho `#EF4444`
- **Formato:** Circular
- **Tamanho:** 28px × 28px
- **Ícone:** ❌ (X branco)
- **Hover:** Vermelho mais escuro `#DC2626`
- **Sombra:** `shadow-lg` para destacar

### **Menu Dropdown (⋮)**
- **Fundo:** Branco
- **Borda:** Cinza claro
- **Sombra:** `shadow-lg`
- **Item Eliminar:** Texto vermelho `#DC2626`

---

## 🔧 Configurações Técnicas

### **Altura da Área de Mensagens**
```css
height: calc(100vh - 280px);
overflow-y: auto;
```

### **Efeito Hover nas Mensagens**
```css
.group:hover .message-bubble {
    box-shadow: 0 2px 8px rgba(0,0,0,.2);
}
```

### **Botão Eliminar (Visibility)**
```css
.opacity-0 .group-hover:opacity-100
```
- Invisível por padrão
- Aparece apenas em hover

---

## 🐛 Troubleshooting

### **"Não vejo o botão eliminar ao passar o mouse"**

**Soluções:**
1. Verificar que está a usar **browser moderno** (Chrome, Firefox, Edge, Safari)
2. Limpar cache do browser: `Ctrl+Shift+Delete`
3. Fazer hard refresh: `Ctrl+F5` ou `Cmd+Shift+R`
4. Verificar que JavaScript está ativado
5. Verificar que não há bloqueador de scripts ativo

**Como testar:**
- Abrir **DevTools** (F12)
- Passar mouse sobre mensagem
- Verificar no **Inspector** se classe `group-hover:opacity-100` está a aplicar

---

### **"Menu ⋮ não aparece"**

**Verificações:**
1. Abrir conversa (clicar em contacto)
2. Procurar no **header superior** (junto ao nome do contacto)
3. Está ao lado direito dos botões "Resolver" e "Atribuir a Mim"
4. Se não vê, verificar largura da janela (pode estar escondido em mobile)

---

### **"Área de mensagens não tem scroll"**

**Causas possíveis:**
1. Poucas mensagens (menos que a altura visível)
2. CSS não aplicado corretamente

**Teste:**
1. Enviar várias mensagens de teste (>10)
2. Verificar se barra de scroll aparece à direita
3. Deve poder scrollar para cima/baixo

---

## 📱 Responsividade

### **Desktop (>1024px)**
- ✅ Lista de conversas: 33% largura
- ✅ Área de mensagens: 67% largura
- ✅ Botão eliminar: sempre visível em hover

### **Tablet (768px - 1024px)**
- ✅ Layout adaptativo
- ✅ Menu ⋮ pode colapsar

### **Mobile (<768px)**
- ⚠️ Recomenda-se usar versão desktop
- Menu pode estar em formato hamburger

---

## 🎓 Boas Práticas

### **Eliminar Mensagens**
- ✅ Use para remover mensagens duplicadas
- ✅ Use para limpar testes
- ⚠️ Cuidado: não há "undo"!

### **Arquivar Conversas**
- ✅ Use para conversas resolvidas mas que quer manter histórico
- ✅ Reduz clutter na lista principal
- ✅ Pode desarquivar depois se necessário

### **Eliminar Conversas**
- ⚠️ Apenas use quando tem CERTEZA absoluta
- ⚠️ Faça backup antes (botão Exportar)
- ❌ NÃO use para conversas ativas de clientes
- ✅ Use apenas para spam ou testes

---

## 📞 Suporte

**Se problemas persistirem:**

1. **Verificar logs do browser:**
   - F12 → Console
   - Procurar erros em vermelho

2. **Verificar deploy Render:**
   - https://dashboard.render.com
   - Ver logs do servidor

3. **Limpar dados e recarregar:**
   ```
   1. Ctrl+Shift+Delete (Chrome)
   2. Limpar cache e cookies
   3. Fechar browser
   4. Abrir novamente
   5. Fazer login
   ```

4. **Testar em modo privado/incognito:**
   - Ctrl+Shift+N (Chrome)
   - Cmd+Shift+N (Chrome Mac)
   - Abre sem extensões/cache

---

## ✅ Checklist Pós-Deploy

- [ ] WhatsApp Dashboard abre sem erros
- [ ] Conversas carregam corretamente
- [ ] Mensagens aparecem com cores corretas (amarelo/azul)
- [ ] Área de mensagens tem scroll quando há muitas mensagens
- [ ] Botão ❌ vermelho aparece ao passar mouse sobre mensagem
- [ ] Menu ⋮ está visível no header da conversa
- [ ] Clicar em Eliminar mensagem funciona
- [ ] Clicar em Arquivar conversa funciona
- [ ] Clicar em Eliminar conversa pede confirmação
- [ ] Mensagens novas recebidas aparecem em tempo real

---

**Última atualização:** 15 Nov 2025  
**Versão:** 2.0 - Com UI melhorada e opções de gestão
