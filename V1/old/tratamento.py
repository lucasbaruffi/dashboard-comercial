from datetime import datetime

def dataEpoch(data):
    """Recebe uma data no formato DD/MM/AAAA HH:mm e trnsforma no padrão Epoch"""
    try:
        # Se o usuário enviar apenas "DD/MM/AAAA", assume "00:00"
        if len(data) == 10:  # "DD/MM/AAAA"
            data += " 00:00"
        
        # Tenta converter a string para um objeto datetime
        data_obj = datetime.strptime(data, "%d/%m/%Y %H:%M")
        
        # Converte para timestamp em milissegundos
        timestamp_ms = int(data_obj.timestamp() * 1000)
        return timestamp_ms
    
    except ValueError:
        return "Erro: Formato inválido! Use 'DD/MM/AAAA' ou 'DD/MM/AAAA HH:mm'."