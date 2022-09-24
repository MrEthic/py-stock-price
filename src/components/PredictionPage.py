import pandas as pd
import streamlit as st
from tensorflow.keras.callbacks import Callback

from utils import ColorIterator
from vizualization import candlestick_predict
from datasources import local
from prediction import HMMPredictor, LSTMPredictor


class PredictionPage:
    PREDICTOR_MAP = {
        'HMM': HMMPredictor,
        'LSTM': LSTMPredictor
    }

    @staticmethod
    def sidebar():
        symbol = st.sidebar.selectbox(
            label='Select symbol...',
            options=['BTCBUSD'],
            index=0
        )

        predict_n_last = st.sidebar.slider(
            label='Predict last...',
            min_value=50,
            max_value=500,
            value=20,
        )

        st.session_state.predict.predict_n_last = predict_n_last

        if st.sidebar.button('Get/Update Data'):
            try:
                st.session_state.predict.data = local.load(symbol)
                st.session_state.predict.symbol = symbol
            except Exception as e:
                st.sidebar.error('Error while retrieving data...', icon=None)
                with st.expander("Exception"):
                    st.exception(e)

    @staticmethod
    def model_control():
        with st.expander("Model controller"):
            col1, col2, col3, col4 = st.columns(4)

            model = col1.selectbox(
                label='Select model...',
                options=PredictionPage.PREDICTOR_MAP.keys(),
                index=1
            )

            epochs = col2.number_input(
                label='Number of epochs:',
                min_value=1,
                max_value=10,
                value=4
            )

            if col1.button(
                    'Load predictor',
                    help=f'Data{" not" if st.session_state.predict.data is None else ""} loaded',
                    disabled=st.session_state.predict.data is None):

                st.session_state.predict.predictor = PredictionPage.PREDICTOR_MAP[model](
                    st.session_state.predict.data,
                    n_look_back=50,
                    predict_n_last=st.session_state.predict.predict_n_last
                )

            if col2.button(
                    f"Fit/Predict {model}",
                    help=f'Model is{" not" if st.session_state.predict.predictor is None else ""} loaded',
                    disabled=st.session_state.predict.predictor is None):

                with st.spinner('Fitting model...'):
                    bar = st.progress(0)
                    st.session_state.predict.predictor.fit(epochs=epochs, callbacks=CustomCallback(bar, epochs))

                with st.spinner('Predicting...'):
                    st.session_state.predict.predictions = st.session_state.predict.predictor.predictions()

            if st.session_state.predict.predictor is not None:
                if st.session_state.predict.predictor._predict_n_last != st.session_state.predict.predict_n_last:
                    st.warning('Predictor must be reloaded as "Predict last" have changed', icon="⚠️")
                else:
                    st.info(f'Predictor is ready to fit | {st.session_state.predict.predictor}', icon="ℹ️")

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


class CustomCallback(Callback):

    def __init__(self, fiting_bar, max_epoch):
        self.bar = fiting_bar
        self.max_epoch = max_epoch

    def on_epoch_end(self, epoch, logs=None):
        value = (epoch + 1) / self.max_epoch
        self.bar.progress(value)

