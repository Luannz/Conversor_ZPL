# Usa uma imagem leve do Python
FROM python:3.11-slim

# Impede o Python de gerar arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define a pasta onde o código vai morar dentro do container
WORKDIR /app

# O ponto final significa: "copie para a pasta atual (WORKDIR)"
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos (main.py, templates, etc)
COPY . .

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando para rodar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]