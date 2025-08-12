# ⚡ AEON ECOSYSTEM - GUIA RÁPIDO

## 🚀 COMANDOS ESSENCIAIS

### 📁 Estrutura Básica
```bash
cd aeon-ecosystem/                    # Ir para o ecossistema
ls                                    # Listar todos os projetos
cd aeon-entropy/                      # Entrar em projeto específico
```

### 🔧 Setup Inicial
```bash
pip install -r requirements.txt      # Instalar dependências
python -m src.entropy_core           # Executar projeto
pytest tests/                        # Executar testes
```

### 🐳 Docker
```bash
docker build -t aeon-entropy .       # Build da imagem
docker run -p 8001:8001 aeon-entropy # Executar container
docker-compose up                    # Iniciar todos os serviços
```

---

## 📊 PROJETOS E PORTAS

| Projeto | Porta | Descrição |
|---------|-------|-----------|
| 🔬 aeon-entropy | 8001 | Simulador de Entropia |
| 🌌 aeon-cosmology | 8002 | Motor Cosmológico |
| 🧠 aeon-verna | 8003 | Sistema V.E.R.N.A. |
| 🤖 aeon-cosma | 8004 | Motor Inteligente |
| 🕸️ aeon-network | 8005 | Sistema P2P |
| 🎯 aeon-coordinator | 8006 | Orquestrador |
| 🌐 aeon-api | 8007 | API REST |
| 🎨 aeon-dashboard | 8008 | Interface Web |
| 🗄️ aeon-data | 8009 | Persistência |
| ☁️ aeon-deploy | 8010 | Deploy |

---

## 🔄 FLUXO DE DESENVOLVIMENTO

### 1. Escolher Projeto
```bash
cd aeon-entropy/  # ou outro projeto
```

### 2. Instalar e Testar
```bash
pip install -r requirements.txt
python -m src.entropy_core
```

### 3. Desenvolver
- Editar arquivos em `src/entropy_core/`
- Adicionar testes em `tests/`
- Atualizar documentação

### 4. Validar
```bash
pytest tests/
docker build -t aeon-entropy .
```

---

## 🛠️ ESTRUTURA DE CADA PROJETO

```
aeon-entropy/
├── src/entropy_core/     # Código principal
├── tests/                # Testes unitários
├── docs/                 # Documentação
├── configs/              # Configurações
├── data/                 # Dados
├── logs/                 # Logs
├── requirements.txt      # Dependências
├── Dockerfile           # Container
└── README.md            # Documentação
```

---

## 🎯 PRÓXIMOS PASSOS

1. **Escolha 1-2 projetos** para começar
2. **Implemente lógica específica** no módulo principal
3. **Crie testes** para validar funcionalidade
4. **Configure APIs** para comunicação entre projetos
5. **Use Docker** para deployment

---

## 🆘 COMANDOS DE TROUBLESHOOTING

```bash
# Verificar Python
python --version

# Verificar portas em uso
netstat -tulpn | grep :8001

# Limpar Docker
docker system prune -a

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Verificar logs
docker logs <container-name>
```

---

## 📝 TEMPLATES ÚTEIS

### Adicionar nova funcionalidade:
```python
# Em src/entropy_core/new_feature.py
class NewFeature:
    def __init__(self):
        pass
    
    def process(self):
        # Implementar lógica
        pass
```

### Adicionar teste:
```python
# Em tests/test_new_feature.py
def test_new_feature():
    feature = NewFeature()
    result = feature.process()
    assert result is not None
```

### Adicionar endpoint API:
```python
# Em src/entropy_core/api.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/entropy")
async def get_entropy():
    return {"status": "ok", "data": []}
```

---

## 🎉 RESUMO

✅ **10 projetos criados** com estrutura completa  
✅ **Docker configurado** para cada projeto  
✅ **Ambiente de desenvolvimento** preparado  
✅ **Documentação** completa disponível  

**🚀 Comece agora: escolha um projeto e siga os comandos essenciais!**
