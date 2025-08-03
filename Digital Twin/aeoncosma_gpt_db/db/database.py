"""
Database Configuration for AEONCOSMA GPT-DB
===========================================
Configuração SQLAlchemy com suporte a múltiplos bancos
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações de banco
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/aeoncosma_gpt.db")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/chroma_db")

# Engine principal
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )
else:
    engine = create_engine(DATABASE_URL, echo=False)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

class DatabaseManager:
    """Gerenciador de banco de dados para AEONCOSMA GPT-DB"""
    
    def __init__(self):
        self.engine = engine
        self.session_factory = SessionLocal
        self.base = Base
    
    def create_tables(self):
        """Criar todas as tabelas"""
        try:
            # Criar diretório se não existir
            os.makedirs("./data", exist_ok=True)
            Base.metadata.create_all(bind=self.engine)
            return True
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
            return False
    
    def get_session(self):
        """Obter sessão do banco"""
        return self.session_factory()
    
    def close_session(self, session):
        """Fechar sessão"""
        try:
            session.close()
        except:
            pass

def get_database():
    """Dependency para FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Inicializar banco de dados"""
    # Criar diretório se não existir
    os.makedirs("./data", exist_ok=True)
    
    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_database()
