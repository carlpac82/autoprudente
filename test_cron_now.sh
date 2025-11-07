#!/bin/bash

# Script para testar endpoints cron AGORA
# Usage: ./test_cron_now.sh [search|report|both]

SECRET_KEY="6875bd76f0ec3cc9826c4bb9c3b450ef"
BASE_URL="https://carrental-api-5f8q.onrender.com"

echo "=========================================="
echo "🧪 TESTE IMEDIATO DE CRON JOBS"
echo "=========================================="
echo ""

test_search() {
    echo "📍 Testando Daily Search..."
    response=$(curl -s -w "\n%{http_code}" -X POST \
        "${BASE_URL}/api/cron/daily-search" \
        -H "X-Cron-Secret: ${SECRET_KEY}" \
        -H "Content-Type: application/json")
    
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" = "200" ]; then
        echo "✅ Daily Search iniciado com sucesso!"
        echo "   Response: $body"
    else
        echo "❌ Erro ao iniciar Daily Search (HTTP $http_code)"
        echo "   Response: $body"
    fi
    echo ""
}

test_report() {
    echo "📍 Testando Daily Report Email..."
    response=$(curl -s -w "\n%{http_code}" -X POST \
        "${BASE_URL}/api/cron/daily-report" \
        -H "X-Cron-Secret: ${SECRET_KEY}" \
        -H "Content-Type: application/json")
    
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" = "200" ]; then
        echo "✅ Daily Report iniciado com sucesso!"
        echo "   Response: $body"
    else
        echo "❌ Erro ao iniciar Daily Report (HTTP $http_code)"
        echo "   Response: $body"
    fi
    echo ""
}

case "$1" in
    search)
        test_search
        ;;
    report)
        test_report
        ;;
    both|"")
        test_search
        sleep 2
        test_report
        ;;
    *)
        echo "Usage: $0 [search|report|both]"
        exit 1
        ;;
esac

echo "=========================================="
echo "Verifique os logs do Render para confirmar execução:"
echo "https://dashboard.render.com/web/rental-price-tracker/logs"
echo ""
echo "URL da aplicação: https://carrental-api-5f8q.onrender.com"
echo "=========================================="
