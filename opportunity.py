from main import log, locationId, authorization, requests

def diasAntes(n:int = None):
    '''
    Formata o dia no padrão mm-dd-yyyy

    Recebe o dia de início da consulta.

    Ex:

    >>> diasAntes(60)

    Retorna o período de até 60 dias antes

    Se não informar nenhum valor, começará em 01/01/2023

    '''
    from datetime import datetime, timedelta

    if n:
        hoje = datetime.now()
        diasAntes = hoje - timedelta(days=n)
        diasAntes = diasAntes.strftime("%m-%d-%Y")
        return(diasAntes)
    
    else:
        return("01-01-2023")


def formatOpportunities(lista:list = []):
    '''
    Recebe uma lista de oportunidades e formata para salvar na planilha
    '''

    for op in lista:
        formatedOp = []
        # Define os campos personalizados
        for cf in op["customFields"]:
            if cf["id"] == '8g08EFI9Qu4DlpVUxkew':
                closer = cf.get("fieldValueString", "")

            elif cf["id"] == '8Lc3bC17M065Edcob4dt':
                sdr = cf.get("fieldValueString", "")

            elif cf["id"] == 'hnAbrYxtSbJSvmzoAHpd':
                tipoVenda = cf.get("fieldValueString", "")
            
            elif cf["id"] == 'XedT4Yg1IuEU1RSVoFJQ':
                isOp = cf.get("fieldValueString", "")

            elif cf["id"] == 'gf9opjOGBMQft8FNnq5P':
                dataGanho = cf.get("fieldValueString", "") # Está em timestamp

            elif cf["id"] == 'xwmET46ovjpsN2oPTHGy':
                segmento = cf.get("fieldValueString", "") 

            elif cf["id"] == '5xpVHjUBibgmZVvMk5r4':
                funcionarios = cf.get("fieldValueString", "")

            elif cf["id"] == 'mLJtYWsRLhd5r4K24mLk':
                faturamento = cf.get("fieldValueString", "")

            elif cf["id"] == 'EUaHadhsk53lpgWVUWn5':
                site = cf.get("fieldValueString", "")

            elif cf["id"] == 'OyRGgjyylLx04EZw3gcC':
                desafio = cf.get("fieldValueString", "")

            elif cf["id"] == 'uWWUdvkMa3AApDCZfIWk':
                urlOrigem = cf.get("fieldValueString", "")

            elif cf["id"] == 'BtPyM0PeQdf2WAH8Uq3E':
                origem = cf.get("fieldValueString", "")

            elif cf["id"] == 'V2TNe5O2rB6VLYYazSI6':
                cargo = cf.get("fieldValueString", "")

            elif cf["id"] == 'YDEL68h3nFgJbfZj1mZV':
                emailCorporativo = cf.get("fieldValueString", "")

            elif cf["id"] == 'Lb7O90ZncOMJRSWbSIMA':
                cidade = cf.get("fieldValueString", "")

            elif cf["id"] == 'OKMKNuJgWNoD3R7Lqw4r':
                score = cf.get("fieldValueString", "")

            elif cf["id"] == 'KOPoVWrK61t4QRLprdeG':
                timeVendas = cf.get("fieldValueString", "")

            elif cf["id"] == 'Q5uphNMlU3W0F3lNhIIV':
                clientesAtivos = cf.get("fieldValueString", "")

        # Formata os Dados em uma lista
        formatedOp = [
        op.get("id", ""),
        op.get("name", ""),
        op.get("monetaryValue"),
        op.get("pipelineId", ""),
        op.get("pipelineStageId", ""),
        op.get("pipelineStageUId", ""),
        op.get("assignedTo", ""),
        op.get("status", ""),
        op.get("source", ""),
        op.get("lastStatusChangeAt", ""),
        op.get("lastStageChangeAt", ""),
        op.get("createdAt", ""),
        op.get("updatedAt", ""),
        op.get("contactId", ""),
        op.get("locationId", ""),
        op.get("lostReasonId", ""),
        op.get("contact", {}).get("name", ""),
        op.get("contact", {}).get("email", ""),
        op.get("contact", {}).get("phone", ""),
        globals().get('closer', ""),
        globals().get('sdr', ""),
        globals().get('tipoVenda', ""),
        globals().get('isOp', ""),
        globals().get('dataGanho', ""),
        globals().get('segmento', ""),
        globals().get('funcionarios', ""),
        globals().get('faturamento', ""),
        globals().get('site', ""),
        globals().get('desafio', ""),
        globals().get('urlOrigem', ""),
        globals().get('origem', ""),
        globals().get('cargo', ""),
        globals().get('emailCorporativo', ""),
        globals().get('cidade', ""),
        globals().get('score', ""),
        globals().get('timeVendas', ""),
        globals().get('clientesAtivos', ""),
        ]

        print(formatedOp)
        print("--------------------------")

   

def getOpportunities():
    '''
    Puxa todas as oportunidades de um determinado período

    Puxa todas as oportunidaes criadas até 90 dias antes e salva em uma lista

    Retorna uma lista com as oportunidades.
    '''

    try:

        # Define uma lista de Oportunidades
        ops = []

        # Define a data do início da consulta
        initialDate = diasAntes(1)

        # Define os parâmetros da consulta
        url = f"https://services.leadconnectorhq.com/opportunities/search?location_id={locationId}&limit=100&date={initialDate}"

        header = {
            "Authorization": f"Bearer {authorization}",
            "Version": "2021-07-28"
        } 

        while url:
                     
            # Faz a requisição
            r = requests.get(url=url, headers=header)  

            # Se a resposta tiver um status code de erro, raise_for_status() vai disparar uma exceção HTTPError
            r.raise_for_status()

            # Transforma em JSON
            r = r.json()

            # Adiciona as oportunidades na lista
            ops.extend(r["opportunities"])

            # Redefine a URL para a próxima página
            url = r["meta"]["nextPageUrl"]

        # Envia a lista para ser formatada
        formatOpportunities(ops)



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

getOpportunities()