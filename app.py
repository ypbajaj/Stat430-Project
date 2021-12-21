# & C:/Users/hp/anaconda3/python.exe c:/Users/hp/Desktop/app.py
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import numpy as np
import pandas as pd
from urllib.request import urlopen
import json
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import regex as re
from datetime import datetime, timedelta, datetime, date
import datetime


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

US_Jurisdiction = pd.read_csv('C:\\Users\\hp\\Downloads\\COVID-19_Vaccinations_in_the_United_States_Jurisdiction.csv')
US_Transmission = pd.read_csv('C:\\Users\\hp\\Downloads\\United_States_COVID-19_County_Level_of_Community_Transmission_as_Originally_Posted.csv')
US_County = pd.read_csv('C:\\Users\\hp\\Downloads\\COVID-19_Vaccinations_in_the_United_States_County.csv',dtype={"FIPS": str})

app = dash.Dash(__name__)

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
    
# invert the dictionary
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))

US_County = US_County.loc[~US_County['Recip_State'].isin(["DC","AS","GU","MP","PR","UM","VI"])]
US_County = US_County.loc[US_County['Recip_County'] != 'Unknown County']
vaccination_type = ['Fully Vaccinated','Atleast 1 dose']
state = US_County['Recip_State'].map(abbrev_to_us_state)
states = state.unique()
states = np.delete(states,40)


US_County_Subset = US_County.copy()
US_County_Subset['Date'] = pd.to_datetime(US_County_Subset['Date'])
US_County_Subset = US_County_Subset.sort_values('Date')

US_Juris_subset = US_Jurisdiction.copy()
US_Juris_subset['Date'] = pd.to_datetime(US_Juris_subset['Date'])
US_Juris_subset = US_Juris_subset.sort_values('Date')

US_Juris_Date = pd.to_datetime(US_Juris_subset['Date'].unique())
mytotaldates = {i:x.strftime("%m/%d/%Y") for i,x in enumerate(US_Juris_Date)}
a = (list(mytotaldates.keys()))

US_County_Date = pd.to_datetime(US_County_Subset['Date'].unique())
mytotaldates1 = {i:x.strftime("%m/%d/%Y") for i,x in enumerate(US_County_Date)}
a1 = (list(mytotaldates1.keys()))

US_Transmission['report_date'] = pd.to_datetime(US_Transmission['report_date'])
US_Transmission['cases_per_100K_7_day_count_change'] = US_Transmission['cases_per_100K_7_day_count_change'].replace('suppressed',np.nan)
US_Transmission['cases_per_100K_7_day_count_change'] = US_Transmission['cases_per_100K_7_day_count_change'].replace('\,','',regex=True)
US_Transmission['cases_per_100K_7_day_count_change'] = US_Transmission['cases_per_100K_7_day_count_change'].astype(np.float32)
US_Transmission_Subset = US_Transmission.copy()

US_Transmission_Date = pd.to_datetime(US_Transmission['report_date'].unique())
mytotaldates2 = {i:x.strftime("%m/%d/%Y") for i,x in enumerate(US_Transmission_Date)}
a2 = (list(mytotaldates2.keys()))




