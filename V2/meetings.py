from logging_config import logging
from requests import get
from os import getenv
from dotenv import load_dotenv
from functions.date import definePeriodo


def getMeetings():
    try:
        # Carrega as variáveis de ambiente
        load_dotenv()

        calendarId = getenv("GHL_CALENDAR_ID")
        locationId = getenv("GHL_LOCATION_ID")
        authorization = getenv("GHL_AUTHORIZATION")


        # Define o período da requisição
        startTime, endTime = definePeriodo()


        # Requisição HTTP
        url = "https://services.leadconnectorhq.com/calendars/events"

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


        # Verifica se a requisição foi bem sucedida
        if r.status_code != 200:
            logging.error(f"Ocorreu um erro na requisição das reuniões: {r.text}")
            return None

        logging.info("Reuniões obtidas com sucesso")

        # Transforma em JSON
        r = r.json()


    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")
        raise

if __name__ == "__main__":
    getMeetings()