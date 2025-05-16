# Integração com Microsoft Teams

🔴 **Nível: Avançado** - Este tutorial requer experiência com Python e desenvolvimento de software.

Este tutorial explica como configurar e utilizar a integração com o Microsoft Teams nos agentes da SMN.

## Pré-requisitos

Para utilizar a integração com o Microsoft Teams, você precisará:

1. Uma conta Microsoft 365 com acesso ao Microsoft Teams
2. Permissões para registrar aplicativos no Azure Active Directory
3. Python 3.8 ou superior
4. Pacotes necessários instalados (incluídos no `requirements.txt`)

## Configuração no Azure Active Directory

Antes de utilizar a integração, você precisa registrar um aplicativo no Azure AD:

1. Acesse o [Portal do Azure](https://portal.azure.com)
2. Navegue até "Azure Active Directory" > "Registros de aplicativos"
3. Clique em "Novo registro"
4. Preencha as informações:
   - **Nome**: Agentes SMN
   - **Tipos de conta suportados**: Contas somente nesta organização (somente diretório padrão)
   - **URI de Redirecionamento**: Web > http://localhost:8000/callback
5. Clique em "Registrar"

## Configurar permissões da API

Após registrar o aplicativo, configure as permissões necessárias:

1. No registro do aplicativo, vá para "Permissões de API"
2. Clique em "Adicionar uma permissão"
3. Selecione "Microsoft Graph"
4. Escolha "Permissões delegadas"
5. Adicione as seguintes permissões:
   - `Chat.ReadWrite`
   - `ChannelMessage.Send`
   - `Team.ReadBasic.All`
   - `Channel.ReadBasic.All`
   - `User.Read`
6. Clique em "Adicionar permissões"
7. Clique em "Conceder consentimento de administrador" (se você tiver permissões de administrador)

## Criar segredo do cliente

1. No registro do aplicativo, vá para "Certificados e segredos"
2. Em "Segredos do cliente", clique em "Novo segredo do cliente"
3. Adicione uma descrição e selecione um período de expiração
4. Clique em "Adicionar"
5. **IMPORTANTE**: Copie o valor do segredo imediatamente, pois ele não ficará visível novamente

## Configurar variáveis de ambiente

1. Edite seu arquivo `.env` na raiz do projeto (ou crie um baseado no `.env.exemplo`):

```
# Credenciais do Microsoft Teams
TEAMS_CLIENT_ID=seu_client_id_teams
TEAMS_CLIENT_SECRET=seu_client_secret_teams
TEAMS_TENANT_ID=seu_tenant_id
```

- `TEAMS_CLIENT_ID` - O ID do aplicativo (Application ID) do registro no Azure AD
- `TEAMS_CLIENT_SECRET` - O segredo do cliente que você criou
- `TEAMS_TENANT_ID` - O ID do diretório (tenant) do Azure AD (disponível na visão geral do registro do aplicativo)

## Testes e validação

Para verificar se sua integração com o Microsoft Teams está funcionando corretamente:

```python
from integracao.teams import TeamsIntegration

# Inicializar a integração
teams = TeamsIntegration()

# Listar times disponíveis
times = teams.listar_times()
for time in times:
    print(f"Time: {time['displayName']} (ID: {time['id']})")
    
    # Listar canais de um time
    canais = teams.listar_canais(time['id'])
    for canal in canais:
        print(f"  Canal: {canal['displayName']} (ID: {canal['id']})")
```

## Exemplo de uso com o agente integrado

```python
from agentes.agente_integrado import AgenteIntegrado

# Inicializar o agente
agente = AgenteIntegrado()

# Processar uma solicitação
resultado = agente.processar_solicitacao(
    "Envie uma mensagem para o canal Geral do time Marketing dizendo 'Reunião de alinhamento amanhã às 10h'"
)

if resultado["sucesso"]:
    print("Mensagem enviada com sucesso!")
else:
    print(f"Erro: {resultado['mensagem']}")
```

## Resolução de problemas comuns

### Erro de autenticação
- Verifique se as credenciais no arquivo `.env` estão corretas
- Confirme se as permissões de API foram concedidas corretamente
- Verifique se o aplicativo tem consentimento do administrador

### Erro ao enviar mensagens
- Confirme se o ID do time/canal está correto
- Verifique se você tem permissões para enviar mensagens no canal específico
- Certifique-se de que o formato da mensagem está correto

### Timeout ou erros de conexão
- Verifique sua conexão com a internet
- Confirme que as APIs do Microsoft Graph estão disponíveis
- Confira se não há nenhum firewall ou proxy bloqueando as requisições

## Recursos adicionais

- [Documentação do Microsoft Graph API](https://docs.microsoft.com/graph/overview)
- [Referência de API para Teams](https://docs.microsoft.com/graph/api/resources/teams-api-overview)
- [Azure Active Directory - Registrar um aplicativo](https://docs.microsoft.com/azure/active-directory/develop/quickstart-register-app)
