import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import numpy as np
import pandas_datareader.data as web
import streamlit.components.v1 as components
from pages.menu import menu

st.title('S&P 500 App')

st.markdown("""
This app retrieves the list of the **S&P 500** (from a pre-existing dataset) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit, pandas_datareader, numpy, matplotlib
""")


menu()

st.sidebar.header('User Input Features')

# Load S&P 500 data from pre-existing CSV file
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv'
    df = pd.read_csv(url)
    return df

with st.sidebar:
    # Setting Fixed Width
    st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
    )



df = load_data()

#st.table(df)

# Sidebar - Sector selection
sectors = df['GICS Sector'].unique()
selected_sector = st.sidebar.multiselect('GICS Sector', sectors, sectors)

# Filtering data
df_selected_sector = df[df['GICS Sector'].isin(selected_sector)]

st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)

# Download S&P500 data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# Fetch stock data
def fetch_stock_data(symbols):
    data = {}
    for symbol in symbols:
        try:
            df = web.DataReader(symbol, data_source='yahoo', start='2024-01-01', end='2024-04-13')
            data[symbol] = df
        except:
            st.write(f"No data found for {symbol}")
    return data

num_company = st.sidebar.slider('Number of Companies', 1, 5)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    selected_symbols = list(df_selected_sector["Symbol"].iloc[:num_company])
    if selected_symbols:
        data = fetch_stock_data(selected_symbols)
        for symbol, df in data.items():
            fig = plt.figure()
            plt.fill_between(df.index, df['Close'], color='skyblue', alpha=0.3)
            plt.plot(df.index, df['Close'], color='skyblue', alpha=0.8)
            plt.xticks(rotation=90)
            plt.title(symbol, fontweight='bold')
            plt.xlabel('Date', fontweight='bold')
            plt.ylabel('Closing Price', fontweight='bold')
            st.pyplot(fig)
    else:
        st.write("Please select at least one company from the sidebar.")
