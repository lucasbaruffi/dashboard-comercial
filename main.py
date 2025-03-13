import requests
import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

googleRequests = 0

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

# ------------- Autenticação GHL -------------------

def authGHL():
    '''
    Fazer a autenticação no GHL

    Essa função tenta fazer uma requisição via API, se não conseguir gera um novo token
    '''
    
    from dotenv import load_dotenv, set_key
    
    # Carrega as variáveis de Ambiente
    clientId = os.getenv("CLIENT_ID")
    clientSecret = os.getenv("CLIENT_SECRET")
    authUrl = os.getenv("AUTH_URL")
    tokenUrl = os.getenv("TOKEN_URL")
    redirectUrl = os.getenv("REDIRECT_URL")
    refreshToken = os.getenv("REFRESH_GHL_TOKEN")

    try:
        # Tenta uma requisição
        url = "https://services.leadconnectorhq.com/calendars/"

        params = {
            "locationId": locationId
        }

        header = {
            "Authorization": f"Bearer {authorization}",
            "Version": "2021-04-15"
        }            

        r = requests.get(url=url, params=params, headers=header)
        
        # Se a resposta tiver um status code de erro, raise_for_status() vai disparar uma exceção HTTPError
        r.raise_for_status()

        log("sucesso", "Token GHL Validado")

    except requests.exceptions.HTTPError as http_err:
        # Se a requisição não tiver funcionado
        log("erro", "Tentando Reconectar com o GHL")

        # Tenta reconectar com o Token Temporário:
        try:
             # Pega o Token
            body = {
                "client_id": clientId,
                "client_secret": clientSecret,
                "grant_type": "refresh_token",
                "refresh_token": refreshToken
            }

            token = requests.post("https://services.leadconnectorhq.com/oauth/token",data=body )

            # Verifica se deu erro
            token.raise_for_status()

            # Extrai o Token de Acesso da resposta
            token = token.json()
            access_token = token['access_token']
            refreshToken = token['refresh_token']

            # Define a variável de Ambiente com o Token
            log("sucesso",f"Conexão com o GHL estabelecida!")
            set_key(".env", "REFRESH_GHL_TOKEN", refreshToken)
            set_key(".env", "AUTHORIZATION", access_token)

        except:
            import urllib.parse
            from requests_oauthlib import OAuth2Session

            log("erro", "Não foi possível conecar com o GHL, necessário nova conexão")

            # Define os Escopos:
            scope = [
                "opportunities.readonly",
                "contacts.readonly",
                "locations.readonly",
                "calendars/events.write",
                "calendars/events.readonly",
                "calendars.write",
                "calendars.readonly"
            ]

            # Cria a sessão OAuth
            oauth = OAuth2Session(clientId, redirect_uri=redirectUrl, scope=scope)

            # 1) Obter a URL de autorização e redirecionar o usuário
            authorization_url, state = oauth.authorization_url(authUrl)
            print("Acesse a URL para autorizar a aplicação:")
            print(authorization_url.replace("+","%20"))

            # 2) Após o usuário autorizar, ele será redirecionado para o redirect_uri.
            #    Copie a URL de redirecionamento (que contém o 'code') e cole aqui.

            log("erro", "Verifique o terminal do Python")

            redirect_response = input("Cole aqui a URL completa de redirecionamento:\n")


            # Faz o parse da URL
            parsed_url = urllib.parse.urlparse(redirect_response)

            # Extrai os parâmetros de query em forma de dicionário
            query_params = urllib.parse.parse_qs(parsed_url.query)

            # Pega o valor de 'code'
            auth_code = query_params.get("code", [None])[0]

            if not auth_code:
                print("Não foi possível encontrar o parâmetro 'code' na URL!")
            else:
                print("Code obtido:", auth_code)

                body = {
                    "client_id": clientId,
                    "client_secret": clientSecret,
                    "grant_type": "authorization_code",
                    "code": auth_code
                }

                token = requests.post("https://services.leadconnectorhq.com/oauth/token",data=body )

                # Extrai o Token de Acesso da resposta
                token = token.json()
                access_token = token['access_token']
                refreshToken = token['refresh_token']

                # Define a variável de Ambiente com o Token
                set_key(".env", "REFRESH_GHL_TOKEN", refreshToken)
                set_key(".env", "AUTHORIZATION", access_token)

                log("sucesso", "Nova conexão estabelecida, conferindo novamente")

                authGHL()




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

        # Abre a tabela de logs
        tabelaLogs = planilha.worksheet("logs")
        # Define o dia de hoje e formata
        diaAtual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Define a nova linha
        novaLinha = [diaAtual, status, obs]
        # Adiciona a linha
        tabelaLogs.append_row(novaLinha)

    except Exception as e:
        print("Erro ao inicializar a planilha de log:", e)
        return
    
authGHL()

