"""
Agente integrado que combina múltiplas fontes de dados.
Este agente pode interagir com Google Calendar, Microsoft Teams e sistemas internos.
"""

import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

from integracao.google_calendar import GoogleCalendarIntegration
from integracao.teams import TeamsIntegration
from integracao.api_interna import APIInterna

load_dotenv()

class AgenteIntegrado:
    """
    Agente que integra múltiplos serviços para fornecer assistência completa.
    """
    
    def __init__(self):
        """Inicializa o agente integrado."""
        # Inicializar o modelo de linguagem
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo", 
            temperature=0.2,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Inicializar integrações
        try:
            self.calendar = GoogleCalendarIntegration()
            self.teams = TeamsIntegration()
            self.api = APIInterna()
            
            self.servicos_disponiveis = ["calendar", "teams", "api_interna"]
        except Exception as e:
            print(f"Aviso: Nem todas as integrações estão disponíveis - {str(e)}")
            self.servicos_disponiveis = []
        
        # Configurar o chain para processamento de linguagem natural
        self.chain = LLMChain(
            llm=self.llm,
            prompt=ChatPromptTemplate.from_template(
                """
                Você é um assistente que ajuda a entender solicitações e determinar quais ações tomar.
                
                Baseado na solicitação abaixo, identifique:
                1. Qual serviço deve ser utilizado (calendar, teams, api_interna)
                2. Qual ação deve ser realizada
                3. Quais parâmetros são necessários
                
                Formate sua resposta como um JSON com os campos:
                - servico: o nome do serviço a ser usado
                - acao: a ação a ser realizada
                - parametros: um objeto com os parâmetros necessários
                
                Solicitação: {solicitacao}
                
                Resposta:
                """
            )
        )
    
    def processar_solicitacao(self, solicitacao):
        """
        Processa uma solicitação em linguagem natural e executa a ação apropriada.
        
        Args:
            solicitacao (str): Solicitação em linguagem natural
            
        Returns:
            dict: Resultados da ação
        """
        # Verificar se temos integrações disponíveis
        if not self.servicos_disponiveis:
            return {
                "sucesso": False,
                "mensagem": "Nenhuma integração está configurada. Verifique as credenciais."
            }
        
        # Usar o LLM para entender a solicitação
        resposta = self.chain.run(solicitacao=solicitacao)
        
        try:
            # Converter a resposta do LLM para um objeto
            instrucoes = json.loads(resposta)
            
            servico = instrucoes.get("servico")
            acao = instrucoes.get("acao")
            parametros = instrucoes.get("parametros", {})
            
            # Executar a ação apropriada
            if servico == "calendar":
                return self._executar_acao_calendar(acao, parametros)
            elif servico == "teams":
                return self._executar_acao_teams(acao, parametros)
            elif servico == "api_interna":
                return self._executar_acao_api(acao, parametros)
            else:
                return {
                    "sucesso": False,
                    "mensagem": f"Serviço desconhecido: {servico}"
                }
        
        except json.JSONDecodeError:
            return {
                "sucesso": False,
                "mensagem": "Erro ao processar a resposta do modelo"
            }
        
        except Exception as e:
            return {
                "sucesso": False,
                "mensagem": f"Erro ao executar ação: {str(e)}"
            }
    
    def _executar_acao_calendar(self, acao, parametros):
        """Executa uma ação no Google Calendar."""
        if acao == "listar_eventos":
            max_results = parametros.get("max_results", 10)
            time_min = parametros.get("time_min")
            time_max = parametros.get("time_max")
            
            eventos = self.calendar.listar_eventos(max_results, time_min, time_max)
            
            return {
                "sucesso": True,
                "tipo": "eventos_calendar",
                "dados": eventos
            }
        
        elif acao == "criar_evento":
            titulo = parametros.get("titulo")
            inicio = parametros.get("inicio")
            fim = parametros.get("fim")
            descricao = parametros.get("descricao")
            participantes = parametros.get("participantes")
            
            evento = self.calendar.criar_evento(titulo, inicio, fim, descricao, participantes)
            
            return {
                "sucesso": True,
                "tipo": "evento_criado",
                "dados": evento
            }
        
        else:
            return {
                "sucesso": False,
                "mensagem": f"Ação desconhecida para Calendar: {acao}"
            }
    
    def _executar_acao_teams(self, acao, parametros):
        """Executa uma ação no Microsoft Teams."""
        if acao == "enviar_mensagem":
            canal = parametros.get("canal")
            texto = parametros.get("texto")
            
            resultado = self.teams.enviar_mensagem(canal, texto)
            
            return {
                "sucesso": True,
                "tipo": "mensagem_enviada",
                "dados": resultado
            }
        
        elif acao == "listar_canais":
            team_id = parametros.get("team_id", None)
            canais = self.teams.listar_canais(team_id)
            
            return {
                "sucesso": True,
                "tipo": "canais_teams",
                "dados": canais
            }
        
        elif acao == "listar_times":
            times = self.teams.listar_times()
            
            return {
                "sucesso": True,
                "tipo": "times_teams",
                "dados": times
            }
        
        elif acao == "enviar_lembrete":
            usuario = parametros.get("usuario")
            texto = parametros.get("texto")
            timestamp = parametros.get("timestamp")
            
            resultado = self.teams.enviar_lembrete(usuario, texto, timestamp)
            
            return {
                "sucesso": True,
                "tipo": "lembrete_enviado",
                "dados": resultado
            }
        
        else:
            return {
                "sucesso": False,
                "mensagem": f"Ação desconhecida para Microsoft Teams: {acao}"
            }
    
    def _executar_acao_api(self, acao, parametros):
        """Executa uma ação na API interna."""
        if acao == "buscar_projetos":
            status = parametros.get("status")
            departamento = parametros.get("departamento")
            
            projetos = self.api.buscar_projetos(status, departamento)
            
            return {
                "sucesso": True,
                "tipo": "projetos",
                "dados": projetos
            }
        
        elif acao == "buscar_funcionario":
            id_funcionario = parametros.get("id")
            email = parametros.get("email")
            
            funcionario = self.api.buscar_funcionario(id_funcionario, email)
            
            return {
                "sucesso": True,
                "tipo": "funcionario",
                "dados": funcionario
            }
        
        elif acao == "registrar_tarefa":
            projeto_id = parametros.get("projeto_id")
            titulo = parametros.get("titulo")
            descricao = parametros.get("descricao")
            responsavel_id = parametros.get("responsavel_id")
            prazo = parametros.get("prazo")
            
            tarefa = self.api.registrar_tarefa(
                projeto_id, titulo, descricao, responsavel_id, prazo
            )
            
            return {
                "sucesso": True,
                "tipo": "tarefa_criada",
                "dados": tarefa
            }
        
        else:
            return {
                "sucesso": False,
                "mensagem": f"Ação desconhecida para API Interna: {acao}"
            }