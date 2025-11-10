# 📸 Backup de Fotos dos Veículos

## Scripts Disponíveis

### 1. `backup_photos_from_render.py` ⭐ RECOMENDADO
Faz backup direto do PostgreSQL do Render (onde estão as fotos em produção)

### 2. `backup_vehicle_photos.py`
Faz backup da base de dados local SQLite (apenas para desenvolvimento)

### 3. `restore_vehicle_photos.py`
Restaura fotos a partir de um backup JSON

---

## Como Fazer Backup do Render

### Passo 1: Obter DATABASE_URL

**Opção A - Via Render Dashboard:**
1. Aceder a https://dashboard.render.com
2. Ir para o serviço `carrental-api-5f8q`
3. Clicar em **Environment**
4. Copiar o valor de `DATABASE_URL`

**Opção B - Via Export do Admin:**
1. Ir para https://carrental-api-5f8q.onrender.com/admin/settings
2. Clicar em **Export Configuration**
3. Descarregar o ficheiro JSON (já inclui todas as fotos)

### Passo 2: Criar ficheiro .env (Opção A)

```bash
# Criar ficheiro .env na raiz do projeto
cat > .env << 'EOF'
DATABASE_URL=postgresql://user:password@host:5432/database
EOF
```

### Passo 3: Instalar dependências

```bash
pip install psycopg2-binary python-dotenv
```

### Passo 4: Executar backup

```bash
python3 backup_photos_from_render.py
```

---

## Resultado do Backup

```
backups/vehicle_photos_render/YYYYMMDD_HHMMSS/
├── backup_complete.json        # JSON com todas as fotos em base64
├── photos/                      # Fotos individuais (vehicle_photos)
│   ├── Fiat_500.jpg
│   ├── VW_Polo.jpg
│   └── ...
└── images/                      # Imagens individuais (vehicle_images)
    ├── C25_Fiat_500.jpg
    ├── C27_VW_Polo.jpg
    └── ...
```

---

## Como Restaurar Fotos

```bash
# Executar script interativo
python3 restore_vehicle_photos.py

# Escolher backup da lista
# Confirmar restauro
```

---

## Método Alternativo (Via Admin)

### Export
1. https://carrental-api-5f8q.onrender.com/admin/settings
2. Clicar **Export Configuration**
3. Descarregar `vehicles_complete_YYYYMMDD_HHMMSS.json`

### Import
1. Mesma página Admin Settings
2. Clicar **Import Configuration**
3. Escolher ficheiro JSON
4. Upload e aguardar processamento

**Vantagens:**
- ✅ Não precisa de DATABASE_URL
- ✅ Funciona via browser
- ✅ Inclui TODOS os dados (não só fotos)

---

## Estatísticas Típicas

- **vehicle_photos**: ~300-500 fotos (carros parametrizados)
- **vehicle_images**: ~150-300 imagens (cache CarJet)
- **Tamanho total**: ~50-200 MB
- **Tempo de backup**: ~1-3 minutos

---

## Troubleshooting

### Erro: `psycopg2 not found`
```bash
pip install psycopg2-binary
```

### Erro: `DATABASE_URL not found`
- Criar ficheiro `.env` com DATABASE_URL
- OU definir variável: `export DATABASE_URL='postgresql://...'`

### Backup vazio (0 fotos)
- Estás a usar SQLite local (sem fotos)
- Usar `backup_photos_from_render.py` em vez de `backup_vehicle_photos.py`

### Fotos não aparecem no site
- Verificar se fotos existem na base de dados
- Restaurar com `restore_vehicle_photos.py`
- OU fazer upload via admin
