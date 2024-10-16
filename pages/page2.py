import dash
from dash import dcc, html, Output, Input, callback, State
from dash.exceptions import PreventUpdate

import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np

df = pd.read_csv("transcriptomics_data/transcriptomics_data.csv")


def makeKMeans(n_clusters, max_iter):
    n_clusters = 132
    Kmeans = KMeans(n_clusters=n_clusters, max_iter=max_iter)
    toKmeans = df.drop(["cell_type", "colour"], axis=1)
    label = Kmeans.fit_predict(toKmeans)
    u_labels = np.unique(label)
    #print(u_labels)
    #Kdf = pd.DataFrame(u_labels)
    return label

def makePCA():
    pca = PCA(n_components=2)
    toPCA = df.drop(["cell_type", "colour"], axis=1)
    components = pca.fit_transform(toPCA)
    dfPCA = pd.DataFrame(components, columns=["firstComponent", "secondComponent"])

    return dfPCA.to_json()

layout = html.Div([
                html.H1(
                    children='WELCOME ON THE ANALYSIS SECTION PART',
                    style={
                            'textAlign': 'center'
                            }
                        ),
                html.Div([
                    html.Div([
                                dcc.Dropdown(
                                    df.columns , "gene_0",
                                    id='xaxis-column'
                                ),
                                dcc.Dropdown(
                                    df.columns , "gene_1",
                                    id='yaxis-column'
                                ),
                                dcc.Store(id="K-means-data"),
                                html.Button('K-means', id='submit-KMeans', n_clicks=0),
                                html.Div(id='container-button-KMeans',
                                             children='Press the button to calculate K-means')
                                ], style={"display":"inline-block", 'width': '48%'}),
                    dcc.Graph(
                        id="K-means",
                    ),
                    dcc.Slider(
                        id='n_clusters',
                        min=1, max=10, step=2, value=10
                    ),
                    dcc.Slider(
                        id="max_iter",
                        min=50, max=300, step=50, value=300
                    )
                ]),

                html.Div([
                    dcc.Store(id="PCA-data"),
                    html.Button('PCA', id='submit-PCA', n_clicks=0),
                    html.Div(id='container-button-PCA',
                             children='Press the button to calculate PCA'),
                    dcc.Graph(
                        id="PCA"
                    )
                ]),

                dcc.Link('Go back to the visualization tools section', href='/page1')
                    ])



@callback(
    Output('K-means-data', 'data'),
    Output("container-button-KMeans", "children"),
    Input('submit-KMeans', 'n_clicks'),
    Input('n_clusters', 'value'),
    Input('max_iter', 'value'))
def runKMeans(n_clicks, n_clusters, max_iter):
    if n_clicks is None or n_clicks < 0:
        raise PreventUpdate
    if n_clicks > 0:
        print("Starting KMeans algo")
        data = makeKMeans(n_clusters, max_iter)
        print("Kmeans end")
        return data,"Kmeans calculated"
    else:
        raise PreventUpdate

@callback(
    Output("K-means", "figure"),
    Input("K-means-data", "data"),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'))
def outputKMeans(data, xaxis, yaxis):
    #print(data)
    if data is None:
        return px.scatter(df, x=xaxis, y=yaxis)
    if data:
        for i in data:
            #print(i)
            originalLabel = df["cell_type"] == i
            toPlot = df[originalLabel]
            fig = px.scatter(toPlot, x=xaxis, y=yaxis)
            return fig
    else:
        raise PreventUpdate

@callback(
    Output("PCA-data", "data"),
    Output("container-button-PCA", "children"),
    Input('submit-PCA', 'n_clicks'),)
def runPCA(n_clicks):

    if n_clicks is None or n_clicks < 0:
        raise PreventUpdate
    if n_clicks > 0:
        print("Starting PCA algo")
        data = makePCA()
        print("PCA end")
        return data,"PCA calculated"
    else:
        raise PreventUpdate

@callback(
    Output("PCA", "figure"),
    Input("PCA-data", "data"))
def outputPCA(data):
    #print(data)

    if data:
        #print(data)
        dfPCA = pd.read_json(data)
        fig = px.scatter(dfPCA, x="firstComponent", y="secondComponent")
        return fig
    else:
        raise PreventUpdate

"""    for i in data:
        print(i)
        originalLabel = df["cell_type"] == i
        toPlot = df[originalLabel]
        #print(toPlot)
        fig = px.scatter(toPlot, x=xaxis, y=yaxis)"""


"""
EXAMPLE OF BUTTON
@callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks')
)
def update_output(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    return (f'Thebutton has been clicked {n_clicks} times')
"""
"""@callback(
    Output('K-means', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'))
def update_graph(xaxis, yaxis):
    #print("value changed")
    fig = px.scatter(df, xaxis, yaxis)
    return fig
"""

"""
EXAMPLE OF KMEANS + GRAPH
@callback(
    Output('K-means-data', 'data'),
    Input('n_clusters', 'value'),
    Input('max_iter', 'value'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'))
def update_graph(n_clusters, max_iter, xaxis, yaxis):
    #print("value changed")
    return make_KMeans(n_clusters, max_iter, xaxis, yaxis)
"""