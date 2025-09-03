"""
scheduler.py
Schedules daily launch checks, signal logic runs, and auto square-off.
Works with the latest signal_logic.py and start_bot.py.
"""

import schedule
import time
from datetime import datetime
from launch_check import run_launch_check
from signal_logic import run_signal_logic
#from slack_alert import send_slack_alert
from alert_manager import send_alert
from position_tracker import auto_square_off
from logger_sqlite import log_trade

# === Scheduled Jobs ===

def scheduled_launch_check():
    """Run diagnostics and auto-correct before market open."""
    run_launch_check()
    send_slack_alert("🛠 Launch check completed.")

def scheduled_signal_check(kite):
    """Run the trading signal logic during market hours."""
    now = datetime.now().strftime("%H:%M")
    # Example: run between 09:15 and 15:15
    if "09:15" <= now <= "15:15":
        send_slack_alert(f"📊 Running signal check at {now}...")
        run_signal_logic(kite)
    else:
        print(f"⏸ Outside trading hours ({now}), skipping signal check.")

def scheduled_auto_square_off(kite):
    """Close open positions and log them."""
    closed_positions = auto_square_off(kite)
    for pos in closed_positions:
        log_trade(pos["symbol"], pos["entry_price"], pos["exit_price"], pos["quantity"])
        send_slack_alert(
            f"⏳ Auto square-off: {pos['symbol']} | PnL: ₹{pos['pnl']:.2f}"
        )

# === Scheduler Start ===

def start_scheduler(kite):
    """
    Start the scheduler loop.
    Args:
        kite (KiteConnect): Authenticated KiteConnect instance from start_bot.py
    """
    # Daily pre-market launch check
    schedule.every().day.at("08:55").do(scheduled_launch_check)

    # Signal logic every minute during market hours
    schedule.every(1).minutes.do(lambda: scheduled_signal_check(kite))

    # Auto square-off near market close (example: 15:20)
    schedule.every().day.at("15:20").do(lambda: scheduled_auto_square_off(kite))

    print("📅 Scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(1)
