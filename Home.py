import streamlit as st
import streamlit.components.v1 as components


st.title("Webscrapping Lab")
st.markdown("""<h3>Welcome to my Webscrapping Lab</h3>
            The  one technique I'm using is table detection. 
            Despite this is table detection, I'm using my knowledge about the table 
            related to the elements' name for example. 
            In more sophisticated trials, I will try using table autodetection. 
            Incoming in newer versions. 
            """
            , unsafe_allow_html=True
            )

# List of pages
pages = {
    "1️⃣ Webscrap using SSL Table detection Technique": "./pages/sp500-app_v1.py",
    "2️⃣ Webscrap using HTTP Table Technique": "./pages/sp500-app_v2.py",
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
