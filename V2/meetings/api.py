from requests import get
from os import getenv
from functions.date import definePeriodo
from dotenv import load_dotenv
from logging_config import logging

def getMeetings():
    '''
    Faz a requisição na API e retorna o JSON
    '''

    try:

        load_dotenv()

        calendarId = getenv("GHL_CALENDAR_ID")
        locationId = getenv("GHL_LOCATION_ID")
        authorization = getenv("GHL_AUTHORIZATION")

        startTime, endTime = definePeriodo()

        url = "https://services.leadconnectorhq.com/calendars/events/appointments/{eventId}"

        # Define os parâmetros necessários para a requisição
        params = {
            "locationId": locationId,
            "calendarId": calendarId,
            "startTime": startTime,
            "endTime": endTime
        }

        header = {
        "Authorization": f"Bearer {authorization}",
        "Version": "2021-04-15"
        }

        r = get(url=url, params=params, headers=header)


    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    getMeetings()