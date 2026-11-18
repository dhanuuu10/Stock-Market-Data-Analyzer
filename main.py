
from modules.data_collector import fetch_stock_data
from modules.data_cleaner import clean_stock_data
from modules.stock_analyzer import analyze_stock_data
from modules.technical_indicators import calculate_technical_indicators
from visualizations.charts import create_stock_charts

print("===================================")
print("   STOCK MARKET DATA ANALYZER")
print("===================================")

# Take stock symbol from user
stock_symbol = input(
    "Enter Stock Symbol (Example: AAPL): "
).upper().strip()

# Step 1: Collect stock data
stock_data = fetch_stock_data(stock_symbol)

if stock_data is not None:

    # Step 2: Clean stock data
    cleaned_data = clean_stock_data(
        stock_data,
        stock_symbol
    )

    if cleaned_data is not None:

        # Step 3: Analyze stock data
        analyzed_data = analyze_stock_data(
            cleaned_data,
            stock_symbol
        )

        if analyzed_data is not None:

            # Step 4: Calculate technical indicators
            indicator_data = calculate_technical_indicators(
                analyzed_data
            )

            if indicator_data is not None:

                # Step 5: Create stock charts
                create_stock_charts(
                    indicator_data,
                    stock_symbol
                )

                print("\nAll operations completed successfully!")

else:
    print("\nStock data collection failed!")




