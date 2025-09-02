from scheduler import start_scheduler

if __name__ == "__main__":
    start_scheduler()

from zerodha_feed import start_feed

if __name__ == "__main__":
    start_feed()

import logging
from datetime import datetime

def setup_logger():
    date_str = datetime.now().strftime("%Y-%m-%d")
    logging.basicConfig(
        filename=f"logs/signal_log_{date_str}.log",
        level=logging.INFO,
        format="%(asctime)s - %(message)s"
    )

def log_signal(symbol, message):
    logging.info(f"{symbol}: {message}")

if config["settings"].get("dry_run"):
    simulate_feed("data/RELIANCE_ohlcv.csv", "RELIANCE")
else:
    start_feed()

try:
    today_open, prev_close = get_previous_close(symbol)
    gap_pct = calculate_gap_pct(prev_close, today_open)
except Exception as e:
    log_signal(symbol, f"Error fetching quote: {e}")
    continue

from logger_sqlite import init_db, log_signal, log_trade
from slack_alert import send_slack_alert, format_alert
from signal_logic import evaluate_signal
from gap_calculator import calculate_gap_pct
from quote_fetcher import get_previous_close

# Initialize DB once at startup
init_db()

for symbol, params in watchlist.items():
    try:
        # Fetch prices
        today_open, prev_close = get_previous_close(symbol)
        gap_pct = calculate_gap_pct(prev_close, today_open)

        # Get live OHLCV data (from WebSocket or simulator)
        df = get_live_ohlcv(params["token"])
        latest = df.iloc[-1]
        rvol = latest["rvol"]
        atr = latest["atr"]

        # Evaluate signal
        triggered = evaluate_signal(
            df, gap_pct,
            direction=params["direction"],
            rvol_thresh=params["rvol_threshold"],
            atr_thresh=params["atr_threshold"]
        )

        timestamp = latest["timestamp"]
        status = "Triggered" if triggered else "Rejected"

from position_tracker import add_position

# After signal is confirmed
entry_price = latest["close"]  # or use LTP from Zerodha
quantity = 4  # or calculate based on capital/exposure logic

add_position(symbol, params["direction"], entry_price, quantity)

        # Log signal
        log_signal(symbol, params["direction"], gap_pct, rvol, atr, status)

        # Send alert if triggered
        if triggered:
            alert_msg = format_alert(symbol, params["direction"], params["tag"], timestamp)
            send_slack_alert(alert_msg)

    except Exception as e:
        error_msg = f"❌ Error for {symbol}: {str(e)}"
        send_slack_alert(error_msg)
        log_signal(symbol, params["direction"], 0, 0, 0, f"Error: {str(e)}")
        continue

