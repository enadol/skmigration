# Import necessary packages
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Read file "edit3.xlsx"
df = pd.read_excel("edit3.xlsx")
print(df.columns)

# Check if required columns are present
required_columns = ["Country of origin", "Country of asylum", "Year"]
for col in required_columns:
    if col not in df.columns:
        st.error(f"Column '{col}' is missing from the data.")
        st.stop()

# Handle missing or empty cells
df.fillna("Unknown", inplace=True)

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
    # Create grouped DataFrame and accumulated values
    df_grouped = df_filtered.groupby(["Country of origin", "Country of asylum"]).size().reset_index(name="Count")

    # Create a list of unique countries for origin and asylum
    unique_origins = list(df_grouped["Country of origin"].unique())
    unique_asylums = list(df_grouped["Country of asylum"].unique())
    all_countries = unique_origins + unique_asylums

    # Create a mapping from country names to indices
    country_to_index = {country: idx for idx, country in enumerate(all_countries)}

    # Map the source and target countries to their respective indices
    df_grouped["source_idx"] = df_grouped["Country of origin"].map(country_to_index)
    df_grouped["target_idx"] = df_grouped["Country of asylum"].map(lambda x: country_to_index[x] + len(unique_origins))

    # Create a list of the Top 50 countries in "Country of asylum"
    top_50_asylums = list(df_grouped.sort_values(by="Count", ascending=False)["Country of asylum"].head(50))
    #create a list of the Top 50 countries in "Country of origin"
    top_20_origins = list(df_grouped.sort_values(by="Count", ascending=False)["Country of origin"].head(20))
    #create source and targets for sankey graph
    source = [country_to_index[country] for country in top_20_origins]
    target = [country_to_index[country] + len(unique_origins) for country in top_50_asylums]
    #create nodes and links
    nodes = list(range(len(all_countries)))
    links = []
    for i in range(len(source)):
        links.append({"source": source[i], "target": target[i], "value": df_grouped.loc[i, "Count"]})
    
    # Create Sankey graph
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_countries,
            color="blue"
        ),
        link=dict(
            source=source,
            target=target,
            value=df_grouped.loc[df_grouped["Country of origin"].isin(top_20_origins) & df_grouped["Country of asylum"].isin(top_50_asylums), "Count"].tolist()
        )
    )])

    fig.update_layout(title_text="Asylum Seekers Flow", font_size=10)
    st.plotly_chart(fig)

    # Create dashboard in Streamlit and place graph and sidebar
    st.title("Asylum Seekers Flow Dashboard")
    st.sidebar.header("Filters")