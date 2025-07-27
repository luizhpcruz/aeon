FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Criar diretório de output
RUN mkdir -p aeon/output

CMD ["python", "main.py"]
