from flask import Blueprint, request

main = Blueprint('main', __name__)

@main.route('/callback')
def index():
    param = request.args.get('code', '')
    if param == "":
        return 'Infelizmente não consegui encontrar o código :( <br> Tente novamente'
    return f'Fala meu consagrado! Code recebido: {param} <br> Já pode fechar essa aba!'