#!/usr/bin/env python
"""
Setup completo do Sistema WEB OS
Este script realiza a configuração inicial completa do sistema
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description="", ignore_errors=False):
    """Executa um comando e exibe o resultado"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"Comando: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Sucesso: {description}")
        if result.stdout.strip():
            print("📄 Saída:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro: {description}")
        print(f"Código de saída: {e.returncode}")
        if e.stderr:
            print(f"⚠️ Erro: {e.stderr}")
        if e.stdout:
            print(f"📄 Saída: {e.stdout}")
        
        if not ignore_errors:
            return False
        else:
            print("⏭️ Continuando apesar do erro...")
            return True

def check_file_exists(file_path, description):
    """Verifica se um arquivo existe"""
    if os.path.exists(file_path):
        print(f"✅ {description}: Encontrado")
        return True
    else:
        print(f"❌ {description}: Não encontrado")
        return False

def create_env_file():
    """Cria arquivo .env se não existir"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("📝 Criando arquivo .env...")
        env_content = """# ================================
# SISTEMA WEB OS - CONFIGURAÇÕES
# ================================

# Django
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production-12345

# Banco de dados (SQLite para desenvolvimento)
DATABASE_URL=sqlite:///db_sistema.sqlite3

# Redis (para Celery)
REDIS_URL=redis://localhost:6379/0

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Configurações de produção
ALLOWED_HOSTS=127.0.0.1,localhost

# Media e Static
MEDIA_ROOT=media/
STATIC_ROOT=staticfiles/
"""
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print(f"✅ Arquivo {env_file} criado com sucesso!")
        return True
    else:
        print(f"ℹ️ Arquivo {env_file} já existe")
        return True

def main():
    """Função principal do setup"""
    print("🚀 SETUP COMPLETO DO SISTEMA WEB OS")
    print("Este script irá configurar todo o ambiente de desenvolvimento")
    print("="*70)
    
    # Verificar se estamos no diretório correto
    required_files = [
        ("manage.py", "Script de gerenciamento do Django"),
        ("requirements.txt", "Lista de dependências"),
        ("sistema_geral/settings.py", "Configurações do Django"),
    ]
    
    print("📁 VERIFICANDO ARQUIVOS DO PROJETO:")
    all_files_exist = True
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_files_exist = False
    
    if not all_files_exist:
        print("❌ Este script deve ser executado na pasta raiz do projeto!")
        sys.exit(1)
    
    print("\n🎯 INICIANDO SETUP COMPLETO...")
    
    # 1. Criar arquivo .env
    print("\n" + "="*50)
    print("1. CONFIGURAÇÃO DE AMBIENTE")
    print("="*50)
    create_env_file()
    
    # 2. Atualizar pip e instalar dependências
    print("\n" + "="*50)
    print("2. INSTALAÇÃO DE DEPENDÊNCIAS")
    print("="*50)
    
    if not run_command("python -m pip install --upgrade pip", "Atualizando pip"):
        print("⚠️ Continuando mesmo com erro no pip...")
    
    if not run_command("pip install -r requirements.txt", "Instalando dependências principais"):
        print("❌ Erro crítico na instalação das dependências!")
        sys.exit(1)
    
    # 3. Configuração do Django
    print("\n" + "="*50)
    print("3. CONFIGURAÇÃO DO DJANGO")
    print("="*50)
    
    # Criar migrações
    run_command("python manage.py makemigrations", "Criando migrações", ignore_errors=True)
    
    # Executar migrações
    run_command("python manage.py migrate", "Executando migrações do banco", ignore_errors=True)
    
    # Coletar arquivos estáticos
    run_command("python manage.py collectstatic --noinput", "Coletando arquivos estáticos", ignore_errors=True)
    
    # 4. Criar superusuário (opcional)
    print("\n" + "="*50)
    print("4. USUÁRIO ADMINISTRADOR")
    print("="*50)
    
    response = input("🔑 Deseja criar um superusuário agora? (s/n): ").lower().strip()
    if response in ['s', 'sim', 'y', 'yes']:
        print("📝 Execute manualmente: python manage.py createsuperuser")
        print("   Usuário sugerido: admin")
        print("   Email: admin@sistema.local")
    
    # 5. Validação final
    print("\n" + "="*50)
    print("5. VALIDAÇÃO DO SISTEMA")
    print("="*50)
    
    run_command("python validate_dependencies.py", "Validando dependências")
    run_command("python manage.py check", "Verificando configuração do Django", ignore_errors=True)
    
    # 6. Informações finais
    print("\n" + "="*70)
    print("✅ SETUP CONCLUÍDO COM SUCESSO!")
    print("="*70)
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. Criar superusuário: python manage.py createsuperuser")
    print("2. Iniciar servidor: python manage.py runserver")
    print("3. Acessar sistema: http://127.0.0.1:8000/")
    print("4. Acessar admin: http://127.0.0.1:8000/admin/")
    
    print("\n🔧 COMANDOS ÚTEIS:")
    print("• Servidor de desenvolvimento: python manage.py runserver")
    print("• Shell Django: python manage.py shell")
    print("• Migrações: python manage.py makemigrations && python manage.py migrate")
    print("• Testes: python manage.py test")
    print("• Celery worker: celery -A sistema_geral worker -l info")
    
    print("\n📚 DOCUMENTAÇÃO:")
    print("• README.md: Documentação principal")
    print("• DEPENDENCIES.md: Informações sobre dependências")
    print("• validate_dependencies.py: Validar ambiente")
    
    print("\n🆘 PROBLEMAS?")
    print("• Execute: python validate_dependencies.py")
    print("• Verifique: python manage.py check")
    print("• Logs: Verifique console do Django")
    
    print("\n" + "="*70)
    print("🎉 SISTEMA WEB OS PRONTO PARA USO!")
    print("="*70)

if __name__ == "__main__":
    main()
