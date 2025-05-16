# ====================================================================
# AGENTE PROCESSADOR DE DOCUMENTOS
# ====================================================================
# Este agente extrai informações importantes de documentos como faturas,
# relatórios e e-mails, facilitando a organização e análise de dados.
# ====================================================================

# Importamos as bibliotecas necessárias
import os
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Carregar configurações do arquivo .env
load_dotenv()

# Chaves de API (nunca compartilhe estas chaves!)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ====================================================================
# PARTE 1: CARREGAMENTO DE DOCUMENTOS
# ====================================================================
# Esta parte se encarrega de carregar diferentes tipos de documentos.
# ====================================================================

def carregar_documento(caminho_arquivo):
    """
    Carrega um documento baseado em sua extensão.
    
    Args:
        caminho_arquivo (str): Caminho para o arquivo
        
    Returns:
        list: Lista de segmentos de texto do documento
    """
    print(f"📄 Carregando documento: {caminho_arquivo}")
    
    # Verificar se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
    
    # Carregar baseado na extensão
    if caminho_arquivo.endswith('.pdf'):
        loader = PyPDFLoader(caminho_arquivo)
        paginas = loader.load()
        
        # Extrair o conteúdo de cada página
        texto = "\n\n".join([pagina.page_content for pagina in paginas])
        
    elif caminho_arquivo.endswith('.txt'):
        loader = TextLoader(caminho_arquivo)
        documentos = loader.load()
        texto = documentos[0].page_content
        
    elif caminho_arquivo.endswith(('.docx', '.doc')):
        # Nota: Para arquivos Word, você precisaria instalar pacotes adicionais
        # como python-docx e adicionar o código apropriado
        raise NotImplementedError("Suporte para arquivos Word ainda não implementado neste exemplo")
        
    else:
        raise ValueError(f"Formato de arquivo não suportado: {caminho_arquivo}")
    
    # Dividir o texto em segmentos menores para processamento
    divisor_texto = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    segmentos = divisor_texto.split_text(texto)
    
    print(f"✅ Documento carregado e dividido em {len(segmentos)} segmentos")
    
    return segmentos

# ====================================================================
# PARTE 2: EXTRAÇÃO DE INFORMAÇÕES
# ====================================================================
# Esta parte analisa o texto e extrai informações estruturadas.
# ====================================================================

# Inicializar o modelo de linguagem
modelo = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")

# Template para extrair informações gerais
template_extracao_geral = """
Você é um especialista em extrair informações relevantes de documentos de negócios.

Analise o seguinte segmento de texto e extraia as informações principais:

TEXTO:
{texto}

Extraia todas as informações relevantes no formato JSON, com campos apropriados para o tipo de documento.
Se não conseguir identificar alguma informação, use "não encontrado" como valor.

Se parecer um e-mail, extraia: remetente, destinatários, assunto, data, mensagem principal e ações requeridas.
Se parecer uma fatura, extraia: número da fatura, data, fornecedor, cliente, itens, valores, total e prazo de pagamento.
Se parecer um relatório, extraia: título, data, autor, seções principais e conclusões.
Se for outro tipo de documento, identifique o tipo e extraia as informações mais relevantes.

Formato JSON:
"""

prompt_extracao_geral = ChatPromptTemplate.from_template(template_extracao_geral)

# Template para extrair dados específicos (como informações de contato)
template_extracao_contatos = """
Você é um especialista em extrair informações de contato de documentos.

Analise o seguinte segmento de texto e extraia todas as informações de contato:

TEXTO:
{texto}

Extraia todas as seguintes informações no formato JSON:
- Nomes de pessoas
- Endereços de e-mail
- Números de telefone
- Empresas/Organizações
- Endereços físicos

Para cada tipo de informação, retorne uma lista, mesmo que vazia.
Não invente informações que não estejam no texto.

Formato JSON:
"""

prompt_extracao_contatos = ChatPromptTemplate.from_template(template_extracao_contatos)

def extrair_informacoes(segmentos, tipo_extracao="geral"):
    """
    Extrai informações estruturadas de segmentos de texto.
    
    Args:
        segmentos (list): Lista de segmentos de texto
        tipo_extracao (str): Tipo de extração a realizar ('geral' ou 'contatos')
        
    Returns:
        list: Lista de resultados de extração
    """
    resultados = []
    
    # Selecionar o prompt apropriado
    if tipo_extracao == "contatos":
        prompt = prompt_extracao_contatos
    else:  # default para "geral"
        prompt = prompt_extracao_geral
    
    print(f"🔍 Extraindo informações ({tipo_extracao}) de {len(segmentos)} segmentos...")
    
    # Processar cada segmento
    for i, segmento in enumerate(segmentos):
        print(f"  Processando segmento {i+1}/{len(segmentos)}...")
        
        # Preparar o prompt
        mensagens = prompt.format_messages(texto=segmento)
        
        # Enviar para o modelo e obter resposta
        resposta = modelo.invoke(mensagens)
        
        # Adicionar aos resultados
        resultados.append(resposta.content)
    
    return resultados

