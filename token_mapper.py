import pandas as pd

def load_token_map(file_path="instruments.csv"):
    df = pd.read_csv(file_path)
    df = df[df['exchange'] == 'NSE']  # Filter for NSE stocks
    return dict(zip(df['tradingsymbol'], df['instrument_token']))

def get_token(symbol, token_map):
    return token_map.get(symbol)
