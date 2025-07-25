#!/usr/bin/env python3
"""
P2P Trading Network Deployment Script
====================================

Script para facilitar o deployment da rede P2P de trading como servidor.
Inclui configurações para diferentes cenários de deployment.
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path


def create_docker_setup():
    """Criar configuração Docker para deployment."""
    
    # Dockerfile
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos
COPY requirements.txt .
COPY p2p_trading_server.py .
COPY p2p_trading_client.py .
COPY *.py .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Criar diretórios
RUN mkdir -p /app/logs /app/data

# Expor porta
EXPOSE 8888

# Comando padrão
CMD ["python", "p2p_trading_server.py", "--daemon", "--host", "0.0.0.0"]
"""

    # docker-compose.yml
    compose_content = """version: '3.8'

services:
  p2p-trading-server:
    build: .
    ports:
      - "8888:8888"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - SERVER_NAME=P2P-Trading-Production
    restart: unless-stopped
    networks:
      - p2p-network

  p2p-client-1:
    build: .
    command: python p2p_trading_client.py --server p2p-trading-server --auto-only
    depends_on:
      - p2p-trading-server
    restart: unless-stopped
    networks:
      - p2p-network

  p2p-client-2:
    build: .
    command: python p2p_trading_client.py --server p2p-trading-server --auto-only
    depends_on:
      - p2p-trading-server
    restart: unless-stopped
    networks:
      - p2p-network

networks:
  p2p-network:
    driver: bridge
"""

    # requirements.txt para Docker
    requirements_content = """sqlite3
asyncio
"""

    print("🐳 Criando configuração Docker...")
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)
    
    with open("requirements-docker.txt", "w") as f:
        f.write(requirements_content)
    
    print("✅ Arquivos Docker criados:")
    print("   • Dockerfile")
    print("   • docker-compose.yml")
    print("   • requirements-docker.txt")
    
    print("\n🚀 Para executar:")
    print("   docker-compose up -d")
    print("   docker-compose logs -f")


def create_systemd_service():
    """Criar serviço systemd para Linux."""
    
    current_dir = os.getcwd()
    python_path = sys.executable
    
    service_content = f"""[Unit]
Description=P2P Trading Network Server
After=network.target
Wants=network.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory={current_dir}
ExecStart={python_path} {current_dir}/p2p_trading_server.py --daemon --host 0.0.0.0
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=p2p-trading

# Segurança
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths={current_dir}

[Install]
WantedBy=multi-user.target
"""

    client_service_content = f"""[Unit]
Description=P2P Trading Client %i
After=network.target p2p-trading-server.service
Wants=p2p-trading-server.service

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory={current_dir}
ExecStart={python_path} {current_dir}/p2p_trading_client.py --auto-only --client-id client-%i
Restart=always
RestartSec=15
StandardOutput=journal
StandardError=journal
SyslogIdentifier=p2p-client-%i

[Install]
WantedBy=multi-user.target
"""

    print("🐧 Criando serviços systemd...")
    
    with open("p2p-trading-server.service", "w") as f:
        f.write(service_content)
    
    with open("p2p-trading-client@.service", "w") as f:
        f.write(client_service_content)
    
    print("✅ Arquivos de serviço criados:")
    print("   • p2p-trading-server.service")
    print("   • p2p-trading-client@.service")
    
    print("\n🚀 Para instalar (como root):")
    print("   sudo cp *.service /etc/systemd/system/")
    print("   sudo systemctl daemon-reload")
    print("   sudo systemctl enable p2p-trading-server")
    print("   sudo systemctl enable p2p-trading-client@{1..3}")
    print("   sudo systemctl start p2p-trading-server")
    print("   sudo systemctl start p2p-trading-client@{1..3}")


