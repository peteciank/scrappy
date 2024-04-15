import streamlit as st
import requests
from bs4 import BeautifulSoup
import streamlit.components.v1 as components
from pages.menu import menu

menu()
def main():
    st.title('S&P 500 Companies List')
    st.write('This app displays a list of companies in the S&P 500.')

    if st.button('Fetch S&P 500 Companies'):
        companies = fetch_sp500_list()
        st.write(f"Found {len(companies)} companies.")
        st.dataframe(companies)

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

def fetch_sp500_list():
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

if __name__ == "__main__":
    main()