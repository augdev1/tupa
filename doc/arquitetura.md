# Arquitetura - TUPA

## Visão Geral

O sistema TUPA utiliza uma arquitetura MVC (Model-View-Controller) baseada em Flask, com separação clara de responsabilidades e modularidade. O sistema é projetado para ser escalável, manutenível e seguro.

## Arquitetura Geral

```
┌─────────────────────────────────────────────────────────────┐
│                        Cliente                               │
│  (Navegador Web - Desktop, Tablet, Mobile)                  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask Application                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Routes (Controller)                      │  │
│  │  - Autenticação                                       │  │
│  │  - Gestão de Usuários                                │  │
│  │  - Gestão de Fazendas                                │  │
│  │  - Gestão de Plantios                                 │  │
│  │  - Monitoramento                                      │  │
│  │  - Alertas                                            │  │
│  │  - Chatbot                                            │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Models (Model)                            │  │
│  │  - User                                               │  │
│  │  - Farm                                               │  │
│  │  - Crop                                               │  │
│  │  - Sensor                                             │  │
│  │  - Device                                             │  │
│  │  - WaterTank                                          │  │
│  │  - Alert                                              │  │
│  │  - Conversation                                       │  │
│  │  - DailySummary                                      │  │
│  │  - AlertConfig                                        │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Templates (View)                          │  │
│  │  - base.html                                          │  │
│  │  - dashboard.html                                     │  │
│  │  - plantios.html                                      │  │
│  │  - plantios_detail.html                               │  │
│  │  - monitor.html                                       │  │
│  │  - alerts.html                                        │  │
│  │  - profile.html                                       │  │
│  │  - profile_edit.html                                  │  │
│  │  - login.html                                         │  │
│  │  - register.html                                      │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Banco de Dados                           │
│  SQLite (com SQLAlchemy ORM)                                │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    APIs Externas                            │
│  - Open-Meteo API (Clima)                                   │
│  - HIDROWEB API (ANA - Nível do Rio)                        │
│  - Groq API (Chatbot)                                       │
│  - NewsAPI (Notícias - opcional)                            │
└─────────────────────────────────────────────────────────────┘
```

## Camadas da Aplicação

### 1. Camada de Apresentação (View)

**Responsabilidades:**
- Renderizar templates HTML
- Exibir dados ao usuário
- Receber inputs do usuário
- Validação básica de formulários

**Tecnologias:**
- Jinja2 (Template Engine)
- TailwindCSS (CSS)
- Font Awesome (Ícones)
- Vanilla JavaScript (ES6+)

**Arquivos:**
- `app/templates/` - Todos os templates HTML
- `app/static/` - Arquivos estáticos (CSS, JS, imagens)

### 2. Camada de Controle (Controller)

**Responsabilidades:**
- Receber requisições HTTP
- Validar dados de entrada
- Chamar serviços de negócio
- Retornar respostas apropriadas
- Gerenciar sessões e autenticação

**Tecnologias:**
- Flask 3.1.3
- Flask-Login (Autenticação)
- Flask-WTF (Formulários)

**Arquivos:**
- `app/routes.py` - Todas as rotas e lógica de controle

**Principais Rotas:**
- `/` - Dashboard
- `/login` - Login
- `/register` - Registro
- `/plantios` - Lista de plantios
- `/plantios/<id>` - Detalhes do plantio
- `/plantios/<id>/chat` - Chatbot
- `/monitor` - Monitoramento
- `/alerts` - Sistema de alertas
- `/profile` - Perfil do usuário
- `/profile/edit` - Edição de perfil
- `/change-password` - Alteração de senha (POST)

### 3. Camada de Modelo (Model)

**Responsabilidades:**
- Definir estrutura do banco de dados
- Validar regras de negócio
- Realizar operações CRUD
- Gerenciar relacionamentos

**Tecnologias:**
- SQLAlchemy 2.0.49 (ORM)
- Flask-SQLAlchemy
- SQLite (Banco de Dados)

**Arquivos:**
- `app/models.py` - Todos os modelos de dados

**Principais Modelos:**
- `User` - Usuário do sistema
- `Farm` - Fazenda
- `Crop` - Plantação/Cultivo
- `Sensor` - Sensor IoT
- `Device` - Dispositivo automatizado
- `WaterTank` - Reservatório de água
- `Alert` - Alerta do sistema
- `Conversation` - Conversa com chatbot
- `DailySummary` - Resumo diário
- `AlertConfig` - Configuração de alertas

