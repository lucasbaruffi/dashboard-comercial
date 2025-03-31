import logging
from pathlib import Path
import datetime

def configurar_logging():
    """Configura as definições de logging para a aplicação"""
    
    # Cria diretório de logs se não existir
    diretorio_log = Path(__file__).parent / 'logs'
    diretorio_log.mkdir(exist_ok=True)
    
    # Arquivo único para todos os logs
    arquivo_log = diretorio_log / 'logs.log'
    
    # Configura o logging
    logging.basicConfig(
        level=logging.DEBUG,
        # Formato: 2024-03-20 14:30:25 | INFO | Mensagem
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            # Handler para arquivo - modo 'a' (append) para preservar histórico
            logging.FileHandler(arquivo_log, encoding='utf-8', mode='a'),
            # Handler para console
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)

# Exemplo de uso em outros arquivos:
"""
from logging_config import configurar_logging

logger = configurar_logging()
logger.info("Aplicação iniciada")
logger.error("Um erro ocorreu")
"""