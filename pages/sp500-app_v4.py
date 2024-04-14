import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import streamlit.components.v1 as components

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
    #pass
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
def get_stock_data(ticker, period="1mo"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist

def main():
    st.title('S&P 500 Companies List and Stock Data')
    st.write('This app displays a list of companies in the S&P 500 and their stock closing prices.')

    companies = fetch_sp500_list()
    company_names = [company['Name'] for company in companies]
    company_symbols = {company['Name']: company['Symbol'] for company in companies}

    selected_company = st.selectbox('Select a company', company_names)

    if st.button('Fetch Stock Data'):
        symbol = company_symbols[selected_company]
        data = get_stock_data(symbol)
        st.write(f"Displaying stock data for {selected_company} ({symbol})")

        # Plotting the closing prices
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data['Close'], marker='o')
        plt.title(f"Closing Prices of {selected_company}")
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.grid(True)
        st.pyplot(plt)

if __name__ == "__main__":
    main()