# TUPA - Sistema de Gestão Agrícola Inteligente

## Visão Geral

O TUPA é um sistema de gestão agrícola inteligente desenvolvido para monitorar e gerenciar plantações, fazendas, sensores IoT e dispositivos automatizados. O sistema integra dados de clima em tempo real, nível de rios e inteligência artificial para fornecer insights especializados sobre culturas agrícolas.

## Características Principais

- **Monitoramento em Tempo Real**: Acompanhamento de sensores IoT (umidade do solo, temperatura, nível de água)
- **Gestão de Plantios**: Cadastro e acompanhamento de plantações com previsão de colheita
- **Alertas Inteligentes**: Sistema de alertas para condições críticas (inundação, seca, chuvas)
- **Integração com APIs**: Dados de clima (Open-Meteo), nível do Rio Negro (ANA) e ANHANGÁ (sistema de monitoramento de queimadas)
- **Reporte de Queimadas**: Sistema para reportar queimadas com foto e localização (GPS ou mapa)
- **Chatbot Especializado**: Assistente de IA especializado em cada cultura específica (café, milho, soja, arroz)
- **Automação**: Controle de bombas de irrigação e LEDs UV
- **Dashboard Interativo**: Visualização de dados e métricas em tempo real

## Stack Tecnológico

### Backend
- **Framework**: Flask 3.1.3
- **Banco de Dados**: SQLite com SQLAlchemy 2.0.49
- **ORM**: Flask-SQLAlchemy
- **Autenticação**: Flask-Login
- **Migrações**: Flask-Migrate com Alembic
- **API de IA**: Groq API (meta-llama/llama-4-scout-17b-16e-instruct)
- **API de Clima**: Open-Meteo API
- **API de Nível de Rio**: HIDROWEB (ANA)

### Frontend
- **Template Engine**: Jinja2
- **CSS**: TailwindCSS (customizado)
- **Ícones**: Font Awesome
- **JavaScript**: Vanilla JS (ES6+)
- **Mapas**: Leaflet.js (para seleção de localização)

## Estrutura do Projeto

```
tupa/
├── app/
│   ├── __init__.py          # Inicialização do aplicativo Flask
│   ├── models.py            # Modelos do banco de dados
│   ├── routes.py            # Rotas e lógica do backend
│   ├── config.py            # Configurações do sistema
│   ├── templates/           # Templates Jinja2
│   │   ├── base.html       # Template base
│   │   ├── dashboard.html  # Dashboard principal
│   │   ├── plantios.html   # Lista de plantios
│   │   ├── plantios_detail.html  # Detalhes do plantio
│   │   ├── monitor.html    # Monitoramento em tempo real
│   │   ├── alerts.html     # Sistema de alertas
│   │   ├── reportar_queimada.html  # Reporte de queimadas
│   │   └── ...
│   └── static/              # Arquivos estáticos
├── doc/                     # Documentação
├── migrations/              # Migrações do banco de dados
├── venv/                    # Ambiente virtual Python
├── .env                     # Variáveis de ambiente
├── requirements.txt         # Dependências Python
├── run.py                   # Script de execução
└── config.py                # Configurações adicionais
```

## Instalação

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)
- venv (ambiente virtual)

### Passos de Instalação

