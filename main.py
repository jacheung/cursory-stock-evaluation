import plotly.express as px
from lib import evaluation_tools as etools

df = etools.build_figure_df(['AMD', 'NVDA'])
fig = px.scatter(df, x="Date", y="Close_pct", color="ticker")
fig.show()
