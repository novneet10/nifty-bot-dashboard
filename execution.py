from logger_sqlite import log_trade
from slack_alert import send_slack_alert

def execute_trade(symbol, side, entry_price, exit_price, quantity):
    """
    Simulates trade execution and logs it.
    Replace this with actual broker API calls when ready.
    """
    # Simulate execution
    print(f"Executing {side} trade for {symbol} | Qty: {quantity} | Entry: ₹{entry_price} | Exit: ₹{exit_price}")

    # Log trade to SQLite
    log_trade(symbol, entry_price, exit_price, quantity)

    # Calculate PnL
    if side == "LONG":
        pnl = (exit_price - entry_price) * quantity
    else:
        pnl = (entry_price - exit_price) * quantity

from position_tracker import close_position
from logger_sqlite import log_trade

#exit_price = latest["close"]  # or use LTP
#result = close_position(symbol, exit_price)

def execute_trade(symbol, side, entry_price, exit_price, quantity):
    # Simulate execution
    print(f"Executing {side} trade for {symbol} | Qty: {quantity} | Entry: ₹{entry_price} | Exit: ₹{exit_price}")

    # Log trade to SQLite
    log_trade(symbol, entry_price, exit_price, quantity)

    # Calculate PnL
    if side == "LONG":
        pnl = (exit_price - entry_price) * quantity
    else:
        pnl = (entry_price - exit_price) * quantity

    # Send Slack alert
    send_slack_alert(
        f"💰 Trade executed: {symbol} | {side} | Qty: {quantity} | Entry: ₹{entry_price} | Exit: ₹{exit_price} | PnL: ₹{pnl:.2f}"
    )
