import pandas as pd
from pandas_datareader.data import DataReader
from pandas_datareader.data import get_data_alphavantage
from dash.dependencies import Output, Input
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
from datetime import timedelta
import colorlover as cl
import re

# today's date
end = datetime.now()
# five years ago - IEX's limit
# start = end - timedelta(days=1825)
# every possible year
start = datetime(1900, 1, 1)

pd.core.common.is_list_like = pd.api.types.is_list_like

df_symbol = pd.read_csv('tickers.csv')

colorscale = cl.scales['9']['qual']['Paired']


def dispatcher(request):
	app = _create_app()

	params = {
		'data': request.body,
		'method': request.method,
		'content_type': request.content_type
	}

	with app.server.test_request_context(request.path, **params):
		app.server.preprocess_request()
		try:
			response = app.server.full_dispatch_request()
		except Exception as e:
			response = app.server.make_response(app.server.handle_exception(e))
		return response.get_data()


def _create_app():
	app = dash.Dash(url_base_pathname="/", csrf_protect=False)
	app.config.suppress_callback_exceptions = True
	app.layout = html.Div([
		html.Div([
			html.H2('Testing',
				style={
					'display': 'inline',
					'float': 'left',
					'font-size': '2.65em',
					'margin-left': '7px',
					'font-weight': 'bolder',
					'font-family': 'Product Sans',
					'color': "rgba(117, 117, 117, 0.95)",
					'margin-top': '20px',
					'margin-bottom': 0
				}),
		]),
		dcc.Dropdown(
			id='stock-ticker-input',
			options=[{'label': s[0], 'value': s[1]} for s in zip(df_symbol.Company, df_symbol.Symbol)],
			value=['AAPL', 'TSLA'],  # default graphs/on loading the page
			multi=True  # it's possible to have multiple graphs
		),
		html.Div(id='graphs'),

	], className="container")

	@app.callback(
		Output('graphs', 'children'),
		[Input('stock-ticker-input', 'value')])
	def update_graph(tickers):
		graphs = []
		for i, ticker in enumerate(tickers):
			try:
				# IEX API
				# df = DataReader(ticker, 'iex', start, end)
				# AlphaVantage API
				# df = get_data_alphavantage(symbols=ticker, start=dt.datetime(2018, 1, 1), end=dt.datetime.now(), api_key='FFCPDAKPHICMS4D0')
				df = get_data_alphavantage(symbols=ticker, start=start, end=end, api_key='FFCPDAKPHICMS4D0')
			except:
				graphs.append(html.H3(
					'Data is not available for {}'.format(ticker),
					style={
						'marginTop': 20,
						'marginBottom': 20
					}
				))
				continue

			candlestick = {
				'x': df.index,
				'open': df['open'],
				'high': df['high'],
				'low': df['low'],
				'close': df['close'],
				'type': 'candlestick',
				'name': ticker,
				'legendgroup': ticker,
				'increasing': {'line': {'color': colorscale[0]}},
				'decreasing': {'line': {'color': colorscale[1]}},
			}

			bb_bands = bbands(df.close)
			bollinger_traces = [{
				'x': df.index,
				'y': y,
				'type': 'scatter',
				'mode': 'lines',
				'line': {'width': 1, 'color': colorscale[(i * 2) % len(colorscale)]},
				'hoverinfo': 'none',
				'legendgroup': ticker,
				'showlegend': True if i == 0 else False,
				'name': '{} - bollinger bands'.format(ticker)
			} for i, y in enumerate(bb_bands)]

			graphs.append(dcc.Graph(
				id=ticker,
				figure={
					'data': [candlestick] + bollinger_traces,
					'layout': {
						'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
						'legend': {'x': 0}
					}
				}
			))

		return graphs

	return app


# number of standard deviations above and below the price
def bbands(price, window_size=10, num_of_std=5):
	rolling_mean = price.rolling(window=window_size).mean()
	rolling_std = price.rolling(window=window_size).std()
	upper_band = rolling_mean + (rolling_std * num_of_std)
	lower_band = rolling_mean - (rolling_std * num_of_std)

	return rolling_mean, upper_band, lower_band


# a hack to get rid of carriage returns in the html returned by the call to dash_dispatcher
def clean_dash_content(dash_content):
	string_content = str(dash_content)
	string_content = string_content.replace("\\n   ", "")
	string_content = string_content.replace("\\\\n", "")
	string_content = string_content.replace("\\\'", "")
	string_content = string_content.replace(">\\n<", "><")
	string_content = string_content[:-6]
	string_content = string_content[1:]
	string_content = re.sub('\s+',' ', string_content)
	string_content = string_content[1:]
	cleaned_dash_content = string_content

	return cleaned_dash_content


if __name__ == "__main__":
	app = _create_app()
	app.run_server()
