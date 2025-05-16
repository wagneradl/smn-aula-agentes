# Personalizando Agentes

🟡 **Nível: Intermediário** - Este tutorial requer compreensão básica de conceitos de programação.

## O que você aprenderá

Neste tutorial, você aprenderá:
- Como personalizar um agente existente para suas necessidades específicas
- Como modificar a base de conhecimento, prompts e comportamento
- Como adaptar parâmetros para melhorar o desempenho

## 1. Personalizando o Agente de FAQ

O Agente de FAQ é um dos mais simples de personalizar. Vamos modificá-lo para responder a perguntas sobre sua própria organização.

### 1.1 Modificando a Base de Conhecimento

1. Abra o arquivo `exemplos/exemplo_faq.py` em um editor de texto
2. Localize a seção "PARTE 1: BASE DE CONHECIMENTO" (cerca da linha 30)
3. Substitua o conteúdo da variável `conhecimento` com suas próprias informações:

```python
conhecimento = """
# Política de Reuniões da [Sua Empresa]

- As reuniões gerais ocorrem todas as segundas-feiras às 10h.
- As reuniões de equipe são agendadas pelos líderes de cada área.
- Todas as reuniões devem ter uma agenda compartilhada com antecedência.
- Para reservar salas de reunião, use o sistema no link: [seu-link-aqui]

# Benefícios para Funcionários

- Plano de saúde: Disponível após 3 meses de empresa.
- Vale refeição: R$ 40 por dia útil trabalhado.
- Auxílio educação: Até R$ 400 mensais para cursos relacionados à função.
- Horário flexível: Núcleo das 10h às 15h, com 8h diárias totais.

# Suporte de TI

- Para problemas técnicos, abra um chamado em: [seu-sistema-de-chamados]
- O horário de atendimento é de segunda a sexta, das 8h às 18h.
- Para emergências fora do horário comercial, ligue para: [número]
"""
```

### 1.2 Personalizando o Comportamento do Agente

Para alterar como o agente responde, modifique o prompt:

1. Localize a seção "PARTE 3: CONFIGURAÇÃO DO AGENTE" (cerca da linha 70)
2. Modifique o `template_prompt` para refletir a voz e estilo da sua empresa:

```python
template_prompt = """
Você é um assistente virtual da [Sua Empresa], especializado em responder perguntas 
sobre nossas políticas e procedimentos. Use um tom profissional e amigável 
que reflita nossos valores de transparência e colaboração.

Informações relevantes da base de conhecimento:
{contexto}

Pergunta do funcionário: {pergunta}

Sua resposta (use apenas as informações fornecidas acima):
"""
```

### 1.3 Ajustando Parâmetros de Busca

Para melhorar a relevância das respostas:

1. Localize a função `responder_pergunta` (cerca da linha 90)
2. Ajuste o parâmetro `k` na busca de similaridade para controlar quantos documentos são considerados:

```python
# Buscar mais documentos para perguntas complexas
documentos_relevantes = base_conhecimento.similarity_search(pergunta, k=5)
```

## 2. Personalizando o Agente de Análise de Dados

### 2.1 Usando Seus Próprios Dados

1. Crie um arquivo CSV com seus dados (ex: `vendas_reais.csv`)
2. Modifique a chamada ao agente para usar seus dados:

```python
python exemplos/exemplo_analise_dados.py vendas_reais.csv
```

Alternativamente, modifique o código para carregar seus dados diretamente:

1. Abra o arquivo `exemplos/exemplo_analise_dados.py`
2. Localize a seção "PARTE 1: DADOS DE EXEMPLO" (cerca da linha 30)
3. Substitua a criação do DataFrame de exemplo com seus próprios dados:

```python
# Carregar dados reais
import pandas as pd
df_vendas = pd.read_csv('caminho/para/seus/dados.csv')
```

### 2.2 Personalizando Visualizações

Para modificar as visualizações geradas:

1. Localize as funções `visualizar_tendencia` e `comparar_categorias`
2. Ajuste os parâmetros como cores, estilos e rótulos:

```python
def visualizar_tendencia(dados, coluna_x, coluna_y, titulo=None):
    plt.figure(figsize=(12, 7))  # Tamanho maior
    sns.lineplot(data=dados, x=coluna_x, y=coluna_y, 
                marker='o', linewidth=3, color='#0066cc')  # Linha mais grossa, cor personalizada
    
    # Resto da função...
```

### 2.3 Customizando Insights

Para direcionar o tipo de insights gerados:

1. Localize o `template_analise` (cerca da linha 150)
2. Modifique para focar em aspectos específicos:

```python
template_analise = """
Você é um analista de dados especializado em vendas e marketing.
Analise os seguintes dados e ofereça 3-5 insights relevantes e práticos.

Dados:
{dados}

Estatísticas básicas:
{estatisticas}

Concentre-se especialmente em tendências de crescimento, sazonalidade 
e oportunidades de otimização de recursos. Sugira ações concretas 
com base nos dados.
"""
```

## 3. Personalizando o Agente de Pesquisa

### 3.1 Configurando Fontes de Informação Personalizadas

O agente de pesquisa pode ser personalizado para buscar em suas fontes internas:

1. Abra o arquivo `exemplos/exemplo_pesquisa.py`
2. Localize a função `buscar_documentos_internos`
3. Modifique o dicionário `documentos` para incluir suas próprias informações:

