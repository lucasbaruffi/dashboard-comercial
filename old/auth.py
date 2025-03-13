import requests
import os
from dotenv import load_dotenv, set_key
from requests_oauthlib import OAuth2Session
import urllib.parse


# Carrega os dados do .env
load_dotenv()

# Puxa as variáveis de ambiente e salva em variáveis locais
clientId = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")
authUrl = os.getenv("AUTH_URL")
tokenUrl = os.getenv("TOKEN_URL")
redirectUrl = os.getenv("REDIRECT_URL")
refreshToken = os.getenv("REFRESH_GHL_TOKEN")

# Define os Escopos:
scope = [
    "opportunities.readonly",
    "contacts.readonly",
    "locations.readonly",
    "calendars/events.write",
    "calendars/events.readonly",
    "calendars.write",
    "calendars.readonly"
]

# Cria a sessão OAuth
oauth = OAuth2Session(clientId, redirect_uri=redirectUrl, scope=scope)

# 1) Obter a URL de autorização e redirecionar o usuário
authorization_url, state = oauth.authorization_url(authUrl)
print("Acesse a URL para autorizar a aplicação:")
print(authorization_url.replace("+","%20"))

# 2) Após o usuário autorizar, ele será redirecionado para o redirect_uri.
#    Copie a URL de redirecionamento (que contém o 'code') e cole aqui.
redirect_response = input("Cole aqui a URL completa de redirecionamento:\n")

# Faz o parse da URL
parsed_url = urllib.parse.urlparse(redirect_response)

# Extrai os parâmetros de query em forma de dicionário
query_params = urllib.parse.parse_qs(parsed_url.query)

# Pega o valor de 'code'
auth_code = query_params.get("code", [None])[0]

if not auth_code:
    print("Não foi possível encontrar o parâmetro 'code' na URL!")
else:
    print("Code obtido:", auth_code)


# Pega o Token

body = {
    "client_id": clientId,
    "client_secret": clientSecret,
    "grant_type": "authorization_code",
    "code": auth_code
}

token = requests.post("https://services.leadconnectorhq.com/oauth/token",data=body )

# Extrai o Token de Acesso da resposta
token = token.json()
access_token = token['access_token']
refreshToken = token['refresh_token']

# Define a variável de Ambiente com o Token
print(f"Token Obtido: {access_token}")
set_key(".env", "REFRESH_GHL_TOKEN", refreshToken)
set_key(".env", "AUTHORIZATION", access_token)