def atualizarAgendamentos(agendamentos: list = [[]]):
    '''
    Adiciona ou atualiza agendamentos na planilha

    Recebe uma lista re reuniões já formatados (do formatEvents), verifica se já existe na planilha.
    
    Se não existe, adiciona uma nova linha
    
    Se existe, verifica se tem diferença dos dados
    
    Se tiver, atualiza.
    
    Senão tiver diferença, ignora
    '''
    # Verifica se possui reuniões
    if agendamentos == []:
        log('erro', 'Nenhuma reunião para atualizar.')

    else:
        try:
            # Puxa a planilha
            planilha = get_worksheet()

            # Abre a tavela de agendamentos 
            tabelaAgendamentos = planilha.worksheet("agendamentos")

            # Salva as reuniões agendadas em uma lista
            reunioesSalvas = tabelaAgendamentos.get_all_values()
            log("sucesso", "Localizados todos os agendamentos Salvos na planilha")
            log(obs="Separando as reuniões...")

            reunioesAtualizar = []
            reunioesAdicionar = []

            # Pra cada agendamento
            for agendamento in agendamentos:
                id = agendamento[0]

                # Procura na lista de reuniões salvas
                for cont, reuniaoSalva in enumerate(reunioesSalvas):

                    # Se o Id de alguma for igual
                    if reuniaoSalva[0] == id:

                        # Se estiver igual
                        if reuniaoSalva == agendamento:
                            break

                        else:
                            # Adiciona à lista dos que precisam atualizar
                            reunioesAtualizar.append(agendamento)
                            break
                    else:
                        # Não é igual é é o ultimo da lista que foi procurado
                        if cont == len(reunioesSalvas)-1:
                            # Se não estiver em nenhum lugar, será adicionado
                            reunioesAdicionar.append(agendamento)

            log(obs=f"Não serão modificadas {len(agendamentos) - len(reunioesAtualizar) - len(reunioesAdicionar)} reuniões")

            log(obs=f"Serão adicionadas {len(reunioesAdicionar)} reuniões")

            # Adicionar reuniões
            tabelaAgendamentos.append_rows(reunioesAdicionar)
            log("sucesso", "Reuniões adicionadas!")

            log(obs=f"Serão atualizadas {len(reunioesAtualizar)} reuniões")

            # Procura as linhas e atualiza os valores
            for reuniaoAAtualizar in reunioesAtualizar:
                # Procura a linha com o agendamento
                linhaAAtualizar = tabelaAgendamentos.find(reuniaoAAtualizar[0], in_column=1)
                row_number = linhaAAtualizar.row

                # Define o espaço que quer atualizar
                range_linha = f"A{row_number}:O{row_number}"
                
                # Atualiza a linha
                tabelaAgendamentos.update(values=reuniaoAAtualizar, range_name=range_linha)

            log("sucesso", "Reuniões atualizadas!")

        except Exception as e:
            log("errro", f"Ocorreu um erro: {e}")

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

def getOpportunity(contactId: int = None):

    # Se não receber o ContactId, retorna "Não Encontrado"
    if not contactId:
        log("erro", "Id do contato não informado para busca da oportunidade")
        return "Não Encontrado"

    else:
        try:
            # Define parâmetros para requisição da API:
            url = "https://services.leadconnectorhq.com/opportunities/search"
        
            params = {
                "contact_id": contactId,
                "location_id": locationId
            }

            header = {
                "Authorization": f"Bearer {authorization}",
                "Version": "2021-07-28"
            }            

            # Faz a requisição
            r = requests.get(url, params=params, headers=header)


            # Se a resposta tiver um status code de erro, raise_for_status() vai disparar uma exceção HTTPError
            r.raise_for_status()

            # Transforma a resposta em Json e retorna
            r = r.json()     
            
            # Pega apenas alista de oportunidades
            oportunidades = r["opportunities"]

            # Verifica se tem oportunidades
            if len(oportunidades) == 0:
                log("erro", f"Oportunidade do contato {contactId} não encontrada")
                return ""
            
            else:
                # Pega a útlima  oportunidade da lista - a mais antiga no CRM
                oportunidade = oportunidades[len(oportunidades)-1]["id"]

                # log("sucesso", f"Oportunidade do cliente {contactId} encontrada")


                # Formata os dados em lista
                # ---------------

                # Salva a oportunidade na planilha
                # ---------------

                return oportunidade




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

        header = {
            "Authorization": f"Bearer {authorization}",
            "Version": "2021-04-15"
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

        # Lista com todos os eventos formatados
        dadosEventos = []

        log(obs="Buscando Oportunidades...")
        for evento in eventos:

            # Procura a última oportunidade deste contato
            opportunityId = getOpportunity(evento.get("contactId", ""))


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
                opportunityId
            ]   

            # Adiciona cada evento na lista
            dadosEventos.append(dados)
        
        # Passa a lista de eventos para o Google Sheets
        atualizarAgendamentos(dadosEventos)
        

#formatEvents(getCalendarEvents())