```python
# Banco de dados simulado de documentos
documentos = {
    "projeto-alpha": "Descrição do Projeto Alpha: [seus detalhes aqui]",
    "cliente-xyz": "Informações sobre o cliente XYZ: [detalhes do cliente]",
    "manual-produto": "Manual do Produto A: [conteúdo do manual]",
    # Adicione mais documentos conforme necessário
}
```

Em um cenário real, você conectaria esta função a um sistema de gestão de documentos ou base de conhecimento interna.

### 3.2 Personalizando o Comportamento de Pesquisa

Para modificar como o agente realiza pesquisas:

1. Localize a seção "PARTE 2: CONFIGURAÇÃO DO MODELO E AGENTE" (cerca da linha 65)
2. Ajuste o modelo, temperatura ou ferramentas:

```python
# Temperatura mais baixa para respostas mais determinísticas
modelo = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0.2)

# Adicionar ou modificar ferramentas
ferramentas = [
    Tool(
        name="Busca na Wikipedia",
        func=wikipedia_tool.run,
        description="Útil para informações gerais e verificáveis."
    ),
    Tool(
        name="Busca em Documentos Internos",
        func=buscar_documentos_internos,
        description="Use para informações específicas da nossa empresa."
    ),
    Tool(
        name="Busca em Base de Conhecimento de Produto",
        func=buscar_info_produto,  # Você precisaria implementar esta função
        description="Use para informações sobre nossos produtos e serviços."
    )
]
```

### 3.3 Personalizando o Formato da Síntese

Para modificar como o agente sintetiza informações:

1. Localize o `template_sintese` (cerca da linha 100)
2. Ajuste para o formato e estilo desejados:

```python
template_sintese = """
Você é um especialista em comunicação da [Sua Empresa].

Com base nas informações a seguir, crie um resumo bem estruturado sobre o tópico "{topico}".

Informações coletadas:
{informacoes}

Seu resumo deve:
1. Começar com um título atrativo
2. Ter uma estrutura clara com subtítulos
3. Incluir apenas fatos verificados
4. Terminar com recomendações práticas
5. Usar nosso tom de voz: profissional mas acessível
6. Ter no máximo 500 palavras

RESUMO:
"""
```

## 4. Personalizando o Agente Processador de Documentos

### 4.1 Adaptando a Extração para Seus Documentos

Para focar na extração de informações específicas:

1. Abra o arquivo `exemplos/exemplo_processador_documentos.py`
2. Localize o `template_extracao_geral` (cerca da linha 60)
3. Modifique para extrair as informações específicas que você precisa:

```python
template_extracao_geral = """
Você é um especialista em extrair informações de [tipo específico de documento].

Analise o seguinte segmento de texto e extraia apenas as informações listadas abaixo:

TEXTO:
{texto}

Extraia no formato JSON:
- Número do projeto
- Datas de início e fim
- Responsáveis
- Orçamento total
- Status atual
- Principais entregas
- Riscos identificados

Para cada campo, use "não encontrado" se a informação não estiver presente.
"""
```

### 4.2 Integrando com Seus Sistemas

Para uma implementação real, você pode adaptar o agente para usar seus sistemas de armazenamento:

```python
def salvar_resultados(resultados, metadados):
    """
    Salva os resultados em um sistema real (ex: banco de dados, API)
    """
    # Exemplo: Salvar em um banco de dados
    # import sqlite3
    # conn = sqlite3.connect('sua_base_de_dados.db')
    # cursor = conn.cursor()
    # cursor.execute(
    #     "INSERT INTO documentos_processados (nome, tipo, data, resultados) VALUES (?, ?, ?, ?)",
    #     (metadados['nome'], metadados['tipo'], metadados['data_processamento'], json.dumps(resultados))
    # )
    # conn.commit()
    # conn.close()
    
    print(f"✅ Resultados salvos para: {metadados['nome']}")
```

## 5. Dicas Gerais para Personalização

### 5.1 Ajustando o Modelo de Linguagem

Para todos os agentes, você pode ajustar o modelo usado:

```python
# Para respostas mais criativas
modelo = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4", temperature=0.7)

# Para respostas mais precisas e determinísticas
modelo = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0)
```

### 5.2 Melhorando os Prompts

Bons prompts são cruciais para o desempenho do agente:

1. Seja específico sobre o papel e o tom que o agente deve adotar
2. Forneça exemplos do formato de saída desejado
3. Inclua restrições claras (ex: "use apenas as informações fornecidas")
4. Especifique o que fazer quando informações estiverem faltando

### 5.3 Lidando com Erros Graciosamente

Adicione tratamento de erros para melhorar a robustez:

```python
try:
    resposta = responder_pergunta(pergunta)
    print(f"🔹 {resposta}\n")
except Exception as e:
    print(f"❌ Desculpe, encontrei um problema: {str(e)}")
    print("Vou tentar uma abordagem alternativa...")
    # Implementar uma estratégia de fallback
```

## 6. Próximos Passos

Agora que você sabe como personalizar agentes existentes, pode:

1. Aplicar essas modificações aos agentes completos na pasta `agentes/`
2. Combinar diferentes agentes para tarefas mais complexas
3. Avançar para o tutorial [Integrando APIs](integrando_apis.md) para conectar agentes a serviços externos
4. Explorar a criação de um agente totalmente novo com [Criando Novo Agente](criando_novo_agente.md)

Lembre-se de testar suas modificações incrementalmente e manter cópias de backup do código original enquanto experimenta!