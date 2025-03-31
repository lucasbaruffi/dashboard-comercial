from logging_config import logging

def definePeriodo(diasAntes: int = 30, diasDepois: int = 15):
    '''
    Retorna as datas em timestamp (formato aceito pelo GHL)

    O usuário passa quantos dias antes e depois do dia atual ele quer em timestamp.
    O código recebe e calcula a diferença baseado no dia atual.

    Se nenhum parâmetro for informado, ele pegará 30 dias antes e 15 dias depois

    Entrada:
    -
       diasAntes (int): quantos dias antes do atual quer transformat em timestamp.
       diasDepois (int): quantos dias depois do atual quer transformat em timestamp.
   
       
    Saída:
    -
        Sairá uma tupla com o tempo anterior e posterior, sucessivamente

    Exemplo:
    >>> definePeriodo(10, 5):
    >>> return: 99999999, 99999999
    '''

    try:
        # Validação do tipo:
        if not isinstance(diasAntes, int) or not isinstance(diasDepois, int):
            raise TypeError("Os parâmetros 'diasAntes' e 'diasDepois' devem ser inteiros.")

        # Validação de dias negativos:
        if diasAntes <= 0 or diasDepois <= 0:
            raise ValueError("Os parâmetros de data não podem ser 0 ou negativos.")

        # Se está tudo certo segue a função
        from datetime import datetime, timedelta

        # Define o dia atual
        data_atual = datetime.now()

        # Calcula a diferença de tempo
        dataDiasAntes = data_atual - timedelta(days=diasAntes)
        dataDiasDepois = data_atual + timedelta(days=diasDepois)

        # Converte para o formato Epoch (timestamp) -> *1000 para transformar em milisegundos
        epoch_x_dias_antes = int(dataDiasAntes.timestamp() * 1000)
        epoch_x_dias_depois = int(dataDiasDepois.timestamp() * 1000)

        logging.debug("Tempo convertido para timestamp")
        return epoch_x_dias_antes, epoch_x_dias_depois

    except Exception as erro:
        logging.info(f"Ocorreu um erro: {erro}")

def iso_to_datetime(data_iso: str) -> str:
    '''
    Converte data ISO 8601 para formato MySQL (YYYY-MM-DD HH:mm:ss)
    
    Params:
        data_iso (str): Data no formato ISO (2023-09-25T16:00:00+05:30)
    
    Returns:
        str: Data formatada (2023-09-25 16:00:00) ou None se inválida
        
    Example:
        >>> iso_to_datetime("2023-09-25T16:00:00+05:30")
        >>> "2023-09-25 16:00:00"
    '''
    try:
        from datetime import datetime
        if not data_iso:
            return None
            
        # Converte string ISO para datetime
        data_datetime = datetime.fromisoformat(data_iso.replace('Z', '+00:00'))
        
        # Formata para string no padrão MySQL
        return data_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
    except Exception as e:
        logging.error(f"Erro ao converter data ISO: {e}")
        return None
