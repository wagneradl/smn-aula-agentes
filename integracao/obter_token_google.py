"""
Utilitário para obter tokens OAuth para o Google Calendar.
Este script facilita a obtenção do refresh_token necessário para a integração.
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import json

# Escopos necessários para o Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def obter_credenciais_google():
    """
    Obtém credenciais OAuth para o Google Calendar.
    Gera os tokens necesários e salva em um arquivo para uso futuro.
    
    Returns:
        Credentials: Objeto de credenciais do Google
    """
    creds = None
    
    # Tentar carregar credenciais do arquivo token.pickle
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Se não houver credenciais válidas, faça login ou atualize
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Carregar credenciais do cliente do arquivo client_secret.json
            if not os.path.exists('client_secret.json'):
                print("Você precisa baixar o arquivo client_secret.json do Google Cloud Console.")
                print("1. Acesse https://console.cloud.google.com/")
                print("2. Crie um projeto e ative a API do Google Calendar")
                print("3. Configure a tela de consentimento OAuth")
                print("4. Crie credenciais OAuth 2.0 para aplicativo de desktop")
                print("5. Baixe o arquivo JSON e salve-o como client_secret.json neste diretório")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Salvar as credenciais para a próxima execução
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        
        # Exibir informações importantes para .env
        print("\n\n" + "="*50)
        print("INFORMAÇÕES PARA SEU ARQUIVO .env:")
        print("="*50)
        print(f"GOOGLE_CLIENT_ID={creds.client_id}")
        print(f"GOOGLE_CLIENT_SECRET={creds.client_secret}")
        print(f"GOOGLE_REFRESH_TOKEN={creds.refresh_token}")
        print("="*50)
        print("\nCopie estas informações para seu arquivo .env")
    
    return creds

def testar_credenciais():
    """Testa as credenciais do Google Calendar."""
    from googleapiclient.discovery import build
    
    creds = obter_credenciais_google()
    if not creds:
        return
    
    try:
        # Construir o serviço do Calendar
        service = build('calendar', 'v3', credentials=creds)
        
        # Listar os próximos 5 eventos
        now = 'datetime.datetime.utcnow().isoformat() + "Z"'  # 'Z' indica UTC
        print('Obtendo os próximos 5 eventos')
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=now,
            maxResults=5, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        
        if not events:
            print('Nenhum evento próximo encontrado.')
        else:
            print('Eventos próximos:')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"- {start} {event['summary']}")
        
        print("\nCredenciais funcionando corretamente!")
        
    except Exception as e:
        print(f"Erro ao testar credenciais: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    
    print("Utilitário de Autenticação para Google Calendar")
    print("="*50)
    print("Este script irá auxiliar na obtenção das credenciais necessárias")
    print("para a integração com o Google Calendar.")
    print("\nO processo irá abrir uma janela do navegador para autorização.")
    print("="*50)
    
    input("Pressione Enter para continuar...")
    
    testar_credenciais()