"""
signal_logic.py
Core trading signal logic for the bot.
Loads watchlist and per-symbol parameters from config.yaml.
Uses quote_fetcher for market data.
"""

import yaml
import os
from quote_fetcher import get_live_data, get_previous_close

CONFIG_FILE = "config.yaml"

def load_watchlist_config():
    """
    Load watchlist and per-symbol settings from config.yaml.

    Expected YAML structure:
    watchlist:
      - symbol: INFY
        quantity: 50
        buy_threshold: 1.01   # 1% above prev close
        sell_threshold: 0.99  # 1% below prev close
        order_type: MARKET
      - symbol: RELIANCE
        quantity: 20
        buy_threshold: 1.02
        sell_threshold: 0.98
        order_type: LIMIT
    """
    if not os.path.exists(CONFIG_FILE):
        print(f"⚠️ Config file {CONFIG_FILE} not found. Using empty watchlist.")
        return []

    try:
        with open(CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f) or {}
        watchlist = config.get("watchlist", [])
        if not isinstance(watchlist, list):
            print("⚠️ 'watchlist' in config is not a list. Using empty watchlist.")
            return []
        return watchlist
    except Exception as e:
        print(f"❌ Error loading watchlist from {CONFIG_FILE}: {e}")
        return []

def run_signal_logic(kite):
    """
    Main entry point for running the trading signal logic.
    
    Args:
        kite (KiteConnect): An authenticated KiteConnect instance.
    """
    watchlist_config = load_watchlist_config()
    if not watchlist_config:
        print("⚠️ No symbols in watchlist. Exiting signal logic.")
        return

    print("📊 Running signal logic with config-based parameters...")

    for item in watchlist_config:
        symbol = item.get("symbol")
        qty = item.get("quantity", 1)
        buy_threshold = item.get("buy_threshold", 1.01)   # default 1% above prev close
        sell_threshold = item.get("sell_threshold", 0.99) # default 1% below prev close
        order_type = item.get("order_type", "MARKET")

        if not symbol:
            print("⚠️ Skipping entry with no symbol.")
            continue

        # Fetch live data
        live_data = get_live_data(kite, symbol)
        if not live_data:
            print(f"⚠️ Skipping {symbol} — no live data returned.")
            continue

        last_price = live_data.get("last_price")
        prev_close = live_data.get("ohlc", {}).get("close")

        if last_price is None or prev_close is None:
            print(f"⚠️ Skipping {symbol} — missing price data.")
            continue

        print(f"🔹 {symbol}: Last Price = {last_price}, Prev Close = {prev_close}")

        # === Parameterized signal logic ===
        if last_price > prev_close * buy_threshold:
            print(f"📈 BUY signal for {symbol} | Qty: {qty} | Order: {order_type}")
            # Place order logic here
        elif last_price < prev_close * sell_threshold:
            print(f"📉 SELL signal for {symbol} | Qty: {qty} | Order: {order_type}")
            # Place order logic here
        else:
            print(f"⏸ No trade signal for {symbol}")

    print("✅ Signal logic run complete.")
