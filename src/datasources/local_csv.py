import os
import pandas as pd


def load_local(symbol):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, 'data', f'{symbol}-DAILY.csv')
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
    else:
        raise FileNotFoundError

    df.drop(columns=['close_time', 'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol', '-'], inplace=True)
    return df