def create_windows_batch():
    """Criar scripts batch para Windows."""
    
    server_batch = """@echo off
title P2P Trading Server
cd /d "%~dp0"
:restart
echo Starting P2P Trading Server...
py p2p_trading_server.py --daemon --host 0.0.0.0
echo Server stopped. Restarting in 10 seconds...
timeout /t 10 /nobreak
goto restart
"""

    client_batch = """@echo off
title P2P Trading Client
cd /d "%~dp0"
:restart
echo Starting P2P Trading Client...
py p2p_trading_client.py --auto-only
echo Client stopped. Restarting in 15 seconds...
timeout /t 15 /nobreak
goto restart
"""

    install_batch = """@echo off
echo Installing P2P Trading Network as Windows Service
echo.

echo Installing Python dependencies...
py -m pip install --upgrade pip
py -m pip install pywin32

echo.
echo To install as Windows Service:
echo 1. Download NSSM from https://nssm.cc/download
echo 2. Run: nssm install P2PTradingServer
echo 3. Set Application Path: %CD%\\start_server.bat
echo 4. Set Startup type: Automatic
echo 5. Start service: nssm start P2PTradingServer

pause
"""

    print("🪟 Criando scripts Windows...")
    
    with open("start_server.bat", "w") as f:
        f.write(server_batch)
    
    with open("start_client.bat", "w") as f:
        f.write(client_batch)
    
    with open("install_windows_service.bat", "w") as f:
        f.write(install_batch)
    
    print("✅ Scripts Windows criados:")
    print("   • start_server.bat")
    print("   • start_client.bat")
    print("   • install_windows_service.bat")


def create_cloud_config():
    """Criar configurações para cloud deployment."""
    
    # AWS EC2 User Data
    aws_userdata = """#!/bin/bash
yum update -y
yum install -y python3 python3-pip git

# Clone repository (substitua pela URL real)
cd /opt
git clone https://github.com/your-repo/p2p-trading.git
cd p2p-trading

# Install dependencies
pip3 install -r requirements.txt

# Create systemd service
cp p2p-trading-server.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable p2p-trading-server
systemctl start p2p-trading-server

# Open firewall
firewall-cmd --permanent --add-port=8888/tcp
firewall-cmd --reload

# Setup log rotation
cat > /etc/logrotate.d/p2p-trading << EOF
/opt/p2p-trading/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
EOF
"""

    # Docker Swarm stack
    swarm_stack = """version: '3.8'

services:
  p2p-trading-server:
    image: p2p-trading:latest
    ports:
      - "8888:8888"
    volumes:
      - p2p-data:/app/data
      - p2p-logs:/app/logs
    environment:
      - SERVER_NAME=P2P-Trading-Swarm
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
        delay: 10s
        max_attempts: 3
      placement:
        constraints: [node.role == manager]
    networks:
      - p2p-network

  p2p-trading-client:
    image: p2p-trading:latest
    command: python p2p_trading_client.py --server p2p-trading-server --auto-only
    deploy:
      replicas: 5
      restart_policy:
        condition: on-failure
        delay: 15s
        max_attempts: 3
    networks:
      - p2p-network

volumes:
  p2p-data:
  p2p-logs:

networks:
  p2p-network:
    driver: overlay
    attachable: true
"""

    # Kubernetes deployment
    k8s_deployment = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: p2p-trading-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: p2p-trading-server
  template:
    metadata:
      labels:
        app: p2p-trading-server
    spec:
      containers:
      - name: server
        image: p2p-trading:latest
        ports:
        - containerPort: 8888
        volumeMounts:
        - name: data-volume
          mountPath: /app/data
        - name: logs-volume
          mountPath: /app/logs
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: p2p-data-pvc
      - name: logs-volume
        persistentVolumeClaim:
          claimName: p2p-logs-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: p2p-trading-service
spec:
  selector:
    app: p2p-trading-server
  ports:
  - port: 8888
    targetPort: 8888
  type: LoadBalancer
