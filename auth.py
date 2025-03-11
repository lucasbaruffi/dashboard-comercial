import requests
import os
from dotenv import load_dotenv, set_key

# Carrega os dados do .env
load_dotenv()

# Puxa as variáveis de ambiente e salva em variáveis locais
clientId = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")
authUrl = os.getenv("AUTH_URL")
tokenUrl = os.getenv("TOKEN_URL")

