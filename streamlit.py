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
import json
from urllib.request import urlopen
from plotly.subplots import make_subplots
#import plotly, plotly.graph_objects as go

st.set_page_config(layout="wide")

@st.cache 
def load_data():

    # Reading engagement data
    engagements = pd.read_csv("cleaned/cleaned_engagement_data.csv")
    
    # Reading State wise School Policy data 
    school_policy = pd.read_csv("cleaned/cleaned_school_policy_data.csv")
    
    # Reading Google Mobility data
    mobility = pd.read_csv("cleaned/cleaned_formatted_mobility.csv")
    
    # Reading State wise Mobility Policy data 
    mobility_policy = pd.read_csv("cleaned/cleaned_mobility_policy_data.csv")
    
    # Reading Apple Mobility traffic information based on years
    apple_mobility2020 = pd.read_csv('cleaned/cleaned_apple_mobility2020.csv').set_index('state')
    apple_mobility2021 = pd.read_csv('cleaned/cleaned_apple_mobility2021.csv').set_index('state')
    
    
    #df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",dtype={"fips": str})

    data_path="mapbox_token/"
    #days = np.sort(plot_df.date.unique())
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    
    df2020=pd.read_csv('cleaned/cleaned_county_covid_2020.csv')
    plot_df=df2020
    plot_var="cases"
    def numpy_dt64_to_str(dt64):
        day_timestamp_dt = (dt64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
        day_dt = dt.datetime.utcfromtimestamp(day_timestamp_dt)
        return day_dt.strftime("%b %d")

    
    return engagements, school_policy, mobility, mobility_policy, apple_mobility2020, apple_mobility2021




engagements, school_policy, mobilityGroups, mobility_policy, apple_mobility2020, apple_mobility2021 = load_data()

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

tools = st.multiselect("Columns", ["Zoom", "Google Classroom","Canvas","Schoology", "Google Docs", "Google Sheets", "Duolingo",  "Grammarly", "Quizlet","i-Ready"], default=["Duolingo", "Zoom"])

columns = tools
columns.append('time')
engagements_df = engagements[columns]


# Plotting the engagemnet data 
fig = px.line(engagements_df, x = "time", y = tools)
fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
fig.layout.plot_bgcolor = '#0E1117'
fig.layout.paper_bgcolor = '#0E1117'
st.plotly_chart(fig, use_container_width=True)


st.header("Covid-19's impact on daily mobility")


fig = make_subplots(rows=2, cols=2, start_cell="top-left", shared_yaxes=True)

fig.add_trace(go.Scatter(x=mobilityGroups["date"].values,y=mobilityGroups["Workplaces"].values.tolist(), fill='tozeroy', name='Workplaces'),row=1, col=1)
fig.add_trace(go.Scatter( x=mobilityGroups["date"].values,y=mobilityGroups['Parks'].values.tolist(),fill='tozeroy', name='Parks'),row=1, col=2)
fig.add_trace(go.Scatter( x=mobilityGroups["date"].values,y=mobilityGroups['Grocery and Pharmacy'].values.tolist(),fill='tozeroy', name='Grocery and Pharmacy'),row=2, col=1)
fig.add_trace(go.Scatter( x=mobilityGroups["date"].values,y=mobilityGroups['Retail and Recreation'].values.tolist(), fill='tozeroy', name='Retail and Recreation'),row=2, col=2)

fig.update_xaxes(title_text="Workplaces", row = 1, col = 1,showticklabels=True)
fig.update_xaxes(title_text="Parks", row = 1, col = 2,showticklabels=True)
fig.update_xaxes(title_text="Grocery and Pharmacy", row = 2, col = 1,showticklabels=True)
fig.update_xaxes(title_text="Retail and Recreation", row = 2, col = 2,showticklabels=True)

# Update yaxis properties
fig.update_yaxes(title_text="Percentage change", row=1, col=1,showticklabels=True)
fig.update_yaxes( row=1, col=2,showticklabels=True)
fig.update_yaxes(title_text="Percentage change", row=2, col=1,showticklabels=True)
fig.update_yaxes( row=2, col=2,showticklabels=True)

fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
fig.update_layout(width=int(1500), height = int(750))
# fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
# fig = px.line(mobilityGroups, x='date' , y='value',color='variable')
fig.layout.plot_bgcolor = '#0E1117'
fig.layout.paper_bgcolor = '#0E1117'
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



###### Plotting Heatmap ######
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
            layout=go.Layout(width = 600,height = 1000, title="Heatmap showing the percentage change from 2019 in the transit traffic"))
