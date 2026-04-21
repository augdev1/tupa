# Requisitos Funcionais (RF) - TUPA

## Visão Geral

Este documento define os requisitos funcionais do sistema TUPA, especificando as funcionalidades que o sistema deve fornecer aos usuários.

## RF-001: Autenticação de Usuários

### RF-001.1: Registro
O sistema deve permitir que novos usuários se cadastrem fornecendo:
- Nome de usuário único
- Email válido
- Senha (mínimo 8 caracteres)

### RF-001.2: Login
O sistema deve permitir que usuários autenticados façam login usando:
- Nome de usuário ou email
- Senha

### RF-001.3: Logout
O sistema deve permitir que usuários autenticados façam logout da sessão.

### RF-001.4: Recuperação de Senha
O sistema deve permitir que usuários recuperem suas senhas através do email cadastrado.

### RF-001.5: Alteração de Senha
O sistema deve permitir que usuários autenticados alterem suas senhas fornecendo:
- Senha atual
- Nova senha
- Confirmação da nova senha

## RF-002: Gestão de Perfil

### RF-002.1: Visualizar Perfil
O sistema deve permitir que usuários visualizem suas informações de perfil:
- Avatar/foto de perfil
- Nome de usuário
- Email
- CPF (se cadastrado)
- Data de cadastro
- Estatísticas (fazendas, plantios, sensores)
- Lista de fazendas associadas

### RF-002.2: Editar Perfil
O sistema deve permitir que usuários editem suas informações de perfil:
- Nome completo
- Email
- Telefone (opcional)
- Foto de perfil (upload)
- Preferências de notificação (email, SMS, push)

### RF-002.3: Upload de Foto de Perfil
O sistema deve permitir que usuários façam upload de foto de perfil:
- Formatos aceitos: PNG, JPG, JPEG
- Tamanho máximo: 5MB
- Preview em tempo real
- Armazenamento em pasta estática
- Nome único do arquivo (user_id + timestamp)

### RF-002.4: Alterar Senha
O sistema deve permitir que usuários alterem suas senhas através de modal:
- Validação de senha atual
- Nova senha com mínimo 8 caracteres
- Confirmação de nova senha
- Validação de igualdade das senhas
- Feedback visual de sucesso/erro

### RF-002.5: Excluir Conta
O sistema deve permitir que usuários excluam suas contas após confirmação.

## RF-003: Gestão de Fazendas

### RF-003.1: Criar Fazenda
O sistema deve permitir que usuários criem novas fazendas fornecendo:
- Nome da fazenda
- Localização
- Descrição (opcional)

### RF-003.2: Listar Fazendas
O sistema deve permitir que usuários visualizem todas as suas fazendas.

### RF-003.3: Editar Fazenda
O sistema deve permitir que usuários editem informações de suas fazendas.

### RF-003.4: Excluir Fazenda
O sistema deve permitir que usuários excluam suas fazendas após confirmação.

### RF-003.5: Visualizar Detalhes da Fazenda
O sistema deve permitir que usuários visualizem detalhes completos de uma fazenda:
- Informações gerais
- Plantios associados
- Sensores associados
- Dispositivos associados
- Reservatórios associados

## RF-004: Gestão de Plantios

### RF-004.1: Criar Plantio
O sistema deve permitir que usuários criem novos plantios fornecendo:
- Nome do plantio
- Tipo de cultura (café, milho, soja, arroz, etc.)
- Data de plantio
- Data estimada de colheita
- Área em hectares
- Produção esperada em kg

### RF-004.2: Listar Plantios
O sistema deve permitir que usuários visualizem todos os seus plantios:
- Nome
- Cultura
- Progresso
- Status
- Data estimada de colheita

### RF-004.3: Visualizar Detalhes do Plantio
O sistema deve permitir que usuários visualizem detalhes completos de um plantio:
- Informações gerais
- Progresso atual
- Cronômetro para colheita
- Sensores associados
- Histórico de irrigações
- Controle de dispositivos

### RF-004.4: Editar Plantio
O sistema deve permitir que usuários editem informações de seus plantios.

