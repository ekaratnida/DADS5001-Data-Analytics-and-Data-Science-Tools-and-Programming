# streamlit_app.py
# pip install st-gsheets-connection 

import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

#st.write(conn)

#df=conn.read()
#st.write(df)
df = conn.read()

# Print results.
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")