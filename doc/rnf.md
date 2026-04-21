# Requisitos Não-Funcionais (RNF) - TUPA

## Visão Geral

Este documento define os requisitos não-funcionais do sistema TUPA, especificando os atributos de qualidade e restrições técnicas que o sistema deve atender.

## RNF-001: Performance

### RNF-001.1: Tempo de Resposta
- O sistema deve responder a requisições em menos de 2 segundos
- O dashboard deve carregar em menos de 3 segundos
- Gráficos devem renderizar em menos de 1 segundo
- A API de chatbot deve responder em menos de 5 segundos

### RNF-001.2: Throughput
- O sistema deve suportar até 100 usuários simultâneos
- O sistema deve processar até 1000 requisições por minuto
- O sistema deve suportar até 10 leituras de sensores por segundo

### RNF-001.3: Atualização em Tempo Real
- Dados do dashboard devem atualizar a cada 30 segundos
- Leituras de sensores devem atualizar em tempo real
- Alertas devem ser gerados em até 5 segundos após detecção

## RNF-002: Disponibilidade

### RNF-002.1: Uptime
- O sistema deve estar disponível 99.5% do tempo
- Tempo máximo de downtime planejado: 4 horas por mês
- Tempo máximo de downtime não planejado: 1 hora por mês

### RNF-002.2: Recuperação de Falhas
- O sistema deve recuperar de falhas em até 5 minutos
- O sistema deve ter backup diário automático
- O sistema deve ter plano de recuperação de desastres

### RNF-002.3: Redundância
- Banco de dados deve ter backup diário
- Logs devem ser mantidos por 180 dias
- Dados críticos devem ter redundância

## RNF-003: Escalabilidade

### RNF-003.1: Escalabilidade Horizontal
- O sistema deve suportar adição de novos servidores
- O sistema deve suportar balanceamento de carga
- O sistema deve suportar arquitetura de microserviços (futuro)

### RNF-003.2: Escalabilidade Vertical
- O sistema deve suportar aumento de recursos do servidor
- O banco de dados deve suportar crescimento de dados
- O sistema deve suportar aumento de usuários

### RNF-003.3: Crescimento de Dados
- O sistema deve suportar até 1 milhão de leituras de sensores
- O sistema deve suportar até 100.000 plantios
- O sistema deve suportar até 10.000 usuários

## RNF-004: Segurança

### RNF-004.1: Autenticação
- O sistema deve usar autenticação baseada em sessão
- As senhas devem ser armazenadas como hash (bcrypt)
- As sessões devem expirar após 30 minutos de inatividade
- O sistema deve suportar login com email ou username

### RNF-004.2: Autorização
- O sistema deve validar permissões em cada requisição
- Usuários só podem acessar seus próprios dados
- O sistema deve ter controle de acesso baseado em roles (futuro)

### RNF-004.3: Proteção de Dados
- As senhas devem ter no mínimo 8 caracteres
- Os dados sensíveis devem ser criptografados
- As conexões devem usar HTTPS (produção)
- As chaves de API não devem ser expostas no frontend

### RNF-004.4: Prevenção de Ataques
- O sistema deve prevenir SQL Injection (SQLAlchemy)
- O sistema deve prevenir XSS (escaping no Jinja2)
- O sistema deve prevenir CSRF (Flask-WTF)
- O sistema deve validar todos os inputs

### RNF-004.5: Auditoria
- O sistema deve registrar todas as ações críticas
- Os logs devem incluir: usuário, ação, timestamp, dados
- Os logs devem ser mantidos por 180 dias
- O sistema deve ter logs de acesso

## RNF-005: Usabilidade

### RNF-005.1: Interface do Usuário
- A interface deve ser intuitiva e fácil de usar
- A interface deve seguir padrões de design consistentes
- A interface deve ter feedback visual para todas as ações
- A interface deve ter mensagens de erro claras

### RNF-005.2: Acessibilidade
- O sistema deve seguir diretrizes WCAG 2.1 AA
- O sistema deve suportar navegação por teclado
- O sistema deve ter contraste adequado
- O sistema deve ter labels em todos os campos

