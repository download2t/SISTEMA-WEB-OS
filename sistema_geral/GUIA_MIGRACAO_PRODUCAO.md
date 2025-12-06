# 🚀 Guia de Migração para Produção - Sistema WEB OS

## 🎯 Visão Geral
Este guia descreve como migrar um ambiente de produção existente para a nova versão do Sistema WEB OS com dependências organizadas e melhorias de layout.

## ⚠️ IMPORTANTE - Leia Antes de Começar

### 📋 Pré-requisitos
- [ ] Acesso ao servidor de produção
- [ ] Backup completo do sistema atual
- [ ] Janela de manutenção agendada
- [ ] Usuários notificados sobre a manutenção
- [ ] Python 3.8+ instalado
- [ ] Virtual environment configurado

### 🔄 Resumo das Principais Mudanças
- **Requirements.txt reorganizado** por categorias
- **Melhorias no layout PDF** (margens, tabelas, legenda)
- **Dashboard modernizado** com botões expandir/retrair
- **Scripts de automação** para instalação e validação
- **Documentação completa** de dependências

## 🚨 Plano de Rollback
**SEMPRE tenha um plano de volta!**
1. Backup do banco de dados atual
2. Backup dos arquivos de configuração
3. Lista das versões das dependências atuais
4. Procedimento de restauração testado

## 📝 Checklist de Migração

### 1️⃣ **Preparação (Antes da Manutenção)**
```bash
# 1.1. Fazer backup completo
cp -r /caminho/para/projeto /backup/projeto_$(date +%Y%m%d_%H%M%S)

# 1.2. Documentar versões atuais
pip freeze > requirements_old_$(date +%Y%m%d).txt

# 1.3. Fazer backup do banco
# SQLite
cp db_sistema.sqlite3 db_sistema_backup_$(date +%Y%m%d_%H%M%S).sqlite3

# SQL Server
# Usar SQL Server Management Studio ou script de backup
```

### 2️⃣ **Durante a Manutenção**

#### A. Parar Serviços
```bash
# Parar servidor web (exemplo Apache)
sudo systemctl stop apache2
# ou
sudo systemctl stop nginx

# Parar Celery workers
sudo systemctl stop celery
sudo systemctl stop celery-beat

# Ou se rodando manualmente:
# Ctrl+C nos terminais do Celery
```

#### B. Atualizar Código
```bash
# Ir para o diretório do projeto
cd /caminho/para/sistema-web-os/sistema_geral

# Fazer backup local adicional
git stash  # Se houver modificações locais

# Buscar atualizações
git fetch origin
git pull origin main

# Verificar se atualizou corretamente
git log --oneline -5
```

#### C. Migração Automatizada
```bash
# Executar script de migração
python migrate_to_production.py
```

**OU Migração Manual:**

```bash
# 1. Ativar virtual environment
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 2. Verificar Python
python --version  # Deve ser 3.8+

# 3. Atualizar pip
python -m pip install --upgrade pip

# 4. Instalar/atualizar dependências
pip install -r requirements.txt --upgrade

# 5. Verificar conflitos
pip check

# 6. Migrações do banco
python manage.py makemigrations
python manage.py migrate

# 7. Coletar arquivos estáticos
python manage.py collectstatic --noinput --clear

# 8. Verificar configuração
python manage.py check

# 9. Validar dependências (se disponível)
python validate_dependencies.py
```

#### D. Reiniciar Serviços
```bash
# Reiniciar Redis (se necessário)
sudo systemctl restart redis

# Reiniciar Celery
sudo systemctl start celery
sudo systemctl start celery-beat

# Reiniciar servidor web
sudo systemctl start apache2
# ou
sudo systemctl start nginx

# Verificar status
sudo systemctl status apache2
sudo systemctl status celery
```

### 3️⃣ **Validação Pós-Migração**

#### Testes Essenciais
```bash
# 1. Testar importações Python
python -c "import django, celery, reportlab, openpyxl; print('✅ Importações OK')"

# 2. Verificar Django
python manage.py check

# 3. Testar conexão com banco
python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); print('✅ Banco OK')"

# 4. Verificar logs
tail -f /var/log/apache2/error.log  # Ajustar caminho conforme necessário
```

