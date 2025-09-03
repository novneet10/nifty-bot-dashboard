"""
start_bot.py
Fully automated Kite Connect login via Brave + local Flask redirect catcher.
Refreshes token daily, adds 30s safety countdown, then launches your trading bot.
"""

import os
import datetime
import yaml
import webbrowser
import time
from kiteconnect import KiteConnect
from flask import Flask, request
import threading

# === BOT IMPORTS ===
from signal_logic import run_signal_logic   # <-- fixed: import function, don't call here
from scheduler import start_scheduler       # <-- your scheduler file

# === CONFIG ===
# Load config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "secrets", "config.yaml")
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

API_KEY = config["API_KEY"]
API_SECRET = config["API_SECRET"]
REDIRECT_URI = config["REDIRECT_URI"

# === TOKEN MANAGEMENT ===
def save_config(api_key, api_secret, access_token):
    config_data = {
        "api_key": api_key,
        "api_secret": api_secret,
        "access_token": access_token,
        "token_generated_at": datetime.datetime.now().isoformat()
    }
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config_data, f)
    print(f"💾 Access token saved to {CONFIG_FILE}")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                return yaml.safe_load(f) or {}
            except yaml.YAMLError:
                return {}
    return {}

def is_token_expired(config):
    if "token_generated_at" not in config:
        return True
    try:
        gen_time = datetime.datetime.fromisoformat(config["token_generated_at"])
    except ValueError:
        return True
    return gen_time.date() != datetime.date.today()

# === AUTO LOGIN FLOW ===
def generate_new_token():
    kite = KiteConnect(api_key=API_KEY)
    login_url = kite.login_url() + f"&redirect_uri=http://127.0.0.1:{REDIRECT_PORT}/callback"

    app = Flask(__name__)
    token_container = {}

    @app.route("/callback")
    def callback():
        request_token = request.args.get("request_token")
        if not request_token:
            return "❌ No request_token found in redirect.", 400

        token_container["request_token"] = request_token
        return "<h2>✅ Login successful. You can close this tab now.</h2>"

    # Run Flask in background thread
    def run_flask():
        app.run(port=REDIRECT_PORT, debug=False, use_reloader=False)

    threading.Thread(target=run_flask, daemon=True).start()

    print("\n🌐 Opening Kite Connect login page in Brave...")
    webbrowser.register('brave', None, webbrowser.BackgroundBrowser(BRAVE_PATH))
    webbrowser.get('brave').open(login_url)

    # Wait until request_token is captured
    print("⏳ Waiting for login to complete in browser...")
    while "request_token" not in token_container:
        pass

    request_token = token_container["request_token"]
    print(f"✅ Captured request_token: {request_token}")

    data = kite.generate_session(request_token, api_secret=API_SECRET)
    access_token = data["access_token"]

    print(f"🎯 Access Token: {access_token}")
    save_config(API_KEY, API_SECRET, access_token)
    return access_token

def get_access_token():
    config = load_config()
    if config and "access_token" in config and not is_token_expired(config):
        print("✅ Using existing access token.")
        return config["access_token"]
    else:
        print("⚠️ No valid token found. Generating new one...")
        return generate_new_token()

# === MAIN BOT START ===
def main():
    access_token = get_access_token()

    # Initialise KiteConnect with token
    kite = KiteConnect(api_key=API_KEY)
    kite.set_access_token(access_token)

    # 30-second safety countdown
    print("\n🛡 Safety buffer: Bot will start in 30 seconds...")
    for i in range(30, 0, -1):
        print(f"Starting in {i} seconds...", end="\r")
        time.sleep(1)
    print("\n🚀 Starting bot with live token...")

    # === Your bot logic here ===
    from scheduler import start_scheduler   # <-- fixed: call your strategy function
    start_scheduler(kite)

if __name__ == "__main__":
    main()
