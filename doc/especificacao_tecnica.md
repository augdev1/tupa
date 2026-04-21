# Especificação Técnica - TUPA

## 1. Introdução

### 1.1 Propósito
Este documento descreve a especificação técnica detalhada do sistema TUPA - Sistema de Gestão Agrícola Inteligente, incluindo requisitos técnicos, arquitetura, tecnologias, padrões e diretrizes de implementação.

### 1.2 Escopo
O sistema TUPA é uma aplicação web para gestão agrícola que integra monitoramento IoT, previsão do tempo, nível de rios e inteligência artificial especializada em culturas agrícolas.

### 1.3 Definições e Abreviações
- **TUPA**: Sistema de Gestão Agrícola Inteligente
- **IoT**: Internet of Things
- **API**: Application Programming Interface
- **ORM**: Object-Relational Mapping
- **MVC**: Model-View-Controller
- **RF**: Requisitos Funcionais
- **RNF**: Requisitos Não-Funcionais
- **LGPD**: Lei Geral de Proteção de Dados Pessoais

## 2. Visão Geral do Sistema

### 2.1 Objetivos
- Monitorar plantações em tempo real através de sensores IoT
- Gerenciar fazendas, plantios e dispositivos automatizados
- Fornecer alertas inteligentes para condições críticas
- Integrar dados de clima e nível de rios
- Oferecer assistente de IA especializado em culturas agrícolas

### 2.2 Stakeholders
- Agricultores e proprietários rurais
- Engenheiros agrônomos
- Técnicos em agricultura
- Administradores do sistema

### 2.3 Contexto Operacional
O sistema opera como uma aplicação web acessível via navegador, com integração com APIs externas para dados de clima, nível de rios e inteligência artificial.

## 3. Arquitetura Técnica

