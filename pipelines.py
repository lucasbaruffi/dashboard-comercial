from logging_config import configurar_logging
from requests import get
from os import getenv
from dotenv import load_dotenv
from database import Database
import mysql.connector

# Configura o logger (Obrigatório em todos os arquivos)
logger = configurar_logging()

def getPipelines():
    try:

        logger.info("Iniciando a busca de Pipelines")
        # Carrega as variáveis de ambiente
        load_dotenv()

        locationId = getenv("GHL_LOCATION_ID")
        authorization = getenv("GHL_AUTHORIZATION")


        # Requisição HTTP
        url = "https://services.leadconnectorhq.com/opportunities/pipelines"

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
            logger.error(f"Ocorreu um erro na requisição das Pipelines: {r.text}")
            return None

        logger.info("Pipelines obtidas com sucesso")


        # Transforma em JSON
        r = r.json()


        # Verifica se existem Pipelines
        if len(r["pipelines"]) == 0:
            logger.info("Nenhuma Pipeline Encontrada")
            return None


        # Usa a conexão já estabelecida
        connection = Database.get_connection()
        cursor = connection.cursor()

        # Para cada Calendário:
        for pipeline in r["pipelines"]:

            # Prepara query de inserção
            query = """
                INSERT INTO pipelines (
                    id, name
                ) VALUES (
                    %s, %s
                )
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name)
            """
            
            # Prepara valores com tratamento de campos vazios
            values = (
                pipeline.get('id') or None,  # Campos obrigatórios mantêm .get('campo')
                pipeline.get('name', None)
            )

            try:
                cursor.execute(query, values)
                logger.debug(f"Pipeline {pipeline.get('name')} inserido/atualizado com sucesso")
            except mysql.connector.Error as e:
                logger.error(f"Erro ao inserir Pipeline {pipeline.get('name')}: {str(e)}")
                continue
            
            for stage in pipeline["stages"]:
                query = """
                    INSERT INTO pipelinestages (
                        id, name, pipelineId
                    ) VALUES (
                        %s, %s, %s
                    )
                    ON DUPLICATE KEY UPDATE
                        name = VALUES(name),
                        pipelineId = VALUES(pipelineId)
                """
                
                values = (
                    stage.get('id') or None,
                    stage.get('name', None),
                    pipeline.get('id') or None
                )
                
                try:
                    cursor.execute(query, values)
                    logger.debug(f"Stage {stage.get('name')} inserido/atualizado com sucesso")
                except mysql.connector.Error as e:
                    logger.error(f"Erro ao inserir Stage {stage.get('name')}: {str(e)}")
                    continue

        # Commit das alterações
        connection.commit()
        logger.info(f"{len(r['pipelines'])} Pipelines inseridos/atualizados")

    except Exception as e:
        logger.error(f"Ocorreu um erro: {e}")
        raise

if __name__ == "__main__":
    # Inicializa conexão com banco
    Database.initialize()
    
    getPipelines()