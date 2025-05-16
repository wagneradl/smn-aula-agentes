# Configuração do Google Calendar

🔴 **Nível: Avançado** - Este tutorial requer experiência com Python e desenvolvimento de software.

Este guia fornece instruções passo a passo para configurar a integração com o Google Calendar no projeto de agentes da SMN.

## Pré-requisitos

- Conta Google
- Acesso à Internet
- Python 3.6 ou superior

## Etapas de Configuração

### 1. Criar um Projeto no Google Cloud

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Clique em "Selecionar um projeto" no topo da página
3. Clique em "Novo Projeto"
4. Dê um nome ao projeto (por exemplo, "SMN Agentes")
5. Clique em "Criar"
6. Aguarde a criação do projeto e selecione-o

### 2. Ativar a API do Google Calendar

1. No menu lateral, clique em "APIs e Serviços" > "Biblioteca"
2. Na caixa de pesquisa, digite "Google Calendar API"
3. Clique no resultado "Google Calendar API"
4. Clique no botão "Ativar"

### 3. Configurar a Tela de Consentimento OAuth

1. No menu lateral, clique em "APIs e Serviços" > "Tela de consentimento OAuth"
2. Selecione "Externo" (disponível para qualquer usuário com uma Conta do Google) e clique em "Criar"
3. Preencha as informações necessárias:
   - Nome do aplicativo: "SMN Agentes Calendar"
   - E-mail de suporte ao usuário: seu e-mail
   - E-mail do desenvolvedor: seu e-mail
4. Clique em "Salvar e Continuar"
5. Na tela "Escopos", clique em "Adicionar ou remover escopos"
6. Pesquise por "calendar" e selecione a opção `.../auth/calendar` (Visualizar, editar, compartilhar e excluir todos os calendários)
7. Clique em "Atualizar" e depois em "Salvar e Continuar"
8. Na tela "Usuários de teste", adicione seu e-mail como usuário de teste
9. Clique em "Salvar e Continuar" e depois em "Voltar ao Painel"

### 4. Criar Credenciais OAuth

1. No menu lateral, clique em "APIs e Serviços" > "Credenciais"
2. Clique em "Criar Credenciais" e selecione "ID do cliente OAuth"
3. Selecione "Aplicativo para Desktop" como tipo de aplicativo
4. Dê um nome à credencial (por exemplo, "SMN Agentes Desktop")
5. Clique em "Criar"
6. Uma janela irá aparecer com seu Client ID e Client Secret
7. Clique em "Download JSON" para baixar o arquivo de credenciais
8. Renomeie o arquivo baixado para `client_secret.json`

### 5. Configurar o Projeto

1. Copie o arquivo `client_secret.json` para a raiz do projeto de agentes da SMN
2. Execute o script de obtenção de token:

```bash
python integracao/obter_token_google.py
```

3. Siga as instruções exibidas no terminal:
   - Uma página web será aberta no seu navegador
   - Faça login com sua conta Google e autorize o aplicativo
   - Após autorizar, você verá uma mensagem de confirmação

4. O script criará um arquivo `token.pickle` e exibirá as informações necessárias para configurar o arquivo `.env`

### 6. Configurar o Arquivo .env

Adicione as seguintes variáveis ao seu arquivo `.env`:

```
GOOGLE_CLIENT_ID=seu_client_id
GOOGLE_CLIENT_SECRET=seu_client_secret
GOOGLE_REFRESH_TOKEN=seu_refresh_token
USER_EMAIL=seu_email@gmail.com
```

Substitua os valores pelos fornecidos pelo script `obter_token_google.py`.

## Testando a Integração

Após configurar todas as credenciais, você pode testar a integração usando:

```bash
python testes/teste_google_calendar.py
```

Ou explorar o exemplo interativo:

```bash
python exemplos/exemplo_google_calendar.py
```

## Solução de Problemas

### Erro de autenticação

Se você encontrar erros de autenticação:
1. Verifique se as credenciais no arquivo `.env` estão corretas
2. Confirme que a API do Google Calendar está ativada
3. Tente regenerar o token executando novamente `obter_token_google.py`

### Erro "invalid_grant"

Este erro geralmente ocorre quando o refresh_token expirou:
1. Exclua o arquivo `token.pickle`
2. Execute novamente o script `obter_token_google.py`
3. Atualize as variáveis de ambiente com o novo refresh_token

### Erros de permissão de calendário

Se você encontrar erros ao tentar criar ou listar eventos:
1. Verifique se você adicionou o escopo correto na tela de consentimento OAuth
2. Confirme que está usando a mesma conta Google que autorizou o aplicativo
3. Verifique se o calendário que está tentando acessar existe e você tem permissões sobre ele

## Recursos Adicionais

- [Documentação da API do Google Calendar](https://developers.google.com/calendar/api/guides/overview)
- [Autenticação OAuth 2.0 para Aplicativos Desktop](https://developers.google.com/identity/protocols/oauth2/native-app)
