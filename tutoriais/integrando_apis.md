# Integrando APIs com Agentes

🔴 **Nível: Avançado** - Este tutorial requer conhecimento de Python e APIs.

## O que você aprenderá

Neste tutorial, você aprenderá:
- Como conectar agentes de IA a APIs externas
- Como integrar serviços como Google Calendar, Microsoft Teams, e sistemas internos
- Como lidar com autenticação e gerenciamento de credenciais
- Como construir um agente que combina múltiplas fontes de dados

## 1. Por que Integrar APIs?

Os agentes de IA se tornam muito mais poderosos quando podem interagir com o mundo real através de APIs. Integrações permitem que seus agentes:

- Acessem dados atualizados e específicos do seu contexto
- Executem ações em outros sistemas
- Monitorem e respondam a eventos externos
- Forneçam informações personalizadas e contextuais

**Exemplo de Caso de Uso**: Um assistente que pode verificar seu calendário, enviar lembretes pelo Microsoft Teams, e buscar informações em um sistema interno de gestão de projetos.

## 2. Preparação para Integração

### 2.1 Entendendo o Básico de APIs

Para integrar um serviço externo, você precisa entender:

- **Endpoints**: URLs específicos que fornecem funcionalidades
- **Métodos HTTP**: GET, POST, PUT, DELETE, etc.
- **Autenticação**: Como o serviço verifica sua identidade
- **Formatos de Dados**: Geralmente JSON ou XML
- **Rate Limits**: Restrições sobre quantas chamadas você pode fazer

### 2.2 Requisitos de Instalação

Para este tutorial, você precisará instalar algumas bibliotecas adicionais:

```bash
pip install requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client msgraph-core azure-identity msgraph-sdk
```

Ou, mais facilmente, atualize seu ambiente usando nosso arquivo requirements.txt atualizado:

```bash
pip install -r requirements.txt
```

### 2.3 Configurando Credenciais

Mantenha suas credenciais seguras:

1. Nunca armazene chaves diretamente no código
2. Use variáveis de ambiente ou arquivos `.env` para armazenar chaves
3. Para OAuth, implemente um fluxo de autenticação adequado
4. Considere usar um gerenciador de credenciais para ambientes de produção

Veja nosso arquivo `.env.exemplo` atualizado:

```
# Chave da OpenAI
OPENAI_API_KEY=sua_chave_aqui

# Credenciais do Google Calendar
GOOGLE_CLIENT_ID=seu_client_id
GOOGLE_CLIENT_SECRET=seu_client_secret
GOOGLE_REFRESH_TOKEN=seu_refresh_token

# Credenciais do Microsoft Teams
TEAMS_CLIENT_ID=seu_client_id_teams
TEAMS_CLIENT_SECRET=seu_client_secret_teams
TEAMS_TENANT_ID=seu_tenant_id

# Credenciais de sistema interno
INTERNAL_API_URL=https://api.sua-empresa.com
INTERNAL_API_KEY=sua_api_key
```

## 3. Integrando com Google Calendar

### 3.1 Configurando a API do Google

1. Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/)
2. Ative a API do Google Calendar
3. Configure credenciais OAuth
4. Obtenha Client ID, Client Secret, e inicialmente um código de autorização
5. Troque o código por tokens de acesso e atualização

### 3.2 Implementando a Integração

Criamos uma classe para encapsular a funcionalidade do Google Calendar. Você pode encontrar o código completo em `integracao/google_calendar.py`:

```python
# Trecho do código - veja o arquivo completo para mais detalhes
class GoogleCalendarIntegration:
    """Classe para interagir com o Google Calendar."""
    
    def __init__(self):
        """Inicializa a integração com o Google Calendar."""
        self.creds = self._obter_credenciais()
        self.service = build('calendar', 'v3', credentials=self.creds)
    
    def listar_eventos(self, max_results=10, time_min=None, time_max=None):
        """Lista eventos do calendário."""
        # Código para listar eventos
        
    def criar_evento(self, titulo, inicio, fim, descricao=None, participantes=None):
        """Cria um novo evento no calendário."""
        # Código para criar evento
```

