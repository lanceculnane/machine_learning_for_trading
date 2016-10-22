import os
import pandas as pd
import pandas_datareader.data as web


def get_stock_csv(symbol, start_date, end_date, filename):
    dframe = web.DataReader(name=symbol, data_source='yahoo', start=start_date, end=end_date)
    dframe.to_csv(filename)


def symbol_to_path(symbol, base_dir="data"):
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, start_date, end_date, fetch=True):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    for symbol in symbols:
        get_stock_csv(symbol, start_date, end_date, "data/{}.csv".format(symbol))

    get_stock_csv('SPY', start_date, end_date, "data/SPY.csv")
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index=dates)

    for symbol in symbols:
        path = symbol_to_path(symbol)
        df_temp = pd.read_csv(path, index_col="Date", parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        if symbol == 'SPY':
            df = df.join(df_temp, how="inner")
        else:
            df = df.join(df_temp)

    return df
