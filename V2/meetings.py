from logging_config import logging, configurar_logging
from requests import get
from os import getenv
from dotenv import load_dotenv
from functions.date import definePeriodo
from database import Database
from datetime import datetime
import mysql.connector

# Configura o logging (Obrigatório em todos os arquivos)
logger = configurar_logging()

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


        # Verifica se existem reuniões
        if len(r["events"]) == 0:
            logging.info("Nenhuma reunião encontrada")
            return None
        

        # Usa a conexão já estabelecida
        connection = Database.get_connection()
        cursor = connection.cursor()


        # Para cada Evento coletado:
        for evento in r["events"]:
            # Converte string ISO para datetime e formata para MySQL
            start_time = datetime.fromisoformat(evento['startTime'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S') if evento.get('startTime') else None
            end_time = datetime.fromisoformat(evento['endTime'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S') if evento.get('endTime') else None
            date_added = datetime.fromisoformat(evento.get('dateAdded', '').replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S') if evento.get('dateAdded') else None
            date_updated = datetime.fromisoformat(evento.get('dateUpdated', '').replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S') if evento.get('dateUpdated') else None

            # Prepara query de inserção
            query = """
                INSERT INTO agenciavfx.meetings (
                    id, address, title, calendarId, contactId, groupId,
                    appointmentStatus, assignedUserId, notes, isRecurring,
                    startTime, endTime, dateAdded, dateUpdated,
                    createdBy, masterEventId
                ) VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s
                )
                ON DUPLICATE KEY UPDATE
                    address = VALUES(address),
                    title = VALUES(title),
                    calendarId = VALUES(calendarId),
                    contactId = VALUES(contactId),
                    groupId = VALUES(groupId),
                    appointmentStatus = VALUES(appointmentStatus),
                    assignedUserId = VALUES(assignedUserId),
                    notes = VALUES(notes),
                    isRecurring = VALUES(isRecurring),
                    startTime = VALUES(startTime),
                    endTime = VALUES(endTime),
                    dateUpdated = VALUES(dateUpdated)
            """
            
            # Prepara valores com tratamento de campos vazios
            values = (
                evento.get('id') or None,  # Campos obrigatórios mantêm .get('campo')
                evento.get('address', None),  # Campos opcionais usam valor default None
                evento.get('title', None),
                evento.get('calendarId', None),
                evento.get('contactId', None),
                evento.get('groupId', None),
                evento.get('status', None),  
                evento.get('assignedUserId', None),
                evento.get('notes', None),
                str(evento.get('isRecurring', False)), 
                start_time,  # Datas já tratadas anteriormente
                end_time,
                date_added,
                date_updated,
                evento.get('createdBy', {}).get('userId', None),  
                evento.get('masterEventId', None)
            )

            try:
                cursor.execute(query, values)
                logging.DEBUG(f"Reunião {evento.get('id')} - {evento.get('title')} inserida/atualizada com sucesso")
            except mysql.connector.Error as e:
                logging.error(f"Erro ao inserir reunião {evento.get('id')} - {evento.get('title')}: {str(e)}")
                continue

        # Commit das alterações
        connection.commit()
        logging.info(f"{len(r['events'])} reuniões processadas")


    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")
        raise

if __name__ == "__main__":
    # Inicializa conexão com banco
    Database.initialize()

    getMeetings()