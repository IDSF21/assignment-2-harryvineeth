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
import plotly.figure_factory as ff



@st.cache 
def load_data():

    # Reading engagement data
    engagements = pd.read_csv("/Users/Vineeth/Downloads/Pandas_output2.csv")
    districts = pd.read_csv("/Users/Vineeth/Downloads/districts_info.csv")
    products = pd.read_csv("/Users/Vineeth/Downloads/products_info.csv")
    engagements.dropna(subset=['lp_id'], inplace=True)
    engagements['lp_id'] = engagements['lp_id'].astype('int')
    engagements['district_id'] = engagements['filename'].str.split(".").str[0].astype('int')
    engagements = pd.merge(pd.merge(engagements, districts, on="district_id"), products, left_on="lp_id", right_on='LP ID')
    engagements = engagements[['time', 'pct_access','engagement_index','state',
             'locale','URL','Product Name','Provider/Company Name',
             'Primary Essential Function']]
    engagements['time'] = pd.to_datetime(engagements['time'])
    engagements = engagements.pivot_table(index='time',columns='Product Name',values='engagement_index', aggfunc=np.mean)
    
    # Reading State wise Policy data 
    plot_data = pd.read_csv("/Users/Vineeth/Downloads/COVID-19-US-State-Policy-Database-master/data.csv", encoding='latin-1')
    plot_data = plot_data[plot_data['date']!='0']
    
    # Reading Google Mobility data
    mobility = pd.read_csv("/Users/Vineeth/Downloads/mobility_cleaned.csv")
    mobility.rename(columns={"retail_and_recreation_percent_change_from_baseline": "Retail and Recreation", 
                         "grocery_and_pharmacy_percent_change_from_baseline": "Grocery and Pharmacy",
                        "parks_percent_change_from_baseline": "Parks", 
                         "workplaces_percent_change_from_baseline": "Workplaces",
                        "residential_percent_change_from_baseline": "Resedential",
                            "sub_region_1": "State"}, inplace=True)
    return engagements, plot_data, mobility



engagements, plot_data, mobility = load_data()

st.header("Covid-19's Impact on Education")
st.subheader("The time when states have closed public schools")
slider = st.slider('Select date (between March and April 2020) to see the states that have schools closed', min_value = dt.date(year=2020,month=3,day=10), max_value = dt.date(year=2020,month=4,day=4), format='MM-DD-YYYY')

plot_data = plot_data.dropna(subset=["date"])[['State Abbreviation','date']]
plot_data['Closed'] = (pd.to_datetime(plot_data['date'], format='%d/%m/%y') < pd.to_datetime(slider)).astype('str')

# Plotting the closed states based on the selected date
fig = px.choropleth(plot_data,  # Input Pandas DataFrame
                    locations="State Abbreviation",  # DataFrame column with locations  # DataFrame column with color values
                    hover_name="State Abbreviation", # DataFrame column hover info
                    locationmode = 'USA-states',
                    color='Closed',
                   color_discrete_map={'True':'red',
                                        'False':'blue'}) # Set to plot as US States
fig.add_scattergeo(name='State Names',
    locations=plot_data['State Abbreviation'],
    locationmode='USA-states',
    text=plot_data['State Abbreviation'],
    mode='text')
fig.update_layout(
    title_text = 'Date when public schools were closed', # Create a Title
    geo_scope='usa',  # Plot only the USA instead of globe
    geo=dict(bgcolor= 'rgba(0,0,0,0)',lakecolor='#4E5D6C'),
    
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("The engagement ration for various tools used for education")

tools = st.multiselect("Columns", ["Zoom", "Google Classroom","Canvas","Schoology", "Google Docs", "Google Sheets", "Duolingo",  "Grammarly", "Quizlet","i-Ready"], default=["Google Classroom", "Zoom"])
engagements = engagements[tools].reset_index()

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







