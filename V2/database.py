import mysql.connector
from os import getenv
from dotenv import load_dotenv
from logging_config import logging

class Database:
    _connection = None

    @classmethod
    def initialize(cls):
        """Inicializa e valida a conexão com o banco"""
        try:
            load_dotenv()
            
            # Valida credenciais
            db_host = getenv("DB_HOST")
            db_user = getenv("DB_USER")
            db_pass = getenv("DB_PASS")
            db_name = getenv("DB_NAME")

            # if not all([db_host, db_user, db_pass, db_name]):
            #     raise ValueError("Credenciais do banco de dados incompletas")

            logging.info("Inicializando conexão com banco de dados")

            # Estabelece conexão
            cls._connection = mysql.connector.connect(
                host=db_host,
                user=db_user,
                passwd=db_pass
            )
            
            # Seleciona o banco
            cursor = cls._connection.cursor()
            cursor.execute(f"USE {db_name}")
            
            logging.info("Conexão com banco estabelecida com sucesso")
            return True

        except mysql.connector.Error as e:
            logging.error(f"Erro na conexão com MySQL: {e}")
            raise
        except Exception as e:
            logging.error(f"Erro ao inicializar banco: {e}")
            raise

    @classmethod
    def get_connection(cls):
        """Retorna conexão existente"""
        if cls._connection is None or not cls._connection.is_connected():
            raise ConnectionError("Conexão com banco não inicializada")
        return cls._connection