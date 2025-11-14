#!/bin/bash

echo "=========================================="
echo "🚀 TESTE DE DETECÇÃO DE TRANSMISSÃO"
echo "=========================================="
echo ""
echo "⏳ Aguardando servidor iniciar (10s)..."
sleep 10

echo ""
echo "🌐 Disparando scraping..."
curl -X POST "http://localhost:8000/api/track-by-params" \
  -H "Content-Type: application/json" \
  -d '{"location":"Aeroporto de Faro","start_date":"2025-11-20","start_time":"15:00","days":7}' \
  --max-time 120 > /tmp/search_result.json 2>&1 &

CURL_PID=$!
echo "   Curl PID: $CURL_PID"

echo ""
echo "⏳ Aguardando scraping terminar (pode demorar 60s)..."
sleep 60

echo ""
echo "=========================================="
echo "📊 ANALISANDO LOGS"
echo "=========================================="

# Verificar se há logs de detecção
echo ""
echo "🔍 Logs de TRANS-DETECT-START:"
grep "TRANS-DETECT-START" /tmp/server_detailed.log | head -5

echo ""
echo "✅ Logs de ICON-TRANS (automáticos):"
grep "ICON-TRANS.*AUTOMATIC" /tmp/server_detailed.log | head -10

echo ""
echo "❌ Logs de ICON-TRANS (manuais):"
grep "ICON-TRANS.*MANUAL" /tmp/server_detailed.log | head -10

echo ""
echo "⚠️  Logs de VEHICLES-CONFLICT:"
grep "VEHICLES-CONFLICT" /tmp/server_detailed.log | head -10

echo ""
echo "📊 Estatísticas:"
grep -A 50 "ESTATÍSTICAS DE TRANSMISSÃO" /tmp/server_detailed.log | head -60

echo ""
echo "=========================================="
echo "✅ ANÁLISE COMPLETA"
echo "=========================================="
echo ""
echo "Logs completos em: /tmp/server_detailed.log"
echo "Resultado da busca: /tmp/search_result.json"
