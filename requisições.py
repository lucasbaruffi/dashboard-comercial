import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis de Ambiente
load_dotenv()

authorization = os.getenv("AUTHORIZATION")
locationId = os.getenv("LOCATION_ID")

def getCalendars():

    header = {
        "Authorization": f"Bearer {authorization}",
        "Version": "2021-04-15"
    }
    query = {
        "locationId": locationId
    }

    r = requests.get("https://services.leadconnectorhq.com/calendars/", params=query, headers=header)

    statusCode = r.status_code

    if statusCode == 200:
        r = r.json()

        print("Requisição Funcionou")

        for calendar in r["calendars"]:
            print(calendar["name"])


    else:
        r = r.text
        print(r)

    
getCalendars()