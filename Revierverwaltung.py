import streamlit as st

from streamlit_folium import st_folium

import folium

import pandas as pd

import geopandas as gpd

from shapely.geometry import Point

 

# -- Helper functions --

def save_points(gdf):

    gdf.to_file('pois.geojson', driver='GeoJSON')

 

def load_points():

    try:

        return gpd.read_file('pois.geojson')

    except:

        return gpd.GeoDataFrame(columns=['name', 'symbol', 'number', 'geometry'], geometry='geometry', crs="EPSG:4326")

 

# -- Streamlit UI --

st.title("POI Manager for Swisstopo")

gdf = load_points()

 

st.write("Existing Points:")

st.write(gdf)

 

# Folium Map

m = folium.Map(location=[46.8, 8.2], zoom_start=7)

for _, row in gdf.iterrows():

    folium.Marker(

        location=[row.geometry.y, row.geometry.x],

        popup=f"{row['name']} ({row['number']})",

        icon=folium.Icon(icon=row['symbol'] if isinstance(row['symbol'], str) else "info-sign")

    ).add_to(m)

 

map_data = st_folium(m, width=600, height=400)

 

# Add new point

st.subheader("Add new Point of Interest")

lat = st.number_input("Latitude", value=46.8, format="%.6f")

lon = st.number_input("Longitude", value=8.2, format="%.6f")

name = st.text_input("Name", value="POI Name")

symbol = st.selectbox("Symbol", options=['info-sign', 'star', 'cloud', 'flag'])

number = st.number_input("Number", value=1, step=1)

 

if st.button("Add Point"):

    new_point = gpd.GeoDataFrame(

        [[name, symbol, number, Point(lon, lat)]],

        columns=['name', 'symbol', 'number', 'geometry'],

        geometry='geometry',

        crs="EPSG:4326"

    )

    gdf = pd.concat([gdf, new_point], ignore_index=True)

    save_points(gdf)

    st.experimental_rerun()

 

# Export

if st.button("Export GeoJSON"):

    save_points(gdf)

    st.success("Exported pois.geojson. You can now upload this to maps.geo.admin.ch.")

 
