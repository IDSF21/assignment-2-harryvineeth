from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
import plotly, plotly.graph_objects as go
import datetime as dt

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",dtype={"fips": str})
df = df.dropna(subset=['fips','cases'])
df["year"]=pd.to_datetime(df["date"]).dt.year
df["day"]=pd.to_datetime(df["date"]).dt.day
df["month"]=pd.to_datetime(df["date"]).dt.strftime("%b")
df2020=df[df["year"]==2020]
df2021=df[df["year"]==2021]

plot_df=df2020
plot_var="cases"
data_path="Byte1/assignment-2-harryvineeth/mapbox_token/"
#days = np.sort(plot_df.date.unique())
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

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

sliders_dict = dict(active=len(days) - 1,
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
fig.show()