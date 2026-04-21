# TUPA - Sistema de Gestão Agrícola Inteligente

![TUPA Logo](https://img.shields.io/badge/TUPA-Agricultura%20Inteligente-brightgreen)
![Flask](https://img.shields.io/badge/Flask-3.1.3-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-Private-red)

## Visão Geral

O **TUPA** é um sistema de gestão agrícola inteligente desenvolvido para monitorar e gerenciar plantações, fazendas, sensores IoT e dispositivos automatizados. O sistema integra dados de clima em tempo real, nível de rios e inteligência artificial para fornecer insights especializados sobre culturas agrícolas.

## Características Principais

### Monitoramento em Tempo Real
- Acompanhamento de sensores IoT (umidade do solo, temperatura, nível de água)
- Dashboard interativo com métricas em tempo real
- Gráficos de tendências e histórico de dados

### Gestão de Plantios
- Cadastro e acompanhamento de plantações com previsão de colheita
- Cronômetro regressivo para colheita
- Controle de irrigação e LEDs UV
- Chatbot especialista por cultura

### Sistema de Alertas
- Alertas inteligentes para condições críticas (inundação, seca, chuvas)
- Notificações por email, SMS e push
- Histórico de sinistros resolvidos

### Integrações
- **Open-Meteo API**: Previsão do tempo em tempo real
- **ANA/HIDROWEB**: Nível do Rio Negro
- **Groq API**: Chatbot especializado com IA
- **ANHANGÁ**: Sistema de monitoramento de queimadas

### Reporte de Queimadas
- Upload de fotos com localização GPS
- Mapa interativo para seleção de pontos
- Envio automático para sistema ANHANGÁ

## Stack Tecnológico

### Backend
- **Framework**: Flask 3.1.3
- **Banco de Dados**: SQLite com SQLAlchemy 2.0.49
- **ORM**: Flask-SQLAlchemy
- **Autenticação**: Flask-Login
- **Migrações**: Flask-Migrate com Alembic
- **Formulários**: Flask-WTF
- **API Client**: Requests 2.32.3

### Frontend
- **Template Engine**: Jinja2
- **CSS**: TailwindCSS (customizado)
- **Ícones**: Font Awesome 6.5.1
- **JavaScript**: Vanilla JS (ES6+)
- **Mapas**: Leaflet.js

### APIs Externas
- **Groq**: `meta-llama/llama-4-scout-17b-16e-instruct`
- **Open-Meteo**: Dados meteorológicos
- **HIDROWEB/ANA**: Nível de rios
- **NewsAPI**: Notícias agrícolas (opcional)

## Estrutura do Projeto

```
tupa/
|
app/
|   __init__.py              # Inicialização do aplicativo Flask
|   models.py                # Modelos do banco de dados (SQLAlchemy)
|   routes.py                # Rotas e lógica do backend (1563 linhas)
|   forms.py                 # Formulários WTForms (18573 bytes)
|   utils.py                 # Utilitários e funções auxiliares
|   templates/               # Templates Jinja2
|   |   base.html           # Template base com navegação
|   |   dashboard.html      # Dashboard principal
|   |   plantios.html       # Lista de plantios
|   |   plantios_detail.html # Detalhes do plantio
|   |   monitor.html        # Monitoramento em tempo real
|   |   alerts.html         # Sistema de alertas
|   |   reportar_queimada.html # Reporte de queimadas
|   |   profile.html        # Perfil do usuário
|   |   login.html          # Login
|   |   register.html       # Registro
|   |   farms/              # Gestão de fazendas
|   |   crops/              # Gestão de culturas
|   |   consultations/      # Consultas técnicas
|   static/                 # Arquivos estáticos
|   |   css/style.css       # Estilos customizados
|   |   js/main.js          # JavaScript principal
|   |   uploads/            # Uploads de imagens
|
doc/                        # Documentação completa
|   README.md               # Documentação detalhada
|   especificacao_tecnica.md # Especificação técnica
|   banco_de_dados.md       # Schema do banco
|   regras_de_negocio.md    # Regras de negócio
|   rf.md                   # Requisitos funcionais
|   rnf.md                  # Requisitos não-funcionais
|   arquitetura.md          # Arquitetura do sistema
|
config.py                   # Configurações do sistema
run.py                      # Script de execução
init_db.py                  # Inicialização do banco
requirements.txt            # Dependências Python
.env                        # Variáveis de ambiente
.gitignore                  # Arquivos ignorados pelo Git
```

## Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git

### Passos de Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/augdev1/tupa.git
cd tupa
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

5. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

6. **Execute as migrações do banco de dados:**
```bash
flask db upgrade
```

7. **Execute o aplicativo:**
```bash
python run.py
```

8. **Acesse o sistema em:**
```
http://localhost:5001
```

## Configuração

### Variáveis de Ambiente

Configure as seguintes variáveis no arquivo `.env`:

```bash
# Configurações básicas
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///agricultura.db
FLASK_ENV=development

# APIs externas
GROQ_API_KEY=sua-chave-api-groq-aqui
NEWS_API_KEY=sua-chave-api-news-aqui  # Opcional
ANHANGA_URL=http://localhost:5000     # Integração ANHANGÁ
```

### Chaves de API Necessárias

1. **Groq API**: Para o chatbot especializado em culturas
   - Obtenha em: https://console.groq.com/
   - Modelo: `meta-llama/llama-4-scout-17b-16e-instruct`

2. **NewsAPI**: Para notícias de agricultura (opcional)
   - Obtenha em: https://newsapi.org/

## Funcionalidades Detalhadas

### Dashboard Principal
- Visão geral dos plantios ativos
- Mini cards com progresso dos plantios
- Notícias de agricultura em tempo real
- Métricas e estatísticas

### Gestão de Plantios
- **Cadastro**: Novos plantios com data, cultura, área
- **Acompanhamento**: Progresso automático com base nas datas
- **Irrigação**: Controle remoto de bombas de água
- **Iluminação**: Controle de LEDs UV para cultivo
- **Chatbot**: Assistente especialista por cultura

### Monitoramento IoT
- **Sensores**: Umidade do solo, temperatura, nível de água
- **Gráficos**: Visualização em tempo real e histórico
- **Alertas**: Notificações automáticas para condições críticas
- **Filtros**: Por período (dia/semana/mês)

### Sistema de Alertas
- **Tipos**: Inundação, seca, chuva, nível do rio
- **Severidades**: Crítico (vermelho), Aviso (amarelo), Info (azul)
- **Notificações**: Email, SMS, push
- **Histórico**: Registro de todos os sinistros

### Reporte de Queimadas
- **Upload**: Fotos com preview
- **Localização**: GPS ou mapa interativo (Leaflet.js)
- **Integração**: Envio automático para ANHANGÁ
- **Histórico**: Lista de reportes recentes

### Gestão de Perfil
- **Dados pessoais**: Nome, email, telefone
- **Foto de perfil**: Upload e crop
- **Senha**: Alteração segura via modal
- **Preferências**: Configuração de notificações
- **Estatísticas**: Fazendas, plantios, sensores

## Modelos de Dados

### Principais Entidades

- **User**: Usuários do sistema (agricultores, técnicos, admin)
- **Farm**: Fazendas cadastradas
- **Crop**: Plantações e cultivos
- **Sensor**: Sensores IoT (umidade, temperatura, nível)
- **Device**: Dispositivos automatizados (bombas, LEDs)
- **WaterTank**: Reservatórios de água
- **Alert**: Sistema de alertas e notificações
- **Conversation**: Conversas com o chatbot
- **FireReport**: Reportes de queimadas

### Relacionamentos

- User 1:N Farm (usuários possuem fazendas)
- Farm 1:N Crop (fazendas possuem plantios)
- Farm 1:N Sensor (fazendas possuem sensores)
- Crop 1:N Device (plantios possuem dispositivos)

## APIs e Integrações

### Open-Meteo (Clima)
```python
# Endpoint: https://api.open-meteo.com/v1/forecast
# Parâmetros: latitude, longitude, current, daily
# Resposta: temperatura, umidade, previsão
```

### HIDROWEB/ANA (Nível do Rio)
```python
# Endpoint: https://snirh.snirh.gov.br/snirh/api/v1/telemetria/estacoes
# Estação: 14020000 (Rio Negro - Manaus)
# Resposta: nível do rio em metros
```

### Groq API (Chatbot)
```python
# Endpoint: https://api.groq.com/openai/v1/chat/completions
# Modelo: meta-llama/llama-4-scout-17b-16e-instruct
# Contextos: Café, Milho, Soja, Arroz, Trigo, Cana
```

### ANHANGÁ (Queimadas)
```python
# Endpoint: POST /api/reportes
# Payload: latitude, longitude, imagem (base64), fonte, nivel
# Integração automática de reportes
```

## Segurança

### Autenticação
- Senhas hash com bcrypt
- Sessão expira após 30 minutos
- Proteção CSRF com Flask-WTF
- Validação de email e username únicos

### Autorização
- Decorador `@login_required` em rotas sensíveis
- Validação de propriedade de dados
- Filtros por usuário em consultas

### Proteção de Dados
- Variáveis de ambiente para chaves de API
- Chaves não expostas no frontend
- Prevenção de SQL Injection (SQLAlchemy)
- Prevenção de XSS (escaping Jinja2)

## Desenvolvimento

### Estrutura MVC
- **Model**: `app/models.py` - Entidades e lógica de negócio
- **View**: `app/templates/` - Templates Jinja2
- **Controller**: `app/routes.py` - Rotas e controle

### Padrões
- PEP 8 compliance
- Docstrings em funções
- Comentários em lógica complexa
- Código modular e reutilizável

### Logs
- Configuração de logging estruturado
- Logs de erros e requisições lentas
- Monitoramento de performance

## Deploy

### Ambiente de Desenvolvimento
- Python 3.8+
- SQLite local
- Flask development server
- Debug mode ativado

### Ambiente de Produção (Planejado)
- PostgreSQL
- Gunicorn ou uWSGI
- Nginx como proxy reverso
- SSL/HTTPS
- Docker containers

## Documentação

A documentação completa está disponível na pasta `doc/`:

- [README Detalhado](./doc/README.md)
- [Especificação Técnica](./doc/especificacao_tecnica.md)
- [Banco de Dados](./doc/banco_de_dados.md)
- [Regras de Negócio](./doc/regras_de_negocio.md)
- [Requisitos Funcionais](./doc/rf.md)
- [Requisitos Não-Funcionais](./doc/rnf.md)
- [Arquitetura](./doc/arquitetura.md)

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto é propriedade da TUPA - Sistema de Gestão Agrícola.

## Suporte

Para suporte e dúvidas, entre em contato com a equipe de desenvolvimento.

---

**TUPA** - Transformando a agricultura com tecnologia e inteligência artificial.
