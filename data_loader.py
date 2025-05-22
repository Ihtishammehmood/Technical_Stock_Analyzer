import yfinance as yf
import streamlit as st
import pandas as pd

@st.cache_data
def get_sp500_components():
    """Fetches the list of S&P 500 companies from Wikipedia."""
    df = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    df = df[0]
    tickers = df["Symbol"].to_list()
    tickers_companies_dict = dict(zip(df["Symbol"], df["Security"]))
    return tickers, tickers_companies_dict

@st.cache_data
def load_data(symbol, start, end):
    """
    Loads historical stock data for a given symbol and date range.
    Handles MultiIndex columns and standardizes column names.
    """
    data = yf.download(symbol, start, end)

    # Fix for MultiIndex columns - flatten the columns if they are MultiIndex
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [' '.join(col).strip() for col in data.columns.values]

    # Ensure standard column names (Open, High, Low, Close, Volume)
    # Map common variations to standard names
    standard_cols = {
        'Open': 'Open',
        'High': 'High',
        'Low': 'Low',
        'Close': 'Close',
        'Volume': 'Volume',
        'Adj Close': 'Adj Close'
    }

    # Create a mapping for the actual columns in the dataframe
    actual_mapping = {}

    # First, try to find exact matches
    for std_col in standard_cols:
        if std_col in data.columns:
            actual_mapping[std_col] = std_col

    # If we don't have all standard columns, look for ticker-specific columns
    # (like "Open MMM", "Close MMM", etc.)
    if len(actual_mapping) < len(standard_cols):
        for col in data.columns:
            for std_col in standard_cols:
                # Check if column starts with standard name (e.g., "Open MMM" starts with "Open")
                if col.startswith(std_col + " ") or col == std_col:
                    actual_mapping[col] = std_col
                # Also check lowercase variations
                elif col.lower().startswith(std_col.lower() + " ") or col.lower() == std_col.lower():
                    actual_mapping[col] = std_col

    # Rename columns if needed
    if actual_mapping:
        data = data.rename(columns=actual_mapping)

    # Debug info
    st.sidebar.write("Available columns:", ", ".join(data.columns))

    return data

@st.cache_data
def convert_df_to_csv(df):
    """Converts a DataFrame to a CSV file for download."""
    return df.to_csv().encode("utf-8")