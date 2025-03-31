from logging_config import configurar_logging
from requests import get
from os import getenv
from dotenv import load_dotenv
from database import Database
import mysql.connector

# Configura o logger (Obrigatório em todos os arquivos)
logger = configurar_logging()

def getContactsCustomFields():
    try:

        logger.info("Iniciando a busca de campos personalizados de contatos")
        # Carrega as variáveis de ambiente
        load_dotenv()

        locationId = getenv("GHL_LOCATION_ID")
        authorization = getenv("GHL_AUTHORIZATION")


        # Requisição HTTP
        url = f"https://services.leadconnectorhq.com/locations/{locationId}/customFields"

        params = {
            "model": "contact"
        }

        header = {
            "Authorization": f"Bearer {authorization}",
            "Version": "2021-07-28"
        }

        r = get(url=url, params=params, headers=header)


        # Verifica se a requisição foi bem sucedida
        if r.status_code != 200:
            logger.error(f"Ocorreu um erro na requisição dos Contact Custom Fields: {r.text}")
            return None

        logger.info("Contact Custom Fields obtidos com sucesso")


        # Transforma em JSON
        r = r.json()


        # Verifica se existem Calendários
        if len(r["customFields"]) == 0:
            logger.info("Nenhum Contact Custom Field encontrado")
            return None


        # Usa a conexão já estabelecida
        connection = Database.get_connection()
        cursor = connection.cursor()

        # Para cada Calendário:
        for customField in r["customFields"]:

            # Prepara query de inserção
            query = """
                INSERT INTO contact_custom_field (
                    id, name, fieldKey, placeholder, dataType
                ) VALUES (
                    %s, %s, %s, %s, %s
                )
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    fieldKey = VALUES(placeholder),
                    placeholder = VALUES(placeholder),
                    dataType = VALUES(dataType)
            """
            
            # Prepara valores com tratamento de campos vazios
            values = (
                customField.get('id') or None,  # Campos obrigatórios mantêm .get('campo')
                customField.get('name', None),
                customField.get('fieldKey', None),
                customField.get('placeholder', None),
                customField.get('dataType', None)
            )

            try:
                cursor.execute(query, values)
                logger.debug(f"Contact Custom Field {customField.get('name')} inserido/atualizado com sucesso")
            except mysql.connector.Error as e:
                logger.error(f"Erro ao inserir Contact Custom Field {customField.get('name')}: {str(e)}")
                continue

        # Commit das alterações
        connection.commit()
        logger.info(f"{len(r['customFields'])} Contact Custom Field inseridos/atualizados")

    except Exception as e:
        logger.error(f"Ocorreu um erro: {e}")
        raise

if __name__ == "__main__":
    # Inicializa conexão com banco
    Database.initialize()
    
    getContactsCustomFields()