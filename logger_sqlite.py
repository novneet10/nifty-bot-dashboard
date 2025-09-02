import sqlite3
from datetime import datetime
import os

DB_PATH = "logs/trades.sqlite"

def init_db():
    """Create the database and tables if they don't exist."""
    os.makedirs("logs", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            direction TEXT,
            timestamp TEXT,
            gap_pct REAL,
            rvol REAL,
            atr REAL,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pnl (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            entry_price REAL,
            exit_price REAL,
            quantity INTEGER,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

def log_signal(symbol, direction, gap_pct, rvol, atr, status):
    """Insert a signal evaluation into the signals table."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO signals (symbol, direction, timestamp, gap_pct, rvol, atr, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (symbol, direction, timestamp, gap_pct, rvol, atr, status))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Error logging signal for {symbol}: {e}")

def log_trade(symbol, entry_price, exit_price, quantity):
    """Insert a completed trade into the pnl table."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO pnl (symbol, entry_price, exit_price, quantity, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (symbol, entry_price, exit_price, quantity, timestamp))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Error logging trade for {symbol}: {e}")

from logger_sqlite import log_trade

#result = close_position("RELIANCE", exit_price=2480.0)
#if result:
#    log_trade(result["symbol"], result["entry_price"], result["exit_price"], result["quantity"])
