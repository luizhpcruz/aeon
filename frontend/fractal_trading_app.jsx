import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const fetchStockData = async (ticker) => {
  const res = await fetch(
    `https://brapi.dev/api/quote/${ticker}?range=1mo&interval=1d`
  );
  const json = await res.json();
  if (!json.results || !json.results[0]) return [];
  return json.results[0].historicalDataPrice.map((entry) => ({
    date: entry.date,
    close: entry.close,
  }));
};

export default function FractalTradingApp() {
  const [ticker, setTicker] = useState("");
  const [data, setData] = useState([]);

  const handleFetch = async () => {
    const cleanedTicker = ticker.trim().toUpperCase();
    const stockData = await fetchStockData(cleanedTicker);
    setData(stockData.reverse());
  };

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold text-center">Fractal Trading Viewer</h1>
      <div className="flex space-x-2 justify-center">
        <Input
          placeholder="Digite o código do ativo (ex: PETR4)"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          className="w-48"
        />
        <Button onClick={handleFetch}>Buscar</Button>
      </div>

      {data.length > 0 && (
        <Card>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data}>
                <XAxis dataKey="date" hide />
                <YAxis domain={["auto", "auto"]} />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="close"
                  stroke="#4f46e5"
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
