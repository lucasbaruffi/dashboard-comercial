from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    # Aqui você pode inserir, atualizar ou deletar no seu banco MySQL
    return jsonify({"status": "sucesso", "data": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
