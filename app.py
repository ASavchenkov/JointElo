import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#because both plots are very similar, we use one function to generate the divs
def create_plot_div(which_plot):
    return html.Div([

        dcc.Graph(
            id=which_plot + ' Elo History',
            figure={
                'data':[],
                'layout': {
                    'title': which_plot + ' Elo History'
                }
            }
        ),
        dcc.RangeSlider(
            id= which_plot+' Conditional Range',
            min = 1000,
            max = 1400,
            marks = { i: i for i in range(1000,1401,100)},
            step= 10,
            value = [1000,1400],
            className = 'six columns'
        ),
        html.Label('Conditional Range', className = 'five columns')
    ], className='six columns')


app.layout = html.Div(children=[

    create_plot_div('Character'),

])


@app.callback(
    Output(component_id='Character Elo History', component_property='figure'),
    [Input(component_id='Character Conditional Range', component_property = 'value')]
)
def update_character_plot(char_cond_range):
    return {
        'data': [
                    {'x': [1, 2], 'y': [4, 1], 'name': 'SF'},
                    {'x': [1, 2], 'y': [2, 4], 'name': u'Montréal'},
                ]
    }


if __name__ == '__main__':
    app.run_server(debug=True)
