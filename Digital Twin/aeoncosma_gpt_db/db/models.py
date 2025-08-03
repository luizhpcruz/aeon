"""
Database Models for AEONCOSMA GPT-DB
=====================================
Modelos SQLAlchemy para logs, contextos e embeddings
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class GPTConversation(Base):
    """Tabela para conversas completas"""
    __tablename__ = "gpt_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), index=True)
    user_id = Column(String(255), index=True)
    title = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON)
    
    # Relacionamento com mensagens
    messages = relationship("GPTMessage", back_populates="conversation")

class GPTMessage(Base):
    """Tabela para mensagens individuais"""
    __tablename__ = "gpt_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("gpt_conversations.id"))
    role = Column(String(50))  # user, assistant, system
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    tokens_used = Column(Integer)
    model_used = Column(String(100))
    metadata = Column(JSON)
    
    # Relacionamento
    conversation = relationship("GPTConversation", back_populates="messages")

class VectorEmbedding(Base):
    """Tabela para embeddings de contexto"""
    __tablename__ = "vector_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    embedding = Column(Text)  # JSON serialized vector
    content_type = Column(String(100))  # message, document, context
    source_id = Column(String(255))  # ID da fonte original
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)

class AEONCOSMAContext(Base):
    """Contexto específico do AEONCOSMA"""
    __tablename__ = "aeoncosma_contexts"
    
    id = Column(Integer, primary_key=True, index=True)
    context_type = Column(String(100))  # network, energy, quantum, etc.
    content = Column(Text)
    embedding_id = Column(Integer, ForeignKey("vector_embeddings.id"))
    relevance_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)
    
    # Relacionamento
    embedding = relationship("VectorEmbedding")

class SystemLog(Base):
    """Logs do sistema"""
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20))  # INFO, WARNING, ERROR
    message = Column(Text)
    component = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)
