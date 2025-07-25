import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ScatterChart,
  Scatter
} from "recharts";
import { TrendingUp, TrendingDown, Activity, Brain, Network, AlertTriangle } from "lucide-react";

// Componentes de UI
const Card = ({ children, className = "" }) => (
  <div className={`bg-zinc-800 border border-zinc-700 rounded-lg shadow-lg ${className}`}>
    {children}
  </div>
);

const CardContent = ({ children, className = "" }) => (
  <div className={`p-6 ${className}`}>
    {children}
  </div>
);

const Button = ({ children, onClick, disabled = false, variant = "default", className = "" }) => {
  const baseClasses = "px-4 py-2 rounded-md font-medium transition-colors duration-200";
  const variants = {
    default: "bg-blue-600 hover:bg-blue-700 text-white",
    success: "bg-green-600 hover:bg-green-700 text-white",
    warning: "bg-yellow-600 hover:bg-yellow-700 text-white",
    danger: "bg-red-600 hover:bg-red-700 text-white"
  };
  
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variants[variant]} ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
    >
      {children}
    </button>
  );
};

const FractalTradingDashboard = () => {
  const [symbol, setSymbol] = useState("AAPL");
  const [marketData, setMarketData] = useState(null);
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [fractalAnalysis, setFractalAnalysis] = useState(null);
  const [p2pStatus, setP2pStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("overview");

  // Configuração da API
  const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

  // Função para buscar dados de mercado
  const fetchMarketData = async (symbolParam = symbol) => {
    try {
      const response = await axios.get(`${API_BASE}/market/${symbolParam}`);
      return response.data;
    } catch (error) {
      console.error("Erro ao buscar dados de mercado:", error);
      throw error;
    }
  };

  // Função para buscar análise de IA
  const fetchAIAnalysis = async (symbolParam = symbol) => {
    try {
      const response = await axios.get(`${API_BASE}/market/analysis/${symbolParam}`);
      return response.data;
    } catch (error) {
      console.error("Erro ao buscar análise de IA:", error);
      throw error;
    }
  };

  // Função para buscar status da rede P2P
  const fetchP2PStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE}/p2p/peers`);
      return response.data;
    } catch (error) {
      console.error("Erro ao buscar status P2P:", error);
      throw error;
    }
  };

  // Função principal de análise
  const handleAnalyze = async () => {
    if (!symbol.trim()) {
      setError("Por favor, digite um símbolo válido.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      // Buscar dados em paralelo
      const [market, ai, p2p] = await Promise.all([
        fetchMarketData(symbol.toUpperCase()),
        fetchAIAnalysis(symbol.toUpperCase()),
        fetchP2PStatus()
      ]);

      setMarketData(market);
      setAiAnalysis(ai);
      setP2pStatus(p2p);

      // Simular análise fractal (seria integrada com backend real)
      setFractalAnalysis({
        hurst_exponent: 0.65,
        box_dimension: 1.45,
        trend_type: "persistent",
        complexity: "medium",
        patterns_detected: 12,
        confidence: 0.78
      });

    } catch (err) {
      setError("Erro ao buscar dados. Verifique o símbolo e tente novamente.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Dados simulados para gráficos quando não há dados reais
  const generateDemoData = () => {
    const data = [];
    const basePrice = 150;
    for (let i = 0; i < 30; i++) {
      data.push({
        date: `2025-${String(7).padStart(2, '0')}-${String(i + 1).padStart(2, '0')}`,
        price: basePrice + Math.sin(i * 0.1) * 10 + Math.random() * 5,
        volume: 1000000 + Math.random() * 500000,
        fractal: basePrice + Math.sin(i * 0.15) * 8
      });
    }
    return data;
  };

  const chartData = marketData ? [marketData] : generateDemoData();

  // Componente de métricas
  const MetricCard = ({ title, value, change, icon: Icon, trend }) => (
    <Card className="p-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-zinc-400">{title}</p>
          <p className="text-2xl font-bold text-white">{value}</p>
          {change && (
            <p className={`text-sm flex items-center gap-1 ${trend === 'up' ? 'text-green-400' : 'text-red-400'}`}>
              {trend === 'up' ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
              {change}
            </p>
          )}
        </div>
        {Icon && <Icon size={24} className="text-blue-400" />}
      </div>
    </Card>
  );

  // Componente de sinais de trading
  const TradingSignals = () => (
    <Card>
      <CardContent>
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Brain size={20} />
          Sinais de Trading
        </h3>
        {aiAnalysis ? (
          <div className="space-y-3">
            <div className={`p-3 rounded-lg border-l-4 ${
              aiAnalysis.prediction === 'buy' ? 'border-green-500 bg-green-900/20' :
              aiAnalysis.prediction === 'sell' ? 'border-red-500 bg-red-900/20' :
              'border-yellow-500 bg-yellow-900/20'
            }`}>
              <div className="flex items-center justify-between">
                <span className="font-medium text-white">
                  {aiAnalysis.prediction === 'buy' ? '🟢 COMPRAR' :
                   aiAnalysis.prediction === 'sell' ? '🔴 VENDER' : '🟡 AGUARDAR'}
                </span>
                <span className="text-sm text-zinc-400">
                  Confiança: {Math.round(aiAnalysis.confidence * 100)}%
                </span>
              </div>
              <div className="mt-2 text-sm text-zinc-300">
                <ul>
                  {aiAnalysis.factors.map((factor, index) => (
                    <li key={index}>• {factor}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        ) : (
          <p className="text-zinc-400">Execute uma análise para ver os sinais</p>
        )}
      </CardContent>
    </Card>
  );

  // Componente de análise fractal
  const FractalAnalysis = () => (
    <Card>
      <CardContent>
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Activity size={20} />
          Análise Fractal
        </h3>
        {fractalAnalysis ? (
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-3 bg-zinc-700 rounded-lg">
              <p className="text-sm text-zinc-400">Expoente de Hurst</p>
              <p className="text-xl font-bold text-white">{fractalAnalysis.hurst_exponent}</p>
              <p className="text-xs text-zinc-500">{fractalAnalysis.trend_type}</p>
            </div>
            <div className="text-center p-3 bg-zinc-700 rounded-lg">
              <p className="text-sm text-zinc-400">Dimensão Fractal</p>
              <p className="text-xl font-bold text-white">{fractalAnalysis.box_dimension}</p>
              <p className="text-xs text-zinc-500">{fractalAnalysis.complexity}</p>
            </div>
            <div className="text-center p-3 bg-zinc-700 rounded-lg">
              <p className="text-sm text-zinc-400">Padrões Detectados</p>
              <p className="text-xl font-bold text-white">{fractalAnalysis.patterns_detected}</p>
            </div>
            <div className="text-center p-3 bg-zinc-700 rounded-lg">
              <p className="text-sm text-zinc-400">Confiança</p>
              <p className="text-xl font-bold text-white">{Math.round(fractalAnalysis.confidence * 100)}%</p>
            </div>
          </div>
        ) : (
          <p className="text-zinc-400">Execute uma análise para ver métricas fractais</p>
        )}
      </CardContent>
    </Card>
  );

  // Componente de status P2P
  const P2PStatus = () => (
    <Card>
      <CardContent>
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Network size={20} />
          Rede P2P
        </h3>
        {p2pStatus ? (
          <div className="space-y-3">
            <div className="flex justify-between items-center p-3 bg-zinc-700 rounded-lg">
              <span className="text-zinc-300">Peers Conectados</span>
              <span className="font-bold text-green-400">{p2pStatus.total_peers}</span>
            </div>
            <div className="space-y-2">
              {p2pStatus.peers.map((peer, index) => (
                <div key={index} className="flex justify-between items-center p-2 bg-zinc-800 rounded">
                  <span className="text-sm text-zinc-400">{peer.id}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-zinc-500">{peer.trades} trades</span>
                    <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <p className="text-zinc-400">Conectando à rede P2P...</p>
        )}
      </CardContent>
    </Card>
  );

  // Auto-refresh dos dados
  useEffect(() => {
    const interval = setInterval(() => {
      if (symbol && !loading) {
        fetchP2PStatus().then(setP2pStatus).catch(console.error);
      }
    }, 30000); // Atualizar a cada 30 segundos

    return () => clearInterval(interval);
  }, [symbol, loading]);

  return (
    <div className="min-h-screen bg-zinc-900 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
          🔮 Fractal P2P Trading Dashboard
        </h1>
        <p className="text-zinc-400">
          Análise fractal avançada com inteligência artificial e rede distribuída
        </p>
      </div>

      {/* Controles */}
      <Card className="mb-6">
        <CardContent>
          <div className="flex flex-col md:flex-row gap-4 items-end">
            <div className="flex-1">
              <label className="block text-sm font-medium text-zinc-300 mb-2">
                Símbolo do Ativo
              </label>
              <input
                type="text"
                placeholder="Ex: AAPL, TSLA, PETR4"
                className="w-full p-3 bg-zinc-800 border border-zinc-700 rounded-md text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
              />
            </div>
            <Button
              onClick={handleAnalyze}
              disabled={loading}
              className="px-8 py-3"
            >
              {loading ? (
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Analisando...
                </div>
              ) : (
                "🔍 Analisar"
              )}
            </Button>
          </div>
          {error && (
            <div className="mt-4 p-3 bg-red-900/20 border border-red-500 rounded-md flex items-center gap-2">
              <AlertTriangle size={16} className="text-red-400" />
              <span className="text-red-400">{error}</span>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Métricas principais */}
      {marketData && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <MetricCard
            title="Preço Atual"
            value={`$${marketData.current_price.toFixed(2)}`}
            change={`${marketData.change_24h > 0 ? '+' : ''}${marketData.change_24h.toFixed(2)}%`}
            trend={marketData.change_24h > 0 ? 'up' : 'down'}
            icon={TrendingUp}
          />
          <MetricCard
            title="Volume"
            value={`${(marketData.volume / 1000000).toFixed(1)}M`}
            icon={Activity}
          />
          <MetricCard
            title="Sinal IA"
            value={aiAnalysis?.prediction?.toUpperCase() || 'AGUARDAR'}
            change={aiAnalysis ? `${Math.round(aiAnalysis.confidence * 100)}% confiança` : null}
            icon={Brain}
          />
          <MetricCard
            title="Peers P2P"
            value={p2pStatus?.total_peers || 0}
            icon={Network}
          />
        </div>
      )}

      {/* Navegação por abas */}
      <div className="mb-6">
        <div className="flex space-x-1 bg-zinc-800 p-1 rounded-lg">
          {[
            { id: 'overview', label: 'Visão Geral' },
            { id: 'charts', label: 'Gráficos' },
            { id: 'fractal', label: 'Análise Fractal' },
            { id: 'p2p', label: 'Rede P2P' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? 'bg-blue-600 text-white'
                  : 'text-zinc-400 hover:text-white hover:bg-zinc-700'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Conteúdo das abas */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {activeTab === 'overview' && (
          <>
            <TradingSignals />
            <FractalAnalysis />
          </>
        )}

        {activeTab === 'charts' && (
          <>
            <Card>
              <CardContent>
                <h3 className="text-lg font-semibold text-white mb-4">Preços e Predições</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                      <XAxis dataKey="date" stroke="#9CA3AF" />
                      <YAxis stroke="#9CA3AF" />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: '#1F2937', 
                          border: '1px solid #374151',
                          borderRadius: '6px'
                        }}
                      />
                      <Legend />
                      <Line 
                        type="monotone" 
                        dataKey="price" 
                        stroke="#10B981" 
                        strokeWidth={2}
                        name="Preço Real"
                      />
                      <Line 
                        type="monotone" 
                        dataKey="fractal" 
                        stroke="#F59E0B" 
                        strokeWidth={2}
                        strokeDasharray="5 5"
                        name="Predição Fractal"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent>
                <h3 className="text-lg font-semibold text-white mb-4">Volume de Negociação</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                      <XAxis dataKey="date" stroke="#9CA3AF" />
                      <YAxis stroke="#9CA3AF" />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: '#1F2937', 
                          border: '1px solid #374151',
                          borderRadius: '6px'
                        }}
                      />
                      <Line 
                        type="monotone" 
                        dataKey="volume" 
                        stroke="#8B5CF6" 
                        strokeWidth={2}
                        name="Volume"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </>
        )}

        {activeTab === 'fractal' && (
          <>
            <FractalAnalysis />
            <Card>
              <CardContent>
                <h3 className="text-lg font-semibold text-white mb-4">Padrões Fractais</h3>
                <div className="space-y-4">
                  <div className="p-4 bg-zinc-700 rounded-lg">
                    <h4 className="font-medium text-white mb-2">Interpretação</h4>
                    <p className="text-sm text-zinc-300">
                      {fractalAnalysis?.hurst_exponent > 0.6 
                        ? "Série apresenta tendência persistente - movimentos passados indicam direção futura"
                        : fractalAnalysis?.hurst_exponent < 0.4
                        ? "Série apresenta comportamento anti-persistente - reversões são mais prováveis"
                        : "Movimento próximo ao aleatório - sem tendência clara definida"
                      }
                    </p>
                  </div>
                  <div className="p-4 bg-zinc-700 rounded-lg">
                    <h4 className="font-medium text-white mb-2">Complexidade</h4>
                    <p className="text-sm text-zinc-300">
                      Dimensão fractal de {fractalAnalysis?.box_dimension} indica 
                      complexidade {fractalAnalysis?.complexity} dos padrões de preço.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </>
        )}

        {activeTab === 'p2p' && (
          <>
            <P2PStatus />
            <Card>
              <CardContent>
                <h3 className="text-lg font-semibold text-white mb-4">Consensus da Rede</h3>
                <div className="space-y-3">
                  <div className="p-3 bg-zinc-700 rounded-lg">
                    <div className="flex justify-between items-center">
                      <span className="text-zinc-300">Sinal Majoritário</span>
                      <span className="px-2 py-1 bg-green-600 text-white rounded text-sm">
                        COMPRAR (67%)
                      </span>
                    </div>
                  </div>
                  <div className="p-3 bg-zinc-700 rounded-lg">
                    <div className="flex justify-between items-center">
                      <span className="text-zinc-300">Confiança da Rede</span>
                      <span className="text-green-400 font-medium">Alta (85%)</span>
                    </div>
                  </div>
                  <div className="p-3 bg-zinc-700 rounded-lg">
                    <div className="flex justify-between items-center">
                      <span className="text-zinc-300">Latência Média</span>
                      <span className="text-blue-400 font-medium">127ms</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </>
        )}
      </div>
    </div>
  );
};

export default FractalTradingDashboard;
