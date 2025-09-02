from kiteconnect import KiteConnect

API_KEY = "your_api_key"
ACCESS_TOKEN = "your_access_token"

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

def get_previous_close(symbol):
    quote = kite.quote([f"NSE:{symbol}"])
    return quote[f"NSE:{symbol}"]['last_price'], quote[f"NSE:{symbol}"]['ohlc']['close']
