# ====================================================================
# AGENTE DE ANÁLISE DE DADOS SIMPLES
# ====================================================================
# Este agente analisa dados básicos e gera visualizações simples.
# É útil para obter insights rápidos de dados como vendas, métricas
# de desempenho ou outras informações numéricas.
# ====================================================================

# Importamos as bibliotecas necessárias
import os
import pandas as pd  # Para manipular dados em formato de tabela
import matplotlib.pyplot as plt  # Para criar gráficos
import seaborn as sns  # Para gráficos mais bonitos
from dotenv import load_dotenv  # Para carregar as variáveis de ambiente
from langchain_openai import ChatOpenAI  # Modelo de linguagem para análise
from langchain.prompts import ChatPromptTemplate  # Para criar prompts estruturados

# Configurar visual dos gráficos
sns.set_theme(style="whitegrid")

# Carregar configurações do arquivo .env
load_dotenv()

# Chaves de API (nunca compartilhe estas chaves!)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ====================================================================
# PARTE 1: DADOS DE EXEMPLO
# ====================================================================
# Aqui criamos alguns dados de exemplo para análise.
# Em um caso real, você importaria dados de um arquivo CSV ou Excel.
# ====================================================================

# Criar dados de exemplo de vendas por mês
dados_vendas = {
    'Mês': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho'],
    'Vendas': [42000, 45000, 51000, 48000, 52000, 58000],
    'Custos': [30000, 31000, 32000, 32500, 33000, 33500],
    'Região': ['Sul', 'Sul', 'Norte', 'Norte', 'Centro', 'Centro']
}

# Converter para DataFrame (formato de tabela)
df_vendas = pd.DataFrame(dados_vendas)

# Calcular lucro
df_vendas['Lucro'] = df_vendas['Vendas'] - df_vendas['Custos']

# Salvar dados para uso posterior (em um caso real, você provavelmente pularia esta etapa)
df_vendas.to_csv("vendas_temp.csv", index=False)
print(f"📊 Dados de exemplo criados e salvos em vendas_temp.csv")

# ====================================================================
# PARTE 2: FUNÇÕES DE ANÁLISE BÁSICA
# ====================================================================
# Estas funções realizam análises básicas nos dados:
# - Resumo estatístico
# - Visualização de tendências
# - Comparação por categoria
# ====================================================================

def resumo_estatistico(dados):
    """
    Gera um resumo estatístico básico dos dados.
    
    Args:
        dados (DataFrame): Dados a serem analisados
    
    Returns:
        DataFrame: Resumo estatístico
    """
    # Selecionar apenas colunas numéricas
    colunas_numericas = dados.select_dtypes(include=['int64', 'float64']).columns
    
    # Calcular estatísticas básicas
    resumo = dados[colunas_numericas].describe()
    
    return resumo

def visualizar_tendencia(dados, coluna_x, coluna_y, titulo=None):
    """
    Cria um gráfico de linha para visualizar tendências ao longo do tempo.
    
    Args:
        dados (DataFrame): Dados a serem visualizados
        coluna_x (str): Nome da coluna para o eixo X (geralmente tempo)
        coluna_y (str): Nome da coluna para o eixo Y (métrica de interesse)
        titulo (str, opcional): Título do gráfico
    """
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=dados, x=coluna_x, y=coluna_y, marker='o', linewidth=2)
    
    if not titulo:
        titulo = f"{coluna_y} por {coluna_x}"
    
    plt.title(titulo, fontsize=16)
    plt.xlabel(coluna_x, fontsize=12)
    plt.ylabel(coluna_y, fontsize=12)
    plt.tight_layout()
    
    # Salvar o gráfico
    nome_arquivo = f"tendencia_{coluna_y}_por_{coluna_x}.png".replace(" ", "_").lower()
    plt.savefig(nome_arquivo)
    plt.close()
    
    print(f"📈 Gráfico de tendência salvo como {nome_arquivo}")
    return nome_arquivo

def comparar_categorias(dados, coluna_categoria, coluna_valor, tipo='barras', titulo=None):
    """
    Cria um gráfico para comparar valores entre diferentes categorias.
    
    Args:
        dados (DataFrame): Dados a serem visualizados
        coluna_categoria (str): Nome da coluna com as categorias
        coluna_valor (str): Nome da coluna com os valores a comparar
        tipo (str): Tipo de gráfico ('barras' ou 'pizza')
        titulo (str, opcional): Título do gráfico
    """
    plt.figure(figsize=(10, 6))
    
    if tipo == 'barras':
        resumo = dados.groupby(coluna_categoria)[coluna_valor].sum().reset_index()
        sns.barplot(data=resumo, x=coluna_categoria, y=coluna_valor)
        
        if not titulo:
            titulo = f"{coluna_valor} por {coluna_categoria}"
            
        plt.title(titulo, fontsize=16)
        plt.xlabel(coluna_categoria, fontsize=12)
        plt.ylabel(coluna_valor, fontsize=12)
        
    elif tipo == 'pizza':
        resumo = dados.groupby(coluna_categoria)[coluna_valor].sum()
        plt.pie(resumo, labels=resumo.index, autopct='%1.1f%%', startangle=90)
        
        if not titulo:
            titulo = f"Distribuição de {coluna_valor} por {coluna_categoria}"
            
        plt.title(titulo, fontsize=16)
        plt.axis('equal')  # Para garantir que o gráfico seja circular
    
    plt.tight_layout()
    
    # Salvar o gráfico
    nome_arquivo = f"comparacao_{coluna_valor}_por_{coluna_categoria}_{tipo}.png".replace(" ", "_").lower()
    plt.savefig(nome_arquivo)
    plt.close()
    
    print(f"📊 Gráfico de comparação salvo como {nome_arquivo}")
    return nome_arquivo

