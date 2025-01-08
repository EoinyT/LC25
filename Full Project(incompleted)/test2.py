import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium
import dash
import dash_leaflet as dl
from dash import html, dcc, Input, Output

# --- Data Loading and Preparation ---
# Load and prepare your data
data = pd.read_csv(r'C:\Users\19ETallon.CDL\Desktop\CS\Full Project(incompleted)\Rainfall_Data_Germany_Complete.csv')

# Ensure necessary columns exist
required_columns = ['City', 'Latitude', 'Longitude', 'Rainfall (mm)', 'Temperature (°C)', 'Month', 'Year']
if not all(col in data.columns for col in required_columns):
    raise ValueError(f"Dataset must contain the following columns: {', '.join(required_columns)}")

# Filter data for the years 2015-2020
data = data[(data['Year'] >= 2015) & (data['Year'] <= 2020)]
data = data.dropna(subset=['Latitude', 'Longitude'])

# Convert to GeoDataFrame
geometry = [Point(xy) for xy in zip(data['Longitude'], data['Latitude'])]
geo_data = gpd.GeoDataFrame(data, geometry=geometry)

# --- Interactive Map with Widgets ---
def create_filtered_map(city=None, min_rainfall=0, max_rainfall=500, month=None, year=None):
    # Filter data based on input parameters
    filtered_data = geo_data[
        (geo_data['Rainfall (mm)'] >= min_rainfall) &
        (geo_data['Rainfall (mm)'] <= max_rainfall)
    ]
    if city:
        filtered_data = filtered_data[filtered_data['City'] == city]
    if month:
        filtered_data = filtered_data[filtered_data['Month'] == month]
    if year:
        filtered_data = filtered_data[filtered_data['Year'] == year]
    
    # Create the map
    map_center = [geo_data['Latitude'].mean(), geo_data['Longitude'].mean()]
    map_obj = folium.Map(location=map_center, zoom_start=6)
    
    # Add markers
    for _, row in filtered_data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"City: {row['City']}<br>Rainfall: {row['Rainfall (mm)']} mm<br>Temperature: {row['Temperature (°C)']} °C<br>Month: {row['Month']}<br>Year: {row['Year']}",
            tooltip=row['City']
        ).add_to(map_obj)
    
    return map_obj

#@interact
def interactive_map(city=geo_data['City'].unique().tolist() + [None], 
                    min_rainfall=(0, 500, 10), 
                    max_rainfall=(0, 500, 10),
                    month=list(range(1, 13)) + [None], 
                    year=list(range(2015, 2021)) + [None]):
    filtered_map = create_filtered_map(city, min_rainfall, max_rainfall, month, year)
    return filtered_map

# --- Dash App for Dynamic Updates ---
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Weather Map"),
    dcc.Dropdown(
        id='city-filter',
        options=[{'label': city, 'value': city} for city in data['City'].unique()],
        placeholder='Select a city'
    ),
    dcc.RangeSlider(
        id='rainfall-filter',
        min=data['Rainfall (mm)'].min(),
        max=data['Rainfall (mm)'].max(),
        step=10,
        marks={i: f"{i}" for i in range(0, 501, 100)},
        value=[data['Rainfall (mm)'].min(), data['Rainfall (mm)'].max()]
    ),
    dcc.Dropdown(
        id='month-filter',
        options=[{'label': f"Month {i}", 'value': i} for i in range(1, 13)],
        placeholder='Select a month'
    ),
    dcc.Dropdown(
        id='year-filter',
        options=[{'label': str(year), 'value': year} for year in range(2015, 2021)],
        placeholder='Select a year'
    ),
    dl.Map(
        id='map',
        center=[data['Latitude'].mean(), data['Longitude'].mean()],
        zoom=6,
        style={'height': '600px'},
        children=[dl.TileLayer()]
    )
])

@app.callback(
    Output('map', 'children'),
    [Input('city-filter', 'value'),
     Input('rainfall-filter', 'value'),
     Input('month-filter', 'value'),
     Input('year-filter', 'value')]
)
def update_map(city, rainfall_range, month, year):
    # Filter data
    filtered_data = data[
        (data['Rainfall (mm)'] >= rainfall_range[0]) &
        (data['Rainfall (mm)'] <= rainfall_range[1])
    ]
    if city:
        filtered_data = filtered_data[filtered_data['City'] == city]
    if month:
        filtered_data = filtered_data[filtered_data['Month'] == month]
    if year:
        filtered_data = filtered_data[filtered_data['Year'] == year]
    
    # Create map markers
    markers = [
        dl.Marker(
            position=[row['Latitude'], row['Longitude']],
            children=dl.Popup(f"City: {row['City']}. Rainfall: {row['Rainfall (mm)']}mm.  Month: {row['Month']}.  Year: {row['Year']}.")
        ) for _, row in filtered_data.iterrows()
    ]
    return [dl.TileLayer()] + markers

# --- Main Execution ---
if __name__ == '__main__':
    # Optionally, comment out one part depending on where you're running this.
    
    # Interactive Map for Jupyter Notebook
    # Uncomment below to use in Jupyter:
    # interactive_map()
    
    # Dynamic Updates with Dash for Web App
    # Uncomment below to run the web app:
    app.run_server(debug=True)
