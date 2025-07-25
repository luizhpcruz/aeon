FROM python:3.9-slim

WORKDIR /app

# Instalar depend�ncias do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos
COPY requirements.txt .
COPY p2p_trading_server.py .
COPY p2p_trading_client.py .
COPY *.py .

# Instalar depend�ncias Python
RUN pip install --no-cache-dir -r requirements.txt

# Criar diret�rios
RUN mkdir -p /app/logs /app/data

# Expor porta
EXPOSE 8888

# Comando padr�o
CMD ["python", "p2p_trading_server.py", "--daemon", "--host", "0.0.0.0"]
