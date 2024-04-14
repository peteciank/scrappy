import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import ssl
import streamlit.components.v1 as components


st.title('S&P 500 App')

st.markdown("""
This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit, yfinance, numpy, matplotlib
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

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
    # List of pages
    pages = {
        "1️⃣ Webscrap using SSL Technique": "./pages/sp500-app_v1.py",
        "2️⃣ Webscrap using HTTP Technique": "./pages/sp500-app_v2.py",
        "3️⃣ Webscrap using Table Detection Technique": "./pages/sp500-app_v3.py",
        "4️⃣ Webscrap using Table Detection 2 Technique": "./pages/sp500-app_v4.py"
    }

    # Dropdown to select the page
    selected_page = st.selectbox("Select a page:", list(pages.keys()))

    # Button to switch page
    switch_page = st.button("Switch page")
    if switch_page:
        # Switch to the selected page
        page_file = pages[selected_page]
        st.switch_page(page_file)

    components.html(
        """
        <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
        <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="large" data-theme="dark" data-type="HORIZONTAL" data-vanity="pedrociancaglini" data-version="v1">
        <a class="badge-base__link LI-simple-link" href="https://es.linkedin.com/in/pedrociancaglini/en?trk=profile-badge"></a></div>
        """,
    height=300,
    )

st.sidebar.header('User Input Features')

# Web scraping of S&P 500 data
#
@st.cache_data

def load_data():
    with st.spinner("Reading HTTPS"):
        try:
            url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
            html = pd.read_html(url, header = 0)
            df = html[0]
        except Exception as e:
            st.warning(e)
    return df


df = []

df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['GICS Sector'].unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]

st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)

# Download S&P500 data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# https://pypi.org/project/yfinance/

data = yf.download(
        tickers = list(df_selected_sector[:10].Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

# Plot Closing Price of Query Symbol
def price_plot(symbol):
  df = pd.DataFrame(data[symbol].Close)
  df['Date'] = df.index
  fig = plt.figure()
  plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
  plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title(symbol, fontweight='bold')
  plt.xlabel('Date', fontweight='bold')
  plt.ylabel('Closing Price', fontweight='bold')
  return st.pyplot(fig)

num_company = st.sidebar.slider('Number of Companies', 1, 5)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)
