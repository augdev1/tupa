# Banco de Dados - TUPA

## Visão Geral

O sistema TUPA utiliza SQLite como banco de dados principal, com SQLAlchemy como ORM. O banco de dados é gerenciado através de Flask-SQLAlchemy e as migrações são controladas pelo Flask-Migrate com Alembic.

## Estrutura do Banco de Dados

### Tabelas

#### 1. users

Armazena informações dos usuários do sistema.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| id | Integer | Chave primária (auto-incremento) |
| username | String(80) | Nome de usuário único |
| email | String(120) | Email do usuário |
| password_hash | String(128) | Hash da senha |
| created_at | DateTime | Data de criação da conta |

**Índices:**
- username (único)
- email (único)

#### 2. farms

Armazena informações das fazendas dos usuários.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| id | Integer | Chave primária (auto-incremento) |
| name | String(100) | Nome da fazenda |
| location | String(200) | Localização da fazenda |
| user_id | Integer | Chave estrangeira para users |
| created_at | DateTime | Data de criação |

**Relacionamentos:**
- user_id → users.id (Many-to-One)
- sensors (One-to-Many)
- crops (One-to-Many)
- devices (One-to-Many)
- water_tanks (One-to-Many)
- alerts (One-to-Many)

#### 3. crops

Armazena informações sobre as plantações/cultivos.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| id | Integer | Chave primária (auto-incremento) |
| name | String(100) | Nome do plantio |
| crop_type | String(50) | Tipo de cultura (café, milho, soja, arroz, etc.) |
| planting_date | Date | Data de plantio |
| estimated_harvest_date | Date | Data estimada de colheita |
| area_hectares | Float | Área em hectares |
| expected_yield | Float | Produção esperada em kg |
| irrigation_count | Integer | Número de irrigações realizadas |
| last_irrigation_date | DateTime | Data da última irrigação |
| needs_irrigation | Boolean | Precisa de irrigação (True/False) |
| led_status | Boolean | Status do LED UV (True/False) |
| pump_status | Boolean | Status da bomba (True/False) |
| farm_id | Integer | Chave estrangeira para farms |
| created_at | DateTime | Data de criação |

**Relacionamentos:**
- farm_id → farms.id (Many-to-One)
- sensors (One-to-Many)
- conversations (One-to-Many)
- alerts (One-to-Many)

**Métodos:**
- `get_progress()`: Calcula o progresso do plantio em porcentagem

#### 4. sensors

Armazena informações dos sensores IoT.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| id | Integer | Chave primária (auto-incremento) |
| name | String(100) | Nome do sensor |
| sensor_type | String(50) | Tipo de sensor (umidade_solo, temperatura, nivel_agua, ultrassonico) |
| location | String(100) | Localização do sensor |
| is_active | Boolean | Status do sensor (ativo/inativo) |
| farm_id | Integer | Chave estrangeira para farms |
| created_at | DateTime | Data de criação |

**Relacionamentos:**
- farm_id → farms.id (Many-to-One)
- readings (One-to-Many)

**Métodos:**
- `get_latest_reading()`: Retorna a leitura mais recente do sensor

#### 5. sensor_readings

Armazena as leituras dos sensores IoT.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| id | Integer | Chave primária (auto-incremento) |
| sensor_id | Integer | Chave estrangeira para sensors |
| value | Float | Valor da leitura |
| unit | String(20) | Unidade de medida (%, °C, m, etc.) |
| timestamp | DateTime | Data e hora da leitura |

**Relacionamentos:**
- sensor_id → sensors.id (Many-to-One)

#### 6. devices

Armazena informações dos dispositivos automatizados.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| id | Integer | Chave primária (auto-incremento) |
| name | String(100) | Nome do dispositivo |
| device_type | String(50) | Tipo de dispositivo (bomba, led_uv, ventilador) |
| is_active | Boolean | Status do dispositivo (ativo/inativo) |
| farm_id | Integer | Chave estrangeira para farms |
| created_at | DateTime | Data de criação |

**Relacionamentos:**
- farm_id → farms.id (Many-to-One)

#### 7. water_tanks

