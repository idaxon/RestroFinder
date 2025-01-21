import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the uploaded dataset
file_path = 'dineout_data_cleaned_final.csv'
data = pd.read_csv(file_path)

# Data preprocessing
data['Cuisine'] = data['Cuisine'].fillna('Unknown')
data['Address'] = data['Address'].fillna('Unknown')
data['Cost_for_2'] = data['Cost_for_2'].fillna(data['Cost_for_2'].mean())
data['Stars'] = data['Stars'].fillna(data['Stars'].mean())
data['Rating_Category'] = pd.cut(data['Stars'], bins=[0, 2, 4, 5], labels=['Low', 'Average', 'High'])

# Famous cuisines for easy selection
famous_cuisines = ['Indian', 'Chinese', 'Italian', 'Mexican', 'Thai']

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "RestoFinder"

# Navbar
navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col(html.A("RestoFinder", href="#", style={"fontSize": "24px", "fontWeight": "bold", "color": "white"})),
        ], align="center"),
    ]),
    color="dark",
    dark=True,
    className="mb-4",
)

# Footer
footer = html.Footer(
    dbc.Container([
        html.Div([
            html.P("RestoFinder: Your personalized restaurant recommendation dashboard.", style={"textAlign": "center"}),
            html.Hr(),
            html.H5("About", style={"textAlign": "center"}),
            html.P("RestoFinder helps you discover the best dining experiences based on your preferences. Whether you're looking for budget-friendly options or top-rated cuisines, we've got you covered.", style={"textAlign": "center", "marginBottom": "10px"}),
            html.P("Contact us: info@restofinder.com", style={"textAlign": "center"}),
        ], style={"padding": "20px"})
    ])
)

# Landing Page
landing_page = html.Div([
    html.Div([
        html.H1("Welcome to RestoFinder!", style={"textAlign": "center", "marginBottom": "20px"}),
        html.P(
            "Discover the best restaurants tailored to your taste and budget. Use our dashboard to filter by cuisine, price, and ratings to find the perfect spot for any occasion.",
            style={"textAlign": "center", "fontSize": "18px", "marginBottom": "20px"}
        ),
        dbc.Row([
            dbc.Col(html.Img(src="https://i.pinimg.com/originals/25/45/9d/25459d1991189f8c04c6e63678f09336.gif", style={"width": "100%", "borderRadius": "10px"}), width=6),
            dbc.Col([
                html.H4("Why Choose Us?", style={"marginBottom": "15px"}),
                html.Ul([
                    html.Li("Personalized recommendations tailored to your taste."),
    html.Li("Extensive database of restaurants across various cuisines."),
    html.Li("Interactive and user-friendly dashboard for seamless browsing."),
    html.Li("Real-time updates on trending restaurants and offers."),
    html.Li("Advanced filtering options to refine your search."),
    html.Li("Verified user reviews and ratings for trustworthy recommendations."),
    html.Li("Detailed restaurant profiles with menus, photos, and pricing."),
    html.Li("Mobile-friendly design for on-the-go access."),
    html.Li("Exclusive deals and discounts available for registered users."),
    html.Li("24/7 customer support to assist with your queries."),
                ], style={"fontSize": "24px"})
            ], width=6),
        ], justify="center"),
    ], style={"padding": "40px"}),
    html.Hr(),
])

# Layout
app.layout = html.Div([
    navbar,
    landing_page,
    html.Div([], style={"height": "20px"}),
    html.Div([
        html.H1("Restaurant Recommendation Dashboard", style={"textAlign": "center"}),

        # Filters
        dbc.Row([
            dbc.Col([
                html.Label("Enter Price per Person (INR)"),
                dcc.Input(id='price-per-person', type='number', placeholder="Enter price per person", style={"width": "100%"})
            ], width=4),
            dbc.Col([
                html.Label("Select Cuisine"),
                html.Div([
                    dbc.Checklist(
                        id='cuisine-checklist',
                        options=[{'label': cuisine, 'value': cuisine} for cuisine in famous_cuisines],
                        inline=True
                    ),
                    dcc.Dropdown(
                        id='cuisine-dropdown',
                        options=[{'label': cuisine, 'value': cuisine} for cuisine in data['Cuisine'].unique() if cuisine not in famous_cuisines],
                        placeholder="Select more cuisines",
                        multi=True
                    )
                ])
            ], width=4),
            dbc.Col([
                html.Label("Number of People"),
                dcc.Input(id='num-people', type='number', placeholder="Enter number of people", style={"width": "100%"})
            ], width=4),
        ]),

        html.Br(),

        # Button and output
        dbc.Row([
            dbc.Col([
                html.Button("Find Top Locations", id='find-locations-btn', n_clicks=0, className="btn btn-primary")
            ], width=12, style={"textAlign": "center"}),
        ]),

        html.Br(),

        html.Div(id='top-locations-output', style={"textAlign": "center", "fontSize": "18px"}),

        html.Br(),

        # Map for selected locations
        html.Div([
            html.H4("Selected Locations Map", style={"textAlign": "center"}),
            dcc.Graph(id='selected-locations-map')
        ]),

        html.Br(),

        # General map
        html.Div([
            html.H4("Overall Restaurant Heatmap", style={"textAlign": "center"}),
            dcc.Graph(id='general-heatmap')
        ]),

        html.Br(),

        # Graphs
        dbc.Row([
            dbc.Col(dcc.Graph(id='rating-distribution'), width=6),
            dbc.Col(dcc.Graph(id='location-heatmap'), width=6),
        ]),

        html.Br(),
    ]),
    footer
])

