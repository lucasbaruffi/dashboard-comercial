def adicionarAgendamento(data=list):

    import gspread
    from google.oauth2.service_account import Credentials
    import os
    from dotenv import load_dotenv

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

    # Autentica e cria o cliente do gspread
    client = gspread.authorize(creds)

    # Abre a planilha pelo Id
    planilha = client.open_by_key(sheetId)

    # Abre a tabela de Agendamentos
    tabela = planilha.worksheet("agendamentos")

    # Dados da nova linha a ser adicionada (lista com os valores para cada coluna)
    nova_linha = data


    # Procura o agendamento pelo ID
    busca = tabela.find(data[0], in_column=1)

    if busca:
        # Define a linha
        linha = busca.row
        print(f"Encontrada na linha {linha} da Planilha")
    else:
        print("Não encontrado")
        # Adiciona a nova linha na última linha disponível
        linhaAdicionada = tabela.append_row(nova_linha, include_values_in_response=True)

        print(f"Linha adicionada com sucesso em {linhaAdicionada.tableRange}")
