#import necessary packages
import pandas as pd
import plotly.graph_objects as go
#import streamlit package
import streamlit as st

#read file "asylum-decisions.csv"
df = pd.read_csv("asylum-decisions.csv")

#establish nodes and links for sankey graph using country of origin and country of destination in df
nodes = [{'name': i} for i in df['Country of origin'].unique()] + [{'name': i} for i in df['Country of asylum'].unique()]
links = []
for i, row in df.iterrows():
    source = nodes.index([node for node in nodes if node['name'] == row['Country of origin']][0])
    target = nodes.index([node for node in nodes if node['name'] == row['Country of asylum']][0])
    value = 1
    links.append({'source': source, 'target': target, 'value': value})\

# Create Sankey graph
#apply filters by year with interactive dropdown including an option to display data fr all years
year = st.sidebar.selectbox("Year", df['Year'].unique())
if year == "All":
    df = df
else: df = df[df['Year'] == year]
#create sankey graph with dropdown interactivity by year, with streamlit
fig = go.Figure(data=[go.Sankey(node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label= [node['name'] for node in nodes]), link=dict(source=[link['source'] for link in links], target=[link['target'] for link in links], value=[link['value'] for link in links]))])
fig.update_layout(title_text="Asylum Seekers by Country of Origin and Destination", font_size=10)
fig.show()