### RNF-005.3: Responsividade
- O sistema deve ser responsivo em desktop (≥ 1024px)
- O sistema deve ser responsivo em tablets (768px - 1023px)
- O sistema deve ser responsivo em mobile (< 768px)
- O sistema deve suportar orientação landscape e portrait

### RNF-005.4: Internacionalização
- O sistema deve suportar português brasileiro
- O sistema deve usar formato de data brasileiro (DD/MM/YYYY)
- O sistema deve usar formato de número brasileiro (vírgula para decimais)
- O sistema deve usar fuso horário de Manaus (UTC-4)

## RNF-006: Manutenibilidade

### RNF-006.1: Código
- O código deve seguir PEP 8
- O código deve ter documentação (docstrings)
- O código deve ter comentários para lógica complexa
- O código deve ter testes unitários (futuro)

### RNF-006.2: Arquitetura
- O sistema deve seguir arquitetura MVC
- O sistema deve ter separação de responsabilidades
- O sistema deve ter baixo acoplamento
- O sistema deve ter alta coesão

### RNF-006.3: Documentação
- O sistema deve ter documentação completa
- O sistema deve ter README detalhado
- O sistema deve ter documentação de API (futuro)
- O sistema deve ter guia de instalação

### RNF-006.4: Versionamento
- O sistema deve usar Git para controle de versão
- O sistema deve ter branches para desenvolvimento
- O sistema deve ter processo de code review (futuro)
- O sistema deve ter CI/CD (futuro)

## RNF-007: Compatibilidade

### RNF-007.1: Navegadores
- O sistema deve funcionar no Chrome (últimas 2 versões)
- O sistema deve funcionar no Firefox (últimas 2 versões)
- O sistema deve funcionar no Safari (últimas 2 versões)
- O sistema deve funcionar no Edge (últimas 2 versões)

### RNF-007.2: Sistemas Operacionais
- O sistema deve funcionar em Windows 10+
- O sistema deve funcionar em macOS 10.14+
- O sistema deve funcionar em Linux (Ubuntu 18.04+)
- O sistema deve funcionar em Android 8+
- O sistema deve funcionar em iOS 12+

### RNF-007.3: Python
- O sistema deve suportar Python 3.8+
- O sistema deve usar virtualenv
- O sistema deve ter requirements.txt atualizado
- O sistema deve ter dependências versionadas

## RNF-008: Confiabilidade

### RNF-008.1: Integridade de Dados
- O sistema deve garantir integridade referencial
- O sistema deve validar todos os inputs
- O sistema deve ter transações atômicas
- O sistema deve ter rollback em caso de erro

### RNF-008.2: Tratamento de Erros
- O sistema deve capturar todas as exceções
- O sistema deve ter mensagens de erro amigáveis
- O sistema deve registrar erros no log
- O sistema deve ter página de erro 500

### RNF-008.3: Testes
- O sistema deve ter testes unitários (futuro)
- O sistema deve ter testes de integração (futuro)
- O sistema deve ter testes E2E (futuro)
- O sistema deve ter cobertura de código > 70% (futuro)

## RNF-009: Portabilidade

### RNF-009.1: Deploy
- O sistema deve ser fácil de deploy
- O sistema deve ter Docker image (futuro)
- O sistema deve suportar múltiplos ambientes (dev, staging, prod)
- O sistema deve ter configuração externalizada

### RNF-009.2: Configuração
- O sistema deve usar variáveis de ambiente
- O sistema deve ter arquivo .env.example
- O sistema deve ter configuração por ambiente
- O sistema deve não ter hardcoded values

## RNF-010: Eficiência

### RNF-010.1: Uso de Recursos
- O sistema deve usar menos de 512MB de RAM
- O sistema deve usar menos de 2GB de armazenamento
- O sistema deve ter baixo consumo de CPU
- O sistema deve otimizar consultas ao banco de dados