"""

    print("☁️ Criando configurações cloud...")
    
    with open("aws-userdata.sh", "w") as f:
        f.write(aws_userdata)
    
    with open("docker-swarm-stack.yml", "w") as f:
        f.write(swarm_stack)
    
    with open("k8s-deployment.yml", "w") as f:
        f.write(k8s_deployment)
    
    print("✅ Configurações cloud criadas:")
    print("   • aws-userdata.sh")
    print("   • docker-swarm-stack.yml")
    print("   • k8s-deployment.yml")


def create_monitoring_config():
    """Criar configuração de monitoramento."""
    
    # Script de monitoramento
    monitor_script = """#!/usr/bin/env python3
import requests
import time
import json
import sqlite3
from datetime import datetime

def check_server_health(host='localhost', port=8888):
    try:
        # Simular client de teste
        import socket
        import pickle
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((host, port))
        
        ping_msg = {
            'type': 'ping',
            'node_id': 'monitor',
            'timestamp': time.time()
        }
        
        s.send(pickle.dumps(ping_msg))
        response = pickle.loads(s.recv(1024))
        s.close()
        
        return True, response
    except Exception as e:
        return False, str(e)

def log_metrics():
    healthy, response = check_server_health()
    
    timestamp = datetime.now()
    status = "UP" if healthy else "DOWN"
    
    print(f"[{timestamp}] Server Status: {status}")
    
    if healthy:
        print(f"  Response: {response}")
    else:
        print(f"  Error: {response}")
    
    # Log to file
    with open('monitoring.log', 'a') as f:
        f.write(f"{timestamp},{status},{response}\\n")

if __name__ == "__main__":
    while True:
        log_metrics()
        time.sleep(60)  # Check every minute
"""

    # Prometheus config
    prometheus_config = """global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'p2p-trading'
    static_configs:
      - targets: ['localhost:8888']
    metrics_path: '/metrics'
    scrape_interval: 30s
"""

    # Grafana dashboard
    grafana_dashboard = """{
  "dashboard": {
    "title": "P2P Trading Network",
    "panels": [
      {
        "title": "Active Connections",
        "type": "stat",
        "targets": [
          {
            "expr": "p2p_active_connections"
          }
        ]
      },
      {
        "title": "Messages Per Second",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(p2p_messages_total[5m])"
          }
        ]
      }
    ]
  }
}"""

    print("📊 Criando configuração de monitoramento...")
    
    with open("monitor.py", "w") as f:
        f.write(monitor_script)
    
    with open("prometheus.yml", "w") as f:
        f.write(prometheus_config)
    
    with open("grafana-dashboard.json", "w") as f:
        f.write(grafana_dashboard)
    
    print("✅ Monitoramento configurado:")
    print("   • monitor.py")
    print("   • prometheus.yml")
    print("   • grafana-dashboard.json")


def show_monetization_guide():
    """Mostrar guia de monetização."""
    
    monetization_guide = """
💰 GUIA DE MONETIZAÇÃO - P2P TRADING NETWORK
===========================================

🎯 MODELO DE NEGÓCIO:

1. **FREEMIUM MODEL**
   • Acesso básico gratuito (dados em tempo real)
   • Premium: Análises avançadas, sinais VIP
   • Enterprise: API dedicada, SLA garantido

2. **SUBSCRIPTION TIERS**
   • Básico ($9.99/mês): 100 sinais/dia
   • Pro ($29.99/mês): Sinais ilimitados + histórico
   • Enterprise ($99.99/mês): API + suporte técnico

3. **PAY-PER-USE**
   • $0.01 por sinal de trading
   • $0.05 por análise fractal premium
   • $0.10 por backtest personalizado

4. **WHITE LABEL SOLUTIONS**
   • Licenciar tecnologia para brokers
   • $10,000 setup + $1,000/mês manutenção
   • Revenue sharing: 30% dos lucros

📊 PROJEÇÃO DE RECEITA:

Ano 1:
• 1,000 usuários gratuitos
• 100 usuários premium ($30k/ano)
• 10 clientes enterprise ($120k/ano)
• Total: $150k ARR

