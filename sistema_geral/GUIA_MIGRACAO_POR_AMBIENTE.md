# 🚀 Guia de Migração por Tipo de Ambiente

## 🎯 Tipos de Ambiente Suportados

### 1. 🖥️ Servidor Windows com IIS
### 2. 🐧 Servidor Linux com Apache/Nginx
### 3. 🐳 Ambiente Docker
### 4. ☁️ Cloud (AWS, Azure, GCP)
### 5. 💻 Ambiente de Desenvolvimento Local

---

## 🖥️ 1. SERVIDOR WINDOWS COM IIS

### Pré-requisitos
- Windows Server 2016+
- IIS configurado com FastCGI
- Python 3.8+ instalado
- Virtual environment ativo

### Comandos de Migração
```powershell
# Parar IIS
iisreset /stop

# Navegar para o projeto
cd C:\inetpub\wwwroot\sistema-web-os\sistema_geral

# Ativar ambiente virtual
.\venv\Scripts\activate

# Executar validação pré-migração
python check_pre_migration.py

# Executar migração
python migrate_to_production.py

# Reiniciar IIS
iisreset /start
```

### Configurações Específicas
```ini
# web.config para IIS
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <handlers>
            <add name="Python FastCGI" 
                 path="*" 
                 verb="*" 
                 modules="FastCgiModule" 
                 scriptProcessor="C:\Python39\python.exe|C:\inetpub\wwwroot\sistema-web-os\sistema_geral\manage.py" 
                 resourceType="Unspecified" />
        </handlers>
    </system.webServer>
</configuration>
```

### Troubleshooting Windows
```powershell
# Verificar logs do IIS
Get-EventLog -LogName Application -Source "FastCGI" | Select-Object -First 10

# Verificar permissões
icacls "C:\inetpub\wwwroot\sistema-web-os" /grant "IIS_IUSRS:(OI)(CI)F"

# Verificar serviços
Get-Service -Name "W3SVC" | Format-Table -AutoSize
```

---

## 🐧 2. SERVIDOR LINUX COM APACHE/NGINX

### Apache + mod_wsgi
```bash
# Parar Apache
sudo systemctl stop apache2

# Navegar para o projeto
cd /var/www/sistema-web-os/sistema_geral

# Ativar ambiente virtual
source venv/bin/activate

# Executar validação pré-migração
python check_pre_migration.py

# Executar migração
python migrate_to_production.py

# Testar configuração Apache
sudo apache2ctl configtest

# Reiniciar Apache
sudo systemctl start apache2

# Verificar status
sudo systemctl status apache2
```

### Configuração Apache
```apache
# /etc/apache2/sites-available/sistema-web-os.conf
<VirtualHost *:80>
    ServerName seu-dominio.com
    DocumentRoot /var/www/sistema-web-os/sistema_geral
    
    WSGIDaemonProcess sistema-web-os python-home=/var/www/sistema-web-os/venv python-path=/var/www/sistema-web-os/sistema_geral
    WSGIProcessGroup sistema-web-os
    WSGIScriptAlias / /var/www/sistema-web-os/sistema_geral/sistema_geral/wsgi.py
    
    <Directory /var/www/sistema-web-os/sistema_geral>
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
    
    Alias /static /var/www/sistema-web-os/sistema_geral/staticfiles
    <Directory /var/www/sistema-web-os/sistema_geral/staticfiles>
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/sistema-web-os-error.log
    CustomLog ${APACHE_LOG_DIR}/sistema-web-os-access.log combined
</VirtualHost>
```

### Nginx + Gunicorn
```bash
# Parar serviços
sudo systemctl stop nginx
sudo systemctl stop sistema-web-os

# Executar migração
cd /var/www/sistema-web-os/sistema_geral
source venv/bin/activate
python migrate_to_production.py

# Reiniciar serviços
sudo systemctl start sistema-web-os
sudo systemctl start nginx
```

### Configuração Nginx
```nginx
# /etc/nginx/sites-available/sistema-web-os
server {
    listen 80;
    server_name seu-dominio.com;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/sistema-web-os/sistema_geral;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/sistema-web-os/sistema_geral/sistema_geral.sock;
    }
}
```

---

## 🐳 3. AMBIENTE DOCKER

