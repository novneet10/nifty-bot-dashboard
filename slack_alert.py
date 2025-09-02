import requests
import yaml

def get_slack_url():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config["slack"]["webhook_url"]

def send_slack_alert(message, webhook_url=None):
    if webhook_url is None:
        webhook_url = get_slack_url()
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 200:
            print(f"❌ Slack error: {response.text}")
    except Exception as e:
        print(f"❌ Slack exception: {e}")
