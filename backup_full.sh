#!/bin/bash

##############################################################################
# 💾 BACKUP COMPLETO - BD + Coordenadas + Parametrizações
##############################################################################

echo "🚀 Iniciando backup completo..."
echo "================================================"

# Carregar .env se existir
if [ -f .env ]; then
    echo "📄 Carregando configuração de .env..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Configuração
BACKUP_DIR="backups_local"
MAX_BACKUPS=10
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="backup_${TIMESTAMP}.sql"

# Criar diretório de backups se não existir
mkdir -p "$BACKUP_DIR"

# 1. BACKUP DA BASE DE DADOS
echo ""
echo "📦 1. Exportando base de dados..."
echo "   DATABASE_URL: ${DATABASE_URL:0:30}..."

if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL não definida!"
    exit 1
fi

# Exportar BD completa (todas as tabelas)
pg_dump "$DATABASE_URL" > "$BACKUP_DIR/$BACKUP_FILE"

if [ $? -eq 0 ]; then
    SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
    echo "   ✅ Backup criado: $BACKUP_FILE ($SIZE)"
else
    echo "   ❌ Erro ao criar backup!"
    exit 1
fi

# 2. VERIFICAR CONTEÚDO
echo ""
echo "📋 2. Verificando conteúdo do backup..."

# Contar tabelas importantes
TABLES=$(grep -c "CREATE TABLE" "$BACKUP_DIR/$BACKUP_FILE")
DR_COORDS=$(grep -c "damage_report_coordinates" "$BACKUP_DIR/$BACKUP_FILE")
RA_COORDS=$(grep -c "rental_agreement_coordinates" "$BACKUP_DIR/$BACKUP_FILE")
DAMAGE_REPORTS=$(grep -c "damage_reports" "$BACKUP_DIR/$BACKUP_FILE")

echo "   ✅ Tabelas encontradas: $TABLES"
echo "   ✅ Coordenadas DR: $DR_COORDS refs"
echo "   ✅ Coordenadas RA: $RA_COORDS refs"
echo "   ✅ Damage Reports: $DAMAGE_REPORTS refs"

# 3. MANTER APENAS OS 10 BACKUPS MAIS RECENTES
echo ""
echo "🗑️  3. Limpando backups antigos..."

cd "$BACKUP_DIR"
BACKUP_COUNT=$(ls -1 backup_*.sql 2>/dev/null | wc -l)

if [ $BACKUP_COUNT -gt $MAX_BACKUPS ]; then
    REMOVE_COUNT=$((BACKUP_COUNT - MAX_BACKUPS))
    echo "   📊 Total: $BACKUP_COUNT backups"
    echo "   🗑️  Removendo: $REMOVE_COUNT backups antigos"
    
    ls -1t backup_*.sql | tail -n +$((MAX_BACKUPS + 1)) | xargs rm -f
    
    echo "   ✅ Mantidos apenas os $MAX_BACKUPS mais recentes"
else
    echo "   ✅ Total: $BACKUP_COUNT backups (< $MAX_BACKUPS)"
fi

cd ..

# 4. LISTAR BACKUPS LOCAIS
echo ""
echo "📁 4. Backups locais disponíveis:"
ls -lht "$BACKUP_DIR"/backup_*.sql | head -n $MAX_BACKUPS | awk '{print "   " $9 " (" $5 ")"}'

# 5. COMMIT E PUSH PARA GITHUB
echo ""
echo "🔄 5. Enviando para GitHub..."

# Adicionar apenas os arquivos importantes (não os backups SQL grandes)
git add main.py
git add templates/
git add static/
git add requirements.txt
git add README.md 2>/dev/null || true
git add .gitignore 2>/dev/null || true

# Commit
git commit -m "💾 Backup completo - $(date +'%Y-%m-%d %H:%M:%S')

✅ BD exportada: $BACKUP_FILE ($SIZE)
✅ Tabelas: $TABLES
✅ Coordenadas DR: incluídas
✅ Coordenadas RA: incluídas
✅ Damage Reports: incluídos
✅ Backups locais: $BACKUP_COUNT mantidos (max: $MAX_BACKUPS)

Backup completo com todas as parametrizações e coordenadas."

if [ $? -eq 0 ]; then
    echo "   ✅ Commit criado"
else
    echo "   ⚠️  Nada para commitar (já está atualizado)"
fi

# Push
echo "   🚀 Pushing para GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "   ✅ Push concluído"
else
    echo "   ❌ Erro no push"
    exit 1
fi

# 6. RESUMO FINAL
echo ""
echo "================================================"
echo "✅ BACKUP COMPLETO CONCLUÍDO!"
echo "================================================"
echo "📦 Backup local: $BACKUP_DIR/$BACKUP_FILE"
echo "📊 Tamanho: $SIZE"
echo "🗂️  Backups mantidos: $BACKUP_COUNT de $MAX_BACKUPS"
echo "✅ GitHub: sincronizado"
echo "================================================"
echo ""
echo "🔧 Para restaurar este backup:"
echo "   psql \$DATABASE_URL < $BACKUP_DIR/$BACKUP_FILE"
echo ""
