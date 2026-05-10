import os
from datetime import datetime

import bson
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import PyMongoError

st.set_page_config(page_title="MongoDB CRUD Operations", layout="wide")
st.title("MongoDB CRUD Operations")

@st.cache_resource
def init_mongo_client():
    if "client" not in st.session_state:
        uri = st.secrets["mongo"]["uri"]
        st.session_state.client = MongoClient(uri)
    return st.session_state.client

def get_db():
    client = init_mongo_client()
    return client['sample_mflix']

def get_movies_collection():
    db = get_db()
    return db['movies']

with st.sidebar:
    st.header("Configuration")
    if st.button("Reconnect to MongoDB"):
        if "client" in st.session_state:
            st.session_state.client.close()
        del st.session_state.client
        st.rerun()
    st.success("Connected to MongoDB")

st.header("1. List Databases")
try:
    client = init_mongo_client()
    databases = client.list_database_names()
    st.write("Available databases:")
    #for db_name in databases:
    #    st.text(f"  - {db_name}")
    st.table(databases)

except PyMongoError as e:
    st.error(f"Error listing databases: {e}")

st.header("2. List Collections in 'sample_mflix'")
try:
    db = get_db()
    collections = db.list_collection_names()
    st.table(collections)
    #for coll in collections:
    #    st.text(f"  - {coll}")
except PyMongoError as e:
    st.error(f"Error listing collections: {e}")

st.header("3. Find 'Blacksmith Scene' Document")
try:
    movies = get_movies_collection()
    doc = movies.find_one({'title': 'Blacksmith Scene'})
    st.info("movies.find_one({'title': 'Blacksmith Scene'}")
    if doc:
        st.json(doc, expanded=True)
    else:
        st.info("Document not found")
except PyMongoError as e:
    st.error(f"Error finding document: {e}")

st.header("4. CRUD Operations for 'Parasite'")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Insert Document")
        if st.button("Insert Parasite Document"):
            try:
                movies = get_movies_collection()
                insert_result = movies.insert_one({
                    "title": "Parasite",
                    "year": 2020,
                    "plot": "A poor family, the Kims, con their way into becoming the servants of a rich family, the Parks. "
                            "But their easy life gets complicated when their deception is threatened with exposure.",
                    "released": datetime(2020, 2, 7, 0, 0, 0),
                })
                st.session_state.parasite_id = insert_result.inserted_id
                st.success(f"Document inserted! _id: {insert_result.inserted_id}")

                doc = movies.find_one({'_id': insert_result.inserted_id})
                if doc:
                    st.write("Inserted document:")
                    st.json(doc, expanded=True)
            except PyMongoError as e:
                st.error(f"Error inserting document: {e}")

        if "parasite_id" in st.session_state:
            st.info(f"Stored _id: {st.session_state.parasite_id}")

with col2:
    with st.container(border=True):
        st.subheader("Find Document by ID")
        if "parasite_id" in st.session_state:
            if st.button("Find by Stored ID"):
                try:
                    movies = get_movies_collection()
                    doc = movies.find_one({'_id': bson.ObjectId(st.session_state.parasite_id)})
                    if doc:
                        st.json(doc, expanded=True)
                    else:
                        st.warning("Document not found")
                except PyMongoError as e:
                    st.error(f"Error finding document: {e}")
        else:
            st.info("Insert a document first")

st.subheader("Find All 'Parasite' Documents")
with st.container(border=True):
    if st.button("Find All Parasite Documents"):
        try:
            movies = get_movies_collection()
            docs = list(movies.find({"title": "Parasite"}))
            if docs:
                st.write(f"Found {len(docs)} document(s)")
                for doc in docs:
                    st.json(doc, expanded=True)
                    st.markdown("---")
            else:
                st.info("No documents found")
        except PyMongoError as e:
            st.error(f"Error finding documents: {e}")

st.subheader("Update Documents")
update_col1, update_col2, update_col3 = st.columns(3)

with update_col1:
    with st.container(border=True):
        st.write("Update by ID (Year to 2019)")
        if "parasite_id" in st.session_state:
            if st.button("Update Year to 2019"):
                try:
                    movies = get_movies_collection()
                    update_result = movies.update_one(
                        {'_id': bson.ObjectId(st.session_state.parasite_id)},
                        {'$set': {"year": 2019}}
                    )
                    st.success(f"Updated {update_result.modified_count} document(s)")

                    doc = movies.find_one({'_id': bson.ObjectId(st.session_state.parasite_id)})
                    if doc:
                        st.write("Updated document:")
                        st.json(doc, expanded=True)
                except PyMongoError as e:
                    st.error(f"Error updating document: {e}")
        else:
            st.info("Insert a document first")

with update_col2:
    with st.container(border=True):
        st.write("Update All (Year to 2019)")
        if st.button("Update All Parasite Docs"):
            try:
                movies = get_movies_collection()
                update_result = movies.update_many(
                    {"title": "Parasite"},
                    {"$set": {"year": 2019}}
                )
                st.success(f"Updated {update_result.modified_count} document(s)")

                docs = list(movies.find({"title": "Parasite"}))
                if docs:
                    st.write("Updated documents:")
                    for doc in docs:
                        st.json(doc, expanded=True)
                        st.markdown("---")
            except PyMongoError as e:
                st.error(f"Error updating documents: {e}")

with update_col3:
    with st.container(border=True):
        st.write("Update All (Reset Year to 2020)")
        if st.button("Reset Year to 2020"):
            try:
                movies = get_movies_collection()
                update_result = movies.update_many(
                    {"title": "Parasite"},
                    {"$set": {"year": 2020}}
                )
                st.success(f"Updated {update_result.modified_count} document(s)")

                docs = list(movies.find({"title": "Parasite"}))
                if docs:
                    st.write("Updated documents:")
                    for doc in docs:
                        st.json(doc, expanded=True)
                        st.markdown("---")
            except PyMongoError as e:
                st.error(f"Error updating documents: {e}")

st.subheader("Delete Documents")
delete_col1, delete_col2 = st.columns(2)

with delete_col1:
    with st.container(border=True):
        st.write("Delete All Parasite Documents")
        if st.button("Delete All Parasite Documents", type="primary"):
            try:
                movies = get_movies_collection()
                delete_result = movies.delete_many({"title": "Parasite"})
                st.success(f"Deleted {delete_result.deleted_count} document(s)")
                if "parasite_id" in st.session_state:
                    del st.session_state.parasite_id
            except PyMongoError as e:
                st.error(f"Error deleting documents: {e}")

with delete_col2:
    with st.container(border=True):
        st.write("Clear Stored ID")
        if st.button("Clear Stored ID"):
            if "parasite_id" in st.session_state:
                del st.session_state.parasite_id
                st.info("Stored ID cleared")
            else:
                st.info("No stored ID to clear")
