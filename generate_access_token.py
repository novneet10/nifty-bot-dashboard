"""
Auto-login & Access Token Generator for Zerodha Kite Connect
Author: Novneet
"""

from kiteconnect import KiteConnect
from urllib.parse import urlparse, parse_qs
import yaml
import os
import datetime
import webbrowser

# --- CONFIG ---
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
CONFIG_FILE = "config.yaml"

# Path to Brave browser executable (update if installed elsewhere)
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

def save_config(api_key, api_secret, access_token):
    config_data = {
        "api_key": api_key,
        "api_secret": api_secret,
        "access_token": access_token,
        "token_generated_at": datetime.datetime.now().isoformat()
    }
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config_data, f)
    print(f"\n💾 Access token saved to {CONFIG_FILE}")

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
    today = datetime.date.today()
    return gen_time.date() != today

def generate_new_token():
    kite = KiteConnect(api_key=API_KEY)
    login_url = kite.login_url()

    print("\n🌐 Opening Kite Connect login page in Brave...")
    webbrowser.register('brave', None, webbrowser.BackgroundBrowser(BRAVE_PATH))
    webbrowser.get('brave').open(login_url)

    redirect_url = input("\n🔑 After login, copy the FULL redirect URL from the address bar and paste it here:\n> ").strip()
    parsed_url = urlparse(redirect_url)
    query_params = parse_qs(parsed_url.query)

    if "request_token" not in query_params:
        print("\n❌ Could not find 'request_token' in the URL. Make sure you pasted the full redirect URL.")
        exit(1)

    request_token = query_params["request_token"][0]
    print(f"\n✅ Extracted request_token: {request_token}")

    data = kite.generate_session(request_token, api_secret=API_SECRET)
    access_token = data["access_token"]

    print(f"\n🎯 Your ACCESS TOKEN is:\n{access_token}")
    save_config(API_KEY, API_SECRET, access_token)

def main():
    config = load_config()

    if config and "access_token" in config and not is_token_expired(config):
        print("✅ Existing access token is still valid for today.")
        print(f"Access Token: {config['access_token']}")
    else:
        print("⚠️ No valid token found or token expired. Generating a new one...")
        generate_new_token()

if __name__ == "__main__":
    main()