app.layout = html.Div(
    [
        html.H1("US COVID-19 DATA TRACKER",style={'text-align':'center','background-color':'Ivory'}),
        html.Br(),
        dcc.RadioItems(
            id = 'vaccine',
            options=[
                {'label': x, 'value': x} for x in vaccination_type],
            value= vaccination_type[0],
            labelStyle={'display': 'inline-block'},
            style={'text-align':'center'}
        ),
        html.Br(),
        html.Br(),
        
        dcc.Graph(id='State_map'),
        dcc.Slider(
         id='map1_slider',
         min=a[0],
         max=a[-1],
         marks={i:{'label':mytotaldates.get(i)} for i in a  if i%20==0},
         value=a[-1],
        ),
        
        html.Br(),
        html.Br(),

        dcc.Dropdown(
            id='state_dropdown',
            options=[
                {'label': x, 'value': x} for x in states],
            value=states[0]
        ),
        
        html.Br(),
        html.Br(),

        dcc.RadioItems(
            id = 'vaccine_county',
            options=[
                {'label': x, 'value': x} for x in vaccination_type],
            value= vaccination_type[0],
            labelStyle={'display': 'inline-block'},
            style={'text-align':'center'}
        ),

        html.Br(),
        html.Br(),

        dcc.Graph(id='Vaccine_map'),
        dcc.Slider(
         id='map2_slider',
         min=a1[0],
         max=a1[-1],
         marks={i:{'label':mytotaldates1.get(i)} for i in a  if i%20==0},
         value=a1[-1],
        ),
        
        html.Br(),
        html.Br(),

        dcc.Dropdown(
            id='county_dropdown',
            options=[],
        ),

        html.Br(),
        html.Br(),

        
        html.Div(id='selected_sc',style={'text-align':'center','background-color':'Ivory','font-weight': 'bold'}),

        html.Br(),
        html.Br(),

        html.H1("Daily % Positivity - 7 day moving average ",style={'text-align':'center','background-color':'Ivory'}),

        html.Br(),

        html.Div(id='my-output',style={'text-align':'center','background-color':'Ivory'}),

        html.Br(),
        html.Br(),

        html.H1("Use slider to update time series chart ",style={'text-align':'center','background-color':'Ivory'}),

        dcc.RangeSlider(
        id='range_slider',
        min=a2[0],
        max=a2[-1],
        value=[a2[0],a2[-1]],
        marks = {i:{'label':mytotaldates2.get(i)} for i in a  if i%5==0}
        ),

        html.Br(),
        html.Br(),

        dcc.Graph(id="time_series_chart",style={'background-color':'Black'}),

        html.Br(),
        html.Br(),

        html.H1("Daily new cases - 7 day moving average per 100k ",style={'text-align':'center','background-color':'Ivory'}),

        html.Br(),
        html.Br(),
        
        dcc.Graph(id="time_series_chart1",style={'background-color':'Black'}),

    ],style = {'background-color':'Ivory'})



#Map1

@app.callback(
    Output("State_map", "figure"),
    Input("vaccine", "value"),
    Input("map1_slider", "value")
)
def state_chloropeth(vaccine,val):
    if vaccine == 'Fully Vaccinated':
        val = mytotaldates[val]
        US_Juris_subset = US_Jurisdiction[US_Jurisdiction['Date'] == val]
        US_Juris_subset['text'] = 'State:' + US_Juris_subset['Location'].map(abbrev_to_us_state)
        fig = go.Figure(data=go.Choropleth(locations=US_Juris_subset['Location'], # Spatial coordinates
        z = US_Juris_subset['Series_Complete_Pop_Pct'].astype(float), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'spectral',
        colorbar_title = "Fully vaccinated (%)", 
        ))
        fig.update_layout(
        title_text = 'Fully vaccinated by State (%)',
        geo_scope='usa', # limite map scope to USA
        )
        fig.update_traces(hovertext = US_Juris_subset['text'])
        return fig
    else:
        val = mytotaldates[val]
        US_Juris_subset = US_Jurisdiction[US_Jurisdiction['Date'] == val]
        US_Juris_subset['text1'] = 'State:' + US_Juris_subset['Location'].map(abbrev_to_us_state)
        fig = go.Figure(data=go.Choropleth(locations=US_Juris_subset['Location'], # Spatial coordinates
        z = US_Juris_subset['Administered_Dose1_Pop_Pct'].astype(float), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Inferno',
        colorbar_title = "Atleast 1 dose (%)",
        text = US_Juris_subset['text1'] #hover text
        ))
        fig.update_layout(
        title_text = 'Atleast 1 dose by State (%)',
        geo_scope='usa', # limite map scope to USA
        )
        return fig




#Map2
@app.callback(
    Output("Vaccine_map", "figure"),
    [Input("state_dropdown", "value"),
    Input("vaccine_county","value"),
    Input("map2_slider", "value")]
)
def display_choropleth(state_dropdown,state,val):
    val = mytotaldates1[val]
    if state == 'Fully Vaccinated':
        US_County_subset = US_County_Subset[(US_County_Subset['Date'] == val) & (US_County_Subset['Recip_State'] == us_state_to_abbrev[state_dropdown])]
        fig = go.Figure(data=go.Choropleth(locations=US_County_subset['FIPS'], # Spatial coordinates
        geojson=counties,
        z = US_County_subset['Series_Complete_Pop_Pct'].astype(float), # Data to be color-coded
        colorscale = 'spectral',
        colorbar_title = "Fully vaccinated (%)",
        ))
        fig.update_layout(
        title_text = 'Fully vaccinated (%)',
        )
        fig.update_geos(fitbounds="locations", visible=False)
        return fig
    else:
        US_County_subset = US_County_Subset[(US_County_Subset['Date'] == val) & (US_County_Subset['Recip_State'] == us_state_to_abbrev[state_dropdown])]
        fig = go.Figure(data=go.Choropleth(locations=US_County_subset['FIPS'], # Spatial coordinates
        geojson=counties,
        z = US_County_subset['Administered_Dose1_Pop_Pct'].astype(float), # Data to be color-coded
        colorscale = 'Inferno',
        colorbar_title = "Atleast 1 dose vaccinated (%)",
        ))
        fig.update_layout(
        title_text = 'Atleast 1 dose by State (%)',
        )
        fig.update_geos(fitbounds="locations", visible=False) 
        return fig


