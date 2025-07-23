// Updated Fractal Trading Viewer with improved dark theme and input bar
import React, { useState } from "react";
import {
  Card,
  CardContent,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const FractalTradingViewer = () => {
  const [symbol, setSymbol] = useState("");
  const [data, setData] = useState([]);

  const handleFetch = async () => {
    // Simulated API call (mock)
    const mockData = [
      { time: "2023-07-01", price: 100 },
      { time: "2023-07-02", price: 102 },
      { time: "2023-07-03", price: 99 },
    ];
    setData(mockData);
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
        <Button className="mt-2" onClick={handleFetch}>
          Buscar Dados
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {data.map((item, index) => (
          <Card key={index} className="bg-zinc-800 text-white">
            <CardContent>
              <p><strong>Data:</strong> {item.time}</p>
              <p><strong>Preço:</strong> R${item.price}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default FractalTradingViewer;
