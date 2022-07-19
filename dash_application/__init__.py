import plotly
from dash import Dash, html, dcc, Input, Output
from broker_connector import StockHistory, df


app = Dash(__name__)


def create_dash_application(flask_app):
    external_stylesheets = ["/static/css/style.css"]
    dash_app = Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/",
                    external_stylesheets=external_stylesheets)

    dash_app.layout = html.Div([
            html.Div(className='flex', children=[html.Div(["ПАН", html.Br(), "БАН"]), html.Div("К")]),
            html.Hr(),
            dcc.Graph(id='live-update-graph', style={'width': '190vh', 'height': '100vh', 'backgroundColor':"#000230"}),
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
        fig = plotly.tools.make_subplots(rows=2*len(StockHistory.security_to_show), cols=1, vertical_spacing=0.04)
        fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
        fig.update_layout(paper_bgcolor="#111111", plot_bgcolor="#000230")

        for num, ticker in enumerate(StockHistory.security_to_show):
            stock = list(df['name'].loc[df['ticker'] == ticker])[0]
            data = StockHistory.get_by_name(stock).time_value_pair
            fig.append_trace({
                'x': list(range(len(data[:, 0]))),
                'y': list(map(float, data[:, 1])),
                'name': f'Price {list(map(float, data[:, 1]))[-1]}',
                'mode': 'lines+markers',
                'type': 'scatter'
            }, num*2+1, 1)
            fig.append_trace({
                'x': list(range(len(data[:, 0]))),
                'y': list(map(int, data[:, 2])),
                'name': f'Quantity {list(map(int, data[:, 2]))[-1]}',
                'mode': 'lines+markers',
                'type': 'scatter'
            }, num*2+2, 1)

        return fig

    return dash_app