### RNF-010.2: Caching
- O sistema deve usar cache para dados frequentes
- O sistema deve ter cache de templates
- O sistema deve ter cache de sessões
- O sistema deve invalidar cache quando necessário

### RNF-010.3: Compressão
- O sistema deve comprimir assets estáticos
- O sistema deve usar GZIP para HTTP
- O sistema deve otimizar imagens
- O sistema deve minificar CSS e JS (futuro)

## RNF-011: Interoperabilidade

### RNF-011.1: APIs Externas
- O sistema deve integrar com Open-Meteo API
- O sistema deve integrar com HIDROWEB API (ANA)
- O sistema deve integrar com Groq API
- O sistema deve integrar com NewsAPI (opcional)

### RNF-011.2: Formato de Dados
- O sistema deve usar JSON para APIs
- O sistema deve usar CSV para exportação
- O sistema deve usar formato padrão de datas
- O sistema deve usar formato padrão de números

### RNF-011.3: Protocolos
- O sistema deve usar HTTP/HTTPS
- O sistema deve usar REST (futuro)
- O sistema deve suportar WebSockets (futuro)
- O sistema deve suportar MQTT (futuro para IoT)

## RNF-012: Privacidade

### RNF-012.1: Coleta de Dados
- O sistema deve coletar apenas dados necessários
- O sistema deve ter política de privacidade
- O sistema deve solicitar consentimento do usuário
- O sistema deve permitir exclusão de dados

### RNF-012.2: Armazenamento de Dados
- Os dados pessoais devem ser criptografados
- Os dados devem ser armazenados em conformidade com LGPD
- O sistema deve ter retenção de dados definida
- O sistema deve permitir acesso aos dados pelo usuário

### RNF-012.3: Compartilhamento de Dados
- O sistema não deve compartilhar dados sem consentimento
- O sistema deve ter termos de uso claros
- O sistema deve ter política de cookies
- O sistema deve respeitar Do Not Track

## RNF-013: Monitoramento

### RNF-013.1: Logs
- O sistema deve registrar todos os erros
- O sistema deve registrar requisições lentas (> 2s)
- O sistema deve registrar acessos não autorizados
- O sistema deve ter logs estruturados

### RNF-013.2: Métricas
- O sistema deve monitorar uso de CPU
- O sistema deve monitorar uso de RAM
- O sistema deve monitorar uso de disco
- O sistema deve monitorar requisições por segundo

### RNF-013.3: Alertas
- O sistema deve alertar sobre erros críticos
- O sistema deve alertar sobre alta latência
- O sistema deve alertar sobre baixa disponibilidade
- O sistema deve alertar sobre uso excessivo de recursos

## RNF-014: Suporte

### RNF-014.1: Documentação
- O sistema deve ter documentação completa
- O sistema deve ter guia de usuário
- O sistema deve ter guia de instalação
- O sistema deve ter FAQ

### RNF-014.2: Help
- O sistema deve ter tooltips explicativos
- O sistema deve ter mensagens de erro claras
- O sistema deve ter suporte em tempo real (futuro)
- O sistema deve ter chat de suporte (futuro)

## RNF-015: Backup e Recuperação

### RNF-015.1: Backup
- O sistema deve ter backup diário automático
- O sistema deve ter backup semanal completo
- O sistema deve ter backup mensal arquivado
- O sistema deve armazenar backups em local seguro

### RNF-015.2: Recuperação
- O sistema deve ter processo de recuperação documentado
- O sistema deve permitir recuperação pontual
- O sistema deve testar backups regularmente
- O sistema deve ter RPO de 24 horas
- O sistema deve ter RTO de 4 horas

## RNF-016: Compliance

### RNF-016.1: LGPD
- O sistema deve estar em conformidade com LGPD
- O sistema deve ter DPO (futuro)
- O sistema deve ter registro de processamento
- O sistema deve ter relatório de impacto

### RNF-016.2: Outros
- O sistema deve seguir melhores práticas de segurança
- O sistema deve ter termos de uso
- O sistema deve ter política de privacidade
- O sistema deve ter política de cookies
