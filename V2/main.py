from logging_config import logging
from auth import ghlAuthorization
from meetings import getMeetings

if __name__ == "__main__":
    logging.info("Aplicação Iniciada")
    # Faz a autenticação com o GHL
    ghlAuthorization()
    getMeetings()