# ====================================================================
# AGENTE DE PESQUISA E SÍNTESE
# ====================================================================
# Este agente realiza pesquisas em múltiplas fontes, reúne informações
# e cria resumos concisos sobre um tópico específico.
# ====================================================================

# Importamos as bibliotecas necessárias
import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import initialize_agent, Tool, AgentType

# Carregar configurações do arquivo .env
load_dotenv()

# Chaves de API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ====================================================================
# PARTE 1: CONFIGURAÇÃO DAS FERRAMENTAS DE PESQUISA
# ====================================================================
# Definimos as fontes onde o agente poderá buscar informações.
# ====================================================================

# Configurar ferramenta de busca na Wikipedia
wikipedia = WikipediaAPIWrapper(
    lang="pt",
    top_k_results=3,
    doc_content_chars_max=3000
)
wikipedia_tool = WikipediaQueryRun(api_wrapper=wikipedia)

# Função para simular uma busca em documentos internos da empresa
# Em um cenário real, isso se conectaria a uma base de documentos da empresa
def buscar_documentos_internos(query):
    """
    Simula uma busca em documentos internos da SMN.
    
    Args:
        query (str): Termo de busca
        
    Returns:
        str: Resultados encontrados
    """
    # Este é apenas um exemplo - numa implementação real, você conectaria
    # a um sistema de gestão documental, SharePoint, etc.
    
    # Banco de dados simulado de documentos
    documentos = {
        "projeto": "Projeto Alpha: Iniciativa estratégica para expansão da SMN no mercado latino-americano, com foco em sustentabilidade e inovação digital. Lançamento previsto para Q3 2025.",
        "processo": "Processo de aprovação de novos fornecedores: 1) Solicitação via portal, 2) Análise financeira, 3) Verificação de compliance, 4) Aprovação final pelo comitê de compras.",
        "cliente": "Principais clientes da SMN incluem: Grupo Nova Era (setor de energia), TechFuture (tecnologia), EcoSolutions (sustentabilidade) e Consórcio Mobilidade Urbana.",
        "produto": "Linha de produtos 2025: SmartEco (eficiência energética), DataConnect (análise de dados integrada), GreenChain (rastreabilidade sustentável) e Urban Solutions (soluções para cidades inteligentes).",
        "equipe": "Estrutura organizacional: Diretoria Executiva (CEO, CFO, COO, CTO), Gerências (Projetos, Produtos, Operações, RH, Finanças), Coordenações e Equipes Técnicas especializadas por verticais."
    }
    
    # Buscar em cada documento
    resultados = []
    for tipo, conteudo in documentos.items():
        if query.lower() in tipo.lower() or any(termo in conteudo.lower() for termo in query.lower().split()):
            resultados.append(f"[{tipo.upper()}]: {conteudo}")
    
    if resultados:
        return "\n\n".join(resultados)
    else:
        return "Nenhum documento interno encontrado para esta consulta."

# ====================================================================
# PARTE 2: CONFIGURAÇÃO DO MODELO E AGENTE
# ====================================================================
# Configuramos o modelo de linguagem e definimos o agente que usará
# as ferramentas para realizar pesquisas.
# ====================================================================

# Inicializar o modelo de linguagem
modelo = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0)

# Definir as ferramentas disponíveis para o agente
ferramentas = [
    Tool(
        name="Busca na Wikipedia",
        func=wikipedia_tool.run,
        description="Útil para obter informações gerais sobre conceitos, pessoas, lugares, eventos históricos, etc. Use para tópicos de conhecimento público e verificáveis."
    ),
    Tool(
        name="Busca em Documentos Internos",
        func=buscar_documentos_internos,
        description="Útil para obter informações específicas sobre a SMN, como projetos, processos, produtos e clientes. Use para informações internas da empresa."
    )
]

# Inicializar o agente
agente = initialize_agent(
    tools=ferramentas,
    llm=modelo,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,  # Mostrar o processo de raciocínio do agente (pode ser definido como False em produção)
    handle_parsing_errors=True
)

