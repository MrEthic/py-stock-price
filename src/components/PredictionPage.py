import pandas as pd
import streamlit as st

from utils import ColorIterator
from vizualization import candlestick_predict
from datasources import local
from prediction import HMMPredictor


class PredictionPage:

    @staticmethod
    def sidebar():
        symbol = st.sidebar.selectbox(
            label='Select symbol...',
            options=['BTCBUSD'],
            index=0
        )

        timerange = st.sidebar.slider(
            label='Choose prediction period',
            min_value=1,
            max_value=300,
            value=10,
        )

        if st.sidebar.button('Get/Update Predictor'):
            try:
                st.session_state.predict.data = local.load(symbol)
                st.session_state.predict.symbol = symbol
                st.session_state.predict.timerange = timerange
            except Exception as e:
                st.sidebar.error('Error while retrieving data...', icon=None)
                with st.expander("Exception"):
                    st.exception(e)

            st.session_state.predict.predictor = HMMPredictor(st.session_state.predict.data, timerange)

        if st.session_state.predict.predictor is not None:
            st.session_state.predict.predictor.fit()
            txt = f'<p style="color:#089981;">Predictor {st.session_state.predict.symbol}<br>{st.session_state.predict.timerange} days to predict</p>'
            st.sidebar.markdown(txt, unsafe_allow_html=True)

    @staticmethod
    def hmm_pred():
        if st.button('Predict future price'):
            with st.spinner('Predicting...'):
                bar = st.progress(0)
                st.session_state.predict.predictions = st.session_state.predict.predictor.predict(bar)

    @staticmethod
    def prediction_plot():
        st.plotly_chart(
            candlestick_predict(
                st.session_state.predict.data,
                st.session_state.predict.predictions
            ),
            use_container_width=True,
            height=600
        )