#### Testes Funcionais
- [ ] **Login no sistema**: Acessar com usuário admin
- [ ] **Dashboard**: Verificar se carrega corretamente
- [ ] **Controle de Quartos**: Criar um novo registro
- [ ] **Geração de PDF**: Exportar relatório
- [ ] **Botões expandir/retrair**: Testar funcionalidade
- [ ] **Responsividade**: Testar em dispositivos móveis

### 4️⃣ **Monitoramento Pós-Migração**

#### Primeiras 24 horas
```bash
# Monitorar logs continuamente
tail -f /var/log/apache2/error.log
tail -f /caminho/para/logs/django.log

# Verificar uso de recursos
htop
df -h

# Testar endpoints críticos
curl -I http://seu-servidor/admin/
curl -I http://seu-servidor/governanca/quartos/dashboard/
```

## 🔧 Resolução de Problemas

### ❌ Problema: Erro de Dependências
```bash
# Solução 1: Reinstalar requirements
pip uninstall -r requirements_old.txt -y
pip install -r requirements.txt

# Solução 2: Limpar cache pip
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

### ❌ Problema: Erro de Migração
```bash
# Solução 1: Migração fake (se tabela já existe)
python manage.py migrate --fake-initial

# Solução 2: Migração específica
python manage.py migrate governanca 0001 --fake
python manage.py migrate governanca
```

### ❌ Problema: Arquivos Estáticos
```bash
# Limpar e recoletar
rm -rf /caminho/para/static/*
python manage.py collectstatic --noinput
```

### ❌ Problema: Permissões
```bash
# Ajustar permissões (exemplo)
chown -R www-data:www-data /caminho/para/projeto
chmod -R 644 /caminho/para/projeto
chmod +x /caminho/para/projeto/manage.py
```

## 🔄 Rollback (Se Necessário)

### Rollback Rápido
```bash
# 1. Parar serviços
sudo systemctl stop apache2 celery celery-beat

# 2. Restaurar backup do banco
cp db_sistema_backup_TIMESTAMP.sqlite3 db_sistema.sqlite3

# 3. Voltar versão do código
git reset --hard COMMIT_ANTERIOR
# ou restaurar backup completo

# 4. Restaurar dependências antigas
pip uninstall -r requirements.txt -y
pip install -r requirements_old.txt

# 5. Reiniciar serviços
sudo systemctl start apache2 celery celery-beat
```

## 📊 Checklist Final

### Validação Completa ✅
- [ ] Sistema acessível via browser
- [ ] Login funcionando
- [ ] Dashboard carregando
- [ ] Botões expandir/retrair funcionando
- [ ] Criação de registros funcionando
- [ ] Exportação PDF funcionando (com layout melhorado)
- [ ] Responsive design funcionando
- [ ] Logs sem erros críticos
- [ ] Performance adequada
- [ ] Celery processando tarefas
- [ ] Backup realizado e validado

### Comunicação ✅
- [ ] Usuários notificados sobre conclusão
- [ ] Documentação atualizada
- [ ] Equipe treinada nas novas funcionalidades
- [ ] Monitoramento configurado

## 📞 Contatos de Emergência

### Em caso de problemas críticos:
1. **Equipe TI**: [contato]
2. **Desenvolvedor**: [contato]
3. **Administrador do Sistema**: [contato]

### Horários de Suporte:
- **Segunda a Sexta**: 8h às 18h
- **Emergências**: 24h (apenas críticas)

## 📈 Métricas de Sucesso

### KPIs da Migração:
- **Downtime**: < 30 minutos
- **Performance**: Mantida ou melhorada
- **Bugs críticos**: 0
- **Satisfação do usuário**: > 95%

---

**⚠️ LEMBRE-SE:**
- **SEMPRE faça backup antes de começar**
- **Teste em ambiente de homologação primeiro**
- **Tenha um plano de rollback**
- **Monitore o sistema após a migração**
- **Documente qualquer problema encontrado**

---
*Guia criado em: Dezembro 2025*  
*Versão do Sistema: 2.0*  
*Última atualização: {{ data_atual }}*
