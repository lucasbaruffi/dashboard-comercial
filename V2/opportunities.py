from logging_config import configurar_logging
from requests import get
from os import getenv
from dotenv import load_dotenv
from database import Database
import mysql.connector
from functions.date import iso_to_datetime

# Configura o logger (Obrigatório em todos os arquivos)
logger = configurar_logging()

def getOpportunities():
    try:

        logger.info("Iniciando a busca de contatos")
        # Carrega as variáveis de ambiente
        load_dotenv()

        locationId = getenv("GHL_LOCATION_ID")
        authorization = getenv("GHL_AUTHORIZATION")


        # Define a URL de requisição primária, as próximas serão para pegar os contatos que faltam
        url = f"https://services.leadconnectorhq.com/contacts/?locationId={locationId}&limit=100"

        header = {
            "Authorization": f"Bearer {authorization}",
            "Version": "2021-07-28"
        }

        # O loop é necessário para obter todos os usuários, pois a API retorna 100 por vez
        while url != None:
            import time

            time.sleep(0.1)
            # Requisição HTTP
            r = get(url=url, headers=header)


            # Verifica se a requisição foi bem sucedida
            if r.status_code != 200:
                logger.error(f"Ocorreu um erro na requisição dos Clientes: {r.text}")
                return None

            logger.info("Clientes obtidos com sucesso")


            # Transforma em JSON
            r = r.json()


            # Deefine a próxima URL	
            url = r.get("meta", {}).get("nextPageUrl", None)

            print(len(r["contacts"]))
            # Verifica se existem contatos
            if len(r["contacts"]) == 0:
                logger.info("Nenhum Contato Encontrado")
                return None


            # Usa a conexão já estabelecida
            connection = Database.get_connection()
            cursor = connection.cursor()


            # Para cada contato:
            for contact in r["contacts"]:

                # Prepara query de inserção
                query = """
                    INSERT INTO agenciavfx.contacts (
                        id,
                        name,
                        firstName,
                        lastName,
                        email,
                        phone,
                        companyName,
                        source,
                        assignedTo,
                        city,
                        state,
                        postalCode,
                        address,
                        dateAdded,
                        dateUpdated,
                        dateOfBirth,
                        website
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s
                    )
                    ON DUPLICATE KEY UPDATE
                        name = VALUES(name),
                        firstName = VALUES(firstName),
                        lastName = VALUES(lastName),
                        email = VALUES(email),
                        phone = VALUES(phone),
                        companyName = VALUES(companyName),
                        source = VALUES(source),
                        assignedTo = VALUES(assignedTo),
                        city = VALUES(city),
                        state = VALUES(state),
                        postalCode = VALUES(postalCode),
                        address = VALUES(address),
                        dateAdded = VALUES(dateAdded),
                        dateUpdated = VALUES(dateUpdated),
                        dateOfBirth = VALUES(dateOfBirth),
                        website = VALUES(website)
                """

                # Formatando as Datas
                dateAdded = iso_to_datetime(contact.get('dateAdded'))
                dateUpdated = iso_to_datetime(contact.get('dateUpdated'))


                # Montando a tupla de valores
                values = (
                    contact.get('id') or None,
                    contact.get('contactName', None),
                    contact.get('firstNameRaw', None),
                    contact.get('lastNameRaw', None),
                    contact.get('email', None),
                    contact.get('phone', None),
                    contact.get('companyName', None),
                    contact.get('source', None),
                    contact.get('assignedTo', None),
                    contact.get('city', None),
                    contact.get('state', None),
                    contact.get('postalCode', None),
                    contact.get('address1', None),
                    dateAdded,   
                    dateUpdated, 
                    contact.get('dateOfBirth', None),
                    contact.get('website', None)
                    )

                try:
                    cursor.execute(query, values)
                    logger.debug(f"Contato {contact.get('contactName')} inserido/atualizado com sucesso")
                except mysql.connector.Error as e:
                    logger.error(f"Erro ao inserir Usuário {contact.get('contactName')}: {str(e)}")
                    continue

                
                # Salva os Campos Personalizados
                for customField in contact.get("customFields", []):
                    query = """
                        INSERT INTO contact_custom_field_value (
                            contact_id, field_id, field_value
                        ) VALUES (
                            %s, %s, %s
                        )
                        ON DUPLICATE KEY UPDATE
                            field_value = VALUES(field_value)
                    """
                    
                    values = (
                        contact.get('id') or None,
                        customField.get('id') or None,
                        customField.get('value') or None
                    )
                    
                    try:
                        cursor.execute(query, values)
                        logger.debug(f"Campo Personalizado {customField.get('id')} inserido/atualizado com sucesso")
                    except mysql.connector.Error as e:
                        logger.error(f"Erro ao inserir Campo Personalizado {customField.get('id')}: {str(e)}")
                        continue



            # Commit das alterações
            connection.commit()
            logger.info(f"{len(r['contacts'])} contatos inseridos/atualizados")

    except Exception as e:
        logger.error(f"Ocorreu um erro: {e}")
        raise

if __name__ == "__main__":
    # Inicializa conexão com banco
    Database.initialize()
    
    getOpportunities()