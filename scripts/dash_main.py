import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from lib import evaluation_tools as tools
import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Welcome!"),
    html.H3("Input stock ticker symbols in the text box to compare % ROI. Separate by commas."),

    html.Div(dcc.Input(id='stock-tickers', type='text', value='AMZN, MSFT, GOOGL')),
    html.Div(['AMZN, MSFT, GOOGL'], id='ticker-div', style={'display': 'none'}),
    html.Button('Submit tickers', id='submit-ticker-button'),

    html.Div(dcc.Input(id='date', type='text', value='2021-01-01')),
    html.Div(['2021-01-01'], id='date-div', style={'display': 'none'}),
    html.Button('Submit dates', id='submit-date-button'),

    dcc.Graph(id='stock-ROI-scatter'),
    dash_table.DataTable(id='ticker_table'),
    dcc.Store(id='intermediate-df')
])


@app.callback(Output('ticker-div', 'children'),
              [Input('submit-ticker-button', 'n_clicks')],
              state=[State(component_id='stock-tickers', component_property='value')])
def update_ticker_div(n_clicks, input_value):
    return input_value


@app.callback(Output('date-div', 'children'),
              [Input('submit-date-button', 'n_clicks')],
              state=[State(component_id='date', component_property='value')])
def update_date_div(n_clicks, input_value):
    return input_value


@app.callback(
    Output('intermediate-df', 'data'),
    Input('date-div', 'children'),
    Input('ticker-div', 'children')
)
def build_dataframe_json(date, stock_tickers):
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
    fig = px.scatter(scatter_df, x="Date", y="% ROI", color="ticker")
    fig.update_traces(mode='lines+markers')
    fig.update_layout(hovermode="x unified")
    return fig


@app.callback(
    [Output(component_id='ticker_table', component_property='data'),
     Output(component_id='ticker_table', component_property='columns')],
    Input('ticker-div', 'children')
)
def display_ticker_info(tickers):
    stock_tickers = tools.clean_string(tickers)
    df = tools.overview_table(stock_tickers).reset_index()
    columns = [{'name': col, 'id': col} for col in df.columns]
    data = df.to_dict(orient='records')
    return data, columns


if __name__ == '__main__':
    app.run_server(debug=True)
