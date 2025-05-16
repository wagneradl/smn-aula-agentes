# Primeiros Passos com Agentes de IA

🟢 **Nível: Iniciante** - Este tutorial não requer conhecimento técnico prévio.

## O que você aprenderá

Neste tutorial, você aprenderá:
- Como configurar o ambiente para usar os agentes
- Como executar um agente de exemplo
- Como entender os resultados
- Próximos passos para aprofundar seu conhecimento

## 1. Configuração do Ambiente

### 1.1 Instalando o Python

Antes de começar, você precisará ter o Python instalado em seu computador.

**No Windows:**
1. Acesse [python.org](https://www.python.org/downloads/)
2. Baixe a versão mais recente do Python para Windows
3. Execute o instalador
4. **Importante**: Marque a caixa "Add Python to PATH" antes de instalar
5. Clique em "Install Now"

**No Mac:**
1. Acesse [python.org](https://www.python.org/downloads/)
2. Baixe a versão mais recente do Python para Mac
3. Execute o instalador e siga as instruções

**No Linux (Ubuntu/Debian):**
1. Abra o Terminal
2. Digite: `sudo apt update && sudo apt install python3 python3-pip`

### 1.2 Obtendo o Repositório

Você pode obter o repositório de duas maneiras:

**Opção 1: Usando Git (recomendado)**
1. Instale o Git a partir de [git-scm.com](https://git-scm.com/downloads)
2. Abra o Terminal ou Prompt de Comando
3. Digite: `git clone https://github.com/smn/agentes-ia.git`
4. Entre na pasta: `cd agentes-smn`

**Opção 2: Download Direto**
1. Acesse o repositório no GitHub
2. Clique no botão verde "Code"
3. Selecione "Download ZIP"
4. Extraia o arquivo ZIP para uma pasta de sua escolha
5. Abra o Terminal ou Prompt de Comando e navegue até a pasta extraída

### 1.3 Instalando as Dependências

1. No Terminal ou Prompt de Comando, navegue até a pasta do repositório
2. Digite: `pip install -r requirements.txt`
3. Aguarde a instalação de todas as bibliotecas necessárias

### 1.4 Configurando a Chave da API

Para usar os agentes que dependem de modelos de linguagem como GPT, você precisará de uma chave de API da OpenAI:

1. Crie uma conta em [platform.openai.com](https://platform.openai.com/)
2. Acesse [API Keys](https://platform.openai.com/api-keys)
3. Clique em "Create new secret key"
4. Copie a chave gerada
5. Na pasta do repositório, crie um arquivo chamado `.env`
6. Adicione a seguinte linha ao arquivo: `OPENAI_API_KEY=sua_chave_aqui`
7. Substitua `sua_chave_aqui` pela chave que você copiou
8. Salve o arquivo

### 1.5 Testando a Configuração

Para verificar se tudo está funcionando corretamente:

1. Na pasta do repositório, digite: `python configuracao/teste_instalacao.py`
2. Você deve ver uma mensagem indicando que tudo está configurado corretamente

## 2. Executando seu Primeiro Agente

Vamos começar com algo simples: o agente de FAQ.

1. Na pasta do repositório, digite: `python exemplos/exemplo_faq.py`
2. O agente será iniciado em modo de linha de comando
3. Digite uma pergunta simples como: "Qual é a política de férias?"
4. Observe como o agente responde com base na sua base de conhecimento

## 3. Entendendo o Funcionamento

Vamos analisar o que acontece quando você executa o agente:

1. **Carregamento da Base de Conhecimento**: O agente primeiro carrega as informações que ele conhece
2. **Processamento da Pergunta**: Quando você faz uma pergunta, o agente:
   - Converte a pergunta em uma representação numérica (embedding)
   - Busca informações relevantes na base de conhecimento
   - Formata um prompt para o modelo de linguagem
3. **Geração da Resposta**: O modelo de linguagem gera uma resposta com base nas informações encontradas
4. **Apresentação**: A resposta é exibida para você

Este fluxo básico é semelhante em todos os agentes, embora cada um tenha suas particularidades dependendo da tarefa que realiza.

## 4. Experimentando Outros Agentes

Agora que você entende o funcionamento básico, experimente outros agentes:

- **Agente de Análise de Dados**: `python exemplos/exemplo_analise_dados.py`
- **Agente de Pesquisa**: `python exemplos/exemplo_pesquisa.py`
- **Agente Processador de Documentos**: `python exemplos/exemplo_processador_documentos.py`

Teste cada um deles e observe como funcionam de maneira diferente para resolver problemas específicos.

## 5. Explorando o Código

Se você estiver curioso sobre como os agentes funcionam, abra os arquivos de exemplo em um editor de texto ou IDE:

1. Use um editor como Notepad++, VSCode, Sublime Text, etc.
2. Abra o arquivo `exemplos/exemplo_faq.py`
3. Leia os comentários que explicam cada parte do código
4. Compare com os outros exemplos para entender as diferenças

## 6. Próximos Passos

Parabéns! Você acabou de começar sua jornada com agentes de IA. Aqui estão algumas sugestões para continuar aprendendo:

1. Leia o tutorial [Personalizando Agentes](personalizando_agentes.md) para aprender a adaptar os agentes às suas necessidades
2. Explore a documentação dos agentes na pasta `agentes/` para implementações mais completas
3. Experimente modificar pequenas partes do código para ver como isso afeta o comportamento dos agentes
4. Participe da comunidade contribuindo com melhorias ou relatando problemas

Lembre-se: a melhor maneira de aprender é experimentando. Não tenha medo de modificar o código e ver o que acontece!

## Resolução de Problemas Comuns

### "ModuleNotFoundError"
- **Problema**: Python não encontra uma biblioteca
- **Solução**: Execute novamente `pip install -r requirements.txt`

### "API key not configured"
- **Problema**: A chave da API não foi configurada corretamente
- **Solução**: Verifique se o arquivo `.env` existe e contém a linha `OPENAI_API_KEY=sua_chave_aqui`

### "Python is not recognized as a command"
- **Problema**: Python não está no PATH do sistema
- **Solução**: Reinstale o Python marcando a opção "Add Python to PATH"

Para mais ajuda, consulte o [guia de solução de problemas](../configuracao/README.md) ou abra uma issue no repositório.