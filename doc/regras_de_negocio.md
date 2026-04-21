# Regras de Negócio - TUPA

## Visão Geral

Este documento define as regras de negócio do sistema TUPA, especificando as lógicas e comportamentos que o sistema deve seguir para garantir a integridade e consistência dos dados.

## Regras de Negócio por Módulo

### 1. Autenticação e Usuários

#### RN-001: Registro de Usuário
- Um usuário deve ter um username único
- Um usuário deve ter um email único
- A senha deve ter no mínimo 8 caracteres
- A senha deve ser armazenada como hash (bcrypt)
- O email deve ser validado (formato válido)

#### RN-002: Login
- O usuário deve fornecer username e senha corretos
- Após login bem-sucedido, o usuário é redirecionado para o dashboard
- A sessão expira após 30 minutos de inatividade

#### RN-003: Perfil de Usuário
- O usuário pode alterar apenas seus próprios dados
- A senha atual é obrigatória para alterar a senha
- O email não pode ser alterado para um email já existente

### 2. Gestão de Fazendas

#### RN-004: Criação de Fazenda
- Cada usuário pode ter múltiplas fazendas
- O nome da fazenda deve ser único para o usuário
- A localização é obrigatória
- A fazenda deve estar associada a um usuário

#### RN-005: Exclusão de Fazenda
- A fazenda só pode ser excluída se não tiver plantios ativos
- A exclusão deve solicitar confirmação do usuário
- Todos os sensores e dispositivos associados são excluídos em cascata

### 3. Gestão de Plantios

#### RN-006: Criação de Plantio
- Um plantio deve estar associado a uma fazenda do usuário
- A data de plantio deve ser anterior à data de colheita estimada
- O tipo de cultura deve ser válido (café, milho, soja, arroz, etc.)
- A área em hectares deve ser maior que zero
- A produção esperada deve ser maior que zero

#### RN-007: Cálculo de Progresso
- O progresso é calculado baseado na data de plantio e data estimada de colheita
- Progresso = (data atual - data de plantio) / (data colheita - data de plantio) * 100
- O progresso máximo é 100%
- O progresso mínimo é 0%

#### RN-008: Cronômetro de Colheita
- O cronômetro mostra o tempo restante até a colheita
- Se a data de colheita já passou, mostra "Colheita pronta"
- O cronômetro é atualizado em tempo real (a cada segundo)

#### RN-009: Irrigação
- A irrigação só pode ser ativada para plantios do usuário
- Cada irrigação incrementa o contador de irrigações
- A data da última irrigação é atualizada
- O status "needs_irrigation" é definido como False após irrigação

#### RN-010: LED UV
- O LED UV só pode ser ativado para plantios do usuário
- O status "led_status" é atualizado imediatamente
- O LED pode ser ligado/desligado a qualquer momento

#### RN-011: Exclusão de Plantio
- O plantio só pode ser excluído se não tiver alertas ativos
- A exclusão deve solicitar confirmação do usuário
- Todas as conversas associadas são excluídas em cascata

### 4. Sensores IoT

#### RN-012: Criação de Sensor
- Um sensor deve estar associado a uma fazenda do usuário
- O tipo de sensor deve ser válido (umidade_solo, temperatura, nivel_agua, ultrassonico)
- O nome do sensor deve ser único na fazenda
- A localização é obrigatória

#### RN-013: Leituras de Sensores
- As leituras são armazenadas com timestamp
- O valor da leitura deve ser numérico
- A unidade de medida deve ser válida para o tipo de sensor
- Leituras antigas podem ser arquivadas após 90 dias

#### RN-014: Alertas Automáticos
- Se umidade do solo < 20%, gerar alerta de seca
- Se nível de água > 80%, gerar alerta de inundação
- Se nível de água < 20%, gerar alerta de nível baixo
- Se ultrassônico detectar água, gerar alerta de inundação

### 5. Dispositivos

#### RN-015: Criação de Dispositivo
- Um dispositivo deve estar associado a uma fazenda do usuário
- O tipo de dispositivo deve ser válido (bomba, led_uv, ventilador)
- O nome do dispositivo deve ser único na fazenda

#### RN-016: Controle de Dispositivos
- Dispositivos só podem ser controlados pelo proprietário
- O status é atualizado imediatamente
- A ação é registrada no log

### 6. Reservatórios de Água

#### RN-017: Criação de Reservatório
- Um reservatório deve estar associado a uma fazenda do usuário
- A capacidade deve ser maior que zero
- O nível inicial não pode exceder a capacidade

#### RN-018: Cálculo de Nível
- Nível atual = (nível atual / capacidade) * 100
- O nível máximo é 100%
- O nível mínimo é 0%
- Se nível < 30%, gerar alerta de nível baixo

### 7. Alertas

#### RN-019: Criação de Alerta
- Um alerta deve estar associado a uma fazenda do usuário
- A severidade deve ser válida (critical, warning, info)
- A mensagem é obrigatória
- Alertas críticos têm prioridade máxima

