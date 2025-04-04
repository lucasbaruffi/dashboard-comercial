# Use uma imagem base com Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências e instala as bibliotecas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da aplicação
COPY . .

# Expõe a porta que a aplicação vai usar
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
