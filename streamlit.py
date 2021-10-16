import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json, ast
from matplotlib.ticker import MaxNLocator
import plotly.figure_factory as ff
import geopandas as gpd
from colour import Color
import plotly.express as px 
import datetime as dt
import plotly.graph_objects as go
import calendar



@st.cache 
def load_data():

    # Reading engagement data
    engagements = pd.read_csv("cleaned/cleaned_engagement_data.csv")
    
    # Reading State wise School Policy data 
    school_policy = pd.read_csv("cleaned/cleaned_school_policy_data.csv")
    
    # Reading Google Mobility data
    mobility = pd.read_csv("cleaned/cleaned_mobility_data.csv")
    
    # Reading State wise Mobility Policy data 
    mobility_policy = pd.read_csv("cleaned/cleaned_mobility_policy_data.csv")
    
    # Reading Apple Mobility traffic information based on years
    apple_mobility2020 = pd.read_csv('cleaned/cleaned_apple_mobility2020.csv').set_index('state')
    apple_mobility2021 = pd.read_csv('cleaned/cleaned_apple_mobility2021.csv').set_index('state')
    return engagements, school_policy, mobility, mobility_policy, apple_mobility2020, apple_mobility2021




engagements, school_policy, mobility, mobility_policy, apple_mobility2020, apple_mobility2021 = load_data()

st.header("Covid-19's Impact on Education")
st.subheader("The time when states have closed public schools")
slider = st.slider('Select date (between March and April 2020) to see the states that have schools closed', min_value = dt.date(year=2020,month=3,day=10), max_value = dt.date(year=2020,month=4,day=4), format='MM-DD-YYYY')

school_policy = school_policy.dropna(subset=["date"])[['State Abbreviation','date']]
school_policy['Closed'] = (pd.to_datetime(school_policy['date'], format='%d/%m/%y') < pd.to_datetime(slider)).astype('str')

# Plotting the closed states based on the selected date
fig = px.choropleth(school_policy,  # Input Pandas DataFrame
                    locations="State Abbreviation",  # DataFrame column with locations  # DataFrame column with color values
                    hover_name="State Abbreviation", # DataFrame column hover info
                    locationmode = 'USA-states',
                    color='Closed',
                   color_discrete_map={'True':'red',
                                        'False':'blue'}) # Set to plot as US States
fig.add_scattergeo(name='State Names',
    locations=school_policy['State Abbreviation'],
    locationmode='USA-states',
    text=school_policy['State Abbreviation'],
    mode='text')
fig.update_layout(
    title_text = 'Date when public schools were closed', # Create a Title
    geo_scope='usa',  # Plot only the USA instead of globe
    geo=dict(bgcolor= 'rgba(0,0,0,0)',lakecolor='#4E5D6C'),
    
)
st.plotly_chart(fig, use_container_width=True)



st.subheader("The engagement ratio for various tools used for education")

tools = st.multiselect("Columns", ["Zoom", "Google Classroom","Canvas","Schoology", "Google Docs", "Google Sheets", "Duolingo",  "Grammarly", "Quizlet","i-Ready"], default=["Google Classroom", "Zoom"])

columns = tools
columns.append('time')
engagements = engagements[columns]


# Plotting the engagemnet data 
fig = px.area(engagements, x = "time", y = tools)
fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
st.plotly_chart(fig, use_container_width=True)


st.header("Covid-19's impact on daily mobility")

parameterOption = st.selectbox('Which mobility parameter do you want to select',
('Retail and Recreation',
       'Grocery and Pharmacy',
       'Parks',
       'Workplaces',
       'Resedential'))

mobility = mobility.reset_index()[['date','State',parameterOption]]

all_options = st.checkbox("Select all states")

if all_options:
    mobilityGroups = mobility.groupby('date').mean().reset_index()
    fig = px.line(mobilityGroups, x="date",y=parameterOption)
    st.plotly_chart(fig, use_container_width=True)

else:
    mobilityGroups = mobility.pivot_table(index='date', columns='State', values=parameterOption).reset_index()
    selected_options = st.multiselect("Columns", ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
           'Colorado', 'Connecticut', 'Delaware', 'District of Columbia',
           'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana',
           'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
           'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
           'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
           'New Jersey', 'New Mexico', 'New York', 'North Carolina',
           'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
           'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
           'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
           'West Virginia', 'Wisconsin', 'Wyoming'], default=['Pennsylvania'])
    fig = px.line(mobilityGroups, x="date",y=selected_options)
    st.plotly_chart(fig, use_container_width=True)


st.header("Covid-19's Impact on Mobility")
st.subheader("The time when states have restricted free movement")
slider = st.slider('Select date (between March and April 2020) to see the states that have schools closed', min_value = dt.date(year=2020,month=2,day=2), max_value = dt.date(year=2020,month=6,day=6), format='MM-DD-YYYY')

mobility_policy = mobility_policy.dropna(subset=["MobilityRestrictedDate"])[['State Abbreviation','MobilityRestrictedDate']]
mobility_policy['Closed'] = (pd.to_datetime(mobility_policy['MobilityRestrictedDate'], format='%m/%d/%Y') < pd.to_datetime(slider,errors='coerce')).astype('str')

# Plotting the closed states based on the selected date
fig = px.choropleth(mobility_policy,  # Input Pandas DataFrame
                    locations="State Abbreviation",  # DataFrame column with locations  # DataFrame column with color values
                    hover_name="State Abbreviation", # DataFrame column hover info
                    locationmode = 'USA-states',
                    color='Closed',
                   color_discrete_map={'True':'red',
                                        'False':'blue'}) # Set to plot as US States
fig.add_scattergeo(name='State Names',
    locations=mobility_policy['State Abbreviation'],
    locationmode='USA-states',
    text=school_policy['State Abbreviation'],
    mode='text')
fig.update_layout(
    title_text = 'Date when mobility was restricted', # Create a Title
    geo_scope='usa',  # Plot only the USA instead of globe
    geo=dict(bgcolor= 'rgba(0,0,0,0)',lakecolor='#4E5D6C'),
    
)
st.plotly_chart(fig, use_container_width=True)


def convert(month_idx):
    return calendar.month_abbr[int(month_idx)]
def df_to_plotly(df):
    x = df.columns.tolist()
    x = list(map(convert, x))
    return {'z': df.values.tolist(),
            'x': x,
            'y': df.index.tolist()}

yearOption = st.selectbox('Which year do you want to select',('2020','2021'))

if(yearOption == '2020'):
    fig = go.Figure(
            data=go.Heatmap(df_to_plotly(apple_mobility2020), type = 'heatmap', colorscale = 'rdbu'),
            layout=go.Layout(width = 800,height = 1000, title="Heatmap showing the percentage change from 2019 in the transit traffic"))
else:
    fig = go.Figure(
            data=go.Heatmap(df_to_plotly(apple_mobility2021), type = 'heatmap', colorscale = 'rdbu'),
            layout=go.Layout(width = 800,height = 1000, title="Heatmap showing the percentage change from 2019 in the transit traffic"))

st.plotly_chart(fig, use_container_width=True)

    






