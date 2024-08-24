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


# Main Home Page
if page == "Home":
    # Create a beautiful UI for the home page
    st.title("📚 Scholars of Islam Project")
    st.write("""
    Welcome to the **Scholars of Islam** project, where we explore the vast contributions of **Muhaddithūn** 
    (scholars of Hadith) and **Fuqahā** (Islamic jurists) through interactive maps and detailed travel journeys. 
    This platform allows you to explore the lives, works, and travels of some of the most influential scholars in 
    Islamic history, while also giving you the opportunity to contribute additional data.
    """)

     # Add a message to direct users to use the sidebar for navigation
    st.info("👉 **Use the sidebar on the left to navigate between different sections of this app.**")

    # Add an expander to provide more detailed explanation
    with st.expander("Learn More About This Project"):
        st.write("""
        The Scholars of Islam Project aims to make the knowledge of early Islamic scholars more accessible and interactive.
        You can visualize the scholars' contributions to Islamic law and hadith sciences, see where they lived, and trace their journeys
        across the Islamic world.

        **Features**:
        - 📍 Explore the geographical spread of the scholars of Hadith and Fiqh.
        - 🌍 Follow the travels of renowned scholars and see what they learned and from whom.
        - ✏️ Contribute new data by adding scholar details and travel information.

        This platform helps to visualize the rich academic history of the Islamic world, bringing to life the journeys of 
        scholars who shaped Islamic law and thought over centuries.
        """)
    # if st.button("Scholar Journey"):
    #     st.switch_page("scholar_journey.py")




# Page 1 
elif page == "Muhaddithūn and Fuqahā Map":
    # Load the dataset
    data_path = 'Fiqh and Hadith Scholars.csv'  # Path to your CSV file
    data = pd.read_csv(data_path)

    # Function to extract the earliest year from the "Date (AH)" column
    def extract_year(date_ah):
        try:
            date_parts = date_ah.replace("c.", "").replace("d.", "").replace("p.", "").split('-')
            return int(date_parts[0].strip()) if len(date_parts) > 0 else None
        except ValueError:
            return None  # Return None if the date is not a valid integer

    # Apply the extraction to the "Date (AH)" column and store it in a new column "BornYear"
    data['BornYear'] = data['Date (AH)'].apply(extract_year)

    # Remove rows with missing years
    data = data.dropna(subset=['BornYear'])

    st.title('Muhaddithūn and Fuqahā Scholars Map')
    # Add a collapsible section for the description
    with st.expander("About this map"):
        st.write("""
        This interactive map showcases the major **Muhaddithūn** (scholars of Hadith) and **Fuqahā’** (Islamic jurists) 
        across different regions and time periods in Islamic history. Each marker represents a scholar, indicating their place of residence, 
        their known works, and the year they were born (in the Islamic calendar).

        **Filter Scholars**: Use the options in the sidebar to filter scholars based on their field of study (Hadith or Fiqh), 
        name, location, and birth year (AH). Click on any marker to learn more about the scholar, including their name, works, born year, and residence.

        The map clusters close markers together, but you can zoom in to view individual scholars and interact with each marker.
        """)

    st.sidebar.title("Filters")

    # Scholar Selection Dropdown
    scholar_name = st.sidebar.selectbox("Select a Scholar", options=["All Scholars"] + list(data['Name'].unique()))

    # Location Selection Dropdown
    location = st.sidebar.selectbox("Select a Location (Residence)", options=["All Locations"] + list(data['Residence'].unique()))

    # Study Selection Dropdown
    study = st.sidebar.selectbox("Select a Study", options=["All Studies"] + list(data['Famous For'].unique()))

    # Filter based on a year range using a slider
    min_year = int(data['BornYear'].min())
    max_year = int(data['BornYear'].max())
    year_range = st.sidebar.slider('Select the Born Year Range (AH)', min_year, max_year, (min_year, max_year))

    # Filter data based on the selected year range
    filtered_data = data[(data['BornYear'] >= year_range[0]) & (data['BornYear'] <= year_range[1])]

    # Apply scholar selection filter if a specific scholar is selected
    if scholar_name != "All Scholars":
        filtered_data = filtered_data[filtered_data['Name'] == scholar_name]

    # Apply location filter if a specific location is selected
    if location != "All Locations":
        filtered_data = filtered_data[filtered_data['Residence'] == location]

    # Apply study filter if a specific study is selected
    if study != "All Studies":
        filtered_data = filtered_data[filtered_data['Famous For'] == study]

    # Set up the folium map
    m = folium.Map(location=[30, 40], zoom_start=4)
    # m = folium.Map(
    # location=[30, 40], zoom_start= 2,
    # tiles='https://watercolormaps.collection.cooperhewitt.org/tile/watercolor/{z}/{x}/{y}.jpg',
    # attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under CC BY SA.'
    # )


    # tiles = "https://tiles.stadiamaps.com/tiles/stamen_watercolor/{z}/{x}/{y}.jpg"
    # attr = (
    #     '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> '
    #     '&copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> '
    #     '&copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> '
    #     '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    # )

    # # Define map location, zoom level, and min/max zoom
    # lat, lon = 41, 29
    # zoom_start = 10
    # min_zoom = 1
    # max_zoom = 16

    # # Create the map with custom tile layer, zoom limits, and attribution
    # m = folium.Map(location=[lat, lon], zoom_start=zoom_start, tiles=None, min_zoom=min_zoom, max_zoom=max_zoom)

    # # Add the custom tile layer
    # folium.TileLayer(tiles=tiles, attr=attr, name="Stadia Stamen Watercolor", min_zoom=min_zoom, max_zoom=max_zoom).add_to(m)

    # Add a marker cluster
    marker_cluster = MarkerCluster(disableClusteringAtZoom=10, maxClusterRadius=10).add_to(m)

    cmap = cm.get_cmap('viridis')

    for idx, row in filtered_data.iterrows():
        # Normalize the year for color grading
        normalized_year = (row['BornYear'] - min_year) / (max_year - min_year)
        rgba_color = cmap(normalized_year)
        hex_color = mcolors.to_hex(rgba_color)

        # Create circle markers with a popup
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=5,
            color=hex_color,
            fill=True,
            fill_color=hex_color,
            fill_opacity=0.8,
            popup=(f"<b>Name:</b> {row['Name']}<br>"
                   f"<b>Work:</b> {row['Work']}<br>"
                   f"<b>Born Year (AH):</b> {row['BornYear']}<br>"
                   f"<b>Residence:</b> {row['Residence']}")
        ).add_to(marker_cluster)

    # Display the map
    st_folium(m, width=700, height=500)

    st.dataframe(data[['Name', 'Residence', 'Famous For', 'Work', 'BornYear']])



