#!/usr/bin/env python
"""
Script de Migração para Produção - Sistema WEB OS
Atualiza ambiente existente para a nova versão com dependências organizadas
"""
import subprocess
import sys
import os
import shutil
from datetime import datetime

def log_message(message, level="INFO"):
    """Log com timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def run_command(command, description="", critical=True):
    """Executa comando com log detalhado"""
    log_message(f"Executando: {description}", "INFO")
    log_message(f"Comando: {command}", "DEBUG")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        log_message(f"✅ Sucesso: {description}", "SUCCESS")
        if result.stdout.strip():
            log_message(f"Saída: {result.stdout[:200]}...", "DEBUG")
        return True
    except subprocess.CalledProcessError as e:
        log_message(f"❌ Erro: {description}", "ERROR")
        log_message(f"Código de saída: {e.returncode}", "ERROR")
        if e.stderr:
            log_message(f"Erro: {e.stderr[:200]}...", "ERROR")
        
        if critical:
            log_message("Migração CANCELADA devido a erro crítico!", "CRITICAL")
            sys.exit(1)
        return False

def backup_database():
    """Faz backup do banco de dados"""
    log_message("=== BACKUP DO BANCO DE DADOS ===", "INFO")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Backup SQLite
    if os.path.exists('db_sistema.sqlite3'):
        backup_file = f"backup_db_{timestamp}.sqlite3"
        try:
            shutil.copy2('db_sistema.sqlite3', backup_file)
            log_message(f"✅ Backup SQLite criado: {backup_file}", "SUCCESS")
        except Exception as e:
            log_message(f"❌ Erro no backup SQLite: {e}", "ERROR")
    
    # Backup de arquivos importantes
    important_files = ['requirements.txt', 'sistema_geral/settings.py', '.env']
    for file_path in important_files:
        if os.path.exists(file_path):
            backup_path = f"backup_{timestamp}_{os.path.basename(file_path)}"
            try:
                shutil.copy2(file_path, backup_path)
                log_message(f"✅ Backup de {file_path} criado", "SUCCESS")
            except Exception as e:
                log_message(f"⚠️ Erro no backup de {file_path}: {e}", "WARNING")

def check_environment():
    """Verifica ambiente atual"""
    log_message("=== VERIFICAÇÃO DO AMBIENTE ===", "INFO")
    
    # Verificar Python
    python_version = sys.version_info
    log_message(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro}", "INFO")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        log_message("❌ Python 3.8+ é necessário!", "CRITICAL")
        sys.exit(1)
    
    # Verificar pip
    run_command("pip --version", "Verificando pip")
    
    # Verificar virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        log_message("✅ Virtual environment detectado", "SUCCESS")
    else:
        log_message("⚠️ Não está em um virtual environment", "WARNING")
        response = input("Continuar mesmo assim? (s/n): ").lower().strip()
        if response not in ['s', 'sim', 'y', 'yes']:
            log_message("Migração cancelada pelo usuário", "INFO")
            sys.exit(0)

def update_dependencies():
    """Atualiza dependências"""
    log_message("=== ATUALIZAÇÃO DE DEPENDÊNCIAS ===", "INFO")
    
    # Salvar lista atual de pacotes
    run_command("pip freeze > requirements_old.txt", "Salvando dependências atuais", critical=False)
    
    # Atualizar pip
    run_command("python -m pip install --upgrade pip", "Atualizando pip")
    
    # Verificar se novo requirements.txt existe
    if not os.path.exists('requirements.txt'):
        log_message("❌ Arquivo requirements.txt não encontrado!", "CRITICAL")
        log_message("Certifique-se de ter feito o pull do repositório Git", "INFO")
        sys.exit(1)
    
    # Instalar novas dependências
    run_command("pip install -r requirements.txt --upgrade", "Instalando/atualizando dependências")
    
    # Verificar se há conflitos
    run_command("pip check", "Verificando conflitos de dependências", critical=False)

def migrate_database():
    """Executa migrações do banco"""
    log_message("=== MIGRAÇÃO DO BANCO DE DADOS ===", "INFO")
    
    # Verificar migrações pendentes
    result = subprocess.run("python manage.py showmigrations --plan", shell=True, capture_output=True, text=True)
    if "[ ]" in result.stdout:
        log_message("Migrações pendentes detectadas", "INFO")
        
        # Criar migrações se necessário
        run_command("python manage.py makemigrations", "Criando novas migrações", critical=False)
        
        # Executar migrações
        run_command("python manage.py migrate", "Executando migrações")
    else:
        log_message("✅ Banco de dados atualizado", "SUCCESS")

def update_static_files():
    """Atualiza arquivos estáticos"""
    log_message("=== ARQUIVOS ESTÁTICOS ===", "INFO")
    
    # Coletar arquivos estáticos
    run_command("python manage.py collectstatic --noinput --clear", "Coletando arquivos estáticos")

def validate_system():
    """Valida o sistema após migração"""
    log_message("=== VALIDAÇÃO DO SISTEMA ===", "INFO")
    
    # Verificar Django
    run_command("python manage.py check", "Verificando configuração Django")
    
    # Validar dependências se script existe
    if os.path.exists('validate_dependencies.py'):
        run_command("python validate_dependencies.py", "Validando dependências", critical=False)
    
    # Teste básico de importações
    try:
        import django
        import celery
        import reportlab
        import openpyxl
        log_message("✅ Importações principais funcionando", "SUCCESS")
    except ImportError as e:
        log_message(f"⚠️ Problema com importações: {e}", "WARNING")

def restart_services():
    """Instruções para reiniciar serviços"""
    log_message("=== REINICIALIZAÇÃO DE SERVIÇOS ===", "INFO")
    
    print("\n" + "="*60)
    print("🔄 REINICIALIZAÇÃO NECESSÁRIA:")
    print("="*60)
    print("1. Reiniciar servidor web (Apache/Nginx)")
    print("2. Reiniciar Celery workers:")
    print("   • celery -A sistema_geral worker --loglevel=info")
    print("3. Reiniciar Celery beat (se usado):")
    print("   • celery -A sistema_geral beat --loglevel=info")
    print("4. Reiniciar Redis (se necessário)")

def main():
    """Função principal da migração"""
    print("🚀 MIGRAÇÃO PARA PRODUÇÃO - SISTEMA WEB OS")
    print("Este script atualizará o ambiente existente para a nova versão")
    print("="*70)
    
    # Confirmação
    print("\n⚠️  ATENÇÃO: Esta operação irá:")
    print("1. Fazer backup do banco de dados atual")
    print("2. Atualizar dependências Python")
    print("3. Executar migrações do banco")
    print("4. Atualizar arquivos estáticos")
    print("5. Validar o sistema")
    
    response = input("\nDeseja continuar? (s/n): ").lower().strip()
    if response not in ['s', 'sim', 'y', 'yes']:
        log_message("Migração cancelada pelo usuário", "INFO")
        sys.exit(0)
    
    try:
        # 1. Verificar ambiente
        check_environment()
        
        # 2. Backup
        backup_database()
        
        # 3. Atualizar dependências
        update_dependencies()
        
        # 4. Migrar banco
        migrate_database()
        
        # 5. Arquivos estáticos
        update_static_files()
        
        # 6. Validação
        validate_system()
        
        # 7. Instruções finais
        restart_services()
        
        print("\n" + "="*70)
        print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*70)
        
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. Reiniciar serviços conforme instruções acima")
        print("2. Testar funcionalidades críticas")
        print("3. Monitorar logs por possíveis erros")
        print("4. Verificar dashboard em: http://seu-servidor/governanca/quartos/dashboard/")
        
        print("\n📋 ARQUIVOS DE BACKUP CRIADOS:")
        backup_files = [f for f in os.listdir('.') if f.startswith('backup_')]
        for backup_file in backup_files:
            print(f"  • {backup_file}")
        
        log_message("Migração finalizada com sucesso!", "SUCCESS")
        
    except KeyboardInterrupt:
        log_message("Migração interrompida pelo usuário", "WARNING")
        sys.exit(1)
    except Exception as e:
        log_message(f"Erro inesperado: {e}", "CRITICAL")
        sys.exit(1)

if __name__ == "__main__":
    main()
