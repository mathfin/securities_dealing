import plotly
from dash import Dash, html, dcc, Input, Output
from broker_connector import StockHistory


app = Dash(__name__)


def create_dash_application(flask_app):
    external_stylesheets = ["/static/css/style.css"]
    dash_app = Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/",
                    external_stylesheets=external_stylesheets)
    dash_app.layout = html.Div([
            html.Div(className='flex', children=[html.Div(["ПАН", html.Br(), "БАН"]), html.Div("К")]),
            html.Hr(),
            dcc.Graph(id='live-update-graph'),
            dcc.Interval(
                id='interval-component',
                interval=1 * 1000,  # in milliseconds
                n_intervals=0
            )
        ]
    )

    @dash_app.callback(Output('live-update-graph', 'figure'),
                       Input('interval-component', 'n_intervals'))
    def update_graph_live(n):
        data = StockHistory.get_by_name('Tesla Motors').time_value_pair
        fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
        fig['layout']['margin'] = {
            'l': 30, 'r': 10, 'b': 30, 't': 10
        }
        fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

        fig.append_trace({
            'x': list(range(len(data[:, 0]))),
            'y': list(map(float, data[:, 1])),
            'name': f'Price {list(map(float, data[:, 1]))[-1]}',
            'mode': 'lines+markers',
            'type': 'scatter'
        }, 1, 1)
        fig.append_trace({
            'x': list(range(len(data[:, 0]))),
            'y': list(map(int, data[:, 2])),
            'name': f'Quantity {list(map(int, data[:, 2]))[-1]}',
            'mode': 'lines+markers',
            'type': 'scatter'
        }, 2, 1)

        return fig

    return dash_app