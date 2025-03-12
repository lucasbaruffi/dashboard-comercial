def adicionarAgendamento(data=list):

    import gspread
    from google.oauth2.service_account import Credentials
    import os
    from dotenv import load_dotenv
    import time

    # Carrega as variáveis de Ambiente
    load_dotenv()

    # Define o Id da Planilha
    sheetId = os.getenv("GOOGLE_SHEET_KEY")

    # Define os escopos de acesso: planilhas e drive
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Carrega as credenciais a partir do arquivo JSON
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)

    try:
        # Autentica e cria o cliente do gspread
        client = gspread.authorize(creds)

        # Abre a planilha pelo Id
        planilha = client.open_by_key(sheetId)

        # Abre a tabela de Agendamentos
        tabela = planilha.worksheet("agendamentos")
    except Exception as e:
        print(f"Erro ao acessar a planilha: {e}")
        return

    # Dados da nova linha a ser adicionada (lista com os valores para cada coluna)
    nova_linha = data

    try:
        # Procura o agendamento pelo ID
        busca = tabela.find(data[0], in_column=1)

        if busca:
            # Define a linha
            linha = busca.row
            print(f"Encontrada na linha {linha} da Planilha")
            # Atualiza a linha com os novos dados
            tabela.update(f"A{linha}", [nova_linha])
        else:
            # Adiciona a nova linha na última linha disponível
            linhaAdicionada = tabela.append_row(nova_linha, include_values_in_response=True)
            print(f"Linha adicionada com sucesso em {linhaAdicionada['updates']['updatedRange']}")

        # Pausa para respeitar o limite de taxa da API
        time.sleep(0.2)  # 300 requests per minute = 1 request every 0.2 seconds
    except Exception as e:
        print(f"Erro ao manipular a planilha: {e}")
