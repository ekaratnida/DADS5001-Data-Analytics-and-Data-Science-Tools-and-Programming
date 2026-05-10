import os

import pymongo
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import PyMongoError

st.set_page_config(page_title="MongoDB Aggregation Examples", layout="wide")
st.title("Starbucks analysis.")

@st.cache_resource
def init_mongo_client():
    if "client" not in st.session_state:
        uri = st.secrets["mongo"]["uri"]
        st.session_state.client = MongoClient(uri)
    return st.session_state.client

def get_db():
    client = init_mongo_client()
    return client["test_db"]

def get_collection():
    db = get_db()
    return db["Starbucks"]

st.header("List Starbucks data")

try:
    starbuck = get_collection()
    ret = starbuck.find_one({'Country':'TH'})
    st.json(ret)
    #for r in ret:
    #    st.write(r)

except PyMongoError as e:
    st.error(f"Error finding document: {e}")