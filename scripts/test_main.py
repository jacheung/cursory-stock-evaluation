import plotly.express as px
from lib import evaluation_tools as tools

stock_tickers = 'AMD, NVDA'
date = '2016-01-29'
stock_tickers = tools.clean_string(stock_tickers)
df = tools.build_figure_df(stock_tickers, start_date=date)
scatter_df, frequency = tools.downsample(df)
fig = px.scatter(scatter_df, x="Date", y="% ROI", color="ticker",
                 title='Stock ' + frequency + ' % ROI')
fig.update_layout(hovermode="x unified")