### 3.3 Testando a Integração

Para testar a integração com o Google Calendar:

```python
# Teste básico
calendar = GoogleCalendarIntegration()
eventos = calendar.listar_eventos(max_results=5)

1. Registre um aplicativo no [Azure AD Portal](https://portal.azure.com)
2. Configure as permissões necessárias (ex: `Chat.ReadWrite`, `ChannelMessage.Send`)
3. Adicione um segredo do cliente
4. Obtenha o Client ID, Client Secret e Tenant ID

### 3.2 Implementando a Classe de Integração com Microsoft Teams

```python
class TeamsIntegration:
    """Classe para interagir com o Microsoft Teams."""
    
    def __init__(self):
        """Inicializa a integração com o Microsoft Teams."""
        client_id = os.getenv("TEAMS_CLIENT_ID")
        client_secret = os.getenv("TEAMS_CLIENT_SECRET")
        tenant_id = os.getenv("TEAMS_TENANT_ID")
        
        if not client_id or not client_secret or not tenant_id:
            raise ValueError("Credenciais do Microsoft Teams não configuradas")
        
        # Configurar a autenticação OAuth2
        self.credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        
        self.client = GraphClient(credential=self.credential)
    
    def enviar_mensagem(self, canal, texto, blocos=None):
        """Envia uma mensagem para um canal ou chat do Microsoft Teams."""
        # Código para enviar mensagem
        
    def listar_canais(self, team_id=None):
        """Lista todos os canais de um time específico ou de todos os times."""
        # Código para listar canais
```

### 3.3 Configurando o Acesso ao Google Calendar

Para integrar com o Google Calendar, você precisa configurar credenciais OAuth:

1. Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/)
2. Ative a API do Google Calendar
3. Configure a tela de consentimento OAuth
4. Crie credenciais OAuth para aplicativo de desktop
5. Baixe o arquivo JSON de credenciais

Para configuração detalhada, consulte nosso guia em `tutoriais/configuracao_google_calendar.md`.

### 3.4 Implementando a Classe de Integração com Google Calendar

```python
class GoogleCalendarIntegration:
    """Classe para interagir com o Google Calendar."""
    
    def __init__(self):
        """Inicializa a integração com o Google Calendar."""
        self.creds = self._obter_credenciais()
        self.service = build('calendar', 'v3', credentials=self.creds)
    
    def _obter_credenciais(self):
        """Obtém credenciais para a API do Google."""
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")
        
        if client_id and client_secret and refresh_token:
            creds = Credentials(
                None,
                refresh_token=refresh_token,
                client_id=client_id,
                client_secret=client_secret,
                token_uri="https://oauth2.googleapis.com/token"
            )
            return creds
        else:
            raise ValueError("Credenciais do Google não configuradas")
    
    def listar_eventos(self, max_results=10, time_min=None, time_max=None):
        """Lista eventos do calendário."""
        # Código para listar eventos do calendário
        # Veja implementação completa em integracao/google_calendar.py
    
    def criar_evento(self, titulo, descricao, inicio, fim, local=None, participantes=None):
        """Cria um novo evento no calendário."""
        # Código para criar um evento no calendário
        # Veja implementação completa em integracao/google_calendar.py
```

### 3.5 Testando a Integração com Microsoft Teams e Google Calendar

Para testar a integração com o Microsoft Teams e Google Calendar:

```python
# Teste básico
teams = TeamsIntegration()
google_calendar = GoogleCalendarIntegration()

# Listar times
times = teams.listar_times()
print("Times disponíveis:")
for time in times:
    print(f"{time['displayName']} (ID: {time['id']})")

# Listar canais
team_id = times[0]['id']  # ID do primeiro time
canais = teams.listar_canais(team_id)
print("Canais disponíveis:")
for canal in canais:
    print(f"{canal['displayName']} (ID: {canal['id']})")