# seconds page
elif page == "Journey of Scholars":

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

elif page == "Contribute!":
    st.title("Contribute to Scholar and Travel Data")
    
    # Display the CSV files
    st.subheader("Fiqh and Hadith Scholars Data")
    fiqh_scholars_df = pd.read_csv('Fiqh and Hadith Scholars.csv')
    st.dataframe(fiqh_scholars_df)

    st.subheader("Scholar Travels Data")
    travels_df = pd.read_csv('scholar_travels.csv')
    st.dataframe(travels_df)
    
    # Scholar Contribution Form
    st.subheader("Add a New Scholar Entry")
    with st.form("contribute_scholar_form"):
        # Scholar information form fields (all required)
        scholar_name = st.text_input("Scholar Name", value="", key="scholar_name")
        birth_year = st.text_input("Born Year (AH)", value="", key="birth_year")
        residence = st.text_input("Residence", value="", key="residence")
        work = st.text_input("Work", value="", key="work")
        famous_for = st.selectbox("Famous For", ["Hadith", "Fiqh", "Both"], key="famous_for")

        # Submit button for scholar form
        submitted_scholar = st.form_submit_button("Submit Scholar")

    # Process the submission for the scholar
    if submitted_scholar:
        if scholar_name and birth_year and residence and work:
            # New scholar entry
            new_scholar_row = {
                "Name": scholar_name,
                "BornYear": birth_year,
                "Residence": residence,
                "Work": work,
                "Famous For": famous_for
            }

            # Append the new row to a new CSV for contributions
            contributions_df = pd.DataFrame([new_scholar_row])
            contributions_file_path = 'contributed_scholars.csv'

            # Check if the file already exists
            try:
                # Append the new row to the existing file
                existing_contributions = pd.read_csv(contributions_file_path)
                contributions_df = pd.concat([existing_contributions, contributions_df], ignore_index=True)
            except FileNotFoundError:
                pass
            
            # Save the updated CSV
            contributions_df.to_csv(contributions_file_path, index=False)
            st.success("Scholar entry has been successfully submitted!")
        else:
            st.error("Please fill in all fields before submitting.")

    # Travel Contribution Form
    st.subheader("Add a New Scholar Travel Entry")
    with st.form("contribute_travel_form"):
        # Travel information form fields (all required)
        travel_scholar_name = st.text_input("Scholar Name", value="", key="travel_scholar_name")
        travel_from = st.text_input("Travel From", value="", key="travel_from")
        travel_to = st.text_input("Travel To", value="", key="travel_to")
        travel_year = st.text_input("Travel Year", value="", key="travel_year")
        what_they_learned = st.text_input("What They Learned", value="", key="what_they_learned")
        teachers = st.text_input("Teacher(s)", value="", key="teachers")

        # Submit button for travel form
        submitted_travel = st.form_submit_button("Submit Travel")

    # Process the submission for the travel
    if submitted_travel:
        if travel_scholar_name and travel_from and travel_to and travel_year and what_they_learned and teachers:
            # New travel entry
            new_travel_row = {
                "Scholar Name": travel_scholar_name,
                "From": travel_from,
                "To": travel_to,
                "Year of Travel": travel_year,
                "What They Learned": what_they_learned,
                "Teacher(s)": teachers
            }

            # Append the new row to a new CSV for contributions
            travels_contrib_df = pd.DataFrame([new_travel_row])
            travels_file_path = 'contributed_travels.csv'

            # Check if the file already exists
            try:
                existing_travels_contrib = pd.read_csv(travels_file_path)
                travels_contrib_df = pd.concat([existing_travels_contrib, travels_contrib_df], ignore_index=True)
            except FileNotFoundError:
                pass
            
            # Save the updated CSV
            travels_contrib_df.to_csv(travels_file_path, index=False)
            st.success("Travel entry has been successfully submitted!")
        else:
            st.error("Please fill in all fields before submitting.")

