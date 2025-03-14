from main import log, locationId, authorization, requests

def formatOpportunities(lista:list = []):
    '''
    Recebe uma lista de oportunidades e formata para salvar na planilha
    '''

def getOpportunities():
    '''
    Puxa todas as oportunidades de um determinado período

    Puxa todas as oportunidaes criadas até 90 dias antes e salva em uma lista

    Retorna uma lista com as oportunidades.
    '''

    try:
        # Define os parâmetros da consulta
        url = "https://services.leadconnectorhq.com/opportunities/search"
        params = {
            "location_id": locationId
        }

        header = {
            "Authorization": f"Bearer {authorization}",
            "Version": "2021-07-28"
        }          

        # Faz a requisição
        r = requests.get(url=url, params=params, headers=header)  

        # Se a resposta tiver um status code de erro, raise_for_status() vai disparar uma exceção HTTPError
        r.raise_for_status()

        # Transforma em JSON
        r = r.json()

        # Envia a lista para ser formatada
        formatOpportunities(r)

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
