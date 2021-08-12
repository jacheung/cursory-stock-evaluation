import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from lib import evaluation_tools as tools

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H6("Input stock ticker symbols in the text box to compare % ROI. Separate by commas."),
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
    dcc.Graph(id='stock-ROI-scatter')
])


@app.callback(
    Output('stock-ROI-scatter', 'figure'),
    Input('stock-tickers', 'value'),
    Input('date', 'value')
)
def update_figure(stock_tickers, date):
    stock_tickers = tools.clean_string(stock_tickers)
    df = tools.build_figure_df(stock_tickers, start_date=date)
    df, frequency = tools.downsample(df)
    fig = px.scatter(df, x="Date", y="% ROI", color="ticker",
                     title='Stock ' + frequency + ' % ROI')
    fig.update_layout(hovermode="x unified")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
