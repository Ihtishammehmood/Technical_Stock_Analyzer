import pandas as pd
import numpy as np

def calculate_macd(df, fast_period=12, slow_period=26, signal_period=9):
    """Calculates MACD, MACD Signal, and MACD Histogram."""
    if 'Close' not in df.columns:
        return df

    df[f'EMA_{fast_period}'] = df['Close'].ewm(span=fast_period, adjust=False).mean()
    df[f'EMA_{slow_period}'] = df['Close'].ewm(span=slow_period, adjust=False).mean()
    df['MACD'] = df[f'EMA_{fast_period}'] - df[f'EMA_{slow_period}']
    df['MACD_Signal'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
    return df

def calculate_atr(df, period=14):
    """Calculates Average True Range (ATR)."""
    if not all(col in df.columns for col in ['High', 'Low', 'Close']):
        return df

    df['TR'] = np.maximum(
        np.maximum(
            df['High'] - df['Low'],
            np.abs(df['High'] - df['Close'].shift(1))
        ),
        np.abs(df['Low'] - df['Close'].shift(1))
    )
    df['ATR'] = df['TR'].rolling(window=period).mean()
    return df

def calculate_obv(df):
    """Calculates On-Balance Volume (OBV)."""
    if not all(col in df.columns for col in ['Close', 'Volume']):
        return df

    df['OBV'] = np.where(
        df['Close'] > df['Close'].shift(1),
        df['Volume'],
        np.where(
            df['Close'] < df['Close'].shift(1),
            -df['Volume'],
            0
        )
    ).cumsum()
    return df

def calculate_stochastic(df, k_period=14, d_period=3):
    """Calculates the Stochastic Oscillator (%K and %D)."""
    if not all(col in df.columns for col in ['High', 'Low', 'Close']):
        return df

    df['Lowest_Low'] = df['Low'].rolling(window=k_period).min()
    df['Highest_High'] = df['High'].rolling(window=k_period).max()
    df['%K'] = 100 * ((df['Close'] - df['Lowest_Low']) / (df['Highest_High'] - df['Lowest_Low']))
    df['%D'] = df['%K'].rolling(window=d_period).mean()
    return df

def calculate_rsi(df, period=14):
    """Calculates the Relative Strength Index (RSI)."""
    if 'Close' not in df.columns:
        return df

    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    # Avoid division by zero
    avg_loss = avg_loss.replace(0, 0.00001)

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def calculate_sma(df, period):
    """Calculates Simple Moving Average (SMA)."""
    if 'Close' not in df.columns:
        return df
    df[f'SMA_{period}'] = df['Close'].rolling(window=period).mean()
    return df

def calculate_bollinger_bands(df, period=20, std_dev=2):
    """Calculates Bollinger Bands (Middle, Upper, Lower)."""
    if 'Close' not in df.columns:
        return df
    df = calculate_sma(df, period) # Ensure SMA is calculated
    df[f'STD_{period}'] = df['Close'].rolling(window=period).std()
    df['Upper_Band'] = df[f'SMA_{period}'] + (df[f'STD_{period}'] * std_dev)
    df['Lower_Band'] = df[f'SMA_{period}'] - (df[f'STD_{period}'] * std_dev)
    return df