import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis de Ambiente
load_dotenv()

authorization = os.getenv("AUTHORIZATION")
locationId = os.getenv("LOCATION_ID")
calendarId = os.getenv("CALENDAR_ID")

# Todas utilizam o mesmo Header, por isso está fora das funções
header = {
    "Authorization": f"Bearer {authorization}",
    "Version": "2021-04-15"
}


def definePeriodo(diasAntes: int = 30, diasDepois: int = 15):
    '''
    Retorna as datas em timestamp (formato aceito pelo GHL)

    O usuário passa quantos dias antes e depois do dia atual ele quer em timestamp.
    O código recebe e calcula a diferença baseado no dia atual.

    Se nenhum parâmetro for informado, ele pegará 30 dias antes e 15 dias depois

    Entrada:
       diasAntes (int): quantos dias antes do atual quer transformat em timestamp.
       diasDepois (int): quantos dias depois do atual quer transformat em timestamp.
   
       
    Saída:
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
            raise ValueError("Os parâmetros não podem ser 0 ou negativos.")

        # Se está tudo certo segue a função
        from datetime import datetime, timedelta

        # Define o dia atual
        data_atual = datetime.now()

        # Calcula a diferença de tempo
        dataDiasAntes = data_atual - timedelta(days=diasAntes)
        dataDiasDepois = data_atual + timedelta(days=diasDepois)

        # Converte para o formato Epoch (timestamp)
        epoch_x_dias_antes = int(dataDiasAntes.timestamp())
        epoch_x_dias_depois = int(dataDiasDepois.timestamp())

        return epoch_x_dias_antes, epoch_x_dias_depois

    except (TypeError, ValueError) as erro:
        print(f"Ocorreu um erro: {erro}")


def getCalendarEvents():
    
    startTime, endTime = definePeriodo()

    url = "https://services.leadconnectorhq.com/calendars/events"

    params = {
        "locationId": locationId,
        "calendarId": calendarId,
        "startTime": startTime,
        "endTime": endTime
    }

    r = requests.get(url=url, params=params, headers=header)

    statusCode = r.status_code

    # Erro por token expirado: 401

    if statusCode == 200:
        r = r.json()        
        return r["events"]
    else:
        r = r.text
        print(r)    







from sheets import adicionarAgendamento

#eventos = getCalendarEvents()

for evento in eventos:
    dados = [
        evento.get("id", ""),
        evento.get("address", ""),
        evento.get("title", ""),
        evento.get("calendarId", ""),
        evento.get("locationId", ""),
        evento.get("contactId", ""),
        evento.get("groupId", ""),
        evento.get("appointmentStatus", ""),
        evento.get("assignedUserId", ""),
        evento.get("startTime", ""),
        evento.get("endTime", ""),
        evento.get("dateAdded", ""),
        evento.get("dateUpdated", ""),
        evento.get("createdBy", {}).get("userId", ""),
        evento.get("opportunityId", "")
    ]   

    #adicionarAgendamento(dados)
