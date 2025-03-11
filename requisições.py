import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis de Ambiente
load_dotenv()

authorization = os.getenv("AUTHORIZATION")
locationId = os.getenv("LOCATION_ID")
calendarId = os.getenv("CALENDAR_ID")

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

def getCalendarEvents():
    from tratamento import dataEpoch
    # start = str(input("Qual a data inicial? (DD/MM/AAAA HH:mm) "))
    # end = str(input("Qual a data final? (DD/MM/AAAA HH:mm) "))
# 
    # startFormated = dataEpoch(start)
    # endFormated = dataEpoch(end)


    header = {
        "Authorization": f"Bearer {authorization}",
        "Version": "2021-04-15"
    }
    query = {
        "locationId": locationId,
        "calendarId": calendarId,
        "startTime": "1741489200000",
        "endTime": "1741662000000"
    }

    r = requests.get("https://services.leadconnectorhq.com/calendars/events", params=query, headers=header)

    statusCode = r.status_code

    if statusCode == 200:
        r = r.json()

        print("Requisição Funcionou")

        for event in r["events"]:
            print(f'''Id: {event["id"]}
Local: {event["address"]}
Título: {event["title"]}
Status: {event["appointmentStatus"]}

''')


    else:
        r = r.text
        print(r)    
    
getCalendarEvents()