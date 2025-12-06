# 📦 Dependências do Sistema WEB OS

## 🎯 Visão Geral
Este documento descreve todas as dependências necessárias para o Sistema Web de Controle de OS e Quartos.

## 🚀 Instalação Rápida

### 1. Instalação Automática (Recomendado)
```bash
python install_dependencies.py
```

### 2. Instalação Manual
```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências principais
pip install -r requirements.txt

# Instalar dependências de desenvolvimento (opcional)
pip install -r requirements-dev.txt
```

### 3. Validação
```bash
python validate_dependencies.py
```

## 📋 Dependências Principais

### 🏗️ Framework Django
- **Django 5.0.9**: Framework web principal
- **asgiref**: Suporte ASGI
- **sqlparse**: Parser SQL para Django
- **tzdata**: Dados de fuso horário

### 🗄️ Banco de Dados
- **SQLite**: Banco padrão (integrado ao Python)
- **django-mssql-backend**: Suporte ao Microsoft SQL Server
- **mssql-django**: Driver Django para SQL Server
- **pyodbc**: Conector ODBC para SQL Server

### ⚡ Processamento Assíncrono
- **Celery 5.5.2**: Sistema de filas de tarefas
- **django-celery-beat**: Agendador de tarefas Django
- **django-celery-results**: Armazenamento de resultados
- **Redis**: Broker de mensagens e cache

### 📅 Agendamento de Tarefas
- **django-cron**: Tarefas cron no Django
- **django-crontab**: Gerenciamento de crontab
- **python-crontab**: Interface Python para crontab

### 📄 Geração de Relatórios PDF
- **ReportLab 4.2.5**: Biblioteca principal para PDF
- **Pillow**: Processamento de imagens

### 📊 Exportação Excel
- **OpenPyXL**: Criação e manipulação de arquivos Excel
- **et_xmlfile**: Dependência do OpenPyXL

### 🌐 Processamento Web
- **requests**: Cliente HTTP
- **urllib3**: Biblioteca HTTP de baixo nível
- **beautifulsoup4**: Parser HTML/XML

### 🧮 Processamento de Dados
- **NumPy**: Computação científica
- **python-dateutil**: Manipulação avançada de datas

## 🛠️ Dependências de Desenvolvimento

### 🐛 Debug e Desenvolvimento
- **django-debug-toolbar**: Barra de debug para Django
- **django-extensions**: Extensões úteis para Django

### 🧪 Testes
- **pytest**: Framework de testes
- **pytest-django**: Integração pytest com Django
- **pytest-cov**: Cobertura de testes
- **factory-boy**: Criação de objetos para testes

### 📝 Formatação de Código
- **black**: Formatador de código Python
- **flake8**: Linter Python
- **isort**: Organizador de imports

### 📚 Documentação
- **Sphinx**: Gerador de documentação
- **sphinx-rtd-theme**: Tema Read the Docs

## 🔧 Configuração do Ambiente

### 1. Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///db_sistema.sqlite3
REDIS_URL=redis://localhost:6379/0
```

### 2. Configuração do Banco de Dados

#### SQLite (Desenvolvimento)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_sistema.sqlite3',
    }
}
```

#### SQL Server (Produção)
```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'db_os',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'servidor',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}
```

### 3. Configuração do Redis
```bash
# Windows (via Chocolatey)
choco install redis-64

# Docker
docker run -d -p 6379:6379 redis:alpine

# WSL/Linux
sudo apt-get install redis-server
```

## 🚨 Resolução de Problemas

### ❌ Erro: Microsoft Visual C++ 14.0 is required
**Solução**: Instale o Build Tools for Visual Studio
```bash
# Download: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019
```

### ❌ Erro: pyodbc installation failed
**Solução**: Instale o ODBC Driver 17 para SQL Server
```bash
# Download: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
```

### ❌ Erro: Redis connection failed
**Solução**: Verifique se o Redis está rodando
```bash
redis-cli ping
# Deve retornar: PONG
```

### ❌ Erro: Permission denied (Windows)
**Solução**: Execute como administrador
```bash
# Abra CMD/PowerShell como administrador
```

## 📊 Comandos Úteis

### 🔍 Verificar Dependências
```bash
pip list
pip show django
pip check
```

### 🔄 Atualizar Dependências
```bash
pip list --outdated
pip install --upgrade package_name
```

### 🧹 Limpar Cache
```bash
pip cache purge
python -m pip install --force-reinstall package_name
```

## 📈 Monitoramento

### 🎯 Health Check
Execute regularmente para verificar a saúde do sistema:
```bash
python validate_dependencies.py
python manage.py check
python manage.py test
```

### 📊 Métricas de Performance
- **Django Debug Toolbar**: Análise de queries e performance
- **Celery Flower**: Monitoramento de tarefas assíncronas
- **Redis Monitor**: Uso de memória e conexões

## 🆘 Suporte

### 📞 Contatos
- **Desenvolvedor**: Equipe TI
- **Documentação**: README.md principal
- **Issues**: Abrir chamado no sistema interno

### 🔗 Links Úteis
- [Django Documentation](https://docs.djangoproject.com/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [ReportLab Documentation](https://www.reportlab.com/docs/)
- [OpenPyXL Documentation](https://openpyxl.readthedocs.io/)

---
*Atualizado em: Dezembro 2025*
*Versão do Sistema: 2.0*
