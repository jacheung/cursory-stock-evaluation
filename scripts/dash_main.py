import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from lib import evaluation_tools as tools
import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Welcome!"),
    html.H3("Input stock ticker symbols in the text box to compare % ROI. Separate by commas."),
    dcc.Input(
        id='stock-tickers',
        type='text',
        value='VOO, VOOG, VV'
    ),
    dcc.Input(
        id='date',
        type='text',
        value='2017-01-01'
    ),
    dcc.Graph(id='stock-ROI-scatter'),
    dcc.Graph(id='stock-daily-histogram'),
    dcc.Store(id='intermediate-df')
])


@app.callback(
    Output('intermediate-df', 'data'),
    Input('stock-tickers', 'value'),
    Input('date', 'value')
)
def build_dataframe_json(stock_tickers, date):
    stock_tickers = tools.clean_string(stock_tickers)
    df = tools.build_figure_df(stock_tickers, start_date=date)
    json_df = df.reset_index(drop=True).to_json()
    return json_df


@app.callback(
    Output('stock-ROI-scatter', 'figure'),
    Input('intermediate-df', 'data')
)
def update_scatter(json_df):
    df = pd.read_json(json_df)
    scatter_df, frequency = tools.downsample(df)
    fig = px.scatter(scatter_df, x="Date", y="% ROI", color="ticker",
                     title='Stock ' + frequency + ' % ROI')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(hovermode="x unified")
    return fig


@app.callback(
    Output('stock-daily-histogram', 'figure'),
    Input('intermediate-df', 'data')
)
def update_histogram(json_df):
    df = pd.read_json(json_df)
    hist_bins = df['Percent change'].quantile([.01, .99]).round(2).values
    fig = px.histogram(df, x='Percent change', color='ticker', nbins=151, range_x=hist_bins.tolist(),
                       histnorm='probability', marginal="rug")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
