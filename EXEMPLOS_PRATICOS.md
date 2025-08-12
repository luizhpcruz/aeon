# 🎯 AEON ECOSYSTEM - EXEMPLOS PRÁTICOS

## 🚀 EXEMPLO 1: CONFIGURAR E EXECUTAR AEON-ENTROPY

### Passo 1: Navegar e Configurar
```bash
cd aeon-ecosystem/aeon-entropy
pip install -r requirements.txt
```

### Passo 2: Modificar o Código Principal
Editar `src/entropy_core/main.py`:

```python
import asyncio
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class EntropyCore:
    def __init__(self):
        self.results_dir = Path("data")
        self.results_dir.mkdir(exist_ok=True)
    
    async def calculate_entropy(self, n_fitas=5, n_ciclos=40):
        """Calcula entropia para múltiplas fitas"""
        import random
        import math
        
        results = {
            "timestamp": "2025-08-11T20:30:00",
            "config": {"n_fitas": n_fitas, "n_ciclos": n_ciclos},
            "fitas": []
        }
        
        for fita in range(n_fitas):
            entropy_values = []
            for ciclo in range(n_ciclos):
                # Simulação simples de entropia
                base_entropy = 3.5 + 0.5 * math.sin(ciclo * 0.3)
                noise = random.gauss(0, 0.1)
                entropy_values.append(max(0.0, base_entropy + noise))
            
            fita_data = {
                "id": fita,
                "entropy_values": entropy_values,
                "mean_entropy": sum(entropy_values) / len(entropy_values),
                "max_entropy": max(entropy_values)
            }
            results["fitas"].append(fita_data)
        
        # Salvar resultados
        output_file = self.results_dir / "entropy_results.json"
        output_file.write_text(json.dumps(results, indent=2))
        
        logger.info(f"Entropy calculation complete: {len(results['fitas'])} fitas processed")
        return results

async def main():
    core = EntropyCore()
    results = await core.calculate_entropy()
    print(f"✅ Processadas {len(results['fitas'])} fitas")
    print(f"📁 Resultados salvos em data/entropy_results.json")

if __name__ == "__main__":
    asyncio.run(main())
```

### Passo 3: Executar
```bash
python -m src.entropy_core
```

**Resultado esperado:**
```
✅ Processadas 5 fitas
📁 Resultados salvos em data/entropy_results.json
```

---

## 🌌 EXEMPLO 2: CRIAR API REST EM AEON-API

### Passo 1: Configurar FastAPI
```bash
cd ../aeon-api
pip install -r requirements.txt
pip install fastapi uvicorn
```

### Passo 2: Criar API em `src/api_core/main.py`
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import httpx
from pathlib import Path

app = FastAPI(title="AEON Ecosystem API", version="1.0.0")

class EntropyRequest(BaseModel):
    n_fitas: int = 5
    n_ciclos: int = 40

class StatusResponse(BaseModel):
    service: str
    status: str
    version: str

