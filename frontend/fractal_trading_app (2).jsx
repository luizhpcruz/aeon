import React, { useState } from "react";
import {
  Card,
  CardContent,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

// Substitua por sua chave real da API
const API_KEY = "demo"; // <-- Troque por sua chave real da AlphaVantage se quiser dados reais

const FractalTradingViewer = () => {
  const [symbol, setSymbol] = useState("");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFetch = async () => {
    if (!symbol) {
      setError("Por favor, digite um símbolo.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const res = await fetch(
        `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=${symbol}&apikey=${API_KEY}`
      );
      const json = await res.json();

      if (json["Time Series (Daily)"]) {
        const rawData = json["Time Series (Daily)"];
        const formattedData = Object.entries(rawData)
          .slice(0, 5)
          .map(([date, value]) => ({
            time: date,
            price: parseFloat(value["4. close"]),
          }))
          .reverse();

        setData(formattedData);
      } else {
        setError("Símbolo inválido ou limite de requisições excedido.");
        setData([]);
      }
    } catch (err) {
      setError("Erro ao buscar dados.");
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="bg-zinc-900 text-white min-h-screen p-6">
      <h1 className="text-3xl font-bold mb-4">Fractal Trading Viewer</h1>

      <div className="mb-4">
        <input
          type="text"
          placeholder="Digite o símbolo da ação (ex: PETR4)"
          className="p-2 rounded bg-zinc-800 text-white border border-zinc-700 w-full md:w-1/3"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
        />
        <Button className="mt-2" onClick={handleFetch} disabled={loading}>
          {loading ? "Buscando..." : "Buscar Dados"}
        </Button>
        {error && <p className="text-red-500 mt-2">{error}</p>}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {data.map((item, index) => (
          <Card key={index} className="bg-zinc-800 text-white">
            <CardContent>
              <p><strong>Data:</strong> {item.time}</p>
              <p><strong>Preço:</strong> R${item.price.toFixed(2)}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default FractalTradingViewer;
