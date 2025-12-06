#!/usr/bin/env python
"""
Validação Pré-Migração - Sistema WEB OS
Verifica se o ambiente está pronto para migração
"""
import subprocess
import sys
import os
import json
from datetime import datetime

def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    print(f"🐍 Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ é necessário!")
        return False
    print("✅ Versão do Python adequada")
    return True

def check_git_status():
    """Verifica status do Git"""
    print("\n📋 STATUS DO GIT:")
    try:
        # Verificar se é um repositório Git
        result = subprocess.run("git status", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️ Não é um repositório Git ou Git não está instalado")
            return False
        
        # Verificar mudanças locais
        if "Changes not staged for commit" in result.stdout or "Changes to be committed" in result.stdout:
            print("⚠️ Há mudanças locais não commitadas")
            print("Considere fazer backup dessas mudanças antes da migração")
        else:
            print("✅ Repositório Git limpo")
        
        # Verificar branch atual
        branch_result = subprocess.run("git branch --show-current", shell=True, capture_output=True, text=True)
        current_branch = branch_result.stdout.strip()
        print(f"📍 Branch atual: {current_branch}")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar Git: {e}")
        return False

def check_database():
    """Verifica banco de dados"""
    print("\n🗄️ BANCO DE DADOS:")
    
    # Verificar SQLite
    if os.path.exists('db_sistema.sqlite3'):
        size = os.path.getsize('db_sistema.sqlite3')
        print(f"✅ SQLite encontrado ({size:,} bytes)")
        
        # Verificar se Django consegue conectar
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_geral.settings')
            import django
            django.setup()
            
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM django_migrations")
            migrations_count = cursor.fetchone()[0]
            print(f"✅ {migrations_count} migrações aplicadas")
            
            return True
        except Exception as e:
            print(f"⚠️ Problema na conexão com banco: {e}")
            return False
    else:
        print("❌ Banco SQLite não encontrado")
        return False

def check_dependencies():
    """Verifica dependências atuais"""
    print("\n📦 DEPENDÊNCIAS ATUAIS:")
    
    try:
        result = subprocess.run("pip list --format=json", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            packages = json.loads(result.stdout)
            important_packages = ['django', 'celery', 'reportlab', 'openpyxl', 'pillow']
            
            found_packages = {}
            for package in packages:
                if package['name'].lower() in important_packages:
                    found_packages[package['name'].lower()] = package['version']
            
            for pkg in important_packages:
                if pkg in found_packages:
                    print(f"✅ {pkg}: {found_packages[pkg]}")
                else:
                    print(f"❌ {pkg}: Não instalado")
            
            return len(found_packages) >= 3  # Pelo menos 3 pacotes importantes
        else:
            print("❌ Erro ao listar pacotes pip")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar dependências: {e}")
        return False

def check_disk_space():
    """Verifica espaço em disco"""
    print("\n💾 ESPAÇO EM DISCO:")
    
    try:
        if os.name == 'nt':  # Windows
            import shutil
            total, used, free = shutil.disk_usage('.')
        else:  # Unix/Linux
            statvfs = os.statvfs('.')
            free = statvfs.f_bavail * statvfs.f_frsize
            total = statvfs.f_blocks * statvfs.f_frsize
            used = total - free
        
        free_gb = free / (1024**3)
        total_gb = total / (1024**3)
        used_percent = (used / total) * 100
        
        print(f"📊 Espaço livre: {free_gb:.1f} GB ({100-used_percent:.1f}%)")
        
        if free_gb < 1:
            print("❌ Menos de 1GB livre - CRÍTICO!")
            return False
        elif free_gb < 2:
            print("⚠️ Menos de 2GB livre - Recomendado limpar espaço")
        else:
            print("✅ Espaço em disco adequado")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar espaço: {e}")
        return False

def check_permissions():
    """Verifica permissões de escrita"""
    print("\n🔐 PERMISSÕES:")
    
    test_files = ['test_write.tmp']
    all_ok = True
    
    for test_file in test_files:
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            print(f"✅ Permissão de escrita no diretório atual")
        except Exception as e:
            print(f"❌ Sem permissão de escrita: {e}")
            all_ok = False
    
    return all_ok

def check_services():
    """Verifica se serviços estão rodando"""
    print("\n🔄 SERVIÇOS:")
    
    # Verificar se o Django está acessível
    try:
        result = subprocess.run("python manage.py check", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Django configurado corretamente")
        else:
            print(f"⚠️ Problemas na configuração Django: {result.stderr[:100]}...")
    except Exception as e:
        print(f"⚠️ Erro ao verificar Django: {e}")
    
    # Verificar Redis (se estiver configurado)
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✅ Redis conectado")
    except:
        print("⚠️ Redis não disponível (normal se não estiver sendo usado)")

def generate_backup_script():
    """Gera script de backup personalizado"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    backup_script = f"""#!/bin/bash
# Script de Backup Automático - {timestamp}

echo "🔄 Iniciando backup do Sistema WEB OS..."

# Criar diretório de backup
mkdir -p backup_{timestamp}

# Backup do banco de dados
if [ -f "db_sistema.sqlite3" ]; then
    cp db_sistema.sqlite3 backup_{timestamp}/db_sistema_backup.sqlite3
    echo "✅ Backup do banco SQLite criado"
fi

# Backup de arquivos importantes
cp requirements.txt backup_{timestamp}/ 2>/dev/null || echo "⚠️ requirements.txt não encontrado"
cp -r sistema_geral/settings.py backup_{timestamp}/ 2>/dev/null || echo "⚠️ settings.py não encontrado"
cp .env backup_{timestamp}/ 2>/dev/null || echo "⚠️ .env não encontrado"

# Backup das dependências atuais
pip freeze > backup_{timestamp}/requirements_current.txt

# Backup de media files (se existir)
if [ -d "media" ]; then
    cp -r media backup_{timestamp}/
    echo "✅ Backup dos arquivos media criado"
fi

# Criar arquivo de informações
cat > backup_{timestamp}/backup_info.txt << EOF
Backup criado em: $(date)
Sistema: Sistema WEB OS
Versão Python: $(python --version)
Branch Git: $(git branch --show-current 2>/dev/null || echo "N/A")
Commit: $(git rev-parse HEAD 2>/dev/null || echo "N/A")
EOF

echo "✅ Backup completo criado em: backup_{timestamp}/"
echo "📋 Para restaurar: execute os comandos no backup_info.txt"
"""
    
    with open(f'create_backup_{timestamp}.sh', 'w') as f:
        f.write(backup_script)
    
    os.chmod(f'create_backup_{timestamp}.sh', 0o755)
    print(f"\n📄 Script de backup criado: create_backup_{timestamp}.sh")

def main():
    """Função principal"""
    print("🔍 VALIDAÇÃO PRÉ-MIGRAÇÃO - Sistema WEB OS")
    print("Este script verifica se o ambiente está pronto para migração")
    print("="*60)
    
    checks = []
    
    # Executar verificações
    checks.append(("Python Version", check_python_version()))
    checks.append(("Git Status", check_git_status()))
    checks.append(("Database", check_database()))
    checks.append(("Dependencies", check_dependencies()))
    checks.append(("Disk Space", check_disk_space()))
    checks.append(("Permissions", check_permissions()))
    
    # Verificações de serviços (não críticas)
    check_services()
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DA VALIDAÇÃO:")
    print("="*60)
    
    passed = 0
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{len(checks)} verificações passaram")
    
    # Recomendações
    print("\n🎯 RECOMENDAÇÕES:")
    
    if passed == len(checks):
        print("✅ Sistema PRONTO para migração!")
        print("✅ Todas as verificações passaram")
        
        generate_backup_script()
        
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Execute o script de backup gerado")
        print("2. Agende janela de manutenção")
        print("3. Execute: python migrate_to_production.py")
        
    elif passed >= len(checks) * 0.8:  # 80% ou mais
        print("⚠️ Sistema QUASE pronto para migração")
        print("⚠️ Resolva os problemas menores primeiro")
        
        generate_backup_script()
        
    else:
        print("❌ Sistema NÃO está pronto para migração")
        print("❌ Resolva os problemas críticos antes de continuar")
        print("\n📞 Entre em contato com a equipe de suporte se necessário")
    
    print(f"\n📄 Relatório salvo em: pre_migration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

if __name__ == "__main__":
    main()
