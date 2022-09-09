import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def get_candlestick_plot(df: pd.DataFrame, ticker: str):

    df['t'] = pd.to_datetime(df['t'], unit='ms')

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=(f'{ticker} Price Chart', 'Volume'),
        row_width=[0.3, 0.7]
    )

    fig.add_trace(
        go.Candlestick(
            x=df['t'],
            open=df['o'],
            high=df['h'],
            low=df['l'],
            close=df['c'],
            name='Price'
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(x=df['t'], y=df['v'], name='Volume'),
        row=2,
        col=1,
    )

    fig['layout']['xaxis2']['title'] = 'Date'
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'

    fig.update_xaxes(
        rangebreaks=[{'bounds': ['sat', 'mon']}],
        rangeslider_visible=False,
    )

    fig.update_layout(height=600)

    return fig
