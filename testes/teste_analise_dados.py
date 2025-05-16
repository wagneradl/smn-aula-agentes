"""
Script para testar o Agente de Análise de Dados de forma não interativa
"""

import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar o exemplo de análise de dados
# Vamos importar apenas o que precisamos para testar
import importlib.util
import types

def load_module_from_path(module_name, file_path):
    """Carrega um módulo Python a partir de um caminho de arquivo"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Não foi possível carregar o módulo {module_name} de {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def testar_agente_analise_dados():
    """Função para testar o Agente de Análise de Dados"""
    print("=" * 70)
    print("TESTE DO AGENTE DE ANÁLISE DE DADOS")
    print("=" * 70)
    
    # Caminho para o arquivo de exemplo
    exemplo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              "exemplos", "exemplo_analise_dados.py")
    
    # Carregar o módulo
    try:
        # Importar as funções necessárias do módulo
        exemplo_analise = load_module_from_path("exemplo_analise_dados", exemplo_path)
        
        # Verificar se conseguimos carregar o módulo
        print("✅ Módulo de análise de dados carregado com sucesso!")
        
        # Vamos testar a geração de um dataset de exemplo
        print("\n📊 Gerando dataset de exemplo...")
        
        # Muitas das funções no exemplo provavelmente dependem de interação do usuário
        # Vamos tentar executar funções específicas que não dependam de input
        
        # Usar o dataframe que já é criado no exemplo
        df_vendas = exemplo_analise.df_vendas
        print(f"✅ Dataset encontrado com {len(df_vendas)} linhas e {len(df_vendas.columns)} colunas")
        print(f"   Colunas: {', '.join(df_vendas.columns.tolist())}")
        
        # Mostrar as primeiras linhas do dataset
        print("\n📋 Primeiras linhas do dataset:")
        print(df_vendas.head().to_string())
        
        # Testar estatísticas descritivas
        print("\n📈 Estatísticas descritivas:")
        print(df_vendas.describe().to_string())
        
        # Testar função de resumo estatístico se disponível
        if hasattr(exemplo_analise, 'resumo_estatistico'):
            print("\n📊 Gerando resumo estatístico...")
            resumo = exemplo_analise.resumo_estatistico(df_vendas)
            print(resumo)
        
        # Testar a função de análise de dados
        if hasattr(exemplo_analise, 'analisar_dados'):
            print("\n🔍 Executando análise exploratória...")
            resultado_analise = exemplo_analise.analisar_dados(df=df_vendas)
            print(f"✅ Análise exploratória concluída!")
            if resultado_analise:
                print(f"   Resultado: {resultado_analise}")
                
            # Testar geração de insights se disponível
            if hasattr(exemplo_analise, 'gerar_insights'):
                print("\n💡 Gerando insights com IA...")
                insights = exemplo_analise.gerar_insights(df_vendas)
                print(f"✅ Insights gerados:\n{insights}")
        else:
            print("❌ Função analisar_dados não encontrada no módulo")
    
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("=" * 70)
    print("TESTE CONCLUÍDO")
    print("=" * 70)

if __name__ == "__main__":
    testar_agente_analise_dados()
