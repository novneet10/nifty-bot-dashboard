"""
slack_alert.py
Utility to send alerts to Slack via Incoming Webhook.
"""

import os
import requests
import yaml

# === Load Slack Webhook URL ===
def _load_webhook_url():
    """
    Load Slack webhook URL from config.yaml or environment variable.
    Priority: ENV > config.yaml
    """
    # 1. Check environment variable
    env_url = os.getenv("SLACK_WEBHOOK_URL")
    if env_url:
        return env_url.strip()

    # 2. Check config.yaml
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f) or {}
            slack_url = config.get("slack", {}).get("webhook_url")
            if slack_url:
                return slack_url.strip()
        except Exception as e:
            print(f"⚠ Failed to read config.yaml for Slack URL: {e}")

    return None


SLACK_WEBHOOK_URL = _load_webhook_url()


# === Core Alert Function ===
def send_slack_alert(message: str, blocks: list = None):
    """
    Send a message to Slack.
    Args:
        message (str): Plain text message to send.
        blocks (list, optional): Slack Block Kit JSON for rich formatting.
    """
    if not SLACK_WEBHOOK_URL:
        print("⚠ Slack webhook URL not configured. Message not sent.")
        return False

    payload = {"text": message}
    if blocks:
        payload["blocks"] = blocks

    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
        resp.raise_for_status()
        print(f"📢 Slack alert sent: {message}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send Slack alert: {e}")
        return False


# === Example Rich Message Helper ===
def format_trade_alert(symbol, entry, exit, qty, pnl):
    """
    Create a Slack Block Kit payload for trade alerts.
    """
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Auto Square-off Executed*\n*Symbol:* {symbol}\n*Qty:* {qty}\n*Entry:* ₹{entry}\n*Exit:* ₹{exit}\n*PnL:* ₹{pnl:.2f}"
            }
        }
    ]


# === Self-test ===
if __name__ == "__main__":
    send_slack_alert("🚀 Test alert from slack_alert.py")
