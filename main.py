import requests
import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Carrega as variáveis de Ambiente
load_dotenv()

authorization = os.getenv("AUTHORIZATION")
locationId = os.getenv("LOCATION_ID")
calendarId = os.getenv("CALENDAR_ID")


# ---------- Autenticação do Google ----------------
# Define os escopos de acesso
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Variáveis globais para armazenar o cliente e a planilha
_cliente = None
_planilha = None

def get_gspread_client():
    """
    Retorna o cliente autenticado do gspread.
    Se já estiver autenticado, retorna o cliente armazenado; 
    caso contrário, realiza a autenticação e o armazena.
    """
    global _cliente
    if _cliente is None:
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        _cliente = gspread.authorize(creds)
    return _cliente

def get_worksheet():
    """
    Retorna a planilha.
    Se a planilha já foi aberta, retorna ela; 
    caso contrário, abre a planilha e a armazena.
    """
    global _planilha
    if _planilha is None:
        # Obtém o ID da planilha a partir da variável de ambiente
        log_sheet_id = os.getenv("GOOGLE_SHEET_LOG_KEY")
        if not log_sheet_id:
            raise ValueError("GOOGLE_SHEET_LOG_KEY não está definida.")
        client = get_gspread_client()
        _planilha = client.open_by_key(log_sheet_id)
    return _planilha

# --------- Fim Autenticação do Google -------------

# Todas utilizam o mesmo Header, por isso está fora das funções
header = {
    "Authorization": f"Bearer {authorization}",
    "Version": "2021-04-15"
}


def log(status: str = "regular", obs: str = "Sem observações"):
    '''
    O Objetivo dessa função é ter um log de tudo o que está acontecendo.

    Em vez de utilizar o "print()" para mostrar, usarei isso para salvar os logs em uma planílha.
    Como não ficaremos com o cógio aberto, é válido ter um log de registros.
    Ele pegará da data atual para salvar na planilha, não sendo necessário passar esse parâmetro.

    Entrada:
    -
        status (str): É bom padronizar entre "erro" e "sucesso", mas o campo é livre.
        obs (str): Campo de string livre para deixar o que aconteceu.

    Retorno:
    -
        O código não retorna nada, apenas salva o registro na plailha.

    ---

    Exemplo:
    >>> log("sucesso", "Foram encontradas 75 reuniões")
    '''
    
    try:
        # Puxa a planilha:
        planilha = get_worksheet()

    except Exception as e:
        print("Erro ao inicializar a planilha de log:", e)
        return
    
    # Abre a tabela de logs
    tabelaLogs = planilha.worksheet("logs")

    # Define o dia de hoje e formata
    diaAtual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Define a nova linha
    novaLinha = [diaAtual, status, obs]

    # Adiciona a linha
    tabelaLogs.append_row(novaLinha)

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

        log("sucesso", "Tempo convertido para timestamp")
        return epoch_x_dias_antes, epoch_x_dias_depois

    except Exception as erro:
        log("errro", f"Ocorreu um erro: {erro}")

def getCalendarEvents():
    try:
        # Define o Início e Fim 
        startTime, endTime = definePeriodo()

        # Define o Endpoint da API
        url = "https://services.leadconnectorhq.com/calendars/events"

        # Define os parâmetros necessários para a requisição
        params = {
            "locationId": locationId,
            "calendarId": calendarId,
            "startTime": startTime,
            "endTime": endTime
        }

        # Faz a requisição
        r = requests.get(url=url, params=params, headers=header)
  

        # Se a resposta tiver um status code de erro, raise_for_status() vai disparar uma exceção HTTPError
        r.raise_for_status()

        # Transforma a resposta em Json e retorna
        r = r.json()     

        # Retorna a lista
        log("sucesso", "Lista de reuniões coletada")
        return r
    

    except requests.exceptions.HTTPError as http_err:
        # Exemplo: tratamento específico para token expirado (status 401)
        if r.status_code == 401:
            log("erro", "Erro 401: Token expirado.")
        else:
            log("erro",f"Erro HTTP: {http_err}")
    except requests.exceptions.RequestException as req_err:
        log("erro ",f"Erro na requisição: {req_err}")
    except Exception as e:
        log("erro",f"Ocorreu um erro inesperado: {e}")

def formatEvents(eventos:list = []):
    '''
    Recebe os eventos do getcCalendarEvents.

    Verifica se não retornou uma lista vazia

    Retorno
    -
        Retorna uma lista pronta para ser adicionada no Google Sheets, seguindo esta ordem:

    >>> formatEvents(getCalendarEvents())
    '''
    from sheets import adicionarAgendamento

    # Deixa apenas os eventos
    eventos = eventos["events"]

    # Verifica se não é uma lista vazia
    if eventos == []:
        log("erro", "Lista de reuniões vazia")

    # Se não, segue o fluxo
    else:
        log("sucesso", f"Encontradas {len(eventos)} reuniões")

        for evento in eventos:

            # Procura a última oportunidade deste contato



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
 
        adicionarAgendamento(dados)
 

formatEvents(getCalendarEvents())