# ====================================================================
# PARTE 3: AGENTE DE ANÁLISE COM IA
# ====================================================================
# Este componente usa IA para interpretar dados e sugerir insights.
# ====================================================================

# Inicializar o modelo de linguagem
modelo = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")

# Template para o prompt de análise
template_analise = """
Você é um analista de dados especializado em extrair insights de métricas de negócios.
Analise os seguintes dados e ofereça 3-5 insights relevantes e práticos.

Dados:
{dados}

Estatísticas básicas:
{estatisticas}

Forneça apenas os insights mais importantes, em linguagem simples e direta.
Foque em tendências, anomalias e oportunidades que você identifica nos dados.
"""

prompt_analise = ChatPromptTemplate.from_template(template_analise)

def gerar_insights(dados):
    """
    Usa IA para gerar insights a partir dos dados.
    
    Args:
        dados (DataFrame): Dados para análise
        
    Returns:
        str: Insights gerados pela IA
    """
    # Obter estatísticas básicas
    estatisticas = resumo_estatistico(dados)
    
    # Preparar o prompt
    mensagens = prompt_analise.format_messages(
        dados=dados.to_string(),
        estatisticas=estatisticas.to_string()
    )
    
    # Gerar insights
    resposta = modelo.invoke(mensagens)
    
    return resposta.content

# ====================================================================
# PARTE 4: FUNÇÃO PRINCIPAL DO AGENTE
# ====================================================================
# Esta função orquestra todo o processo de análise.
# ====================================================================

def analisar_dados(caminho_arquivo=None, df=None):
    """
    Função principal que realiza a análise completa dos dados.
    
    Args:
        caminho_arquivo (str, opcional): Caminho para arquivo CSV/Excel
        df (DataFrame, opcional): DataFrame já carregado
        
    Returns:
        dict: Resultados da análise, incluindo caminhos dos gráficos
    """
    # Carregar dados se um caminho de arquivo for fornecido
    if caminho_arquivo:
        if caminho_arquivo.endswith('.csv'):
            df = pd.read_csv(caminho_arquivo)
        elif caminho_arquivo.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(caminho_arquivo)
        else:
            raise ValueError("Formato de arquivo não suportado. Use CSV ou Excel.")
    
    # Usar o DataFrame fornecido ou os dados de exemplo
    if df is None:
        if os.path.exists("vendas_temp.csv"):
            df = pd.read_csv("vendas_temp.csv")
        else:
            raise ValueError("Nenhum dado fornecido para análise.")
    
    print(f"📊 Analisando dados com {len(df)} linhas e {len(df.columns)} colunas.")
    
    # Identificar colunas numéricas e categóricas
    colunas_numericas = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    colunas_categoricas = df.select_dtypes(include=['object']).columns.tolist()
    
    # Coletar resultados
    resultados = {
        'resumo': resumo_estatistico(df),
        'graficos': [],
        'insights': None
    }
    
    # Gerar visualizações de tendência
    if len(df) > 1 and len(colunas_numericas) > 0 and len(colunas_categoricas) > 0:
        for coluna_y in colunas_numericas:
            coluna_x = colunas_categoricas[0]  # Assumimos a primeira coluna categórica como temporal
            nome_grafico = visualizar_tendencia(df, coluna_x, coluna_y)
            resultados['graficos'].append(nome_grafico)
    
    # Gerar visualizações de comparação
    if len(colunas_categoricas) > 0 and len(colunas_numericas) > 0:
        for coluna_categoria in colunas_categoricas:
            for coluna_valor in colunas_numericas:
                nome_grafico = comparar_categorias(df, coluna_categoria, coluna_valor, 'barras')
                resultados['graficos'].append(nome_grafico)
    
    # Gerar insights
    resultados['insights'] = gerar_insights(df)
    
    return resultados

# ====================================================================
# PARTE 5: INTERFACE SIMPLES
# ====================================================================
# Interface de linha de comando para interagir com o agente.
# ====================================================================

def interface_simples():
    """Interface simples para interagir com o agente de análise."""
    print("="*70)
    print("🤖 AGENTE DE ANÁLISE DE DADOS DA SMN")
    print("="*70)
    print("Este agente analisa dados e gera visualizações e insights.")
    print("Por padrão, usará os dados de exemplo (vendas).")
    print("Digite o caminho para um arquivo CSV/Excel ou pressione Enter para usar os dados de exemplo.")
    print("Digite 'sair' para encerrar.")
    print("="*70)
    
    while True:
        caminho = input("\n📄 Caminho do arquivo (ou Enter para dados de exemplo): ")
        
        if caminho.lower() == "sair":
            print("\n👋 Até a próxima!")
            break
        
        caminho_arquivo = None if not caminho else caminho
        
        print("\n🔍 Iniciando análise. Isso pode levar alguns segundos...\n")
        
        try:
            resultados = analisar_dados(caminho_arquivo)
            
            print("\n📊 RESUMO ESTATÍSTICO:\n")
            print(resultados['resumo'])
            
            print("\n📈 GRÁFICOS GERADOS:")
            for grafico in resultados['graficos']:
                print(f"- {grafico}")
            
            print("\n💡 INSIGHTS:\n")
            print(resultados['insights'])
            
        except Exception as e:
            print(f"❌ Ocorreu um erro: {str(e)}")
            print("Por favor, verifique se o arquivo existe e está em formato válido.")

# ====================================================================
# PARTE 6: EXECUTAR O AGENTE
# ====================================================================
# Executamos a interface se este arquivo for executado diretamente.
# ====================================================================

if __name__ == "__main__":
    interface_simples()
    
    # Limpeza do arquivo temporário
    if os.path.exists("vendas_temp.csv"):
        os.remove("vendas_temp.csv")