Ano 2:
• 5,000 usuários gratuitos
• 500 usuários premium ($180k/ano)
• 25 clientes enterprise ($300k/ano)
• 2 white labels ($240k/ano)
• Total: $720k ARR

Ano 3:
• 15,000 usuários gratuitos
• 1,500 usuários premium ($540k/ano)
• 50 clientes enterprise ($600k/ano)
• 5 white labels ($600k/ano)
• Total: $1.74M ARR

🚀 ESTRATÉGIAS DE CRESCIMENTO:

1. **NETWORK EFFECTS**
   • Quanto mais nós, melhor a precisão
   • Incentivos para operadores de nós
   • Token rewards para contribuições

2. **DATA MONETIZATION**
   • Vender dados agregados anonimizados
   • Market insights para instituições
   • Research reports premium

3. **PARTNERSHIPS**
   • Integração com exchanges
   • Parcerias com trading bots
   • Colaboração com fundos quant

4. **TECHNOLOGY LICENSING**
   • Fractal analysis IP
   • P2P consensus algorithms
   • Real-time trading infrastructure

💡 IMPLEMENTAÇÃO IMEDIATA:

1. **DEPLOY PRODUCTION SERVER**
   • AWS/Google Cloud instance
   • Load balancer + auto-scaling
   • Monitoring e alertas

2. **BUILD API GATEWAY**
   • Rate limiting por tier
   • Authentication/billing
   • Analytics dashboard

3. **DEVELOP FRONTEND**
   • Web dashboard profissional
   • Mobile app básico
   • Trading signals interface

4. **LEGAL STRUCTURE**
   • Incorporar empresa
   • Terms of service
   • Privacy policy compliance

📈 MÉTRICAS DE SUCESSO:

• Daily Active Users (DAU)
• Average Revenue Per User (ARPU)
• Churn rate < 5%
• API uptime > 99.9%
• Signal accuracy > 75%

🎯 MARCOS DE 90 DIAS:

Dia 1-30:
✅ Deploy production server
✅ Basic web interface
✅ Payment integration

Dia 31-60:
✅ Mobile app MVP
✅ Advanced analytics
✅ Customer support

Dia 61-90:
✅ Partnership outreach
✅ Marketing campaign
✅ Series A preparation

💰 POTENCIAL: $10M+ ARR em 3-5 anos
"""

    print(monetization_guide)


def main():
    """Menu principal de deployment."""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║            🚀 P2P TRADING NETWORK DEPLOYMENT 🚀             ║
║                                                              ║
║               Transforme sua rede em um ATIVO               ║
╚══════════════════════════════════════════════════════════════╝

Opções de deployment:

1. 🐳 Docker (Recomendado para desenvolvimento)
2. 🐧 SystemD Linux (Produção em servidor)
3. 🪟 Windows Services (Produção Windows)
4. ☁️  Cloud Deployment (AWS/GCP/Azure)
5. 📊 Monitoring Setup (Prometheus/Grafana)
6. 💰 Monetization Guide (Como ganhar dinheiro)
7. 🧪 Test Local Setup (Testar antes do deploy)
8. ❌ Sair
    """)
    
    while True:
        try:
            choice = input("\n🎯 Escolha uma opção (1-8): ").strip()
            
            if choice == "1":
                create_docker_setup()
            elif choice == "2":
                create_systemd_service()
            elif choice == "3":
                create_windows_batch()
            elif choice == "4":
                create_cloud_config()
            elif choice == "5":
                create_monitoring_config()
            elif choice == "6":
                show_monetization_guide()
            elif choice == "7":
                print("🧪 Testando setup local...")
                print("Executando: py p2p_trading_server.py &")
                print("Executando: py p2p_trading_client.py")
                print("💡 Execute os comandos acima em terminais separados")
            elif choice == "8":
                print("👋 Saindo...")
                break
            else:
                print("❌ Opção inválida")
                
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
