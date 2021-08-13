import plotly.express as px
from lib import evaluation_tools as tools
import pandas as pd

stock_tickers = 'VOO, MDIJX'
date = []
stock_tickers = tools.clean_string(stock_tickers)
df = tools.build_figure_df(stock_tickers, start_date=date)
df = pd.read_json(df.reset_index(drop=True).to_json())
scatter_df, frequency = tools.downsample(df)
fig = px.scatter(scatter_df, x="Date", y="% ROI", color="ticker",
                 title='Stock ' + frequency + ' % ROI')
fig.update_traces(mode='lines+markers')
fig.update_layout(hovermode="x unified")

# hist_bins = df['Percent change'].quantile([.01, .99]).round(2).values
# fig = px.histogram(df, x='Percent change', color='ticker', nbins=151, range_x=hist_bins.tolist(),
#                    histnorm='probability', marginal="rug")

fig.show()