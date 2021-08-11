import plotly.express as px
from lib import evaluation_tools as tools

df = tools.build_figure_df(['QQQ', 'VOO'], start_date='2016-01-01')
fig = px.scatter(df, x="Date", y="Close_pct", color="ticker")
fig.show()
