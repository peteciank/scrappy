import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import streamlit.components.v1 as components
from pages.menu import menu


st.set_page_config("S&P 500 Webscrap - v1", "💹", layout="wide")

st.title('S&P 500 - List of Companies')

st.markdown("""
            This app retrieves the list of the **S&P 500** from Wikipedia, using Webscraping.
            * **Python libraries:** base64, pandas, streamlit, pandas_datareader, numpy, matplotlib, beautifulSoup. 
            Stock pricing retrived using Alpha Vantage API. 
            """)


menu()

ALPHA_VANTAGE_API_KEY = st.secrets("ALPHA_KEY")

def fetch_sp500_list():
    # Your existing fetch_sp500_list function
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})
    
    companies = []
    rows = table.find_all('tr')[1:]  # Skip the header row
    for row in rows:
        cols = row.find_all('td')
        company = {
            'Symbol': cols[0].text.strip(),
            'Name': cols[1].text.strip(),
            'Sector': cols[3].text.strip()
        }
        companies.append(company)
    
    return companies

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

def get_stock_data(ticker, output_size="compact"):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize={output_size}"
    response = requests.get(url)
    data = response.json()
    if "Monthly Time Series" in data:
        df = pd.DataFrame(data["Monthly Time Series"]).T
        df.index = pd.to_datetime(df.index)
        df.columns = ["open", "high", "low", "close", "volume"]
        df = df.astype(float)
        return df
    else:
        st.write("Error fetching data.")
        return None

def main():

    companies = fetch_sp500_list()
    company_names = [company['Name'] for company in companies]
    company_symbols = {company['Name']: company['Symbol'] for company in companies}

    selected_company = st.selectbox('Select a company', company_names)

    if st.button('Fetch Stock Data'):
        symbol = company_symbols[selected_company]
        data = get_stock_data(symbol)
        if data is not None:
            st.write(f"Displaying stock data for {selected_company} ({symbol})")

            # Plotting the closing prices
            plt.figure(figsize=(10, 5))
            plt.plot(data.index, data['close'], marker='o')
            plt.title(f"Closing Prices of {selected_company}")
            plt.xlabel('Date')
            plt.ylabel('Closing Price')
            plt.grid(True)
            st.pyplot(plt)

if __name__ == "__main__":
    main()
