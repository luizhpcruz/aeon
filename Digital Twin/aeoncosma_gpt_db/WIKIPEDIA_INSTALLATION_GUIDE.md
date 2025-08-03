
# 🌐 Guia de Instalação - Wikipedia Integration AEONCOSMA

## 📋 Pré-requisitos
- Python 3.7+
- pip funcionando
- Vector Store AEONCOSMA já configurado

## 🚀 Instalação

### Opção 1: pip tradicional
```bash
pip install wikipedia
```

### Opção 2: python -m pip
```bash
python -m pip install wikipedia
```

### Opção 3: py launcher (Windows)
```bash
py -m pip install wikipedia
```

## ✅ Validação da Instalação
```python
import wikipedia
print(wikipedia.summary("Python"))
```

## 🎯 Uso Básico
```python
from wikipedia_integration import WikipediaIntegration

# Inicializar
wiki = WikipediaIntegration()

# Buscar dados
articles = wiki.get_wikipedia_data("inteligência artificial")

# Salvar localmente
wiki.save_articles_to_db(articles)

# Integrar ao vector store
# (ver wikipedia_vector_demo.py)
```

## 🔧 Solução de Problemas

### Problema: "Python não foi encontrado"
**Solução:**
1. Instalar Python do Microsoft Store
2. Ou baixar de python.org
3. Adicionar ao PATH do sistema

### Problema: "No module named pip"
**Solução:**
```bash
python -m ensurepip --upgrade
```

### Problema: Erro de certificado SSL
**Solução:**
```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

## 💰 Custos
- Wikipedia API: **GRATUITO**
- Armazenamento local: **GRATUITO**
- Embeddings HuggingFace: **GRATUITO**
- **Total: R$ 0,00**

## 📊 Resultado Esperado
- Base expandida com artigos relevantes
- Busca semântica melhorada
- Conhecimento contextual ampliado
- Sistema 100% local e privado
