# 🏢 Sistema WEB OS - Sistema de Controle Integrado

> **Sistema completo para gestão de Ordens de Serviço, Controle de Quartos, Banco de Senhas, Agendamentos SPA e muito mais.**

---

## 📋 Visão Geral

O **Sistema WEB OS** é uma aplicação web Django completa e moderna, desenvolvida para atender diversas necessidades de gestão empresarial. O sistema integra múltiplos módulos que trabalham em conjunto para oferecer uma solução robusta e escalável.

### 🎯 **Principais Módulos:**

| Módulo | Descrição | Status |
|--------|-----------|---------|
| 🛠️ **Ordens de Serviço** | Gestão completa de OS, chamados e manutenções | ✅ Ativo |
| 🏨 **Governança - Quartos** | Controle de limpeza e performance de quartos | ✅ Ativo |
| 🔐 **Banco de Senhas** | Armazenamento seguro de credenciais | ✅ Ativo |
| 💆 **SPA - Agendamentos** | Sistema de agendamento para spa/massagens | ✅ Ativo |
| 📞 **Ramais** | Controle de ramais telefônicos | ✅ Ativo |
| 📺 **Canais** | Gestão de canais de comunicação | ✅ Ativo |
| 📄 **Contratos** | Gerenciamento de contratos e documentos | ✅ Ativo |

---

## 🏨 **MÓDULO GOVERNANÇA - Controle de Quartos**

### 📊 **Funcionalidades Principais:**

#### 👥 **Gestão de Funcionários**
- ✅ Cadastro completo com nome, cargo e status
- ✅ Controle de funcionários ativos/inativos  
- ✅ Interface para edição e exclusão
- ✅ Histórico de atividades

#### 🛏️ **Controle de Quartos**
- ✅ Registro diário de performance por funcionário
- ✅ Controle de quartos limpos vs. total de quartos
- ✅ Cálculo automático de porcentagem de produtividade
- ✅ Sistema inteligente que considera apenas dias úteis

#### 🏥 **Motivos de Ausência**
- ✅ Sistema flexível de motivos (Folga, Falta Justificada, Doença, etc.)
- ✅ Configuração de cores para identificação visual
- ✅ Impacto automático nos cálculos de performance
- ✅ Não afeta negativamente as estatísticas

#### 📊 **Dashboard Inteligente**
- ✅ Visão geral com estatísticas do dia/semana
- ✅ Gráfico interativo de evolução de performance individual
- ✅ Comparação entre funcionários (últimos 30 dias)
- ✅ Botões de expandir/retrair seções
- ✅ Layout responsivo e moderno
- ✅ Filtros por período (7 ou 30 dias)

#### 📄 **Relatórios Avançados**
- ✅ **PDF Profissional**: Layout moderno com cores corporativas
- ✅ **Excel Detalhado**: Dados estruturados para análise
- ✅ **Resumo Estatístico Executivo**: Ranking de funcionários
- ✅ **Dados por Período**: Performance diária detalhada
- ✅ **Gráficos e Visualizações**: Charts interativos

### 🎯 **Casos de Uso:**
- 🏨 **Hotéis**: Controle de limpeza de quartos e apartamentos
- 🏥 **Hospitais**: Controle de higienização de enfermarias
- 🏠 **Pousadas**: Gestão de arrumação e manutenção
- 🏢 **Escritórios**: Controle de limpeza de salas e ambientes
- 🏭 **Indústrias**: Monitoramento de atividades de limpeza

### 💡 **Diferenciais:**
- 🧠 **Inteligência**: Cálculos que excluem automaticamente ausências justificadas
- 🎨 **Interface Moderna**: Design responsivo e intuitivo
- 📊 **Analytics**: Performance em tempo real com métricas avançadas
- 🔧 **Flexibilidade**: Sistema adaptável a diferentes tipos de estabelecimento
- 📱 **Mobile-Friendly**: Funciona perfeitamente em dispositivos móveis

---

## 🚀 **Instalação e Configuração**

### 📦 **Instalação Rápida**

```bash
# 1. Clone o repositório
git clone [url-do-repositorio]
cd sistema_geral

# 2. Execute o setup completo
python setup_sistema.py

# 3. Crie um superusuário
python manage.py createsuperuser

# 4. Inicie o servidor
python manage.py runserver
```

### 🛠️ **Instalação Manual**

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar banco de dados
python manage.py makemigrations
python manage.py migrate

# 3. Coletar arquivos estáticos
python manage.py collectstatic

