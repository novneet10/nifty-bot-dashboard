from datetime import datetime

# In-memory position store
positions = {}

def add_position(symbol, side, entry_price, quantity):
    positions[symbol] = {
        "side": side,
        "entry_price": entry_price,
        "quantity": quantity,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def close_position(symbol, exit_price):
    if symbol not in positions:
        return None

    pos = positions.pop(symbol)
    qty = pos["quantity"]
    entry = pos["entry_price"]
    side = pos["side"]

    if side == "LONG":
        pnl = (exit_price - entry) * qty
    else:
        pnl = (entry - exit_price) * qty

    return {
        "symbol": symbol,
        "side": side,
        "entry_price": entry,
        "exit_price": exit_price,
        "quantity": qty,
        "pnl": pnl,
        "closed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def get_open_positions():
    return positions

def get_exposure():
    return sum(pos["entry_price"] * pos["quantity"] for pos in positions.values())

def auto_square_off(cutoff_time="15:20"):
    now = datetime.now().strftime("%H:%M")
    if now >= cutoff_time:
        closed = []
        for symbol in list(positions.keys()):
            # Simulate square-off at last known price (mocked here)
            exit_price = positions[symbol]["entry_price"]  # Replace with LTP
            closed.append(close_position(symbol, exit_price))
        return closed
    return []
