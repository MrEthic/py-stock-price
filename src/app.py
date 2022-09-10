import streamlit as st
import pandas as pd

from datasource import get_polygon_tickers, get_ticker_candles
from config import configure_streamlit
import components as cp


def update_candles(ticker, timespan):
    try:
        st.session_state.candles = get_ticker_candles(ticker, timespan)
    except Exception:
        st.sidebar.error('Error while retrieving data...', icon=None)


def update_indicators():
    for indicator_name, indicator_config in st.session_state.indicators_dict.items():
        func, args = indicator_config
        st.session_state.candles = func(st.session_state.candles, *args)
        st.session_state.indicators.add(f"{func.__name__}{''.join([f'_{arg}' for arg in args])}")


def main():

    configure_streamlit()

    tickers = get_polygon_tickers()

    cp.sidebar(tickers)

    ticker = tickers[st.session_state.selected_crypto_name]

    if 'candles' not in st.session_state:
        st.session_state.candles = None

    st.session_state.indicators_dict = {}
    st.session_state.indicators = set()

    if st.sidebar.button('Get/Update Data'):
        update_candles(ticker, st.session_state.timespan)

    if st.session_state.candles is not None:
        chart_tabs, simulation_tabs = st.tabs(["Charts", "Simulation"])
        with chart_tabs:
            chart_container = st.container()
            cp.chart_options_expander()
            update_indicators()
            with chart_container:
                cp.candles_price_chart()
    else:
        st.sidebar.info("Press the Get/Update Data button to display charts", icon=None)


if __name__ == '__main__':
    main()
