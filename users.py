from logging_config import configurar_logging
from requests import get
from os import getenv
from dotenv import load_dotenv
from database import Database
import mysql.connector

# Configura o logger (Obrigatório em todos os arquivos)
logger = configurar_logging()

def getUsers():
    try:

        # Define a foto padrão (caso não exista)
        fotoPadrao = getenv("GHL_DEFAULT_PHOTO")

        logger.info("Iniciando a busca de usuários")
        # Carrega as variáveis de ambiente
        load_dotenv()

        locationId = getenv("GHL_LOCATION_ID")
        authorization = getenv("GHL_AUTHORIZATION")


        # Requisição HTTP
        url = "https://services.leadconnectorhq.com/users/"

        params = {
            "locationId": locationId
        }

        header = {
            "Authorization": f"Bearer {authorization}",
            "Version": "2021-07-28"
        }

        r = get(url=url, params=params, headers=header)


        # Verifica se a requisição foi bem sucedida
        if r.status_code != 200:
            logger.error(f"Ocorreu um erro na requisição dos usuários: {r.text}")
            return None

        logger.info("Usuários obtidos com sucesso")


        # Transforma em JSON
        r = r.json()


        # Verifica se existem usuários
        if len(r["users"]) == 0:
            logger.info("Nenhum Usuário Encontrado")
            return None


        # Usa a conexão já estabelecida
        connection = Database.get_connection()
        cursor = connection.cursor()

        # Para cada Usuário:
        for user in r["users"]:

            # Prepara query de inserção
            query = """
                INSERT INTO users (
                    id, name, firstName, lastName, email, phone, profilePhoto
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                )
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    firstName = VALUES(firstName),
                    lastName = VALUES(lastName),
                    email = VALUES(email),
                    phone = VALUES(phone),
                    profilePhoto = VALUES(profilePhoto)
            """
            
            # Prepara valores com tratamento de campos vazios
            values = (
                user.get('id') or None,  # Campos obrigatórios mantêm .get('campo')
                user.get('name', None),  # Campos opcionais usam valor default None
                user.get('firstName', None),
                user.get('lastName', None),
                user.get('email', None),
                user.get('phone', None),
                user.get('profilePhoto', fotoPadrao)  # Substitua 'fotoPadrao' por um valor padrão adequado
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
    
    getUsers()