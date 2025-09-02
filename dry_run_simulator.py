import pandas as pd
import time
from signal_logic import evaluate_signal
from slack_alert import send_slack_alert
from gap_calculator import calculate_gap_pct

def simulate_feed(file_path, symbol, direction="LONG"):
    df = pd.read_csv(file_path)
    prev_close = df.iloc[0]['prev_close']
    today_open = df.iloc[0]['open']
    gap_pct = calculate_gap_pct(prev_close, today_open)

    for i in range(1, len(df)):
        tick_df = df.iloc[:i]
        if evaluate_signal(tick_df, gap_pct, direction):
            send_slack_alert(f"✅ {direction} signal for {symbol} at {tick_df.iloc[-1]['timestamp']}")
        time.sleep(0.5)  # Simulate real-time delay

# Example usage
simulate_feed("data/RELIANCE_ohlcv.csv", "RELIANCE", direction="LONG")
