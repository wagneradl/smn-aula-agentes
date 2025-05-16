"""
Módulo para interagir com o Microsoft Teams.
Permite enviar mensagens, programar lembretes e listar canais.
"""

import os
import datetime
from msgraph_core import GraphClientFactory
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv

load_dotenv()

class TeamsIntegration:
    """Classe para interagir com o Microsoft Teams via Microsoft Graph API."""
    
    def __init__(self):
        """Inicializa a integração com o Microsoft Teams."""
        client_id = os.getenv("TEAMS_CLIENT_ID")
        client_secret = os.getenv("TEAMS_CLIENT_SECRET")
        tenant_id = os.getenv("TEAMS_TENANT_ID")
        
        if not client_id or not client_secret or not tenant_id:
            raise ValueError("Credenciais do Microsoft Teams não configuradas corretamente")
        
        # Configurar a autenticação OAuth2
        self.credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        
        # Criar cliente usando o GraphClientFactory
        self.client = GraphClientFactory.create_with_credential(self.credential)
    
    def enviar_mensagem(self, canal, texto, blocos=None):
        """
        Envia uma mensagem para um canal ou chat do Microsoft Teams.
        
        Args:
            canal (str): ID do canal no formato 'team_id/channel_id' ou ID do chat
            texto (str): Texto da mensagem
            blocos (list, opcional): Cartões formatados para mensagens ricas (não usado diretamente)
            
        Returns:
            dict: Resposta da API do Microsoft Graph
        """
        try:
            # Determinar se estamos enviando para um chat ou canal
            if '/' in canal:
                # É um canal (formato: team_id/channel_id)
                team_id, channel_id = canal.split('/')
                
                # Criar mensagem para o canal
                message = {
                    "body": {
                        "content": texto,
                        "contentType": "text"
                    }
                }
                
                # Enviar para o canal
                resultado = self.client.post(
                    f'/teams/{team_id}/channels/{channel_id}/messages',
                    json=message
                )
                
            else:
                # É um chat direto (formato: chat_id)
                message = {
                    "body": {
                        "content": texto,
                        "contentType": "text"
                    }
                }
                
                # Enviar para o chat
                resultado = self.client.post(
                    f'/chats/{canal}/messages',
                    json=message
                )
            
            return resultado.json()
            
        except Exception as e:
            print(f"Erro ao enviar mensagem para o Teams: {str(e)}")
            raise
    
    def enviar_lembrete(self, usuario, texto, timestamp):
        """
        Cria um lembrete usando mensagem agendada no MS Teams.
        
        Args:
            usuario (str): ID do usuário ou ID do chat
            texto (str): Texto do lembrete
            timestamp (str): Data/hora para o lembrete (formato "2023-12-31 14:30")
            
        Returns:
            dict: Resposta da API do Microsoft Graph
        """
        try:
            # Converter timestamp para formato ISO
            if isinstance(timestamp, str):
                # Assumir formato "YYYY-MM-DD HH:MM"
                dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
            else:
                dt = timestamp
                
            scheduled_datetime = dt.isoformat() + 'Z'  # Formato ISO8601
            
            # Criar mensagem com lembrete
            message = {
                "body": {
                    "content": f"⏰ LEMBRETE: {texto}",
                    "contentType": "text"
                },
                "scheduledDateTime": scheduled_datetime
            }
            
            # Enviar como mensagem agendada para o chat com o usuário
            resultado = self.client.post(
                f'/chats/{usuario}/messages',
                json=message
            )
            
            return resultado.json()
            
        except Exception as e:
            print(f"Erro ao programar lembrete no Teams: {str(e)}")
            raise
    
    def listar_canais(self, team_id=None):
        """
        Lista todos os canais de um time específico ou de todos os times.
        
        Args:
            team_id (str, opcional): ID do time específico
            
        Returns:
            list: Lista de canais
        """
        try:
            canais = []
            
            if team_id:
                # Listar canais de um time específico
                response = self.client.get(f'/teams/{team_id}/channels')
                canais = response.json().get('value', [])
            else:
                # Listar todos os times primeiro
                response = self.client.get('/me/joinedTeams')
                times = response.json().get('value', [])
                
                # Para cada time, obter seus canais
                for time in times:
                    time_id = time['id']
                    time_name = time['displayName']
                    
                    channels_response = self.client.get(f'/teams/{time_id}/channels')
                    time_canais = channels_response.json().get('value', [])
                    
                    # Adicionar o nome do time a cada canal para facilitar a identificação
                    for canal in time_canais:
                        canal['teamName'] = time_name
                        canal['teamId'] = time_id
                    
                    canais.extend(time_canais)
            
            return canais
            
        except Exception as e:
            print(f"Erro ao listar canais do Teams: {str(e)}")
            raise
    
    def obter_id_canal(self, team_id, nome_canal):
        """
        Obtém o ID de um canal pelo nome.
        
        Args:
            team_id (str): ID do time
            nome_canal (str): Nome do canal
            
        Returns:
            str: ID do canal
        """
        try:
            canais = self.listar_canais(team_id)
            
            for canal in canais:
                if canal['displayName'].lower() == nome_canal.lower():
                    return canal['id']
            
            raise ValueError(f"Canal '{nome_canal}' não encontrado no time {team_id}")
            
        except Exception as e:
            print(f"Erro ao obter ID do canal: {str(e)}")
            raise
            
    def listar_times(self):
        """
        Lista todos os times que o usuário autenticado participa.
        
        Returns:
            list: Lista de times
        """
        try:
            response = self.client.get('/me/joinedTeams')
            return response.json().get('value', [])
            
        except Exception as e:
            print(f"Erro ao listar times: {str(e)}")
            raise