### 3.1 Arquitetura Geral
```
┌─────────────────────────────────────────────────────────┐
│                    Camada de Apresentação                 │
│  (Navegador Web - HTML, CSS, JavaScript)                │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/HTTPS
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    Camada de Aplicação                    │
│  (Flask - MVC Architecture)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Controller  │  │    Model     │  │    View      │  │
│  │  (Routes)    │  │  (SQLAlchemy) │  │  (Jinja2)    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Camada de Dados                        │
│  (SQLite com SQLAlchemy ORM)                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  APIs Externas                          │
│  - Open-Meteo (Clima)                                   │
│  - HIDROWEB/ANA (Nível do Rio)                          │
│  - Groq (Chatbot)                                        │
│  - NewsAPI (Notícias)                                    │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Padrão MVC
- **Model**: `app/models.py` - Entidades do banco de dados e lógica de negócio
- **View**: `app/templates/` - Templates Jinja2 para renderização HTML
- **Controller**: `app/routes.py` - Rotas Flask e lógica de controle

### 3.3 Componentes Principais

#### 3.3.1 Backend
- **Framework**: Flask 3.1.3
- **ORM**: SQLAlchemy 2.0.49
- **Autenticação**: Flask-Login
- **Formulários**: Flask-WTF
- **Migrações**: Flask-Migrate com Alembic
- **HTTP Client**: requests 2.32.3
- **Chatbot**: groq 0.11.2

#### 3.3.2 Frontend
- **Template Engine**: Jinja2
- **CSS Framework**: TailwindCSS
- **Ícones**: Font Awesome 6.5.1
- **JavaScript**: Vanilla ES6+

#### 3.3.3 Banco de Dados
- **Desenvolvimento**: SQLite
- **Produção**: PostgreSQL (planejado)
- **ORM**: SQLAlchemy

## 4. Especificação de Módulos

### 4.1 Módulo de Autenticação

#### 4.1.1 Funcionalidades
- Registro de usuário
- Login/Logout
- Recuperação de senha
- Alteração de senha
- Gerenciamento de perfil

#### 4.1.2 Rotas
- `GET /register` - Formulário de registro
- `POST /register` - Processar registro
- `GET /login` - Formulário de login
- `POST /login` - Processar login
- `GET /logout` - Logout
- `GET /profile` - Perfil do usuário
- `POST /profile` - Atualizar perfil

#### 4.1.3 Segurança
- Senhas armazenadas como hash (bcrypt)
- Sessão expira após 30 minutos
- Proteção CSRF com Flask-WTF
- Validação de email e username únicos

### 4.2 Módulo de Gestão de Perfil

#### 4.2.1 Funcionalidades
- Visualizar perfil do usuário
- Editar informações pessoais
- Upload de foto de perfil
- Alterar senha via modal
- Visualizar estatísticas (fazendas, plantios, sensores)
- Lista de fazendas associadas

#### 4.2.2 Rotas
- `GET /profile` - Visualizar perfil
- `GET /profile/edit` - Formulário de edição de perfil
- `POST /profile/edit` - Atualizar perfil
- `POST /change-password` - Alterar senha (AJAX)

#### 4.2.3 Formulários
- **ProfileForm**: full_name, email, phone, profile_image, alert_email, alert_sms, alert_push
- **ChangePasswordForm**: current_password, new_password, confirm_password

#### 4.2.4 Upload de Foto
- Pasta: `app/static/uploads/profile_images/`
- Formatos aceitos: PNG, JPG, JPEG
- Tamanho máximo: 5MB
- Nome do arquivo: `{user_id}_{original_filename}`
- Armazenamento: Caminho relativo no banco de dados

#### 4.2.5 Validações
- Email único
- Telefone opcional
- Senha atual obrigatória para alteração
- Nova senha mínimo 8 caracteres
- Confirmação de senha deve coincidir

#### 4.2.6 Preferências de Notificação
- alert_email: Boolean (default: True)
- alert_sms: Boolean (default: False)
- alert_push: Boolean (default: True)

### 4.3 Módulo de Gestão de Fazendas

#### 4.3.1 Funcionalidades
- CRUD de fazendas
- Listagem de fazendas do usuário
- Detalhes da fazenda com recursos associados

#### 4.3.2 Rotas
- `GET /farms` - Listar fazendas
- `GET /farms/new` - Formulário de criação
- `POST /farms/new` - Criar fazenda
- `GET /farms/<id>/edit` - Formulário de edição
- `POST /farms/<id>/edit` - Atualizar fazenda
- `POST /farms/<id>/delete` - Excluir fazenda

#### 4.3.3 Validações
- Nome único por usuário
- Localização obrigatória
- Não pode excluir com plantios ativos

### 4.4 Módulo de Gestão de Plantios

#### 4.4.1 Funcionalidades
- CRUD de plantios
- Cronômetro regressivo para colheita
- Controle de irrigação (bomba)
- Controle de LED UV
- Chatbot especialista
- Cálculo de progresso

#### 4.4.2 Rotas
- `GET /plantios` - Listar plantios
- `GET /plantios/new` - Formulário de criação
- `POST /plantios/new` - Criar plantio
- `GET /plantios/<id>` - Detalhes do plantio
- `POST /plantios/<id>/edit` - Atualizar plantio
- `POST /plantios/<id>/delete` - Excluir plantio
- `POST /plantios/<id>/irrigate` - Ativar irrigação
- `POST /plantios/<id>/led_on` - Ativar LED
- `POST /plantios/<id>/led_off` - Desativar LED
- `POST /plantios/<id>/chat` - Chatbot

#### 4.4.3 Cálculos
- **Progresso**: `(data atual - data plantio) / (data colheita - data plantio) * 100`
- **Cronômetro**: Tempo restante até data de colheita
- **Nível reservatório**: `(nível atual / capacidade) * 100`

### 4.5 Módulo de Sensores IoT

#### 4.5.1 Funcionalidades
- CRUD de sensores
- Leituras em tempo real
- Histórico de leituras
- Gráficos de tendências
- Alertas automáticos

#### 4.5.2 Rotas
- `GET /sensors` - Listar sensores
- `GET /sensors/new` - Formulário de criação
- `POST /sensors/new` - Criar sensor
- `GET /sensors/<id>` - Detalhes do sensor
- `POST /sensors/<id>/edit` - Atualizar sensor
- `POST /sensors/<id>/delete` - Excluir sensor
- `POST /sensors/<id>/toggle` - Ativar/Desativar

#### 4.5.3 Tipos de Sensores
- `umidade_solo`: Umidade do solo em %
- `temperatura`: Temperatura em °C
- `nivel_agua`: Nível de água em metros
- `ultrassonico`: Detecção de água (booleano)

#### 4.5.4 Alertas Automáticos
- Umidade < 20%: Alerta de seca
- Nível > 80%: Alerta de inundação
- Nível < 20%: Alerta de nível baixo
- Ultrassônico detecta água: Alerta de inundação

### 4.6 Módulo de Dispositivos

#### 4.6.1 Funcionalidades
- CRUD de dispositivos
- Controle remoto (ligar/desligar)
- Status em tempo real

#### 4.6.2 Rotas
- `GET /devices` - Listar dispositivos
- `GET /devices/new` - Formulário de criação
- `POST /devices/new` - Criar dispositivo
- `POST /devices/<id>/toggle` - Ligar/Desligar

#### 4.6.3 Tipos de Dispositivos
- `bomba`: Bomba de irrigação
- `led_uv`: LED UV para cultivo
- `ventilador`: Ventilador

### 4.7 Módulo de Reservatórios

#### 4.7.1 Funcionalidades
- CRUD de reservatórios
- Atualização de nível
- Alerta de nível baixo

#### 4.7.2 Rotas
- `GET /tanks` - Listar reservatórios
- `GET /tanks/new` - Formulário de criação
- `POST /tanks/new` - Criar reservatório
- `POST /tanks/<id>/update_level` - Atualizar nível

### 4.8 Módulo de Alertas

#### 4.8.1 Funcionalidades
- Listagem de alertas ativos
- Histórico de alertas resolvidos
- Resolução de alertas
- Alertas piscantes para críticos
- Configuração de limites

#### 4.8.2 Rotas
- `GET /alerts` - Listar alertas
- `POST /alerts/<id>/resolve` - Resolver alerta
- `GET /alerts/config` - Configuração de alertas
- `POST /alerts/config` - Salvar configuração

#### 4.8.3 Tipos de Alertas
- `inundacao`: Alerta de inundação (crítico)
- `seca`: Alerta de seca (aviso)
- `chuva`: Alerta de chuva (aviso)
- `nivel_rio`: Alerta de nível do rio (crítico/aviso)

#### 4.8.4 Severidades
- `critical`: Vermelho piscante
- `warning`: Amarelo piscante
- `info`: Azul piscante

### 4.9 Módulo de Monitoramento

#### 4.9.1 Funcionalidades
- Dashboard de monitoramento
- Leituras em tempo real
- Gráficos de tendências
- Previsão do tempo
- Nível do Rio Negro
- Filtros por período

#### 4.9.2 Rotas
- `GET /monitor` - Dashboard de monitoramento
- `GET /sensor/<id>` - Detalhes do sensor

#### 4.9.3 Atualização
- Dashboard: a cada 30 segundos
- Gráficos: a cada 30 segundos
- Leituras: em tempo real

### 4.10 Módulo de Chatbot

#### 4.10.1 Funcionalidades
- Iniciar conversa
- Enviar mensagem
- Receber resposta
- Histórico de conversa
- Especialização por cultura

#### 4.10.2 Rotas
- `POST /plantios/<id>/chat` - Enviar mensagem

#### 4.10.3 Configuração Groq API
- **Modelo**: `meta-llama/llama-4-scout-17b-16e-instruct`
- **Temperature**: 1
- **Max tokens**: 1024
- **Timeout**: 30 segundos

#### 4.10.4 Contextos Especializados
Cada cultura tem um contexto específico com expertise agronômica:
- Café: manejo, nutrição, pragas, doenças, colheita
- Milho: manejo, nutrição, pragas, doenças, colheita
- Soja: manejo, nutrição, pragas, doenças, colheita
- Arroz: manejo, nutrição, pragas, doenças, colheita
- Trigo: manejo, nutrição, pragas, doenças, colheita
- Cana: manejo, nutrição, pragas, doenças, colheita

## 5. Especificação de APIs Externas

### 5.1 Open-Meteo API (Clima)

#### 5.1.1 Endpoint
```
GET https://api.open-meteo.com/v1/forecast
```

#### 5.1.2 Parâmetros
```python
params = {
    'latitude': -3.1190,  # Manaus
    'longitude': -60.0217,
    'current': 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,surface_pressure',
    'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code',
    'timezone': 'America/Manaus',
    'forecast_days': 7
}
```

#### 5.1.3 Resposta Esperada
```json
{
  "current": {
    "temperature_2m": 28.5,
    "relative_humidity_2m": 75,
    "weather_code": 3,
    "wind_speed_10m": 12.5,
    "surface_pressure": 1013
  },
  "daily": {
    "time": ["2024-01-01", ...],
    "temperature_2m_max": [30, 31, ...],
    "temperature_2m_min": [24, 25, ...],
    "precipitation_sum": [0, 5, ...],
    "weather_code": [3, 61, ...]
  }
}
```

#### 5.1.4 Códigos do Clima
- 0: Céu limpo
- 1-3: Principalmente limpo, parcialmente nublado, nublado
- 45, 48: Nevoeiro
- 51-67: Drizzle e chuva leve
- 80-99: Chuva forte e trovoada

### 5.2 HIDROWEB API (ANA - Nível do Rio)

#### 5.2.1 Endpoint
```
GET https://snirh.snirh.gov.br/snirh/api/v1/telemetria/estacoes
```

#### 5.2.2 Parâmetros
```python
params = {
    'codigo': '14020000',  # Estação do Rio Negro em Manaus
    'tipoDados': 'NIVEL'
}
```

#### 5.2.3 Resposta Esperada
```json
[
  {
    "valor": 18.5,
    "data_hora": "2024-01-01T12:00:00"
  }
]
```

#### 5.2.4 Valores de Referência
- Média anual: 18.0m
- Nível crítico alto: > 25m (inundação)
- Nível crítico baixo: < 12m (seca)

### 5.3 Groq API (Chatbot)

#### 5.3.1 Endpoint
```
POST https://api.groq.com/openai/v1/chat/completions
```

#### 5.3.2 Headers
```python
headers = {
    'Authorization': f'Bearer {GROQ_API_KEY}',
    'Content-Type': 'application/json'
}
```

#### 5.3.3 Payload
```python
payload = {
    'model': 'meta-llama/llama-4-scout-17b-16e-instruct',
    'messages': messages,
    'temperature': 1,
    'max_completion_tokens': 1024,
    'top_p': 1,
    'stream': False
}
```

#### 5.3.4 Resposta Esperada
```json
{
  "choices": [
    {
      "message": {
        "content": "Resposta do assistente..."
      }
    }
  ]
}
```

### 5.4 NewsAPI (Notícias - Opcional)

#### 5.4.1 Endpoint
```
GET https://newsapi.org/v2/everything
```

#### 5.4.2 Parâmetros
```python
params = {
    'q': 'agricultura',
    'language': 'pt',
    'sortBy': 'publishedAt',
    'pageSize': 5
}
```

## 6. Especificação de Banco de Dados

### 6.1 Schema

#### 6.1.1 Tabela: users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
```

