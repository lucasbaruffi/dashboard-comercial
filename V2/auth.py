from dotenv import load_dotenv, set_key
import os
import requests
import json
from werkzeug.serving import make_server
import threading
import time
from pathlib import Path


# Carrega as variáveis de ambiente
load_dotenv()

# Define as variáveis de ambiente
clientId = os.getenv('GHL_CLIENT_ID')
clientSecret = os.getenv('GHL_CLIENT_SECRET')
authUrl = os.getenv('GHL_AUTH_URL')
tokenUrl = os.getenv('GHL_TOKEN_URL')
redirectUri = os.getenv('GHL_REDIRECT_URI')
locationId = os.getenv('GHL_LOCATION_ID')
calendarId = os.getenv('GHL_CALENDAR_ID')
authToken = os.getenv('GHL_AUTHORIZATION')
refreshToken = os.getenv('GHL_REFRESH_TOKEN')

# Isto serve para deixar um servidor online para receber o código de autorização
class FlaskServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()



def refreshAuth():
    url = tokenUrl
    
    body = {
        "client_id": clientId,
        "client_secret": clientSecret,
        "grant_type": "refresh_token",
        "refresh_token": refreshToken
    }

    token = requests.post(url, data=body)

    token.raise_for_status()

def getTokens(code):
    '''
    Recebe o Code e retorna o Token e o Refresh Token
    Salva ambos nas variáveis de ambiente.
    '''
    try:
        url = tokenUrl
        body = {
            "client_id": clientId,
            "client_secret": clientSecret,
            "grant_type": "authorization_code",
            "code": code
        }

        tokens = requests.post(url, data=body)
        tokens.raise_for_status()
        tokens = tokens.json()

        accessToken = tokens['access_token']
        refreshToken = tokens['refresh_token']

        # Define o caminho absoluto para o arquivo .env
        env_path = str(Path(__file__).parent / '.env')
        
        print(f"Salvando tokens no arquivo: {env_path}")

        # Atualiza os tokens usando set_key
        set_key(env_path, "GHL_AUTHORIZATION", accessToken)
        set_key(env_path, "GHL_REFRESH_TOKEN", refreshToken)
            
        print("Tokens salvos com sucesso no .env")
        
    except Exception as e:
        print('Erro ao obter os Tokens:', e)
        return


def read_code_from_env():
    """Lê o GHL_CODE diretamente do arquivo .env"""
    # Força recarregamento do .env
    load_dotenv(override=True)
    return os.getenv('GHL_CODE')

def wait_for_code(timeout=180):
    """Aguarda até que o GHL_CODE seja atualizado no arquivo .env ou timeout seja atingido"""
    start_time = time.time()
    
    # Lê o código atual para comparação
    initial_code = read_code_from_env()

    while True:
        # Verifica se passou do timeout
        if time.time() - start_time > timeout:
            raise TimeoutError("Tempo limite excedido. Por favor, tente novamente.")
            
        # Lê o código atual com cache limpo
        current_code = read_code_from_env()
        
        # Se o código mudou, retorna o novo código
        if current_code and current_code != initial_code:
            print("Código de autorização recebido!")
            return current_code
            
        # Espera 1 segundo antes de verificar novamente
        time.sleep(1)

def auth():
    from app import app  # Import local para evitar importação circular
    import urllib.parse
    from requests_oauthlib import OAuth2Session
    
    # Inicia o servidor Flask em uma thread
    flask_thread = FlaskServerThread(app)
    flask_thread.daemon = True  # Thread será encerrada quando o programa principal terminar
    flask_thread.start()

    scopes = [
        "calendars/events.readonly",
        "calendars.readonly",
        "locations.readonly",
        "locations/customFields.readonly"
    ]

    # Cria a sessão OAuth
    oauth = OAuth2Session(clientId, redirect_uri=redirectUri, scope=scopes)

    # 1) Obter a URL de autorização e redirecionar o usuário
    authorization_url, state = oauth.authorization_url(authUrl)
    print("Acesse a URL para autorizar a aplicação:")
    print(authorization_url.replace("+","%20"))

    try:
        # Aguarda o código ser atualizado no .env
        code = wait_for_code()
        print(f"Code Salvo com sucesso!")
        return code
    except TimeoutError as e:
        print(f"Erro: {e}")
        return None
    finally:
        # Garante que o servidor será desligado
        flask_thread.shutdown()


def ghlAuthorization():
    '''
    Tenta as várias formas de Conectar

    Primeiro chama a função refreshAuth() para tentar autenticar com o Refresh Token

    Se não conseguir, chama a função auth() para que o usuário refaça a conexão
    '''
    try:    
        # Tenta autenticar com o Refresh Token
        refreshAuth()
        print('Autenticado com o Refresh Token')

    except Exception as e:
        print('Erro ao autenticar com o Refresh Token:', e)
        print('Tentando Reconectar...')
        code = auth()

        try:
            # Tenta autenticar com o Code
            getTokens(code)
            print('Autenticado com o Code')

        except Exception as e:
            print('Erro ao autenticar com o Code:', e)
            print('Tente novamente')

ghlAuthorization()