# ====================================================================
# PARTE 3: CONSOLIDAÇÃO DE RESULTADOS
# ====================================================================
# Esta parte combina resultados de múltiplos segmentos.
# ====================================================================

def consolidar_resultados(resultados_extracao, metadados_documento):
    """
    Consolida resultados de múltiplos segmentos em um único resumo.
    
    Args:
        resultados_extracao (list): Lista de resultados da extração
        metadados_documento (dict): Informações sobre o documento
        
    Returns:
        str: Resumo consolidado em formato JSON
    """
    # Template para consolidação
    template_consolidacao = f"""
    Você é um especialista em consolidar informações de diferentes partes de um documento.
    
    Informações sobre o documento:
    - Nome do arquivo: {metadados_documento.get('nome', 'Desconhecido')}
    - Tipo de arquivo: {metadados_documento.get('tipo', 'Desconhecido')}
    - Data de processamento: {metadados_documento.get('data_processamento', 'Desconhecida')}
    
    Abaixo estão os resultados da extração de informações de diferentes segmentos do documento.
    Consolide essas informações em um único JSON coerente, removendo duplicações e organizando
    as informações de forma lógica.
    
    Resultados da extração:
    {resultados_extracao}
    
    Resultado consolidado (em formato JSON):
    """
    
    # Preparar o prompt
    mensagens = ChatPromptTemplate.from_template(template_consolidacao).format_messages(
        resultados_extracao="\n\n".join(resultados_extracao)
    )
    
    # Enviar para o modelo e obter resposta
    resposta = modelo.invoke(mensagens)
    
    return resposta.content

# ====================================================================
# PARTE 4: FUNÇÃO PRINCIPAL DE PROCESSAMENTO
# ====================================================================
# Esta função coordena todo o processo de análise de documentos.
# ====================================================================

def processar_documento(caminho_arquivo, tipos_extracao=["geral"]):
    """
    Função principal que processa um documento do início ao fim.
    
    Args:
        caminho_arquivo (str): Caminho para o arquivo a ser processado
        tipos_extracao (list): Lista de tipos de extração a realizar
        
    Returns:
        dict: Resultados consolidados para cada tipo de extração
    """
    # Obter metadados básicos do documento
    nome_arquivo = os.path.basename(caminho_arquivo)
    tipo_arquivo = os.path.splitext(nome_arquivo)[1]
    metadados = {
        "nome": nome_arquivo,
        "tipo": tipo_arquivo,
        "caminho": caminho_arquivo,
        "data_processamento": "2025-05-15"  # Em um sistema real, usaria a data atual
    }
    
    print(f"🔄 Iniciando processamento do documento: {nome_arquivo}")
    
    # Carregar o documento
    segmentos = carregar_documento(caminho_arquivo)
    
    # Armazenar resultados para cada tipo de extração
    resultados_consolidados = {}
    
    # Processar cada tipo de extração solicitado
    for tipo in tipos_extracao:
        print(f"🔄 Realizando extração do tipo: {tipo}")
        
        # Extrair informações
        resultados = extrair_informacoes(segmentos, tipo)
        
        # Consolidar resultados
        consolidado = consolidar_resultados(resultados, metadados)
        
        # Armazenar resultado consolidado
        resultados_consolidados[tipo] = consolidado
    
    print(f"✅ Processamento concluído para: {nome_arquivo}")
    
    return resultados_consolidados

# ====================================================================
# PARTE 5: DOCUMENTO DE EXEMPLO
# ====================================================================
# Esta parte cria um documento de exemplo para demonstração.
# ====================================================================