#### 6.1.2 Tabela: farms
```sql
CREATE TABLE farms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200) NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### 6.1.3 Tabela: crops
```sql
CREATE TABLE crops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    crop_type VARCHAR(50) NOT NULL,
    planting_date DATE NOT NULL,
    estimated_harvest_date DATE NOT NULL,
    area_hectares FLOAT NOT NULL,
    expected_yield FLOAT NOT NULL,
    irrigation_count INTEGER DEFAULT 0,
    last_irrigation_date DATETIME,
    needs_irrigation BOOLEAN DEFAULT FALSE,
    led_status BOOLEAN DEFAULT FALSE,
    pump_status BOOLEAN DEFAULT FALSE,
    farm_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id)
);

CREATE INDEX idx_crops_farm_id ON crops(farm_id);
CREATE INDEX idx_crops_needs_irrigation ON crops(needs_irrigation);
```

#### 6.1.4 Tabela: sensors
```sql
CREATE TABLE sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    farm_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id)
);

CREATE INDEX idx_sensors_farm_id ON sensors(farm_id);
CREATE INDEX idx_sensors_is_active ON sensors(is_active);
```

#### 6.1.5 Tabela: sensor_readings
```sql
CREATE TABLE sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER NOT NULL,
    value FLOAT NOT NULL,
    unit VARCHAR(20) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id)
);

