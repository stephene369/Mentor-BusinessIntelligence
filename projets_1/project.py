import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)


data = pd.read_csv('US+Candy+Distributor/sales_uszips.csv')
data.columns

# Create map
fig_map = px.scatter_mapbox(data, 
                            lat='lat', 
                            lon='lng',
                            # size='Cost',
                            color='isFactory',
                            # animation_frame='year',
                            animation_group='isFactory',
                            hover_name='city',
                            # color_continuous_scale='viridis',
                            zoom=5 ,     width=900,
                            size = [1] * len(data),
    height=400
                            )

fig_map.update_layout(
    mapbox_style='open-street-map',
    mapbox_zoom=3,
    mapbox_center={'lat': 40, 'lon': -90},
    margin={'l': 0, 'r': 0, 't': 0, 'b': 0}
)




data_ = pd.read_csv('US+Candy+Distributor/profit-shipMode.csv')
wonka = data_[data_['Product-Name'] == 'Wonka Bar - Nutty Crunch Surprise']
fig = px.bar(
    data_frame=wonka,
    x='Ship-Mode',
    y='Profit',
    color='Ship-Mode',
    barmode='group',
    width=800,
    height=500
)

# Amélioration du style
fig.update_layout(
    bargap=0.1,
    bargroupgap=0.1,
    title='Profit par Mode de Livraison',
    xaxis_title='Mode de Livraison',
    yaxis_title='Profit ($)', 
    
)


# Create pivot table
tableau_croise_dynamique = data_.pivot_table(values='Profit', 
                                           index='Product-Name', 
                                           columns='Ship-Mode')

# Create heatmap visualization
fig_pivot = px.imshow(tableau_croise_dynamique,
                     labels=dict(x="Ship Mode", 
                               y="Product Name", 
                               color="Profit"),
                     aspect="auto",
                     
                     width=800,
                     height=500)

fig_pivot.update_layout(
    title='Profit by Product and Shipping Mode',
    xaxis_title='Shipping Mode',
    yaxis_title='Product Name'
)





title = html.H1('US Candy Distributor')



# Dashboard layout
app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='assets/style.css'
    ),
    title,
    
    html.H3('Localisation des clients de US candy; Distance Clients Usine ' , className='questions'),
    html.Div([

        html.Div([
        
        html.H2('Repartition des clients de la compani a travers les Etats Unis '),
        html.P('''
            Cette carte montre la repartition des clients de US Candy. En bleue les clients ayant deja acheter une fois au moins chez nous 
               et en rouge les usines. 
               '''),
            html.Ul([
                html.Li(""" 
                        D'après l'analyse de la carte, les clients de US 
                        Candy présentent une distribution géographique stratégique 
                        à travers le pays. La répartition spatiale révèle une couverture 
                        nationale efficace, avec une présence notable sur l'ensemble du 
                        territoire. Cette distribution équilibrée témoigne d'une pénétration 
                        de marché réussie et d'un réseau de distribution bien établi.
                        """),


            ]) , 

        ] , className='description'),
        dcc.Graph(figure=fig_map) , 
    

    ], className='dashboard-card'),
    







    html.H3('Temps de livraison et cout d\'expedition ;' , className='questions'),
    html.Div([

    html.Div([
        html.H2('Variation du profit en function du mode de livraison '),

        ] , className='description'),

        html.Div([
        dcc.Graph(figure=fig) , 
        dcc.Graph(figure=fig_pivot , className='tableau') ,
        ], style={'display': 'flex', 'flexDirection': 'row'}), 

        html.P('''
            Ce graphique montre la variation du profit en fonction du mode de 
               livraison pour le produit Wonka Bar - Nutty Crunch Surprise.

Nous pouvons observer que, quelle que soit le mode de livraison sélectionné 
               (qu’il s’agisse d’une livraison standard, rapide, ou express), 
               le profit reste constant. 
               Cette absence de variation semble également s'appliquer à l'ensemble des produits, indépendamment de la quantité achetée par les clients.
               '''),


    ], className='dashboard-card', style={'display': 'flex', 'flexDirection': 'column'}),









], className='dashboard-container')

# Create a new file 'assets/style.css' with the following content:
''''''

# To access the server from Windows browser:
# 1. Find your WSL IP address by running 'ip addr show' in WSL terminal
# 2. Use the WSL IP instead of 127.0.0.1
# Example: If WSL IP is 172.17.xxx.xxx, access http://172.17.xxx.xxx:8051 in Windows browser

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8051)