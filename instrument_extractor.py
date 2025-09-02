import pandas as pd

def extract_instruments(file_path, sheet_name="Sheet1", filters=None):
    """
    Extracts instruments from Excel based on filters.
    :param file_path: Path to Excel file
    :param sheet_name: Sheet name to read
    :param filters: Dict of column:value pairs to filter
    :return: List of instrument names
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    if filters:
        for col, val in filters.items():
            df = df[df[col] == val]

    instruments = df["Instrument"].dropna().unique().tolist()
    return instruments

