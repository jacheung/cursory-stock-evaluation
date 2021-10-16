from lib import evaluation_tools as tools

stock_tickers = 'AMZN, VO'
date = '1/1/2021'
stock_tickers = tools.clean_string(stock_tickers)
df = tools.overview_table(stock_tickers).reset_index()

columns = [{'name': col, 'id': col} for col in df.columns]
data = df.to_dict(orient='records')