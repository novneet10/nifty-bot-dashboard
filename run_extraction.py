from instrument_extractor import extract_instruments
from slack_alert import send_slack_alert

filters = {"Status": "Active", "Sector": "Logistics"}
instruments = extract_instruments("input_data.xlsx", filters=filters)

msg = f"Extracted {len(instruments)} instruments: {', '.join(instruments)}"
send_slack_alert(msg, webhook_url="https://hooks.slack.com/services/...")