def criar_documento_exemplo():
    """
    Cria um documento de exemplo para demonstrar o processador.
    
    Returns:
        str: Caminho para o documento criado
    """
    # Conteúdo de exemplo (um relatório simples)
    conteudo_exemplo = """
    RELATÓRIO TRIMESTRAL DE PROJETOS - Q1 2025
    
    Autor: Maria Silva
    Data: 31/03/2025
    Departamento: Tecnologia
    
    SUMÁRIO EXECUTIVO
    
    O primeiro trimestre de 2025 apresentou avanços significativos nos projetos estratégicos da SMN. 
    Alcançamos 87% das metas estabelecidas para o período, com destaque para o lançamento da plataforma SmartEco 
    que superou as expectativas iniciais de adoção pelo mercado.
    
    PROJETOS EM ANDAMENTO
    
    1. Projeto SmartEco
       Status: Lançado em 15/02/2025
       Orçamento: R$ 1.200.000,00
       Utilização: 82%
       Principais marcos:
       - Lançamento da versão 1.0 (concluído)
       - Integração com sistemas de parceiros (em andamento - 65%)
       - Expansão para mercado internacional (planejado para Q2)
    
    2. Projeto DataConnect
       Status: Em desenvolvimento
       Orçamento: R$ 850.000,00
       Utilização: 40%
       Principais marcos:
       - Finalização da arquitetura (concluído)
       - Desenvolvimento do backend (em andamento - 78%)
       - Testes de integração (previsto para início em 15/04/2025)
    
    3. Projeto GreenChain
       Status: Em fase inicial
       Orçamento: R$ 620.000,00
       Utilização: 15%
       Principais marcos:
       - Pesquisa de mercado (concluído)
       - Definição de requisitos (em andamento - 45%)
       - Prototipagem (previsto para Q2)
    
    INDICADORES FINANCEIROS
    
    Total investido no trimestre: R$ 945.000,00
    Economia gerada por otimizações: R$ 120.000,00
    ROI projetado para 2025: 23%
    
    EQUIPE E RECURSOS
    
    Total de colaboradores alocados: 34
    Novas contratações no período: 5
    Índice de satisfação da equipe: 85%
    
    DESAFIOS E RISCOS
    
    1. Atrasos na cadeia de suprimentos afetando componentes para o Projeto GreenChain
       Mitigação: Identificação de fornecedores alternativos em andamento
    
    2. Escassez de desenvolvedores especializados em IA para o Projeto DataConnect
       Mitigação: Programa de capacitação interna iniciado em fevereiro
    
    CONCLUSÕES E PRÓXIMOS PASSOS
    
    O trimestre demonstrou solidez na execução dos projetos principais, com desafios concentrados 
    principalmente em fatores externos. Para o Q2 2025, focaremos na internacionalização do SmartEco
    e na aceleração do desenvolvimento do DataConnect, com previsão de beta fechado para junho.
    
    Contatos para mais informações:
    
    Maria Silva - maria.silva@smn.com.br - (11) 98765-4321
    João Oliveira (DataConnect) - joao.oliveira@smn.com.br
    Ana Mendes (GreenChain) - ana.mendes@smn.com.br - (11) 3456-7890
    
    SMN Tecnologia
    Av. Paulista, 1000, São Paulo - SP
    contato@smn.com.br
    """
    
    # Criar arquivo temporário
    caminho_arquivo = "relatorio_exemplo.txt"
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo_exemplo)
    
    print(f"📄 Documento de exemplo criado: {caminho_arquivo}")
    
    return caminho_arquivo

# ====================================================================
# PARTE 6: INTERFACE SIMPLES
# ====================================================================
# Interface de linha de comando para interagir com o agente.
# ====================================================================

def interface_simples():
    """Interface simples para interagir com o processador de documentos."""
    print("="*70)
    print("🤖 AGENTE PROCESSADOR DE DOCUMENTOS DA SMN")
    print("="*70)
    print("Este agente extrai informações relevantes de documentos como relatórios e e-mails.")
    print("Digite o caminho para um arquivo ou 'exemplo' para usar o documento de demonstração.")
    print("Digite 'sair' para encerrar.")
    print("="*70)
    
    while True:
        entrada = input("\n📄 Caminho do arquivo (ou 'exemplo' ou 'sair'): ")
        
        if entrada.lower() == "sair":
            print("\n👋 Até a próxima!")
            break
        
        # Definir o caminho do arquivo
        if entrada.lower() == "exemplo":
            caminho_arquivo = criar_documento_exemplo()
        else:
            caminho_arquivo = entrada
        
        # Definir tipos de extração
        tipos_extracao = ["geral"]
        
        opcao = input("🔍 Deseja extrair também informações de contato? (s/n): ")
        if opcao.lower() == "s":
            tipos_extracao.append("contatos")
        
        print("\n🔄 Iniciando processamento. Isso pode levar alguns minutos dependendo do tamanho do documento...\n")
        
        try:
            # Processar o documento
            resultados = processar_documento(caminho_arquivo, tipos_extracao)
            
            # Exibir resultados
            for tipo, resultado in resultados.items():
                print(f"\n📊 RESULTADO DA EXTRAÇÃO ({tipo.upper()}):\n")
                print(resultado)
                
                # Salvar em arquivo
                nome_arquivo = f"extracao_{tipo}_{os.path.basename(caminho_arquivo)}.json"
                with open(nome_arquivo, "w", encoding="utf-8") as f:
                    f.write(resultado)
                print(f"\n✅ Resultado salvo em: {nome_arquivo}")
            
        except Exception as e:
            print(f"❌ Ocorreu um erro: {str(e)}")
            
        # Limpar arquivo de exemplo se necessário
        if entrada.lower() == "exemplo" and os.path.exists("relatorio_exemplo.txt"):
            os.remove("relatorio_exemplo.txt")
            print("\n🧹 Arquivo de exemplo removido.")

# ====================================================================
# PARTE 7: EXECUTAR O AGENTE
# ====================================================================
# Executamos a interface se este arquivo for executado diretamente.
# ====================================================================

if __name__ == "__main__":
    interface_simples()