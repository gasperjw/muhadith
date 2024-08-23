import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Muhaddithūn and Fuqahā Map", "Journey of Scholars", "Contribute!"])

# Convert to dataframe
df = pd.read_csv('scholar_travels.csv')
#df = pd.DataFrame(data)

# Coordinates of locations (for simplicity, pre-determined for the example)
coordinates = {
    'Mecca': [21.4225, 39.8262],
    'Medina': [24.5247, 39.5692],
    'Kufa': [32.0511, 44.4409],
    'Basra': [30.5085, 47.7835],
    'Baghdad': [33.3152, 44.3661],
    'Egypt': [30.0333, 31.2333],
    'Nishapur': [36.2133, 58.7958],
    'Iraq': [33.3152, 44.3661],
    'Syria': [33.5138, 36.2765],
    'Gaza': [31.5017, 34.4668],
    'Yemen': [15.5527, 48.5164],
    'India': [20.5937, 78.9629],
    'China': [35.8617, 104.1954],
    'Tangier': [35.7595, -5.8340],
    'Damascus': [33.5138, 36.2765],
    'Tus': [36.5967, 59.1042],
    'Jerusalem': [31.7683, 35.2137],
    'Harran': [36.8610, 39.0278]
}

# Color-coding function based on travel index
def get_color(index):
    colors = ['blue', 'green', 'orange', 'purple', 'red', 'black']
    return colors[index % len(colors)]

def get_color_block(color):
# Return a block of color as an emoji to mimic the colored line
    color_blocks = {
        'blue': '🟦',
        'green': '🟩',
        'orange': '🟧',
        'purple': '🟪',
        'red': '🟥',
        'black': '⬛',
    }
    return color_blocks.get(color, '⬜')  # Default to white if color is not found

# Create a function to plot the map
def plot_map(scholar_filter=None):
    m = folium.Map(location=[25.0, 45.0], zoom_start=3)
    
    if scholar_filter:
        filtered_df = df[df['Scholar Name'] == scholar_filter]
        # Reset the travel index for each scholar
        for travel_index, row in enumerate(filtered_df.iterrows()):
            from_loc = coordinates[row[1]['From']]
            to_loc = coordinates[row[1]['To']]
            color = get_color(travel_index)
            
            # Popup information
            popup_info = f"""
            <strong>Travel {travel_index+1}</strong><br>
            <strong>Year:</strong> {row[1]['Year of Travel']}<br>
            <strong>From:</strong> {row[1]['From']}<br>
            <strong>To:</strong> {row[1]['To']}<br>
            <strong>What They Learned:</strong> {row[1]['What They Learned']}<br>
            <strong>Teacher(s):</strong> {row[1]['Teacher']}
            """
            
            # Add marker and line with popups
            folium.Marker(location=from_loc, popup=popup_info).add_to(m)
            folium.Marker(location=to_loc, popup=popup_info).add_to(m)
            folium.PolyLine(locations=[from_loc, to_loc], color=color, weight=2.5, opacity=0.8, popup=popup_info).add_to(m)
    else:
        # Handle the case when no scholar is selected (default to all scholars)
        for index, row in df.iterrows():
            from_loc = coordinates[row['From']]
            to_loc = coordinates[row['To']]
            color = get_color(index)
            
            # Popup information
            popup_info = f"""
            <strong>Travel {index+1}</strong><br>
            <strong>Year:</strong> {row['Year of Travel']}<br>
            <strong>From:</strong> {row['From']}<br>
            <strong>To:</strong> {row['To']}<br>
            <strong>What They Learned:</strong> {row['What They Learned']}<br>
            <strong>Teacher(s):</strong> {row['Teacher']}
            """
            
            # Add marker and line with popups
            folium.Marker(location=from_loc, popup=popup_info).add_to(m)
            folium.Marker(location=to_loc, popup=popup_info).add_to(m)
            folium.PolyLine(locations=[from_loc, to_loc], color=color, weight=2.5, opacity=0.8, popup=popup_info).add_to(m)

    return m


# Streamlit app
st.title("Travel Routes of Islamic Scholars")

scholar = st.selectbox('Select a Scholar:', options=['All Scholars'] + list(df['Scholar Name'].unique()))


# Scholar selection in sidebar
#  scholar = st.sidebar.selectbox('Select a Scholar:', options=['All Scholars'] + list(df['Scholar Name'].unique()))

# Plot map based on selection
if scholar == 'All Scholars':
    scholar_map = plot_map()
else:
    scholar_map = plot_map(scholar_filter=scholar)

# Display map
st_folium(scholar_map, width=700)

# Display scholar's travels details with a button click
if scholar != 'All Scholars':
    st.write(f"### Travels of {scholar}")
    scholar_info = df[df['Scholar Name'] == scholar]
    
    # Reset the travel index for each scholar in the expander
    for travel_index, (idx, row) in enumerate(scholar_info.iterrows(), start=1):  # Reset index for each scholar
        travel_color = get_color(travel_index - 1)  # Get the color for this travel (0-based for color)
        color_block = get_color_block(travel_color)  # Get the corresponding color block emoji
        
        # Expander title with colored block and reset travel index
        with st.expander(f"{color_block} Travel {travel_index}: {row['From']} to {row['To']} in {row['Year of Travel']}"):
            # Display travel details inside the expander
            st.write(f"**What They Learned**: {row['What They Learned']}")
            st.write(f"**Teacher(s)**: {row['Teacher']}")
