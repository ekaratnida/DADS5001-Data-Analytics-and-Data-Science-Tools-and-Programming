import os

import pymongo
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import PyMongoError

st.set_page_config(page_title="MongoDB Aggregation Examples", layout="wide")
st.title("MongoDB Aggregation Examples")

@st.cache_resource
def init_mongo_client():
    if "client" not in st.session_state:
        uri = st.secrets["mongo"]["uri"]
        st.session_state.client = MongoClient(uri)
    return st.session_state.client

def get_db():
    client = init_mongo_client()
    return client["sample_mflix"]

def get_movies_collection():
    db = get_db()
    return db["movies"]
'''
with st.sidebar:
    st.header("Configuration")
    if st.button("Reconnect to MongoDB"):
        if "client" in st.session_state:
            st.session_state.client.close()
        del st.session_state.client
        st.rerun()
    st.success("Connected to MongoDB")
'''
st.header("All Aggregation Functions Summary")
with st.container(border=True):
    st.markdown("""
    This app demonstrates the following MongoDB aggregation stages:
    - **$match**: Filter documents
    - **$sort**: Sort documents by field(s)
    - **$limit**: Limit the number of documents
    - **$lookup**: Join with another collection
    - **$addFields**: Add computed fields
    - **$group**: Group documents and compute aggregates
    - **$size**: Calculate the size of an array
    """)

st.header("0. List Collections in 'sample_mflix'")
try:
    db = get_db()
    collections = db.list_collection_names()
    st.table(collections)
    #for coll in collections:
    #    st.text(f"  - {coll}")
except PyMongoError as e:
    st.error(f"Error listing collections: {e}")

st.header("1. A Sample Movie (A Star Is Born)")
with st.container(border=True):
    pipeline = [
        {"$match": {"title": "A Star Is Born"}},
        {"$limit": 1},
    ]

    #if st.button("Code1"):
    #    st.toast(pipeline)
    st.info("Mongo cmd: " + str(pipeline))

    try:
        movies = get_movies_collection()
        results = list(movies.aggregate(pipeline))
        if results:
            for movie in results:
                st.json(movie, expanded=True)
        else:
            st.info("No document found")
    except PyMongoError as e:
        st.error(f"Error: {e}")

st.header("2. A Sample Comment")
with st.container(border=True):
    pipeline = [{"$limit": 1}]
    st.info("Mongo cmd: " + str(pipeline))
    try:
        db = get_db()
        results = list(db["comments"].aggregate(pipeline))
        if results:
            for comment in results:
                st.json(comment, expanded=True)
        else:
            st.info("No comment found")
    except PyMongoError as e:
        st.error(f"Error: {e}")

st.header("3. A Star Is Born - All Documents (Sorted by Year)")
with st.container(border=True):
    pipeline = [
        {"$match": {"title": "A Star Is Born"}},
        {"$sort": {"year": pymongo.ASCENDING}},
    ]
    st.info("Mongo cmd: " + str(pipeline))
    try:
        movies = get_movies_collection()
        results = list(movies.aggregate(pipeline))
        if results:
            st.write(f"Found {len(results)} document(s)")
            for movie in results:
                st.markdown(f"- **{movie['title']}**, {movie['cast'][0]}, {movie['year']}")
        else:
            st.info("No documents found")
    except PyMongoError as e:
        st.error(f"Error: {e}")

st.header("4. A Star Is Born - Most Recent")
with st.container(border=True):
    pipeline = [
        {"$match": {"title": "A Star Is Born"}},
        {"$sort": {"year": pymongo.DESCENDING}},
        {"$limit": 1},
    ]
    st.info("Mongo cmd: " + str(pipeline))
    try:
        movies = get_movies_collection()
        results = list(movies.aggregate(pipeline))
        if results:
            for movie in results:
                st.markdown(f"**{movie['title']}**, {movie['cast'][0]}, {movie['year']}")
                st.json(movie, expanded=True)
        else:
            st.info("No document found")
    except PyMongoError as e:
        st.error(f"Error: {e}")

st.header("5. Movies With Comments (Top 5)")
with st.container(border=True):
    limit_option = st.radio("Select document limit:", ["1000 (faster)", "No limit (slower)"], horizontal=True)
    if st.button("Run Aggregation", use_container_width=True):
        with st.spinner("Running aggregation..."):
            stage_lookup_comments = {
                "$lookup": {
                    "from": "comments",
                    "localField": "_id",
                    "foreignField": "movie_id",
                    "as": "related_comments"
                }
            }
            stage_add_comment_count = {
                "$addFields": {
                    "comment_count": {"$size": "$related_comments"}
                }
            }
            stage_match_with_comments = {
                "$match": {"comment_count": {"$gt": 2}}
            }
            limit_5 = {"$limit": 5}

            pipeline = [stage_lookup_comments, stage_add_comment_count, stage_match_with_comments, limit_5]
            st.info("Mongo cmd: " + str(pipeline))
            if limit_option == "1000 (faster)":
                pipeline.insert(0, {"$limit": 1000})

            try:
                movies = get_movies_collection()
                results = list(movies.aggregate(pipeline))
                if results:
                    for movie in results:
                        with st.expander(f"{movie['title']} ({movie['comment_count']} comments)", expanded=False):
                            st.write(f"**Comment count:** {movie['comment_count']}")
                            for comment in movie["related_comments"][:5]:
                                st.markdown(f"- **{comment['name']}:** {comment['text']}")
                else:
                    st.info("No movies found with more than 2 comments")
            except PyMongoError as e:
                st.error(f"Error: {e}")

st.header("6. Movies Grouped By Year (Before 1920)")
with st.container(border=True):
    max_year = st.slider("Max year", min_value=1900, max_value=1920, value=1920)
    if st.button("Grouped By Year", use_container_width=True):
        with st.spinner("Running aggregation..."):
            stage_group_year = {
                "$group": {
                    "_id": "$year",
                    "movie_count": {"$sum": 1},
                    "movie_titles": {"$push": "$title"},
                }
            }
            stage_match_years = {
                "$match": {
                    "_id": {"$type": "number", "$lt": max_year}
                }
            }
            stage_sort_year_ascending = {"$sort": {"_id": pymongo.ASCENDING}}

            pipeline = [stage_group_year, stage_match_years, stage_sort_year_ascending]

            st.info("Mongo cmd: " + str(pipeline))
            try:
                movies = get_movies_collection()
                results = list(movies.aggregate(pipeline))
                if results:
                    tabs = st.tabs([str(r["_id"]) for r in results])
                    for i, year_summary in enumerate(results):
                        with tabs[i]:
                            st.metric("Movie Count", year_summary["movie_count"])
                            for title in year_summary["movie_titles"]:
                                st.markdown(f"- {title}")
                else:
                    st.info("No movies found")
            except PyMongoError as e:
                st.error(f"Error: {e}")

