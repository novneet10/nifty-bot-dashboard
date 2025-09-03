"""
quote_fetcher.py
Utility functions to fetch live and historical quote data from Kite Connect.
These functions expect a valid, logged-in KiteConnect instance to be passed in.
"""

from kiteconnect import KiteConnect

def get_live_data(kite: KiteConnect, symbol: str) -> dict:
    """
    Fetch the latest live market data for a given NSE symbol.
    
    Args:
        kite (KiteConnect): An authenticated KiteConnect instance.
        symbol (str): The trading symbol, e.g., "INFY", "RELIANCE".
    
    Returns:
        dict: The full quote dictionary for the symbol.
    """
    try:
        quote = kite.quote([f"NSE:{symbol}"])
        return quote.get(f"NSE:{symbol}", {})
    except Exception as e:
        print(f"❌ Error fetching live data for {symbol}: {e}")
        return {}

def get_previous_close(kite: KiteConnect, symbol: str) -> tuple:
    """
    Fetch the last traded price and previous close for a given NSE symbol.
    
    Args:
        kite (KiteConnect): An authenticated KiteConnect instance.
        symbol (str): The trading symbol, e.g., "INFY", "RELIANCE".
    
    Returns:
        tuple: (last_price, previous_close) or (None, None) if error.
    """
    try:
        quote = kite.quote([f"NSE:{symbol}"])
        data = quote.get(f"NSE:{symbol}", {})
        last_price = data.get('last_price')
        prev_close = data.get('ohlc', {}).get('close')
        return last_price, prev_close
    except Exception as e:
        print(f"❌ Error fetching previous close for {symbol}: {e}")
        return None, None
