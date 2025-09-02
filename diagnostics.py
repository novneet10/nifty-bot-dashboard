import os
import yaml
import sqlite3
import pandas as pd
import requests

def check_config(path="config.yaml"):
    try:
        with open(path, "r") as f:
            config = yaml.safe_load(f)
        required_keys = ["slack", "settings", "watchlist"]
        for key in required_keys:
            if key not in config:
                return f"❌ Missing key in config: {key}"
        return "✅ Config file is valid"
    except Exception as e:
        return f"❌ Config error: {e}"

def check_slack(webhook_url):
    try:
        test = requests.post(webhook_url, json={"text": "🔍 Slack test from diagnostics"})
        if test.status_code == 200:
            return "✅ Slack webhook is working"
        return f"❌ Slack error: {test.text}"
    except Exception as e:
        return f"❌ Slack exception: {e}"

def check_sqlite(path="logs/trades.sqlite"):
    if not os.path.exists(path):
        return "❌ SQLite file missing"
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        if "signals" in tables and "pnl" in tables:
            return "✅ SQLite tables present"
        return f"❌ Missing tables: {tables}"
    except Exception as e:
        return f"❌ SQLite error: {e}"

def check_token_mapping(path="instruments.csv"):
    if not os.path.exists(path):
        return "❌ instruments.csv missing"
    try:
        df = pd.read_csv(path)
        if "tradingsymbol" in df.columns and "instrument_token" in df.columns:
            return "✅ Token mapping file is valid"
        return "❌ Token mapping file missing required columns"
    except Exception as e:
        return f"❌ Token mapping error: {e}"

def run_diagnostics():
    print("🔍 Running diagnostics...\n")

    config_status = check_config()
    print(config_status)

    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        slack_status = check_slack(config["slack"]["webhook_url"])
        print(slack_status)
    except:
        print("⚠️ Skipping Slack check due to config error")

    print(check_sqlite())
    print(check_token_mapping())

if __name__ == "__main__":
    run_diagnostics()