# 4. Validar instalação
python validate_dependencies.py
```

### 🔧 **Scripts Auxiliares**

| Script | Função |
|---------|--------|
| `setup_sistema.py` | Setup completo automatizado |
| `install_dependencies.py` | Instalação de dependências |
| `validate_dependencies.py` | Validação do ambiente |

---

## 🔧 **Tecnologias Utilizadas**

### 🌟 **Backend**
- **Django 5.0.9**: Framework web principal
- **Celery 5.5.2**: Processamento assíncrono
- **Redis**: Cache e broker de mensagens
- **SQLite/SQL Server**: Banco de dados

### 🎨 **Frontend**
- **Bootstrap 5**: Framework CSS responsivo
- **Chart.js**: Gráficos interativos
- **Font Awesome**: Ícones modernos
- **jQuery**: Manipulação DOM

### 📊 **Relatórios**
- **ReportLab 4.2.5**: Geração de PDF avançada
- **OpenPyXL 3.1.5**: Exportação Excel
- **Pillow**: Processamento de imagens

### 🔐 **Segurança**
- **Django Auth**: Sistema de autenticação
- **Permissions**: Controle de acesso granular
- **CSRF Protection**: Proteção contra ataques

---

## 📊 **Métricas e Analytics**

### 🎯 **Métricas Calculadas pelo Sistema:**

#### 👤 **Por Funcionário:**
- Performance diária (% de quartos limpos)
- Média semanal e mensal
- Número de dias trabalhados
- Dias com ausência justificada
- Ranking de produtividade

#### 📈 **Globais:**
- Performance média da equipe
- Tendências de melhoria/piora
- Comparação entre períodos
- Estatísticas de ausências

#### 📊 **Visualizações:**
- Gráfico de linha com evolução temporal
- Barras de progresso por funcionário
- Cards informativos com métricas principais
- Tabelas detalhadas exportáveis

---

## 🔄 **Funcionalidades Avançadas**

### ⚡ **Dashboard Interativo**
- **Tempo Real**: Dados atualizados automaticamente
- **Filtros Dinâmicos**: Por período, funcionário ou tipo
- **Exportações**: PDF e Excel com um clique
- **Responsivo**: Funciona em qualquer dispositivo

### 📄 **Sistema de Relatórios**
- **Templates Profissionais**: Layout corporativo moderno
- **Dados Estruturados**: Informações organizadas e claras
- **Gráficos Integrados**: Visualizações direto no PDF
- **Personalização**: Filtros e períodos configuráveis

### 🔧 **Administração**
- **Interface Admin Django**: Gestão completa via web
- **Logs de Auditoria**: Rastreamento de alterações
- **Backup Automático**: Proteção dos dados
- **Configurações Flexíveis**: Adaptação a diferentes cenários

---

## 🆘 **Suporte e Documentação**

### 📚 **Documentação Disponível**
- `README.md`: Documentação principal (este arquivo)
- `DEPENDENCIES.md`: Guia completo de dependências
- `ATUALIZACOES_REQUIREMENTS.md`: Log de atualizações

### 🔍 **Troubleshooting**
```bash
# Validar ambiente
python validate_dependencies.py

# Verificar configuração Django
python manage.py check

# Executar testes
python manage.py test governanca
```

### 📞 **Contato**
- **Equipe**: TI Sistema WEB OS
- **Documentação**: Arquivos MD no repositório
- **Issues**: Sistema interno de chamados

---

## 📋 **Roadmap e Futuras Implementações**

### 🎯 **Próximas Funcionalidades**
- [ ] **Dashboard Mobile**: App nativo para celulares
- [ ] **Notificações Push**: Alertas em tempo real
- [ ] **Relatórios Avançados**: Mais visualizações e métricas
- [ ] **Integração API**: Conexão com sistemas externos
- [ ] **Machine Learning**: Previsão de performance

### 🔄 **Melhorias Planejadas**
- [ ] **Performance**: Otimização de queries e cache
- [ ] **UI/UX**: Modernização da interface
- [ ] **Segurança**: Autenticação multifator
- [ ] **Escalabilidade**: Suporte a mais usuários simultâneos

---

## 📈 **Estatísticas do Projeto**

```
📁 Estrutura:
├── 🏨 Governança (Controle de Quartos)     ✅ 100%
├── 🛠️ Ordens de Serviço                   ✅ 100%
├── 🔐 Banco de Senhas                     ✅ 100%
├── 💆 SPA - Agendamentos                  ✅ 100%
├── 📞 Ramais                              ✅ 100%
├── 📺 Canais                              ✅ 100%
└── 📄 Contratos                           ✅ 100%

💻 Tecnologias: Python, Django, JavaScript, HTML5, CSS3
📊 Relatórios: PDF, Excel, Charts interativos
🔧 DevOps: Scripts automatizados, validação de ambiente
📱 Interface: Responsiva, moderna, acessível
```

---

## ✅ **Status do Projeto**

**Versão Atual**: 2.0  
**Status**: ✅ **PRODUÇÃO**  
**Última Atualização**: Dezembro 2025  
**Cobertura de Testes**: Em desenvolvimento  
**Documentação**: Completa  

---

*Sistema desenvolvido com ❤️ pela equipe TI para otimizar processos e aumentar a produtividade empresarial.*
