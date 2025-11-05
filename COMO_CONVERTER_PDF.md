# 📄 COMO CONVERTER PARA PDF

## 🎯 OPÇÃO 1: Script Automático (RECOMENDADO)

### **Passo 1: Instalar Dependências**

```bash
pip install markdown2 weasyprint pillow
```

### **Passo 2: Executar Script**

```bash
cd /Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay
python convert_to_pdf.py
```

### **Resultado:**
- ✅ `FUNCIONALIDADES_SISTEMA.pdf` criado
- ✅ `MANUAL_UTILIZADOR.pdf` criado
- ✅ Header azul AUTOPRUDENTE incluído
- ✅ Logo incluído
- ✅ Formatação profissional

---

## 🎨 OPÇÃO 2: Online (Sem Instalação)

### **Site 1: Markdown to PDF**
1. Ir para: https://www.markdowntopdf.com/
2. Upload `FUNCIONALIDADES_SISTEMA.md`
3. Download PDF
4. Repetir para `MANUAL_UTILIZADOR.md`

### **Site 2: CloudConvert**
1. Ir para: https://cloudconvert.com/md-to-pdf
2. Upload ficheiros `.md`
3. Converter
4. Download PDFs

**Nota:** Estes sites NÃO incluem o header azul e logo automaticamente.

---

## 🖥️ OPÇÃO 3: VS Code

### **Passo 1: Instalar Extensão**
1. Abrir VS Code
2. Extensions (Ctrl+Shift+X)
3. Procurar: **"Markdown PDF"**
4. Instalar

### **Passo 2: Converter**
1. Abrir `FUNCIONALIDADES_SISTEMA.md`
2. `Ctrl+Shift+P` (Command Palette)
3. Escrever: "Markdown PDF: Export (pdf)"
4. Enter
5. PDF criado na mesma pasta

**Nota:** Para adicionar header personalizado, criar ficheiro `markdown-pdf.css`

---

## 🎨 ADICIONAR LOGO REAL

Se quiseres usar o logo real da AUTOPRUDENTE:

### **Passo 1: Preparar Logo**
1. Ter ficheiro `logo.png` ou `logo.jpg`
2. Copiar para pasta do projeto
3. Tamanho recomendado: 300x120 pixels

### **Passo 2: Editar Script**
Abrir `convert_to_pdf.py` e alterar linha do logo:

```python
# ANTES:
.logo {{
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: #1e3a8a;
    font-size: 18pt;
}}

# DEPOIS:
.logo {{
    background: url('logo.png') no-repeat center center;
    background-size: contain;
}}
```

---

## 🎨 PERSONALIZAR CORES

Para alterar as cores do header:

### **Azul Atual:**
- Primário: `#1e3a8a`
- Secundário: `#3b82f6`

### **Alterar no Script:**
Procurar por `#1e3a8a` e `#3b82f6` e substituir pelas cores da AUTOPRUDENTE.

---

## ❌ RESOLUÇÃO DE PROBLEMAS

### **Erro: "No module named 'markdown2'"**
```bash
pip install markdown2
```

### **Erro: "No module named 'weasyprint'"**
```bash
pip install weasyprint
```

**Mac:**
```bash
brew install cairo pango gdk-pixbuf libffi
pip install weasyprint
```

### **Erro: "Permission denied"**
```bash
chmod +x convert_to_pdf.py
python convert_to_pdf.py
```

---

## 📊 CARACTERÍSTICAS DOS PDFs GERADOS

### ✅ **Incluído:**
- Header azul AUTOPRUDENTE
- Logo (placeholder ou real)
- Numeração de páginas
- Índice clicável
- Tabelas formatadas
- Código com syntax highlight
- Emojis preservados
- Footer com copyright

### 🎨 **Estilo:**
- Fonte: Segoe UI (profissional)
- Cores: Azul AUTOPRUDENTE
- Layout: A4
- Margens: 2cm

---

## 📞 SUPORTE

Se tiveres problemas:
1. Verificar se Python está instalado: `python --version`
2. Verificar se pip funciona: `pip --version`
3. Instalar dependências novamente
4. Executar script com `python3` em vez de `python`

---

**Boa sorte com a conversão!** 🎉
