import yaml

def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_watchlist(config):
    return config["watchlist"]

def get_slack_url(config):
    return config["slack"]["webhook_url"]

def get_market_window(config):
    return config["settings"]["market_window"]
