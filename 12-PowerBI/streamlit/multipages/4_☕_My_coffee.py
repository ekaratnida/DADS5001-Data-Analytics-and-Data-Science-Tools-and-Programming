import streamlit as st
import duckdb as db
import pandas as pd

st.set_page_config(
    page_title="Starbucks coffee",
    page_icon=":coffee:",
)

st.write("Starbuck analysis :coffee: ")
#st.sidebar.success("Select a demo above.")
@st.cache_data
def readData():
    #return db.read_csv("Starbucks.csv").df()
    return db.read_csv("https://raw.githubusercontent.com/ekaratnida/DADS5001-Data-Analytics-and-Data-Science-Tools-and-Programming/refs/heads/main/12-PowerBI/streamlit/multipages/Starbucks.csv").df()

df1 = readData()
if st.toggle("Show dataset"): 
    st.write(df1)

selectedCity = st.sidebar.selectbox('Choose your city',['Bangkok','Chiangmai','Phuket'])
results = db.sql(f"SELECT \"Store Name\" FROM df1 where City='{selectedCity}'").df()
#st.table(results)


if st.toggle("Show details of each selected row."):

    selection = st.dataframe(
        results,
        on_select="rerun",
        selection_mode="single-cell", # Use single-cell mode
        use_container_width=True,
        width="stretch"
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
            result2 = db.sql(f"SELECT * FROM df1 where \"Store Name\"='{cell_value}'").df()
            st.write(result2)
            #st.write(f"Row Index: {row_index}, Column: {col_name}, Value: {cell_value}")        
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