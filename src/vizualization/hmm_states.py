import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def get_hmm_states_plot(df: pd.DataFrame, ticker: str, states, Z):

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=(f'{ticker} Price (USD)', 'Price Variation'),
        row_width=[0.3, 0.7]
    )

    for i in states:
        want = (Z == i)
        x = df["open_time"].iloc[want]
        y = df["close"].iloc[want]

        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                name=f"State {i}",
                mode='lines'
            ),
            row=1,
            col=1
        )

    for i in states:
        want = (Z == i)
        x = df["open_time"].iloc[want]
        y = df["price_change"].iloc[want]

        fig.add_trace(
            go.Bar(
                x=x,
                y=y,
                name=f"State {i}"
            ),
            row=2,
            col=1
        )

    fig['layout']['xaxis2']['title'] = 'Date'
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Price Change'

    fig['layout']['yaxis']['gridcolor'] = '#2E323D'
    fig['layout']['xaxis']['gridcolor'] = '#2E323D'
    fig['layout']['yaxis2']['gridcolor'] = '#2E323D'
    fig['layout']['xaxis2']['gridcolor'] = '#2E323D'

    fig.update_xaxes(
        rangeslider_visible=False
    )

    fig.update_layout(height=600)

    return fig
