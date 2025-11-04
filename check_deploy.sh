#!/bin/bash

echo ""
echo "======================================================================"
echo "🚀 DEPLOY STATUS CHECK"
echo "======================================================================"
echo ""

# GitHub Actions Status
echo "📊 GitHub Actions:"
curl -s https://api.github.com/repos/comercial-autoprudente/carrental_api/actions/runs | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('workflow_runs'):
    run = data['workflow_runs'][0]
    status = run.get('status')
    conclusion = run.get('conclusion')
    name = run.get('name', 'Unknown')
    if status == 'completed':
        if conclusion == 'success':
            print(f'   ✅ {name} - SUCCESS')
        else:
            print(f'   ❌ {name} - {conclusion}')
    else:
        print(f'   🔄 {name} - Running...')
else:
    print('   ℹ️  No recent runs')
"

echo ""

# Render App Status
echo "🌐 Render App:"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://cartracker-6twv.onrender.com --max-time 10)

if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✅ Online (HTTP $HTTP_CODE)"
elif [ "$HTTP_CODE" = "000" ]; then
    echo "   🔄 Deploying or timeout"
else
    echo "   ⚠️  Status: HTTP $HTTP_CODE"
fi

echo ""

# Git Status
echo "📝 Git Local:"
BRANCH=$(git branch --show-current 2>/dev/null)
LAST_COMMIT=$(git log -1 --oneline 2>/dev/null)
echo "   Branch: $BRANCH"
echo "   Commit: $LAST_COMMIT"

echo ""
echo "======================================================================"
echo "🔗 Quick Links:"
echo "   GitHub Actions: https://github.com/comercial-autoprudente/carrental_api/actions"
echo "   Render Dashboard: https://dashboard.render.com"
echo "   Live App: https://cartracker-6twv.onrender.com"
echo "======================================================================"
echo ""
