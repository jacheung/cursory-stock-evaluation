import plotly.express as px
from lib import evaluation_tools as tools


def update_figure(stock_tickers, date):
    stock_tickers = tools.clean_string(stock_tickers)
    df = tools.build_figure_df(stock_tickers, start_date=date)
    df, frequency = tools.downsample(df)
    fig = px.scatter(df, x="Date", y="% ROI", color="ticker",
                     title='Stock ' + frequency + ' % ROI')
    fig.update_layout(hovermode="x unified")
    return fig


if __name__ == '__main__':
    update_figure('AMD, NVDA, INTEL', '2018-01-01')