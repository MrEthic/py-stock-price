import streamlit as st

from utils import ColorIterator
from vizualization import get_candlestick_plot
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


def sidebar(tickers):
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
