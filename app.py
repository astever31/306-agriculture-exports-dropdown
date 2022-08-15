import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import pandas as pd

########### Define your variables ######

tabtitle = 'Food, Glorious Food'
charturl = 'https://plot.ly/python/choropleth-maps/'
sourceurl = 'https://www.ers.usda.gov/data-products/state-agricultural-trade-data/'
githublink = 'https://github.com/astever31/306-agriculture-exports-dropdown'
# here's the list of possible columns to choose from.
list_of_columns =['Animal fats',
 'Bakery goods, cereals, and pasta',
 'Beef and beef products',
 'Beer',
 'Chocolate and cocoa products',
 'Coarse grains (ex. corn)',
 'Condiments and sauces',
 'Confectionery',
 'Corn',
 'Cotton',
 'Dairy products',
 'Dextrins, peptones, and proteins',
 'Distilled spirits',
 'Distillers grains',
 'Dog and cat food',
 'Eggs and products',
 'Essential oils',
 'Ethanol (non-bev.)',
 'Food preparations',
 'Fresh fruit',
 'Fresh vegetables',
 'Fruit and vegetable juices',
 'Hay',
 'Hides and skins',
 'Live animals',
 'Meat products NESOI',
 'Milled grains and products',
 'Non-alcoholic bev. (ex. juices)',
 'Nursery products and cut flowers',
 'Oilseeds (ex. soybean)',
 'Other feeds, meals, and fodders',
 'Planting seeds',
 'Pork and pork products',
 'Poultry meat and products (ex. eggs)',
 'Processed fruit',
 'Processed vegetables',
 'Pulses',
 'Rice',
 'Soybean meal',
 'Soybean oil',
 'Soybeans',
 'Sugar, sweeteners, bev. bases',
 'Tobacco',
 'Tree nuts',
 'Vegetable oils (ex. soybean)',
 'Wheat',
 'Wine and related products']


########## Set up the chart

import pandas as pd
df = pd.read_csv('assets/us-exports-2022.csv')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1('2022 Agricultural Exports, by State, Fiscal Quarters 1 & 2'),
    html.Div([
        html.Div([
                html.H6('Select a variable for analysis:'),
                dcc.Dropdown(
                    id='options-drop',
                    options=[{'label': i, 'value': i} for i in list_of_columns],
                    value='Corn'#,
                    #optionHeight=50
                ),
        ], className='two columns'),
        html.Div([dcc.Graph(id='figure-1'),
            ], className='ten columns'),
    ], className='twelve columns'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Chart Source", href=charturl),
    html.Br(),
    html.A("Data Source", href=sourceurl),
]
)


# make a function that can intake any varname and produce a map.
@app.callback(Output('figure-1', 'figure'),
             [Input('options-drop', 'value')])
def make_figure(varname):
    mygraphtitle = f'Exports of {varname} in 2022'
    mycolorscale = 'sunset' # Note: The error message will list possible color scales.
    mycolorbartitle = "Millions USD"

    data=go.Choropleth(
        locations=df['State'], # Spatial coordinates
        locationmode = 'USA-states', # set of locations match entries in `locations`
        z = df[varname].astype(float), # Data to be color-coded
        colorscale = mycolorscale,
        colorbar_title = mycolorbartitle,
    )
    fig = go.Figure(data)
    fig.update_layout(
        title_text = mygraphtitle,
        geo_scope='usa',
        width=1200,
        height=800
    )
    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
