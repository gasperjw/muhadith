import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Load the dataset
data_path = 'Hadith Scholars - Sheet1.csv'  # Path to your CSV file
data = pd.read_csv(data_path)

# Function to extract the earliest year from the "Date (AH)" column
def extract_year(date_ah):
    # Handle entries like "c. 19-103" or just "33-110" by splitting and taking the first year
    date_parts = date_ah.replace("c.", "").replace("d.", "").split('-')
    return int(date_parts[0].strip()) if len(date_parts) > 0 else None

# Apply the extraction to the "Date (AH)" column and store it in a new column "BornYear"
data['BornYear'] = data['Date (AH)'].apply(extract_year)

# Normalize the years for color grading
min_year = data['BornYear'].min()
max_year = data['BornYear'].max()

# Set up the folium map
m = folium.Map(location=[30, 40], zoom_start=4)

# Add a marker cluster
marker_cluster = MarkerCluster().add_to(m)

# Add points to the map
for idx, row in data.iterrows():
    # Determine color based on BornYear (normalized between min_year and max_year)
    normalized_year = (row['BornYear'] - min_year) / (max_year - min_year)
    color = plt.cm.viridis(normalized_year)

    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"<b>Name:</b> {row['Name']}<br><b>Work:</b> {row['Work']}<br><b>Born Year (AH):</b> {row['BornYear']}<br><b>Residence:</b> {row['Residence']}",
        icon=folium.Icon(color='blue' if normalized_year < 0.5 else 'green')
    ).add_to(marker_cluster)

# Display the map in the Streamlit app
st.title('Hadith Scholars Map')
st_folium(m, width=700, height=500)

