"""
alert_manager.py
Unified alert dispatcher for Slack, Telegram, Email.
"""

import os
import yaml
import requests
import smtplib
from email.mime.text import MIMEText

# === Load config.yaml ===
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f) or {}

ALERTS_CFG = CONFIG.get("alerts", {})


# === Slack ===
def _send_slack(message):
    cfg = ALERTS_CFG.get("slack", {})
    if not cfg.get("enabled"):
        return
    url = cfg.get("webhook_url")
    if not url:
        print("⚠ Slack enabled but no webhook URL set.")
        return
    try:
        resp = requests.post(url, json={"text": message}, timeout=5)
        resp.raise_for_status()
        print(f"📢 Slack alert sent: {message}")
    except Exception as e:
        print(f"❌ Slack alert failed: {e}")


# === Telegram ===
def _send_telegram(message):
    cfg = ALERTS_CFG.get("telegram", {})
    if not cfg.get("enabled"):
        return
    token = cfg.get("bot_token")
    chat_id = cfg.get("chat_id")
    if not token or not chat_id:
        print("⚠ Telegram enabled but bot_token/chat_id missing.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(url, data={"chat_id": chat_id, "text": message}, timeout=5)
        resp.raise_for_status()
        print(f"📢 Telegram alert sent: {message}")
    except Exception as e:
        print(f"❌ Telegram alert failed: {e}")


# === Email ===
def _send_email(message):
    cfg = ALERTS_CFG.get("email", {})
    if not cfg.get("enabled"):
        return
    try:
        msg = MIMEText(message)
        msg["Subject"] = "Trading Bot Alert"
        msg["From"] = cfg["username"]
        msg["To"] = cfg["to"]

        with smtplib.SMTP(cfg["smtp_server"], cfg["smtp_port"]) as server:
            server.starttls()
            server.login(cfg["username"], cfg["password"])
            server.sendmail(cfg["username"], [cfg["to"]], msg.as_string())
        print(f"📢 Email alert sent: {message}")
    except Exception as e:
        print(f"❌ Email alert failed: {e}")


# === Public API ===
def send_alert(message):
    """Send alert to all enabled channels."""
    _send_slack(message)
    _send_telegram(message)
    _send_email(message)
