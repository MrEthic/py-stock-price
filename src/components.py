import streamlit as st

from utils import ColorIterator
from vizualization import get_candlestick_plot, get_hmm_states_plot
from indicators import ma


def candles_price_chart():
    st.plotly_chart(
        get_candlestick_plot(
            st.session_state.candles,
            st.session_state.selected_crypto_name,
            ColorIterator(),
            *st.session_state.indicators
        ),
        use_container_width=True,
        height=600
    )


def hmm_modeling_chart():
    st.plotly_chart(
        get_hmm_states_plot(
            st.session_state.data,
            st.session_state.modeling_symbol,
            st.session_state.hmm_states,
            st.session_state.hmm_Z
        ),
        use_container_width=True,
        height=600
    )


def hmm_container():
    pass


def sidebar(tickers):
    datasource = st.sidebar.radio(
        "Data source",
        ('Polygon API',),
        index=0,
        key='datasource'
    )

    if datasource == 'Polygon API':

        st.sidebar.selectbox(
            label='Select Polygon ticker...',
            options=tickers.keys(),
            index=list(tickers.keys()).index('BTC'),
            key='selected_crypto_name'
        )

        st.sidebar.selectbox(
            label='Select timespan...',
            options=['Hourly', 'Daily'],
            index=0,
            key='timespan'
        )

    elif datasource == 'Binance (local)':
        st.session_state.selected_crypto_name = 'BTC'


def chart_options_expander():
    with st.expander("Chart options", expanded=True):
        st.multiselect(
            'Indicators',
            options=['Moving Average'],
            default=['Moving Average'],
            key='indicators_select'
        )

        cols = st.columns(4)

        if 'Moving Average' in st.session_state.indicators_select:

            for i, c in enumerate(cols):
                with c:
                    val = st.number_input(
                        f"MA {i + 1}",
                        min_value=0,
                        max_value=50,
                        value=0,
                        step=1
                    )
                    if val != 0:
                        st.session_state.indicators_dict[f'ma_{val}'] = (ma, (val,))
