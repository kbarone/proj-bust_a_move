from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import graph_functions as gf


app = Dash(__name__)

colors = {
    'background': '#FDFEFE',
    'text': '#17202A'
}

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# Running cleaning stuff
exec(open("zhvi_cleaning.py").read())

#----------------APP STARTS HERE---------------------#
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.H1(
        children='Bust A Move!',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Exploring Regional Mobility in the US\n', style={
        'textAlign': 'center',
        'color': colors['text']
    }),


    html.Div(children='Click on a county on the map to view mobility and demographic data.',
    style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div([
        dcc.Graph(
            id='zhvf',
            clickData={'points': [{'location': '30029'}]},
            figure=gf.create_chloropleth(counties, zhvi_county_inc_pop, natl_parks))], 
            style={'width': '55%','display': 'inline-block'}),

    html.Div([dcc.Graph(
                id='mobility_demo',)],
                style={'width': '45%','display': 'inline-block'}),
    

    html.Div([
            dcc.Dropdown(
                ['Percent change in GPS activity by Category',
                'Distribution of Median Income and Poverty rate'],
                'Percent change in GPS activity by Category',
                id='mobility_demo_toggle')],
                style={'width': '30%','float': 'right','display': 'inline-block'})

])

def make_side_graph(toggle_val, FIPS):
    '''
    Plot side graph based on toggle values
    '''

    if toggle_val == 'Percent change in GPS activity by Category':
        return gf.create_mobility_graph(mobility, zhvi_county_inc_pop, FIPS)
    
    if toggle_val == 'Distribution of Median Income and Poverty rate':
        return gf.create_income_graph(zhvi_county_inc_pop, FIPS)


@app.callback(
    Output('mobility_demo', 'figure'),
    Input('zhvf', 'clickData'),
    Input('mobility_demo_toggle', 'value'))
def update_graph_series(clickData, toggle):
    # Figure 2
    county = clickData['points'][0]['location']
    return make_side_graph(str(toggle), county)

'''
html.Div([
    dcc.Markdown(),
    html.Pre(id='click-data', style=styles['pre'])], 
    className='three columns')

@app.callback(
    Output('click-data', 'children'),
    Input('zhvf', 'clickData'),
    Input('mobility_demo_toggle', 'value'))
def display_click_data(clickData, toggle):
    return json.dumps(str(clickData['points'][0]['location'] + " " + toggle), indent=2)
'''

if __name__ == '__main__':
    app.run_server(debug=True)

