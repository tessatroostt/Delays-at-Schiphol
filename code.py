# import packages
import pandas as pd
import plotly as plt
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

@st.cache(allow_output_mutation=True)
def createDataFrame():
  weerdata = pd.read_excel('weather.xlsx')
  return weerdata 

def getAllDetails():
  delay = pd.read_excel('delays.xlsx')
  return delay

weerdata = createDataFrame()
delay = getAllDetails()



# delay file is exported from notebook after cleaning etc because original file is too big to put into github, cleaning steps are down below:
# delay['FLT_DATE'] = pd.to_datetime(delay['FLT_DATE'], format = '%Y%m%d') -> to datetime
# delay = delay[(delay.APT_ICAO == "EHAM")] -> only EHAM 
# delayreason = delayreason.rename(columns = {'DLY_APT_ARR_A_1':'Disruptions',
                                          #'DLY_APT_ARR_C_1':'Capacity (ATC)',
                                         #'DLY_APT_ARR_D_1': 'Weather',
                                         #'DLY_APT_ARR_E_1':'Disruptions',
                                         #'DLY_APT_ARR_G_1':'Capacity',
                                         #'DLY_APT_ARR_I_1':'Disruptions',
                                         #'DLY_APT_ARR_M_1':'Capacity',
                                         #'DLY_APT_ARR_N_1':'Disruptions',
                                         #'DLY_APT_ARR_O_1':'Disruptions',
                                         #'DLY_APT_ARR_P_1':'Events',
                                         #'DLY_APT_ARR_R_1':'Capacity',
                                         #'DLY_APT_ARR_S_1':'Staffing',
                                         #'DLY_APT_ARR_T_1':'Disruptions (ATC)',
                                         #'DLY_APT_ARR_V_1':'Capacity',
                                         #'DLY_APT_ARR_W_1':'Weather',
                                         #'DLY_APT_ARR_NA_1':'Disruptions'}) 
# delayreason = delayreason.drop(['YEAR','MONTH_NUM','MONTH_MON','APT_ICAO','APT_NAME','STATE_NAME','FLT_ARR_1','DLY_APT_ARR_1','FLT_ARR_1_DLY','FLT_ARR_1_DLY_15','ATFM_VERSION','Pivot Label'],1)
# delay['Disruptions sum'] = delay['Disruptions']+delay['Disruptions.1'] + delay['Disruptions.2'] + delay['Disruptions.3']+ delay['Disruptions.4'] + delay['Disruptions.5] -> create one column for all disruption values
# delay['Capacity sum'] = delay['Capacity'] + delay['Capacity.1'] + delay['Capacity.2'] + delay['Capacity.3'] -> create one column for all capacity values
# delay['Weather sum'] = delay['Weather'] + delay['Weather.1'] -> create one column for all weather values
# delay = delay.drop(['Disruptions','Disruptions.1','Disruptions.2','Disruptions.3','Disruptions.4','Disruptions.5','Capacity','Capacity.1','Capacity.2','Capacity.3','Weather','Weather.1'],1) -> drop previous disruption etc columns
# delay.rename(columns = {'Disruptions sum':'Disruptions','Capacity sum':'Capacity','Weather sum':'Weather'}, inplace = True) -> rename columns

#weather file is also exported from notebook after cleaning
#weerdata = weerdata.drop(['DDVEC','FHVEC','  FHX',' FHXH','  FHN',' FHNH','  FXX',' FXXH','   TN','  TNH','  TXH',' T10N','T10NH','   SQ','   SP','    Q','  RHX','   PX','  PXH','   PN','  PNH',' VVNH',' VVXH','   UX','  UXH','   UN','  UNH',' EV24','# STN','   TX', ' RHXH'],1)
#weerdata.rename(columns = {'YYYYMMDD':'Date','   FG':'Windspeed','   TG':'Temperature','   DR':'Prec. duration','   RH':'Precipation','   PG':'Pressure','  VVN':'Min. visibility','  VVX':'Max. visibility','   NG':'Clouds','   UG':'Humidity'}, inplace = True)

#set to datetime
weerdata['Date'] = pd.to_datetime(weerdata['Date'],format='%Y%m%d')

# delay reason 2018-2021
delayyears = delay[(delay['FLT_DATE'] > '2018-01-01') & (delay['FLT_DATE'] <= '2021-12-31')]
delayyears = pd.melt(delayyears, id_vars=['FLT_DATE'],var_name= 'reasons',value_name = 'disruption')

#delay reason 2018
delay2018 = delay[(delay['FLT_DATE'] > '2018-01-01') & (delay['FLT_DATE'] <= '2018-12-31')]
delay2018 = pd.melt(delay2018, id_vars=['FLT_DATE'],var_name= 'reasons',value_name = 'disruption')

