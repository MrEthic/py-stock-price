from .polygon import polygon_get_tickers, polygon_get_ticker_candles
from .local_csv import load_local


polygon = type("DataSource", (object,), {})()
polygon.get_tickers = polygon_get_tickers
polygon.get_candles = polygon_get_ticker_candles

local = type("DataSource", (object,), {})()
local.load = load_local