# Populate the options of counties dropdown based on states dropdown
@app.callback(
    Output("county_dropdown","options"),
    Input("state_dropdown", "value"),
)
def s_dropdowns(S_dropdown):
    US_Dropdown = US_County[US_County['Recip_State'] == us_state_to_abbrev.get(S_dropdown)]
    return [{'label': c, 'value': c} for c in sorted(US_Dropdown.Recip_County.unique())]

#populate initial values of counties dropdown
@app.callback(
    Output('county_dropdown', 'value'),
    Input('county_dropdown', 'options')
)
def set_cities_value(available_options):
    return available_options[0]['value']

#Selected State Selected County
@app.callback(
    Output(component_id='selected_sc', component_property='children'),
    Input(component_id='county_dropdown', component_property='value'),
    Input(component_id='state_dropdown', component_property='value')
)
def update_output_div_sc(county,state):
    return 'Selected County: {} , Selected State: {}'.format(county,state)

#Date Output
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='range_slider', component_property='value')
)
def update_output_div(val):
    a = datetime.datetime.strptime(mytotaldates2[val[0]],"%m/%d/%Y")
    b = datetime.datetime.strptime(mytotaldates2[val[1]],"%m/%d/%Y")
    return '{} - {}'.format(a.strftime("%A, %d %B, %Y"),b.strftime("%A, %d %B, %Y"))

#Graph1
@app.callback(
    Output("time_series_chart", "figure"), 
    [Input("county_dropdown", "value"),
    Input("state_dropdown","value"),
    Input("range_slider","value")]
    )
def display_time_series(county_dropdown,state_dropdown,val):
    state_selected = US_Transmission[(US_Transmission["state_name"] == state_dropdown)]
    state_selected =  state_selected[(state_selected["county_name"] == county_dropdown)]
    state_selected = state_selected.sort_values('report_date',ascending=True)
    state_selected = state_selected[(state_selected["report_date"] >= mytotaldates2[val[0]]) & (state_selected["report_date"] <= mytotaldates2[val[1]])]
    fig = px.line(state_selected, x='report_date', y='percent_test_results_reported_positive_last_7_days',labels={
                     "report_date": "Report Date",
                     "percent_test_results_reported_positive_last_7_days": "% Test Results Reported Positive in last 7 days",
                 })
    fig.update_layout(plot_bgcolor='rgb(0,0,0)')
    return fig

#Graph2
@app.callback(
    Output("time_series_chart1", "figure"),
    [Input("county_dropdown", "value"),
    Input("state_dropdown","value"),
    Input("range_slider","value") 
    ])
def display_time_series1(county_dropdown,state_dropdown,val):
    state_selected1 = US_Transmission[(US_Transmission["state_name"] == state_dropdown)]
    state_selected1 =  state_selected1[(state_selected1["county_name"] == county_dropdown)]
    state_selected1 = state_selected1.sort_values('report_date',ascending=True)
    state_selected1 = state_selected1[(state_selected1['report_date'] >= mytotaldates2[val[0]]) & (state_selected1['report_date'] <= mytotaldates2[val[1]])]
    fig = px.line(state_selected1, x='report_date', y='cases_per_100K_7_day_count_change',labels={
                     "report_date": "Report Date",
                     "cases_per_100K_7_day_count_change": "Cases per 100k for 7 day count change",
                 })
    fig.update_layout(plot_bgcolor='rgb(0,0,0)')
    return fig 
    
if __name__ == "__main__":
    app.run_server(debug = True,dev_tools_ui=True, dev_tools_props_check=False)