# Callbacks
@app.callback(
    [Output('top-locations-output', 'children'),
     Output('selected-locations-map', 'figure')],
    [Input('find-locations-btn', 'n_clicks')],
    [State('price-per-person', 'value'),
     State('cuisine-checklist', 'value'),
     State('cuisine-dropdown', 'value'),
     State('num-people', 'value')]
)
def find_top_locations(n_clicks, price_per_person, selected_cuisines, additional_cuisines, num_people):
    if n_clicks > 0:
        if not all([price_per_person, num_people]) or not (selected_cuisines or additional_cuisines):
            return "Please provide all inputs.", {}

        # Combine selected cuisines
        all_cuisines = (selected_cuisines or []) + (additional_cuisines or [])

        # Filter and calculate total cost
        data['Cost_per_Person'] = data['Cost_for_2'] / 2
        filtered_data = data[(data['Cost_per_Person'] <= price_per_person) & (data['Cuisine'].isin(all_cuisines))]
        filtered_data['Total_Cost'] = filtered_data['Cost_per_Person'] * num_people

        # Sort by rating and get top 5
        top_locations = filtered_data.sort_values(by='Stars', ascending=False).head(5)

        if top_locations.empty:
            return "No restaurants found matching your criteria.", {}

        # Predict the best restaurant
        best_restaurant = top_locations.iloc[0]
        reasons = [
            f"Highest rating of {best_restaurant['Stars']} stars.",
            f"Serves {best_restaurant['Cuisine']}, a popular choice.",
            f"Located at {best_restaurant['Address']}.",
            f"Affordable with a cost of {best_restaurant['Cost_per_Person']} per person."
        ]
        reasons_bullets = html.Ul([html.Li(reason) for reason in reasons])

        # Create output table
        table = dbc.Table.from_dataframe(
            top_locations[['Address', 'Cuisine', 'Cost_per_Person', 'Stars', 'Total_Cost', 'Name']],
            striped=True, bordered=True, hover=True, className="table-dark"
        )

        # Create map for selected locations
        map_fig = px.scatter_mapbox(
            top_locations,
            lat='Latitude', lon='Longitude',
            text='Name',
            hover_name='Address',
            color='Stars',
            size='Stars',
            center=dict(lat=28.61, lon=77.23),
            zoom=10,
            mapbox_style="open-street-map",
            title="Selected Restaurant Locations"
        )

        return html.Div([
            html.H5(f"Best Restaurant: {best_restaurant['Name']}", style={"marginBottom": "10px"}),
            reasons_bullets,
            html.Br(),
            table
        ]), map_fig

    return "", {}

@app.callback(
    [Output('rating-distribution', 'figure'),
     Output('location-heatmap', 'figure'),
     Output('general-heatmap', 'figure')],
    [Input('find-locations-btn', 'n_clicks')]
)
def update_visuals(n_clicks):
    if n_clicks >= 0:
        # Rating distribution
        rating_fig = px.histogram(
            data, x='Stars', nbins=20,
            title="Rating Distribution",
            labels={'Stars': 'Rating', 'count': 'Count'}
        )

        # Location-specific heatmap
        heatmap_fig = px.density_mapbox(
            data,
            lat='Latitude', lon='Longitude',
            z='Stars',
            radius=10,
            center=dict(lat=28.61, lon=77.23),
            zoom=10,
            mapbox_style="open-street-map",
            title="Top Restaurant Locations Heatmap"
        )

        # General heatmap
        general_heatmap_fig = px.density_mapbox(
            data,
            lat='Latitude', lon='Longitude',
            radius=10,
            center=dict(lat=28.61, lon=77.23),
            zoom=10,
            mapbox_style="open-street-map",
            title="Overall Restaurant Heatmap"
        )

        return rating_fig, heatmap_fig, general_heatmap_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
