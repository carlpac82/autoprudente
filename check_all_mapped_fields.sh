#!/bin/bash
# Verificar coordenadas em todos os locais

echo "🔍 VERIFICAÇÃO COMPLETA DE CAMPOS MAPEADOS"
echo "=========================================="
echo ""

echo "📍 LOCAL (SQLite):"
echo "Total de campos:"
sqlite3 data.db "SELECT COUNT(*) FROM damage_report_coordinates"
echo ""
echo "Campos mapeados:"
sqlite3 data.db "SELECT field_id FROM damage_report_coordinates ORDER BY field_id"
echo ""

echo "📅 Última modificação:"
sqlite3 data.db "SELECT field_id, mapped_at FROM damage_report_mapping_history ORDER BY mapped_at DESC LIMIT 1"
echo ""

echo "📊 Campos por tipo:"
echo "- Danos (damage_description_line_*):"
sqlite3 data.db "SELECT COUNT(*) FROM damage_report_coordinates WHERE field_id LIKE 'damage_description_line_%'"
echo "- Reparação (repair_line_*):"
sqlite3 data.db "SELECT COUNT(*) FROM damage_report_coordinates WHERE field_id LIKE 'repair_line%'"
echo "- Fotos (damage_photo_*):"
sqlite3 data.db "SELECT COUNT(*) FROM damage_report_coordinates WHERE field_id LIKE 'damage_photo_%'"
echo "- Diagrama (vehicle_diagram):"
sqlite3 data.db "SELECT COUNT(*) FROM damage_report_coordinates WHERE field_id = 'vehicle_diagram'"
echo ""

echo "📄 JSON Backup:"
if [ -f "damage_report_coordinates.json" ]; then
    echo "Existe: sim"
    echo "Total de campos no JSON:"
    jq 'keys | length' damage_report_coordinates.json 2>/dev/null || echo "Erro ao ler JSON"
else
    echo "Não existe"
fi
echo ""

echo "⚠️  NOTA:"
echo "Se mapeaste em PRODUÇÃO (Render), os dados estão no PostgreSQL,"
echo "não nesta base de dados local."
echo ""
echo "Para verificar em produção:"
echo "1. Abrir: https://carrental-api-5f8q.onrender.com/admin/damage-report"
echo "2. Clicar 'Mapper de Campos'"
echo "3. Ver se os campos aparecem mapeados"
