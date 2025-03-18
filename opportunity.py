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
        
        for cf in op["customFiels"]:
            if cf["id"] == '5xpVHjUBibgmZVvMk5r4':
                tamanhoEmpresa = cf["fieldValueStrig"]

            elif cf["id"] == 'uWWUdvkMa3AApDCZfIWk':
                site = cf["fieldValueStrig"]

            elif cf["id"] == 'BtPyM0PeQdf2WAH8Uq3E':
                site = cf["fieldValueStrig"]
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
        op.get("customFiels", {}.get()),
        op.get("", ""),
        op.get("", ""),
        op.get("", ""),
        ]
        print(op)

   

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