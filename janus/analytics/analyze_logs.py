from pathlib import Path
import pandas as pd


def analyze_file(path: Path):
    df = pd.read_csv(path, parse_dates=["timestamp"])

    symbol = df["symbol"].iloc[0]

    # Regime counts
    state_counts = df["state"].value_counts(normalize=True) * 100

    # Regime changes
    events = df[df["event"].notna() & (df["event"] != "")]
    n_regime_changes = len(events)

    # Score stats
    score_stats = df.groupby("state")["score"].agg(
        mean="mean",
        max="max",
        min="min",
        count="count"
    )

    # Durations (in steps)
    durations = (
        df["state"]
        .ne(df["state"].shift())
        .cumsum()
        .groupby(df["state"])
        .value_counts()
        .groupby(level=0)
        .mean()
    )

    print("\n" + "=" * 60)
    print(f"ASSET: {symbol}")
    print("=" * 60)

    print("\nTime in Regimes (%):")
    for state, pct in state_counts.items():
        print(f"  {state:<10}: {pct:5.1f}%")

    print(f"\nRegime changes detected: {n_regime_changes}")

    print("\nScore statistics by regime:")
    print(score_stats.round(2))

    print("\nAverage duration per regime (steps):")
    for state, avg_len in durations.items():
        print(f"  {state:<10}: {avg_len:.1f}")

    print("\nKey events:")
    for _, row in events.iterrows():
        print(f"  {row['timestamp']} | {row['event']} | score={row['score']}")


def main():
    logs_dir = Path("logs")

    if not logs_dir.exists():
        print("No logs directory found.")
        return

    for csv_file in logs_dir.glob("*.csv"):
        analyze_file(csv_file)


if __name__ == "__main__":
    main()
