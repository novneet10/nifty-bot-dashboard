import os
import yaml
import pandas as pd
import sqlite3

def fix_config(path="config.yaml"):
    default_config = {
        "slack": {"webhook_url": "https://hooks.slack.com/services/your/webhook/url"},
        "settings": {"dry_run": True, "market_window": {"start": "09:00", "end": "10:00"}},
        "watchlist": {
            "RELIANCE": {
                "token": 738561,
                "direction": "LONG",
                "rvol_threshold": 1.5,
                "atr_threshold": 2.0,
                "tag": "Energy"
            }
        }
    }
    with open(path, "w") as f:
        yaml.dump(default_config, f)
    print("✅ Config file reset with default values")

def fix_sqlite(path="logs/trades.sqlite"):
    os.makedirs("logs", exist_ok=True)
    conn = sqlite3.connect(path)
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
    print("✅ SQLite file and tables created")

def fix_token_mapping(path="instruments.csv"):
    df = pd.DataFrame([
        {"tradingsymbol": "RELIANCE", "instrument_token": 738561},
        {"tradingsymbol": "TATAMOTORS", "instrument_token": 884737}
    ])
    df.to_csv(path, index=False)
    print("✅ Token mapping file created with sample entries")

def run_autocorrect():
    print("🛠️ Running auto-correct...\n")
    fix_config()
    fix_sqlite()
    fix_token_mapping()

if __name__ == "__main__":
    run_autocorrect()
