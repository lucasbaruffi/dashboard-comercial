from flask import Flask, request
import os
from dotenv import load_dotenv
from pathlib import Path

# Carrega variáveis de ambiente
load_dotenv()

# Define o caminho absoluto para o arquivo .env (mesmo diretório)
ENV_PATH = Path(__file__).parent / '.env'

app = Flask(__name__)

@app.route('/callback')
def callback():
    """
    Endpoint que recebe o código de autorização do OAuth2
    Retorna uma mensagem amigável confirmando o recebimento
    """
    code = request.args.get('code', '')
    if code == "":
        return 'Infelizmente não consegui encontrar o código :( <br> Tente novamente'
    
    try:
        print(f"Código recebido: {code}")
        print(f"Salvando no arquivo: {ENV_PATH}")
        
        # Lê o conteúdo atual do arquivo
        with open(ENV_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Atualiza a linha do GHL_CODE
        for i, line in enumerate(lines):
            if line.startswith('GHL_CODE='):
                lines[i] = f"GHL_CODE='{code}'\n"
                break
                
        # Salva o arquivo mantendo o formato
        with open(ENV_PATH, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            
        print("Código salvo com sucesso no .env")
        
    except Exception as e:
        print(f"Erro ao salvar no .env: {str(e)}")
    
    # Salva o código em um arquivo temporário para ser lido pelo processo principal
    with open('auth_code.tmp', 'w') as f:
        f.write(code)
        
    return f'Fala meu consagrado! Code recebido: {code} <br> Já pode fechar essa aba!'

if __name__ == '__main__':
    print("Servidor rodando na porta 5000")
    app.run(debug=True, port=5000)
