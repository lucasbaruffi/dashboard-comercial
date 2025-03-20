from V1.main import log, locationId, authorization, requests, get_worksheet

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

def atualizarOportunidades(ops: list = [[]]):
    '''
    Adiciona ou atualiza Oportunidades na planilha

    Recebe uma lista de oportunidades já formatados (do formatOpportunities), verifica se já existe na planilha.
    
    Se não existe, adiciona uma nova linha
    
    Se existe, verifica se tem diferença dos dados
    
    Se tiver, atualiza.
    
    Senão tiver diferença, ignora
    '''
    # Verifica se possui reuniões
    if ops == []:
        log('erro', 'Nenhuma reunião para atualizar.')

    else:
        try:
            # Puxa a planilha
            planilha = get_worksheet()

            # Abre a tavela de agendamentos 
            tabelaDeals = planilha.worksheet("deals")

            # Salva as reuniões agendadas em uma lista
            opsSalvas = tabelaDeals.get_all_values()
            log("sucesso", "Localizados todas as oportunidades salvas na planilha")
            log(obs="Separando as oportunidades...")

            opsAtualizar = []
            opsAdicionar = []

            # Pra cada oportunidade
            for op in ops:
                id = op[0]

                # Procura na lista de reuniões salvas
                for cont, opSalva in enumerate(opsSalvas):

                    # Se o Id de alguma for igual
                    if opSalva[0] == id:

                        # Se estiver igual
                        if opSalva == op:
                            break

                        else:
                            # Adiciona à lista dos que precisam atualizar
                            opsAtualizar.append(op)
                            break
                    else:
                        # Não é igual é é o ultimo da lista que foi procurado
                        if cont == len(opsSalvas)-1:
                            # Se não estiver em nenhum lugar, será adicionado
                            opsAdicionar.append(op)

            log(obs=f"Não serão modificadas {len(ops) - len(opsAtualizar) - len(opsAdicionar)} oportunidades")

            log(obs=f"Serão adicionadas {len(opsAdicionar)} oportunidades")

            # Adicionar reuniões
            tabelaDeals.append_rows(opsAdicionar)
            log("sucesso", "Oportunidades adicionadas!")

            log(obs=f"Serão atualizadas {len(opsAtualizar)} oportunidades")

            # Procura as linhas e atualiza os valores
            for opAAtualizar in opsAtualizar:
                # Procura a linha com o op
                linhaAAtualizar = tabelaDeals.find(opAAtualizar[0], in_column=1)
                row_number = linhaAAtualizar.row

                # Define o espaço que quer atualizar
                range_linha = f"A{row_number}:AL{row_number}"
                
                # Atualiza a linha
                tabelaDeals.update(values=[opAAtualizar], range_name=range_linha)

            log("sucesso", "Oportunidades atualizadas!")

        except Exception as e:
            log("errro", f"Ocorreu um erro: {e}")


def formatOpportunities(lista:list = []):
    '''
    Recebe uma lista de oportunidades e formata para salvar na planilha
    '''
    opsFormated = []
    for op in lista:
        formatedOp = []
        custom_fields = {
            'closer': '',
            'sdr': '',
            'tipoVenda': '',
            'isOp': '',
            'dataGanho': '',
            'segmento': '',
            'funcionarios': '',
            'faturamento': '',
            'site': '',
            'desafio': '',
            'urlOrigem': '',
            'origem': '',
            'cargo': '',
            'emailCorporativo': '',
            'cidade': '',
            'score': '',
            'timeVendas': '',
            'clientesAtivos': ''
        }

        # Define os campos personalizados
        for cf in op["customFields"]:
            if cf["id"] == '8g08EFI9Qu4DlpVUxkew':
                custom_fields['closer'] = cf.get("fieldValueString", "")

            elif cf["id"] == '8Lc3bC17M065Edcob4dt':
                custom_fields['sdr'] = cf.get("fieldValueString", "")

            elif cf["id"] == 'hnAbrYxtSbJSvmzoAHpd':
                custom_fields['tipoVenda'] = cf.get("fieldValueString", "")
            
            elif cf["id"] == 'XedT4Yg1IuEU1RSVoFJQ':
                custom_fields['isOp'] = cf.get("fieldValueString", "")

            elif cf["id"] == 'gf9opjOGBMQft8FNnq5P':
                custom_fields['dataGanho'] = cf.get("fieldValueString", "") # Está em timestamp

            elif cf["id"] == 'xwmET46ovjpsN2oPTHGy':
                custom_fields['segmento'] = cf.get("fieldValueString", "") 

            elif cf["id"] == '5xpVHjUBibgmZVvMk5r4':
                custom_fields['funcionarios'] = cf.get("fieldValueString", "")

            elif cf["id"] == 'mLJtYWsRLhd5r4K24mLk':
                custom_fields['faturamento'] = cf.get("fieldValueString", "")

            elif cf["id"] == 'EUaHadhsk53lpgWVUWn5':
                custom_fields['site'] = cf.get("fieldValueString", "")

            elif cf["id"] == 'OyRGgjyylLx04EZw3gcC':
                custom_fields['desafio'] = cf.get("fieldValueString", "")

            elif cf["id"] == 'uWWUdvkMa3AApDCZfIWk':
                custom_fields['urlOrigem'] = cf.get("fieldValueString", "")

            elif cf["id"] == 'BtPyM0PeQdf2WAH8Uq3E':
                custom_fields['origem'] = cf.get("fieldValueString", "")

            elif cf["id"] == 'V2TNe5O2rB6VLYYazSI6':
                custom_fields['cargo'] = cf.get("fieldValueString", "")

            elif cf["id"] == 'YDEL68h3nFgJbfZj1mZV':
                custom_fields['emailCorporativo'] = cf.get("fieldValueString", "")

            elif cf["id"] == 'Lb7O90ZncOMJRSWbSIMA':
                custom_fields['cidade'] = cf.get("fieldValueString", "")

            elif cf["id"] == 'OKMKNuJgWNoD3R7Lqw4r':
                custom_fields['score'] = cf.get("fieldValueString", "")

            elif cf["id"] == 'KOPoVWrK61t4QRLprdeG':
                custom_fields['timeVendas'] = cf.get("fieldValueString", "")

            elif cf["id"] == 'Q5uphNMlU3W0F3lNhIIV':
                custom_fields['clientesAtivos'] = cf.get("fieldValueString", "")

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
            op.get("contact", {}).get("companyName", ""),
            op.get("contact", {}).get("email", ""),
            op.get("contact", {}).get("phone", ""),
            custom_fields['closer'],
            custom_fields['sdr'],
            custom_fields['tipoVenda'],
            custom_fields['isOp'],
            custom_fields['dataGanho'],
            custom_fields['segmento'],
            custom_fields['funcionarios'],
            custom_fields['faturamento'],
            custom_fields['site'],
            custom_fields['desafio'],
            custom_fields['urlOrigem'],
            custom_fields['origem'],
            custom_fields['cargo'],
            custom_fields['emailCorporativo'],
            custom_fields['cidade'],
            custom_fields['score'],
            custom_fields['timeVendas'],
            custom_fields['clientesAtivos'],
        ]
        opsFormated.append(formatedOp)

    atualizarOportunidades(opsFormated)


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
        initialDate = diasAntes()

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


if __name__ == "__main__":
    getOpportunities()