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
    df_grouped["target_idx"] = df_grouped["Country of asylum"].map(country_to_index)

    # Create a list of the Top 50 countries in "Country of asylum"
    top_50_asylums = list(df_grouped.sort_values(by="Count", ascending=False)["Country of asylum"].head(50))
    # Create a list of the Top 20 countries in "Country of origin"
    top_20_origins = list(df_grouped.sort_values(by="Count", ascending=False)["Country of origin"].head(20))

    # Filter the grouped DataFrame for the top origins and asylums
    df_top_grouped = df_grouped[
        df_grouped["Country of origin"].isin(top_20_origins) & 
        df_grouped["Country of asylum"].isin(top_50_asylums)
    ]

    # Create source and target lists for the Sankey graph
    source = df_top_grouped["source_idx"].tolist()
    target = df_top_grouped["target_idx"].tolist()
    value = df_top_grouped["Count"].tolist()

    # Create a list of unique countries in top_50_asylums
    unique_countries_asylum = list(set(top_50_asylums))
    length_unique_countries_asylum = len(unique_countries_asylum)

    # Create a list of 50 beautiful colors as valid values
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5", "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5", "#393b79", "#637939", "#8c6d31", "#843c39", "#5254a3", "#843c39", "#5254a3", "#393b79", "#637939", "#8c6d31", "#843c39", "#5254a3", "#393b79", "#637939", "#8c6d31", "#843c39", "#5254a3", "#393b79", "#637939", "#8c6d31", "#843c39", "#5254a3", "#393b79", "#637939", "#8c6d31", "#843c39", "#5254a3"]
    # Make dictionary with 50 unique countries in top_50_asylums as keys and 50 beautiful colors as values
    color_dict = {unique_countries_asylum[i]: colors[i] for i in range(length_unique_countries_asylum)}

    # Create Sankey graph
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_countries,
            color=["blue"] * len(all_countries)  # Assuming a uniform color for simplicity
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=[color_dict[df_grouped.loc[i, "Country of asylum"]] for i in df_top_grouped.index]
        )
    )])

    fig.update_layout(title_text="Asylum Seekers Flow", font_size=10)
    st.plotly_chart(fig)
