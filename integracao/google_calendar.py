"""
Módulo para interagir com o Google Calendar.
Permite listar eventos e criar novos compromissos no calendário.
"""

import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

class GoogleCalendarIntegration:
    """Classe para interagir com o Google Calendar."""
    
    def __init__(self):
        """Inicializa a integração com o Google Calendar."""
        self.creds = self._obter_credenciais()
        self.service = build('calendar', 'v3', credentials=self.creds)
    
    def _obter_credenciais(self):
        """Obtém credenciais para a API do Google."""
        # Se você já tem um refresh token
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")
        
        if client_id and client_secret and refresh_token:
            creds = Credentials(
                None,
                refresh_token=refresh_token,
                client_id=client_id,
                client_secret=client_secret,
                token_uri="https://oauth2.googleapis.com/token"
            )
            return creds
        else:
            raise ValueError("Credenciais do Google não configuradas")
    
    def listar_eventos(self, max_results=10, time_min=None, time_max=None):
        """
        Lista eventos do calendário.
        
        Args:
            max_results (int): Número máximo de eventos a retornar
            time_min (str): Limite inferior para a hora do evento (ISO format)
            time_max (str): Limite superior para a hora do evento (ISO format)
            
        Returns:
            list: Lista de eventos
        """
        # Definir período padrão se não fornecido (de agora até uma semana depois)
        agora = datetime.datetime.utcnow()
        time_min = time_min or agora.isoformat() + 'Z'  # 'Z' indica UTC
        time_max = time_max or (agora + datetime.timedelta(days=7)).isoformat() + 'Z'
        
        eventos = self.service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return eventos.get('items', [])
    
    def criar_evento(self, titulo, inicio, fim, descricao=None, participantes=None):
        """
        Cria um novo evento no calendário.
        
        Args:
            titulo (str): Título do evento
            inicio (str): Horário de início (ISO format)
            fim (str): Horário de fim (ISO format)
            descricao (str, opcional): Descrição do evento
            participantes (list, opcional): Lista de e-mails dos participantes
            
        Returns:
            dict: Evento criado
        """
        event = {
            'summary': titulo,
            'start': {
                'dateTime': inicio,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': fim,
                'timeZone': 'UTC',
            }
        }
        
        if descricao:
            event['description'] = descricao
        
        if participantes:
            event['attendees'] = [{'email': email} for email in participantes]
        
        evento_criado = self.service.events().insert(
            calendarId='primary',
            body=event,
            sendUpdates='all'  # Enviar e-mails para participantes
        ).execute()
        
        return evento_criado