# Enviar mensagem
canal_id = canais[0]['id']  # ID do primeiro canal
teams.enviar_mensagem(f"{team_id}/{canal_id}", "Olá! Esta é uma mensagem de teste.")

# Listar eventos do calendário
eventos = google_calendar.listar_eventos(max_results=5)

for evento in eventos:
    start = evento['start'].get('dateTime', evento['start'].get('date'))
    print(f"{start} - {evento['summary']}")
```

## 4. Criando um Agente Integrado

Agora vamos aprender a integrar esses serviços em um único agente que pode realizar múltiplas tarefas.

### 4.3 Criando uma API para Sistemas Internos

Para sistemas internos, você geralmente precisará criar sua própria classe de integração adaptada para as APIs específicas da sua empresa.

#### 4.3.1 Cliente de API Genérico

Criamos uma classe genérica que pode ser adaptada para suas APIs internas. Você pode encontrar o código completo em `integracao/api_interna.py`:

```python
# Trecho do código - veja o arquivo completo para mais detalhes
class APIInterna:
    """Cliente para a API interna da empresa."""
    
    def __init__(self):
        """Inicializa o cliente da API interna."""
        self.base_url = os.getenv("INTERNAL_API_URL")
        self.api_key = os.getenv("INTERNAL_API_KEY")
        
        if not self.base_url or not self.api_key:
            raise ValueError("Configuração da API interna ausente")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def buscar_projetos(self, status=None, departamento=None):
        """Busca projetos na API interna."""
        # Código para buscar projetos
        
    def registrar_tarefa(self, projeto_id, titulo, descricao, responsavel_id, prazo):
        """Registra uma nova tarefa em um projeto."""
        # Código para registrar tarefa
```

### 5.2 Testando a Integração

Para testar a integração com a API interna:

```python
# Teste básico
api = APIInterna()

# Buscar projetos ativos
projetos = api.buscar_projetos(status="ativo")
print(f"Encontrados {len(projetos)} projetos ativos")

# Buscar um funcionário
funcionario = api.buscar_funcionario(email="maria@empresa.com")
print(f"Funcionário encontrado: {funcionario['nome']}")
```

### 4.2 Construindo um Agente Integrado

Agora vamos criar um agente que utiliza todas estas integrações para fornecer um assistente completo:

#### 4.2.1 Classe Principal do Agente

Criamos uma classe que integra todas as APIs e usa um modelo de linguagem para interpretar solicitações. Você pode encontrar o código completo em `agentes/agente_integrado.py`:

```python
# Trecho do código - veja o arquivo completo para mais detalhes
class AgenteIntegrado:
    """
    Agente que integra múltiplos serviços para fornecer assistência completa.
    """
    
    def __init__(self):
        """Inicializa o agente integrado."""
        # Inicializar o modelo de linguagem
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo", 
            temperature=0.2,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Inicializar integrações
        try:
            self.calendar = GoogleCalendarIntegration()
            self.teams = TeamsIntegration()
            self.api = APIInterna()
            
            self.servicos_disponiveis = ["calendar", "teams", "api_interna"]
        except Exception as e:
            print(f"Aviso: Nem todas as integrações estão disponíveis - {str(e)}")
            self.servicos_disponiveis = []
        
        # Configurar o chain para processamento de linguagem natural
        self.chain = LLMChain(
            llm=self.llm,
            prompt=ChatPromptTemplate.from_template(
                """
                Você é um assistente que ajuda a entender solicitações e determinar quais ações tomar.
                
                Baseado na solicitação abaixo, identifique:
                1. Qual serviço deve ser utilizado (calendar, teams, api_interna)
                2. Qual ação deve ser realizada
                3. Quais parâmetros são necessários
                
                Formate sua resposta como um JSON com os campos:
                - servico: o nome do serviço a ser usado
                - acao: a ação a ser realizada
                - parametros: um objeto com os parâmetros necessários
                
                Solicitação: {solicitacao}
                
                Resposta:
                """
            )
        )
    
    def processar_solicitacao(self, solicitacao):
        """Processa uma solicitação em linguagem natural e executa a ação apropriada."""
        # Código para processar solicitações