### RF-004.5: Excluir Plantio
O sistema deve permitir que usuários excluam seus plantios após confirmação.

### RF-004.6: Cronômetro de Colheita
O sistema deve exibir um cronômetro regressivo mostrando o tempo restante até a colheita:
- Dias, horas, minutos, segundos
- Atualização em tempo real (a cada segundo)
- Indicação de colheita pronta se a data já passou

### RF-004.7: Controle de Irrigação
O sistema deve permitir que usuários controlem a irrigação de um plantio:
- Ativar bomba de irrigação
- Desativar bomba de irrigação
- Visualizar status atual da bomba
- Visualizar contador de irrigações realizadas
- Visualizar data da última irrigação

### RF-004.8: Controle de LED UV
O sistema deve permitir que usuários controlem o LED UV de um plantio:
- Ativar LED UV
- Desativar LED UV
- Visualizar status atual do LED

## RF-005: Gestão de Sensores IoT

### RF-005.1: Criar Sensor
O sistema deve permitir que usuários cadastrem novos sensores fornecendo:
- Nome do sensor
- Tipo de sensor (umidade_solo, temperatura, nivel_agua, ultrassonico)
- Localização
- Descrição (opcional)

### RF-005.2: Listar Sensores
O sistema deve permitir que usuários visualizem todos os seus sensores:
- Nome
- Tipo
- Status
- Leitura mais recente
- Localização

### RF-005.3: Visualizar Detalhes do Sensor
O sistema deve permitir que usuários visualizem detalhes completos de um sensor:
- Informações gerais
- Leitura mais recente
- Histórico de leituras (últimas 24 horas)
- Gráfico de tendências

### RF-005.4: Editar Sensor
O sistema deve permitir que usuários editem informações de seus sensores.

### RF-005.5: Excluir Sensor
O sistema deve permitir que usuários excluam seus sensores após confirmação.

### RF-005.6: Ativar/Desativar Sensor
O sistema deve permitir que usuários ativem ou desativem seus sensores.

### RF-005.7: Leituras em Tempo Real
O sistema deve exibir leituras dos sensores em tempo real:
- Valor atual
- Unidade de medida
- Timestamp da leitura
- Atualização automática

## RF-006: Gestão de Dispositivos

### RF-006.1: Criar Dispositivo
O sistema deve permitir que usuários cadastrem novos dispositivos fornecendo:
- Nome do dispositivo
- Tipo de dispositivo (bomba, led_uv, ventilador)
- Localização
- Descrição (opcional)

### RF-006.2: Listar Dispositivos
O sistema deve permitir que usuários visualizem todos os seus dispositivos:
- Nome
- Tipo
- Status
- Localização

### RF-006.3: Editar Dispositivo
O sistema deve permitir que usuários editem informações de seus dispositivos.

### RF-006.4: Excluir Dispositivo
O sistema deve permitir que usuários excluam seus dispositivos após confirmação.

### RF-006.5: Controlar Dispositivo
O sistema deve permitir que usuários controlem seus dispositivos:
- Ligar dispositivo
- Desligar dispositivo
- Visualizar status atual

## RF-007: Gestão de Reservatórios

### RF-007.1: Criar Reservatório
O sistema deve permitir que usuários cadastrem novos reservatórios fornecendo:
- Nome do reservatório
- Capacidade em litros
- Nível inicial em litros
- Localização

### RF-007.2: Listar Reservatórios
O sistema deve permitir que usuários visualizem todos os seus reservatórios:
- Nome
- Capacidade
- Nível atual (litros e porcentagem)
- Localização

### RF-007.3: Editar Reservatório
O sistema deve permitir que usuários editem informações de seus reservatórios.

### RF-007.4: Excluir Reservatório
O sistema deve permitir que usuários excluam seus reservatórios após confirmação.

### RF-007.5: Atualizar Nível
O sistema deve permitir que usuários atualizem o nível atual dos reservatórios.

## RF-008: Sistema de Alertas