#delay reason 2019
delay2019 = delay[(delay['FLT_DATE'] > '2019-01-01') & (delay['FLT_DATE'] <= '2019-12-31')]
delay2019 = pd.melt(delay2019, id_vars=['FLT_DATE'],var_name= 'reasons',value_name = 'disruption')

#delay reason 2020
delay2020 = delay[(delay['FLT_DATE'] > '2020-01-01') & (delay['FLT_DATE'] <= '2020-12-31')]
delay2020 = pd.melt(delay2020, id_vars=['FLT_DATE'],var_name= 'reasons',value_name = 'disruption')

#delay reason 2021
delay2021 = delay[(delay['FLT_DATE'] > '2021-01-01') & (delay['FLT_DATE'] <= '2021-12-31')]
delay2021 = pd.melt(delay2021, id_vars=['FLT_DATE'],var_name= 'reasons',value_name = 'disruption')

with st.sidebar:
  sidebar_keuze= st.radio('Chapters:', ['Reasons of delay at Schiphol','Weather analysis at Schiphol','Sources'])

 
  
if sidebar_keuze == 'Reasons of delay at Schiphol':
  st.markdown('***')
  st.markdown("<h3 style='text-align: center; color: black;'>Reasons of delay at Schiphol Airport Amsterdam 2018-2021</h3>", unsafe_allow_html=True)
  st.markdown('***')
  

  
  # barplots with different year

  barplot_opties = st.selectbox('Choose a year:', ['2018-2021','2018','2019','2020','2021'])
  if barplot_opties == '2018-2021':
    fig = px.histogram(delayyears, x="reasons", y = 'disruption', color = 'reasons', color_discrete_sequence=px.colors.qualitative.Pastel).update_layout(showlegend=False, title = 'Reasons of delay Schiphol Aiport Amsterdam 2018-2021 ', xaxis_title = 'Delay reasons', yaxis_title = 'Delay time????')
    st.write(fig)
  if barplot_opties == '2018':
    fig = px.histogram(delay2018, x="reasons", y = 'disruption', color = 'reasons', color_discrete_sequence=px.colors.qualitative.Pastel).update_layout(showlegend=False, title = 'Reasons of delay Schiphol Aiport Amsterdam 2018', xaxis_title = 'Delay reasons', yaxis_title = 'Delay time????')
    st.write(fig)
  if barplot_opties == '2019':
    fig = px.histogram(delay2019, x="reasons", y = 'disruption', color = 'reasons', color_discrete_sequence=px.colors.qualitative.Pastel).update_layout(showlegend=False, title = 'Reasons of delay Schiphol Aiport Amsterdam 2019', xaxis_title = 'Delay reasons', yaxis_title = 'Delay time????')
    st.write(fig)
  if barplot_opties == '2020':
    fig = px.histogram(delay2020, x="reasons", y = 'disruption', color = 'reasons', color_discrete_sequence=px.colors.qualitative.Pastel).update_layout(showlegend=False, title = 'Reasons of delay Schiphol Aiport Amsterdam 2020', xaxis_title = 'Delay reasons', yaxis_title = 'Delay time????')
    st.write(fig)
  if barplot_opties == '2021':
    fig = px.histogram(delay2021, x="reasons", y = 'disruption', color = 'reasons', color_discrete_sequence=px.colors.qualitative.Pastel).update_layout(showlegend=False, title = 'Reasons of delay Schiphol Aiport Amsterdam 2021', xaxis_title = 'Delay reasons', yaxis_title = 'Delay time????')
    st.write(fig)
    
  

  


  
