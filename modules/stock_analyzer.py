
import pandas as pd


def analyze_stock_data(data, stock_symbol):

    print("\n===================================")
    print("STOCK MARKET FINANCIAL ANALYSIS")
    print("===================================")

    # Check whether data is available
    if data is None or data.empty:
        print("No data available for analysis!")
        return None

    # Calculate daily returns
    data["Daily Return (%)"] = (
        data["Close"].pct_change() * 100
    )

    # Calculate important stock statistics
    opening_price = data["Open"].iloc[0]

    latest_close = data["Close"].iloc[-1]

    average_price = data["Close"].mean()

    highest_price = data["High"].max()

    lowest_price = data["Low"].min()

    average_volume = data["Volume"].mean()

    # Calculate total return
    total_return = (
        (latest_close - data["Close"].iloc[0])
        / data["Close"].iloc[0]
    ) * 100

    # Calculate daily average return
    average_daily_return = data["Daily Return (%)"].mean()

    # Display analysis
    print(f"\nStock Symbol: {stock_symbol}")

    print("\nSTOCK PRICE STATISTICS")

    print(f"Opening Price: {opening_price:.2f}")

    print(f"Latest Closing Price: {latest_close:.2f}")

    print(f"Average Closing Price: {average_price:.2f}")

    print(f"Highest Price: {highest_price:.2f}")

    print(f"Lowest Price: {lowest_price:.2f}")

    print("\nRETURN ANALYSIS")

    print(f"Total Return: {total_return:.2f}%")

    print(f"Average Daily Return: {average_daily_return:.2f}%")

    print("\nTRADING VOLUME ANALYSIS")

    print(f"Average Trading Volume: {average_volume:.0f}")

    # Determine price movement
    if latest_close > data["Close"].iloc[0]:
        print("\nStock Performance: Positive Growth")

    elif latest_close < data["Close"].iloc[0]:
        print("\nStock Performance: Negative Growth")

    else:
        print("\nStock Performance: No Change")

    print("\n===================================")

    return data
