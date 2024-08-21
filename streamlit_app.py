import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Load the dataset
data_path = 'Hadith Scholars - Sheet1.csv'  # Path to your CSV file
data = pd.read_csv(data_path)

# Function to extract the earliest year from the "Date (AH)" column
def extract_year(date_ah):
    try:
        # Handle entries like "c. 19-103" or just "33-110" by splitting and taking the first year
        date_parts = date_ah.replace("c.", "").replace("d.", "").replace("p.", "").split('-')
        return int(date_parts[0].strip()) if len(date_parts) > 0 else None
    except ValueError:
        return None  # Return None if the date is not a valid integer

# Apply the extraction to the "Date (AH)" column and store it in a new column "BornYear"
data['BornYear'] = data['Date (AH)'].apply(extract_year)

# Remove rows with missing years
data = data.dropna(subset=['BornYear'])

# Add a collapsible section for the description
with st.expander("About this map"):
    st.write("""
    This interactive map showcases the major **Muhaddithūn** (scholars of Hadith) across different regions 
    and time periods in Islamic history. Each marker represents a scholar, indicating their place of residence, 
    their known works, and the year they were born (in the Islamic calendar).

    **Filter Scholars**: Use the slider in the sidebar to filter scholars based on their birth year (AH). 
    Click on any marker to learn more about the scholar, including their name, works, born year, and residence.

    The map clusters close markers together, but you can zoom in to view individual scholars and interact with each marker.
    """)

# Set up Streamlit app layout
st.title('Hadith Scholars Map')
st.sidebar.title('Filter Scholars')

# Scholar Selection Dropdown
scholar_name = st.sidebar.selectbox("Select a Scholar", options=["All Scholars"] + list(data['Name']))

# Filter based on a year range using a slider
min_year = int(data['BornYear'].min())
max_year = int(data['BornYear'].max())
year_range = st.sidebar.slider('Select the Born Year Range (AH)', min_year, max_year, (min_year, max_year))

# Filter data based on the selected range
filtered_data = data[(data['BornYear'] >= year_range[0]) & (data['BornYear'] <= year_range[1])]

# Apply scholar selection filter if a specific scholar is selected
if scholar_name != "All Scholars":
    filtered_data = filtered_data[filtered_data['Name'] == scholar_name]

# Set up the folium map
m = folium.Map(location=[30, 40], zoom_start=4)

# Add a marker cluster with options to disable clustering at higher zoom levels
marker_cluster = MarkerCluster(
    disableClusteringAtZoom=10,  # Disable clustering at zoom levels above 10
    maxClusterRadius=30          # Make the clustering more sensitive to distance
).add_to(m)

# Add points to the map
for idx, row in filtered_data.iterrows():
    # Normalize the year for color grading
    normalized_year = (row['BornYear'] - min_year) / (max_year - min_year)
    
    # Use a colormap for better contrast (e.g., viridis)
    color = cm.viridis(normalized_year)

    # Create markers with a popup showing detailed information
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=(
            f"<b>Name:</b> {row['Name']}<br>"
            f"<b>Work:</b> {row['Work']}<br>"
            f"<b>Born Year (AH):</b> {row['BornYear']}<br>"
            f"<b>Residence:</b> {row['Residence']}"
        ),
        icon=folium.Icon(color='blue' if normalized_year < 0.5 else 'green')
    ).add_to(marker_cluster)

# Display the map in Streamlit app
st_folium(m, width=700, height=500)


# import streamlit as st
# import pandas as pd
# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import st_folium
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm

# # Load the dataset
# data_path = 'Hadith Scholars - Sheet2.csv'  # Path to your CSV file
# data = pd.read_csv(data_path)

# # Function to extract the earliest year from the "Date (AH)" column
# def extract_year(date_ah):
#     try:
#         # Handle entries like "c. 19-103" or just "33-110" by splitting and taking the first year
#         date_parts = date_ah.replace("c.", "").replace("d.", "").replace("p.", "").split('-')
#         return int(date_parts[0].strip()) if len(date_parts) > 0 else None
#     except ValueError:
#         return None  # Return None if the date is not a valid integer

# # Apply the extraction to the "Date (AH)" column and store it in a new column "BornYear"
# data['BornYear'] = data['Date (AH)'].apply(extract_year)

# # Remove rows with missing years
# data = data.dropna(subset=['BornYear'])

# # Set up Streamlit app layout
# st.title('Hadith Scholars Map')
# st.sidebar.title('Filter Scholars by Born Year')

# with st.expander("About this map"):
#     st.write("""
#     This interactive map showcases the major **Muhaddithūn** (scholars of Hadith) across different regions 
#     and time periods in Islamic history. Each marker represents a scholar, indicating their place of residence, 
#     their known works, and the year they were born (in the Islamic calendar).

#     **Filter Scholars**: Use the slider in the sidebar to filter scholars based on their birth year (AH). 
#     Click on any marker to learn more about the scholar, including their name, works, born year, and residence.

#     The map clusters close markers together, but you can zoom in to view individual scholars and interact with each marker.
#     """)

# # Filter based on a year range using a slider
# min_year = int(data['BornYear'].min())
# max_year = int(data['BornYear'].max())
# year_range = st.sidebar.slider('Select the Born Year Range (AH)', min_year, max_year, (min_year, max_year))

# # Filter data based on the selected range
# filtered_data = data[(data['BornYear'] >= year_range[0]) & (data['BornYear'] <= year_range[1])]

# # Set up the folium map
# m = folium.Map(location=[30, 40], zoom_start=4)

# # Add a marker cluster
# marker_cluster = MarkerCluster().add_to(m)

# # Add points to the map
# for idx, row in filtered_data.iterrows():
#     # Normalize the year for color grading
#     normalized_year = (row['BornYear'] - min_year) / (max_year - min_year)
    
#     # Use a colormap for better contrast (e.g., viridis)
#     color = cm.viridis(normalized_year)

#     # Create markers with a popup showing detailed information
#     folium.Marker(
#         location=[row['Latitude'], row['Longitude']],
#         popup=(
#             f"<b>Name:</b> {row['Name']}<br>"
#             f"<b>Work:</b> {row['Work']}<br>"
#             f"<b>Born Year (AH):</b> {row['BornYear']}<br>"
#             f"<b>Residence:</b> {row['Residence']}"
#         ),
#         icon=folium.Icon(color='blue' if normalized_year < 0.5 else 'green')
#     ).add_to(marker_cluster)

# # Display the map in Streamlit app
# st_folium(m, width=700, height=500)