### RF-008.1: Listar Alertas Ativos
O sistema deve permitir que usuários visualizem todos os seus alertas ativos:
- Tipo de alerta
- Severidade
- Mensagem
- Timestamp
- Fazenda/Plantio associado

### RF-008.2: Listar Histórico de Alertas
O sistema deve permitir que usuários visualizem o histórico de alertas resolvidos:
- Tipo de alerta
- Severidade
- Mensagem
- Data de resolução
- Ação tomada

### RF-008.3: Resolver Alerta
O sistema deve permitir que usuários marquem alertas como resolvidos:
- Informar ação tomada
- Registrar data de resolução
- Mover para histórico

### RF-008.4: Alertas Automáticos
O sistema deve gerar alertas automaticamente baseado em:
- Umidade do solo abaixo do limite (seca)
- Nível de água acima do limite (inundação)
- Nível de água abaixo do limite (nível baixo)
- Sensor ultrassônico detectando água (inundação)
- Previsão de chuva (próximos 3 dias)
- Nível do Rio Negro acima de 25m (inundação)
- Nível do Rio Negro abaixo de 12m (seca)

### RF-008.5: Alertas Piscantes
O sistema deve exibir alertas críticos com animação piscante:
- Alertas de inundação: vermelho
- Alertas de seca: amarelo
- Alertas de chuva: azul

### RF-008.6: Configurar Limites de Alerta
O sistema deve permitir que usuários configurem limites personalizados para alertas:
- Umidade mínima do solo
- Umidade máxima do solo
- Nível mínimo de água
- Nível máximo de água

## RF-009: Chatbot Especialista

### RF-009.1: Iniciar Conversa
O sistema deve permitir que usuários iniciem uma conversa com o chatbot especialista em um plantio específico.

### RF-009.2: Enviar Mensagem
O sistema deve permitir que usuários enviem mensagens ao chatbot:
- Texto livre
- Máximo 1000 caracteres

### RF-009.3: Receber Resposta
O sistema deve fornecer respostas do chatbot:
- Contexto especializado na cultura do plantio
- Informações agronômicas relevantes
- Recomendações baseadas no contexto

### RF-009.4: Histórico de Conversa
O sistema deve manter o histórico de conversa:
- Mensagens do usuário
- Respostas do assistente
- Timestamp de cada mensagem

### RF-009.5: Especialização por Cultura
O sistema deve fornecer contexto especializado para cada tipo de cultura:
- Café: manejo, nutrição, pragas, doenças, colheita
- Milho: manejo, nutrição, pragas, doenças, colheita
- Soja: manejo, nutrição, pragas, doenças, colheita
- Arroz: manejo, nutrição, pragas, doenças, colheita
- Trigo: manejo, nutrição, pragas, doenças, colheita
- Cana: manejo, nutrição, pragas, doenças, colheita

## RF-010: Monitoramento em Tempo Real

### RF-010.1: Dashboard de Monitoramento
O sistema deve fornecer um dashboard de monitoramento mostrando:
- Todos os sensores do usuário
- Leitura mais recente de cada sensor
- Status de cada sensor
- Dispositivos e seus status
- Reservatórios e seus níveis

### RF-010.2: Gráficos de Tendências
O sistema deve exibir gráficos de tendências para:
- Umidade do solo
- Temperatura
- Nível de água
- Período selecionável (dia, semana, mês)

### RF-010.3: Atualização Automática
O sistema deve atualizar os dados automaticamente:
- Dashboard: a cada 30 segundos
- Gráficos: a cada 30 segundos
- Leituras de sensores: em tempo real

## RF-011: Previsão do Tempo

### RF-011.1: Clima Atual
O sistema deve exibir o clima atual de Manaus, Amazonas:
- Temperatura atual
- Umidade relativa
- Condição do tempo (nublado, limpo, etc.)
- Vento
- Pressão atmosférica

### RF-011.2: Previsão Semanal
O sistema deve exibir a previsão do tempo para os próximos 7 dias:
- Temperatura máxima
- Temperatura mínima
- Condição do tempo (ícone)
- Dia da semana