CREATE INDEX idx_sensor_readings_sensor_id ON sensor_readings(sensor_id);
CREATE INDEX idx_sensor_readings_timestamp ON sensor_readings(timestamp);
```

#### 6.1.6 Tabela: alerts
```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_at DATETIME,
    action_taken TEXT,
    farm_id INTEGER NOT NULL,
    crop_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id),
    FOREIGN KEY (crop_id) REFERENCES crops(id)
);

CREATE INDEX idx_alerts_farm_id ON alerts(farm_id);
CREATE INDEX idx_alerts_is_resolved ON alerts(is_resolved);
CREATE INDEX idx_alerts_created_at ON alerts(created_at);
```

### 6.2 Migrações

As migrações são gerenciadas pelo Flask-Migrate com Alembic:

```bash
# Criar nova migração
flask db migrate -m "descrição"

# Aplicar migrações
flask db upgrade

# Reverter última migração
flask db downgrade
```

## 7. Especificação de Frontend

### 7.1 Templates Jinja2

#### 7.1.1 Estrutura
- `base.html`: Template base com navegação e layout
- Templates herdam de `base.html` usando `{% extends "base.html" %}`
- Blocos definidos em `base.html`: `title`, `content`, `scripts`

#### 7.1.2 Componentes Comuns
- Navegação inferior (mobile)
- Barra de navegação (desktop)
- Cards de plantios
- Cards de alertas
- Gráficos SVG

### 7.2 Estilos

#### 7.2.1 TailwindCSS
- Framework CSS utilitário
- Configuração customizada
- Tema escuro

#### 7.2.2 Cores Principais
- Primary: `#EBC165` (Amarelo dourado)
- Secondary: `#98D3B7` (Verde claro)
- Background: `#0B2F25` (Verde escuro)
- Text: `#c5ebdb` (Verde claro)
- Error: `#ff6b6b` (Vermelho)
- Warning: `#EBC165` (Amarelo)
- Info: `#3b82f6` (Azul)

