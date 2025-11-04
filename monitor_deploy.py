#!/usr/bin/env python3
"""
Monitor de Deploy - Verifica status do GitHub Actions e Render
"""
import requests
import time
import sys
from datetime import datetime

# Cores para terminal
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header():
    print("\n" + "="*70)
    print(f"{BOLD}{BLUE}🚀 MONITOR DE DEPLOY - Rental Price Tracker{RESET}")
    print("="*70 + "\n")

def print_status(emoji, title, message, color=RESET):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {emoji} {color}{BOLD}{title}{RESET}: {message}")

def check_github_actions():
    """Verificar status do GitHub Actions"""
    try:
        # URL pública do repositório
        repo = "comercial-autoprudente/carrental_api"
        url = f"https://api.github.com/repos/{repo}/actions/runs"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('workflow_runs'):
                latest_run = data['workflow_runs'][0]
                status = latest_run.get('status')
                conclusion = latest_run.get('conclusion')
                name = latest_run.get('name', 'Unknown')
                commit = latest_run.get('head_commit', {}).get('message', 'N/A')[:50]
                
                if status == 'completed':
                    if conclusion == 'success':
                        print_status("✅", "GitHub Actions", f"{name} - SUCCESS", GREEN)
                        return 'success'
                    else:
                        print_status("❌", "GitHub Actions", f"{name} - FAILED", RED)
                        return 'failed'
                else:
                    print_status("🔄", "GitHub Actions", f"{name} - Running...", YELLOW)
                    return 'running'
            else:
                print_status("ℹ️", "GitHub Actions", "No recent runs", YELLOW)
                return 'none'
        else:
            print_status("⚠️", "GitHub Actions", f"API error: {response.status_code}", RED)
            return 'error'
    except Exception as e:
        print_status("⚠️", "GitHub Actions", f"Error: {str(e)}", RED)
        return 'error'

def check_render_status():
    """Verificar status do Render (via URL pública)"""
    try:
        # URL da aplicação (ajustar se necessário)
        app_url = "https://cartracker-6twv.onrender.com"
        
        response = requests.get(app_url, timeout=10)
        
        if response.status_code == 200:
            print_status("✅", "Render App", "Online and responding", GREEN)
            return 'online'
        else:
            print_status("⚠️", "Render App", f"Status code: {response.status_code}", YELLOW)
            return 'warning'
    except requests.exceptions.Timeout:
        print_status("⏳", "Render App", "Timeout (may be deploying)", YELLOW)
        return 'timeout'
    except requests.exceptions.ConnectionError:
        print_status("🔄", "Render App", "Connection error (deploying?)", YELLOW)
        return 'deploying'
    except Exception as e:
        print_status("⚠️", "Render App", f"Error: {str(e)}", RED)
        return 'error'

def check_git_status():
    """Verificar status local do Git"""
    import subprocess
    try:
        # Verificar branch atual
        branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
        
        # Verificar último commit
        last_commit = subprocess.check_output(['git', 'log', '-1', '--oneline'], text=True).strip()
        
        # Verificar se há mudanças não commitadas
        status = subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip()
        
        print_status("📝", "Git Local", f"Branch: {branch}", BLUE)
        print_status("📝", "Last Commit", last_commit, BLUE)
        
        if status:
            print_status("⚠️", "Git Status", "Uncommitted changes detected", YELLOW)
        else:
            print_status("✅", "Git Status", "Clean working directory", GREEN)
        
        return True
    except Exception as e:
        print_status("⚠️", "Git", f"Error: {str(e)}", RED)
        return False

def monitor_loop(duration_minutes=10, interval_seconds=30):
    """Loop de monitoramento"""
    print_header()
    print_status("🚀", "Monitoring", f"Starting {duration_minutes}min monitor (every {interval_seconds}s)", BLUE)
    print()
    
    # Status inicial
    check_git_status()
    print()
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    iteration = 0
    
    github_success = False
    render_online = False
    
    while time.time() < end_time:
        iteration += 1
        print(f"\n{BOLD}--- Check #{iteration} ---{RESET}")
        
        # Verificar GitHub Actions
        github_status = check_github_actions()
        if github_status == 'success':
            github_success = True
        
        # Verificar Render
        render_status = check_render_status()
        if render_status == 'online':
            render_online = True
        
        # Se ambos estão OK, podemos parar
        if github_success and render_online:
            print()
            print("="*70)
            print_status("🎉", "DEPLOY COMPLETE", "All systems operational!", GREEN)
            print("="*70)
            print()
            print(f"{GREEN}✅ GitHub Actions: SUCCESS{RESET}")
            print(f"{GREEN}✅ Render App: ONLINE{RESET}")
            print()
            print(f"{BOLD}🔗 App URL:{RESET} https://cartracker-6twv.onrender.com")
            print(f"{BOLD}📊 GitHub:{RESET} https://github.com/comercial-autoprudente/carrental_api/actions")
            print()
            return True
        
        # Aguardar próximo check
        if time.time() < end_time:
            remaining = int(end_time - time.time())
            print(f"\n⏳ Next check in {interval_seconds}s (monitoring for {remaining//60}m {remaining%60}s more)")
            time.sleep(interval_seconds)
    
    # Timeout
    print()
    print("="*70)
    print_status("⏰", "TIMEOUT", f"Monitoring ended after {duration_minutes} minutes", YELLOW)
    print("="*70)
    print()
    
    if not github_success:
        print(f"{YELLOW}⚠️  GitHub Actions: Still running or not completed{RESET}")
    else:
        print(f"{GREEN}✅ GitHub Actions: SUCCESS{RESET}")
    
    if not render_online:
        print(f"{YELLOW}⚠️  Render App: Not responding yet{RESET}")
    else:
        print(f"{GREEN}✅ Render App: ONLINE{RESET}")
    
    print()
    print("💡 Check manually:")
    print(f"   GitHub: https://github.com/comercial-autoprudente/carrental_api/actions")
    print(f"   Render: https://dashboard.render.com")
    print(f"   App: https://cartracker-6twv.onrender.com")
    print()
    
    return False

if __name__ == "__main__":
    try:
        # Monitorar por 10 minutos, checando a cada 30 segundos
        monitor_loop(duration_minutes=10, interval_seconds=30)
    except KeyboardInterrupt:
        print()
        print_status("🛑", "Stopped", "Monitoring interrupted by user", YELLOW)
        print()
        sys.exit(0)
