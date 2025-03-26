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

        logger.info("Iniciando a busca de Oportunidades")
        # Carrega as variáveis de ambiente
        load_dotenv()

        locationId = getenv("GHL_LOCATION_ID")
        authorization = getenv("GHL_AUTHORIZATION")


        # Define a URL de requisição primária, as próximas serão para pegar os contatos que faltam
        url = f"https://services.leadconnectorhq.com/opportunities/search/?location_id={locationId}&limit=100"

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
                logger.error(f"Ocorreu um erro na requisição das Oportunidades: {r.text}")
                return None

            logger.info("Oportunidades obtidas com sucesso")


            # Transforma em JSON
            r = r.json()


            # Deefine a próxima URL	
            url = r.get("meta", {}).get("nextPageUrl", None)

            # Verifica se existem Oportunidades
            if len(r["opportunities"]) == 0:
                logger.info("Nenhum Oportunidade Encontrada")
                return None


            # Usa a conexão já estabelecida
            connection = Database.get_connection()
            cursor = connection.cursor()


            # Para cada oportunidade:
            for opportunity in r["opportunities"]:
                # Prepara query de inserção
                query = """
                    INSERT INTO agenciavfx.opportunities (
                        id, name, monetaryValue, pipelineId, pipelineStageId,
                        assignedTo, status, source, lastStatusChangeAt,
                        lastStageChangeAt, lastActionDate, createdAt,
                        updatedAt, contactId
                    ) VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s,
                        %s, %s
                    )
                    ON DUPLICATE KEY UPDATE
                        name = VALUES(name),
                        monetaryValue = VALUES(monetaryValue),
                        pipelineId = VALUES(pipelineId),
                        pipelineStageId = VALUES(pipelineStageId),
                        assignedTo = VALUES(assignedTo),
                        status = VALUES(status),
                        source = VALUES(source),
                        lastStatusChangeAt = VALUES(lastStatusChangeAt),
                        lastStageChangeAt = VALUES(lastStageChangeAt),
                        lastActionDate = VALUES(lastActionDate),
                        updatedAt = VALUES(updatedAt),
                        contactId = VALUES(contactId)
                """

                # Formatando as Datas
                lastStatusChangeAt = iso_to_datetime(opportunity.get('lastStatusChangeAt'))
                lastStageChangeAt = iso_to_datetime(opportunity.get('lastStageChangeAt'))
                lastActionDate = iso_to_datetime(opportunity.get('lastActionDate'))
                createdAt = iso_to_datetime(opportunity.get('createdAt'))
                updatedAt = iso_to_datetime(opportunity.get('updatedAt'))

                # Montando a tupla de valores
                values = (
                    opportunity.get('id') or None,
                    opportunity.get('name', None),
                    opportunity.get('monetaryValue', None),
                    opportunity.get('pipelineId', None),
                    opportunity.get('pipelineStageId', None),
                    opportunity.get('assignedTo', None),
                    opportunity.get('status', None),
                    opportunity.get('source', None),
                    lastStatusChangeAt,
                    lastStageChangeAt,
                    lastActionDate,
                    createdAt,
                    updatedAt,
                    opportunity.get('contactId', None)
                )

                try:
                    cursor.execute(query, values)
                    logger.debug(f"Oportunidade {opportunity.get('name')} inserida/atualizada com sucesso")
                except mysql.connector.Error as e:
                    logger.error(f"Erro ao inserir Oportunidade {opportunity.get('name')}: {str(e)}")
                    continue


            # Commit das alterações
            connection.commit()
            logger.info(f"{len(r['opportunities'])} oportunidades inseridas/atualizadas")

    except Exception as e:
        logger.error(f"Ocorreu um erro: {e}")
        raise

if __name__ == "__main__":
    # Inicializa conexão com banco
    Database.initialize()
    
    getOpportunities()