import streamlit as st
import pandas as pd
import requests

url = 'https://api-dolar-argentina.herokuapp.com/api/evolucion/dolaroficial'
r = requests.get(url)
json = r.json()
df = pd.DataFrame(json['meses'])

st.title('Cotitacion del Dolar historico')

st.markdown("""
This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit, yfinance, numpy, matplotlib
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

st.sidebar.header('User Input Features')

# Web scraping of S&P 500 data
#
@st.cache

sector = df.groupby('anio')

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['anio'].unique() )
selected_sector = st.sidebar.multiselect('mes', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[ (df['anio'].isin(selected_sector)) ]

st.header('Cotizacion del dolar por año')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)
