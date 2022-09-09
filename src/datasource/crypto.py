from dotenv import load_dotenv
from os import getenv
import pandas as pd
import requests
import json
from datetime import date, timedelta
import streamlit as st


BASE_ENDPOINT = 'https://api.polygon.io'


def get_polygon_apikey() -> str:
    """
    Get Polygon.io Api Key query parameter

    :return: Polygon key
    """
    load_dotenv()
    return f"&apiKey={getenv('POLYGON_API_KEY')}"


@st.cache
def get_polygon_tickers() -> dict:
    endpoint = f"{BASE_ENDPOINT}/v3/reference/tickers?market=crypto&limit=1000{get_polygon_apikey()}"
    tickers_raw = requests.get(url=endpoint).json()
    tickers = {t.get('base_currency_symbol'): t.get('ticker') for t in tickers_raw.get('results')}
    return tickers


def build_polygon_endpoint(crypto_ticker, timespan):
    if timespan == 'Hourly':
        timespan = 'hour'
        delta = 60
    else:
        timespan = 'day'
        delta = 365*2

    multiplier = 1
    end = date.today()
    start = end - timedelta(days=delta)
    start = start.strftime('%Y-%m-%d')
    end = end.strftime('%Y-%m-%d')
    endpoint = f"/v2/aggs/ticker/{crypto_ticker}/range/{multiplier}/{timespan}/{start}/{end}?adjusted=true&sort=asc&limit=50000{get_polygon_apikey()}"
    return endpoint


@st.experimental_memo
def get_ticker_candles(crypto_ticker, timespan, as_df=True) -> pd.DataFrame:
    """
    Get historical data of crypto ticker

    :param timespan:
    :param crypto_ticker:
    :param as_df:
    :return:
    """
    endpoint = f"{BASE_ENDPOINT}{build_polygon_endpoint(crypto_ticker, timespan)}{get_polygon_apikey()}"
    data_raw = requests.get(endpoint).json()
    data = data_raw.get('results', None)

    if data is None or crypto_ticker is None:
        raise Exception('Data fetch from polygon is null')
    return pd.DataFrame(data) if as_df else data