## Padrões de Projeto

### 1. MVC (Model-View-Controller)

O sistema segue o padrão MVC para separar responsabilidades:
- **Model**: `app/models.py` - Lógica de dados
- **View**: `app/templates/` - Interface do usuário
- **Controller**: `app/routes.py` - Lógica de controle

### 2. Repository Pattern

Os modelos SQLAlchemy atuam como repositories, fornecendo:
- Métodos de consulta (`get_latest_reading()`)
- Métodos de cálculo (`get_progress()`, `get_current_level()`)
- Abstração do banco de dados

### 3. Service Layer (Futuro)

Planejado para separar lógica de negócio dos controllers:
- `app/services/user_service.py`
- `app/services/crop_service.py`
- `app/services/alert_service.py`

### 4. Dependency Injection (Futuro)

Planejado para injetar dependências nos controllers:
- Injeção de serviços
- Injeção de repositories
- Facilitar testes

## Estrutura de Diretórios

```
tupa/
├── app/
│   ├── __init__.py              # Inicialização do Flask app
│   ├── models.py                # Modelos SQLAlchemy
│   ├── routes.py                # Rotas e controllers
│   ├── config.py                # Configurações
│   ├── services/                # Serviços de negócio (futuro)
│   ├── templates/               # Templates Jinja2
│   │   ├── base.html           # Template base
│   │   ├── dashboard.html      # Dashboard
│   │   ├── plantios.html       # Lista de plantios
│   │   ├── plantios_detail.html # Detalhes do plantio
│   │   ├── monitor.html        # Monitoramento
│   │   ├── alerts.html         # Alertas
│   │   ├── profile.html        # Perfil
│   │   ├── login.html          # Login
│   │   └── register.html       # Registro
│   └── static/                  # Arquivos estáticos
│       ├── css/                # Arquivos CSS
│       ├── js/                 # Arquivos JavaScript
│       └── images/             # Imagens
├── doc/                        # Documentação
│   ├── README.md
│   ├── banco_de_dados.md
│   ├── regras_de_negocio.md
│   ├── rf.md
│   ├── rnf.md
│   └── arquitetura.md
├── migrations/                  # Migrações do banco de dados
├── venv/                       # Ambiente virtual Python
├── .env                        # Variáveis de ambiente
├── .env.example               # Exemplo de variáveis de ambiente
├── requirements.txt            # Dependências Python
├── run.py                     # Script de execução
└── config.py                  # Configurações adicionais
```

## Fluxo de Dados

### 1. Fluxo de Autenticação

```
Usuário → Formulário Login → POST /login
    ↓
Route (Controller)
    ↓
Valida credenciais
    ↓
Flask-Login cria sessão
    ↓
Redireciona para Dashboard
```

### 2. Fluxo de Criação de Plantio

```
Usuário → Formulário Plantio → POST /plantios
    ↓
Route (Controller)
    ↓
Valida dados
    ↓
Cria instância de Crop
    ↓
Salva no banco de dados
    ↓
Redireciona para lista de plantios
```

### 3. Fluxo de Monitoramento

```
Usuário → GET /monitor
    ↓
Route (Controller)
    ↓
Busca fazendas do usuário
    ↓
Busca sensores e dispositivos
    ↓
Busca dados da API de clima
    ↓
Renderiza template com dados
    ↓
JavaScript atualiza em tempo real
```

### 4. Fluxo de Chatbot

```
Usuário → Formulário Chat → POST /plantios/<id>/chat
    ↓
Route (Controller)
    ↓
Busca histórico de conversa
    ↓
Chama Groq API com contexto especializado
    ↓
Salva mensagem do usuário
    ↓
Salva resposta do assistente
    ↓
Retorna resposta JSON
    ↓
JavaScript atualiza chat
```

## Integrações

### 1. Open-Meteo API (Clima)

**Endpoint:**
```
https://api.open-meteo.com/v1/forecast
```

**Parâmetros:**
- Latitude: -3.1190 (Manaus)
- Longitude: -60.0217 (Manaus)
- Current: temperature_2m, relative_humidity_2m, weather_code, wind_speed_10m, surface_pressure
- Daily: temperature_2m_max, temperature_2m_min, precipitation_sum, weather_code
- Timezone: America/Manaus
- Forecast_days: 7

**Uso:**
- Dados de clima atual
- Previsão semanal
- Gráfico de temperatura

