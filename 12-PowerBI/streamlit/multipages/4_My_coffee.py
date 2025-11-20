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

if st.toggle("select"):

    selection = st.dataframe(
        results,
        on_select="rerun",
        selection_mode="single-cell", # Use single-cell mode
        use_container_width=True
    )

    # Check if a cell has been selected
    if selection and selection["selection"]["cells"]:
        # The selection data is a dictionary.
        # selection["selection"]["cells"] contains a list of (row, col) tuples
        for row_index, col_name in selection["selection"]["cells"]:
            # Get the value of the selected cell
            cell_value = results.iloc[row_index][col_name]
            
            # Trigger other components or logic
            st.subheader("Details for the selected cell:")
            st.write(f"Row Index: {row_index}, Column: {col_name}, Value: {cell_value}")        
    else:
        st.info("Select a cell to see the details and update the chart.")

else:
    st.write(results)

st.markdown(
    """
    Exercise:
    1. Create a plotly chart from the Starbucks data.
    """
)


