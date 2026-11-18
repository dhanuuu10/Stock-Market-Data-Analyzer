
import pandas as pd
import os


def clean_stock_data(data, stock_symbol):

    print("\n===================================")
    print("STOCK MARKET DATA CLEANING")
    print("===================================")

    # Check whether data is available
    if data is None or data.empty:
        print("No data available for cleaning!")
        return None

    # Create a copy of original data
    cleaned_data = data.copy()

    # Display original data information
    print("\nOriginal data shape:", cleaned_data.shape)

    # Remove duplicate records
    cleaned_data = cleaned_data[~cleaned_data.index.duplicated(keep="first")]

    # Remove rows with missing important values
    important_columns = ["Open", "High", "Low", "Close", "Volume"]

    cleaned_data = cleaned_data.dropna(
        subset=important_columns
    )

    # Remove invalid stock prices
    cleaned_data = cleaned_data[
        (cleaned_data["Open"] > 0) &
        (cleaned_data["High"] > 0) &
        (cleaned_data["Low"] > 0) &
        (cleaned_data["Close"] > 0)
    ]

    # Remove invalid volume records
    cleaned_data = cleaned_data[
        cleaned_data["Volume"] >= 0
    ]

    # Ensure data is sorted by date
    cleaned_data = cleaned_data.sort_index()

    # Create processed data folder
    os.makedirs("data/processed", exist_ok=True)

    # Save cleaned data
    filename = f"data/processed/{stock_symbol}_cleaned.csv"

    cleaned_data.to_csv(filename)

    # Display cleaning results
    print("\nData cleaning completed!")

    print("Cleaned data shape:", cleaned_data.shape)

    print("\nMissing values:")
    print(cleaned_data.isnull().sum())

    print("\nCleaned data preview:")
    print(cleaned_data.head())

    print("\nCleaned file saved at:", filename)

    return cleaned_data
