
import plotly.graph_objects as go
import os


def create_stock_charts(data, stock_symbol):

    print("\n===================================")
    print("STOCK MARKET DATA VISUALIZATION")
    print("===================================")

    if data is None or data.empty:
        print("No data available for visualization!")
        return

    # Create folder for saving charts
    os.makedirs("exports/charts", exist_ok=True)

    # Chart 1: Historical Stock Price
    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=data.index,
        y=data["Close"],
        mode="lines",
        name="Closing Price"
    ))

    fig1.update_layout(
        title=f"{stock_symbol} Historical Stock Price",
        xaxis_title="Date",
        yaxis_title="Stock Price",
        template="plotly_white"
    )

    fig1.write_html(
        f"exports/charts/{stock_symbol}_historical_price.html"
    )

    # Chart 2: Moving Averages
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=data.index,
        y=data["Close"],
        mode="lines",
        name="Closing Price"
    ))

    fig2.add_trace(go.Scatter(
        x=data.index,
        y=data["SMA_20"],
        mode="lines",
        name="SMA 20"
    ))

    fig2.add_trace(go.Scatter(
        x=data.index,
        y=data["SMA_50"],
        mode="lines",
        name="SMA 50"
    ))

    fig2.update_layout(
        title=f"{stock_symbol} Moving Average Analysis",
        xaxis_title="Date",
        yaxis_title="Stock Price",
        template="plotly_white"
    )

    fig2.write_html(
        f"exports/charts/{stock_symbol}_moving_averages.html"
    )

    # Chart 3: Trading Volume
    fig3 = go.Figure()

    fig3.add_trace(go.Bar(
        x=data.index,
        y=data["Volume"],
        name="Trading Volume"
    ))

    fig3.update_layout(
        title=f"{stock_symbol} Trading Volume",
        xaxis_title="Date",
        yaxis_title="Number of Shares",
        template="plotly_white"
    )

    fig3.write_html(
        f"exports/charts/{stock_symbol}_trading_volume.html"
    )

    # Chart 4: Daily Returns
    fig4 = go.Figure()

    fig4.add_trace(go.Bar(
        x=data.index,
        y=data["Daily_Return"],
        name="Daily Returns"
    ))

    fig4.update_layout(
        title=f"{stock_symbol} Daily Returns",
        xaxis_title="Date",
        yaxis_title="Daily Return (%)",
        template="plotly_white"
    )

    fig4.write_html(
        f"exports/charts/{stock_symbol}_daily_returns.html"
    )

    print("\nAll four charts created successfully!")

    print("\nCharts saved inside exports/charts folder.")

    print("\n1. Historical Stock Price")
    print("2. Moving Average Analysis")
    print("3. Trading Volume")
    print("4. Daily Returns")

    print("\n===================================")
