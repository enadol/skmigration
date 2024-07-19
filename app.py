#import necessary packages
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#import streamlit package
import streamlit as st

#read file "asylum-decisions.csv"
df = pd.read_csv("asylum-decisions.csv")
#check for missing values
missing_values = df.isnull().sum()
#print df columns
print(df.columns)
#establish nodes and links for sankey graph using country of origin and country of destination in df
nodes = [{'name': i} for i in df['Country of origin'].unique()] + [{'name': i} for i in df['Country of asylum'].unique()]
links = []
for i, row in df.iterrows():
    source = nodes.index([node for node in nodes if node['name'] == row['Country of origin']][0])
    target = nodes.index([node for node in nodes if node['name'] == row['Country of asylum']][0])
    value = 1
    links.append({'source': source, 'target': target, 'value': value})\

# Create Sankey graph
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

fig.update_layout(title_text="Asylum Seekers Origin and Destination", font_size=10)
fig.show()

#deploy graph in streamlit
st.plotly_chart(fig)
#display dataframe
st.dataframe(df)
#display missing values
st.write("Missing values:", missing_values)
#display dataframe shape
st.write("Dataframe shape:", df.shape)
#display dataframe info
st.write("Dataframe info:", df.info())
#display dataframe columns
st.write("Dataframe columns:", df.columns)
#display dataframe head
st.write("Dataframe head:", df.head())
#display dataframe tail
st.write("Dataframe tail:", df.tail())
#display dataframe describe
st.write("Dataframe describe:", df.describe())
#display dataframe value counts
st.write("Dataframe value counts:", df['Country of origin'].value_counts())
#display dataframe value counts
st.write("Dataframe value counts:", df['Country of asylum'].value_counts())
#display sankey graph on a web page
st.markdown(fig.to_html(include_plotlyjs='cdn'))