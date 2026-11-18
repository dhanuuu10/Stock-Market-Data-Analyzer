import os 
import pandas as pd


def calculate_technical_indicators(data):

    print("\n===================================")
    print("TECHNICAL INDICATOR CALCULATION")
    print("===================================")

    # Check whether stock data exists
    if data is None or data.empty:
        print("No data available!")
        return None

    # Create a copy of stock data
    data = data.copy()

    # Calculate 20-day Simple Moving Average
    data["SMA_20"] = data["Close"].rolling(
        window=20
    ).mean()

    # Calculate 50-day Simple Moving Average
    data["SMA_50"] = data["Close"].rolling(
        window=50
    ).mean()

    # Calculate daily percentage returns
    data["Daily_Return"] = data["Close"].pct_change() * 100

    # Calculate 20-day rolling volatility
    data["Volatility"] = data["Daily_Return"].rolling(
        window=20
    ).std()

    # Display results
    print("\nTechnical Indicators Calculated Successfully!")

    print("\nLatest Technical Indicator Values:")

    print(data[[
        "Close",
        "SMA_20",
        "SMA_50",
        "Daily_Return",
        "Volatility"
    ]].tail())

    # Display latest values
    latest = data.iloc[-1]

    print("\nLATEST INDICATORS")

    print(f"Closing Price: {latest['Close']:.2f}")

    print(f"20-Day SMA: {latest['SMA_20']:.2f}")

    print(f"50-Day SMA: {latest['SMA_50']:.2f}")

    print(f"Daily Return: {latest['Daily_Return']:.2f}%")

    print(f"Volatility: {latest['Volatility']:.2f}%")

    print("\n===================================")
    os.makedirs("data/processed", exist_ok=True)

    data.to_csv(
    "data/processed/technical_indicators.csv"
)

    print("\nTechnical indicator data saved successfully!")
    return data
