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


def clean_string(string):
    cleaned = [symbols.replace(' ', '').upper() for symbols in string.split(',')]

    return cleaned


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
    else:
        filtered_list = [lists[lists > start_date] for lists in dates_list]
        start_date = min(set(filtered_list[0]).intersection(*filtered_list))
    tmp_df = tmp_df[tmp_df['Date'] >= pd.to_datetime(start_date)]

    for ticker_symbol in tickers:
        yf_df = tmp_df[tmp_df['ticker'] == ticker_symbol].copy().sort_values('Date').reset_index(drop=True)
        yf_df['% ROI'] = ((yf_df['Close'] / yf_df['Close'][0])-1)*100
        yf_df['Percent change'] = yf_df['Close'].pct_change()*100
        final_df = pd.concat([final_df, yf_df])

    return final_df


def downsample(df, points_threshold=1000):
    for frequency in ['W', 'M']:
        final_df = pd.DataFrame()
        if df.shape[0] > points_threshold:
            print('Too many points. Downsampling daily data to', frequency, 'data.')
            for ticker_symbol in df['ticker'].unique():
                yf_df = df[df['ticker'] == ticker_symbol].copy()
                yf_df = yf_df.resample(frequency, on='Date').last()
                final_df = pd.concat([final_df, yf_df])
            if final_df.shape[0] <= points_threshold:
                return final_df, frequency
        else:
            print('Points under threshold. Keeping daily frequency')
            frequency = 'D'
            return df, frequency


def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def overview_table(tickers):
    compiled_df = pd.DataFrame()
    for ticker in tickers:
        data = yf.Ticker(ticker)
        df = data.major_holders.rename(columns={0: ticker, 1: 'Feature'}).set_index('Feature').transpose()
        # grab numeric features into human readable formats
        numeric_features = ['fullTimeEmployees', 'marketCap', 'trailingPE']
        for feature in numeric_features:
            if feature in data.info.keys() and data.info[feature] is not None:
                df[feature] = human_format(data.info[feature])

        # YOY revenue growth
        if not data.earnings.empty:
            YOY = (data.earnings['Revenue'].pct_change() * 100).dropna().round(1)
            YOY_strings = [str(k) + '-' + str(k + 1) + ' revenue growth' for k in data.earnings['Revenue'].index][:-1]
            df[YOY_strings] = YOY.values
        # compile final dataframe
        compiled_df = pd.concat([compiled_df, df])
    return compiled_df.transpose().sort_index()

