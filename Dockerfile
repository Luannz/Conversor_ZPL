# Usa uma imagem leve do Python
FROM python:3.11-slim

# Define a pasta onde o código vai morar dentro do container
WORKDIR /app

# Copia os arquivos do seu PC/GitHub para dentro do container
COPY . /app

# Instala as bibliotecas
RUN pip install --no-cache-dir fastapi uvicorn pillow python-multipart jinja2

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando para rodar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]