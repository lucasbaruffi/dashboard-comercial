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

        logging.info("Tempo convertido para timestamp")
        return epoch_x_dias_antes, epoch_x_dias_depois

    except Exception as erro:
        logging.info(f"Ocorreu um erro: {erro}")
