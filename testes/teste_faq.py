"""
Script para testar o Agente FAQ de forma não interativa
"""

import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exemplos.exemplo_faq import responder_pergunta

def testar_agente_faq():
    """Função para testar o Agente FAQ com perguntas predefinidas"""
    print("=" * 70)
    print("TESTE DO AGENTE FAQ")
    print("=" * 70)
    
    perguntas_teste = [
        "Qual é a política de férias da empresa?",
        "Como funciona o home office?",
        "Quais são os benefícios oferecidos?"
    ]
    
    for i, pergunta in enumerate(perguntas_teste, 1):
        print(f"\nPergunta {i}: {pergunta}")
        print("-" * 70)
        
        try:
            resposta = responder_pergunta(pergunta)
            print(f"✅ Resposta: {resposta}\n")
        except Exception as e:
            print(f"❌ Erro: {str(e)}\n")
    
    print("=" * 70)
    print("TESTE CONCLUÍDO")
    print("=" * 70)

if __name__ == "__main__":
    testar_agente_faq()
