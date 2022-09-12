import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def candlestick_plot(df: pd.DataFrame, ticker: str, colors, *args):

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
            name='Price',
            increasing_fillcolor='#089981',
            increasing_line_color='#089981',
            decreasing_fillcolor='#F23645',
            decreasing_line_color='#F23645',
            increasing_line_width=1,
            decreasing_line_width=1
        ),
        row=1,
        col=1
    )

    # https://plotly.com/python/reference/#scatter-line-dash
    for indicator in args:
        c = colors.get_indicator_color(indicator)
        fig.add_trace(
            go.Scatter(
                x=df['t'],
                y=df[indicator],
                name=indicator,
                line=dict(
                    color=c,
                    shape='linear',
                    width=1
                ),
                mode='lines'
            ),
            row=1,
            col=1
        )

    fig.add_trace(
        go.Bar(x=df['t'], y=df['v'], name='Volume'),
        row=2,
        col=1,
    )

    fig['layout']['xaxis2']['title'] = 'Date'
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'

    fig['layout']['yaxis']['gridcolor'] = '#2E323D'
    fig['layout']['xaxis']['gridcolor'] = '#2E323D'
    fig['layout']['yaxis2']['gridcolor'] = '#2E323D'
    fig['layout']['xaxis2']['gridcolor'] = '#2E323D'

    fig.update_xaxes(
        rangeslider_visible=False
    )

    fig.update_layout(height=600)

    return fig
