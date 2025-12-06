#!/usr/bin/env python
"""
Script para validar se todas as dependências estão funcionando corretamente
"""
import sys
import os

def test_import(module_name, friendly_name=None):
    """Testa a importação de um módulo"""
    friendly_name = friendly_name or module_name
    try:
        __import__(module_name)
        print(f"✅ {friendly_name}")
        return True
    except ImportError as e:
        print(f"❌ {friendly_name} - Erro: {e}")
        return False

def main():
    """Função principal para validar dependências"""
    print("🔍 VALIDAÇÃO DE DEPENDÊNCIAS - SISTEMA WEB OS")
    print("="*60)
    
    success_count = 0
    total_count = 0
    
    # Lista de dependências críticas
    dependencies = [
        ('django', 'Django Framework'),
        ('celery', 'Celery (tarefas assíncronas)'),
        ('reportlab', 'ReportLab (geração de PDF)'),
        ('openpyxl', 'OpenPyXL (exportação Excel)'),
        ('PIL', 'Pillow (processamento de imagens)'),
        ('requests', 'Requests (requisições HTTP)'),
        ('redis', 'Redis (cache e broker)'),
        ('pyodbc', 'PyODBC (SQL Server)'),
        ('sqlite3', 'SQLite3 (banco de dados padrão)'),
        ('json', 'JSON (manipulação de dados)'),
        ('datetime', 'DateTime (manipulação de datas)'),
        ('os', 'OS (sistema operacional)'),
        ('io', 'IO (entrada e saída)'),
        ('locale', 'Locale (localização)'),
    ]
    
    print("📦 TESTANDO IMPORTAÇÕES:")
    print("-" * 40)
    
    for module, description in dependencies:
        total_count += 1
        if test_import(module, description):
            success_count += 1
    
    print("-" * 40)
    print(f"📊 RESULTADO: {success_count}/{total_count} dependências funcionando")
    
    if success_count == total_count:
        print("🎉 Todas as dependências estão funcionando corretamente!")
        result = True
    else:
        print("⚠️ Algumas dependências apresentaram problemas!")
        result = False
    
    # Testar funcionalidades específicas do Django
    print("\n" + "="*60)
    print("🔧 TESTANDO FUNCIONALIDADES DO DJANGO:")
    print("-" * 40)
    
    try:
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_geral.settings')
        import django
        django.setup()
        print("✅ Django configurado corretamente")
        
        # Testar models
        try:
            from governanca.models import Funcionarios, ControleQuartos
            print("✅ Models do sistema carregados")
        except Exception as e:
            print(f"❌ Erro ao carregar models: {e}")
            result = False
        
        # Testar geração de PDF
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from io import BytesIO
            
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            p.drawString(100, 750, "Teste de PDF")
            p.save()
            buffer.seek(0)
            print("✅ Geração de PDF funcionando")
        except Exception as e:
            print(f"❌ Erro na geração de PDF: {e}")
            result = False
        
        # Testar Excel
        try:
            from openpyxl import Workbook
            wb = Workbook()
            ws = wb.active
            ws['A1'] = "Teste Excel"
            print("✅ Geração de Excel funcionando")
        except Exception as e:
            print(f"❌ Erro na geração de Excel: {e}")
            result = False
            
    except Exception as e:
        print(f"❌ Erro ao configurar Django: {e}")
        result = False
    
    print("-" * 40)
    
    # Verificar versões importantes
    print("\n" + "="*60)
    print("📋 VERSÕES DAS DEPENDÊNCIAS PRINCIPAIS:")
    print("-" * 40)
    
    version_checks = [
        ('django', 'Django'),
        ('celery', 'Celery'),
        ('reportlab', 'ReportLab'),
        ('openpyxl', 'OpenPyXL'),
        ('PIL', 'Pillow'),
    ]
    
    for module, name in version_checks:
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', 'Versão não disponível')
            print(f"  {name}: {version}")
        except:
            print(f"  {name}: Não instalado ou erro")
    
    print("="*60)
    
    if result:
        print("✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
        print("🚀 O sistema está pronto para uso!")
    else:
        print("❌ ALGUNS PROBLEMAS FORAM ENCONTRADOS!")
        print("🔧 Execute: python install_dependencies.py para corrigir")
        
    return result

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
