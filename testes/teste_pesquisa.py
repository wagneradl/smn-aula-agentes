"""
Script para testar o Agente de Pesquisa de forma não interativa
"""

import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar a função de pesquisa do exemplo
from exemplos.exemplo_pesquisa import pesquisar_e_sintetizar

def testar_agente_pesquisa():
    """Função para testar o Agente de Pesquisa com consultas predefinidas"""
    print("=" * 70)
    print("TESTE DO AGENTE DE PESQUISA")
    print("=" * 70)
    
    consultas_teste = [
        "Quais são os principais frameworks de desenvolvimento web?",
        "Explique o conceito de inteligência artificial"
    ]
    
    for i, consulta in enumerate(consultas_teste, 1):
        print(f"\nConsulta {i}: {consulta}")
        print("-" * 70)
        
        try:
            print(f"🔍 Pesquisando e sintetizando resposta para: '{consulta}'...\n")
            resposta = pesquisar_e_sintetizar(consulta)
            print(f"✅ Resposta: {resposta}\n")
        except Exception as e:
            print(f"❌ Erro: {str(e)}\n")
    
    print("=" * 70)
    print("TESTE CONCLUÍDO")
    print("=" * 70)

if __name__ == "__main__":
    testar_agente_pesquisa()
