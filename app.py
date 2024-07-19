# Import necessary packages
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Read file "solutions-edit.csv"
df = pd.read_excel("edit2.xlsx")
print(df.columns)

#create column "Count", and initialize empty
df['Count'] = ''


# Apply filters by year with interactive dropdown including an option to display data for all years
year_options = list(df['Year'].unique())
year_options.append("All")
year = st.sidebar.selectbox("Year", year_options)

if year != "All":
    df = df[df['Year'] == year]

# Establish nodes and links for Sankey graph using country of origin and country of asylum in df

nodes = []
links = []
for i, row in df.iterrows():
    source = row['Origin']
    target = row['Destination']
    value = row['Count']

    
    if source not in nodes:
        nodes.append({'name': source})
    if target not in nodes:
        nodes.append({'name': target})

    
    links.append({'source': nodes.index([node for node in nodes if node['name'] == source][0]),
                   'target': nodes.index([node for node in nodes if node['name'] == target][0]),
                   'value': value})

# Create Sankey graph with dropdown interactivity by year, with Streamlit
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=[node['name'] for node in nodes]
    ),
    link=dict(
        source=[link['source'] for link in links],
        target=[link['target'] for link in links],
        value=[link['value'] for link in links]
    )
)])
fig.update_layout(title_text="Asylum Seekers by Country of Origin and Destination", font_size=10)

# Display the Sankey diagram using Streamlit
st.plotly_chart(fig)
