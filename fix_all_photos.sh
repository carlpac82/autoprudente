#!/bin/bash
# Script completo para corrigir todas as fotos dos carros

echo "🖼️  CORREÇÃO COMPLETA DE FOTOS DOS CARROS"
echo "=========================================="
echo ""

# Passo 1: Diagnóstico inicial
echo "📊 Passo 1: Diagnóstico inicial..."
python3 diagnose_photos.py | tail -20
echo ""

# Passo 2: Corrigir fotos existentes
echo "🔧 Passo 2: Corrigindo fotos com mapeamento atual..."
python3 fix_photo_urls.py | tail -10
echo ""

# Passo 3: Mostrar estatísticas finais
echo "📈 Passo 3: Estatísticas finais..."
sqlite3 car_images.db "SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN photo_url LIKE '%loading-car%' THEN 1 ELSE 0 END) as placeholders,
    SUM(CASE WHEN photo_url NOT LIKE '%loading-car%' THEN 1 ELSE 0 END) as valid
FROM car_images"
echo ""

# Passo 4: Mostrar próximos passos
echo "✅ Correção completa!"
echo ""
echo "📋 PRÓXIMOS PASSOS OPCIONAIS:"
echo "1. Para adicionar mais 154 mapeamentos:"
echo "   python3 generate_missing_mappings.py"
echo ""
echo "2. Para forçar download das imagens (servidor deve estar rodando):"
echo "   curl -X POST http://localhost:8000/api/vehicles/images/download"
echo ""
echo "3. Para ver detalhes completos:"
echo "   python3 diagnose_photos.py"
echo ""
echo "📖 Documentação:"
echo "   - RESUMO_FOTOS.md (resumo executivo)"
echo "   - FOTOS_CARROS_SOLUCAO.md (documentação técnica)"
echo "   - ADICIONAR_MAPEAMENTOS.txt (instruções detalhadas)"
echo ""
