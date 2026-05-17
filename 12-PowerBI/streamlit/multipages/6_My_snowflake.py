# streamlit_app.py

import streamlit as st

conn = st.connection("snowflake")
df = conn.query("SELECT * FROM mytable;", ttl="10m")

for row in df.itertuples():
    st.write(f"{row.NAME} has a :{row.PET}:")