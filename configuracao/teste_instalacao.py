# Script para testar a instalação e configuração do ambiente

import os
import sys
import importlib.util
from dotenv import load_dotenv

# Cores para saída no terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Imprime um cabeçalho formatado."""
    width = 70
    print("\n" + "=" * width)
    print(f"{Colors.BOLD}{text}{Colors.ENDC}".center(width))
    print("=" * width)

def print_success(text):
    """Imprime uma mensagem de sucesso."""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    """Imprime uma mensagem de aviso."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def print_error(text):
    """Imprime uma mensagem de erro."""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def check_python_version():
    """Verifica a versão do Python."""
    print_header("Verificando versão do Python")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} detectado")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} detectado, mas Python 3.8+ é requerido")
        return False

def check_required_packages():
    """Verifica se os pacotes requeridos estão instalados."""
    print_header("Verificando pacotes requeridos")
    
    required_packages = [
        "langchain", 
        "openai", 
        "python-dotenv", 
        "pandas", 
        "matplotlib", 
        "seaborn",
        "faiss-cpu", 
        "tiktoken",
        "pypdf"
    ]
    
    all_installed = True
    
    for package in required_packages:
        if importlib.util.find_spec(package):
            print_success(f"Pacote {package} instalado")
        else:
            print_error(f"Pacote {package} não encontrado")
            all_installed = False
    
    if not all_installed:
        print_warning("Alguns pacotes necessários não estão instalados.")
        print("Execute: pip install -r requirements.txt")
    
    return all_installed

def check_env_file():
    """Verifica se o arquivo .env existe e está configurado."""
    print_header("Verificando arquivo .env")
    
    # Verificar se o arquivo .env existe
    if not os.path.exists('.env'):
        if os.path.exists('./configuracao/.env'):
            print_warning("Arquivo .env encontrado na pasta configuracao, mas não na raiz.")
            print("Copie o arquivo .env para a raiz do projeto.")
            return False
        else:
            print_error("Arquivo .env não encontrado.")
            print("Copie o arquivo .env.exemplo para .env e adicione suas chaves de API.")
            return False
    
    # Carregar as variáveis de ambiente
    load_dotenv()
    
    # Verificar chave da OpenAI
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        print_error("Chave da OpenAI não encontrada no arquivo .env")
        return False
    elif openai_key == "SUA_CHAVE_OPENAI_AQUI":
        print_error("Chave da OpenAI não foi alterada do valor de exemplo")
        return False
    else:
        print_success("Chave da OpenAI configurada")
    
    # Verificar credenciais do Microsoft Teams (opcional)
    teams_client_id = os.getenv('TEAMS_CLIENT_ID')
    teams_client_secret = os.getenv('TEAMS_CLIENT_SECRET')
    teams_tenant_id = os.getenv('TEAMS_TENANT_ID')
    
    if not teams_client_id or not teams_client_secret or not teams_tenant_id:
        print_warning("Credenciais do Microsoft Teams não encontradas ou incompletas")
        print("A integração com o Microsoft Teams não estará disponível")
    else:
        print_success("Credenciais do Microsoft Teams configuradas")
    
    return True

def test_openai_connection():
    """Testa a conexão com a API da OpenAI."""
    print_header("Testando conexão com OpenAI")
    
    try:
        from openai import OpenAI
        
        # Carregar a chave da API
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print_error("Chave da API OpenAI não encontrada")
            return False
        
        # Inicializar o cliente
        client = OpenAI(api_key=api_key)
        
        # Fazer uma chamada simples para testar
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente útil."},
                {"role": "user", "content": "Diga 'A configuração está funcionando corretamente' em uma palavra."}
            ],
            max_tokens=5
        )
        
        print_success("Conexão com a API da OpenAI estabelecida com sucesso")
        return True
        
    except ImportError:
        print_error("Módulo OpenAI não está instalado")
        return False
    except Exception as e:
        print_error(f"Erro ao conectar com a API da OpenAI: {str(e)}")
        return False

def main():
    """Função principal."""
    print_header("TESTE DE CONFIGURAÇÃO - AGENTES SMN")
    
    tests = [
        check_python_version,
        check_required_packages,
        check_env_file,
        test_openai_connection
    ]
    
    results = [test() for test in tests]
    
    print_header("RESULTADOS")
    
    if all(results):
        print_success("TODOS OS TESTES PASSARAM! Seu ambiente está corretamente configurado.")
        print("\nVocê pode começar a usar os agentes. Experimente um exemplo:")
        print("  python exemplos/exemplo_faq.py")
    else:
        print_error("ALGUNS TESTES FALHARAM. Corrija os problemas antes de continuar.")
        print("\nConsulte as mensagens acima para resolver os problemas detectados.")
        print("Se precisar de ajuda, consulte a documentação ou entre em contato com o suporte.")

if __name__ == "__main__":
    main()