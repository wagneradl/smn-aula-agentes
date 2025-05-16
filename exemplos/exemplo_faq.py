# ====================================================================
# AGENTE DE ATENDIMENTO A DÚVIDAS FREQUENTES
# ====================================================================
# Este agente responde a perguntas comuns usando uma base de conhecimento simples.
# É útil para fornecer respostas rápidas sobre políticas, processos ou informações
# da empresa sem precisar consultar um humano.
# ====================================================================

# Importamos as bibliotecas necessárias
# (estas precisam ser instaladas usando pip, conforme instruções em configuracao/README.md)
import os
from dotenv import load_dotenv  # Para carregar as variáveis de ambiente
from langchain_openai import ChatOpenAI  # Modelo de linguagem para conversa
from langchain.prompts import ChatPromptTemplate  # Para criar prompts estruturados
from langchain_community.vectorstores import FAISS  # Para armazenar e buscar informações
from langchain_openai import OpenAIEmbeddings  # Para converter texto em números que o computador entende
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Para dividir documentos grandes
from langchain_community.document_loaders import TextLoader  # Para carregar documentos de texto

# Carregar configurações do arquivo .env
load_dotenv()

# Chaves de API (nunca compartilhe estas chaves!)
# Você precisa obter sua própria chave em https://platform.openai.com/api-keys
# e colocá-la no arquivo .env conforme explicado em configuracao/.env.exemplo
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ====================================================================
# PARTE 1: BASE DE CONHECIMENTO
# ====================================================================
# Esta é a base de conhecimento do seu agente. Em um sistema real, 
# isso poderia vir de documentos da empresa, mas para este exemplo
# usaremos algumas informações diretamente no código.
# ====================================================================

# Informações de exemplo da SMN (substitua por informações reais da sua organização)
conhecimento = """
# Políticas de Férias da SMN

- Os funcionários têm direito a 30 dias de férias por ano após 12 meses de trabalho.
- As férias devem ser solicitadas com pelo menos 30 dias de antecedência.
- O sistema para solicitar férias é o Portal RH, acessível em https://rh.smn.com.br
- É possível vender até 10 dias de férias.
- Dúvidas sobre férias devem ser enviadas para o e-mail ferias@smn.com.br

# Política de Home Office

- Os funcionários podem trabalhar remotamente até 3 dias por semana.
- Os dias de trabalho remoto devem ser acordados com o gestor direto.
- Reuniões importantes sempre ocorrem às terças-feiras, quando todos devem estar presencialmente.
- Para trabalhar remotamente, é necessário ter uma conexão estável e equipamentos adequados.

# Reembolso de Despesas

- Despesas de viagem a trabalho são reembolsáveis mediante apresentação de notas fiscais.
- O prazo para solicitar reembolso é de até 7 dias após o retorno da viagem.
- O reembolso é processado em até 10 dias úteis.
- O formulário de reembolso está disponível no Portal RH.
"""

# Salvamos a base de conhecimento em um arquivo temporário
with open("conhecimento_temp.txt", "w", encoding="utf-8") as f:
    f.write(conhecimento)

# ====================================================================
# PARTE 2: PREPARAÇÃO DA BASE DE CONHECIMENTO
# ====================================================================
# Aqui, transformamos o texto em um formato que o agente pode usar
# para encontrar rapidamente as informações relevantes.
# ====================================================================

# Carregar o documento
loader = TextLoader("conhecimento_temp.txt", encoding="utf-8")
documentos = loader.load()

# Dividir o documento em pedaços menores para facilitar a busca
divisor_texto = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
textos = divisor_texto.split_documents(documentos)

# Criar embeddings (representações numéricas do texto)
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Criar a base de conhecimento vetorial
base_conhecimento = FAISS.from_documents(textos, embeddings)

# ====================================================================
# PARTE 3: CONFIGURAÇÃO DO AGENTE
# ====================================================================
# Configuramos o modelo de linguagem e definimos como ele deve 
# formatar as respostas.
# ====================================================================

# Inicializar o modelo de linguagem
modelo = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")

# Template para o prompt (instrução) que será enviado ao modelo
template_prompt = """
Você é um assistente de atendimento da SMN, especializado em responder perguntas 
sobre as políticas e procedimentos da empresa. Seja educado, conciso e direto.

Informações relevantes da base de conhecimento:
{contexto}

Pergunta do funcionário: {pergunta}

Sua resposta (use apenas as informações fornecidas acima, seja breve e direto):
"""

prompt = ChatPromptTemplate.from_template(template_prompt)

# ====================================================================
# PARTE 4: FUNÇÃO PRINCIPAL DO AGENTE
# ====================================================================
# Esta função é o coração do agente - ela recebe uma pergunta, busca 
# informações relevantes, e gera uma resposta.
# ====================================================================

def responder_pergunta(pergunta):
    """
    Função principal do agente que responde a perguntas com base na base de conhecimento.
    
    Args:
        pergunta (str): A pergunta do usuário
        
    Returns:
        str: A resposta gerada pelo agente
    """
    # Passo 1: Buscar documentos relevantes para a pergunta
    documentos_relevantes = base_conhecimento.similarity_search(pergunta, k=3)
    
    # Passo 2: Extrair o conteúdo dos documentos
    contexto = "\n\n".join([doc.page_content for doc in documentos_relevantes])
    
    # Passo 3: Criar o prompt com o contexto e a pergunta
    mensagens = prompt.format_messages(contexto=contexto, pergunta=pergunta)
    
    # Passo 4: Gerar a resposta usando o modelo de linguagem
    resposta = modelo.invoke(mensagens)
    
    return resposta.content

# ====================================================================
# PARTE 5: INTERFACE SIMPLES PARA TESTAR O AGENTE
# ====================================================================
# Uma interface de linha de comando para interagir com o agente.
# ====================================================================

def interface_simples():
    """Interface de linha de comando para interagir com o agente."""
    print("="*70)
    print("🤖 AGENTE DE ATENDIMENTO A DÚVIDAS FREQUENTES DA SMN")
    print("="*70)
    print("Faça perguntas sobre políticas da empresa, como férias, home office, etc.")
    print("Digite 'sair' para encerrar.")
    print("="*70)
    
    while True:
        pergunta = input("\n💬 Sua pergunta: ")
        
        if pergunta.lower() == "sair":
            print("\n👋 Até a próxima!")
            break
        
        print("\n🤖 Buscando resposta...\n")
        try:
            resposta = responder_pergunta(pergunta)
            print(f"🔹 {resposta}\n")
        except Exception as e:
            print(f"❌ Ocorreu um erro: {str(e)}\n")
            print("Por favor, verifique sua conexão com a internet e a configuração da API.")

# ====================================================================
# PARTE 6: EXECUTAR O AGENTE
# ====================================================================
# Executamos a interface se este arquivo for executado diretamente.
# ====================================================================

if __name__ == "__main__":
    interface_simples()
    
    # Limpeza do arquivo temporário
    if os.path.exists("conhecimento_temp.txt"):
        os.remove("conhecimento_temp.txt")