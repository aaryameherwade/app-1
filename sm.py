import streamlit as st
import yfinance as yf
import plotly.express as px

st.set_page_config(
    page_title="Global Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>

.main{
background-color:#0e1117;
}

.big-font{
font-size:42px;
font-weight:bold;
text-align:center;
color:#00FFAA;
}

.small{
text-align:center;
font-size:18px;
color:white;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">📈 Global Stock Market Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="small">Powered by Yahoo Finance</p>', unsafe_allow_html=True)

popular = [
"AAPL",
"MSFT",
"GOOGL",
"TSLA",
"NVDA",
"AMZN",
"META",
"TCS.NS",
"RELIANCE.NS",
"INFY.NS"
]

st.sidebar.header("Search Stock")

stock = st.sidebar.selectbox(
"Choose Popular Stock",
popular
)

custom = st.sidebar.text_input(
"Or Enter Stock Symbol"
)

ticker = custom.upper() if custom else stock

period = st.sidebar.selectbox(
"Select Time Period",
[
"5d",
"1mo",
"3mo",
"6mo",
"1y",
"5y",
"max"
]
)

with st.spinner("Fetching Stock Data..."):

    data = yf.Ticker(ticker)

    info = data.info

    history = data.history(period=period)

try:

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Current Price",
              f"${info['currentPrice']}")

    c2.metric("Open",
              f"${info['open']}")

    c3.metric("High",
              f"${info['dayHigh']}")

    c4.metric("Low",
              f"${info['dayLow']}")

    c5,c6,c7 = st.columns(3)

    c5.metric("Previous Close",
              f"${info['previousClose']}")

    c6.metric("Volume",
              f"{info['volume']:,}")

    c7.metric("Market",
              info['exchange'])

    st.subheader(info['longName'])

    fig = px.line(
        history,
        x=history.index,
        y="Close",
        title=f"{ticker} Stock Price"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Closing Price",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(history.tail(10))

except:

    st.error("Invalid Stock Symbol!")