### 2. HIDROWEB API (ANA - Nível do Rio)

**Endpoint:**
```
https://snirh.snirh.gov.br/snirh/api/v1/telemetria/estacoes
```

**Parâmetros:**
- Código: 14020000 (Rio Negro em Manaus)
- Tipo de dados: NIVEL

**Uso:**
- Nível atual do Rio Negro
- Comparação com média anual
- Alertas de inundação/seca

### 3. Groq API (Chatbot)

**Endpoint:**
```
https://api.groq.com/openai/v1/chat/completions
```

**Parâmetros:**
- Model: meta-llama/llama-4-scout-17b-16e-instruct
- Messages: Histórico de conversa + contexto especializado
- Temperature: 1
- Max tokens: 1024

**Contextos Especializados:**
- Café: Manejo, nutrição, pragas, doenças, colheita
- Milho: Manejo, nutrição, pragas, doenças, colheita
- Soja: Manejo, nutrição, pragas, doenças, colheita
- Arroz: Manejo, nutrição, pragas, doenças, colheita
- Trigo: Manejo, nutrição, pragas, doenças, colheita
- Cana: Manejo, nutrição, pragas, doenças, colheita

### 4. NewsAPI (Notícias - Opcional)

**Endpoint:**
```
https://newsapi.org/v2/everything
```

**Parâmetros:**
- Query: agricultura
- Language: pt
- Sort by: publishedAt
- Page size: 5

**Uso:**
- Notícias de agricultura no dashboard

## Segurança

### 1. Autenticação

- Flask-Login para gerenciamento de sessão
- Senhas armazenadas como hash (bcrypt)
- Sessão expira após 30 minutos de inatividade
- Proteção CSRF com Flask-WTF

### 2. Autorização

- Decorador `@login_required` em rotas sensíveis
- Validação de propriedade de dados
- Filtros por usuário em todas as consultas

### 3. Proteção de Dados

- Variáveis de ambiente para chaves de API
- Chaves não expostas no frontend
- SQL Injection prevenido pelo SQLAlchemy
- XSS prevenido pelo escaping do Jinja2

## Performance

### 1. Otimizações Atuais

- Índices no banco de dados
- Consultas otimizadas com SQLAlchemy
- Lazy loading de relacionamentos
- Cache de templates

### 2. Otimizações Futuras

- Redis para cache
- CDN para assets estáticos
- Paginação de dados
- Compressão GZIP

## Escalabilidade

### 1. Escalabilidade Vertical

- Aumento de recursos do servidor
- Otimização de consultas
- Arquivamento de dados antigos

### 2. Escalabilidade Horizontal (Futuro)

- Load balancer
- Múltiplos servidores
- Banco de dados separado
- Microserviços

## Monitoramento e Logging

### 1. Logging

- Logs de erros
- Logs de requisições
- Logs de acesso
- Logs estruturados

### 2. Monitoramento (Futuro)

- Métricas de CPU, RAM, Disco
- Monitoramento de requisições por segundo
- Alertas de alta latência
- Dashboard de monitoramento

## Deploy

### 1. Ambiente de Desenvolvimento

- SQLite local
- Flask development server
- Debug mode ativado

### 2. Ambiente de Produção (Futuro)

- PostgreSQL
- Gunicorn ou uWSGI
- Nginx como proxy reverso
- SSL/HTTPS
- Docker containers

## Backup e Recuperação

### 1. Backup

- Backup diário automático do banco de dados
- Backup semanal completo
- Backup mensal arquivado
- Armazenamento em local seguro

### 2. Recuperação

- RPO: 24 horas
- RTO: 4 horas
- Processo de recuperação documentado
- Testes regulares de backup

## Tecnologias Utilizadas

### Backend
- Python 3.8+
- Flask 3.1.3
- SQLAlchemy 2.0.49
- Flask-SQLAlchemy
- Flask-Login
- Flask-Migrate
- Flask-WTF
- requests (APIs externas)
- groq (Chatbot)

### Frontend
- Jinja2
- TailwindCSS
- Font Awesome
- Vanilla JavaScript (ES6+)

### Banco de Dados
- SQLite (desenvolvimento)
- PostgreSQL (produção - futuro)

### APIs Externas
- Open-Meteo API (Clima)
- HIDROWEB API (ANA)
- Groq API (Chatbot)
- NewsAPI (Notícias - opcional)
