from requests import get
from os import getenv
from dotenv import load_dotenv
from logging_config import logging
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from functions.date import definePeriodo

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
        r.raise_for_status()
        return r.json()

    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")
        raise

if __name__ == "__main__":
    getMeetings()