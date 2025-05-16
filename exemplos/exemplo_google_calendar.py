"""
EXEMPLO DE INTEGRAÇÃO COM GOOGLE CALENDAR
=====================================================================
Este exemplo demonstra como usar a integração com o Google Calendar
para listar eventos e criar novos compromissos.
=====================================================================
"""

import os
import sys
import datetime
from dotenv import load_dotenv

# Adicionar o diretório raiz ao path para importar módulos personalizados
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar a integração com o Google Calendar
from integracao.google_calendar import GoogleCalendarIntegration

# Carregar variáveis de ambiente
load_dotenv()

def verificar_configuracao():
    """Verifica se as variáveis de ambiente necessárias estão configuradas."""
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
        print("\n⚙️  Configure-as no arquivo .env antes de continuar.")
        return False
    
    return True

def listar_eventos_hoje():
    """Lista os eventos do calendário para o dia atual."""
    try:
        # Inicializar a integração com o Google Calendar
        calendar = GoogleCalendarIntegration()
        
        # Definir o período para hoje
        hoje = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        amanha = hoje + datetime.timedelta(days=1)
        
        # Formatar datas no formato ISO
        time_min = hoje.isoformat() + 'Z'  # 'Z' indica UTC
        time_max = amanha.isoformat() + 'Z'
        
        # Listar eventos
        print("\n📅 EVENTOS DE HOJE:")
        print("=" * 50)
        
        eventos = calendar.listar_eventos(
            max_results=10,
            time_min=time_min,
            time_max=time_max
        )
        
        if not eventos:
            print("Nenhum evento encontrado para hoje.")
        else:
            for evento in eventos:
                inicio = evento.get('inicio', 'Horário não definido')
                titulo = evento.get('titulo', 'Sem título')
                participantes = evento.get('participantes', [])
                
                print(f"⏰ {inicio} - {titulo}")
                if participantes:
                    print(f"   👥 Participantes: {', '.join(participantes)}")
                print("-" * 50)
    
    except Exception as e:
        print(f"❌ Erro ao listar eventos: {str(e)}")

def criar_evento_exemplo():
    """Cria um evento de exemplo no calendário."""
    try:
        # Inicializar a integração com o Google Calendar
        calendar = GoogleCalendarIntegration()
        
        # Definir data e hora para o evento (amanhã às 15h)
        amanha = datetime.datetime.now() + datetime.timedelta(days=1)
        inicio = amanha.replace(hour=15, minute=0, second=0, microsecond=0)
        fim = inicio + datetime.timedelta(hours=1)
        
        # Criar o evento
        titulo = "Reunião de Teste - API Calendar"
        descricao = "Este é um evento de teste criado pela integração com o Google Calendar"
        local = "Sala de Reuniões Virtual"
        participantes = ["seuemail@gmail.com"]  # Adicione seu email aqui
        
        evento_id = calendar.criar_evento(
            titulo=titulo,
            descricao=descricao,
            inicio=inicio.isoformat(),
            fim=fim.isoformat(),
            local=local,
            participantes=participantes
        )
        
        if evento_id:
            print("\n✅ EVENTO CRIADO COM SUCESSO:")
            print("=" * 50)
            print(f"🏷️  Título: {titulo}")
            print(f"📝 Descrição: {descricao}")
            print(f"🕒 Início: {inicio.strftime('%d/%m/%Y %H:%M')}")
            print(f"🕓 Fim: {fim.strftime('%d/%m/%Y %H:%M')}")
            print(f"📍 Local: {local}")
            print(f"👥 Participantes: {', '.join(participantes)}")
            print(f"🔑 ID do Evento: {evento_id}")
        else:
            print("❌ Falha ao criar o evento")
    
    except Exception as e:
        print(f"❌ Erro ao criar evento: {str(e)}")

def listar_proximos_eventos():
    """Lista os próximos eventos do calendário."""
    try:
        # Inicializar a integração com o Google Calendar
        calendar = GoogleCalendarIntegration()
        
        # Definir período para os próximos 7 dias
        agora = datetime.datetime.now()
        proxima_semana = agora + datetime.timedelta(days=7)
        
        # Formatar datas no formato ISO
        time_min = agora.isoformat() + 'Z'
        time_max = proxima_semana.isoformat() + 'Z'
        
        # Listar eventos
        print("\n📅 PRÓXIMOS EVENTOS (7 DIAS):")
        print("=" * 50)
        
        eventos = calendar.listar_eventos(
            max_results=10,
            time_min=time_min,
            time_max=time_max
        )
        
        if not eventos:
            print("Nenhum evento encontrado para os próximos 7 dias.")
        else:
            for evento in eventos:
                inicio = evento.get('inicio', 'Horário não definido')
                titulo = evento.get('titulo', 'Sem título')
                participantes = evento.get('participantes', [])
                
                print(f"⏰ {inicio} - {titulo}")
                if participantes:
                    print(f"   👥 Participantes: {', '.join(participantes)}")
                print("-" * 50)
    
    except Exception as e:
        print(f"❌ Erro ao listar eventos: {str(e)}")

def interface_usuario():
    """Interface simples para interagir com a integração do Google Calendar."""
    while True:
        print("\n🗓️  INTEGRAÇÃO COM GOOGLE CALENDAR")
        print("=" * 50)
        print("1. Listar eventos de hoje")
        print("2. Listar próximos eventos (7 dias)")
        print("3. Criar evento de teste")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            listar_eventos_hoje()
        elif opcao == "2":
            listar_proximos_eventos()
        elif opcao == "3":
            criar_evento_exemplo()
        elif opcao == "0":
            print("\n👋 Até a próxima!")
            break
        else:
            print("❌ Opção inválida!")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    print("\n🗓️  EXEMPLO DE INTEGRAÇÃO COM GOOGLE CALENDAR")
    print("=" * 70)
    
    if verificar_configuracao():
        print("✅ Configuração verificada com sucesso!")
        interface_usuario()
    else:
        print("\n❌ Configure as variáveis de ambiente no arquivo .env antes de continuar.")
        print("   Siga as instruções no arquivo README.md ou execute:")
        print("   python integracao/obter_token_google.py")
