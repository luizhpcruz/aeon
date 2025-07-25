"""
IA P2P Trader - FastAPI Backend
===============================

Sistema de trading peer-to-peer com inteligência artificial
para análise de mercado e execução automatizada de trades.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
from datetime import datetime
from typing import List, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="IA P2P Trader API",
    description="API para sistema de trading P2P com IA",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Modelos de dados
from pydantic import BaseModel

class TradeRequest(BaseModel):
    symbol: str
    amount: float
    trade_type: str  # "buy" or "sell"
    price: Optional[float] = None

class TradeResponse(BaseModel):
    trade_id: str
    symbol: str
    amount: float
    price: float
    status: str
    timestamp: datetime

class MarketData(BaseModel):
    symbol: str
    current_price: float
    volume: float
    change_24h: float
    timestamp: datetime

class AIAnalysis(BaseModel):
    symbol: str
    prediction: str  # "buy", "sell", "hold"
    confidence: float
    factors: List[str]
    timestamp: datetime

# Rotas da API

@app.get("/")
async def root():
    """Endpoint raiz da API."""
    return {
        "message": "IA P2P Trader API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now()
    }

@app.get("/api/health")
async def health_check():
    """Verificação de saúde do sistema."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "services": {
            "api": "running",
            "p2p_network": "connected",
            "ai_engine": "active"
        }
    }

@app.get("/api/market/{symbol}", response_model=MarketData)
async def get_market_data(symbol: str):
    """Obter dados de mercado para um símbolo específico."""
    # Simulação de dados - integrar com API real de mercado
    mock_data = MarketData(
        symbol=symbol.upper(),
        current_price=150.75,
        volume=1000000.0,
        change_24h=2.34,
        timestamp=datetime.now()
    )
    return mock_data

@app.get("/api/market/analysis/{symbol}", response_model=AIAnalysis)
async def get_ai_analysis(symbol: str):
    """Obter análise de IA para um símbolo específico."""
    # Simulação de análise - integrar com modelo de IA real
    mock_analysis = AIAnalysis(
        symbol=symbol.upper(),
        prediction="buy",
        confidence=0.78,
        factors=[
            "Tendência de alta confirmada",
            "Volume acima da média",
            "Indicadores técnicos positivos"
        ],
        timestamp=datetime.now()
    )
    return mock_analysis

@app.post("/api/trade", response_model=TradeResponse)
async def execute_trade(trade_request: TradeRequest):
    """Executar uma ordem de trade."""
    try:
        # Validar dados do trade
        if trade_request.amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount must be positive"
            )
        
        # Simular execução do trade
        trade_response = TradeResponse(
            trade_id=f"trade_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            symbol=trade_request.symbol.upper(),
            amount=trade_request.amount,
            price=trade_request.price or 150.75,
            status="executed",
            timestamp=datetime.now()
        )
        
        logger.info(f"Trade executado: {trade_response.trade_id}")
        return trade_response
        
    except Exception as e:
        logger.error(f"Erro ao executar trade: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error executing trade"
        )

@app.get("/api/trades")
async def get_trade_history():
    """Obter histórico de trades."""
    # Simulação de histórico
    return {
        "trades": [
            {
                "trade_id": "trade_20250723_142530",
                "symbol": "BTC",
                "amount": 0.1,
                "price": 45000.0,
                "status": "executed",
                "timestamp": "2025-07-23T14:25:30"
            }
        ],
        "total": 1
    }

@app.get("/api/p2p/peers")
async def get_connected_peers():
    """Obter lista de peers conectados na rede P2P."""
    return {
        "peers": [
            {"id": "peer_001", "status": "connected", "trades": 15},
            {"id": "peer_002", "status": "connected", "trades": 8}
        ],
        "total_peers": 2
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