if sidebar_keuze == 'Weather analysis at Schiphol':
  st.markdown('***')
  st.markdown("<h3 style='text-align: center; color: black;'>Weather analysis at Schiphol Airport Amsterdam 2018-2021</h3>", unsafe_allow_html=True)
  st.markdown('***')
  
      
  #fill in na values in delay dataset with 0 to make lineplot
  delayna = delay.fillna(0)
  
  delayyearsweather = delayna[(delayna['FLT_DATE'] > '2018-01-01') & (delay['FLT_DATE'] <= '2021-12-31')]
  
  #select 2018-2021
  weerallyears = weerdata[(weerdata['Date'] > '2018-01-01') & (weerdata['Date'] <= '2021-12-31')]
  
  #change columns from object to integer
  weerallyears["Precipation"] = weerallyears["Precipation"].astype(str).astype(int)
  weerallyears["Max. visibility"] = weerallyears["Max. visibility"].astype(str).astype(int)
  
  # divide temperature column by 10, because it is in 0.1 degrees celsius and precipation column as well (0.1 mm)
  weerallyears["Temperature"] = weerallyears["Temperature"] / 10
  weerallyears['Precipation'] = weerallyears['Precipation'] / 10
  # divide windspeed column by 10 (it's 0.1 m/s) then multiply by 3.6 so we get km/h
  weerallyears['Windspeed'] = weerallyears['Windspeed']/10 * 3.6
  # multiply visibility by 100 (1 = 100m)
  weerallyears['Max. visibility'] = weerallyears['Max. visibility'] * 100
  
  # rename delay column name so we can merge with weerallyears
  delayna.rename(columns = {'FLT_DATE':'Date'}, inplace = True)
  
  # merge weerallyears and delay
  merged = weerallyears.merge(delayna, on = 'Date')
  

  #create plot

  linechart_opties = st.selectbox('Choose variable:', ['Windspeed','Temperature','Precipation'])
  if linechart_opties == 'Windspeed':
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4.add_trace(go.Scatter(x=merged['Date'], y=merged['Weather']),secondary_y=False)
    fig4.add_trace(go.Scatter(x=merged['Date'], y=merged['Windspeed']),secondary_y=True)
    fig4.update_layout(title_text="Weather delays vs. windspeed at Schiphol Airport Amsterdam 2018-2021", width = 1500, height = 700, showlegend = False)
    fig4.update_xaxes(title_text="Date")
    fig4.update_yaxes(title_text="Delay in minutes", secondary_y=False)
    fig4.update_yaxes(title_text="Windspeed in km/h ", secondary_y=True)
    fig4.update_layout(xaxis=dict(range=["2018-01-01", "2021-12-31"],rangeselector=dict(buttons=list([dict(count=1,label="1m",step="month",stepmode="backward"),
                                                                                                      dict(count=3,label="3m",step="month",stepmode="backward"),
                                                                                                      dict(count=6,label="6m",step="month",stepmode="backward"),
                                                                                                      dict(step="all")])),rangeslider=dict(range=["2018-01-01", "2021-12-31"],visible=True),type="date"))
    st.write(fig4)
  if linechart_opties == 'Temperature':
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4.add_trace(go.Scatter(x=merged['Date'], y=merged['Weather']),secondary_y=False)
    fig4.add_trace(go.Scatter(x=merged['Date'], y=merged['Temperature']),secondary_y=True)
    fig4.update_layout(title_text="Weather delays vs. temperature at Schiphol Aiport Amsterdam 2018-2021", width = 1500, height = 700, showlegend = False)
    fig4.update_xaxes(title_text="Date")
    fig4.update_yaxes(title_text="Delay in minutes", secondary_y=False)
    fig4.update_yaxes(title_text="Temperature in degrees Celsius ", secondary_y=True)
    fig4.update_layout(xaxis=dict(range=["2018-01-01", "2021-12-31"],rangeselector=dict(buttons=list([dict(count=1,label="1m",step="month",stepmode="backward"),
                                                                                                      dict(count=3,label="3m",step="month",stepmode="backward"),
                                                                                                      dict(count=6,label="6m",step="month",stepmode="backward"),
                                                                                                      dict(step="all")])),rangeslider=dict(range=["2018-01-01", "2021-12-31"],visible=True),type="date"))
    st.write(fig4)
  if linechart_opties == 'Precipation':
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4.add_trace(go.Scatter(x=merged['Date'], y=merged['Weather']),secondary_y=False)
    fig4.add_trace(go.Scatter(x=merged['Date'], y=merged['Precipation']),secondary_y=True)
    fig4.update_layout(title_text="Weather delays vs. precipation at Schiphol Airport Amsterdam 2018-2021", width = 1500, height = 700, showlegend = False)
    fig4.update_xaxes(title_text="Date")
    fig4.update_yaxes(title_text="Delay in minutes", secondary_y=False)
    fig4.update_yaxes(title_text="Precipation in mm ", secondary_y=True)
    fig4.update_layout(xaxis=dict(range=["2018-01-01", "2021-12-31"],rangeselector=dict(buttons=list([dict(count=1,label="1m",step="month",stepmode="backward"),
                                                                                                      dict(count=3,label="3m",step="month",stepmode="backward"),
                                                                                                      dict(count=6,label="6m",step="month",stepmode="backward"),
                                                                                                      dict(step="all")])),rangeslider=dict(range=["2018-01-01", "2021-12-31"],visible=True),type="date"))
    st.write(fig4)
  
   

  st.markdown("""
  - The blue line represents the delay in minutes 
  - The red line represents the chosen variable
  """)

  
  
  
if sidebar_keuze == 'Sources':
  st.markdown('***')
  st.markdown("<h3 style='text-align: center; color: black;'>Sources</h3>", unsafe_allow_html=True)
  st.markdown('***')
  
  st.markdown("""
  The following sources were used:
  - https://ansperformance.eu/data/ (En-route IFR flights and ATFM delays)
  - https://www.knmi.nl/nederland-nu/klimatologie/daggegevens
  """)
