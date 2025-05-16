# Criando Novos Agentes

🔴 **Nível: Avançado** - Este tutorial requer experiência com Python e desenvolvimento de software.

## O que você aprenderá

Neste tutorial, você aprenderá:
- Como criar um agente de IA do zero
- Como estruturar seu código para facilitar a manutenção
- Como integrar APIs e serviços externos ao seu agente
- Melhores práticas para prompts e gerenciamento de respostas

## 1. Estrutura Básica de um Agente

Todo agente de IA precisa dos seguintes componentes:

1. **Interface de Usuário**: Como o usuário interage com o agente
2. **Lógica de Processamento**: Como interpretar solicitações do usuário
3. **Modelo de IA**: Como gerar respostas inteligentes
4. **Ferramentas**: Capacidades específicas do agente (busca, análise, etc.)

## 2. Configurando o Projeto

Comece criando um novo arquivo Python para seu agente:

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Carregar variáveis de ambiente
load_dotenv()

# Configurar o modelo de IA
modelo = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def processar_solicitacao(texto_usuario):
    """Função principal para processar solicitações do usuário."""
    # Implementação básica aqui
    pass
    
def main():
    """Função principal do agente."""
    print("Bem-vindo ao seu novo agente!")
    while True:
        texto = input("👤 Você: ")
        if texto.lower() in ['sair', 'exit', 'quit']:
            break
        resposta = processar_solicitacao(texto)
        print(f"🤖 Agente: {resposta}")

if __name__ == "__main__":
    main()
```

## 3. Implementando as Ferramentas

As ferramentas são funções específicas que seu agente pode usar para realizar tarefas:

```python
def ferramenta_buscar_informacao(consulta):
    """Ferramenta para buscar informações."""
    # Implementação da busca
    return f"Resultados para: {consulta}"

def ferramenta_analisar_dados(dados):
    """Ferramenta para analisar dados."""
    # Implementação da análise
    return f"Análise dos dados: {len(dados)} itens processados"
```

## 4. Criando Prompts Eficazes

A qualidade dos prompts afeta diretamente o desempenho do seu agente:

```python
template = """
Você é um assistente especializado em {area_especialidade}.
O usuário precisa de ajuda com: {consulta_usuario}

Conhecimento relevante: {conhecimento_base}

Responda de forma {estilo} e {tom}.
"""

prompt = ChatPromptTemplate.from_template(template)

def gerar_resposta(consulta, area, conhecimento, estilo="clara", tom="profissional"):
    """Gera uma resposta usando o modelo de IA."""
    mensagens = prompt.format_messages(
        area_especialidade=area,
        consulta_usuario=consulta,
        conhecimento_base=conhecimento,
        estilo=estilo,
        tom=tom
    )
    resposta = modelo.invoke(mensagens)
    return resposta.content
```

## 5. Integrando com APIs Externas

Para adicionar funcionalidades avançadas, integre APIs externas:

```python
import requests

def obter_dados_api(endpoint, parametros=None):
    """Obtém dados de uma API externa."""
    try:
        resposta = requests.get(endpoint, params=parametros)
        resposta.raise_for_status()
        return resposta.json()
    except Exception as e:
        return f"Erro ao acessar API: {str(e)}"
```

## 6. Interface de Linha de Comando

Adicione uma interface de linha de comando para maior usabilidade:

```python
import argparse

def configurar_argumentos():
    """Configura argumentos da linha de comando."""
    parser = argparse.ArgumentParser(description='Meu Agente de IA')
    parser.add_argument('--modo', choices=['chat', 'arquivo'], default='chat',
                        help='Modo de operação (chat interativo ou leitura de arquivo)')
    parser.add_argument('--arquivo', help='Arquivo para processamento em modo arquivo')
    return parser.parse_args()

def main():
    """Função principal com suporte a argumentos."""
    args = configurar_argumentos()
    
    if args.modo == 'chat':
        # Modo de chat interativo
        print("Iniciando chat interativo...")
        while True:
            texto = input("👤 Você: ")
            if texto.lower() in ['sair', 'exit', 'quit']:
                break
            resposta = processar_solicitacao(texto)
            print(f"🤖 Agente: {resposta}")
    elif args.modo == 'arquivo' and args.arquivo:
        # Modo de processamento de arquivo
        print(f"Processando arquivo: {args.arquivo}")
        with open(args.arquivo, 'r') as f:
            conteudo = f.read()
        resposta = processar_solicitacao(conteudo)
        print(f"🤖 Resultado: {resposta}")
```

## 7. Dicas e Melhores Práticas

### Gerenciando o Contexto

- Use estruturas de dados para manter o histórico de conversas
- Implemente mecanismos para condensar históricos longos

### Tratamento de Erros

- Sempre implemente tratamento de exceções robusto
- Forneça mensagens de erro úteis para o usuário

### Testando seu Agente

- Crie casos de teste para validar diferentes cenários
- Teste com diferentes formatos de entrada e edge cases

### Otimizando Custos

- Monitore o uso de tokens para controlar custos
- Implemente caching quando apropriado

## Conclusão

Criar um agente do zero permite máxima flexibilidade e controle. Ao seguir essas diretrizes, você pode criar agentes personalizados para atender necessidades específicas do seu negócio.

## Próximos Passos

- Experimente incorporar ferramentas adicionais
- Explore técnicas avançadas como Chain of Thought e Few-Shot Learning
- Considere adicionar uma interface gráfica ou web
