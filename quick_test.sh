#!/bin/bash
# Teste rápido automatizado

echo "🧪 Teste rápido da API..."

# Login e pegar cookie
COOKIE=$(curl -s -c - -b - -L -X POST "https://carrental-api-5f8q.onrender.com/login" \
  -d "username=admin&password=admin" | grep session | awk '{print $NF}')

if [ -z "$COOKIE" ]; then
    echo "❌ Login falhou!"
    exit 1
fi

echo "✅ Login OK"
echo ""
echo "⏱️  Testando API (timeout 120s)..."

START=$(date +%s)

RESPONSE=$(curl -s -b "session=$COOKIE" --max-time 120 \
  "https://carrental-api-5f8q.onrender.com/api/prices?location=Faro&start_date=2025-12-19&start_time=10:00&end_date=2026-01-02&end_time=10:00")

END=$(date +%s)
ELAPSED=$((END - START))

echo ""
echo "⏱️  Tempo: ${ELAPSED}s"
echo ""

# Verificar se tem erro de timeout=6
if echo "$RESPONSE" | grep -q "timeout=6"; then
    echo "❌ AINDA COM ERRO DE TIMEOUT=6"
    echo "   Deploy ainda não aplicado!"
    echo ""
    echo "Resposta:"
    echo "$RESPONSE" | head -5
    exit 1
fi

# Verificar se retornou resultados
ITEMS=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('items', [])))" 2>/dev/null)

if [ -n "$ITEMS" ] && [ "$ITEMS" -gt 0 ]; then
    echo "✅ SUCESSO! Retornou $ITEMS carros"
    echo ""
    echo "Top 3:"
    echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for i, car in enumerate(data.get('items', [])[:3], 1):
    print(f\"  {i}. €{car.get('price')} - {car.get('name')} ({car.get('supplier')})\")
" 2>/dev/null
else
    echo "⚠️  Nenhum carro retornado"
    echo ""
    echo "Resposta:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
fi
