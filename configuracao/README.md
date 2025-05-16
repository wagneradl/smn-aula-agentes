# Configuração do Ambiente

Este guia irá ajudá-lo a configurar seu ambiente para usar os agentes de IA deste repositório, mesmo se você nunca programou antes.

## 1. Pré-requisitos

Você precisará instalar:

- **Python**: A linguagem de programação que usamos (versão 3.8 ou superior)
- **Pip**: O gerenciador de pacotes Python (geralmente vem com o Python)
- **Git**: Para clonar e gerenciar o repositório (opcional)

### Instalando o Python

1. Visite [python.org](https://www.python.org/downloads/) e baixe a versão mais recente para seu sistema operacional
2. Execute o instalador e siga as instruções
3. **Importante**: Marque a opção "Add Python to PATH" durante a instalação

### Verificando a instalação

Abra um terminal (Prompt de Comando no Windows, Terminal no Mac/Linux) e digite:

```
python --version
pip --version
```

Você deve ver as versões instaladas do Python e do Pip.

## 2. Configuração do Projeto

### Clone ou Download do Repositório

**Opção 1 - Usando Git**:
```
git clone https://github.com/smn/agentes-ia.git
cd agentes-smn
```

**Opção 2 - Download direto**:
1. Clique no botão "Code" no GitHub
2. Selecione "Download ZIP"
3. Extraia o arquivo ZIP para uma pasta
4. Navegue até a pasta extraída no terminal

### Instalação das Dependências

No terminal, na pasta do projeto, execute:

```
pip install -r requirements.txt
```

Este comando instalará todas as bibliotecas necessárias para executar os agentes.

## 3. Configuração das Chaves de API

Muitos dos agentes usam serviços de IA como OpenAI (ChatGPT). Para usar esses serviços, você precisará de uma chave de API.

### Obtendo uma Chave OpenAI

1. Crie uma conta em [platform.openai.com](https://platform.openai.com/)
2. Navegue até [API Keys](https://platform.openai.com/api-keys)
3. Clique em "Create new secret key"
4. Dê um nome para sua chave (ex: "Agentes SMN")
5. Copie a chave gerada (você não poderá vê-la novamente!)

### Configurando o Arquivo .env

1. Faça uma cópia do arquivo `.env.exemplo` e renomeie para `.env`
2. Abra o arquivo `.env` em um editor de texto
3. Substitua `SUA_CHAVE_OPENAI_AQUI` pela chave que você copiou
4. Salve o arquivo

Exemplo do arquivo `.env`:
```
OPENAI_API_KEY=sk-sua123chave456openai789aqui
```

## 4. Teste da Configuração

Para verificar se tudo está funcionando corretamente, execute:

```
python configuracao/teste_instalacao.py
```

Se tudo estiver configurado corretamente, você verá uma mensagem de sucesso.

## 5. Solução de Problemas Comuns

### "ModuleNotFoundError"

Se você ver erro como "No module named 'langchain'", execute novamente:
```
pip install -r requirements.txt
```

### "API key not configured"

Verifique se o arquivo `.env` está:
1. Na pasta raiz do projeto
2. Contém a linha `OPENAI_API_KEY=sua-chave-aqui` sem espaços extras
3. A chave API está correta e ativa

### "Python is not recognized as a command"

Se o comando Python não for reconhecido:
1. Reinstale o Python marcando "Add Python to PATH"
2. Ou adicione manualmente o Python ao PATH do seu sistema

## 6. Próximos Passos

Agora que você configurou o ambiente, está pronto para explorar os agentes!

- Experimente os exemplos na pasta `exemplos/`
- Siga os tutoriais em `tutoriais/`
- Personalize os agentes para suas necessidades

Se precisar de ajuda adicional, consulte nossa [documentação](../tutoriais/) ou entre em contato com a equipe de suporte.
