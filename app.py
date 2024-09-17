# Import necessary packages
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="UNHCR Refugee Data Explorer", layout="wide")

@st.cache_data
# Read file "edit3.xlsx"
def load_data(url):
    """read data for data cache"""
    cache_df = pd.read_excel(url)
    return cache_df

# Load data from the URL
df=load_data("edit4.xlsx")
#st.dataframe(df)

# Check if required columns are present
required_columns = ["Country of origin", "Country of asylum", "Year"]
for col in required_columns:
    if col not in df.columns:
        st.error(f"Column '{col}' is missing from the data.")
        st.stop()

# Handle missing or empty cells
df.fillna(0.0, inplace=True)

# Create filters by year with interactive dropdown including an option to display data for all years
st.sidebar.subheader("Filters")
year_options = ["All Years"] + list(df["Year"].unique())
year_filter = st.sidebar.selectbox("Year", year_options)

# Filter data based on the selected year
if year_filter != "All Years":
    df_filtered = df[df["Year"] == year_filter]
else:
    df_filtered = df

# Check if the filtered data is empty
if df_filtered.empty:
    st.warning("No data available for the selected year.")
else:
    # Create grouped DataFrame and accumulated values. 
    df_grouped = df_filtered.groupby(["Country of origin", "Country of asylum", "Refugees under UNHCR's mandate"]).size().reset_index(name="Count")

    # Create a list of unique countries for origin and asylum
    unique_origins = list(df_grouped["Country of origin"].unique())
    unique_asylums = list(df_grouped["Country of asylum"].unique())
    all_countries = unique_origins + unique_asylums

    # Create a mapping from country names to indices
    country_to_index = {country: idx for idx, country in enumerate(all_countries)}

    # Map the source and target countries to their respective indices
    df_grouped["source_idx"] = df_grouped["Country of origin"].map(country_to_index)
    df_grouped["target_idx"] = df_grouped["Country of asylum"].map(country_to_index)

    # Create a list of the Top 50 countries in "Country of asylum"
    top_50_asylums = list(df_grouped.sort_values(by="Refugees under UNHCR's mandate", ascending=False)["Country of asylum"].head(50))
    # Create a list of the Top 20 countries in "Country of origin"
    top_20_origins = list(df_grouped.sort_values(by="Refugees under UNHCR's mandate", ascending=False)["Country of origin"].head(20))

    # Filter the grouped DataFrame for the top origins and asylums
    df_top_grouped = df_grouped[
        df_grouped["Country of origin"].isin(top_20_origins) & 
        df_grouped["Country of asylum"].isin(top_50_asylums)
    ]

    # Create source and target lists for the Sankey graph
    source = df_top_grouped["source_idx"].tolist()
    target = df_top_grouped["target_idx"].tolist()
    value = df_top_grouped["Refugees under UNHCR's mandate"].tolist()

    # Create a list of unique countries in top_50_asylums
    unique_countries_asylum = list(set(top_50_asylums))
    length_unique_countries_asylum = len(unique_countries_asylum)

    # Create a list of unique countries in top_20_origins
    unique_countries_origin = list(set(top_20_origins))
    length_unique_countries_origin = len(unique_countries_origin)                                   

    # Create a list of 50 beautiful colors as valid values. Exclude black
    colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    # Make dictionary with 50 unique countries in top_50_asylums as keys and 50 beautiful colors as values
    color_dict = {unique_countries_asylum[i]: colors[i] for i in range(length_unique_countries_asylum)}

    # Create a list of 20 beautiful colors as valid values. Exclude black
    colors_orgin=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5']
    # Make dictionary with 20 unique countries in top_20_origins as keys and 20 beautiful colors as values
    color_dict_origin = {unique_countries_origin[i]: colors[i] for i in range(length_unique_countries_origin)}

    # Create Sankey graph
    # assign colors to node and link 
    node_colors = [color_dict.get(country, "gray") for country in all_countries]
    link_colors = [color_dict.get(df_top_grouped["Country of asylum"].iloc[i], "gray") for i in range(len(df_top_grouped))]

    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_countries,
            color=node_colors,
        ),
        link=dict(
            source=source,  
            target=target,  
            value=value,
            color=link_colors,
        )
    )])

    
    # Update layout to make the graph container bigger and wider
    fig.update_layout(
        title_text=f"REFUGEES GLOBAL FLOW - ({year_filter})",
        title_font_size=25,
        font_size=15,
        width=1200,  # Set the width of the figure
        height=1200   # Set the height of the figure
    )
    
    # Display the figure in Streamlit with full container width
    st.plotly_chart(fig, use_container_width=True)