1. Clone o repositório:
```bash
git clone <repositório>
cd tupa
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

6. Execute as migrações do banco de dados:
```bash
flask db upgrade
```

7. Execute o aplicativo:
```bash
python run.py
```

8. Acesse o sistema em:
```
http://localhost:5000
```

## Configuração

### Variáveis de Ambiente

As seguintes variáveis de ambiente devem ser configuradas no arquivo `.env`:

```
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///agricultura.db
FLASK_ENV=development
GROQ_API_KEY=sua-chave-api-groq-aqui
NEWS_API_KEY=sua-chave-api-news-aqui (opcional)
ANHANGA_URL=http://localhost:5000 (opcional, padrão: http://localhost:5000)
```

### API Keys

- **Groq API**: Necessária para o chatbot especializado em culturas
- **NewsAPI**: Opcional, para notícias de agricultura no dashboard

## Funcionalidades

### Dashboard
- Visão geral dos plantios ativos
- Mini cards com progresso dos plantios
- Notícias de agricultura (NewsAPI)
- Métricas em tempo real

### Plantios
- Cadastro de novos plantios
- Detalhes do plantio (data, cultura, área, produção esperada)
- Cronômetro regressivo para colheita
- Controle de irrigação (bomba)
- Controle de LEDs UV
- Chatbot especialista na cultura

### Monitoramento
- Dados dos sensores IoT em tempo real
- Gráficos de temperatura e umidade
- Previsão do tempo (Open-Meteo API)
- Nível do Rio Negro (ANA API)
- Filtros por período (dia/semana/mês)

### Alertas
- Alertas de inundação (sensores de água e ultrassônico)
- Alertas de seca
- Alertas de chuva (previsão do tempo)
- Alertas de nível do Rio Negro
- Histórico de sinistros resolvidos
- Animações piscantes para alertas críticos

### Perfil de Usuário
- Visualização de perfil do usuário
- Edição de informações pessoais (nome completo, email, telefone)
- Upload de foto de perfil
- Alteração de senha via modal
- Preferências de notificação (email, SMS, push)
- Estatísticas do usuário (fazendas, plantios, sensores)
- Lista de fazendas associadas

### Reportar Queimadas
- Upload de foto da queimada
- Seleção de localização via GPS ou mapa interativo (Leaflet.js)
- Preview da imagem selecionada
- Envio automático para o sistema ANHANGÁ
- Salvamento no banco de dados local
- Lista de reportes recentes

## Integração ANHANGÁ

O TUPA está integrado com o sistema ANHANGÁ para envio automático de reportes de queimadas.

### Configuração

A URL do ANHANGÁ pode ser configurada via variável de ambiente:
```
ANHANGA_URL=http://localhost:5000
```

Se não configurada, o padrão é `http://localhost:5000`.

### Funcionamento

Quando um usuário envia um reporte de queimada no TUPA:

1. O reporte é salvo no banco de dados local (tabela `fire_report`)
2. A imagem é convertida para base64
3. O reporte é enviado automaticamente para ANHANGÁ via POST para `/api/reportes`
4. O payload enviado inclui:
   - `latitude`: Coordenada latitude
   - `longitude`: Coordenada longitude
   - `imagem`: Imagem em base64
   - `fonte`: "tupa"
   - `nivel`: 3 (confirmado)
   - `usuario`: "tupa_{username}" (se usuário autenticado)

### Endpoint ANHANGÁ

O ANHANGÁ deve ter o endpoint `/api/reportes` configurado para receber os reportes externos do TUPA.

## Modelos de Dados

### Principais Entidades

- **User**: Usuário do sistema
- **Farm**: Fazenda do usuário
- **Crop**: Plantação/cultivo
- **Sensor**: Sensor IoT
- **Device**: Dispositivo automatizado
- **WaterTank**: Reservatório de água
- **Alert**: Alerta do sistema
- **Conversation**: Conversa com o chatbot
- **DailySummary**: Resumo diário
- **AlertConfig**: Configuração de alertas
- **FireReport**: Reporte de queimada (integração com ANHANGÁ)

## Documentação Adicional

- [Banco de Dados](./banco_de_dados.md)
- [Regras de Negócio](./regras_de_negocio.md)
- [Requisitos Funcionais (RF)](./rf.md)
- [Requisitos Não-Funcionais (RNF)](./rnf.md)
- [Arquitetura](./arquitetura.md)
- [Especificação Técnica](./especificacao_tecnica.md)

## Suporte

Para suporte e dúvidas, entre em contato com a equipe de desenvolvimento.

## Licença

Este projeto é propriedade da TUPA - Sistema de Gestão Agrícola.
