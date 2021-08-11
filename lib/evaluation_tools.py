import yfinance as yf
import pandas as pd
import datetime as dt
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
    tmp_df = pd.DataFrame()
    final_df = pd.DataFrame()
    dates_list = []
    for ticker_symbol in tickers:
        ticker_data = yf.Ticker(ticker_symbol)
        yf_df = pd.DataFrame(ticker_data.history(period='1D', start='1970-1-1', end=dt.datetime.now())).reset_index()
        dates_list.append(yf_df['Date'])
        yf_df['ticker'] = ticker_symbol
        tmp_df = pd.concat([tmp_df, yf_df], axis=0)
    if not start_date:
        start_date = min(set(dates_list[0]).intersection(*dates_list))
    tmp_df = tmp_df[tmp_df['Date'] >= pd.to_datetime(start_date)]

    for ticker_symbol in tickers:
        yf_df = tmp_df[tmp_df['ticker'] == ticker_symbol].copy()
        if (dt.datetime.now() - pd.to_datetime(start_date)) > dt.timedelta(days=600):
            print('Data resampled to end of week')
            frequency = 'weekly'
            yf_df = yf_df.resample('M', on='Date').last()
        yf_df['Close_pct'] = yf_df['Close'] / yf_df['Close'][0]
        final_df = pd.concat([final_df, yf_df])
        
    return final_df
