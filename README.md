
# Technical Stock Analyzer

![image](https://github.com/user-attachments/assets/97cc93c4-e044-40b4-978c-52e6b81bea32)

# [See Full YouTube Video Here](https://www.youtube.com/watch?v=E3bdXKeFvsU)


## Overview
This is a Streamlit-based web application that performs technical analysis on stocks. The application allows users to select companies from the S&P 500 index, visualize stock price data, and apply various technical indicators to assist with stock analysis.

## Features
- Select any company from the S&P 500 constituents
- Customize date range for analysis
- Display stock price charts with customizable technical indicators:
  - Volume visualization
  - Simple Moving Average (SMA)
  - Moving Average Convergence Divergence (MACD)
  - Average True Range (ATR)
  - On-Balance Volume (OBV)
  - Bolinger Bands
  - Stochastic Oscillator
- You can also download the stock data

## Installation

### Prerequisites
- Python 3.13

### Setup
1. Clone Repository `https://github.com/Ihtishammehmood/Technical_Stock_Analyzer.git`
2. Create Virtual Environment `uv venv` and activate virtual evironment `.venv\Scripts\activate`
3. Install Dependencies `uv sync`


## Usage

### Running the Application
Start the Streamlit application:
```bash
streamlit run main_app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### User Interface
1. **Main Panel**: Displays the stock chart and technical analysis
2. **Sidebar**: Contains controls for:
   - Stock ticker selection
   - Date range selection
   - Technical indicator options

### Workflow
1. Select a company from the S&P 500 dropdown
2. Set your desired date range for analysis
3. Choose which technical indicators to display using the expanders in the sidebar
4. View and analyze the resulting chart


## Author
Ihtisham M - [LinkedIn](https://www.linkedin.com/in/ihtishammehmood)
