from launch_check import run_launch_check
import schedule
import time
from datetime import datetime
from signal_logic import evaluate_signal
from slack_alert import send_slack_alert

# Run diagnostics + auto-correct at 08:55
schedule.every().day.at("08:55").do(run_launch_check)


def run_signal_check():
    now = datetime.now().strftime("%H:%M")
    if "09:00" <= now <= "10:00":
        # Replace with real data loading
        df = pd.read_csv("data/sample_ohlcv.csv")
        gap_pct = 1.2  # Replace with actual gap calculation
        if evaluate_signal(df, gap_pct, direction="LONG"):
            send_slack_alert("✅ LONG signal confirmed.")
        elif evaluate_signal(df, gap_pct, direction="SHORT"):
            send_slack_alert("✅ SHORT signal confirmed.")
        else:
            print("No signal at this time.")

# Schedule to run every minute
schedule.every(1).minutes.do(run_signal_check)

def start_scheduler():
    print("Scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(1)

from position_tracker import auto_square_off
from logger_sqlite import log_trade

closed_positions = auto_square_off()

for pos in closed_positions:
    log_trade(pos["symbol"], pos["entry_price"], pos["exit_price"], pos["quantity"])
    send_slack_alert(f"⏳ Auto square-off: {pos['symbol']} | PnL: ₹{pos['pnl']:.2f}")

def start_scheduler():
    print("📅 Scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(1)
