import streamlit as st
import streamlit.components.v1 as components
from pages.menu import menu

st.title("Webscrapping Lab")
st.set_option("client.showSidebarNavigation", False)

menu()

st.markdown("""<h3>Welcome to my Webscrapping Lab</h3>
            The  one technique I'm using is table detection. 
            Despite this is table detection, I'm using my knowledge about the table 
            related to the elements' name for example. 
            In more sophisticated trials, I will try using table autodetection. 
            Incoming in newer versions. 
            """
            , unsafe_allow_html=True
            )


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

