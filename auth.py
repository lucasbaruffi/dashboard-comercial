import requests
import os
from dotenv import load_dotenv, set_key
from requests_oauthlib import OAuth2Session


# Carrega os dados do .env
load_dotenv()

# Puxa as variáveis de ambiente e salva em variáveis locais
clientId = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")
authUrl = os.getenv("AUTH_URL")
tokenUrl = os.getenv("TOKEN_URL")
redirectUrl = os.getenv("REDIRECT_URL")

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

# 3) Trocar o 'code' pelo 'access token'
token = oauth.fetch_token(
    token_url=tokenUrl,
    authorization_response=redirect_response,
    client_secret=clientSecret
)

print("Token obtido com sucesso:")
print(token)