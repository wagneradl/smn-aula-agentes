"""
EXEMPLO DE AGENTE DE AGENDA COM GOOGLE CALENDAR
=====================================================================
Este exemplo mostra como criar um agente de IA para gerenciar sua agenda
usando o Google Calendar. O agente pode verificar eventos, criar compromissos
e fornecer resumos da sua agenda.
=====================================================================
"""

import os
import sys
import datetime
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import initialize_agent, Tool, AgentType

# Adicionar o diretório raiz ao path para importar módulos personalizados
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar a integração com o Google Calendar
from integracao.google_calendar import GoogleCalendarIntegration

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do modelo de linguagem
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class AgenteAgenda:
    """
    Agente de IA para gerenciar a agenda usando o Google Calendar.
    
    Este agente permite:
    - Verificar eventos do dia ou período específico
    - Criar novos compromissos
    - Fornecer resumos e análises da agenda
    """
    
    def __init__(self):
        """Inicializa o agente de agenda."""
        # Verificar se as configurações necessárias estão disponíveis
        self._verificar_configuracao()
        
        # Inicializar integração com o Google Calendar
        self.calendar = GoogleCalendarIntegration()
        
        # Inicializar modelo de linguagem
        self.llm = ChatOpenAI(temperature=0)
        
        # Configurar as ferramentas (tools) disponíveis para o agente
        self.tools = self._configurar_ferramentas()
        
        # Inicializar o agente
        self.agente = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )
    
    def _verificar_configuracao(self):
        """Verifica se as variáveis de ambiente necessárias estão configuradas."""
        variaveis_necessarias = [
            "OPENAI_API_KEY",
            "GOOGLE_CLIENT_ID",
            "GOOGLE_CLIENT_SECRET",
            "GOOGLE_REFRESH_TOKEN"
        ]
        
        faltando = []
        for var in variaveis_necessarias:
            if not os.getenv(var):
                faltando.append(var)
        
        if faltando:
            raise ValueError(
                f"Faltam as seguintes variáveis de ambiente: {', '.join(faltando)}. "
                "Configure-as no arquivo .env antes de continuar."
            )
    
    def _configurar_ferramentas(self) -> List[Tool]:
        """Configura as ferramentas disponíveis para o agente."""
        return [
            Tool(
                name="verificar_eventos_hoje",
                func=self._verificar_eventos_hoje,
                description="Verifica os eventos agendados para hoje"
            ),
            Tool(
                name="verificar_proximos_eventos",
                func=self._verificar_proximos_eventos,
                description="Verifica os próximos eventos agendados para os próximos dias"
            ),
            Tool(
                name="criar_compromisso",
                func=self._criar_compromisso,
                description="Cria um novo compromisso na agenda"
            ),
            Tool(
                name="resumir_semana",
                func=self._resumir_semana,
                description="Fornece um resumo dos compromissos da semana atual"
            ),
            Tool(
                name="analisar_disponibilidade",
                func=self._analisar_disponibilidade,
                description="Analisa os horários disponíveis em um determinado dia"
            )
        ]
    
    def _verificar_eventos_hoje(self) -> str:
        """Verifica os eventos agendados para hoje."""
        try:
            # Definir o período para hoje
            hoje = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            amanha = hoje + datetime.timedelta(days=1)
            
            # Formatar datas
            time_min = hoje.isoformat() + 'Z'
            time_max = amanha.isoformat() + 'Z'
            
            # Obter eventos
            eventos = self.calendar.listar_eventos(time_min=time_min, time_max=time_max)
            
            if not eventos:
                return "Não há eventos agendados para hoje."
            
            # Formatar resposta
            resposta = "Eventos de hoje:\n"
            for evento in eventos:
                inicio = evento.get('inicio', 'Horário não definido')
                titulo = evento.get('titulo', 'Sem título')
                resposta += f"- {inicio}: {titulo}\n"
            
            return resposta
        
        except Exception as e:
            return f"Erro ao verificar eventos de hoje: {str(e)}"
    
    def _verificar_proximos_eventos(self, dias: int = 7) -> str:
        """
        Verifica os próximos eventos agendados.
        
        Args:
            dias: Número de dias a considerar (padrão: 7)
        """
        try:
            # Definir o período
            agora = datetime.datetime.now()
            futuro = agora + datetime.timedelta(days=dias)
            
            # Formatar datas
            time_min = agora.isoformat() + 'Z'
            time_max = futuro.isoformat() + 'Z'
            
            # Obter eventos
            eventos = self.calendar.listar_eventos(time_min=time_min, time_max=time_max)
            
            if not eventos:
                return f"Não há eventos agendados para os próximos {dias} dias."
            
            # Organizar eventos por dia
            eventos_por_dia = {}
            for evento in eventos:
                data_hora = datetime.datetime.fromisoformat(evento['inicio'].replace('Z', '+00:00'))
                data = data_hora.strftime('%Y-%m-%d')
                
                if data not in eventos_por_dia:
                    eventos_por_dia[data] = []
                
                eventos_por_dia[data].append(evento)
            
            # Formatar resposta
            resposta = f"Próximos eventos ({dias} dias):\n"
            for data in sorted(eventos_por_dia.keys()):
                data_formatada = datetime.datetime.fromisoformat(data).strftime('%d/%m/%Y')
                resposta += f"\n{data_formatada}:\n"
                
                for evento in eventos_por_dia[data]:
                    hora = datetime.datetime.fromisoformat(evento['inicio'].replace('Z', '+00:00')).strftime('%H:%M')
                    titulo = evento.get('titulo', 'Sem título')
                    resposta += f"- {hora}: {titulo}\n"
            
            return resposta
        
        except Exception as e:
            return f"Erro ao verificar próximos eventos: {str(e)}"
    
    def _criar_compromisso(self, titulo: str, data: str, hora_inicio: str, duracao_minutos: int = 60, 
                          descricao: str = "", participantes: Optional[List[str]] = None) -> str:
        """
        Cria um novo compromisso na agenda.
        
        Args:
            titulo: Título do compromisso
            data: Data no formato DD/MM/YYYY
            hora_inicio: Hora de início no formato HH:MM
            duracao_minutos: Duração em minutos (padrão: 60)
            descricao: Descrição do compromisso
            participantes: Lista de e-mails dos participantes
        """
        try:
            # Converter data e hora para datetime
            try:
                data_obj = datetime.datetime.strptime(data, '%d/%m/%Y')
                hora_obj = datetime.datetime.strptime(hora_inicio, '%H:%M').time()
                inicio = datetime.datetime.combine(data_obj.date(), hora_obj)
                fim = inicio + datetime.timedelta(minutes=duracao_minutos)
            except ValueError:
                return "Erro: Formato de data ou hora inválido. Use DD/MM/YYYY para data e HH:MM para hora."
            
            # Formatar datas no formato ISO
            inicio_iso = inicio.isoformat()
            fim_iso = fim.isoformat()
            
            # Criar evento
            participantes_lista = participantes or []
            
            evento_id = self.calendar.criar_evento(
                titulo=titulo,
                descricao=descricao,
                inicio=inicio_iso,
                fim=fim_iso,
                participantes=participantes_lista
            )
            
            if evento_id:
                return f"Compromisso '{titulo}' criado com sucesso para {data} às {hora_inicio}."
            else:
                return "Erro ao criar compromisso."
        
        except Exception as e:
            return f"Erro ao criar compromisso: {str(e)}"
    
    def _resumir_semana(self) -> str:
        """Fornece um resumo dos compromissos da semana atual."""
        try:
            # Calcular o início e fim da semana atual
            hoje = datetime.datetime.now()
            inicio_semana = hoje - datetime.timedelta(days=hoje.weekday())
            inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
            fim_semana = inicio_semana + datetime.timedelta(days=7)
            
            # Formatar datas
            time_min = inicio_semana.isoformat() + 'Z'
            time_max = fim_semana.isoformat() + 'Z'
            
            # Obter eventos
            eventos = self.calendar.listar_eventos(time_min=time_min, time_max=time_max)
            
            if not eventos:
                return "Não há eventos agendados para esta semana."
            
            # Analisar eventos
            total_eventos = len(eventos)
            duracao_total = 0
            categorias = {}
            dias_ocupados = set()
            
            for evento in eventos:
                # Calcular duração
                inicio = datetime.datetime.fromisoformat(evento['inicio'].replace('Z', '+00:00'))
                fim = datetime.datetime.fromisoformat(evento['fim'].replace('Z', '+00:00')) if 'fim' in evento else inicio + datetime.timedelta(hours=1)
                duracao = (fim - inicio).total_seconds() / 60  # em minutos
                duracao_total += duracao
                
                # Registrar dia
                dias_ocupados.add(inicio.date())
                
                # Categorizar (simplificado - usando primeira palavra do título como categoria)
                titulo = evento.get('titulo', 'Outros')
                categoria = titulo.split()[0] if titulo else 'Outros'
                
                if categoria not in categorias:
                    categorias[categoria] = 0
                categorias[categoria] += 1
            
            # Formatar resposta
            resposta = "Resumo da semana:\n\n"
            resposta += f"Total de compromissos: {total_eventos}\n"
            resposta += f"Tempo total em reuniões: {int(duracao_total/60)} horas e {int(duracao_total%60)} minutos\n"
            resposta += f"Dias com compromissos: {len(dias_ocupados)} de 7\n\n"
            
            if categorias:
                resposta += "Distribuição por categoria:\n"
                for categoria, quantidade in sorted(categorias.items(), key=lambda x: x[1], reverse=True):
                    resposta += f"- {categoria}: {quantidade} evento(s)\n"
            
            return resposta
        
        except Exception as e:
            return f"Erro ao resumir semana: {str(e)}"
    
    def _analisar_disponibilidade(self, data: str = None) -> str:
        """
        Analisa os horários disponíveis em um determinado dia.
        
        Args:
            data: Data no formato DD/MM/YYYY (padrão: hoje)
        """
        try:
            # Definir data
            if data:
                try:
                    data_obj = datetime.datetime.strptime(data, '%d/%m/%Y')
                except ValueError:
                    return "Erro: Formato de data inválido. Use DD/MM/YYYY."
            else:
                data_obj = datetime.datetime.now()
            
            # Definir início e fim do dia
            inicio_dia = data_obj.replace(hour=8, minute=0, second=0, microsecond=0)  # Considerando dia útil 8h-18h
            fim_dia = data_obj.replace(hour=18, minute=0, second=0, microsecond=0)
            
            # Formatar datas
            time_min = inicio_dia.isoformat() + 'Z'
            time_max = fim_dia.isoformat() + 'Z'
            
            # Obter eventos
            eventos = self.calendar.listar_eventos(time_min=time_min, time_max=time_max)
            
            # Formatar eventos em blocos de tempo
            blocos_ocupados = []
            for evento in eventos:
                inicio = datetime.datetime.fromisoformat(evento['inicio'].replace('Z', '+00:00'))
                fim = datetime.datetime.fromisoformat(evento['fim'].replace('Z', '+00:00')) if 'fim' in evento else inicio + datetime.timedelta(hours=1)
                blocos_ocupados.append((inicio, fim, evento.get('titulo', 'Compromisso')))
            
            # Ordenar blocos por horário de início
            blocos_ocupados.sort(key=lambda x: x[0])
            
            # Encontrar horários disponíveis
            horarios_disponiveis = []
            hora_atual = inicio_dia
            
            for inicio, fim, _ in blocos_ocupados:
                if hora_atual < inicio:
                    horarios_disponiveis.append((hora_atual, inicio))
                hora_atual = max(hora_atual, fim)
            
            if hora_atual < fim_dia:
                horarios_disponiveis.append((hora_atual, fim_dia))
            
            # Formatar resposta
            data_formatada = data_obj.strftime('%d/%m/%Y')
            resposta = f"Disponibilidade para {data_formatada}:\n\n"
            
            if not eventos:
                resposta += "Dia completamente livre das 8h às 18h.\n"
            else:
                # Mostrar compromissos
                resposta += "Compromissos:\n"
                for inicio, fim, titulo in blocos_ocupados:
                    resposta += f"- {inicio.strftime('%H:%M')} a {fim.strftime('%H:%M')}: {titulo}\n"
                
                resposta += "\nHorários disponíveis:\n"
                if horarios_disponiveis:
                    for inicio, fim in horarios_disponiveis:
                        resposta += f"- {inicio.strftime('%H:%M')} a {fim.strftime('%H:%M')} ({int((fim-inicio).total_seconds()/60)} minutos)\n"
                else:
                    resposta += "Não há horários disponíveis neste dia.\n"
            
            return resposta
        
        except Exception as e:
            return f"Erro ao analisar disponibilidade: {str(e)}"
    
    def executar(self, consulta: str) -> str:
        """Executa uma consulta no agente de agenda."""
        try:
            resposta = self.agente.run(consulta)
            return resposta
        except Exception as e:
            return f"Erro ao processar sua solicitação: {str(e)}"

def interface_usuario():
    """Interface simples para interagir com o agente de agenda."""
    print("\n🤖 AGENTE DE AGENDA COM GOOGLE CALENDAR")
    print("=" * 70)
    print("Este agente pode ajudar você a gerenciar sua agenda usando o Google Calendar.")
    print("Você pode fazer perguntas como:")
    print("- Quais são meus compromissos de hoje?")
    print("- Agende uma reunião com a equipe amanhã às 14h")
    print("- Mostre minha disponibilidade na próxima terça-feira")
    print("- Faça um resumo da minha semana")
    print("\nDigite 'sair' para encerrar.")
    print("=" * 70)
    
    try:
        agente = AgenteAgenda()
        
        while True:
            consulta = input("\n💬 O que você gostaria de fazer? ")
            
            if consulta.lower() in ['sair', 'exit', 'quit']:
                print("\n👋 Até a próxima!")
                break
            
            print("\n🔄 Processando...")
            resposta = agente.executar(consulta)
            print(f"\n🤖 {resposta}")
    
    except ValueError as e:
        print(f"\n❌ Erro de configuração: {str(e)}")
        print("\nSiga as instruções no arquivo tutoriais/configuracao_google_calendar.md para configurar as credenciais necessárias.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    interface_usuario()
