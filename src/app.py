import streamlit as st
import pandas as pd

from datasource import get_polygon_tickers, get_ticker_candles, load_local
from modeling import hmm_predict
from config import configure_streamlit
import components as cp


def update_candles(ticker, timespan):
    try:
        if st.session_state.datasource == 'Polygon API':
            st.session_state.candles = get_ticker_candles(ticker, timespan)
        elif st.session_state.datasource == 'Binance (local)':
            pass
            # st.session_state.candles = get_btc_data()
    except Exception as e:
        st.sidebar.error('Error while retrieving data...', icon=None)
        print(e)


def update_indicators():
    for indicator_name, indicator_config in st.session_state.indicators_dict.items():
        func, args = indicator_config
        st.session_state.candles = func(st.session_state.candles, *args)
        st.session_state.indicators.add(f"{func.__name__}{''.join([f'_{arg}' for arg in args])}")


def get_hmm_model():
    st.session_state.data['price_change'] = st.session_state.data['close'].diff()
    st.session_state.data.fillna(0, inplace=True)
    Z, states, model = hmm_predict(st.session_state.data, 'price_change')
    st.session_state.hmm_Z = Z
    st.session_state.hmm_states = states


def main():
    configure_streamlit()

    tickers = get_polygon_tickers()

    cp.sidebar(tickers)

    ticker = tickers[st.session_state.selected_crypto_name]

    if 'candles' not in st.session_state:
        st.session_state.candles = None

    if 'data' not in st.session_state:
        st.session_state.data = None

    if 'hmm_states' not in st.session_state:
        st.session_state.hmm_states = None

    if 'hmm_Z' not in st.session_state:
        st.session_state.hmm_Z = None

    st.session_state.indicators_dict = {}
    st.session_state.indicators = set()

    if st.sidebar.button('Get/Update Data'):
        update_candles(ticker, st.session_state.get('timespan', None))

    if st.session_state.candles is not None:
        chart_tabs, modeling_tabs = st.tabs(["Charts", "Modeling"])
        with chart_tabs:
            chart_container = st.container()
            cp.chart_options_expander()
            update_indicators()
            with chart_container:
                cp.candles_price_chart()

        with modeling_tabs:
            with st.expander('Hidden Markov Chain Modeling', expanded=True):
                symbol = st.selectbox(
                    label="Select Symbol",
                    options=['BTCBUSD', 'ETHBUSD', 'XRPBUSD'],
                    index=0,
                    key='modeling_symbol'
                )

                if st.button("Start modeling"):
                    with st.spinner('Modeling...'):
                        st.session_state.data = load_local(symbol)
                        get_hmm_model()
                        cp.hmm_modeling_chart()







    else:
        st.sidebar.info("Press the Get/Update Data button to display charts", icon=None)


if __name__ == '__main__':
    main()
