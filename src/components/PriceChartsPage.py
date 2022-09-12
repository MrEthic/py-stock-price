import streamlit as st

from utils import ColorIterator
from datasources import polygon
from vizualization import candlestick_plot
from indicators import ma


class PriceChartsPage:

    @staticmethod
    def sidebar(tickers):
        symbol = st.sidebar.selectbox(
            label='Select Polygon ticker...',
            options=tickers.keys(),
            index=list(tickers.keys()).index('BTC'),
            key='charts.ticker'
        )

        ticker = tickers[symbol]

        timespan = st.sidebar.selectbox(
            label='Select timespan...',
            options=['Hourly', 'Daily'],
            index=0,
            key='charts.timespan'
        )

        if st.sidebar.button('Get/Update Data'):
            try:
                st.session_state.charts.data = polygon.get_candles(ticker, timespan)
            except Exception as e:
                st.sidebar.error('Error while retrieving data...', icon=None)
                with st.expander("Exception"):
                    st.exception(e)

    @staticmethod
    def chart_options_expander():
        with st.expander("Chart options", expanded=True):
            selected = st.multiselect(
                'Indicators',
                options=['Moving Average'],
                default=['Moving Average'],
                key='charts.indicators_selected'
            )

            cols = st.columns(4)

            if 'Moving Average' in selected:

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
                            st.session_state.charts.indicators_dict[f'ma_{val}'] = (ma, (val,))

    @staticmethod
    def candles_price_chart():
        st.plotly_chart(
            candlestick_plot(
                st.session_state.charts.data,
                st.session_state.charts.ticker,
                ColorIterator(),
                *st.session_state.charts.indicators
            ),
            use_container_width=True,
            height=600
        )

    @staticmethod
    def update_indicators():
        for indicator_name, indicator_config in st.session_state.charts.indicators_dict.items():
            func, args = indicator_config
            st.session_state.charts.data = func(st.session_state.charts.data, *args)
            st.session_state.charts.indicators.add(f"{func.__name__}{''.join([f'_{arg}' for arg in args])}")



