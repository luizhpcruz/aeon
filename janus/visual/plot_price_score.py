import pandas as pd
import matplotlib.pyplot as plt


def plot_price_and_score(csv_path="data/janus_log.csv"):
    # =========================
    # Load data
    # =========================
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])

    # Safety sort
    df = df.sort_values("timestamp").reset_index(drop=True)

    # =========================
    # Figure setup
    # =========================
    plt.style.use("dark_background")
    fig, ax1 = plt.subplots(figsize=(14, 6))

    # =========================
    # Regime background
    # =========================
    regime_colors = {
        "Normal": "#003300",
        "Attention": "#665500",
        "Stress": "#660000",
    }

    current_state = None
    start_time = None

    for _, row in df.iterrows():
        if row["state"] != current_state:
            if current_state is not None:
                ax1.axvspan(
                    start_time,
                    row["timestamp"],
                    color=regime_colors[current_state],
                    alpha=0.18,
                )
            current_state = row["state"]
            start_time = row["timestamp"]

    # Close last regime
    if current_state is not None:
        ax1.axvspan(
            start_time,
            df["timestamp"].iloc[-1],
            color=regime_colors[current_state],
            alpha=0.18,
        )

    # =========================
    # Price plot
    # =========================
    ax1.plot(
        df["timestamp"],
        df["price"],
        color="white",
        linewidth=1.6,
        label="Price",
    )

    ax1.set_ylabel("Price", color="white")
    ax1.tick_params(axis="y", labelcolor="white")

    # =========================
    # Score axis
    # =========================
    ax2 = ax1.twinx()

    ax2.plot(
        df["timestamp"],
        df["score"],
        color="orange",
        linewidth=1.4,
        label="Anomaly Score",
    )

    ax2.set_ylim(0, 100)
    ax2.set_ylabel("Anomaly Score", color="orange")
    ax2.tick_params(axis="y", labelcolor="orange")

    # =========================
    # Score bands
    # =========================
    ax2.axhspan(0, 30, color="green", alpha=0.08)
    ax2.axhspan(30, 60, color="yellow", alpha=0.08)
    ax2.axhspan(60, 100, color="red", alpha=0.08)

    # =========================
    # Regime change markers
    # =========================
    events = df[df["event"].notna() & (df["event"] != "")]

    for _, row in events.iterrows():
        ax1.axvline(
            row["timestamp"],
            color="red",
            linestyle="--",
            alpha=0.85,
            linewidth=1,
        )

    # =========================
    # Title & legend
    # =========================
    symbol = df["symbol"].iloc[0]
    plt.title(f"JANUS — {symbol} | Price vs Structural Anomaly Score")

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()

    ax1.legend(
        lines_1 + lines_2,
        labels_1 + labels_2,
        loc="upper left",
        frameon=False,
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_price_and_score()
