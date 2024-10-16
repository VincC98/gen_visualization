from dash import Dash, dcc, html, dash_table, Output, Input, callback
import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px
import numpy as np
import plotly.figure_factory as ff


df = pd.read_csv("transcriptomics_data/transcriptomics_data.csv")
df = df[:100]
dftemp = df.copy()
for i in dftemp.columns:
    #print(i)
    describeDF = dftemp[i].describe()
    if i != "colour" and i != "cell_type":
        if (describeDF["25%"] == describeDF["50%"] and describeDF["25%"] == describeDF["75%"]):
            #print(f"same value in {i}")
            dftemp.drop(i, axis=1, inplace=True)
dftemp.drop(["cell_type", "colour"], axis=1, inplace=True)
dfCorr = dftemp.corr()

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def update_df(percentage):
    #print(percentage)
    nRows = len(df) * percentage/100
    #print(nRows)
    # = df.head(int(nRows))
    return "Slider to choose which percentage of the dataset u want to visualize"

def make_graph(yaxis_column_name, graph_type):

    if graph_type == 'scatter':
        fig = px.scatter(df, x=df.index,
                         y=yaxis_column_name,
                         color="colour",
                         size='cell_type',
                         title="Custom Graph")

        fig.update_xaxes(title="Index")
        fig.update_yaxes(title=yaxis_column_name)
        return fig

    elif graph_type == "histogram2d":
        fig = px.bar(df, x=df.index, y=yaxis_column_name, title="Custom Graph")

        fig.update_xaxes(title="Index")
        fig.update_yaxes(title=yaxis_column_name)
        return fig

    elif graph_type == "line":

        fig = px.line(df, x=df.index, y=yaxis_column_name, title="Custom Graph")

        fig.update_xaxes(title="Index")
        fig.update_yaxes(title=yaxis_column_name)

        return fig
fig = make_graph("gene_0", "scatter")

layout = \
    html.Div([
        html.H1(
            children='LDATA2010',
            style={
                'textAlign': 'center'
            }
        ),

    html.Div(children='Choose which single-cell RNA transcriptomics in the brain of a rat you want to see', style={
        'textAlign': 'left'
    }),
        html.Div([html.Div([
            dcc.Dropdown(
                df.columns , "gene_0",
                id='yaxis-column'
            ),
            ], style={ "position":"center"}),

            ]),
        html.Div(
                [dcc.RadioItems(
                        id="charts_radio",
                        options=[
                            {"label": "Scatter", "value": "scatter"},
                            {"label": "Histogram", "value": "histogram2d"},
                            {"label": "Line", "value": "line"},
                        ],
                        labelClassName="radio__labels",
                        inputClassName="radio__input",
                        value="scatter",
                        className="radio__group",
                    ),
                    dcc.Graph(
                                id="firstGraph",
                                figure=fig,
                                style={"margin-left":"auto","margin-right":"auto"}
                ),
                    html.Div(style={"textAlign":"center"}, id="showDatasetUtilisation"),
                    dcc.Slider(id="sliderFirstGraph", min=1, max=100, step=1, value=100)
                ],
            ),
    html.Div([
            dcc.Graph(
                id="test",
                style={"margin-left":"auto","margin-right":"auto"}
                #figure = px.scatter(x=df.index, y=df["gene_0"])
            )
            ]),

    html.Div([
            dcc.Graph(
                id="heatmap",
                figure = px.imshow(dfCorr, text_auto=True, title="Heatmap Correlation"),
                style={"width" : "900px", "height":"900px","margin-left":"auto","margin-right":"auto"})
            ]),

    dcc.Link('Go to the analysis section', href='/page2')

    ], style={"align-items":"center"})



@callback(
    Output('firstGraph', 'figure'),
    Input('yaxis-column', 'value'),
    Input('charts_radio', 'value'))
def update_graph(yaxis_column_name, graph_type):
    #print("value changed")
    return make_graph(yaxis_column_name, graph_type)
## RETOURNER DANS UNE AUTRE FONCTION LA VARIABLE POUR UPDATE LE DATAFRAME ##
@callback(
    Output(component_id='showDatasetUtilisation', component_property="children"),
    Input("sliderFirstGraph", "value"))
def update_dataSize(percentage):
    if percentage is None:
        return "100 % of the dataset is used"
    else:
        return update_df(percentage)

@callback(
    Output('test', 'figure'),
    Input('firstGraph', 'selectedData'),
    Input('yaxis-column', "value"))
def callback(selectedData, yaxis):

    if selectedData != None:
        #print(f'selected data: {selectedData}')
        xList = []
        yList = []

        for i in selectedData["points"]:
            xList.append(i["x"])
            yList.append(i["y"])

        return px.scatter(df.filter(items=xList, axis=0), y=yaxis, color="cell_type")
    else:
        return px.scatter(df, x=df.index, y=df["gene_1"], size=df["cell_type"], color=df['colour'], title="Interactive Graph")

'''
def callback(selectedData):

    if selectedData != None:
        #print(f'selected data: {selectedData}')
        xList = []
        yList = []

        for i in selectedData["points"]:
            xList.append(i["x"])
            yList.append(i["y"])

        return px.scatter(x=xList, y=yList)
    else:
        return px.scatter(df, x=df.index, y=df["gene_1"], size=df["cell_type"], color=df['colour'], title="Interactive Graph")
'''