import streamlit as st
import pandas as pd
from types import SimpleNamespace
import base64

from config import configure_page
from components import PredictionPage

predict_model = {
    'data': None,
    'symbol': None,
    'predictor': None,
    'predictions': None,
    'predict_n_last': None
}


def predict_page():
    configure_page()

    # Init state
    if "predict" not in st.session_state:
        st.session_state.predict = SimpleNamespace(**predict_model)

    PredictionPage.sidebar()
    PredictionPage.model_control()

    if st.session_state.predict.predictions is not None:
        PredictionPage.prediction_plot()

        st.dataframe(st.session_state.predict.predictions)

        csv = st.session_state.predict.predictions.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown(f'<a href="data:file/csv;base64,{b64}" download="tmp/predictions.csv">Download csv file</a>', unsafe_allow_html=True)


if __name__ == '__main__':
    predict_page()
