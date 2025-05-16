"""
Script para testar o Agente Processador de Documentos de forma não interativa
"""

import os
import sys
import importlib.util

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_module_from_path(module_name, file_path):
    """Carrega um módulo Python a partir de um caminho de arquivo"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Não foi possível carregar o módulo {module_name} de {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def testar_processador_documentos():
    """Função para testar o Processador de Documentos"""
    print("=" * 70)
    print("TESTE DO PROCESSADOR DE DOCUMENTOS")
    print("=" * 70)
    
    try:
        # Caminho para o arquivo de exemplo
        exemplo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                "exemplos", "exemplo_processador_documentos.py")
        
        # Carregar o módulo
        exemplo_processador = load_module_from_path("exemplo_processador_documentos", exemplo_path)
        print("✅ Módulo do processador de documentos carregado com sucesso!")
        
        # Criar um documento de exemplo para processamento
        if hasattr(exemplo_processador, 'criar_documento_exemplo'):
            print("\n📄 Criando documento de exemplo para teste...")
            caminho_documento = exemplo_processador.criar_documento_exemplo()
            print(f"✅ Documento de exemplo criado: {caminho_documento}")
            
            # Testar carregamento do documento
            if hasattr(exemplo_processador, 'carregar_documento'):
                print("\n📂 Carregando documento...")
                try:
                    texto = exemplo_processador.carregar_documento(caminho_documento)
                    print(f"✅ Documento carregado com sucesso!")
                except Exception as e:
                    print(f"❌ Erro ao carregar documento: {str(e)}")
                    # Se falhar no carregamento, criar um texto simples para testar
                    texto = "Este é um texto de exemplo para teste de processamento. "
                    texto += "Contém informações sobre a SMN Tecnologia e seu diretor João Silva. "
                    texto += "O projeto tem prazo até 15/12/2025 e orçamento de R$ 150.000,00."
            else:
                # Se não houver função de carregamento, criar um texto simples
                texto = "Este é um texto de exemplo para teste de processamento. "
                texto += "Contém informações sobre a SMN Tecnologia e seu diretor João Silva. "
                texto += "O projeto tem prazo até 15/12/2025 e orçamento de R$ 150.000,00."
            
            # Testar processamento do documento
            if hasattr(exemplo_processador, 'processar_documento'):
                print("\n🔍 Processando documento...")
                try:
                    resultados = exemplo_processador.processar_documento(caminho_documento)
                    print("✅ Documento processado com sucesso!")
                    print("📋 Resultados do processamento:")
                    print(resultados)
                except Exception as e:
                    print(f"❌ Erro ao processar documento: {str(e)}")
            
            # Testar extração de informações diretamente
            if hasattr(exemplo_processador, 'extrair_informacoes'):
                print("\n🔎 Extraindo informações do texto...")
                segmentos = [texto]
                try:
                    informacoes = exemplo_processador.extrair_informacoes(segmentos)
                    print("✅ Informações extraídas com sucesso:")
                    print(informacoes)
                except Exception as e:
                    print(f"❌ Erro ao extrair informações: {str(e)}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("=" * 70)
    print("TESTE CONCLUÍDO")
    print("=" * 70)

if __name__ == "__main__":
    testar_processador_documentos()