# ====================================================================
# PARTE 3: FUNÇÃO DE SÍNTESE
# ====================================================================
# Esta função pega os resultados da pesquisa e cria um resumo conciso.
# ====================================================================

# Template para o prompt de síntese
template_sintese = """
Você é um especialista em sintetizar informações complexas em resumos claros e concisos.

Com base nas informações a seguir, crie um resumo bem estruturado sobre o tópico "{topico}".

Informações coletadas:
{informacoes}

Seu resumo deve:
1. Ter entre 3-5 parágrafos
2. Começar com uma visão geral do tópico
3. Destacar os pontos mais importantes
4. Organizar as informações de forma lógica
5. Usar linguagem clara e direta
6. Incluir apenas informações presentes no texto acima

RESUMO:
"""

prompt_sintese = ChatPromptTemplate.from_template(template_sintese)

def sintetizar_informacoes(topico, informacoes):
    """
    Sintetiza informações coletadas em um resumo conciso.
    
    Args:
        topico (str): O tópico da pesquisa
        informacoes (str): Informações coletadas
        
    Returns:
        str: Resumo sintetizado
    """
    # Criar o prompt
    mensagens = prompt_sintese.format_messages(
        topico=topico, 
        informacoes=informacoes
    )
    
    # Gerar o resumo
    resposta = modelo.invoke(mensagens)
    
    return resposta.content

# ====================================================================
# PARTE 4: FUNÇÃO PRINCIPAL DE PESQUISA
# ====================================================================
# Esta função coordena o processo de pesquisa e síntese.
# ====================================================================

def pesquisar_e_sintetizar(topico):
    """
    Função principal que realiza pesquisa e síntese sobre um tópico.
    
    Args:
        topico (str): Tópico da pesquisa
        
    Returns:
        str: Resumo sintetizado
    """
    print(f"🔍 Pesquisando sobre: {topico}")
    print("="*70)
    print("Fase 1: Coletando informações...")
    
    # Criar uma consulta para o agente
    consulta = f"Pesquise sobre '{topico}'. Busque tanto informações gerais quanto informações específicas da SMN, se relevantes. Seja meticuloso e abrangente."
    
    try:
        # Executar o agente
        resultados = agente.run(consulta)
        
        print("\nFase 2: Sintetizando informações...")
        
        # Sintetizar os resultados
        resumo = sintetizar_informacoes(topico, resultados)
        
        return resumo
    except Exception as e:
        return f"Erro durante a pesquisa: {str(e)}"

# ====================================================================
# PARTE 5: INTERFACE SIMPLES
# ====================================================================
# Interface de linha de comando para interagir com o agente.
# ====================================================================

def interface_simples():
    """Interface simples para interagir com o agente de pesquisa."""
    print("="*70)
    print("🤖 AGENTE DE PESQUISA E SÍNTESE DA SMN")
    print("="*70)
    print("Este agente pesquisa informações e cria resumos concisos.")
    print("Digite o tópico que deseja pesquisar ou 'sair' para encerrar.")
    print("="*70)
    
    while True:
        topico = input("\n📚 Tópico para pesquisa: ")
        
        if topico.lower() == "sair":
            print("\n👋 Até a próxima!")
            break
        
        # Registrar hora de início
        inicio = time.time()
        
        print("\n🔍 Iniciando pesquisa e síntese. Isso pode levar alguns segundos...\n")
        
        try:
            resumo = pesquisar_e_sintetizar(topico)
            
            # Calcular tempo decorrido
            tempo = time.time() - inicio
            
            print("\n📝 RESUMO:\n")
            print(resumo)
            print(f"\n⏱️ Pesquisa concluída em {tempo:.2f} segundos.")
            
        except Exception as e:
            print(f"❌ Ocorreu um erro: {str(e)}")
            print("Por favor, verifique sua conexão com a internet e a configuração da API.")

# ====================================================================
# PARTE 6: EXECUTAR O AGENTE
# ====================================================================
# Executamos a interface se este arquivo for executado diretamente.
# ====================================================================

if __name__ == "__main__":
    interface_simples()