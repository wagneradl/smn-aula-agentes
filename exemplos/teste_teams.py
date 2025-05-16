"""
Script para testar a integração com o Microsoft Teams
"""

import os
import sys
import datetime
from dotenv import load_dotenv

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integracao.teams import TeamsIntegration

def print_titulo(texto):
    """Formata um título para exibição no terminal"""
    print("\n" + "=" * 70)
    print(f" {texto} ".center(70, "="))
    print("=" * 70)

def main():
    """Função principal do script de teste"""
    print_titulo("TESTE DE INTEGRAÇÃO COM MICROSOFT TEAMS")
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Verificar configuração
    client_id = os.getenv("TEAMS_CLIENT_ID")
    client_secret = os.getenv("TEAMS_CLIENT_SECRET")
    tenant_id = os.getenv("TEAMS_TENANT_ID")
    
    if not client_id or not client_secret or not tenant_id:
        print("❌ Erro: Credenciais do Microsoft Teams não configuradas!")
        print("Por favor, configure as variáveis TEAMS_CLIENT_ID, TEAMS_CLIENT_SECRET e TEAMS_TENANT_ID no arquivo .env")
        return
    
    print("✅ Credenciais do Microsoft Teams encontradas.")
    
    # Inicializar a integração com o Teams
    try:
        print("\nConectando ao Microsoft Teams...")
        teams = TeamsIntegration()
        print("✅ Conexão estabelecida com sucesso!")
        
        # Listar times disponíveis
        print("\nObtendo lista de times...")
        times = teams.listar_times()
        
        if not times:
            print("ℹ️ Nenhum time encontrado. Verifique se o usuário tem acesso a times no Microsoft Teams.")
        else:
            print(f"✅ {len(times)} times encontrados:")
            for i, time in enumerate(times, 1):
                print(f"  {i}. {time['displayName']} (ID: {time['id']})")
            
            # Selecionar o primeiro time para testes adicionais
            time_teste = times[0]
            time_id = time_teste['id']
            print(f"\nUsando o time '{time_teste['displayName']}' para testes adicionais...")
            
            # Listar canais do time
            print("\nObtendo canais do time...")
            canais = teams.listar_canais(time_id)
            
            if not canais:
                print("ℹ️ Nenhum canal encontrado neste time.")
            else:
                print(f"✅ {len(canais)} canais encontrados:")
                for i, canal in enumerate(canais, 1):
                    print(f"  {i}. {canal['displayName']} (ID: {canal['id']})")
                
                # Para testes de envio de mensagem, você pode descomentar o código abaixo
                # e adicionar um ID de canal específico
                """
                print("\nTestando envio de mensagem...")
                canal_id = canais[0]['id']  # Use um canal específico para testes
                mensagem = "Esta é uma mensagem de teste do agente SMN"
                resultado = teams.enviar_mensagem(f"{time_id}/{canal_id}", mensagem)
                print("✅ Mensagem enviada com sucesso!")
                """
                
                # Para testes de envio de lembrete, você pode descomentar o código abaixo
                # e adicionar um ID de chat específico
                """
                print("\nTestando envio de lembrete...")
                chat_id = "ID_DO_CHAT_AQUI"  # Você precisará de um chat_id válido
                mensagem = "Lembrete de teste do agente SMN"
                amanha = datetime.datetime.now() + datetime.timedelta(days=1)
                amanha = amanha.replace(hour=10, minute=0, second=0, microsecond=0)
                resultado = teams.enviar_lembrete(chat_id, mensagem, amanha)
                print("✅ Lembrete criado com sucesso!")
                """
        
    except Exception as e:
        print(f"❌ Erro ao testar a integração com o Microsoft Teams: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    print_titulo("TESTE FINALIZADO")

if __name__ == "__main__":
    main()
