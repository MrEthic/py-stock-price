def get_hmm_model():
    st.session_state.data['price_change'] = st.session_state.data['close'].diff()
    st.session_state.data.fillna(0, inplace=True)
    Z, states, model = hmm_predict(st.session_state.data, 'price_change')
    st.session_state.hmm_Z = Z
    st.session_state.hmm_states = states

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

def p():
    if 'data' not in st.session_state:
        st.session_state.data = None

    if 'hmm_states' not in st.session_state:
        st.session_state.hmm_states = None

    if 'hmm_Z' not in st.session_state:
        st.session_state.hmm_Z = None


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
