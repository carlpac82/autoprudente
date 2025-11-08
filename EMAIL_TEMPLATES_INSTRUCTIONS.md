# 📧 INSTRUÇÕES - Templates de Email Damage Report

## 🎯 Objetivo

Criar templates de email profissionais com:
1. **Cabeçalho** - Logo + DR Number + RA Number (fundo azul)
2. **Corpo** - Texto do email em HTML
3. **Rodapé** - Informações legais e contactos (fundo azul)

---

## 📂 Ficheiros Criados

```
email_template_pt_complete.html  (Português)
email_template_en_complete.html  (English)
email_template_fr_complete.html  (Français)
email_template_de_complete.html  (Deutsch)
```

---

## 🔧 Como Configurar (Passo a Passo)

### **1. Abrir Admin Settings**
- Ir para: `https://carrental-api-5f8q.onrender.com/admin`
- Clicar: **"Damage Report"**
- Scroll até: **"Templates de E-mail"**

### **2. Configurar Template Português (PT)**
1. Clicar na tab **🇵🇹 PT**
2. No campo **"Assunto"**, colar:
   ```
   Relatório de Danos {drNumber} - Auto Prudente
   ```

3. No campo **"Corpo do Email"**, abrir o ficheiro:
   ```
   email_template_pt_complete.html
   ```
   
4. **COPIAR TODO O CONTEÚDO** do ficheiro

5. **COLAR** no campo "Corpo do Email"

6. Clicar **"Guardar Template"**

### **3. Configurar Template Inglês (EN)**
1. Clicar na tab **🇬🇧 EN**
2. No campo **"Assunto"**, colar:
   ```
   Damage Report {drNumber} - Auto Prudente
   ```

3. Abrir o ficheiro: `email_template_en_complete.html`

4. **COPIAR TODO O CONTEÚDO**

5. **COLAR** no campo "Corpo do Email"

6. Clicar **"Guardar Template"**

### **4. Configurar Template Francês (FR)**
1. Clicar na tab **🇫🇷 FR**
2. No campo **"Assunto"**, colar:
   ```
   Rapport de Dommages {drNumber} - Auto Prudente
   ```

3. Abrir o ficheiro: `email_template_fr_complete.html`

4. **COPIAR TODO O CONTEÚDO**

5. **COLAR** no campo "Corpo do Email"

6. Clicar **"Guardar Template"**

### **5. Configurar Template Alemão (DE)**
1. Clicar na tab **🇩🇪 DE**
2. No campo **"Assunto"**, colar:
   ```
   Schadensbericht {drNumber} - Auto Prudente
   ```

3. Abrir o ficheiro: `email_template_de_complete.html`

4. **COPIAR TODO O CONTEÚDO**

5. **COLAR** no campo "Corpo do Email"

6. Clicar **"Guardar Template"**

---

## 🎨 Design do Template

### **Cabeçalho (Header)**
- Fundo: Azul gradiente (#009cb6 → #007a8f)
- Logo: À esquerda
- DR/RA: À direita (branco, negrito)

### **Corpo (Content)**
- Fundo: Branco
- Texto: Preto (#333)
- Links: Azul
- Espaçamento: 20px

### **Rodapé (Footer)**
- Fundo: Azul (#009cb6)
- Texto: Branco
- Tamanho: 12px
- Informações legais + contactos

---

## 🔄 Parâmetros Substituídos Automaticamente

O sistema substitui automaticamente:

| Placeholder | Substituído por | Exemplo |
|------------|----------------|---------|
| `{drNumber}` | Nº do DR | DR 01/2025 |
| `{raNumber}` | Nº do RA | 06424-09 |
| `{firstName}` | Nome do cliente | TAINAN |
| `{email}` | Email do cliente | cliente@exemplo.com |
| `{vehiclePlate}` | Matrícula | 30-XQ-97 |
| `{contractNumber}` | Nº Contrato | 12345 |

---

## ✅ Testar o Template

1. Ir para: **Damage Report → Histórico**
2. Clicar no **ícone envelope** de um DR
3. Modal abre com **preview do email**
4. Verificar:
   - ✅ Cabeçalho azul com logo
   - ✅ DR e RA preenchidos
   - ✅ Nome do cliente correto
   - ✅ Rodapé azul com contactos
5. Clicar **"Enviar Email"**
6. **Verificar inbox do cliente**

---

## 🖼️ Como Ficará o Email

```
┌─────────────────────────────────────┐
│  [LOGO]        Damage Report: DR... │  ← Cabeçalho Azul
│                Rental Agreement: ... │
├─────────────────────────────────────┤
│                                      │
│  Olá TAINAN,                        │
│                                      │
│  Obrigado por ter escolhido...     │  ← Corpo Branco
│  ...                                 │
│                                      │
├─────────────────────────────────────┤
│  ☏ +351 289 542 160                │
│                                      │
│  @ Auto Prudente Rent a Car        │  ← Rodapé Azul
│  You are receiving this email...    │
│  ...                                 │
└─────────────────────────────────────┘
```

---

## 🛠️ Personalizar Template

Se quiseres alterar:

### **Mudar Cor do Cabeçalho:**
```css
.header { background: linear-gradient(135deg, #009cb6 0%, #007a8f 100%); }
```
→ Alterar `#009cb6` e `#007a8f` para as cores desejadas

### **Mudar Tamanho do Logo:**
```css
.logo { height: 60px; }
```
→ Alterar `60px` para o tamanho desejado

### **Adicionar Imagem no Corpo:**
```html
<img src="https://example.com/imagem.jpg" alt="Descrição" style="max-width: 100%;">
```

### **Adicionar Link:**
```html
<a href="https://www.auto-prudente.com">Visite o nosso website</a>
```

---

## 📝 Notas Importantes

1. **Logo URL:**
   ```
   https://carrental-api-5f8q.onrender.com/static/logos/logo_autoprudente_header.png
   ```
   Se alterares o logo, atualiza este URL nos 4 templates

2. **Responsive:**
   - Templates adaptam-se a mobile/desktop
   - Largura máxima: 600px

3. **Suporte HTML:**
   - `<strong>` - Negrito
   - `<em>` - Itálico
   - `<br>` - Quebra de linha
   - `<a href="">` - Links
   - `<img src="">` - Imagens

4. **Fallback:**
   - Se faltar template, usa o default simples

---

## 🚀 Próximos Passos

1. ✅ Copiar templates para Admin Settings
2. ✅ Guardar cada idioma (PT, EN, FR, DE)
3. ✅ Testar com DR real
4. ✅ Verificar email recebido
5. ✅ Ajustar texto se necessário

---

## 📞 Contacto

Se tiveres dúvidas, contacta:
- Email: info@auto-prudente.com
- Telefone: +351 289 542 160
