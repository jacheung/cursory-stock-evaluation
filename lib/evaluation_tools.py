import yfinance as yf
import pandas as pd
from datetime import datetime as dt
from dateutil.parser import parse


def _is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def build_figure_df(tickers, start_date=[]):
    if not start_date:
        dates_list = []
        for ticker_symbol in tickers:
            ticker_data = yf.Ticker(ticker_symbol)
            yf_df = pd.DataFrame(ticker_data.history(period='1D', start='1970-1-1', end=dt.now()))
            dates_list.append(yf_df.index)
        start_date = min(set(dates_list[0]).intersection(*dates_list))
        print('No start date selected. Using', str(start_date))

    if not _is_date(str(start_date)):
        raise ValueError('date format invalid. Try yyyy-mm-dd')

    full_df = pd.DataFrame()
    for ticker_symbol in tickers:
        ticker_data = yf.Ticker(ticker_symbol)
        yf_df = pd.DataFrame(ticker_data.history(period='1day', start=start_date, end=dt.now()))
        yf_df['Close_pct'] = yf_df['Close'] / yf_df['Close'][0]
        yf_df['ticker'] = ticker_symbol
        full_df = pd.concat([full_df, yf_df], axis=0)

    return full_df.reset_index()