```

### 6.2 Aplicação de Exemplo

Criamos uma aplicação simples que usa nosso agente integrado. Você pode encontrar o código completo em `exemplos/app_integrado.py`:

```python
# Trecho do código - veja o arquivo completo para mais detalhes
def main():
    """Função principal da aplicação."""
    print("=" * 70)
    print("ASSISTENTE INTEGRADO SMN")
    print("=" * 70)
    
    # Inicializar o agente
    agente = AgenteIntegrado()
    
    while True:
        solicitacao = input("\n🤖 Digite sua solicitação: ")
        
        if solicitacao.lower() == "sair":
            print("\nAté a próxima!")
            break
        
        print("\nProcessando sua solicitação...")
        resultado = agente.processar_solicitacao(solicitacao)
        
        # Código para exibir resultados
```

## 7. Considerações Práticas

### 7.1 Gerenciamento de Erros

Ao integrar com APIs externas, é importante lidar adequadamente com erros:

1. **Rate Limits**: Implemente backoff exponencial para tentativas
2. **Timeouts**: Defina timeouts apropriados para evitar bloqueios
3. **Erros de Autenticação**: Implemente renovação de tokens
4. **Indisponibilidade**: Tenha uma estratégia para quando o serviço estiver indisponível

Exemplo de backoff exponencial (disponível em `integracao/utils.py`):

```python
def backoff_retry(func, max_retries=3, initial_delay=1):
    """Executa uma função com backoff exponencial em caso de falhas."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            # Calcular delay com jitter para evitar thundering herd
            delay = initial_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"Tentativa {attempt+1} falhou: {str(e)}. Tentando novamente em {delay:.2f}s...")
            time.sleep(delay)
```

### 7.2 Segurança e Privacidade

Ao lidar com dados sensíveis:

1. **Minimizar Dados**: Solicite apenas as informações necessárias
2. **Escopos de API**: Use o escopo mais restrito possível
3. **Auditoria**: Mantenha logs de todas as ações realizadas
4. **Permissões**: Verifique permissões antes de realizar ações
5. **Sanitização**: Evite injeção de código e outros ataques

### 7.3 Testando Integrações

Para testar integrações de forma confiável:

1. **Mocking**: Use bibliotecas como `unittest.mock` ou `pytest-mock`
2. **Ambientes de Teste**: Crie ambientes separados para desenvolvimento e produção
3. **Fixtures**: Prepare dados de teste consistentes
4. **Integração Contínua**: Automatize testes para detectar problemas rapidamente
5. **Testes de Carga**: Verifique o comportamento sob alta demanda

## 8. Próximos Passos

Agora que você tem um agente integrado com múltiplos serviços, considere estas melhorias:

1. **Adicionar Mais Integrações**: Conecte a outros serviços como Trello, GitHub, ou sistemas de CRM
2. **Melhorar o Entendimento**: Ajuste os prompts para melhor compreensão das solicitações
3. **Interface Gráfica**: Crie uma interface web ou desktop para interagir com o agente
4. **Agentes Personalizados**: Crie agentes especializados para diferentes departamentos
5. **Automação**: Configure o agente para executar tarefas recorrentes automaticamente

## 9. Conclusão

Integrar APIs com agentes de IA permite criar assistentes poderosos que podem interagir com o mundo real. Este agente pode interagir com Google Calendar, Microsoft Teams e sistemas internos. Você aprendeu a:

- Conectar com Google Calendar, Microsoft Teams e APIs internas
- Lidar com autenticação e credenciais de forma segura
- Criar um agente que entende solicitações em linguagem natural
- Gerenciar erros e considerar segurança

Com estas técnicas, você pode criar agentes que aumentam significativamente a produtividade da sua equipe, automatizando tarefas complexas que envolvem múltiplos sistemas.

---

Você pode encontrar todo o código deste tutorial no diretório `integracao/` e um exemplo funcional em `exemplos/app_integrado.py`. Lembre-se de configurar suas credenciais no arquivo `.env` antes de testar.