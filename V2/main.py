from logging_config import logging, configurar_logging
from auth import ghlAuthorization
from meetings import getMeetings
from database import Database

if __name__ == "__main__":
    try:
        logging.info("Aplicação Iniciada")
        
        # Inicializa conexão com banco
        Database.initialize()
        
        # Faz a autenticação com o GHL
        ghlAuthorization()
        
        # Busca reuniões
        getMeetings()
    
    except Exception as e:
        logging.error(f"Erro crítico: {e}")
        logging.critical("Programa finalizado com erro")