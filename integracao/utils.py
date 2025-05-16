"""
Utilidades para integração de APIs.
Funções auxiliares para tratamento de erros, autenticação, etc.
"""

import time
import random
import logging

# Configurar logger
logger = logging.getLogger(__name__)

def backoff_retry(func, max_retries=3, initial_delay=1):
    """
    Executa uma função com backoff exponencial em caso de falhas.
    
    Args:
        func (callable): Função a ser executada
        max_retries (int): Número máximo de tentativas
        initial_delay (float): Delay inicial entre tentativas (em segundos)
        
    Returns:
        O resultado da função, se bem-sucedida
        
    Raises:
        Exception: Se todas as tentativas falharem
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Todas as {max_retries} tentativas falharam. Última erro: {str(e)}")
                raise
            
            # Calcular delay com jitter para evitar thundering herd
            delay = initial_delay * (2 ** attempt) + random.uniform(0, 1)
            logger.warning(f"Tentativa {attempt+1} falhou: {str(e)}. Tentando novamente em {delay:.2f}s...")
            time.sleep(delay)

def sanitize_input(value, max_length=1000):
    """
    Sanitiza entrada de texto para evitar injeção e outros problemas.
    
    Args:
        value (str): Valor a ser sanitizado
        max_length (int): Comprimento máximo permitido
        
    Returns:
        str: Valor sanitizado
    """
    if not isinstance(value, str):
        return str(value)
    
    # Truncar se muito longo
    if len(value) > max_length:
        value = value[:max_length]
    
    # Remover caracteres potencialmente perigosos
    # Isso é uma simplificação - em produção use uma biblioteca específica
    chars_to_remove = ['<', '>', '"', "'", ';', '\\', '&']
    for char in chars_to_remove:
        value = value.replace(char, '')
    
    return value