Armazena informações dos reservatórios de água.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| id | Integer | Chave primária (auto-incremento) |
| name | String(100) | Nome do reservatório |
| capacity_liters | Float | Capacidade em litros |
| current_level_liters | Float | Nível atual em litros |
| farm_id | Integer | Chave estrangeira para farms |
| created_at | DateTime | Data de criação |

**Relacionamentos:**
- farm_id → farms.id (Many-to-One)

**Métodos:**
- `get_current_level()`: Retorna o nível atual em porcentagem

#### 8. alerts

Armazena os alertas do sistema.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| id | Integer | Chave primária (auto-incremento) |
| alert_type | String(50) | Tipo de alerta (inundacao, seca, chuva, nivel_rio) |
| severity | String(20) | Severidade (critical, warning, info) |
| message | Text | Mensagem do alerta |
| is_resolved | Boolean | Status de resolução (True/False) |
| resolved_at | DateTime | Data de resolução |
| action_taken | Text | Ação tomada para resolver |
| farm_id | Integer | Chave estrangeira para farms |
| crop_id | Integer | Chave estrangeira para crops (opcional) |
| created_at | DateTime | Data de criação |

**Relacionamentos:**
- farm_id → farms.id (Many-to-One)
- crop_id → crops.id (Many-to-One, opcional)

#### 9. conversations

Armazena as conversas com o chatbot.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| id | Integer | Chave primária (auto-incremento) |
| role | String(20) | Papel (user, assistant) |
| message | Text | Conteúdo da mensagem |
| crop_id | Integer | Chave estrangeira para crops |
| timestamp | DateTime | Data e hora da mensagem |

**Relacionamentos:**
- crop_id → crops.id (Many-to-One)

#### 10. daily_summaries

Armazena resumos diários das atividades.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| id | Integer | Chave primária (auto-incremento) |
| date | Date | Data do resumo |
| summary_text | Text | Conteúdo do resumo |
| farm_id | Integer | Chave estrangeira para farms |
| created_at | DateTime | Data de criação |

**Relacionamentos:**
- farm_id → farms.id (Many-to-One)

#### 11. alert_configs

Armazena configurações de alertas por usuário.

| Coluna | Tipo | Descrição |
|--------|------|------------|
| id | Integer | Chave primária (auto-incremento) |
| user_id | Integer | Chave estrangeira para users |
| min_soil_moisture | Float | Umidade mínima do solo para alerta |
| max_soil_moisture | Float | Umidade máxima do solo para alerta |
| min_water_level | Float | Nível mínimo de água para alerta |
| max_water_level | Float | Nível máximo de água para alerta |
| created_at | DateTime | Data de criação |
| updated_at | DateTime | Data de atualização |

**Relacionamentos:**
- user_id → users.id (Many-to-One)

## Diagrama de Relacionamento (ER)

```
users (1) ----< (N) farms
        |
        +----< (N) alert_configs

farms (1) ----< (N) crops
       |
       +----< (N) sensors
       |
       +----< (N) devices
       |
       +----< (N) water_tanks
       |
       +----< (N) alerts

crops (1) ----< (N) conversations
       |
       +----< (N) alerts (opcional)

sensors (1) ----< (N) sensor_readings
```

## Migrações

As migrações são gerenciadas pelo Flask-Migrate com Alembic. Para criar uma nova migração:

```bash
flask db migrate -m "descrição da migração"
```

Para aplicar as migrações:

```bash
flask db upgrade
```

## Backup e Restauração

### Backup

```bash
# Copiar o arquivo do banco de dados
cp agriculture.db agriculture_backup_$(date +%Y%m%d).db
```

### Restauração

```bash
# Restaurar de um backup
cp agriculture_backup_YYYYMMDD.db agriculture.db
```

## Otimizações

### Índices

Índices foram criados para melhorar a performance:
- `users.username` (único)
- `users.email` (único)
- `alerts.is_resolved`
- `alerts.created_at`
- `sensor_readings.timestamp`
- `conversations.crop_id`

### Consultas Frequentes

As consultas mais frequentes do sistema são:
- Busca de plantios ativos por usuário
- Leituras recentes de sensores
- Alertas não resolvidos
- Conversas por plantio

## Segurança

- Senhas são armazenadas como hash usando bcrypt
- Todas as consultas filtram por usuário atual
- Relacionamentos validam propriedade dos dados
- SQL Injection prevenido pelo SQLAlchemy
