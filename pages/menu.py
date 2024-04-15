import streamlit as st
import streamlit.components.v1 as components



def menu():
    st.sidebar.page_link("Home.py", label="Home")
    st.sidebar.page_link("pages/sp500-app_v1.py", label="SP 500 SSL WebScrap 1")
    #st.sidebar.markdown("This is the first version of this app, trying to access to Wikipedia using SSL.")



    st.sidebar.page_link("pages/sp500-app_v2.py", label="SP 500 SSL WebScrap 2")
    #st.sidebar.markdown("This is the second version of this app, trying to access to Wikipedia using HTTP.")



    st.sidebar.page_link("pages/sp500-app_v3.py", label="SP 500 SSL WebScrap 3")
    st.sidebar.page_link("pages/sp500-app_v4.py", label="SP 500 SSL WebScrap 4")

    with st.sidebar:

        components.html(
            """
            <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
            <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="large" data-theme="dark" data-type="HORIZONTAL" data-vanity="pedrociancaglini" data-version="v1">
            <a class="badge-base__link LI-simple-link" href="https://es.linkedin.com/in/pedrociancaglini/en?trk=profile-badge"></a></div>
            """,
        height=300,
        )