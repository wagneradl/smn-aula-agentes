"""
Aplicação de exemplo que usa o agente integrado.
Esta aplicação permite interagir com múltiplos serviços através de linguagem natural.
"""

import os
import datetime
from agentes.agente_integrado import AgenteIntegrado

def formatar_evento(evento):
    """Formata um evento do Google Calendar para exibição."""
    inicio = evento['start'].get('dateTime', evento['start'].get('date'))
    fim = evento['end'].get('dateTime', evento['end'].get('date'))
    
    if 'T' in inicio:  # Formato com hora
        inicio_dt = datetime.datetime.fromisoformat(inicio.replace('Z', '+00:00'))
        inicio_str = inicio_dt.strftime("%d/%m/%Y %H:%M")
    else:  # Formato só com data
        inicio_str = inicio
    
    return f"{inicio_str} - {evento['summary']}"

def main():
    """Função principal da aplicação."""
    print("=" * 70)
    print("ASSISTENTE INTEGRADO SMN")
    print("=" * 70)
    print("Digite sua solicitação em linguagem natural, por exemplo:")
    print("- Quais são meus próximos compromissos?")
    print("- Envie uma mensagem no canal geral do time Marketing dizendo 'Reunião às 15h'")
    print("- Liste os times disponíveis no Microsoft Teams")
    print("- Crie uma tarefa para o projeto 123 com prazo para semana que vem")
    print("Digite 'sair' para encerrar.")
    print("=" * 70)
    
    # Inicializar o agente
    agente = AgenteIntegrado()
    
    while True:
        solicitacao = input("\n🤖 Digite sua solicitação: ")
        
        if solicitacao.lower() == "sair":
            print("\nAté a próxima!")
            break
        
        print("\nProcessando sua solicitação...")
        resultado = agente.processar_solicitacao(solicitacao)
        
        if resultado["sucesso"]:
            print("\n✅ Ação realizada com sucesso!")
            
            # Formatar a saída de acordo com o tipo de resultado
            if resultado["tipo"] == "eventos_calendar":
                print("\nEventos encontrados:")
                for evento in resultado["dados"]:
                    print(f"- {formatar_evento(evento)}")
            
            elif resultado["tipo"] == "evento_criado":
                evento = resultado["dados"]
                print(f"\nEvento criado: {evento['summary']}")
                print(f"Link: {evento.get('htmlLink', 'N/A')}")
            
            elif resultado["tipo"] == "canais_teams":
                print("\nCanais disponíveis:")
                for canal in resultado["dados"]:
                    print(f"- {canal.get('teamName', 'Time desconhecido')}: {canal['displayName']}")
            
            elif resultado["tipo"] == "times_teams":
                print("\nTimes disponíveis:")
                for time in resultado["dados"]:
                    print(f"- {time['displayName']} (ID: {time['id']})")
            
            elif resultado["tipo"] == "mensagem_enviada":
                print(f"\nMensagem enviada com sucesso!")
            
            elif resultado["tipo"] == "projetos":
                print(f"\nProjetos encontrados: {len(resultado['dados'])}")
                for projeto in resultado["dados"]:
                    print(f"- {projeto['nome']} ({projeto['status']})")
            
            else:
                print(f"\nTipo de resultado: {resultado['tipo']}")
                print("Dados retornados:")
                print(resultado["dados"])
        
        else:
            print(f"\n❌ Erro: {resultado['mensagem']}")

if __name__ == "__main__":
    main()