### RF-011.3: Previsão de Chuva
O sistema deve alertar sobre previsão de chuva:
- Próximos 3 dias
- Precipitação esperada
- Alerta piscante se chuva prevista

### RF-011.4: Gráfico de Temperatura
O sistema deve exibir um gráfico de temperatura:
- Período selecionável (dia, semana, mês)
- Dados da API Open-Meteo
- Atualização automática

## RF-012: Nível do Rio Negro

### RF-012.1: Nível Atual
O sistema deve exibir o nível atual do Rio Negro em Manaus:
- Valor em metros
- Comparação com média anual (18.0m)

### RF-012.2: Alerta de Inundação
O sistema deve alertar se o nível do rio estiver alto:
- Nível > 25m
- Alerta piscante em vermelho

### RF-012.3: Alerta de Seca
O sistema deve alertar se o nível do rio estiver baixo:
- Nível < 12m
- Alerta piscante em amarelo

### RF-012.4: Média Anual
O sistema deve exibir a média anual do nível do Rio Negro:
- Valor médio histórico
- Comparação com nível atual

## RF-013: Dashboard Principal

### RF-013.1: Visão Geral
O sistema deve fornecer um dashboard principal mostrando:
- Mini cards dos plantios ativos
- Progresso de cada plantio
- Status de cada plantio
- Atalhos rápidos

### RF-013.2: Mini Cards de Plantios
O sistema deve exibir mini cards para cada plantio:
- Nome do plantio
- Tipo de cultura
- Progresso atual
- Status (ativo, pronto, colhido)
- Data estimada de colheita

### RF-013.3: Notícias de Agricultura
O sistema deve exibir notícias de agricultura:
- Até 5 notícias
- Fonte: NewsAPI
- Atualização diária

### RF-013.4: Métricas Resumidas
O sistema deve exibir métricas resumidas:
- Total de plantios
- Plantios ativos
- Plantios prontos para colheita
- Alertas ativos
- Total de fazendas

## RF-014: Navegação

### RF-014.1: Menu de Navegação
O sistema deve fornecer um menu de navegação com acesso a:
- Dashboard
- Plantios
- Monitoramento
- Alertas
- Perfil

### RF-014.2: Barra de Navegação Inferior
O sistema deve fornecer uma barra de navegação inferior para mobile com:
- Início
- Plantios
- Monitoramento
- Alertas
- Perfil

### RF-014.3: Breadcrumbs
O sistema deve fornecer breadcrumbs para navegação hierárquica.

## RF-015: Responsividade

### RF-015.1: Desktop
O sistema deve ser responsivo em telas desktop (≥ 1024px).

### RF-015.2: Tablet
O sistema deve ser responsivo em tablets (768px - 1023px).

### RF-015.3: Mobile
O sistema deve ser responsivo em mobile (< 768px).

## RF-016: Internacionalização

### RF-016.1: Idioma Padrão
O sistema deve suportar português como idioma padrão.

### RF-016.2: Formato de Data
O sistema deve usar formato de data brasileiro (DD/MM/YYYY).

### RF-016.3: Formato de Número
O sistema deve usar formato de número brasileiro (vírgula para decimais).

## RF-017: Exportação de Dados

### RF-017.1: Exportar Plantios
O sistema deve permitir que usuários exportem dados de plantios em formato CSV.

### RF-017.2: Exportar Leituras de Sensores
O sistema deve permitir que usuários exportem leituras de sensores em formato CSV.

### RF-017.3: Exportar Histórico de Alertas
O sistema deve permitir que usuários exportem histórico de alertas em formato CSV.

## RF-018: Relatórios

### RF-018.1: Relatório de Plantios
O sistema deve gerar relatórios de plantios:
- Período selecionável
- Resumo de atividades
- Estatísticas

### RF-018.2: Relatório de Irrigação
O sistema deve gerar relatórios de irrigação:
- Total de irrigações
- Frequência por plantio
- Consumo estimado de água

### RF-018.3: Relatório de Alertas
O sistema deve gerar relatórios de alertas:
- Total de alertas
- Alertas por tipo
- Tempo médio de resolução
