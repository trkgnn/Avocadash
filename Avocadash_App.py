import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

#analyzing the given data and formatting in the way needed for the plots
df = pd.read_csv(r'C:\Users\user\Coding\Avocadash\avocado.csv')
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
df.sort_values("Date", inplace=True)
df['week'] = pd.DatetimeIndex(df['Date']).week
df=df[df['week'] != 53]
df=df[df["region"] != "TotalUS"]

#creating lists for the clickable options
year_options = []
for year in df['year'].unique():
    year_options.append({'label':str(year),'value':year})
type_options = []
for type in df['type'].unique():
    type_options.append({'label':str(type),'value':type})
plot_options=[{'label':"price compare",'value':"price"},
              {'label':"volume compare",'value':"volume"}
              ]

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Avocado Analytics: Understand Your Avocados!"


#setting up the layout for the app
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Avocado Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze and Compare the behavior of avocado prices"
                    " and the number of avocados sold in the US"
                    " between 2015 and 2018",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Year", className="menu-title"),
                        dcc.Dropdown(
                            id='year-picker',options=year_options,value=df['year'].min(),
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.RadioItems(
                            id='type_picker',options=type_options,value="conventional",
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Comparison", className="menu-title"
                        ),
                        dcc.RadioItems(id='plot_picker',options=plot_options,value="price"
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children="Double click on any region name below to see its values and click on another one to compare"
                )
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="graph",
                        ),
                    className="card",
                )
            ],
            className="wrapper",
        ),
        
    ]
)

#function to reflect the graph by taking all choosen options as inputs and creating the graphs for user to see.
@app.callback(Output('graph', 'figure'),
              [Input('year-picker', 'value'),
               Input('type_picker', 'value'),
               Input('plot_picker', 'value')])
def update_figure(selected_year, selected_type, selected_plot):
    type_filtered_df=df[df["type"]== selected_type]
    filtered_df = type_filtered_df[type_filtered_df['year'] == selected_year]
    traces_for_price = []
    for region_name in filtered_df['region'].unique():
        df_by_region = filtered_df[filtered_df['region'] == region_name]
        traces_for_price.append(go.Scatter(
            x=df_by_region['week'],
            y=df_by_region['AveragePrice'],
            text=df_by_region['region'],
            name=region_name
        ))

    traces_for_volume = []
    for region_name in filtered_df['region'].unique():
        df_by_region = filtered_df[filtered_df['region'] == region_name]
        traces_for_volume.append(go.Scatter(
            x=df_by_region['week'],
            y=df_by_region['Total Volume'],
            text=df_by_region['region'],
            name=region_name
        ))


    if selected_plot=="price":
        return {
            'data': traces_for_price,
            'layout': go.Layout(
                xaxis={'title': 'week of the year'},
                yaxis={'title': 'Price'},
                hovermode='closest'
            )
        }
    
    elif selected_plot=="volume":
        return {
            'data': traces_for_volume,
            'layout': go.Layout(
                xaxis={'title': 'week of the year'},
                yaxis={'title': 'Total Volume'},
                hovermode='closest'
            )
        }
    


if __name__ == "__main__":
    app.run_server(debug=True)

