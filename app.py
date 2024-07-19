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
                   'value': 1})

# Create Sankey graph with dropdown interactivity by year, with Streamlit
# lines should be color coded by Destination country and the canvas area should be wider in order to see the whole graph
# colors should not be similar to each other. please use pastel color
import plotly.graph_objects as go

# Assuming nodes and links are defined elsewhere in the code
# nodes = [{'name': 'A'}, {'name': 'B'}, ...]
# links = [{'source': 0, 'target': 1, 'value': 10}, ...]

# Define a list of colors for the nodes and links
node_colors = ["#A6CEE3", "#1F78B4", "#B2DF8A", "#33A02C", "#FB9A99", "#E31A1C", "#FDBF6F", "#FF7F00", "#CAB2D6", "#6A3D9A"]
link_colors = ["#A6CEE3", "#1F78B4", "#B2DF8A", "#33A02C", "#FB9A99", "#E31A1C", "#FDBF6F", "#FF7F00", "#CAB2D6", "#6A3D9A"]

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=[node['name'] for node in nodes],
        color=node_colors[:len(nodes)]
    ),
    link=dict(
        source=[link['source'] for link in links],
        target=[link['target'] for link in links],
        value=[link['value'] for link in links],  # This should reflect the number of cases
        color=[link_colors[i % len(link_colors)] for i in range(len(links))]
    )
)])

# Add dropdown menu
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=[{"visible": [True, True]}],
                    label="All",
                    method="update"
                ),
                dict(
                    args=[{"visible": [True, False]}],
                    label="Nodes Only",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, True]}],
                    label="Links Only",
                    method="update"
                )
            ]),
            direction="down",
            showactive=True,
        )
    ]
)

fig.show()


fig.update_layout(title_text="Refugee Flow by Country of Origin and Destination", font_size=10)
# Display the Sankey diagram using Streamlit
st.plotly_chart(fig)
