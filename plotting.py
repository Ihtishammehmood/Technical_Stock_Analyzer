import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from indicators import (
    calculate_macd, calculate_atr, calculate_obv,
    calculate_stochastic, calculate_rsi, calculate_sma,
    calculate_bollinger_bands
)

def plot_stock_chart(df, ticker, tickers_companies_dict, indicator_params):
    """
    Generates and displays a stock chart with selected technical indicators.
    """
    title_str = f"{tickers_companies_dict[ticker]}'s stock price"

    try:
        fig = go.Figure()

        # Check if we have the necessary columns for a candlestick chart
        required_ohlc_cols = ['Open', 'High', 'Low', 'Close']
        has_ohlc = all(col in df.columns for col in required_ohlc_cols)

        if not has_ohlc:
            st.error(f"Missing required columns for candlestick chart: {', '.join([col for col in required_ohlc_cols if col not in df.columns])}")
            st.write("Falling back to a line chart for the available data")

            # Try to use Adj Close if available, then Close, then any numeric
            price_col = None
            for col_candidate in ['Close', 'Adj Close', 'Price', 'Last']:
                if col_candidate in df.columns:
                    price_col = col_candidate
                    break

            if price_col:
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df[price_col],
                    name=price_col,
                    line=dict(color='blue')
                ))
            else:
                # Just use the first numeric column if no common price column is found
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                if len(numeric_cols) > 0:
                    price_col = numeric_cols[0]
                    fig.add_trace(go.Scatter(
                        x=df.index,
                        y=df[price_col],
                        name=price_col,
                        line=dict(color='blue')
                    ))
                else:
                    st.error("No numeric columns found for plotting.")
                    return # Exit if no data to plot

        else:
            # Add candlestick trace
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Price'
            ))

        # Add Volume if requested and available
        if indicator_params["volume_flag"] and 'Volume' in df.columns:
            fig.add_trace(go.Bar(
                x=df.index,
                y=df['Volume'],
                name='Volume',
                yaxis='y2'
            ))
            fig.update_layout(
                yaxis2=dict(
                    title="Volume",
                    overlaying="y",
                    side="right"
                )
            )

        # Add SMA if requested
        if indicator_params["sma_flag"] and 'Close' in df.columns:
            df = calculate_sma(df, indicator_params["sma_periods"])
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df[f'SMA_{indicator_params["sma_periods"]}'],
                name=f'SMA ({indicator_params["sma_periods"]})',
                line=dict(color='blue')
            ))

        # Add Bollinger Bands if requested
        if indicator_params["bb_flag"] and 'Close' in df.columns:
            df = calculate_bollinger_bands(df, indicator_params["bb_periods"], indicator_params["bb_std"])
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Upper_Band'],
                name=f'Upper Band ({indicator_params["bb_periods"]}, {indicator_params["bb_std"]})',
                line=dict(color='rgba(250, 0, 0, 0.5)')
            ))
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Lower_Band'],
                name=f'Lower Band ({indicator_params["bb_periods"]}, {indicator_params["bb_std"]})',
                line=dict(color='rgba(250, 0, 0, 0.5)')
            ))

        # Add RSI if requested
        if indicator_params["rsi_flag"] and 'Close' in df.columns:
            df = calculate_rsi(df, indicator_params["rsi_periods"])
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['RSI'],
                name='RSI',
                yaxis='y3',
                line=dict(color='purple')
            ))
            fig.add_trace(go.Scatter(
                x=df.index,
                y=[indicator_params["rsi_upper"]] * len(df),
                name=f'RSI Upper ({indicator_params["rsi_upper"]})',
                yaxis='y3',
                line=dict(color='rgba(250, 0, 0, 0.5)', dash='dash')
            ))
            fig.add_trace(go.Scatter(
                x=df.index,
                y=[indicator_params["rsi_lower"]] * len(df),
                name=f'RSI Lower ({indicator_params["rsi_lower"]})',
                yaxis='y3',
                line=dict(color='rgba(0, 250, 0, 0.5)', dash='dash')
            ))
            fig.update_layout(
                yaxis3=dict(
                    title="RSI",
                    anchor="free",
                    overlaying="y",
                    side="right",
                    position=1.0,
                    range=[0, 100]
                )
            )

        # Add MACD if requested
        if indicator_params["macd_flag"] and 'Close' in df.columns:
            df = calculate_macd(df, indicator_params["macd_fast"], indicator_params["macd_slow"], indicator_params["macd_signal"])
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['MACD'],
                name='MACD',
                yaxis='y4',
                line=dict(color='blue')
            ))
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['MACD_Signal'],
                name='MACD Signal',
                yaxis='y4',
                line=dict(color='red')
            ))
            fig.add_trace(go.Bar(
                x=df.index,
                y=df['MACD_Histogram'],
                name='MACD Histogram',
                yaxis='y4',
                marker=dict(
                    color=np.where(df['MACD_Histogram'] >= 0, 'green', 'red'),
                    opacity=0.7
                )
            ))
            fig.update_layout(
                yaxis4=dict(
                    title="MACD",
                    anchor="free",
                    overlaying="y",
                    side="right",
                    position=0.95
                )
            )

        # Add ATR if requested
        if indicator_params["atr_flag"] and all(col in df.columns for col in ['High', 'Low', 'Close']):
            df = calculate_atr(df, indicator_params["atr_period"])
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['ATR'],
                name=f'ATR ({indicator_params["atr_period"]})',
                yaxis='y5',
                line=dict(color='orange')
            ))
            fig.update_layout(
                yaxis5=dict(
                    title="ATR",
                    anchor="free",
                    overlaying="y",
                    side="right",
                    position=0.90
                )
            )

        # Add OBV if requested
        if indicator_params["obv_flag"] and all(col in df.columns for col in ['Close', 'Volume']):
            df = calculate_obv(df)
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['OBV'],
                name='OBV',
                yaxis='y6',
                line=dict(color='brown')
            ))
            fig.update_layout(
                yaxis6=dict(
                    title="OBV",
                    anchor="free",
                    overlaying="y",
                    side="right",
                    position=0.85
                )
            )

        # Add Stochastic Oscillator if requested
        if indicator_params["stoch_flag"] and all(col in df.columns for col in ['High', 'Low', 'Close']):
            df = calculate_stochastic(df, indicator_params["stoch_k"], indicator_params["stoch_d"])
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['%K'],
                name='%K',
                yaxis='y7',
                line=dict(color='blue')
            ))
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['%D'],
                name='%D',
                yaxis='y7',
                line=dict(color='red')
            ))
            fig.add_trace(go.Scatter(
                x=df.index,
                y=[80] * len(df),
                name='Overbought (80)',
                yaxis='y7',
                line=dict(color='rgba(250, 0, 0, 0.5)', dash='dash')
            ))
            fig.add_trace(go.Scatter(
                x=df.index,
                y=[20] * len(df),
                name='Oversold (20)',
                yaxis='y7',
                line=dict(color='rgba(0, 250, 0, 0.5)', dash='dash')
            ))
            fig.update_layout(
                yaxis7=dict(
                    title="Stochastic",
                    anchor="free",
                    overlaying="y",
                    side="right",
                    position=0.80,
                    range=[0, 100]
                )
            )

        # Update layout
        fig.update_layout(
            title=title_str,
            xaxis_title='Date',
            yaxis_title='Price',
            xaxis_rangeslider_visible=False,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=800
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error generating chart: {str(e)}")
        st.write("There was an error generating the chart. Please try different parameters or a different stock symbol.")
        st.write("DataFrame head:")
        st.write(df.head())
        st.write("Available columns:", ", ".join(df.columns))