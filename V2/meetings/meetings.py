from logging_config import logging
from api import getMeetings  # Importação relativa ao mesmo diretório

def salvarReuiniões():
    '''
    Função responsável por salvar as reuniões no banco de dados
    '''
    logging.info("Iniciando Salvamento das Reuniões")

def pegarSalvarReuniões():
    '''
    Função responsável por consultar as reuniões e salvar no banco de dados	
    '''
    meetings = getMeetings()
    salvarReuiniões()

if __name__ == "__main__":
    pegarSalvarReuniões()