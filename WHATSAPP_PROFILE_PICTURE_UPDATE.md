# Como Atualizar Foto de Perfil dos Contactos WhatsApp

## ✅ Implementado (Nov 15, 2025)

### 🎯 Funcionalidade

Sistema completo para fazer upload e atualizar fotos de perfil dos contactos WhatsApp no dashboard.

## 🖼️ Como Usar

### 1. **Abrir Conversa**
- Ir para WhatsApp Dashboard
- Clicar numa conversa/contacto da lista

### 2. **Aceder à Opção de Foto**
- Passar o rato sobre o avatar circular no header do chat
- Aparece um ícone de câmera cinza com fundo semi-transparente

### 3. **Fazer Upload**
- Clicar no avatar ou no ícone de câmera
- Abre modal "Atualizar Foto de Perfil"
- Clicar na área de upload ou arrastar imagem
- Visualizar preview da foto (circular, 64x64px)
- Ver nome e tamanho do ficheiro
- Clicar "Guardar"

### 4. **Resultado**
- ✅ Foto atualizada no avatar do header
- ✅ Foto atualizada na lista de conversas
- ✅ Foto guardada no servidor (pasta e BD)

## 🔧 Implementação Técnica

### Backend - Endpoint API

**URL:** `PUT /api/whatsapp/contacts/{contact_id}/picture`

**Aceita:**
- Upload de ficheiro (FormData com campo `picture`)
- URL de imagem (campo `picture_url`)

**Validações:**
- Tipo de ficheiro: apenas imagens
- Tamanho máximo: 5MB
- Contacto deve existir

**Guardar:**
- Ficheiro salvo em: `/static/whatsapp_profiles/contact_{id}_{random}.{ext}`
- URL guardada na coluna `profile_picture_url` da tabela `whatsapp_conversations`

**Resposta:**
```json
{
  "ok": true,
  "success": true,
  "message": "Foto de perfil atualizada com sucesso",
  "profile_picture_url": "/static/whatsapp_profiles/contact_1_a3f2b8c4.jpg"
}
```

### Frontend - UI/UX

**Componentes:**

1. **Avatar Interativo (Header do Chat):**
```html
<div class="relative group">
    <div id="chat-avatar-container" class="w-10 h-10 avatar-circle rounded-full">
        <i class="far fa-user text-white"></i>
    </div>
    <!-- Camera icon on hover -->
    <div class="absolute inset-0 bg-black bg-opacity-50 rounded-full opacity-0 group-hover:opacity-100">
        <i class="fas fa-camera text-white"></i>
    </div>
</div>
```

2. **Modal de Upload:**
- Preview circular da imagem
- Nome e tamanho do ficheiro
- Drag & drop ou clique
- Botões: Cancelar e Guardar
- Loading spinner durante upload

**Funções JavaScript:**

- `openProfilePictureModal()` - Abre modal
- `closeProfilePictureModal()` - Fecha modal
- `handleProfilePictureUpload(event)` - Processa ficheiro selecionado
- `clearProfilePicturePreview()` - Limpa preview
- `uploadProfilePicture()` - Faz upload para servidor
- `selectConversation()` - Atualizada para mostrar foto no header

### Base de Dados

**Tabela:** `whatsapp_conversations`

**Coluna:** `profile_picture_url` (TEXT)

Guarda URL relativa da foto:
- Exemplo: `/static/whatsapp_profiles/contact_5_a3f2b8c4.jpg`

**Quando preenche:**
- Upload manual (este sistema)
- Verificação automática via WhatsApp API
- Import de contactos com fotos

## 📁 Estrutura de Ficheiros

```
static/
└── whatsapp_profiles/
    ├── .gitignore          # Ignora imagens (*.jpg, *.png, etc)
    ├── .gitkeep            # Mantém pasta no git
    └── contact_1_*.jpg     # Fotos dos contactos (não versionadas)
```

## 🎨 Design

**Ícone de Câmera no Hover:**
- Fundo: `bg-black bg-opacity-50`
- Ícone: Font Awesome `fa-camera`
- Transição suave: `opacity-0 group-hover:opacity-100`

**Modal:**
- Fundo branco com sombra
- Área de upload: borda tracejada hover azul
- Preview: circular 64x64px
- Botões: Cinza (cancelar) e Azul (guardar)

**Lista de Conversas:**
- Avatar atualizado automaticamente após upload
- Fallback: ícone user se sem foto

## ⚙️ Configurações

