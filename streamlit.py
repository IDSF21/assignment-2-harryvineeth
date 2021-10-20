import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json, ast
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
    
    return engagements, school_policy, mobility, mobility_policy, apple_mobility2020, apple_mobility2021




engagements, school_policy, mobilityGroups, mobility_policy, apple_mobility2020, apple_mobility2021 = load_data()


buff, col, buff2 = st.columns([1,3,1])
col.title("How has COVID affected the daily lives of people?")
col.markdown("On 17th November 2019 the first case of COVID-19 was detected. It has been almost two years since then and the world continues to change and adapt to the ever-evolving pandemic. These changes can be classfied as macro and micro level changes. The former refers to changes at a global scale whereas the latter refers to changes at an individual's scale. Macro level changes include the effects on global economy, trade and commerce. Such changes have been quantified and presented in numerous studies. However, the effects of COVID at a micro level are just as apparent and important. The pandemic has led to subtle and not-so-subtle adjustments in the daily routines of people. These adjustments will cumulate over time and lead to several social and psychological repercussions. This is a study to attempt to quantify these adjustments and discuss the possible implications. The visualizations have been ordered in a descending order according to impact. Thus the impact on the lives of children has been discussed first and we then go on to discuss the changes for adults.")
col.markdown("******")
col.header("How has COVID-19 affected the lives of children?")
col.markdown("To prevent the spread of infection, public schools were shut down all across the United States. Different schools were shut at different times in accordance with state policies.")

buff, col2, buff2 = st.columns([2,3,2])
slider = col2.slider('Move the slider below to view schools in states getting shut over the course of 2020.', min_value = dt.date(year=2020,month=3,day=10), max_value = dt.date(year=2020,month=4,day=4), format='MM-DD-YYYY')
school_policy = school_policy.dropna(subset=["date"])[['State Abbreviation','date']]
school_policy['Public Schools Closed'] = (pd.to_datetime(school_policy['date'], format='%d/%m/%y') < pd.to_datetime(slider)).astype('str')

# Plotting the closed states based on the selected date
fig = px.choropleth(school_policy,  # Input Pandas DataFrame
                    locations="State Abbreviation",  # DataFrame column with locations  # DataFrame column with color values
                    hover_name="State Abbreviation", # DataFrame column hover info
                    locationmode = 'USA-states',
                    color='Public Schools Closed',
                   color_discrete_map={'True':'red',
                                        'False':'blue'}) # Set to plot as US States
fig.add_scattergeo(name='State Names',
    locations=school_policy['State Abbreviation'],
    locationmode='USA-states',
    text=school_policy['State Abbreviation'],
    mode='text')
fig.update_layout( # Create a Title
    geo_scope='usa',  # Plot only the USA instead of globe
    geo=dict(bgcolor= 'rgba(0,0,0,0)',lakecolor='#4E5D6C'),
    
)
buff, col, buff2 = st.columns([1,3,1])
col.plotly_chart(fig, use_container_width=True)

col.markdown("******")

buff, col, buff2 = st.columns([1,3,1])
col.header("How have schools adapted to these changes?")
tools = col.multiselect("Educational Tools", ["Zoom", "Google Classroom","Canvas","Schoology", "Google Docs", "Google Sheets", "Duolingo",  "Grammarly", "Quizlet","i-Ready"], default=["Duolingo", "Zoom"])

columns = tools
columns.append('time')
engagements_df = engagements[columns]
# Plotting the engagemnet data 
fig = px.line(engagements_df, x = "time", y = tools, markers=True)
fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.layout.plot_bgcolor = '#0E1117'
fig.layout.paper_bgcolor = '#0E1117'
fig.update_layout(legend_title_text='Educational tools', title='Usage of various Education tools during 2020',
                   xaxis_title='Month',
                   yaxis_title='Usage')
col.plotly_chart(fig, use_container_width=True)
col.markdown("Interestingly, one can clearly see the sharp or gradual rise in the usage of these tools around March and April. Another interesting observation is that Duolingo is the only tool that shows a sharp decline since March. This can be explained by the imposition of travel restrictions around that time.")
buff, col, buff2 = st.columns([1,3,1])
col.markdown("The long term impact of these changes is currently unknown and can merely be guessed. Both physical and mental development of children is bound to be affected. Increased screen time has become unavoidable and children are missing out on peer interactions that are vital for soft skills development. Another case to consider would be of infants who have spent the first 2 years of their lives completely indoors. ")
col.markdown("******")
col.header("What about adults?")
col.markdown("The government issued stay-at-home regulations to curb the growing number of cases. Different states issued orders at different times in as a reactionary response to the number of active cases.")
buff, col2, buff2 = st.columns([2,3,2])
slider = col2.slider('Move the slider below to view states issuing stay-at-home orders over the course of 2020.', min_value = dt.date(year=2020,month=2,day=28), max_value = dt.date(year=2020,month=3,day=22), format='MM-DD-YYYY')

