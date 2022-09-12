from datetime import date, datetime, timedelta
import pytz
import os
from dotenv import load_dotenv
from binance.client import Client
import pandas as pd


def get_binance_client():
    load_dotenv()
    client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_API_SECRET'))
    return client


def get_interval(symbol, start, end):
    client = get_binance_client()
    klines = client.get_historical_klines(
        symbol=symbol,
        interval=Client.KLINE_INTERVAL_5MINUTE,
        start_str=int(start.timestamp()) * 1000,
        end_str=int(end.timestamp()) * 1000
    )
    return klines


def get_daily(symbol):
    client = get_binance_client()
    klines = client.get_historical_klines(
        symbol=symbol,
        interval=Client.KLINE_INTERVAL_1DAY
    )

    df = pd.DataFrame(klines, columns=['open_time',
                                       'open',
                                       'high',
                                       'low',
                                       'close',
                                       'volume',
                                       'close_time',
                                       'qav',
                                       'num_trades',
                                       'taker_base_vol',
                                       'taker_quote_vol', '-'])
    df.to_csv(f'{symbol}-DAILY.csv', index=False)


def get_large_interval(symbol):
    data = []

    start_date = datetime(2020, 1, 1, 0, 0, 0, 0, pytz.UTC)
    end_date = datetime(2022, 9, 1, 0, 0, 0, 0, pytz.UTC)
    delta = timedelta(days=3)

    d1 = start_date
    d2 = start_date + delta

    try:
        while d2 <= end_date:
            d1 += delta
            d2 += delta
            print(d1, d2)
            klines = get_interval(symbol, d1, d2)
            data += klines
    except:
        pass
    finally:
        df = pd.DataFrame(data, columns=['open_time',
                                         'open',
                                         'high',
                                         'low',
                                         'close',
                                         'volume',
                                         'close_time',
                                         'qav',
                                         'num_trades',
                                         'taker_base_vol',
                                         'taker_quote_vol', '-'])
        df.to_csv(f'{symbol}.csv', index=False)


get_daily('BTCBUSD')
