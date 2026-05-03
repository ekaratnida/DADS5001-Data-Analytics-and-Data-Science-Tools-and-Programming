# streamlit_app.py

import streamlit as st
from pymongo import MongoClient


st.title("MongoDB connection")

@st.cache_resource
def init_connection():
    uri = st.secrets["mongo"]["uri"]
    return MongoClient(uri)

client = init_connection()
st.write(client)

db = client['sample_airbnb']

# Create or access a collection
collection = db['listingsAndReviews']

#result = collection.find_one({'name':'Big, Bright & Convenient Sheung Wan'})
#st.write(result)
#result = collection.find_one({'name': 'Alice'})
for user in collection.find({
    'description': {
        '$regex': 'clean room', 
        '$options': 'i'
    }
}):
    st.write(user)
    #st.write(user["name"]+" : "+str(user["age"]))