else:
    fig = go.Figure(
            data=go.Heatmap(df_to_plotly(apple_mobility2021), type = 'heatmap', colorscale = 'rdbu'),
            layout=go.Layout(width = 600,height = 1000, title="Heatmap showing the percentage change from 2019 in the transit traffic"))

st.plotly_chart(fig, use_container_width=True)


### Plotting covid data ####
data_path="mapbox_token/"
#days = np.sort(plot_df.date.unique())
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

df2020=pd.read_csv('cleaned/cleaned_county_covid_2020.csv')
plot_df=df2020
plot_var="cases"
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
fig_data =go.Choroplethmapbox(geojson=counties, locations=plot_df.fips, 
                              z=np.log10(plot_df[plot_var]),
                              zmin=0,
                              zmax=np.log10(plot_df[plot_var].max()),
                              customdata=plot_df[plot_var],
                              name="",
                              text=plot_df.county.astype(str),
                              hovertemplate="%{text}<br>Cases: %{customdata}",
                              colorbar=dict(outlinewidth=1,
                                            outlinecolor="#333333",
                                            len=0.9,
                                            lenmode="fraction",
                                            xpad=30,
                                            xanchor="right",
                                            bgcolor=None,
                                            title=dict(text="Cases",
                                                       font=dict(size=14)),
                                            tickvals=[0,1,2,3,4,5,6],
                                            ticktext=["1", "10", "100", "1K", "10K", "100K", "1M"],
                                            tickcolor="#333333",
                                            tickwidth=2,
                                            tickfont=dict(color="#333333",
                                                          size=12)),
                              colorscale="ylorrd", #ylgn
                              #reversescale=True,
                              marker_opacity=0.7,
                              marker_line_width=0)

token = open(data_path + ".mapbox_token").read()
fig_layout = go.Layout(mapbox_style="light",
                       mapbox_zoom=3,
                       mapbox_accesstoken=token,
                       mapbox_center={"lat": 37.0902, "lon": -95.7129},
                       margin={"r":0,"t":0,"l":0,"b":0},
                       plot_bgcolor=None)

fig_layout["updatemenus"] = [dict(type="buttons",
                                  buttons=[dict(label="Play",
                                                method="animate",
                                                args=[None,
                                                      dict(frame=dict(duration=1000,
                                                                      redraw=True),
                                                           fromcurrent=True)]),
                                           dict(label="Pause",
                                                method="animate",
                                                args=[[None],
                                                      dict(frame=dict(duration=0,
                                                                      redraw=True),
                                                           mode="immediate")])],
                                  direction="left",
                                  pad={"r": 10, "t": 35},
                                  showactive=False,
                                  x=0.1,
                                  xanchor="right",
                                  y=0,
                                  yanchor="top")]

sliders_dict = dict(active=len(months) - 1,
                    visible=True,
                    yanchor="top",
                    xanchor="left",
                    currentvalue=dict(font=dict(size=20),
                                      prefix="Month: ",
                                      visible=True,
                                      xanchor="right"),
                    pad=dict(b=10,
                             t=10),
                    len=0.875,
                    x=0.125,
                    y=0,
                    steps=[])

fig_frames = []
for month in months:
    plot_df = df2020[df2020.month == month]
    frame = go.Frame(data=[go.Choroplethmapbox(locations=plot_df.fips,
                                               z=np.log10(plot_df[plot_var]),
                                               customdata=plot_df[plot_var],
                                               name="",
                                               text=plot_df.county.astype(str),
                                               hovertemplate="%{text}<br>%{customdata}")],
                     name=month)
    fig_frames.append(frame)

    slider_step = dict(args=[[month],
                             dict(mode="immediate",
                                  frame=dict(duration=300,
                                             redraw=True))],
                       method="animate",
                       label=month)
    sliders_dict["steps"].append(slider_step)

fig_layout.update(sliders=[sliders_dict])

# Plot the figure 
countychloro=go.Figure(data=fig_data, layout=fig_layout, frames=fig_frames)
st.plotly_chart(countychloro, use_container_width=True)


    






