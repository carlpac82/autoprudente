#!/bin/bash
# Teste simples de performance da API

echo "🧪 Testando performance da API CarJet..."
echo "============================================================"
echo ""

URL="https://carrental-api-5f8q.onrender.com/api/prices"
PARAMS="location=Faro&start_date=2025-12-19&start_time=10:00&end_date=2026-01-02&end_time=10:00"

echo "📍 URL: $URL"
echo "📋 Params: $PARAMS"
echo ""
echo "⏱️  Iniciando teste (timeout: 120s)..."
echo "------------------------------------------------------------"
echo ""

# Medir tempo de resposta
START=$(date +%s)

# Fazer request (sem autenticação - só para medir tempo)
HTTP_CODE=$(curl -w "%{http_code}" -o /tmp/api_response.txt -s \
  --max-time 120 \
  "$URL?$PARAMS")

END=$(date +%s)
ELAPSED=$((END - START))

echo ""
echo "============================================================"
echo "✅ Resposta recebida!"
echo ""
echo "📊 Resultados:"
echo "   Status HTTP: $HTTP_CODE"
echo "   Tempo: ${ELAPSED}s"
echo "   Tamanho: $(wc -c < /tmp/api_response.txt) bytes"
echo ""

# Análise de performance
if [ $ELAPSED -lt 30 ]; then
    echo "✅ EXCELENTE! Resposta em menos de 30s"
elif [ $ELAPSED -lt 60 ]; then
    echo "⚠️  ACEITÁVEL. Resposta em ${ELAPSED}s (meta: <30s)"
else
    echo "❌ LENTO! Resposta em ${ELAPSED}s (meta: <30s)"
fi

echo ""
echo "💡 Nota: Se HTTP=200 → Login necessário mas API está respondendo"
echo "        Se HTTP=303 → Redirect (esperado sem autenticação)"
echo ""

# Preview da resposta
echo "📄 Preview da resposta:"
head -c 500 /tmp/api_response.txt
echo ""
echo "..."
