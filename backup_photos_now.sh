#!/bin/bash

# Script para fazer backup automático das fotos após deploy
# Aguarda Render fazer deploy e executa backup via API

BASE_URL="https://carrental-api-5f8q.onrender.com"
BACKUP_SCRIPT="backup_photos_via_api.py"

echo "============================================================"
echo "🚨 BACKUP URGENTE DE FOTOS DOS VEÍCULOS"
echo "============================================================"
echo ""
echo "⏳ Aguardando Render fazer deploy..."
echo "   (Normalmente demora 2-3 minutos)"
echo ""

# Aguardar 2 minutos para deploy
for i in {1..12}; do
    echo -ne "   ⏱️  ${i}0 segundos...\r"
    sleep 10
done

echo ""
echo ""
echo "🔍 Verificando se deploy está completo..."
echo ""

# Tentar fazer ping ao servidor
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/health" 2>/dev/null || echo "000")

if [ "$HTTP_CODE" == "000" ]; then
    echo "⚠️  Servidor ainda não responde, aguardando mais 1 minuto..."
    sleep 60
fi

echo ""
echo "✅ Servidor respondendo! Iniciando backup..."
echo ""
echo "============================================================"
echo ""

# Executar backup
python3 "$BACKUP_SCRIPT"

EXIT_CODE=$?

echo ""
echo "============================================================"

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ BACKUP COMPLETO COM SUCESSO!"
    echo ""
    echo "📁 Localização: backups/vehicle_photos_api/"
    echo ""
    echo "💡 IMPORTANTE:"
    echo "   - Guarda o ficheiro backup_complete.json em local seguro"
    echo "   - Este ficheiro contém TODAS as fotos dos veículos"
    echo "   - Podes restaurar a qualquer momento com restore_vehicle_photos.py"
else
    echo "❌ Backup falhou com código: $EXIT_CODE"
    echo ""
    echo "🔧 Soluções:"
    echo "   1. Aguardar mais tempo e tentar novamente"
    echo "   2. Fazer backup manual via Admin Settings > Export Configuration"
    echo "   3. Verificar logs do Render: https://dashboard.render.com"
fi

echo "============================================================"
