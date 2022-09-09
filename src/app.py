import streamlit as st
import pandas as pd

from datasource import get_polygon_tickers, get_ticker_candles
from vizualization import get_candlestick_plot
from config import configure_streamlit


def init_app():

    tickers = get_polygon_tickers()

    selected_crypto_name = st.sidebar.selectbox(
        label='Select Polygon ticker...',
        options=tickers.keys(),
        index=list(tickers.keys()).index('BTC'),
        key='selected_crypto_name'
    )

    timespan = st.sidebar.selectbox(
        label='Select timespan...',
        options=['Hourly', 'Daily'],
        index=0
    )

    ticker = tickers[selected_crypto_name]

    if 'candles' not in st.session_state:
        st.session_state.candles = None

    if st.sidebar.button('Get/Update Data'):
        update_candles(ticker, timespan)


def update_candles(ticker, timespan):
    try:
        st.session_state.candles = get_ticker_candles(ticker, timespan)
    except Exception:
        st.sidebar.error('Error while retrieving data...', icon=None)


def candle_chart():

    st.plotly_chart(
        get_candlestick_plot(st.session_state.candles, st.session_state.selected_crypto_name),
        use_container_width=True,
        height=600
    )


configure_streamlit()
init_app()
if st.session_state.candles is not None:
    candle_chart()
else:
    st.sidebar.info("Press the Get/Update Data button to display charts", icon=None)

