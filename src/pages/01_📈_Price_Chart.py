import streamlit as st
from types import SimpleNamespace

from config import configure_page
from datasources import polygon
from components import PriceChartsPage

charts_model = {
    'data': None,
    'ticker': None,
    'indicators_dict': {},
    'indicators': set()
}


def price_chart_page():
    configure_page()

    # Init state
    if "charts" not in st.session_state:
        st.session_state.charts = SimpleNamespace(**charts_model)

    # Load polygon.io ticker list
    tickers = polygon.get_tickers()

    # Create sidebar
    PriceChartsPage.sidebar(tickers)

    # Content
    PriceChartsPage.chart_options_expander()
    PriceChartsPage.update_indicators()
    if st.session_state.charts.data is not None:
        PriceChartsPage.candles_price_chart()
    else:
        st.info("Click on Get/Update Data to display price chart")


if __name__ == '__main__':
    price_chart_page()