mobility_policy = mobility_policy.dropna(subset=["MobilityRestrictedDate"])[['State Abbreviation','MobilityRestrictedDate']]
mobility_policy['Stay at Home Policy declared'] = (pd.to_datetime(mobility_policy['MobilityRestrictedDate'], format='%m/%d/%Y') < pd.to_datetime(slider,errors='coerce')).astype('str')

# Plotting the closed states based on the selected date
fig = px.choropleth(mobility_policy,  # Input Pandas DataFrame
                    locations="State Abbreviation",  # DataFrame column with locations  # DataFrame column with color values
                    hover_name="State Abbreviation", # DataFrame column hover info
                    locationmode = 'USA-states',
                    color='Stay at Home Policy declared',
                   color_discrete_map={'True':'red',
                                        'False':'blue'}) # Set to plot as US States
fig.add_scattergeo(name='State Names',
    locations=mobility_policy['State Abbreviation'],
    locationmode='USA-states',
    text=school_policy['State Abbreviation'],
    mode='text')
fig.update_layout(# Create a Title
    geo_scope='usa',  # Plot only the USA instead of globe
    geo=dict(bgcolor= 'rgba(0,0,0,0)',lakecolor='#4E5D6C'),
    
)
buff, col, buff2 = st.columns([1,3,1])
col.plotly_chart(fig, use_container_width=True)
col.markdown("The daily activities of adults have changed quite a bit due to restrictions on movements in public areas. These changes can be tracked by measuring the percent change in frequency of commonly visited places. Workplaces were the first to shut and we see a large negative change from our baseline (pre-pandemic times). Parks were frequented more often and there was a sharp decline in mall visits.")
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
fig.update_layout(legend_title_text='Commonly Visited Places', title='Percentage Change in Frequency of commonly visited places compared to baseline (2019)')
# fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
# fig = px.line(mobilityGroups, x='date' , y='value',color='variable')
fig.layout.plot_bgcolor = '#0E1117'
fig.layout.paper_bgcolor = '#0E1117'
st.plotly_chart(fig, use_container_width=True)
buff, col, buff2 = st.columns([1,3,1])
col.markdown("******")



###### Plotting Heatmap ######
def convert(month_idx):
    return calendar.month_abbr[int(month_idx)]
def df_to_plotly(df):
    x = df.columns.tolist()
    x = list(map(convert, x))
    return {'z': df.values.tolist(),
            'x': x,
            'y': df.index.tolist()}


col.header("So, has traffic reduced?")
col.markdown("To look at the positive side of things, in response to schools shutting and stay-at-home orders being issued, transit traffic reduced significantly in 2020. This year as few workplaces opened up and restrictions have been eased, traffic levels have increased again. This can be seen in the heatmap below.")

buff, col, buff2 = st.columns([6,1,6])
yearOption = col.selectbox('Year',('2020','2021'))

if(yearOption == '2020'):
    fig = go.Figure(
            data=go.Heatmap(df_to_plotly(apple_mobility2020), type = 'heatmap', colorscale = 'rdbu'),
            layout=go.Layout(width = 600,height = 1000, title="Percentage change in transit traffic compared to baseline (2019)"))
else:
    fig = go.Figure(
            data=go.Heatmap(df_to_plotly(apple_mobility2021), type = 'heatmap', colorscale = 'rdbu'),
            layout=go.Layout(width = 600,height = 1000, title="Percentage change in transit traffic compared to baseline (2019)"))

buff, col, buff2 = st.columns([1,3,1])
col.plotly_chart(fig, use_container_width=True)
col.markdown("******")

col.header("Conclusion")
col.markdown("As we can see there is a clear decrease in traffic over the course of 2020. The number of COVID cases are also decreasing gradually after their initial increase. We can see this in the visualization below. Hopefully, the alterations in people's lifestyles and routines do not lead to long term negative changes. As we adapt to a new normal, we should aim to reach a new equilibrium which leads to routines that prioritize physical and mental well being of children and adults alike.")
### Plotting covid data ####
data_path="mapbox_token/"
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
df2020=pd.read_csv("cleaned/cleaned_covid_data.csv",index_col=False,dtype={"fips": str,"county": str})
plot_df=df2020
plot_var="diffs"
#days = np.sort(plot_df.date.unique())
months = ["Jan 2020","Feb 2020","Mar 2020","Apr 2020","May 2020","Jun 2020","Jul 2020","Aug 2020","Sep 2020","Oct 2020","Nov 2020","Dec 2020", "Jan 2021","Feb 2021","Mar 2021","Apr 2021","May 2021","Jun 2021","Jul 2021","Aug 2021","Sep 2021","Oct 2021"]

def numpy_dt64_to_str(dt64):
    day_timestamp_dt = (dt64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    day_dt = dt.datetime.utcfromtimestamp(day_timestamp_dt)
    return day_dt.strftime("%b %d")

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
fig=go.Figure(data=fig_data, layout=fig_layout, frames=fig_frames)

# fig=go.Figure(data=fig_data, layout=fig_layout, frames=fig_frames)
st.plotly_chart(fig, use_container_width=True)
    






