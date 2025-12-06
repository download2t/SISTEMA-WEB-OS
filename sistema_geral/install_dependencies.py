#!/usr/bin/env python
"""
Script para atualizar e instalar dependências do Sistema WEB OS
"""
import subprocess
import sys
import os

def run_command(command, description=""):
    """Executa um comando e exibe o resultado"""
    print(f"\n{'='*60}")
    if description:
        print(f"🔄 {description}")
    print(f"Executando: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Sucesso: {description if description else command}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro: {description if description else command}")
        print(f"Código de saída: {e.returncode}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def main():
    """Função principal"""
    print("🚀 SISTEMA WEB OS - ATUALIZAÇÃO DE DEPENDÊNCIAS")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('requirements.txt'):
        print("❌ Erro: Arquivo requirements.txt não encontrado!")
        print("Execute este script na pasta raiz do projeto.")
        sys.exit(1)
    
    # Atualizar pip
    run_command("python -m pip install --upgrade pip", "Atualizando pip")
    
    # Instalar dependências principais
    run_command("pip install -r requirements.txt", "Instalando dependências principais")
    
    # Perguntar se deseja instalar dependências de desenvolvimento
    response = input("\n🔧 Deseja instalar dependências de desenvolvimento? (s/n): ").lower().strip()
    if response in ['s', 'sim', 'y', 'yes']:
        if os.path.exists('requirements-dev.txt'):
            run_command("pip install -r requirements-dev.txt", "Instalando dependências de desenvolvimento")
        else:
            print("⚠️ Arquivo requirements-dev.txt não encontrado")
    
    # Coletar arquivos estáticos
    response = input("\n📦 Deseja coletar arquivos estáticos do Django? (s/n): ").lower().strip()
    if response in ['s', 'sim', 'y', 'yes']:
        run_command("python manage.py collectstatic --noinput", "Coletando arquivos estáticos")
    
    # Migrar banco de dados
    response = input("\n🗄️ Deseja executar migrações do banco de dados? (s/n): ").lower().strip()
    if response in ['s', 'sim', 'y', 'yes']:
        run_command("python manage.py makemigrations", "Criando migrações")
        run_command("python manage.py migrate", "Executando migrações")
    
    print("\n" + "="*60)
    print("✅ Processo de atualização concluído!")
    print("="*60)
    
    # Mostrar versões instaladas
    print("\n📋 VERSÕES PRINCIPAIS INSTALADAS:")
    packages = ['Django', 'celery', 'reportlab', 'openpyxl', 'pillow']
    for package in packages:
        try:
            result = subprocess.run(f"pip show {package}", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('Version:'):
                        version = line.split(':')[1].strip()
                        print(f"  {package}: {version}")
                        break
        except:
            print(f"  {package}: Não instalado")
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. Configurar banco de dados em settings.py")
    print("2. Configurar Redis para Celery (se necessário)")
    print("3. Executar: python manage.py runserver")
    print("4. Acessar: http://127.0.0.1:8000/")

if __name__ == "__main__":
    main()
