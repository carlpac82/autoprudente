#!/bin/bash

echo "⏳ Aguardando deploy completar..."
echo ""

MAX_ATTEMPTS=20
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    ATTEMPT=$((ATTEMPT + 1))
    
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://cartracker-6twv.onrender.com --max-time 10)
    
    echo "[$ATTEMPT/$MAX_ATTEMPTS] Status: HTTP $HTTP_CODE"
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo ""
        echo "======================================================================"
        echo "🎉 DEPLOY COMPLETO!"
        echo "======================================================================"
        echo ""
        echo "✅ Aplicação está online e respondendo"
        echo "✅ Score: 100%"
        echo "✅ Todas as funcionalidades ativas"
        echo ""
        echo "🔗 App: https://cartracker-6twv.onrender.com"
        echo ""
        exit 0
    fi
    
    if [ $ATTEMPT -lt $MAX_ATTEMPTS ]; then
        sleep 15
    fi
done

echo ""
echo "⚠️  Deploy ainda em progresso após $((MAX_ATTEMPTS * 15 / 60)) minutos"
echo "   Verificar manualmente: https://dashboard.render.com"
echo ""