### Docker Compose
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:8000"
    volumes:
      - ./sistema_geral:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    environment:
      - DEBUG=False
      - DATABASE_URL=sqlite:///db_sistema.sqlite3
    depends_on:
      - redis

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  celery:
    build: .
    command: celery -A sistema_geral worker --loglevel=info
    volumes:
      - ./sistema_geral:/app
    depends_on:
      - redis

volumes:
  static_volume:
  media_volume:
```

### Migração Docker
```bash
# Fazer backup
docker-compose exec web python manage.py dumpdata > backup_$(date +%Y%m%d).json

# Parar containers
docker-compose down

# Atualizar código
git pull origin main

# Reconstruir imagens
docker-compose build

# Executar migração
docker-compose run web python migrate_to_production.py

# Subir containers
docker-compose up -d

# Verificar logs
docker-compose logs -f web
```

---

## ☁️ 4. AMBIENTE CLOUD

### AWS (Elastic Beanstalk)
```bash
# Instalar EB CLI
pip install awsebcli

# Fazer backup
eb ssh production -c "cd /opt/python/current/app && python manage.py dumpdata > backup.json"

# Deploy da nova versão
eb deploy production

# Verificar saúde
eb health production

# Ver logs
eb logs production
```

### Azure (App Service)
```bash
# Fazer backup via portal Azure ou CLI
az webapp deployment source show --name sistema-web-os --resource-group meu-grupo

# Deploy
az webapp deployment source sync --name sistema-web-os --resource-group meu-grupo

# Verificar logs
az webapp log tail --name sistema-web-os --resource-group meu-grupo
```

### Google Cloud Platform
```bash
# Fazer backup
gcloud sql export sql INSTANCE_NAME gs://BUCKET_NAME/backup-$(date +%Y%m%d).sql

# Deploy
gcloud app deploy

# Ver logs
gcloud app logs tail -s default
```

---

## 💻 5. DESENVOLVIMENTO LOCAL

### Migração Local
```bash
# Criar backup
cp db_sistema.sqlite3 db_backup_$(date +%Y%m%d).sqlite3

# Ativar virtual environment
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Atualizar repositório
git stash  # Se houver mudanças locais
git pull origin main

# Executar migração
python migrate_to_production.py

# Testar
python manage.py runserver
```

---

## 🔧 Comandos Universais

### Verificação Pré-Migração (Todos os Ambientes)
```bash
python check_pre_migration.py
```

### Migração Automática (Todos os Ambientes)
```bash
python migrate_to_production.py
```

### Validação Pós-Migração (Todos os Ambientes)
```bash
python validate_dependencies.py
python manage.py check
python manage.py test
```

---

## 🚨 Planos de Rollback por Ambiente

### Windows IIS
```powershell
iisreset /stop
# Restaurar backup do código e banco
# Reinstalar dependências antigas: pip install -r requirements_old.txt
iisreset /start
```

### Linux Apache/Nginx
```bash
sudo systemctl stop apache2  # ou nginx
# Restaurar backup: git reset --hard COMMIT_ANTERIOR
# Restaurar banco: cp db_backup.sqlite3 db_sistema.sqlite3
sudo systemctl start apache2  # ou nginx
```

### Docker
```bash
docker-compose down
# Reverter para imagem anterior: docker-compose pull
docker-compose up -d
```

### Cloud
- **AWS**: `eb deploy --version=previous`
- **Azure**: Usar slot de staging para rollback
- **GCP**: `gcloud app versions migrate PREVIOUS_VERSION`

---

## 📞 Suporte por Ambiente

### Windows
- Event Viewer: `eventvwr.msc`
- IIS Logs: `C:\inetpub\logs\LogFiles\W3SVC1\`
- Performance Monitor: `perfmon.msc`

### Linux
- Logs Apache: `/var/log/apache2/`
- Logs Nginx: `/var/log/nginx/`
- System logs: `journalctl -u apache2`

### Docker
- Logs: `docker-compose logs`
- Shell: `docker-compose exec web /bin/bash`
- Stats: `docker stats`

### Cloud
- AWS: CloudWatch Logs
- Azure: Application Insights
- GCP: Stackdriver Logging

---

*Escolha o guia correspondente ao seu ambiente e siga as instruções específicas.*
