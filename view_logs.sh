#!/bin/bash
# Ver logs do servidor em tempo real
# Uso: ./view_logs.sh

echo "📊 LOGS DO SERVIDOR EM TEMPO REAL"
echo "=================================="
echo ""

# Se server.log existe, mostrar
if [ -f "server.log" ]; then
    tail -f server.log | grep --line-buffered "\[SELENIUM_SIMPLE\]\|\[SELENIUM\]\|\[POST_DIRETO\]\|\[API\]"
else
    echo "❌ server.log não encontrado"
    echo "Inicie o servidor com: python3 main.py 2>&1 | tee server.log"
fi
