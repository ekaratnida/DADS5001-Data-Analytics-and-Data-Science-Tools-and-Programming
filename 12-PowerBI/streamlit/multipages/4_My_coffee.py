import streamlit as st
import duckdb as db
import pandas as pd

st.set_page_config(
    page_title="Starbucks coffee",
    page_icon=":coffee:",
)

st.write("Starbuck analysis")
#st.sidebar.success("Select a demo above.")
@st.cache_data
def readData():
    return db.read_csv("Starbucks.csv").df()

df1 = readData() 
st.write(df1)
#x = 'Bangkok'
selectedCity = st.sidebar.selectbox('Choose your city',['Bangkok','Chiangmai','Phuket'])
results = db.sql(f"SELECT \"Store Name\" FROM df1 where City='{selectedCity}'").df()
#results2 = db.sql(f"select \"Store Name\" from results").df()
st.write(results)

st.markdown(
    """
    Exercise:
    1. Create a plotly chart from the Starbucks data.
    """
)


