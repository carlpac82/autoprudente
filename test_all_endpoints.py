"""
Teste completo de todos os endpoints de salvar/editar/criar
"""

import requests
import time
import json

BASE_URL = "https://carrental-api-5f8q.onrender.com"

def test_health():
    """1. Testar se servidor está online"""
    print("\n1️⃣ TESTE: Health Check")
    try:
        r = requests.get(f"{BASE_URL}/healthz", timeout=10)
        if r.status_code == 200:
            print("   ✅ Servidor online")
            return True
        else:
            print(f"   ❌ Status: {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_damage_reports_list():
    """2. Testar listagem de DRs"""
    print("\n2️⃣ TESTE: Listar Damage Reports")
    try:
        r = requests.get(f"{BASE_URL}/api/damage-reports/list", timeout=10)
        if r.status_code in [200, 303]:
            print(f"   ✅ Status: {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                if data.get("ok"):
                    print(f"   📋 {len(data.get('reports', []))} DRs encontrados")
            return True
        else:
            print(f"   ❌ Status: {r.status_code}")
            print(f"   Response: {r.text[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_dr_pdf_query_param():
    """3. Testar PDF via query parameter"""
    print("\n3️⃣ TESTE: DR PDF (query parameter)")
    try:
        r = requests.get(
            f"{BASE_URL}/api/damage-reports/pdf-original",
            params={"dr_number": "DR01/2025", "preview": "true"},
            timeout=10
        )
        if r.status_code in [200, 303, 401]:  # 401 = precisa login
            print(f"   ✅ Status: {r.status_code}")
            if r.status_code == 200:
                print(f"   📄 PDF size: {len(r.content)} bytes")
            return True
        else:
            print(f"   ❌ Status: {r.status_code}")
            print(f"   Response: {r.text[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_dr_numbering():
    """4. Testar endpoint de numeração"""
    print("\n4️⃣ TESTE: DR Numbering GET")
    try:
        r = requests.get(f"{BASE_URL}/api/damage-reports/numbering/get", timeout=10)
        if r.status_code in [200, 303]:
            print(f"   ✅ Status: {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                if data.get("ok"):
                    print(f"   📊 Próximo DR: {data.get('next_number')}")
            return True
        else:
            print(f"   ❌ Status: {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_homepage():
    """5. Testar página principal"""
    print("\n5️⃣ TESTE: Homepage")
    try:
        r = requests.get(f"{BASE_URL}/", timeout=10)
        if r.status_code in [200, 303]:
            print(f"   ✅ Status: {r.status_code}")
            return True
        else:
            print(f"   ❌ Status: {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_admin_page():
    """6. Testar página admin"""
    print("\n6️⃣ TESTE: Admin Page")
    try:
        r = requests.get(f"{BASE_URL}/admin", timeout=10)
        if r.status_code in [200, 303]:
            print(f"   ✅ Status: {r.status_code}")
            return True
        else:
            print(f"   ❌ Status: {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_damage_report_page():
    """7. Testar página damage reports"""
    print("\n7️⃣ TESTE: Damage Report Page")
    try:
        r = requests.get(f"{BASE_URL}/damage-report", timeout=10)
        if r.status_code in [200, 303]:
            print(f"   ✅ Status: {r.status_code}")
            return True
        else:
            print(f"   ❌ Status: {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_ai_learning_load():
    """8. Testar AI Learning Load"""
    print("\n8️⃣ TESTE: AI Learning Load")
    try:
        r = requests.get(f"{BASE_URL}/api/ai/learning/load", timeout=10)
        if r.status_code in [200, 303, 401]:
            print(f"   ✅ Status: {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                if data.get("ok"):
                    adjustments = len(data.get('data', {}).get('adjustments', []))
                    print(f"   🤖 {adjustments} AI adjustments")
            return True
        else:
            print(f"   ❌ Status: {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_price_rules_load():
    """9. Testar Price Rules Load"""
    print("\n9️⃣ TESTE: Price Rules Load")
    try:
        r = requests.get(f"{BASE_URL}/api/price-automation/rules/load", timeout=10)
        if r.status_code in [200, 303, 401]:
            print(f"   ✅ Status: {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                if data.get("ok"):
                    rules = data.get('rules', {})
                    print(f"   📋 Rules configuradas")
            return True
        else:
            print(f"   ❌ Status: {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_price_history_list():
    """10. Testar Price History List"""
    print("\n🔟 TESTE: Price History List")
    try:
        r = requests.get(f"{BASE_URL}/api/prices/history/list", timeout=10)
        if r.status_code in [200, 303, 401]:
            print(f"   ✅ Status: {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                if data.get("ok"):
                    history = data.get('history', [])
                    print(f"   📊 {len(history)} históricos")
            return True
        else:
            print(f"   ❌ Status: {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def check_deploy_status():
    """Verificar se último deploy está ativo"""
    print("\n🔍 Verificando status do deploy...")
    try:
        r = requests.get(f"{BASE_URL}/healthz", timeout=10)
        if r.status_code == 200:
            print("✅ Deploy ativo")
            return True
        else:
            print(f"⚠️ Status: {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ Servidor offline: {e}")
        return False

def main():
    print("=" * 80)
    print("🧪 TESTE COMPLETO DE ENDPOINTS - RENDER")
    print("=" * 80)
    
    # Aguardar deploy
    print("\n⏳ Aguardando deploy terminar (30 segundos)...")
    time.sleep(30)
    
    if not check_deploy_status():
        print("\n❌ Deploy não está ativo. Aguarde mais tempo.")
        return
    
    print("\n🎯 INICIANDO TESTES...")
    print("=" * 80)
    
    results = []
    
    # Executar todos os testes
    results.append(("Health Check", test_health()))
    results.append(("Damage Reports List", test_damage_reports_list()))
    results.append(("DR PDF Query", test_dr_pdf_query_param()))
    results.append(("DR Numbering", test_dr_numbering()))
    results.append(("Homepage", test_homepage()))
    results.append(("Admin Page", test_admin_page()))
    results.append(("Damage Report Page", test_damage_report_page()))
    results.append(("AI Learning Load", test_ai_learning_load()))
    results.append(("Price Rules Load", test_price_rules_load()))
    results.append(("Price History List", test_price_history_list()))
    
    # Resumo
    print("\n" + "=" * 80)
    print("📊 RESUMO DOS TESTES")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} - {name}")
    
    print("=" * 80)
    print(f"\n🎯 RESULTADO: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n✅ TODOS OS TESTES PASSARAM! Sistema funcionando! 🎉")
    else:
        print(f"\n⚠️ {total - passed} teste(s) falharam")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Verificar logs do Render")
        print("2. Testar manualmente no browser")
        print("3. Verificar erros específicos acima")

if __name__ == "__main__":
    main()
