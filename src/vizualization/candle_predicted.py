import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def candlestick_predict(df: pd.DataFrame, prediction):

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Recorded Price',
            increasing_fillcolor='#089981',
            increasing_line_color='#089981',
            decreasing_fillcolor='#F23645',
            decreasing_line_color='#F23645',
            increasing_line_width=1,
            decreasing_line_width=1
        )
    )

    fig.add_trace(
        go.Scatter(
            x=prediction['date'],
            y=prediction['predicted_close'],
            name='Predicted close',
            marker=dict(
                size=4,
                color='#1c83e1',
                symbol='circle'
            ),
            line=dict(
                color='#1c83e1',
                shape='linear',
                width=1
            ),
            mode='lines+markers'
        )
    )

    fig['layout']['yaxis']['gridcolor'] = '#2E323D'
    fig['layout']['xaxis']['gridcolor'] = '#2E323D'

    fig.update_xaxes(
        rangeslider_visible=False
    )

    fig.update_layout(height=600)

    return fig
