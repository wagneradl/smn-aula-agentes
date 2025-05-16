"""
Módulo para interagir com API internas da empresa.
Este é um cliente genérico que pode ser adaptado para APIs específicas.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

class APIInterna:
    """Cliente para a API interna da empresa."""
    
    def __init__(self):
        """Inicializa o cliente da API interna."""
        self.base_url = os.getenv("INTERNAL_API_URL")
        self.api_key = os.getenv("INTERNAL_API_KEY")
        
        if not self.base_url or not self.api_key:
            raise ValueError("Configuração da API interna ausente")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _request(self, method, endpoint, params=None, data=None):
        """
        Faz uma requisição para a API interna.
        
        Args:
            method (str): Método HTTP (GET, POST, etc.)
            endpoint (str): Endpoint da API
            params (dict, opcional): Parâmetros de consulta
            data (dict, opcional): Dados para enviar no corpo da requisição
            
        Returns:
            dict: Resposta da API
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data
            )
            
            response.raise_for_status()  # Lança exceção para códigos de erro
            
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {str(e)}")
            raise
    
    def buscar_projetos(self, status=None, departamento=None):
        """
        Busca projetos na API interna.
        
        Args:
            status (str, opcional): Filtrar por status (ex: 'em_andamento')
            departamento (str, opcional): Filtrar por departamento
            
        Returns:
            list: Lista de projetos
        """
        params = {}
        if status:
            params["status"] = status
        if departamento:
            params["departamento"] = departamento
        
        return self._request("GET", "projetos", params=params)
    
    def buscar_funcionario(self, id=None, email=None):
        """
        Busca informações de um funcionário.
        
        Args:
            id (int, opcional): ID do funcionário
            email (str, opcional): Email do funcionário
            
        Returns:
            dict: Dados do funcionário
        """
        params = {}
        if id:
            params["id"] = id
        if email:
            params["email"] = email
        
        return self._request("GET", "funcionarios", params=params)
    
    def registrar_tarefa(self, projeto_id, titulo, descricao, responsavel_id, prazo):
        """
        Registra uma nova tarefa em um projeto.
        
        Args:
            projeto_id (int): ID do projeto
            titulo (str): Título da tarefa
            descricao (str): Descrição da tarefa
            responsavel_id (int): ID do responsável
            prazo (str): Prazo da tarefa (formato YYYY-MM-DD)
            
        Returns:
            dict: Tarefa criada
        """
        data = {
            "projeto_id": projeto_id,
            "titulo": titulo,
            "descricao": descricao,
            "responsavel_id": responsavel_id,
            "prazo": prazo
        }
        
        return self._request("POST", "tarefas", data=data)