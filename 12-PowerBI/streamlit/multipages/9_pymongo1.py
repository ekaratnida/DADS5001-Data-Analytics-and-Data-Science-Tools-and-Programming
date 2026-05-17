# streamlit_app.py
import streamlit as st
from pymongo import MongoClient

st.title("MongoDB connection")

@st.cache_resource
def init_connection():
    uri = st.secrets["mongo"]["uri"]
    return MongoClient(uri)

client = init_connection()

db = client['sample_airbnb']

# Create or access a collection
collection = db['listingsAndReviews']

st.write("Number of data = " + str(collection.count_documents({})))
results = collection.find({}, limit = 3)

for res in results:
    st.write(res)
