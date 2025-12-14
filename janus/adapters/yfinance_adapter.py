import yfinance as yf
import pandas as pd


def fetch_series(symbol: str, interval="1d", period="6mo"):
    df = yf.download(
        tickers=symbol,
        interval=interval,
        period=period,
        progress=False,
        auto_adjust=True
    )

    if df.empty:
        raise ValueError("No data returned from Yahoo Finance")

    # --- GARANTIA ABSOLUTA ---
    # Se vier DataFrame (MultiIndex ou não), força Series
    if isinstance(df, pd.DataFrame):
        if "Close" in df.columns:
            close = df["Close"]
        else:
            # fallback defensivo
            close = df.iloc[:, 0]
    else:
        close = df

    # Se ainda for DataFrame, reduz para Series
    if isinstance(close, pd.DataFrame):
        close = close.squeeze()

    return close.dropna().astype(float).values.tolist()
