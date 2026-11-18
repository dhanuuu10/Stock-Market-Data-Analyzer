
import yfinance as yf
import os


def fetch_stock_data(stock_symbol, period="1y"):

    print("\n===================================")
    print("STOCK MARKET DATA COLLECTION")
    print("===================================")

    print(f"Fetching data for: {stock_symbol}")

    try:
        # Connect to Yahoo Finance
        stock = yf.Ticker(stock_symbol)

        # Download historical stock data
        data = stock.history(
            period=period,
            interval="1d",
            auto_adjust=False
        )

        # Check whether data is available
        if data.empty:
            print("No stock data found!")
            print("Please check the stock symbol.")
            return None

        # Remove timezone information from index
        data.index = data.index.tz_localize(None)

        # Create data folder if it does not exist
        os.makedirs("data/raw", exist_ok=True)

        # Save stock data into CSV file
        filename = f"data/raw/{stock_symbol}_stock_data.csv"

        data.to_csv(filename)

        print("\nStock data collected successfully!")

        print("\nFirst 5 records:")
        print(data.head())

        print("\nTotal records:", len(data))

        print("\nFile saved at:", filename)

        return data

    except Exception as e:
        print("Error while collecting stock data:", e)
        return None