**Validações:**
- Formato: `image/*` (PNG, JPG, JPEG, GIF, WEBP)
- Tamanho máximo: 5 MB (5 * 1024 * 1024 bytes)
- Nome único: `contact_{id}_{uuid}.{ext}`

**Pasta de Upload:**
- Criada automaticamente se não existir: `os.makedirs("static/whatsapp_profiles", exist_ok=True)`

## 🧪 Como Testar

### 1. Local (Desenvolvimento)
```bash
# Criar pasta se não existir
mkdir -p static/whatsapp_profiles

# Iniciar servidor
python main.py

# Aceder ao WhatsApp Dashboard
# http://localhost:8000/whatsapp/dashboard

# Clicar numa conversa
# Hover sobre avatar → câmera aparece
# Clicar para fazer upload
```

### 2. Produção (Render)
```
1. Deploy automático após push
2. Pasta static/whatsapp_profiles criada no servidor
3. Aceder: https://carrental-api-5f8q.onrender.com/whatsapp/dashboard
4. Testar upload de foto
5. Verificar se foto persiste após refresh
```

## 📊 Fluxo Completo

```
User                    Frontend                Backend                 Database
  │                         │                       │                        │
  │  Hover avatar          │                       │                        │
  ├────────────────────────>│                       │                        │
  │  Câmera aparece         │                       │                        │
  │                         │                       │                        │
  │  Clica câmera          │                       │                        │
  ├────────────────────────>│                       │                        │
  │  Modal abre             │                       │                        │
  │                         │                       │                        │
  │  Seleciona imagem      │                       │                        │
  ├────────────────────────>│                       │                        │
  │  Preview circular       │                       │                        │
  │                         │                       │                        │
  │  Clica Guardar         │                       │                        │
  ├────────────────────────>│  PUT /api/...        │                        │
  │                         ├──────────────────────>│                        │
  │                         │                       │  Valida imagem         │
  │                         │                       │  Salva ficheiro        │
  │                         │                       │  UPDATE conversation   │
  │                         │                       ├───────────────────────>│
  │                         │                       │<───────────────────────┤
  │                         │<──────────────────────┤                        │
  │  ✅ Foto atualizada     │  {ok, url}            │                        │
  │<────────────────────────┤                       │                        │
  │  Avatar atualizado      │                       │                        │
  │  Lista atualizada       │                       │                        │
```

## 🔒 Segurança

**Validações no Backend:**
- ✅ Requer autenticação (`require_auth`)
- ✅ Valida formato de ficheiro
- ✅ Valida tamanho (5MB max)
- ✅ Valida existência do contacto
- ✅ Nome de ficheiro único (UUID)
- ✅ Sanitização de extensão

**Validações no Frontend:**
- ✅ Valida tipo `image/*`
- ✅ Valida tamanho antes de upload
- ✅ Preview seguro (FileReader)
- ✅ Desabilita botão durante upload
- ✅ Feedback de erro claro

## 📝 Notas

- Fotos não são versionadas no Git (`.gitignore`)
- Fotos antigas não são eliminadas automaticamente (TODO: cleanup)
- Fotos da WhatsApp API têm prioridade (se existirem)
- Compatível com PostgreSQL e SQLite
- Suporta múltiplos formatos de imagem

## 🐛 Troubleshooting

**Foto não aparece após upload:**
- Verificar logs: `[WHATSAPP] 💾 Saved profile picture: ...`
- Verificar permissões da pasta `static/whatsapp_profiles/`
- Verificar se URL está correto na BD
- Hard refresh do browser (Ctrl+Shift+R)

**Upload falha:**
- Verificar tamanho da imagem (<5MB)
- Verificar formato (PNG, JPG, etc)
- Verificar logs do servidor
- Verificar se contacto existe

**Foto não persiste:**
- Verificar se está a guardar na BD (não só localStorage)
- Verificar coluna `profile_picture_url` na tabela
- Verificar deploy do código no Render

## 📦 Ficheiros Modificados

**Backend:**
- `main.py`: Endpoint `PUT /api/whatsapp/contacts/{contact_id}/picture` (linhas 6293-6400)

**Frontend:**
- `templates/whatsapp_dashboard.html`:
  - Avatar com hover câmera (linhas 203-211)
  - Modal de upload (linhas 321-372)
  - Funções JavaScript (linhas 1158-1259)
  - Atualização em `selectConversation()` (linhas 580-585)

**Estrutura:**
- `static/whatsapp_profiles/.gitkeep` - Pasta vazia
- `static/whatsapp_profiles/.gitignore` - Ignora imagens