### 7.3 JavaScript

#### 7.3.1 Funcionalidades
- Atualização em tempo real (setInterval)
- Toggle de dispositivos
- Chatbot (fetch API)
- Filtros de período
- Gráficos dinâmicos

#### 7.3.2 Padrões
- Vanilla JavaScript ES6+
- Fetch API para requisições assíncronas
- Event listeners para interações
- Template literals para HTML dinâmico

## 8. Especificação de Segurança

### 8.1 Autenticação
- Flask-Login para gerenciamento de sessão
- Senhas hash com bcrypt
- Sessão expira após 30 minutos
- Proteção CSRF com Flask-WTF

### 8.2 Autorização
- Decorador `@login_required` em rotas sensíveis
- Validação de propriedade de dados
- Filtros por usuário em consultas

### 8.3 Proteção de Dados
- Variáveis de ambiente para chaves de API
- Chaves não expostas no frontend
- SQL Injection prevenido pelo SQLAlchemy
- XSS prevenido pelo escaping do Jinja2

### 8.4 Validação de Inputs
- Flask-WTF para validação de formulários
- Validação no backend
- Sanitização de inputs
- Validação de tipos e formatos

## 9. Especificação de Performance

### 9.1 Requisitos
- Tempo de resposta: < 2 segundos
- Dashboard carrega em < 3 segundos
- Gráficos renderizam em < 1 segundo
- Chatbot responde em < 5 segundos

### 9.2 Otimizações
- Índices no banco de dados
- Consultas otimizadas com SQLAlchemy
- Lazy loading de relacionamentos
- Cache de templates

### 9.3 Monitoramento
- Logs de requisições lentas (> 2s)
- Monitoramento de uso de recursos
- Alertas de alta latência

## 10. Especificação de Deploy

### 10.1 Ambiente de Desenvolvimento
- Python 3.8+
- SQLite local
- Flask development server
- Debug mode ativado

### 10.2 Ambiente de Produção (Planejado)
- PostgreSQL
- Gunicorn ou uWSGI
- Nginx como proxy reverso
- SSL/HTTPS
- Docker containers

### 10.3 Variáveis de Ambiente
```bash
SECRET_KEY=sua-chave-secreta
DATABASE_URL=sqlite:///agricultura.db
FLASK_ENV=production
GROQ_API_KEY=sua-chave-api-groq
NEWS_API_KEY=sua-chave-api-news
```

## 11. Especificação de Backup e Recuperação

### 11.1 Backup
- Backup diário automático do banco de dados
- Backup semanal completo
- Backup mensal arquivado
- Armazenamento em local seguro

### 11.2 Recuperação
- RPO: 24 horas
- RTO: 4 horas
- Processo de recuperação documentado
- Testes regulares de backup

## 12. Especificação de Monitoramento e Logging

### 12.1 Logging
- Logs de erros
- Logs de requisições lentas
- Logs de acessos não autorizados
- Logs estruturados

### 12.2 Métricas
- Uso de CPU
- Uso de RAM
- Uso de disco
- Requisições por segundo

## 13. Especificação de Testes (Planejado)

### 13.1 Testes Unitários
- Testes de modelos
- Testes de rotas
- Testes de serviços

### 13.2 Testes de Integração
- Testes de APIs externas
- Testes de fluxos completos

### 13.3 Testes E2E
- Testes de cenários de usuário
- Testes de UI

## 14. Especificação de Documentação

### 14.1 Documentação de Código
- Docstrings em todas as funções
- Comentários em lógica complexa
- PEP 8 compliance

### 14.2 Documentação de Usuário
- Guia de instalação
- Guia de usuário
- FAQ

### 14.3 Documentação Técnica
- README.md
- banco_de_dados.md
- regras_de_negocio.md
- rf.md
- rnf.md
- arquitetura.md
- especificacao_tecnica.md

## 15. Especificação de Compliance

### 15.1 LGPD
- Conformidade com LGPD
- Política de privacidade
- Consentimento do usuário
- Direito ao esquecimento

### 15.2 Outros
- Termos de uso
- Política de cookies
- Registro de processamento
