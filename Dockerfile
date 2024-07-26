# Use a imagem oficial do Python como base
FROM python:3.10-slim

# Instale as dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    libatlas-base-dev \
    liblapack-dev \
    libblas-dev \
    libgomp1 \
    && apt-get clean

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos do projeto
COPY . .

# Comando padrão ao iniciar o container
CMD ["python", "app.py"]
