import streamlit as st
import datetime
from data_loader import get_sp500_components, load_data, convert_df_to_csv
# from indicators import calculate_macd, calculate_atr, calculate_obv, calculate_stochastic
from plotting import plot_stock_chart
from utils import configure_cufflinks

configure_cufflinks()

# User Interface

st.set_page_config(
    page_title="Stock Analyzer",
    page_icon='📈',
    layout='wide'
)

st.title("Technical Stock Analysis")
st.write("""
    ### User manual
    * You can select any company from the S&P 500 constituents
    * Customize technical indicators from the sidebar
""")
st.markdown("---")
st.caption("Author: Ihtisham M | [LinkedIn](https://www.linkedin.com/in/ihtishammehmood)")



st.sidebar.header("Stock Parameters")
available_tickers, tickers_companies_dict = get_sp500_components()

ticker = st.sidebar.selectbox(
    "Ticker",
    available_tickers,
    format_func=tickers_companies_dict.get
)
start_date = st.sidebar.date_input(
    "Start date",
    datetime.date(2024, 1, 1)
)
end_date = st.sidebar.date_input(
    "End date",
    datetime.date.today()
)
if start_date > end_date:
    st.sidebar.error("The end date must fall after the start date")

# Volume option
exp_volume = st.sidebar.expander("Volume")
volume_flag = exp_volume.checkbox(label="Add Volume")

# SMA options
exp_sma = st.sidebar.expander("SMA")
sma_flag = exp_sma.checkbox(label="Add SMA")
sma_periods = exp_sma.number_input(
    label="SMA Periods",
    min_value=1,
    max_value=50,
    value=20,
    step=1
)

# Bollinger Bands options
exp_bb = st.sidebar.expander("Bollinger Bands")
bb_flag = exp_bb.checkbox(label="Add Bollinger Bands")
bb_periods = exp_bb.number_input(
    label="BB Periods",
    min_value=1,
    max_value=50,
    value=20,
    step=1
)
bb_std = exp_bb.number_input(
    label="# of standard deviations",
    min_value=1,
    max_value=4,
    value=2,
    step=1
)

# RSI options
exp_rsi = st.sidebar.expander("Relative Strength Index")
rsi_flag = exp_rsi.checkbox(label="Add RSI")
rsi_periods = exp_rsi.number_input(
    label="RSI Periods",
    min_value=1,
    max_value=50,
    value=20,
    step=1
)
rsi_upper = exp_rsi.number_input(
    label="RSI Upper",
    min_value=50,
    max_value=90,
    value=70,
    step=1
)
rsi_lower = exp_rsi.number_input(
    label="RSI Lower",
    min_value=10,
    max_value=50,
    value=30,
    step=1
)

# MACD options
exp_macd = st.sidebar.expander("MACD")
macd_flag = exp_macd.checkbox(label="Add MACD")
macd_fast = exp_macd.number_input(
    label="Fast Period",
    min_value=5,
    max_value=30,
    value=12,
    step=1
)
macd_slow = exp_macd.number_input(
    label="Slow Period",
    min_value=10,
    max_value=50,
    value=26,
    step=1
)
macd_signal = exp_macd.number_input(
    label="Signal Period",
    min_value=3,
    max_value=20,
    value=9,
    step=1
)

# ATR options
exp_atr = st.sidebar.expander("Average True Range")
atr_flag = exp_atr.checkbox(label="Add ATR")
atr_period = exp_atr.number_input(
    label="ATR Period",
    min_value=5,
    max_value=30,
    value=14,
    step=1
)

# OBV options
exp_obv = st.sidebar.expander("On-Balance Volume")
obv_flag = exp_obv.checkbox(label="Add OBV")

# Stochastic Oscillator options
exp_stoch = st.sidebar.expander("Stochastic Oscillator")
stoch_flag = exp_stoch.checkbox(label="Add Stochastic")
stoch_k = exp_stoch.number_input(
    label="K Period",
    min_value=5,
    max_value=30,
    value=14,
    step=1
)
stoch_d = exp_stoch.number_input(
    label="D Period",
    min_value=1,
    max_value=10,
    value=3,
    step=1
)


df = load_data(ticker, start_date, end_date)

data_exp = st.expander("Preview data")
available_cols = df.columns.tolist()
columns_to_show = data_exp.multiselect(
    "Columns",
    available_cols,
    default=available_cols
)

data_exp.dataframe(df[columns_to_show])
csv_file = convert_df_to_csv(df[columns_to_show])
data_exp.download_button(
    label="Download selected as CSV",
    data=csv_file,
    file_name=f"{ticker}_stock_prices.csv",
    mime="text/csv",
)

