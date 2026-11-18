from modules.report_exporter import export_to_excel
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import date, timedelta

from modules.data_cleaner import clean_stock_data
from modules.technical_indicators import calculate_technical_indicators


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Stock Market Data Analyzer",
    page_icon="📈",
    layout="wide"
)


# ==========================================
# DASHBOARD TITLE
# ==========================================

st.title("📈 Stock Market Data Analyzer")

st.markdown(
    "Analyze historical stock prices, financial performance, "
    "technical indicators, and trading volume."
)

st.divider()


# ==========================================
# STOCK DATA COLLECTION
# ==========================================

@st.cache_data(ttl=900)
def get_stock_data(symbol, start_date, end_date):

    stock = yf.Ticker(symbol)

    data = stock.history(
        start=start_date,
        end=end_date + timedelta(days=1),
        interval="1d",
        auto_adjust=False
    )

    if data.empty:
        return pd.DataFrame()

    data.index = data.index.tz_localize(None)

    return data


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("Stock Selection")

stock_symbol = st.sidebar.text_input(
    "Enter Stock Symbol",
    value="AAPL"
).upper().strip()

start_date = st.sidebar.date_input(
    "Start Date",
    value=date.today() - timedelta(days=365)
)

end_date = st.sidebar.date_input(
    "End Date",
    value=date.today()
)

analyze_button = st.sidebar.button(
    "Analyze Stock",
    use_container_width=True
)

st.sidebar.info(
    "Examples: AAPL, TSLA, MSFT, "
    "RELIANCE.NS, TCS.NS, INFY.NS"
)


# ==========================================
# STOCK ANALYSIS
# ==========================================

if analyze_button:

    if not stock_symbol:
        st.error("Please enter a valid stock symbol.")

    elif start_date >= end_date:
        st.error("End date must be after start date.")

    else:

        with st.spinner("Fetching and analyzing stock data..."):

            try:

                # Fetch historical stock data
                stock_data = get_stock_data(
                    stock_symbol,
                    start_date,
                    end_date
                )

                if stock_data.empty:

                    st.error(
                        "No stock data found. "
                        "Please check the stock symbol and dates."
                    )

                else:

                    # Clean stock data
                    cleaned_data = clean_stock_data(
                        stock_data,
                        stock_symbol
                    )

                    if cleaned_data is None or cleaned_data.empty:

                        st.error("Unable to clean stock data.")

                    else:

                        # Calculate technical indicators
                        analyzed_data = calculate_technical_indicators(
                            cleaned_data
                        )

                        if analyzed_data is None or analyzed_data.empty:

                            st.error("Stock analysis failed.")

                        else:

                            # Calculate financial statistics
                            latest_price = analyzed_data["Close"].iloc[-1]

                            highest_price = analyzed_data["High"].max()

                            lowest_price = analyzed_data["Low"].min()

                            average_price = analyzed_data["Close"].mean()

                            total_return = (
                                (analyzed_data["Close"].iloc[-1] -
                                 analyzed_data["Close"].iloc[0])
                                / analyzed_data["Close"].iloc[0]
                            ) * 100

                            average_volume = analyzed_data["Volume"].mean()

                            volatility = analyzed_data[
                                "Daily_Return"
                            ].std()

                            # Store results in session state
                            st.session_state["stock_data"] = analyzed_data
                            st.session_state["stock_symbol"] = stock_symbol

                            st.success(
                                f"Analysis completed successfully for {stock_symbol}!"
                            )

            except Exception as e:

                st.error(f"An error occurred: {e}")


# ==========================================
# DISPLAY DASHBOARD
# ==========================================

if "stock_data" in st.session_state:

    data = st.session_state["stock_data"]

    symbol = st.session_state["stock_symbol"]

    latest_price = data["Close"].iloc[-1]

    highest_price = data["High"].max()

    lowest_price = data["Low"].min()

    average_price = data["Close"].mean()

    total_return = (
        (data["Close"].iloc[-1] - data["Close"].iloc[0])
        / data["Close"].iloc[0]
    ) * 100

    average_volume = data["Volume"].mean()

    volatility = data["Daily_Return"].std()

    st.header(f"{symbol} Stock Performance Dashboard")

    # ======================================
    # KPI CARDS
    # ======================================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Latest Closing Price",
        f"{latest_price:,.2f}"
    )

    col2.metric(
        "Highest Price",
        f"{highest_price:,.2f}"
    )

    col3.metric(
        "Lowest Price",
        f"{lowest_price:,.2f}"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Total Return",
        f"{total_return:.2f}%"
    )

    col5.metric(
        "Average Price",
        f"{average_price:,.2f}"
    )

    col6.metric(
        "Average Trading Volume",
        f"{average_volume:,.0f}"
    )

    st.divider()

    # ======================================
    # HISTORICAL STOCK PRICE CHART
    # ======================================

    st.subheader("Historical Stock Price")

    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=data.index,
        y=data["Close"],
        mode="lines",
        name="Closing Price"
    ))

    fig1.update_layout(
        xaxis_title="Date",
        yaxis_title="Stock Price",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig1, use_container_width=True)

    # ======================================
    # MOVING AVERAGE CHART
    # ======================================

    st.subheader("Moving Average Analysis")

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
        xaxis_title="Date",
        yaxis_title="Stock Price",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig2, use_container_width=True)

    # ======================================
    # TRADING VOLUME CHART
    # ======================================

    st.subheader("Trading Volume Analysis")

    fig3 = go.Figure()

    fig3.add_trace(go.Bar(
        x=data.index,
        y=data["Volume"],
        name="Trading Volume"
    ))

    fig3.update_layout(
        xaxis_title="Date",
        yaxis_title="Volume",
        template="plotly_white",
        height=400
    )

    st.plotly_chart(fig3, use_container_width=True)

    # ======================================
    # DAILY RETURNS CHART
    # ======================================

    st.subheader("Daily Returns Analysis")

    fig4 = go.Figure()

    fig4.add_trace(go.Bar(
        x=data.index,
        y=data["Daily_Return"],
        name="Daily Returns"
    ))

    fig4.update_layout(
        xaxis_title="Date",
        yaxis_title="Daily Return (%)",
        template="plotly_white",
        height=400
    )

    st.plotly_chart(fig4, use_container_width=True)

    # ======================================
    # VOLATILITY
    # ======================================

    st.subheader("Risk and Volatility Analysis")

    st.metric(
        "Daily Return Volatility",
        f"{volatility:.2f}%"
    )

    st.caption(
        "Volatility is the standard deviation of daily returns. "
        "Higher volatility indicates greater historical price fluctuation."
    )

    # ======================================
    # DATA TABLE
    # ======================================

    st.subheader("Historical Stock Data")

    st.dataframe(
        data.tail(20),
        use_container_width=True
    )

    # ======================================
    # DOWNLOAD CSV
    # ======================================

    st.subheader("Download Analyzed Data")

    csv_data = data.to_csv().encode("utf-8")

    st.download_button(
        label="Download Stock Analysis CSV",
        data=csv_data,
        file_name=f"{symbol}_stock_analysis.csv",
        mime="text/csv"
    )
    excel_file = export_to_excel(data, symbol)

    st.download_button(
    label="Download Excel Report",
    data=excel_file,
    file_name=f"{symbol}_stock_analysis.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
else:

    st.info(
        "Enter a stock symbol and select a date range "
        "from the sidebar, then click Analyze Stock."
    )

    st.write(
        "Your stock market analytics dashboard will appear here."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Stock Market Data Analyzer | Built using Python, "
    "Pandas, Yahoo Finance, Plotly and Streamlit. "
    "For educational and analytical purposes only."
)
