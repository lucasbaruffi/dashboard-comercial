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

        logger.info("Iniciando a busca de campos personalizados dos contatos")
        # Carrega as variáveis de ambiente
        load_dotenv()

        locationId = getenv("GHL_LOCATION_ID")
        authorization = getenv("GHL_AUTHORIZATION")


        # Define a URL de requisição primária, as próximas serão para pegar os contatos que faltam
        url = f"https://services.leadconnectorhq.com/contacts/?locationId={locationId}&limit=1&query=Baruffi"

        header = {
            "Authorization": f"Bearer {authorization}",
            "Version": "2021-07-28"
        }

        # O loop é necessário para obter todos os usuários, pois a API retorna 100 por vez
        while url != None:

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


            # Verifica se existem contatos
            if len(r["contacts"]) == 0:
                logger.info("Nenhum Usuário Encontrado")
                return None


            # Usa a conexão já estabelecida
            connection = Database.get_connection()
            cursor = connection.cursor()


            # Para cada contato:
            for contact in r["contacts"]:

                print (contact)

                # Prepara query de inserção
                query = """
                    INSERT INTO agenciavfx.contacts (
                        id, name, firstName, lastName, email, phone
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s
                    )
                    ON DUPLICATE KEY UPDATE
                        name = VALUES(name),
                        firstName = VALUES(firstName),
                        lastName = VALUES(lastName),
                        email = VALUES(email),
                        phone = VALUES(phone)
                """
                
                # Prepara valores com tratamento de campos vazios
                values = (
                    user.get('id') or None,  # Campos obrigatórios mantêm .get('campo')
                    user.get('name', None),  # Campos opcionais usam valor default None
                    user.get('firstName', None),
                    user.get('lastName', None),
                    user.get('email', None),
                    user.get('phone', None)
                )

                try:
                    cursor.execute(query, values)
                    logger.debug(f"Usuário {user.get('name')} inserido/atualizado com sucesso")
                except mysql.connector.Error as e:
                    logger.error(f"Erro ao inserir Usuário {user.get('name')}: {str(e)}")
                    continue

        # Commit das alterações
        connection.commit()
        logger.info(f"{len(r['users'])} Usuários inseridos/atualizados")

    except Exception as e:
        logger.error(f"Ocorreu um erro: {e}")
        raise

if __name__ == "__main__":
    # Inicializa conexão com banco
    Database.initialize()
    
    getContactsCustomFields()