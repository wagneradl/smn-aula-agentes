"""
Script para testar a integração com o Google Calendar
"""

import os
import sys
import datetime
import importlib.util

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar módulos necessários
from dotenv import load_dotenv

def load_module_from_path(module_name, file_path):
    """Carrega um módulo Python a partir de um caminho de arquivo"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Não foi possível carregar o módulo {module_name} de {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def testar_google_calendar():
    """Função para testar a integração com o Google Calendar"""
    print("=" * 70)
    print("TESTE DE INTEGRAÇÃO COM GOOGLE CALENDAR")
    print("=" * 70)
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Verificar configurações necessárias
    variaveis_necessarias = [
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_SECRET",
        "GOOGLE_REFRESH_TOKEN"
    ]
    
    faltando = []
    for var in variaveis_necessarias:
        if not os.getenv(var):
            faltando.append(var)
    
    if faltando:
        print("⚠️  As seguintes variáveis de ambiente estão faltando:")
        for var in faltando:
            print(f"   - {var}")
        print("\n⚙️  Para configurar, siga os passos:")
        print("   1. Crie um projeto no Google Cloud Console (https://console.cloud.google.com/)")
        print("   2. Ative a API do Google Calendar")
        print("   3. Configure a tela de consentimento OAuth")
        print("   4. Crie credenciais OAuth 2.0 para aplicativo de desktop")
        print("   5. Baixe o arquivo JSON e salve-o como client_secret.json")
        print("   6. Execute o script: python integracao/obter_token_google.py")
        print("   7. Adicione as credenciais obtidas ao seu arquivo .env")
        print("\n⏭️  Pulando os testes de integração com o Google Calendar")
        return
    
    try:
        # Importar a integração com o Google Calendar
        from integracao.google_calendar import GoogleCalendarIntegration
        
        print("✅ Módulo GoogleCalendarIntegration importado com sucesso!")
        
        # Testar inicialização da classe de integração
        print("\n🔄 Inicializando conexão com o Google Calendar...")
        try:
            calendar = GoogleCalendarIntegration()
            print("✅ Conexão estabelecida com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao inicializar a conexão: {str(e)}")
            print("⚠️  Verifique se as credenciais estão corretas e se tem acesso à API")
            return
        
        # Testar listagem de eventos
        print("\n🔄 Testando listagem de eventos...")
        try:
            # Definir período para os próximos 30 dias
            agora = datetime.datetime.now()
            futuro = agora + datetime.timedelta(days=30)
            
            # Formatar datas no formato ISO
            time_min = agora.isoformat() + 'Z'
            time_max = futuro.isoformat() + 'Z'
            
            # Listar eventos
            eventos = calendar.listar_eventos(
                max_results=5,
                time_min=time_min,
                time_max=time_max
            )
            
            print(f"✅ Listagem de eventos concluída! Encontrados: {len(eventos)} eventos")
            
            # Mostrar detalhes dos eventos encontrados
            if eventos:
                print("\n📅 DETALHES DOS EVENTOS:")
                print("-" * 50)
                for i, evento in enumerate(eventos[:3], 1):  # Mostrar até 3 eventos
                    inicio = evento.get('inicio', 'Horário não definido')
                    titulo = evento.get('titulo', 'Sem título')
                    print(f"Evento {i}: {inicio} - {titulo}")
                
                if len(eventos) > 3:
                    print(f"... e mais {len(eventos) - 3} evento(s)")
        except Exception as e:
            print(f"❌ Erro ao listar eventos: {str(e)}")
        
        # Testar criação de evento
        print("\n🔄 Testando criação de evento de teste...")
        try:
            # Definir data e hora para o evento (amanhã às 10h)
            amanha = datetime.datetime.now() + datetime.timedelta(days=1)
            inicio = amanha.replace(hour=10, minute=0, second=0, microsecond=0)
            fim = inicio + datetime.timedelta(hours=1)
            
            # Detalhes do evento
            titulo = f"Evento de Teste API - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
            descricao = "Este é um evento automático criado pelo script de teste de integração"
            
            # Verificar o email do usuário no ambiente ou usar um valor padrão
            email_usuario = os.getenv("USER_EMAIL", "seu_email@example.com")
            participantes = [email_usuario]
            
            print(f"📝 Criando evento: '{titulo}'")
            evento_id = calendar.criar_evento(
                titulo=titulo,
                descricao=descricao,
                inicio=inicio.isoformat(),
                fim=fim.isoformat(),
                participantes=participantes
            )
            
            if evento_id:
                print(f"✅ Evento criado com sucesso! ID: {evento_id}")
                
                # Testar exclusão do evento (opcional - comentado para não excluir por padrão)
                # print("\n🔄 Testando exclusão do evento...")
                # if calendar.excluir_evento(evento_id):
                #     print("✅ Evento excluído com sucesso!")
                # else:
                #     print("❌ Falha ao excluir evento")
            else:
                print("❌ Falha ao criar evento")
        except Exception as e:
            print(f"❌ Erro ao criar evento: {str(e)}")
        
        print("\n✅ Testes de integração com o Google Calendar concluídos!")
    
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {str(e)}")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("=" * 70)
    print("TESTE CONCLUÍDO")
    print("=" * 70)

if __name__ == "__main__":
    testar_google_calendar()
