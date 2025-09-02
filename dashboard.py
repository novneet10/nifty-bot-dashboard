from position_tracker import get_open_positions, get_exposure
from datetime import datetime

from db_reader import read_signals, read_pnl
import streamlit as st
import pandas as pd
import yaml
import os
from datetime import datetime

# Load config
def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

config = load_config()
watchlist = config["watchlist"]

st.set_page_config(page_title="Signal Bot Dashboard", layout="wide")

# Header
st.title("📊 Signal Bot Dashboard")
st.caption(f"Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Watchlist Overview
st.subheader("🔍 Watchlist")
watchlist_df = pd.DataFrame([
    {"Symbol": sym, "Direction": params["direction"], "Tag": params["tag"],
     "RVOL Threshold": params["rvol_threshold"], "ATR Threshold": params["atr_threshold"]}
    for sym, params in watchlist.items()
])
st.dataframe(watchlist_df)

from db_reader import read_signals

st.subheader("📈 Live Signal Status")
signal_df = read_signals()  # Pulls latest signals from SQLite
st.dataframe(signal_df)


from db_reader import read_pnl

st.subheader("📉 Risk Monitor")
pnl_df = read_pnl()

total_pnl = pnl_df["pnl"].sum()
exposure = (pnl_df["entry_price"] * pnl_df["quantity"]).sum()
capital = 10000  # Or pull from config
daily_stop = -0.02 * capital

st.metric("Exposure", f"₹{exposure:,.0f}", delta=f"{(exposure/capital)*100:.1f}% of capital")
st.metric("PnL Today", f"₹{total_pnl:,.0f}", delta="Safe" if total_pnl > daily_stop else "⚠️ Breached")
st.metric("Daily Stop", f"₹{daily_stop:,.0f}", delta="Limit")

st.subheader("📂 Open Positions")

positions = get_open_positions()

if positions:
    pos_df = pd.DataFrame([
        {
            "Symbol": sym,
            "Side": pos["side"],
            "Entry Price": pos["entry_price"],
            "Quantity": pos["quantity"],
            "Timestamp": pos["timestamp"]
        }
        for sym, pos in positions.items()
    ])
    st.dataframe(pos_df)

    # Exposure summary
    exposure = get_exposure()
    capital = 10000  # Or pull from config
    st.metric("Total Exposure", f"₹{exposure:,.0f}", delta=f"{(exposure/capital)*100:.1f}% of capital")

    # Square-off countdown
    now = datetime.now()
    cutoff = datetime.strptime(now.strftime("%Y-%m-%d") + " 15:20", "%Y-%m-%d %H:%M")
    minutes_left = int((cutoff - now).total_seconds() / 60)

    if minutes_left > 0:
        st.info(f"⏳ Auto square-off in {minutes_left} minutes")
    else:
        st.warning("⚠️ Square-off window has passed")
else:
    st.success("✅ No open positions")


# Log Viewer
st.subheader("📁 Logs")
log_date = datetime.now().strftime("%Y-%m-%d")
signal_log_path = f"logs/signal_log_{log_date}.log"
error_log_path = f"logs/error_log_{log_date}.log"

def read_log(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().splitlines()[-10:]  # Last 10 entries
    return ["No log entries found."]

st.text("🧠 Signal Log")
st.code("\n".join(read_log(signal_log_path)))

st.text("❌ Error Log")
st.code("\n".join(read_log(error_log_path)))

# Controls
st.subheader("🛑 Controls")
dry_run = config["settings"].get("dry_run", False)
if st.button("Toggle Dry-Run Mode"):
    config["settings"]["dry_run"] = not dry_run
    with open("config.yaml", "w") as f:
        yaml.dump(config, f)
    st.success(f"Dry-run mode set to {not dry_run}")

if st.button("Halt Bot"):
    st.warning("Bot halted manually.")
    # You can trigger a flag file or API call here



## 🚀 Run the Dashboard

st.markdown("To launch the dashboard manually, run:")
st.code("streamlit run dashboard.py", language="bash")