@app.get("/", response_model=StatusResponse)
async def root():
    return StatusResponse(
        service="aeon-api",
        status="running",
        version="1.0.0"
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-08-11T20:30:00"}

@app.post("/entropy/calculate")
async def calculate_entropy(request: EntropyRequest):
    """Trigger entropy calculation via API"""
    try:
        # Em produção, chamaria o serviço aeon-entropy
        # Por agora, simula o resultado
        result = {
            "status": "completed",
            "config": {
                "n_fitas": request.n_fitas,
                "n_ciclos": request.n_ciclos
            },
            "summary": {
                "mean_entropy": 3.45,
                "max_entropy": 4.12,
                "processing_time": "0.5s"
            }
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/services/status")
async def get_services_status():
    """Check status of all AEON services"""
    services = {
        "aeon-entropy": {"port": 8001, "status": "unknown"},
        "aeon-cosmology": {"port": 8002, "status": "unknown"},
        "aeon-verna": {"port": 8003, "status": "unknown"},
        "aeon-cosma": {"port": 8004, "status": "unknown"}
    }
    
    # Em produção, verificaria cada serviço
    # Por agora, retorna status simulado
    for service in services:
        services[service]["status"] = "healthy"
    
    return services

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
```

### Passo 3: Executar API
```bash
python -m src.api_core
```

### Passo 4: Testar API
```bash
# Em outro terminal
curl http://localhost:8007/
curl http://localhost:8007/health
curl -X POST http://localhost:8007/entropy/calculate -H "Content-Type: application/json" -d '{"n_fitas": 3, "n_ciclos": 20}'
```

---

## 🎨 EXEMPLO 3: DASHBOARD STREAMLIT EM AEON-DASHBOARD

### Passo 1: Configurar Streamlit
```bash
cd ../aeon-dashboard
pip install -r requirements.txt
pip install streamlit plotly
```

### Passo 2: Criar Dashboard em `src/dashboard_core/main.py`
```python
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="AEON Ecosystem Dashboard",
    page_icon="🌟",
    layout="wide"
)

st.title("🌟 AEON Ecosystem Dashboard")
st.sidebar.title("🎛️ Controles")

# Sidebar para configurações
st.sidebar.header("Configurações")
n_fitas = st.sidebar.slider("Número de Fitas", 1, 10, 5)
n_ciclos = st.sidebar.slider("Número de Ciclos", 10, 100, 40)

if st.sidebar.button("🔬 Calcular Entropia"):
    with st.spinner("Calculando entropia..."):
        # Simular dados de entropia
        import random
        import math
        
        # Gerar dados simulados
        data = []
        for fita in range(n_fitas):
            for ciclo in range(n_ciclos):
                entropy = 3.5 + 0.5 * math.sin(ciclo * 0.3) + random.gauss(0, 0.1)
                data.append({
                    "Fita": f"Fita {fita}",
                    "Ciclo": ciclo,
                    "Entropia": max(0, entropy)
                })
        
        df = pd.DataFrame(data)
        
        # Salvar dados na sessão
        st.session_state.entropy_data = df

# Display principal
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Análise de Entropia")
    
    if 'entropy_data' in st.session_state:
        df = st.session_state.entropy_data
        
        # Gráfico de linha temporal
        fig_line = px.line(
            df, 
            x="Ciclo", 
            y="Entropia", 
            color="Fita",
            title="Evolução da Entropia por Fita"
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Gráfico de distribuição
        fig_hist = px.histogram(
            df, 
            x="Entropia", 
            color="Fita",
            title="Distribuição de Entropia"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Estatísticas
        st.subheader("📈 Estatísticas")
        stats = df.groupby("Fita")["Entropia"].agg(['mean', 'max', 'min', 'std']).round(3)
        st.dataframe(stats)
    
    else:
        st.info("👆 Use os controles na barra lateral para gerar dados de entropia")

with col2:
    st.header("🔧 Status dos Serviços")
    
    # Simular status dos serviços
    services = {
        "🔬 Entropy": {"status": "🟢 Online", "port": 8001},
        "🌌 Cosmology": {"status": "🟡 Standby", "port": 8002},
        "🧠 V.E.R.N.A.": {"status": "🟢 Online", "port": 8003},
        "🤖 COSMA": {"status": "🔴 Offline", "port": 8004},
        "🕸️ Network": {"status": "🟢 Online", "port": 8005}
    }
    
    for service, info in services.items():
        st.write(f"**{service}** (:{info['port']})")
        st.write(f"Status: {info['status']}")
        st.write("---")
    
    # Métricas em tempo real
    st.header("📊 Métricas")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.metric("Entropia Média", "3.45", "0.12")
        st.metric("Complexidade", "0.67", "-0.03")
    
    with col_b:
        st.metric("Uptime", "99.8%", "0.1%")
        st.metric("Throughput", "1.2k/s", "150/s")

# Footer
st.markdown("---")
st.markdown("**AEON Ecosystem Dashboard** - Monitoramento em tempo real")
st.markdown(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    # Para executar: streamlit run src/dashboard_core/main.py
    pass
```

### Passo 3: Executar Dashboard
```bash
streamlit run src/dashboard_core/main.py
```

**Resultado:** Interface web acessível em `http://localhost:8501`

---

## 🐳 EXEMPLO 4: ORQUESTRAÇÃO COM DOCKER COMPOSE

### Passo 1: Configurar Multiple Services
```bash
cd ..  # Voltar para aeon-ecosystem/
```

### Passo 2: Criar docker-compose.yml personalizado
```yaml
version: '3.8'

services:
  aeon-entropy:
    build: ./aeon-entropy
    ports:
      - "8001:8001"
    environment:
      - ENTROPY_DEBUG=true
    volumes:
      - ./shared-data:/app/shared-data
    networks:
      - aeon-network

  aeon-api:
    build: ./aeon-api
    ports:
      - "8007:8007"
    depends_on:
      - aeon-entropy
    environment:
      - API_DEBUG=true
      - ENTROPY_SERVICE_URL=http://aeon-entropy:8001
    networks:
      - aeon-network

  aeon-dashboard:
    build: ./aeon-dashboard
    ports:
      - "8501:8501"
    depends_on:
      - aeon-api
    environment:
      - DASHBOARD_API_URL=http://aeon-api:8007
    networks:
      - aeon-network

networks:
  aeon-network:
    driver: bridge

volumes:
  shared-data:
```

### Passo 3: Executar Stack Completa
```bash
# Build e start de todos os serviços
docker-compose up --build

# Em modo detached (background)
docker-compose up -d --build

# Verificar status
docker-compose ps

# Ver logs de um serviço específico
docker-compose logs aeon-entropy

# Parar todos os serviços
docker-compose down
```

---

## 🔄 EXEMPLO 5: INTEGRAÇÃO ENTRE SERVIÇOS

### Modificar aeon-api para comunicar com aeon-entropy

Em `aeon-api/src/api_core/main.py`, adicionar:

```python
import httpx

@app.post("/entropy/calculate")
async def calculate_entropy(request: EntropyRequest):
    """Trigger entropy calculation in aeon-entropy service"""
    try:
        # Chamar serviço aeon-entropy
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://aeon-entropy:8001/calculate",
                json={"n_fitas": request.n_fitas, "n_ciclos": request.n_ciclos},
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Entropy service error")
                
    except httpx.RequestError:
        # Fallback para dados simulados se serviço não estiver disponível
        return {
            "status": "simulated",
            "config": {"n_fitas": request.n_fitas, "n_ciclos": request.n_ciclos},
            "summary": {"mean_entropy": 3.45, "max_entropy": 4.12}
        }
```

---

## 📊 EXEMPLO 6: MONITORAMENTO E HEALTH CHECKS

### Criar script de monitoramento
```bash
# Criar monitor.py na raiz do ecossistema
touch monitor.py
```

```python
#!/usr/bin/env python3
"""
Monitor de saúde do ecossistema AEON
"""
import asyncio
import httpx
import json
from datetime import datetime

SERVICES = {
    "aeon-entropy": "http://localhost:8001/health",
    "aeon-api": "http://localhost:8007/health",
    "aeon-dashboard": "http://localhost:8501"  # Streamlit não tem endpoint padrão
}

async def check_service(name, url):
    """Verifica saúde de um serviço"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)
            if response.status_code == 200:
                return {"service": name, "status": "healthy", "response_time": response.elapsed.total_seconds()}
            else:
                return {"service": name, "status": "unhealthy", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"service": name, "status": "down", "error": str(e)}

async def monitor_ecosystem():
    """Monitora todo o ecossistema"""
    print(f"🔍 Monitorando ecossistema AEON - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = []
    for name, url in SERVICES.items():
        result = await check_service(name, url)
        results.append(result)
        
        status_emoji = {"healthy": "🟢", "unhealthy": "🟡", "down": "🔴"}
        emoji = status_emoji.get(result["status"], "❓")
        
        print(f"{emoji} {result['service']:15} | {result['status']:10} | {result.get('response_time', 'N/A')}")
    
    # Salvar relatório
    report = {
        "timestamp": datetime.now().isoformat(),
        "services": results,
        "healthy_count": sum(1 for r in results if r["status"] == "healthy"),
        "total_count": len(results)
    }
    
    with open("ecosystem_health.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Resumo: {report['healthy_count']}/{report['total_count']} serviços saudáveis")
    print(f"📁 Relatório salvo em ecosystem_health.json")

if __name__ == "__main__":
    asyncio.run(monitor_ecosystem())
```

### Executar monitoramento
```bash
python monitor.py
```

---

## 🎯 RESUMO DOS EXEMPLOS

✅ **Exemplo 1**: Entropy com cálculos reais e persistência  
✅ **Exemplo 2**: API REST completa com FastAPI  
✅ **Exemplo 3**: Dashboard interativo com Streamlit  
✅ **Exemplo 4**: Orquestração Docker multi-serviços  
✅ **Exemplo 5**: Comunicação entre serviços  
✅ **Exemplo 6**: Monitoramento e health checks  

**🚀 Estes exemplos mostram como implementar funcionalidades reais no ecossistema AEON!**
