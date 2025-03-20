from flask import Flask, request
from dotenv import load_dotenv, set_key
from pathlib import Path

# Carrega variáveis de ambiente
load_dotenv()

# Define o caminho absoluto para o arquivo .env
ENV_PATH = str(Path(__file__).parent / '.env')

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
        
        # Atualiza o código usando set_key
        set_key(ENV_PATH, "GHL_CODE", code)
            
        print("Código salvo com sucesso no .env")
        
    except Exception as e:
        print(f"Erro ao salvar no .env: {str(e)}")
            
    return f'Fala meu consagrado! Code recebido: {code} <br> Já pode fechar essa aba!'

if __name__ == '__main__':
    print("Servidor rodando na porta 5000")
    app.run(debug=True, port=5000)
