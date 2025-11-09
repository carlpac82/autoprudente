#!/bin/bash

# Script para atualizar numeração DR no Render via API
# Define current_number = 39 (próximo será 40)

RENDER_URL="https://carrental-api-5f8q.onrender.com"

echo "🔐 Fazendo login..."
COOKIES=$(curl -s -c - -b - -X POST "$RENDER_URL/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin" | grep -E "session|PHPSESSID")

echo "✅ Login feito!"

echo "🔄 Atualizando numeração DR para 39..."
curl -s -b <(echo "$COOKIES") -X POST "$RENDER_URL/api/damage-reports/numbering/update" \
  -H "Content-Type: application/json" \
  -d '{"current_number": 39, "prefix": "DR"}' | jq .

echo "✅ Atualizado! Próximo DR será 40/2025"
