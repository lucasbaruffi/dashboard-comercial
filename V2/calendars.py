from logging_config import configurar_logging
from requests import get
from os import getenv
from dotenv import load_dotenv
from database import Database
import mysql.connector

# Configura o logger (Obrigatório em todos os arquivos)
logger = configurar_logging()

def getCalendars():
    try:

        logger.info("Iniciando a busca de usuários")
        # Carrega as variáveis de ambiente
        load_dotenv()

        locationId = getenv("GHL_LOCATION_ID")
        authorization = getenv("GHL_AUTHORIZATION")


        # Requisição HTTP
        url = "https://services.leadconnectorhq.com/calendars/"

        params = {
            "locationId": locationId
        }

        header = {
            "Authorization": f"Bearer {authorization}",
            "Version": "2021-04-15"
        }

        r = get(url=url, params=params, headers=header)


        # Verifica se a requisição foi bem sucedida
        if r.status_code != 200:
            logger.error(f"Ocorreu um erro na requisição dos usuários: {r.text}")
            return None

        logger.info("Calendários obtidos com sucesso")


        # Transforma em JSON
        r = r.json()


        # Verifica se existem Calendários
        if len(r["calendars"]) == 0:
            logger.info("Nenhum Calendário Encontrado")
            return None


        # Usa a conexão já estabelecida
        connection = Database.get_connection()
        cursor = connection.cursor()

        # Para cada Calendário:
        for calendar in r["calendars"]:

            # Prepara query de inserção
            query = """
                INSERT INTO agenciavfx.calendars (
                    id, name
                ) VALUES (
                    %s, %s
                )
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    description = VALUES(description)
            """
            
            # Prepara valores com tratamento de campos vazios
            values = (
                calendar.get('id') or None,  # Campos obrigatórios mantêm .get('campo')
                calendar.get('name', None)
            )

            try:
                cursor.execute(query, values)
                logger.debug(f"Calendário {calendar.get('name')} inserido/atualizado com sucesso")
            except mysql.connector.Error as e:
                logger.error(f"Erro ao inserir Calendário {calendar.get('name')}: {str(e)}")
                continue

        # Commit das alterações
        connection.commit()
        logger.info(f"{len(r['calendars'])} Calendário inseridos/atualizados")

    except Exception as e:
        logger.error(f"Ocorreu um erro: {e}")
        raise

if __name__ == "__main__":
    # Inicializa conexão com banco
    Database.initialize()
    
    getCalendars()