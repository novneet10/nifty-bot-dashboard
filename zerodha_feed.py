from kiteconnect import KiteTicker
import pandas as pd
from datetime import datetime
from signal_logic import evaluate_signal
from slack_alert import send_slack_alert

API_KEY = "your_api_key"
ACCESS_TOKEN = "your_access_token"
tokens = [738561, 5633]  # Example instrument tokens

kite_ws = KiteTicker(API_KEY, ACCESS_TOKEN)

ohlcv_data = {token: [] for token in tokens}

def on_ticks(ws, ticks):
    for tick in ticks:
        token = tick['instrument_token']
        ts = datetime.fromtimestamp(tick['timestamp']).strftime('%H:%M')
        ohlcv_data[token].append({
            'timestamp': ts,
            'open': tick['ohlc']['open'],
            'high': tick['ohlc']['high'],
            'low': tick['ohlc']['low'],
            'close': tick['last_price'],
            'volume': tick['volume']
        })

        # Evaluate signal every minute
        if ts >= "09:00" and ts <= "10:00" and ts.endswith(":00"):
            df = pd.DataFrame(ohlcv_data[token])
            gap_pct = 1.2  # Replace with actual gap logic
            if evaluate_signal(df, gap_pct, direction="LONG"):
                send_slack_alert(f"✅ LONG signal for token {token}")
            elif evaluate_signal(df, gap_pct, direction="SHORT"):
                send_slack_alert(f"✅ SHORT signal for token {token}")

def on_connect(ws, response):
    ws.subscribe(tokens)

def on_close(ws, code, reason):
    print("WebSocket closed:", reason)

kite_ws.on_ticks = on_ticks
kite_ws.on_connect = on_connect
kite_ws.on_close = on_close

def start_feed():
    kite_ws.connect(threaded=True)

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
