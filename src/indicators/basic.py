import pandas as pd
import pandas_ta as ta


def ma(df, n):
    if n == 0:
        return df
    col_name = f'ma_{n}'
    df[col_name] = df['c'].rolling(window=n).mean()
    return df