#### RN-020: Resolução de Alerta
- Apenas alertas não resolvidos podem ser resolvidos
- A ação tomada é obrigatória
- A data de resolução é registrada
- Alertas resolvidos são movidos para o histórico

#### RN-021: Alertas Piscantes
- Alertas críticos (inundação) piscam em vermelho
- Alertas de aviso (seca, nível baixo) piscam em amarelo
- Alertas de chuva piscam em azul
- A animação para quando o alerta é resolvido

### 8. Chatbot

#### RN-022: Especialização por Cultura
- O chatbot usa um contexto especializado para cada tipo de cultura
- Contextos disponíveis: café, milho, soja, arroz, trigo, cana
- O contexto inclui expertise agronômica específica
- O modelo AI é meta-llama/llama-4-scout-17b-16e-instruct

#### RN-023: Histórico de Conversa
- Cada plantio tem seu próprio histórico de conversa
- As conversas são armazenadas com timestamp
- O usuário e assistente têm papéis distintos
- O histórico é mantido para contexto futuro

#### RN-024: Limitações do Chatbot
- O chatbot não pode executar ações no sistema
- O chatbot fornece apenas informações e recomendações
- As mensagens são limitadas a 1000 caracteres
- O modelo tem limite de tokens (1024)

### 9. Monitoramento

#### RN-025: Dados em Tempo Real
- Os dados dos sensores são atualizados em tempo real
- O dashboard atualiza automaticamente a cada 30 segundos
- Leituras antigas são arquivadas após 90 dias

#### RN-026: Previsão do Tempo
- Os dados de clima são buscados da API Open-Meteo
- A localização é fixa em Manaus, Amazonas
- A previsão é para 7 dias
- Os dados são atualizados a cada hora

#### RN-027: Nível do Rio Negro
- O nível do rio é buscado da API HIDROWEB (ANA)
- A estação é 14020000 (Manaus)
- O nível médio anual é 18.0m
- Nível > 25m = risco de inundação
- Nível < 12m = seca

### 10. Dashboard

#### RN-028: Mini Cards
- Cada plantio ativo tem um mini card
- O mini card mostra: nome, cultura, progresso, status
- O progresso é atualizado em tempo real
- Clicar no card leva aos detalhes do plantio

#### RN-029: Notícias
- As notícias são buscadas da NewsAPI
- As notícias são filtradas por agricultura
- As notícias são atualizadas diariamente
- Máximo de 5 notícias no dashboard

### 11. Configuração de Alertas

#### RN-030: Configuração Personalizada
- Cada usuário pode configurar seus próprios limites
- Os limites são: umidade mínima/máxima do solo, nível mínimo/máximo de água
- A configuração é opcional
- Valores padrão são usados se não configurado

### 12. APIs Externas

#### RN-031: Open-Meteo API
- API gratuita, sem necessidade de chave
- Coordenadas: Manaus (-3.1190, -60.0217)
- Parâmetros: temperatura, umidade, código do clima, vento, pressão
- Previsão diária: 7 dias
- Timeout: 10 segundos

#### RN-032: HIDROWEB API (ANA)
- API da Agência Nacional de Águas
- Estação: 14020000 (Rio Negro em Manaus)
- Dados: nível do rio em metros
- Timeout: 10 segundos
- Fallback para valores médios se falhar

#### RN-033: Groq API
- API para chatbot especializado
- Modelo: meta-llama/llama-4-scout-17b-16e-instruct
- Temperatura: 1
- Max tokens: 1024
- Chave de API obrigatória

### 13. Validações de Dados

#### RN-034: Validação de Datas
- Todas as datas devem estar no formato YYYY-MM-DD
- A data de plantio deve ser anterior à data de colheita
- A data de colheita deve ser futura ou igual à data atual

#### RN-035: Validação de Números
- Área deve ser > 0
- Produção esperada deve ser > 0
- Capacidade do reservatório deve ser > 0
- Nível atual não pode exceder a capacidade

#### RN-036: Validação de Strings
- Username: 3-80 caracteres, alfanumérico
- Email: formato válido de email
- Nome: 2-100 caracteres
- Tipo de cultura: valores pré-definidos

### 14. Segurança

#### RN-037: Controle de Acesso
- Usuários só podem acessar seus próprios dados
- Rotas sensíveis exigem login
- Rotas de API validam permissões

#### RN-038: Auditoria
- Todas as ações críticas são registradas
- Logs incluem: usuário, ação, timestamp, dados
- Logs são mantidos por 180 dias

## Regras de Integridade

### RI-001: Integridade Referencial
- Chaves estrangeiras devem apontar para registros válidos
- Exclusão em cascata para relacionamentos dependentes
- Não é possível excluir um usuário com dados ativos

### RI-002: Consistência de Dados
- O progresso do plantio é calculado, não armazenado
- O nível do reservatório é calculado, não armazenado
- Leituras de sensores são imutáveis

### RI-003: Unicidade
- Username é único por sistema
- Email é único por sistema
- Nome de fazenda é único por usuário
- Nome de sensor é único por fazenda
