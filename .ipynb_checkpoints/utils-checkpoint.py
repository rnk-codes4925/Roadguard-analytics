import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_data_filepath():
    return "data.csv"

def generate_mock_data():
    filepath = get_data_filepath()
    if os.path.exists(filepath):
        return

    np.random.seed(42)
    n_records = 8000

    # Date range: 2021 (PY) and 2022 (CY)
    start_date = datetime(2021, 1, 1)
    dates = [start_date + timedelta(days=int(np.random.randint(0, 730))) for _ in range(n_records)]
    
    # Severity distribution
    severities = np.random.choice(['Fatal', 'Serious', 'Slight'], size=n_records, p=[0.02, 0.15, 0.83])
    
    # Speed limits
    speed_limits = np.random.choice([20, 30, 40, 50, 60, 70], size=n_records, p=[0.1, 0.5, 0.1, 0.05, 0.2, 0.05])
    
    # Road types
    road_types = np.random.choice(
        ['Single carriageway', 'Dual carriageway', 'Roundabout', 'One way street', 'Slip road'],
        size=n_records,
        p=[0.70, 0.18, 0.07, 0.03, 0.02]
    )
    
    # Urban or Rural
    urban_rural = np.random.choice(['Urban', 'Rural'], size=n_records, p=[0.62, 0.38])
    
    # Weather conditions
    weather = np.random.choice(
        ['Fine no high winds', 'Raining no high winds', 'Raining + high winds', 'Snowing no high winds', 'Fog or mist'],
        size=n_records,
        p=[0.80, 0.14, 0.03, 0.01, 0.02]
    )
    
    # Light conditions
    light = np.random.choice(['Day', 'Dark'], size=n_records, p=[0.74, 0.26])
    
    # Road Surface Conditions
    road_surface = np.random.choice(
        ['Dry', 'Wet or damp', 'Frost or ice', 'Snow', 'Flood'],
        size=n_records,
        p=[0.72, 0.23, 0.03, 0.01, 0.01]
    )
    
    # Districts (Geographical Hotspots)
    districts = np.random.choice(
        ['Birmingham', 'Leeds', 'Cornwall', 'Bradford', 'Sheffield', 'County Durham', 'Liverpool', 'Cheshire East', 'Manchester', 'Kirklees'],
        size=n_records,
        p=[0.25, 0.18, 0.12, 0.10, 0.09, 0.07, 0.06, 0.05, 0.05, 0.03]
    )
    
    # Coordinates mapping for realistic visualization
    district_coords = {
        'Birmingham': (52.4862, -1.8904),
        'Leeds': (53.8008, -1.5491),
        'Cornwall': (50.2632, -5.0510),
        'Bradford': (53.7960, -1.7594),
        'Sheffield': (53.3811, -1.4701),
        'County Durham': (54.7761, -1.5733),
        'Liverpool': (53.4084, -2.9916),
        'Cheshire East': (53.2291, -2.3168),
        'Manchester': (53.4808, -2.2426),
        'Kirklees': (53.6458, -1.7850)
    }
    
    latitudes = []
    longitudes = []
    for d in districts:
        base_lat, base_lon = district_coords[d]
        # Add slight jitter for realistic coordinate spreads
        latitudes.append(base_lat + np.random.normal(0, 0.03))
        longitudes.append(base_lon + np.random.normal(0, 0.03))
        
    # Casualties: random integer based on severity
    casualties = []
    for s in severities:
        if s == 'Fatal':
            casualties.append(np.random.choice([1, 2, 3], p=[0.8, 0.15, 0.05]))
        elif s == 'Serious':
            casualties.append(np.random.choice([1, 2, 3, 4], p=[0.7, 0.2, 0.08, 0.02]))
        else:
            casualties.append(np.random.choice([1, 2], p=[0.9, 0.1]))
            
    # Vehicle Type
    vehicles = np.random.choice(
        ['Car', 'Bike', 'Bus', 'Van', 'Agricultural', 'Other'],
        size=n_records,
        p=[0.75, 0.12, 0.05, 0.05, 0.01, 0.02]
    )

    df = pd.DataFrame({
        'Accident_Index': [f"ACC{2021000000 + i}" for i in range(n_records)],
        'Date': [d.strftime('%Y-%m-%d') for d in dates],
        'Speed_Limit': speed_limits,
        'Road_Type': road_types,
        'Urban_or_Rural_Area': urban_rural,
        'Weather_Conditions': weather,
        'Light_Conditions': light,
        'Road_Surface_Conditions': road_surface,
        'Casualties': casualties,
        'Severity': severities,
        'District': districts,
        'Latitude': latitudes,
        'Longitude': longitudes,
        'Vehicle_Type': vehicles
    })
    
    df.to_csv(filepath, index=False)

def load_and_preprocess_data():
    generate_mock_data()
    df = pd.read_csv(get_data_filepath())
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Month_Name'] = df['Date'].dt.strftime('%b')
    return df

def get_filter_options(df):
    return {
        'road_surface': ['All'] + sorted(df['Road_Surface_Conditions'].dropna().unique().tolist()),
        'weather': ['All'] + sorted(df['Weather_Conditions'].dropna().unique().tolist()),
        'severity': ['All'] + sorted(df['Severity'].dropna().unique().tolist()),
        'urban_rural': ['All'] + sorted(df['Urban_or_Rural_Area'].dropna().unique().tolist()),
        'district': ['All'] + sorted(df['District'].dropna().unique().tolist())
    }

def filter_dataframe(df, road_surface='All', weather='All', severity='All', urban_rural='All', district='All'):
    filtered = df.copy()
    if road_surface != 'All':
        filtered = filtered[filtered['Road_Surface_Conditions'] == road_surface]
    if weather != 'All':
        filtered = filtered[filtered['Weather_Conditions'] == weather]
    if severity != 'All':
        filtered = filtered[filtered['Severity'] == severity]
    if urban_rural != 'All':
        filtered = filtered[filtered['Urban_or_Rural_Area'] == urban_rural]
    if district != 'All':
        filtered = filtered[filtered['District'] == district]
    return filtered