# Prepare indicator parameters for plotting function
indicator_params = {
    "volume_flag": volume_flag,
    "sma_flag": sma_flag,
    "sma_periods": sma_periods,
    "bb_flag": bb_flag,
    "bb_periods": bb_periods,
    "bb_std": bb_std,
    "rsi_flag": rsi_flag,
    "rsi_periods": rsi_periods,
    "rsi_upper": rsi_upper,
    "rsi_lower": rsi_lower,
    "macd_flag": macd_flag,
    "macd_fast": macd_fast,
    "macd_slow": macd_slow,
    "macd_signal": macd_signal,
    "atr_flag": atr_flag,
    "atr_period": atr_period,
    "obv_flag": obv_flag,
    "stoch_flag": stoch_flag,
    "stoch_k": stoch_k,
    "stoch_d": stoch_d,
}

plot_stock_chart(df, ticker, tickers_companies_dict, indicator_params)

# Add a section for technical analysis summary
if 'Close' in df.columns:
    st.subheader("Technical Analysis Summary")

    # Create columns for the summary
    col1, col2 = st.columns(2)

    # Get the latest values
    latest_close = df['Close'].iloc[-1]

    with col1:
        st.write(f"**Latest Close:** ${latest_close:.2f}")

        if sma_flag:
            # Recalculate SMA here to ensure it's on the latest data if needed,
            # or pass the calculated SMA from plotting.py
            if f'SMA_{sma_periods}' in df.columns:
                latest_sma = df[f'SMA_{sma_periods}'].iloc[-1]
                sma_signal = "BULLISH" if latest_close > latest_sma else "BEARISH"
                st.write(f"**SMA ({sma_periods}):** ${latest_sma:.2f} - Signal: {sma_signal}")

        if rsi_flag:
            if 'RSI' in df.columns:
                latest_rsi = df['RSI'].iloc[-1]
                if latest_rsi > rsi_upper:
                    rsi_signal = "OVERBOUGHT"
                elif latest_rsi < rsi_lower:
                    rsi_signal = "OVERSOLD"
                else:
                    rsi_signal = "NEUTRAL"
                st.write(f"**RSI ({rsi_periods}):** {latest_rsi:.2f} - Signal: {rsi_signal}")

        if macd_flag:
            if 'MACD' in df.columns and 'MACD_Signal' in df.columns and 'MACD_Histogram' in df.columns:
                latest_macd = df['MACD'].iloc[-1]
                latest_signal = df['MACD_Signal'].iloc[-1]
                latest_hist = df['MACD_Histogram'].iloc[-1]
                macd_cross_signal = "BULLISH" if latest_macd > latest_signal else "BEARISH"
                macd_trend = "STRENGTHENING" if latest_hist > 0 else "WEAKENING"
                st.write(f"**MACD:** {latest_macd:.2f} - Signal: {macd_cross_signal}, Trend: {macd_trend}")

    with col2:
        if bb_flag:
            if 'Upper_Band' in df.columns and 'Lower_Band' in df.columns:
                latest_upper = df['Upper_Band'].iloc[-1]
                latest_lower = df['Lower_Band'].iloc[-1]
                if latest_close > latest_upper:
                    bb_signal = "OVERBOUGHT"
                elif latest_close < latest_lower:
                    bb_signal = "OVERSOLD"
                else:
                    bb_signal = "NEUTRAL"
                st.write(f"**Bollinger Bands:** Signal: {bb_signal}")
                st.write(f"  - Upper: ${latest_upper:.2f}")
                st.write(f"  - Lower: ${latest_lower:.2f}")

        if stoch_flag:
            if '%K' in df.columns and '%D' in df.columns:
                latest_k = df['%K'].iloc[-1]
                latest_d = df['%D'].iloc[-1]
                if latest_k > 80:
                    stoch_signal = "OVERBOUGHT"
                elif latest_k < 20:
                    stoch_signal = "OVERSOLD"
                else:
                    stoch_signal = "NEUTRAL"
                st.write(f"**Stochastic:** %K: {latest_k:.2f}, %D: {latest_d:.2f} - Signal: {stoch_signal}")

        if atr_flag:
            if 'ATR' in df.columns:
                latest_atr = df['ATR'].iloc[-1]
                atr_percent = (latest_atr / latest_close) * 100
                st.write(f"**ATR ({atr_period}):** ${latest_atr:.2f} ({atr_percent:.2f}% of price)")